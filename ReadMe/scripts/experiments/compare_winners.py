"""Winners-only composite: restore GOOD dasha (functional-benefic, no aggressive
2x2 node penalties) + Rahu Yoga + D60 + 10th-AV + 1st-AV. 79 famous vs 96 ordinary."""
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
_BAD={3,6,8,12}; NOW=2026
FEAT=["dasha_good","dhana","prosperity","raja","func_ben","av_1st","av_10th","d60","rahu_yoga"]

def feats(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon); P,lag,sb=c["planets"],c["lagna"],c["shadbala"]; ls=lag["sign"]
    def L(h): return SIGN_LORDS[(ls+h-1)%12]
    fb=FB_A if ls in CAMP_A else FB_B; by=int(dob[:4])
    dl=calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]
    def ds_good(pl):   # functional-benefic bonus; node inherits dispositor's benefic nature (NO 2x2 penalties)
        s=min(sb.get(pl,{}).get("ratio",1.0)/1.5,1.0)*100
        isben=(pl in fb) or (pl==L(1))
        if pl in ("Rahu","Ketu"):
            disp=SIGN_LORDS[P[pl]["sign"]]; isben=(disp in fb) or (disp==L(1))
        if isben: s=min(s*1.15,100)
        return s
    acc=tot=0.0
    for d in dl:
        ov=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
        if ov<=0: continue
        acc+=ds_good(d["planet"])*ov; tot+=ov
    fd=acc/tot if tot else 50; fbc=sum(1 for p in fb if P[p]["house"] in KT)
    tv=c["ashtakavarga"]["totals"]; d60=calc_divisional_charts(P,lag)["D60"]
    fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    ra=next(((int(d["start_date"][:4])-by,int(d["end_date"][:4])-by) for d in dl if d["planet"]=="Rahu"),None)
    elapsed=max(0,min(ra[1],50,NOW-by)-max(ra[0],20)) if ra else 0
    dispf=1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    ry=elapsed*dispf
    return [fd,dhana_yoga_score(c)[0],prosperity_yoga_score(c)[0],raja_yoga_score(c)[0],fbc,tv[ls],tv[(ls+9)%12],fd60,ry]

def bd(p): return (p["birth"]["date"],p["birth"]["time"],p["birth"]["lat"],p["birth"]["lon"])
F=np.array([feats(*bd(p)) for p in FAM]); R=np.array([feats(*bd(p)) for p in ORDD])
print("lift (famous vs ordinary):")
for i,n in enumerate(FEAT): print(f"  {n:11} {F[:,i].mean():7.2f} {R[:,i].mean():7.2f}  {F[:,i].mean()-R[:,i].mean():+6.2f}")

def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))
def report(cols,label):
    Xf=F[:,cols]; Xr=R[:,cols]; X=np.vstack([Xf,Xr]); y=np.array([1]*len(Xf)+[0]*len(Xr),float)
    np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5); cvc=np.zeros(len(y)); cvs=np.zeros(len(y))
    for i in range(5):
        te=folds[i]; tr=np.concatenate([folds[j] for j in range(5) if j!=i])
        sg=np.sign(X[tr][y[tr]==1].mean(0)-X[tr][y[tr]==0].mean(0)); m,s=X[tr].mean(0),X[tr].std(0)+1e-9
        Z=((X[te]-m)/s)*sg; cvc[te]=(Z>0).sum(1); cvs[te]=Z.sum(1)
    print(f"  {label:34s} count-AUC={auc(cvc,y):.3f}  sum-AUC={auc(cvs,y):.3f}")
NAMES={n:i for i,n in enumerate(FEAT)}
print()
report(list(range(9)),"all 9 (good dasha)")
report([NAMES[x] for x in ["dasha_good","rahu_yoga","d60","av_10th","av_1st"]],"WINNERS (dasha+rahu+d60+10AV+1AV)")
report([NAMES[x] for x in ["dasha_good","rahu_yoga","d60","av_10th","av_1st","raja"]],"WINNERS + raja")
report([NAMES[x] for x in ["rahu_yoga","d60","av_10th","av_1st"]],"WINNERS minus dasha (compare)")
