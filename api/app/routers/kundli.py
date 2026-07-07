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
from fastapi.concurrency import run_in_threadpool
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
from app.services.kundli_calculator.argala import argala_analysis
from app.services.kundli_calculator.ashtakavarga import ashtakavarga_table
from app.services.kundli_calculator.degree_calculator import degree_analysis
from app.services.kundli_calculator.divisional import divisional_table
from app.services.kundli_calculator.shadbala import shadbala_table
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
    except Exception:
        logger.exception("Kundli preview failed")
        raise HTTPException(status_code=500, detail="Preview failed. Please try again.")


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
        # compute_vimsopaka is CPU-heavy (16 divisional charts); run it off the
        # event loop so it doesn't stall the 0.25-vCPU async worker under load.
        report = await run_in_threadpool(compute_vimsopaka, dob, tob, lat, lon)
    except Exception:
        logger.exception("Vimsopaka calculation failed")
        raise HTTPException(
            status_code=422,
            detail="Could not compute for these birth details. Please check the inputs.",
        )
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


@router.get("/divisional-charts")
async def divisional_charts_endpoint(
    dob: str = Query(..., description="Birth date YYYY-MM-DD"),
    tob: str = Query("12:00", description="Birth time HH:MM (24h)"),
    lat: float = Query(..., description="Birth latitude"),
    lon: float = Query(..., description="Birth longitude"),
    upagrahas: bool = Query(False, description="Also fold the 11 upagrahas into every varga"),
):
    """Each body's sign across the divisional charts (D1 Rāśi … D60 Ṣaṣṭyāṁśa) —
    the Ascendant + 9 grahas + 3 outer planets. When ``upagrahas=true`` the 11
    sub-planets are added to every varga too. Read-only, no DB write."""
    from app.services.muhurta import build_muhurta_chart

    def _compute():
        # Divisionals don't need Shadbala — skip it (much faster).
        chart = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False)
        ups = None
        if upagrahas:
            from app.services.kundli_calculator._core import get_julian_day
            from app.services.kundli_calculator.upagraha import calc_upagrahas
            jd = get_julian_day(dob, tob, lat, lon)
            ups = calc_upagrahas(jd, dob, lat, lon, chart["planets"]["Sun"]["longitude"])
        return divisional_table(chart["planets"], chart["lagna"], upagrahas=ups)

    try:
        return await run_in_threadpool(_compute)
    except Exception:
        logger.exception("divisional-charts failed")
        raise HTTPException(
            status_code=422,
            detail="Could not compute for these birth details. Please check the inputs.",
        )


@router.get("/shadbala")
async def shadbala_endpoint(
    dob: str = Query(..., description="Birth date YYYY-MM-DD"),
    tob: str = Query("12:00", description="Birth time HH:MM (24h)"),
    lat: float = Query(..., description="Birth latitude"),
    lon: float = Query(..., description="Birth longitude"),
):
    """Shadbala (six-fold planetary strength) for a birth moment: Sthana, Dig,
    Kala, Cheshta, Naisargika and Drik bala per body (in Rupas), the total vs
    the classical minimum requirement, and the ratio. Covers the 7 classical
    planets, the 3 outer planets, and Rahu/Ketu (dispositor method — scored as
    the sign-lord in its own sign at the node's house). Read-only, no DB write."""
    from app.services.muhurta import build_muhurta_chart
    from app.services.kundli_calculator._core import get_julian_day
    from app.services.kundli_calculator.shadbala import dispositor_shadbala

    def _compute():
        chart = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=True)
        # Rahu/Ketu via the dispositor method (extra shadbala runs, CPU-bound).
        jd = get_julian_day(dob, tob, lat, lon)
        sun_sunset = {"sunrise": chart.get("sunrise"), "sunset": chart.get("sunset")}
        sb = dict(chart["shadbala"])
        node_via = {}
        for node in ("Rahu", "Ketu"):
            lord, row = dispositor_shadbala(
                chart["planets"], chart["lagna"], jd, dob, tob, node, sun_sunset
            )
            sb[node] = row
            node_via[node] = lord
        return shadbala_table({**chart, "shadbala": sb}, node_via=node_via)

    try:
        return await run_in_threadpool(_compute)
    except Exception:
        logger.exception("shadbala failed")
        raise HTTPException(
            status_code=422,
            detail="Could not compute for these birth details. Please check the inputs.",
        )


@router.get("/ashtakavarga")
async def ashtakavarga_endpoint(
    dob: str = Query(..., description="Birth date YYYY-MM-DD"),
    tob: str = Query("12:00", description="Birth time HH:MM (24h)"),
    lat: float = Query(..., description="Birth latitude"),
    lon: float = Query(..., description="Birth longitude"),
):
    """Ashtakavarga for a birth moment: Sarvashtakavarga (total bindus per house,
    baseline 28) and each planet's Bhinnashtakavarga (bindus per house, 0-8).
    Read-only, no DB write."""
    from app.services.muhurta import build_muhurta_chart
    try:
        # Ashtakavarga doesn't need Shadbala — skip it (much faster).
        chart = await run_in_threadpool(
            build_muhurta_chart, dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False
        )
        return ashtakavarga_table(chart)
    except Exception:
        logger.exception("ashtakavarga failed")
        raise HTTPException(
            status_code=422,
            detail="Could not compute for these birth details. Please check the inputs.",
        )


@router.get("/degree-analysis")
async def degree_analysis_endpoint(
    dob: str = Query(..., description="Birth date YYYY-MM-DD"),
    tob: str = Query("12:00", description="Birth time HH:MM (24h)"),
    lat: float = Query(..., description="Birth latitude"),
    lon: float = Query(..., description="Birth longitude"),
):
    """Per-body auspicious/poison degree analysis for a birth moment — Pushkara
    Navāṁśa & Bhāga (auspicious) and Vish Navāṁśa & Mṛtyu Bhāga (poison) for the 9
    grahas + Uranus/Neptune/Pluto + the Ascendant. Read-only, no DB write. Mṛtyu
    Bhāga is null for the outer planets (no classical table)."""
    from app.services.muhurta import build_muhurta_chart
    try:
        # CPU-bound ephemeris build — off the event loop.
        chart = await run_in_threadpool(
            build_muhurta_chart, dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False
        )
        return degree_analysis(chart)
    except Exception:
        logger.exception("degree-analysis failed")
        raise HTTPException(
            status_code=422,
            detail="Could not compute for these birth details. Please check the inputs.",
        )


@router.get("/argala-analysis")
async def argala_analysis_endpoint(
    dob: str = Query(..., description="Birth date YYYY-MM-DD"),
    tob: str = Query("12:00", description="Birth time HH:MM (24h)"),
    lat: float = Query(..., description="Birth latitude"),
    lon: float = Query(..., description="Birth longitude"),
):
    """Per-house Argala (Jaimini intervention) quality table for a birth moment.
    For each of the 12 houses: a signed strength % that weighs each intervener's
    dignity toward the house, its natural-nature/house-type fit, and its Shadbala
    (green = net-helpful, red = net-harmful), plus a per-planet breakdown. Only
    argalas that outweigh their virodha counter are counted. Read-only, no DB
    write."""
    from app.services.muhurta import build_muhurta_chart
    try:
        # Shadbala is needed for the weighting — CPU-bound, off the event loop.
        chart = await run_in_threadpool(
            build_muhurta_chart, dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=True
        )
        return argala_analysis(chart)
    except Exception:
        logger.exception("argala-analysis failed")
        raise HTTPException(
            status_code=422,
            detail="Could not compute for these birth details. Please check the inputs.",
        )


@router.get("/upagraha")
async def upagraha_endpoint(
    dob: str = Query(..., description="Birth date YYYY-MM-DD"),
    tob: str = Query("12:00", description="Birth time HH:MM (24h)"),
    lat: float = Query(..., description="Birth latitude"),
    lon: float = Query(..., description="Birth longitude"),
):
    """The 11 upagrahas (sub-planets): 5 Sun-derived (Dhūma, Vyatīpāta, Parivesha,
    Indrachāpa, Upaketu) + 6 time-based (Kāla, Mṛtyu, Arthaprahāra, Yamaghaṇṭaka,
    Māndi, Gulika), each with sign / longitude / nakṣatra / pada, plus a per-sign
    grouping for the North-Indian chart and the lagna sign. Read-only, no DB write."""
    from app.services.muhurta import build_muhurta_chart
    from app.services.kundli_calculator._core import get_julian_day
    from app.services.kundli_calculator.upagraha import upagraha_table

    def _compute():
        chart = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False)
        jd = get_julian_day(dob, tob, lat, lon)
        return upagraha_table(
            jd, dob, lat, lon, chart["planets"]["Sun"]["longitude"], chart["lagna"]["sign"]
        )

    try:
        return await run_in_threadpool(_compute)
    except Exception:
        logger.exception("upagraha failed")
        raise HTTPException(
            status_code=422,
            detail="Could not compute for these birth details. Please check the inputs.",
        )


@router.get("/matching")
async def matching_endpoint(
    boy_dob: str = Query(..., description="Boy birth date YYYY-MM-DD"),
    boy_tob: str = Query("12:00", description="Boy birth time HH:MM"),
    boy_lat: float = Query(..., description="Boy birth latitude"),
    boy_lon: float = Query(..., description="Boy birth longitude"),
    girl_dob: str = Query(..., description="Girl birth date YYYY-MM-DD"),
    girl_tob: str = Query("12:00", description="Girl birth time HH:MM"),
    girl_lat: float = Query(..., description="Girl birth latitude"),
    girl_lon: float = Query(..., description="Girl birth longitude"),
):
    """Ashtakoota (Guna Milap) horoscope matching for two people: the 8 kootas
    (Varna…Nadi, max 36) with per-koota points + interpretation, the total,
    each partner's Mangal-Dosha grade (No/Low/High) and the overall verdict.
    Read-only, no DB write."""
    from app.services.muhurta import build_muhurta_chart
    from app.services.kundli_calculator.matching import compute_matching

    def _compute():
        boy = build_muhurta_chart(dob=boy_dob, tob=boy_tob, lat=boy_lat, lon=boy_lon, with_shadbala=False)
        girl = build_muhurta_chart(dob=girl_dob, tob=girl_tob, lat=girl_lat, lon=girl_lon, with_shadbala=False)
        return compute_matching(boy, girl)

    try:
        return await run_in_threadpool(_compute)
    except Exception:
        logger.exception("matching failed")
        raise HTTPException(
            status_code=422,
            detail="Could not compute for these birth details. Please check the inputs.",
        )


@router.get("/degree-analysis/page", response_class=HTMLResponse)
async def degree_analysis_page():
    """Self-contained calculator page for the degree-analysis endpoint — enter a
    birth moment and see each body's Pushkara/Vish Navāṁśa + Pushkara/Mṛtyu Bhāga."""
    return HTMLResponse(_DEGREE_PAGE)


_DEGREE_PAGE = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auspicious &amp; Poison Degrees — VedicJivan</title>
<style>
 :root{--accent:#6d3a9e;--ink:#221a2e;--muted:#6b6478;--line:#e7e2f0;--panel:#fff;--bg:#f7f5fb;
   --good:#1f6b45;--good-bg:#dcf0e2;--bad:#a03443;--bad-bg:#f7dfe2;--none:#b9b3c4;}
 *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--ink);
   font:15px/1.55 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;font-variant-numeric:tabular-nums}
 .wrap{max-width:900px;margin:0 auto;padding:34px 20px 80px}
 h1{font-size:clamp(24px,4vw,36px);margin:0 0 6px;letter-spacing:-.01em}
 h1 em{color:var(--accent);font-style:italic}
 .sub{color:var(--muted);margin:0 0 22px;max-width:66ch}
 form{display:flex;flex-wrap:wrap;gap:10px;align-items:end;background:var(--panel);
   border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:14px}
 label{display:flex;flex-direction:column;font-size:12px;color:var(--muted);gap:4px}
 input{padding:8px 10px;border:1px solid var(--line);border-radius:8px;font:14px inherit;background:#fff;color:var(--ink)}
 input.coord{width:110px}
 button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:10px 18px;font:600 14px inherit;cursor:pointer}
 button:hover{background:#7c46b0}
 .presets{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 20px;font-size:12px;color:var(--muted);align-items:center}
 .presets button{background:#efe7f6;color:var(--accent);padding:4px 10px;font-weight:600}
 .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:14px;overflow-x:auto}
 table{border-collapse:separate;border-spacing:0;width:100%;font-size:13.5px;min-width:640px}
 th,td{padding:7px 8px;text-align:center;border-top:1px solid var(--line)}
 th{background:var(--accent);color:#fff;font-weight:600;font-size:12px}
 th:first-child,td:first-child{text-align:left;white-space:nowrap}
 thead th:first-child{border-top-left-radius:8px} thead th:last-child{border-top-right-radius:8px}
 .b{display:inline-block;font-size:12px;font-weight:700;border-radius:6px;padding:2px 9px;min-width:26px}
 .yes-good{background:var(--good-bg);color:var(--good)} .yes-bad{background:var(--bad-bg);color:var(--bad)}
 .no{color:var(--none)} .na{color:var(--none);font-style:italic}
 .asc td{background:#f3ecfa}
 .tot{font-weight:700}
 .note{font-size:12.5px;color:var(--muted);line-height:1.55;margin-top:12px}
 .err{color:var(--bad);font-size:13px}
 code{background:#efe7f6;border-radius:4px;padding:1px 5px;font-size:12.5px}
</style></head><body><div class="wrap">
<h1>Auspicious &amp; <em>Poison</em> Degrees</h1>
<p class="sub">For a birth moment, each of the 9 grahas + the three outer planets + the Ascendant is checked against four
classical degree categories &mdash; <b style="color:var(--good)">Pushkara Navāṁśa</b> &amp; <b style="color:var(--good)">Pushkara Bhāga</b>
(auspicious) and <b style="color:var(--bad)">Vish Navāṁśa</b> &amp; <b style="color:var(--bad)">Mṛtyu Bhāga</b> (poison).</p>
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
const f=document.getElementById("f"), out=document.getElementById("out");
document.querySelectorAll(".presets button").forEach(b=>b.onclick=e=>{
  e.preventDefault(); lat.value=b.dataset.lat; lon.value=b.dataset.lon;});
function goodCell(v){return v?'<span class="b yes-good">Yes</span>':'<span class="b no">&ndash;</span>';}
function badCell(v){if(v===null||v===undefined)return '<span class="na">n/a</span>';
  return v?'<span class="b yes-bad">Yes</span>':'<span class="b no">&ndash;</span>';}
f.onsubmit=async e=>{
  e.preventDefault(); out.innerHTML='<div class="card">Calculating…</div>';
  const q=new URLSearchParams({dob:dob.value,tob:tob.value,lat:lat.value,lon:lon.value});
  try{
    const r=await fetch("/api/kundli/degree-analysis?"+q); if(!r.ok) throw new Error((await r.json()).detail||r.status);
    const d=await r.json();
    let rows=d.bodies.map(x=>`<tr class="${x.body==='Ascendant'?'asc':''}"><td>${x.body}</td><td>${x.sign}</td>`+
      `<td>${x.degree.toFixed(2)}&deg;</td><td>${x.navamsa}</td>`+
      `<td>${goodCell(x.pushkara_navamsa)}</td><td>${goodCell(x.pushkara_bhaga)}</td>`+
      `<td>${badCell(x.vish_navamsa)}</td><td>${badCell(x.mrityu_bhaga)}</td></tr>`).join("");
    const t=d.totals;
    out.innerHTML=`<div class="card"><table>
      <thead><tr><th>Body</th><th>Sign</th><th>Degree</th><th>Navāṁśa</th>
      <th>Pushkara<br>Navāṁśa</th><th>Pushkara<br>Bhāga</th><th>Vish<br>Navāṁśa</th><th>Mṛtyu<br>Bhāga</th></tr></thead>
      <tbody>${rows}</tbody>
      <tfoot><tr class="tot"><td colspan="4" style="text-align:right">Totals</td>
        <td style="color:var(--good)">${t.pushkara_navamsa}</td><td style="color:var(--good)">${t.pushkara_bhaga}</td>
        <td style="color:var(--bad)">${t.vish_navamsa}</td><td style="color:var(--bad)">${t.mrityu_bhaga}</td></tr></tfoot>
      </table>
      <p class="note"><b style="color:var(--good)">Auspicious:</b> Pushkara Navāṁśa (2 nourishing navamsas per sign, by element) ·
      Pushkara Bhāga (one auspicious degree per sign, &plusmn;1&deg;). <b style="color:var(--bad)">Poison:</b> Vish Navāṁśa
      (the poison navamsa per sign) · Mṛtyu Bhāga (the fatal degree per body per sign, &plusmn;1&deg;). Mṛtyu Bhāga has no
      classical table for the outer planets (shown <span class="na">n/a</span>). Vish Navāṁśa + Mṛtyu Bhāga are factor 18 of
      the worldly-potential model (fewer poison degrees leans famous); the Pushkara pair are shown for completeness (tested
      as fame-noise). Guidance only &mdash; consult an astrologer.</p></div>`;
  }catch(err){out.innerHTML=`<div class="card err">Could not compute: ${err.message}. Check the date/time/coordinates.</div>`;}
};
f.requestSubmit?f.requestSubmit():f.dispatchEvent(new Event("submit"));
</script></div></body></html>"""
