"""Era/geography-MATCHED test — kills the age confound. Winners composite (NATAL
age-free Rahu Yoga + D60 + 10th-AV + 1st-AV) for: all 140 famous vs ordinary;
famous born >=1940 (era-matched); famous born >=1940 & India-born (era+geo)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM=json.load(open("/app/src_celebrities.json",encoding="utf-8"))
ORDD=json.load(open("/app/normal_people.json",encoding="utf-8"))
_C=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
_DP={"Exalted":100,"Moolatrikona":85,"Own Sign":75,"Friendly Sign":55,"Neutral Sign":45,"Enemy Sign":25,"Debilitated":5}
_BAD={3,6,8,12}

def feats(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon,with_shadbala=False)
    P,lag=c["planets"],c["lagna"]; ls=lag["sign"]; by=int(dob[:4])
    dl=calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]
    ra=next(((int(d["start_date"][:4])-by,int(d["end_date"][:4])-by) for d in dl if d["planet"]=="Rahu"),None)
    dispf=1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    natal=max(0,min(ra[1],50)-max(ra[0],20)) if ra else 0    # age-free
    tv=c["ashtakavarga"]["totals"]; d60=calc_divisional_charts(P,lag)["D60"]
    fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    return [natal*dispf, fd60, tv[(ls+9)%12], tv[ls]]

def bd(p): return (p["birth"]["date"],p["birth"]["time"],p["birth"]["lat"],p["birth"]["lon"])
FF=np.array([feats(*bd(p)) for p in FAM]); RR=np.array([feats(*bd(p)) for p in ORDD])
fyear=np.array([int(p["birth"]["date"][:4]) for p in FAM])
find=np.array(["India" in p["birth"]["place"] for p in FAM])
oyear=np.mean([int(p["birth"]["date"][:4]) for p in ORDD])
def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))
def report(mask,label):
    Ff=FF[mask]; X=np.vstack([Ff,RR]); y=np.array([1]*len(Ff)+[0]*len(RR),float)
    np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5); cvs=np.zeros(len(y))
    for i in range(5):
        te=folds[i]; tr=np.concatenate([folds[j] for j in range(5) if j!=i])
        sg=np.sign(X[tr][y[tr]==1].mean(0)-X[tr][y[tr]==0].mean(0)); m,s=X[tr].mean(0),X[tr].std(0)+1e-9
        cvs[te]=(((X[te]-m)/s)*sg).sum(1)
    fy=fyear[mask].mean()
    print(f"  {label:34s} n_fam={len(Ff):3d}  avg_birth_yr={fy:.0f} (ord {oyear:.0f}, gap {oyear-fy:+.0f})  sum-AUC={auc(cvs,y):.3f}")
print("Winners composite (NATAL, age-free) — famous vs 96 ordinary:\n")
report(np.ones(len(FF),bool),"ALL 140 famous")
report(fyear>=1940,"era-matched (born >=1940)")
report(fyear>=1955,"era-matched (born >=1955)")
report((fyear>=1940)&find,"era + INDIA-born (born >=1940)")
report((fyear>=1955)&find,"era + INDIA-born (born >=1955)")
