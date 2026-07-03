"""Rahu hypothesis v2: 'Rahu's dispositor NOT in 3/6/8/12 + Rahu dasha in prime (20-50)'.
Base rate in 79 famous vs 96 ordinary."""
import json
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM=json.load(open("/app/src_celebrities.json",encoding="utf-8"))
ORDD=json.load(open("/app/normal_people.json",encoding="utf-8"))
BAD={3,6,8,12}

def flags(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon,with_shadbala=False); P=c["planets"]
    disp=SIGN_LORDS[P["Rahu"]["sign"]]; dh=P[disp]["house"]
    by=int(dob[:4]); ov=0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]:
        if d["planet"]=="Rahu":
            ov=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
    return (dh not in BAD, dh==1, ov>0, ov)

def analyze(data,label):
    n=len(data); good=one=dp=comb=comb1=0; ovs=0
    for p in data:
        b=p["birth"]; g,o1,dpr,ov=flags(b["date"],b["time"],b["lat"],b["lon"])
        good+=g; one+=o1; dp+=dpr; ovs+=ov; comb+=(g and dpr); comb1+=(o1 and dpr)
    print(f"{label} (n={n})")
    print(f"  Rahu dispositor NOT in 3/6/8/12         {good/n*100:4.0f}%  ({good}/{n})")
    print(f"  Rahu dispositor in 1st house            {one/n*100:4.0f}%  ({one}/{n})")
    print(f"  Rahu dasha overlaps prime (20-50)       {dp/n*100:4.0f}%  ({dp}/{n})  avg {ovs/n:.1f} yrs")
    print(f"  COMBINED: (NOT 3/6/8/12) + dasha-prime  {comb/n*100:4.0f}%  ({comb}/{n})")
    print(f"  STRICT:   1st-house + dasha-prime        {comb1/n*100:4.0f}%  ({comb1}/{n})")
    return {"good":good/n,"one":one/n,"dp":dp/n,"comb":comb/n,"comb1":comb1/n}

print("=== RAHU HYPOTHESIS v2: dispositor NOT in 3/6/8/12 + Rahu dasha in prime ===\n")
f=analyze(FAM,"FAMOUS"); print(); o=analyze(ORDD,"ORDINARY")
def lift(k):
    r=f[k]/o[k] if o[k] else float('inf')
    return f"{(f[k]-o[k])*100:+4.0f} pts   (famous {f[k]*100:.0f}% vs ordinary {o[k]*100:.0f}%,  {r:.2f}x)"
print("\nLIFT (famous vs ordinary):")
print(f"  dispositor NOT in 3/6/8/12   {lift('good')}")
print(f"  dispositor in 1st            {lift('one')}")
print(f"  Rahu dasha in prime          {lift('dp')}")
print(f"  COMBINED (NOT 3/6/8/12 +prime) {lift('comb')}")
print(f"  STRICT (1st + prime)         {lift('comb1')}")
for nm in ("Mahendra Singh Dhoni","Virat Kohli"):
    p=[x for x in FAM if x["name"]==nm][0]; b=p["birth"]
    g,o1,dpr,ov=flags(b["date"],b["time"],b["lat"],b["lon"])
    print(f"  [check] {nm}: disp_not_dusthana={g} disp_1st={o1} dasha_prime={dpr} ({ov} yrs)")
