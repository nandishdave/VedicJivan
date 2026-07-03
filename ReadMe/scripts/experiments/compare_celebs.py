"""Re-run the famous-vs-ordinary count with the EXPANDED gallery (79 celebrities,
read straight from src_celebrities.json) vs 96 ordinary. Reports lift + composite
strong-factor count CV-AUC, for ALL famous and for the higher-reliability AA+A cut."""
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
FEAT=["dasha","dhana","prosperity","raja","func_ben","av_1st","av_10th","d60"]
_BAD={3,6,8,12}

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
RAT=np.array([p["rating"] for p in FAM])
print(f"FAMOUS={len(F)} (AA={sum(RAT=='AA')} A={sum(RAT=='A')} B={sum(RAT=='B')} C={sum(RAT=='C')})  ORDINARY={len(R)}")

def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))
def fit(Xt,yt,l2=1.0,lr=0.2,it=3000):
    w=np.zeros(Xt.shape[1]);b=0.0
    for _ in range(it):
        p=1/(1+np.exp(-(Xt@w+b)));w-=lr*(Xt.T@(p-yt)/len(yt)+l2*w/len(yt));b-=lr*np.mean(p-yt)
    return w,b

def report(Ff,label):
    X=np.vstack([Ff,R]); y=np.array([1]*len(Ff)+[0]*len(R),float)
    np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5)
    # composite strong-count (orientation learned per fold)
    cvc=np.zeros(len(y)); cvl=np.zeros(len(y))
    for i in range(5):
        te=folds[i]; tr=np.concatenate([folds[j] for j in range(5) if j!=i])
        sg=np.sign(X[tr][y[tr]==1].mean(0)-X[tr][y[tr]==0].mean(0)); m,s=X[tr].mean(0),X[tr].std(0)+1e-9
        cvc[te]=(((X[te]-m)/s*sg)>0).sum(1)
        w,b=fit((X[tr]-m)/s,y[tr]); cvl[te]=1/(1+np.exp(-(((X[te]-m)/s)@w+b)))
    sign=np.sign(Ff.mean(0)-R.mean(0)); mu,sd=X.mean(0),X.std(0)+1e-9
    cnt=(((X-mu)/sd)*sign>0).sum(1)
    order=np.argsort(-cnt); fam_ranks=[list(order).index(i)+1 for i in range(len(Ff))]
    print(f"\n=== {label}: {len(Ff)} famous vs {len(R)} ordinary ===")
    print(f"  composite strong-count CV-AUC = {auc(cvc,y):.3f}   | linear 8-feat CV-AUC = {auc(cvl,y):.3f}")
    print(f"  famous mean stack={cnt[y==1].mean():.2f} vs ordinary={cnt[y==0].mean():.2f}  | famous median rank={np.median(fam_ranks):.0f}/{len(y)}")

print("\nlift (ALL famous vs ordinary):")
for i,n in enumerate(FEAT): print(f"  {n:11} {F[:,i].mean():7.2f} {R[:,i].mean():7.2f}  {F[:,i].mean()-R[:,i].mean():+6.2f}")
report(F,"ALL 79 famous")
report(F[np.isin(RAT,["AA","A"])],"AA+A only")
report(F[RAT=="AA"],"AA only")
