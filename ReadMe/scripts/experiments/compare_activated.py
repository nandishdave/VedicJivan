"""DASHA-TIMED YOGA PEAK — the teacher's rule in code.
For each chart, take the strongest classical combination (Dhana/Prosperity/Raja
link, or a Rahu/Ketu placement) WHOSE forming planet's mahadasha fires in the prime
(20-50), and score THAT single activated combination. Does activated depth separate
famous from ordinary better than static breadth (~0.58)?  79 famous vs 96 ordinary."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score, prosperity_yoga_score
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM=json.load(open("/app/src_celebrities.json",encoding="utf-8"))
ORDD=json.load(open("/app/normal_people.json",encoding="utf-8"))

def node_hf(h):
    if h==11: return 12.0
    if h in (3,6,10): return 10.0     # upachaya — Rahu/Ketu thrive
    if h in (1,4,5,7,9): return 8.0
    if h==2: return 7.0
    return 5.0                         # 8,12

def combos(c):
    out=[]
    for f in (dhana_yoga_score, prosperity_yoga_score, raja_yoga_score):
        for lk in f(c)[1]: out.append((lk["score"], lk["planets"]))
    P=c["planets"]
    for node in ("Rahu",):   # RAHU only — Ketu dasha rarely lifts to worldly heights
        disp=SIGN_LORDS[P[node]["sign"]]; dispf=1.0 if P[disp]["house"] not in (3,6,8,12) else 0.5
        out.append((node_hf(P[node]["house"])*dispf, [node]))
    return out

def prime_dasha(c,dob,tob):
    by=int(dob[:4]); ov={}
    for d in calc_vimshottari_dasha(c["planets"]["Moon"]["longitude"],dob,tob)["dashas"]:
        o=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
        if o>0: ov[d["planet"]]=ov.get(d["planet"],0)+o
    return ov

def peaks(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon,with_shadbala=False)
    cb=combos(c); pd=prime_dasha(c,dob,tob)
    any_peak=max((s for s,_ in cb),default=0.0)
    act=[(s,max((pd.get(p,0) for p in pls),default=0)) for s,pls in cb if any(p in pd for p in pls)]
    act_peak=max((s for s,_ in act),default=0.0)
    act_peak_w=max((s*(w/18.0) for s,w in act),default=0.0)
    return any_peak,act_peak,act_peak_w

def bd(p): return (p["birth"]["date"],p["birth"]["time"],p["birth"]["lat"],p["birth"]["lon"])
Ff=np.array([peaks(*bd(p)) for p in FAM]); Rr=np.array([peaks(*bd(p)) for p in ORDD])
y=np.array([1]*len(Ff)+[0]*len(Rr),float); X=np.vstack([Ff,Rr])
def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))
LAB=["peak-any (strongest combo, NO dasha filter)",
     "PEAK activated (combo whose planet's dasha in prime)",
     "PEAK activated x dasha-years-in-prime"]
print("Does a DASHA-ACTIVATED combination separate famous from ordinary?")
print("(breadth sum-z baseline was 0.581)\n")
for i,l in enumerate(LAB):
    print(f"  {l:52s} famous {Ff[:,i].mean():5.1f} vs ord {Rr[:,i].mean():5.1f}   AUC={auc(X[:,i],y):.3f}")
for nm in ("Mahendra Singh Dhoni","Virat Kohli","Albert Einstein"):
    p=[x for x in FAM if x["name"]==nm][0]; v=peaks(*bd(p))
    print(f"  [check] {nm:22s} activated-peak={v[1]:.1f}  weighted={v[2]:.1f}")
