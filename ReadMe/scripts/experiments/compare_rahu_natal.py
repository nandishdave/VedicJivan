"""Age-independent Rahu Yoga check. rahu_natal = TOTAL Rahu-dasha years falling in
the 20-50 window (a fixed birth-chart property, NO 'elapsed/today') x dispositor-
unafflicted. Compare vs the age-dependent 'elapsed' version in the winners composite."""
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
_BAD={3,6,8,12}; NOW=2026
FEAT=["rahu_elapsed","rahu_natal","d60","av_10th","av_1st"]

def feats(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon,with_shadbala=False)
    P,lag=c["planets"],c["lagna"]; ls=lag["sign"]; by=int(dob[:4])
    dl=calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]
    ra=next(((int(d["start_date"][:4])-by,int(d["end_date"][:4])-by) for d in dl if d["planet"]=="Rahu"),None)
    dispf=1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    natal=max(0,min(ra[1],50)-max(ra[0],20)) if ra else 0            # ALL Rahu-dasha yrs in 20-50 (age-free)
    elapsed=max(0,min(ra[1],50,NOW-by)-max(ra[0],20)) if ra else 0   # only those lived by NOW (age-dependent)
    tv=c["ashtakavarga"]["totals"]; d60=calc_divisional_charts(P,lag)["D60"]
    fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    return [elapsed*dispf, natal*dispf, fd60, tv[(ls+9)%12], tv[ls]]

def bd(p): return (p["birth"]["date"],p["birth"]["time"],p["birth"]["lat"],p["birth"]["lon"])
F=np.array([feats(*bd(p)) for p in FAM]); R=np.array([feats(*bd(p)) for p in ORDD])
# avg birth-year, to show the age gap
fy=np.mean([int(p["birth"]["date"][:4]) for p in FAM]); oy=np.mean([int(p["birth"]["date"][:4]) for p in ORDD])
print(f"avg birth year: famous {fy:.0f} vs ordinary {oy:.0f}  (age gap ~{oy-fy:.0f} yrs → the confound)\n")
print("lift (famous vs ordinary):")
for i,n in enumerate(FEAT): print(f"  {n:13} {F[:,i].mean():7.2f} {R[:,i].mean():7.2f}  {F[:,i].mean()-R[:,i].mean():+6.2f}")
def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))
def report(cols,label):
    Xf=F[:,cols]; Xr=R[:,cols]; X=np.vstack([Xf,Xr]); y=np.array([1]*len(Xf)+[0]*len(Xr),float)
    np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5); cvc=np.zeros(len(y)); cvs=np.zeros(len(y))
    for i in range(5):
        te=folds[i]; tr=np.concatenate([folds[j] for j in range(5) if j!=i])
        sg=np.sign(X[tr][y[tr]==1].mean(0)-X[tr][y[tr]==0].mean(0)); m,s=X[tr].mean(0),X[tr].std(0)+1e-9
        Z=((X[te]-m)/s)*sg; cvc[te]=(Z>0).sum(1) if len(cols)>1 else Z[:,0]; cvs[te]=Z.sum(1)
    print(f"  {label:40s} count-AUC={auc(cvc,y):.3f}  sum-AUC={auc(cvs,y):.3f}")
N={n:i for i,n in enumerate(FEAT)}
print()
report([N["rahu_elapsed"]],"rahu_ELAPSED alone (age-dependent)")
report([N["rahu_natal"]],"rahu_NATAL alone (age-free)")
report([N["rahu_elapsed"],N["d60"],N["av_10th"],N["av_1st"]],"WINNERS w/ elapsed (baseline)")
report([N["rahu_natal"],N["d60"],N["av_10th"],N["av_1st"]],"WINNERS w/ NATAL (age-free)")
