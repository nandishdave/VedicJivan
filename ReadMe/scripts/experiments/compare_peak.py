"""PEAK vs BREADTH: does the single strongest combination separate famous from
ordinary better than the count-of-many? Tests the classical 'one yoga + dasha'
principle against the composite count. 79 famous vs 96 ordinary."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score, prosperity_yoga_score
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM=json.load(open("/app/src_celebrities.json",encoding="utf-8"))
ORDD=json.load(open("/app/normal_people.json",encoding="utf-8"))
_C=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
KT={1,4,5,7,9,10}; CAMP_A={9,10,6,1,2,5}; FB_A={"Saturn","Venus","Mercury"}; FB_B={"Sun","Moon","Mars","Jupiter"}
_DP={"Exalted":100,"Moolatrikona":85,"Own Sign":75,"Friendly Sign":55,"Neutral Sign":45,"Enemy Sign":25,"Debilitated":5}
_BAD={3,6,8,12}
FEAT=["dasha","dhana","prosperity","raja","func_ben","av_1st","av_10th","d60"]

def feats(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon); P,lag,sb=c["planets"],c["lagna"],c["shadbala"]; ls=lag["sign"]
    def L(h): return SIGN_LORDS[(ls+h-1)%12]
    fb=FB_A if ls in CAMP_A else FB_B
    def ds(pl):
        if pl in ("Rahu","Ketu"):
            disp=SIGN_LORDS[P[pl]["sign"]]; base=min(sb.get(disp,{}).get("ratio",1.0)/1.5,1.0)*100
            ben=disp in fb or disp==L(1); good=P[disp]["house"] not in _BAD
            return min(base*(1.15 if (ben and good) else 0.95 if ben else 0.85 if good else 0.65),100)
        s=min(sb.get(pl,{}).get("ratio",1.0)/1.5,1.0)*100
        if pl in fb or pl==L(1): s=min(s*1.15,100)
        return s
    by=int(dob[:4]); acc=tot=0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]:
        ov=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
        if ov<=0: continue
        acc+=ds(d["planet"])*ov; tot+=ov
    fd=acc/tot if tot else 50; fbc=sum(1 for p in fb if P[p]["house"] in KT)
    tv=c["ashtakavarga"]["totals"]; d60=calc_divisional_charts(P,lag)["D60"]
    fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    return [fd,dhana_yoga_score(c)[0],prosperity_yoga_score(c)[0],raja_yoga_score(c)[0],fbc,tv[ls],tv[(ls+9)%12],fd60]

def bd(p): return (p["birth"]["date"],p["birth"]["time"],p["birth"]["lat"],p["birth"]["lon"])
F=np.array([feats(*bd(p)) for p in FAM]); R=np.array([feats(*bd(p)) for p in ORDD])
X=np.vstack([F,R]); y=np.array([1]*len(F)+[0]*len(R),float)
def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))
np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5)
def cvauc(metric):
    cv=np.zeros(len(y))
    for i in range(5):
        te=folds[i]; tr=np.concatenate([folds[j] for j in range(5) if j!=i])
        sg=np.sign(X[tr][y[tr]==1].mean(0)-X[tr][y[tr]==0].mean(0)); m,s=X[tr].mean(0),X[tr].std(0)+1e-9
        cv[te]=metric(((X[te]-m)/s)*sg)
    return auc(cv,y)

YOGA=[1,3]  # dhana, raja indices
metrics={
 "BREADTH count (#>0)":   lambda Z:(Z>0).sum(1),
 "BREADTH sum-z":         lambda Z:Z.sum(1),
 "PEAK max-z (single strongest factor)": lambda Z:Z.max(1),
 "PEAK max-yoga (dhana|raja)":           lambda Z:Z[:,YOGA].max(1),
 "top-2 sum":             lambda Z:np.sort(Z,1)[:,-2:].sum(1),
 "top-3 sum":             lambda Z:np.sort(Z,1)[:,-3:].sum(1),
}
print("Which shape of the signal separates famous from ordinary? (0.5 = nothing)\n")
for name,m in metrics.items():
    print(f"  CV-AUC  {name:40s} = {cvauc(m):.3f}")
