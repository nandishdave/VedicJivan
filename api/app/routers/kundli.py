"""Public endpoint for free Kundli report generation.

The endpoint inserts a `pending` record + enqueues an SQS message for the
out-of-process Lambda worker to pick up, then returns 202 Accepted. The
Lambda runs the chart calculation, PDF rendering, and email delivery,
and writes the final state back to the same record.

This pattern replaced the original FastAPI BackgroundTask approach
because PDF generation on Playwright takes ~10-30 s per render and was
starving the API event loop on a 0.25 vCPU Fargate task.

This module is intentionally thin — every business rule (rate limit,
"what counts as enabled and free", error persistence) lives in
`app/use_cases/kundli.py`.
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, Response

from app.dependencies import get_kundli_repository, get_message_queue
from app.infrastructure.logging import get_logger
from app.infrastructure.queue import MessageQueue
from app.models.kundli import KundliRequest
# These imports are kept at module scope on purpose: tests patch them as
# `app.routers.kundli.build_chart` / `generate_pdf` / `load_report_sections`,
# and the render use case below resolves them lazily through this module's
# globals.
from app.repositories.kundli_repository import KundliRepository
from app.services.kundli_calculator import build_chart
from app.services.kundli_calculator.vimsopaka import compute_vimsopaka
from app.services.kundli_pdf import generate_pdf
from app.services.report_sections import load_report_sections
from app.use_cases.kundli import (
    QueueKundliGeneration,
    RenderKundliReport,
)

logger = get_logger(__name__)

router = APIRouter(prefix="/api/kundli", tags=["Kundli"])


# ── Use-case factories ────────────────────────────────────────────────────


def _queue_kundli_use_case(
    repo: KundliRepository = Depends(get_kundli_repository),
) -> QueueKundliGeneration:
    return QueueKundliGeneration(repo)


def _render_use_case() -> RenderKundliReport:
    # Construct fresh each call so mock.patch on the module globals here
    # (build_chart / generate_pdf / load_report_sections) is honoured.
    return RenderKundliReport(
        build_chart=build_chart,
        generate_pdf=generate_pdf,
        load_report_sections=load_report_sections,
    )


# ── Endpoints ────────────────────────────────────────────────────────────


@router.post("/generate", status_code=202)
async def generate_kundli(
    req: KundliRequest,
    use_case: QueueKundliGeneration = Depends(_queue_kundli_use_case),
    queue: MessageQueue = Depends(get_message_queue),
):
    """Queue a Kundli report for generation.

    Inserts a `pending` row + enqueues to SQS, then returns 202. The
    Lambda worker picks up the message, renders the PDF, and emails it.
    The user receives the report by email when it's ready (typically
    under a minute).
    """
    record_id = await use_case.execute(req)

    # If SQS enqueue fails, the pending row stays in Mongo — its TTL
    # (set inside QueueKundliGeneration) reaps it within 24 h. We
    # surface a 500 to the caller so they know to retry rather than
    # silently dropping the request.
    try:
        await queue.send({"record_id": str(record_id), **req.model_dump()})
    except Exception:
        logger.exception(
            "Failed to enqueue kundli generation for record_id=%s", record_id
        )
        raise HTTPException(
            status_code=500,
            detail="Could not queue your kundli report. Please try again.",
        )

    return {
        "message": (
            "Your Kundli report is being generated and will arrive in your "
            "email within a minute."
        )
    }


@router.get("/preview")
async def preview_kundli(
    name: str = Query("Nandish Dave"),
    gender: str = Query("male"),
    dob: str = Query("1988-11-11"),
    tob: str = Query("12:55"),
    lat: float = Query(21.7333),
    lon: float = Query(70.6167),
    place_name: str = Query("Jetpur, Gujarat, India"),
    timezone: str = Query("Asia/Kolkata"),
):
    """Instant PDF preview — returns the PDF directly in the browser.

    No email, no background task, no rate limit, no DB write. Designed for
    fast layout iteration during development. Bookmark the URL and refresh
    after each deploy to see changes immediately.

    **Disabled in production.** Only works when APP_ENV is not "production".
    """
    if os.environ.get("APP_ENV", "").lower() == "production":
        raise HTTPException(status_code=404, detail="Not found")

    try:
        _, pdf_bytes = await _render_use_case().execute(
            name=name,
            gender=gender,
            dob=dob,
            tob=tob,
            lat=lat,
            lon=lon,
            place_name=place_name,
            timezone=timezone,
        )
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f"inline; filename=Kundli_Preview_{name.replace(' ', '_')}.pdf"
                )
            },
        )
    except Exception as e:
        logger.exception("Kundli preview failed")
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)[:200]}")


@router.get("/vimsopaka")
async def vimsopaka(
    dob: str = Query(..., description="Birth date YYYY-MM-DD"),
    tob: str = Query("12:00", description="Birth time HH:MM (24h)"),
    lat: float = Query(..., description="Birth latitude"),
    lon: float = Query(..., description="Birth longitude"),
    detail: bool = Query(False, description="Include the per-varga breakdown"),
):
    """Per-planet Vimśopaka Bala (0-20) for a birth moment.

    Read-only, no DB write. Returns each classical planet's cross-divisional
    strength across the 16 Shodashavarga charts, its interpretation band, and the
    single strongest planet + whether it sits in a prominence seat (1/2/4/5/11 —
    factor 16 of the worldly-potential model). Pass ``detail=true`` for the
    per-varga dignity breakdown.
    """
    try:
        report = compute_vimsopaka(dob, tob, lat, lon)
    except Exception as e:
        logger.exception("Vimsopaka calculation failed")
        raise HTTPException(status_code=422, detail=f"Could not compute: {str(e)[:200]}")
    if not detail:
        for p in report["planets"].values():
            p.pop("vargas", None)
    return report


@router.get("/vimsopaka/page", response_class=HTMLResponse)
async def vimsopaka_page():
    """A tiny self-contained calculator page for the Vimśopaka endpoint.

    Enter a birth date/time and coordinates (a few city presets provided) and it
    calls ``/api/kundli/vimsopaka`` and renders the per-planet table. Same-origin,
    no build step — bookmark on the test environment.
    """
    return HTMLResponse(_VIMSOPAKA_PAGE)


_VIMSOPAKA_PAGE = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vimśopaka Bala Calculator — VedicJivan</title>
<style>
 :root{--accent:#6d3a9e;--ink:#221a2e;--muted:#6b6478;--line:#e7e2f0;--panel:#fff;--bg:#f7f5fb;
   --g:#1f6b45;--gb:#dcf0e2;--m:#8a5a12;--mb:#fbeecc;--w:#a03443;--wb:#f7dfe2;}
 *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--ink);
   font:15px/1.55 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;font-variant-numeric:tabular-nums}
 .wrap{max-width:820px;margin:0 auto;padding:34px 20px 80px}
 h1{font-size:clamp(26px,4vw,40px);margin:0 0 6px;letter-spacing:-.01em}
 h1 em{color:var(--accent);font-style:italic}
 .sub{color:var(--muted);margin:0 0 22px;max-width:60ch}
 form{display:flex;flex-wrap:wrap;gap:10px;align-items:end;background:var(--panel);
   border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:14px}
 label{display:flex;flex-direction:column;font-size:12px;color:var(--muted);gap:4px}
 input{padding:8px 10px;border:1px solid var(--line);border-radius:8px;font:14px inherit;background:#fff;color:var(--ink)}
 input[type=date]{min-width:150px} input[type=time]{min-width:110px} input.coord{width:110px}
 button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:10px 18px;font:600 14px inherit;cursor:pointer}
 button:hover{background:#7c46b0}
 .presets{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 20px;font-size:12px;color:var(--muted);align-items:center}
 .presets button{background:#efe7f6;color:var(--accent);padding:4px 10px;font-weight:600}
 .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:14px}
 table{border-collapse:separate;border-spacing:0;width:100%;font-size:14px}
 th,td{padding:8px 8px;text-align:center;border-top:1px solid var(--line)}
 th{background:var(--accent);color:#fff;font-weight:600;font-size:12.5px}
 th:first-child,td:first-child{text-align:left}
 thead th:first-child{border-top-left-radius:8px} thead th:last-child{border-top-right-radius:8px}
 .bar{position:relative;display:inline-block;width:80px;height:14px;border-radius:4px;background:#efeaf5;vertical-align:middle;margin-left:8px;overflow:hidden}
 .bar>span{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,#b493d6,#6d3a9e)}
 .b{display:inline-block;font-size:11px;font-weight:700;border-radius:5px;padding:2px 7px}
 .b.vs{background:var(--gb);color:var(--g)} .b.ms{background:var(--gb);color:var(--g)}
 .b.wk{background:var(--mb);color:var(--m)} .b.vw{background:var(--wb);color:var(--w)}
 .hl{background:#f3ecfa}
 .note{font-size:12.5px;color:var(--muted);line-height:1.5;margin-top:10px}
 .err{color:var(--w);font-size:13px}
 code{background:#efe7f6;border-radius:4px;padding:1px 5px;font-size:12.5px}
</style></head><body><div class="wrap">
<h1>Vimśopaka <em>Bala</em> Calculator</h1>
<p class="sub">Per-planet cross-divisional strength (0–20) across the sixteen Shodashavarga charts.
Enter a birth moment; the strongest planet's seat (1/2/4/5/11) is highlighted — that's factor 16 of the worldly-potential model.</p>
<form id="f">
 <label>Date<input type="date" id="dob" value="1988-11-11" required></label>
 <label>Time<input type="time" id="tob" value="12:55" required></label>
 <label>Latitude<input class="coord" type="number" step="0.0001" id="lat" value="21.7333" required></label>
 <label>Longitude<input class="coord" type="number" step="0.0001" id="lon" value="70.6167" required></label>
 <button type="submit">Calculate</button>
</form>
<div class="presets"><span>Quick city:</span>
 <button data-lat="28.6139" data-lon="77.2090">Delhi</button>
 <button data-lat="19.0760" data-lon="72.8777">Mumbai</button>
 <button data-lat="13.0827" data-lon="80.2707">Chennai</button>
 <button data-lat="22.5726" data-lon="88.3639">Kolkata</button>
 <button data-lat="21.7333" data-lon="70.6167">Jetpur</button>
</div>
<div id="out"></div>
<script>
const BAND={"Very strong":"vs","Moderately strong":"ms","Weak":"wk","Very weak":"vw"};
const f=document.getElementById("f"), out=document.getElementById("out");
document.querySelectorAll(".presets button").forEach(b=>b.onclick=e=>{
  e.preventDefault(); document.getElementById("lat").value=b.dataset.lat; document.getElementById("lon").value=b.dataset.lon;});
f.onsubmit=async e=>{
  e.preventDefault(); out.innerHTML='<div class="card">Calculating…</div>';
  const q=new URLSearchParams({dob:dob.value,tob:tob.value,lat:lat.value,lon:lon.value});
  try{
    const r=await fetch("/api/kundli/vimsopaka?"+q); if(!r.ok) throw new Error((await r.json()).detail||r.status);
    const d=await r.json();
    const order=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"];
    let rows=order.map(p=>{const x=d.planets[p]; const hl=(p===d.strongest.planet)?' class="hl"':'';
      const bar=`<span class="bar"><span style="width:${Math.min(100,x.vimsopaka/20*100)}%"></span></span>`;
      return `<tr${hl}><td>${p}${p===d.strongest.planet?' ★':''}</td><td>${x.sign}</td><td>${x.house}</td>`+
        `<td><b>${x.vimsopaka.toFixed(2)}</b>${bar}</td><td><span class="b ${BAND[x.band]}">${x.band}</span></td></tr>`;}).join("");
    const seat=d.strongest.in_prominence_seat;
    out.innerHTML=`<div class="card"><table><thead><tr><th>Planet</th><th>Sign</th><th>House</th><th>Vimśopaka /20</th><th>Strength</th></tr></thead><tbody>${rows}</tbody></table>
      <p class="note">Lagna <b>${d.lagna}</b> · chart average <b>${d.average.toFixed(2)}</b>/20.
      Strongest planet: <b>${d.strongest.planet}</b> (${d.strongest.vimsopaka.toFixed(2)}) in house ${d.strongest.house} —
      ${seat?'<b style="color:var(--g)">in a prominence seat (1/2/4/5/11)</b> ✓ (factor 16 active).':'not in a prominence seat (1/2/4/5/11).'}</p>
      <p class="note">Band (per planet): 15–20 very strong · 10–15 moderately strong · 5–10 weak · below 5 very weak.
      Add <code>&detail=true</code> to the API URL for the per-varga breakdown.</p></div>`;
  }catch(err){out.innerHTML=`<div class="card err">Could not compute: ${err.message}. Check the date/time/coordinates.</div>`;}
};
f.requestSubmit?f.requestSubmit():f.dispatchEvent(new Event("submit"));
</script></div></body></html>"""
