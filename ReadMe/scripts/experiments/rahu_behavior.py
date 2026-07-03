"""Scan ALL charts (celebrity + ordinary) for the user's Rahu rule:
Rahu mahadasha substantially LIVED in the peak (20-50) + dispositor NOT in 3/6/8/12.
Only counts charts where >=8 yrs of Rahu-dasha-in-peak have already elapsed (by 2026),
so the Rahu chapter has genuinely played out (excludes childhood-Rahu + just-started)."""
import json
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM=json.load(open("/app/src_celebrities.json",encoding="utf-8"))
ORDD=json.load(open("/app/normal_people.json",encoding="utf-8"))
NOW=2026; BAD={3,6,8,12}; MIN_ELAPSED=8

def rahu_info(p):
    b=p["birth"]
    c=build_muhurta_chart(dob=b["date"],tob=b["time"],lat=b["lat"],lon=b["lon"],with_shadbala=False)
    P=c["planets"]; by=int(b["date"][:4]); disp=SIGN_LORDS[P["Rahu"]["sign"]]; dh=P[disp]["house"]
    ra=None
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"],b["date"],b["time"])["dashas"]:
        if d["planet"]=="Rahu": ra=(int(d["start_date"][:4])-by,int(d["end_date"][:4])-by)
    prime=max(0,min(ra[1],50)-max(ra[0],20)) if ra else 0
    elapsed=max(0,min(ra[1],50,NOW-by)-max(ra[0],20)) if ra else 0
    qualify=elapsed>=MIN_ELAPSED and dh not in BAD
    return {"name":p["name"],"rahu_h":P["Rahu"]["house"],"rahu_sign":SIGN_NAMES[P["Rahu"]["sign"]],
            "ages":f"{ra[0]}-{ra[1]}" if ra else "-","prime":prime,"elapsed":elapsed,
            "disp":disp,"dh":dh,"good":dh not in BAD,"qualify":qualify}

famrows=[rahu_info(p) for p in FAM]; ordrows=[rahu_info(p) for p in ORDD]
def show(rows,label):
    q=[r for r in rows if r["qualify"]]
    print(f"\n=== {label}: {len(q)}/{len(rows)} QUALIFY ({len(q)/len(rows)*100:.0f}%) ===")
    for r in sorted(q,key=lambda x:-x["elapsed"]):
        print(f"  {r['name']:24} Rahu H{r['rahu_h']:<2} {r['rahu_sign']:11} dasha age {r['ages']:7} "
              f"prime {r['prime']:>2}y elapsed {r['elapsed']:>2}y  disp {r['disp']} H{r['dh']}")
    return len(q),len(rows)
fq,fn=show(famrows,"CELEBRITIES")
oq,on=show(ordrows,"ORDINARY")
print(f"\n>>> QUALIFY rate: celebrities {fq}/{fn}={fq/fn*100:.0f}%  vs  ordinary {oq}/{on}={oq/on*100:.0f}%  "
      f"(ratio {(fq/fn)/(oq/on):.2f}x)")
print(f">>> Of all who qualify, {fq}/{fq+oq}={fq/(fq+oq)*100:.0f}% are celebrities (base rate {fn/(fn+on)*100:.0f}%)")
