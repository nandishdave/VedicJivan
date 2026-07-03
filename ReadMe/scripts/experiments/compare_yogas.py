"""Does the graded-yoga recalculation improve famous-vs-ordinary separation?
Reports univariate lift per feature + CV-AUC for: full model / yogas-only /
non-yoga-only, so we can see if the yogas add ANY discriminative power."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score, prosperity_yoga_score
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAMOUS = [
    ("1961-08-04","19:24",21.3069,-157.8583),("1946-06-14","10:54",40.7020,-73.8060),
    ("1917-05-29","15:00",42.3318,-71.1212),("1947-10-26","20:02",41.85,-87.65),
    ("1946-08-19","08:51",33.67,-93.59),("1946-07-06","07:26",41.31,-72.92),
    ("1911-02-06","02:04",41.63,-89.79),("1889-04-20","18:30",48.2585,13.0333),
    ("1874-11-30","01:30",51.8517,-1.3520),("1926-04-21","02:40",51.5074,-0.1278),
    ("1948-11-14","21:14",51.5074,-0.1278),("1961-07-01","19:45",52.8312,0.5152),
    ("1982-06-21","21:03",51.5074,-0.1278),("1984-09-15","16:20",51.5074,-0.1278),
    ("1926-06-01","09:30",34.0522,-118.2437),("1935-01-08","04:35",34.2576,-88.7034),
    ("1958-08-29","23:53",41.5934,-87.3464),("1958-08-16","07:05",43.5945,-83.8889),
    ("1954-01-29","04:30",33.0576,-89.5887),("1989-12-13","05:17",40.3356,-75.9269),
    ("1975-06-04","09:09",34.05,-118.24),("1943-12-08","11:55",28.08,-80.61),
    ("1967-02-20","19:38",46.98,-123.82),("1879-03-14","11:30",48.3984,9.9916),
    ("1875-07-26","19:32",47.60,9.30),("1856-05-06","18:30",49.64,18.15),
    ("1809-02-12","03:00",52.71,-2.75),("1856-07-10","00:00",44.5811,15.3144),
    ("1942-01-17","18:35",38.2527,-85.7585),("1940-10-09","18:30",53.4084,-2.9916),
    ("1942-06-18","14:00",53.4084,-2.9916),("1942-11-27","10:15",47.61,-122.33),
]
with open("/app/normal_people.json", encoding="utf-8") as fh:
    ORD_DATA = json.load(fh)
ORD = [(p["birth"]["date"],p["birth"]["time"],p["birth"]["lat"],p["birth"]["lon"]) for p in ORD_DATA]
_C=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]; _BEN={"Jupiter","Venus","Mercury"}
KT={1,4,5,7,9,10}; CAMP_A={9,10,6,1,2,5}; FB_A={"Saturn","Venus","Mercury"}; FB_B={"Sun","Moon","Mars","Jupiter"}
_DP={"Exalted":100,"Moolatrikona":85,"Own Sign":75,"Friendly Sign":55,"Neutral Sign":45,"Enemy Sign":25,"Debilitated":5}
FEAT=["dasha","dhana","prosperity","raja","func_ben","av_1st","av_10th","d60"]
YOGA_IDX=[1,2,3]; NONYOGA_IDX=[0,4,5,6,7]

def feats(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon); P,lag,sb=c["planets"],c["lagna"],c["shadbala"]
    ls=lag["sign"]
    def L(h): return SIGN_LORDS[(ls+h-1)%12]
    fb=FB_A if ls in CAMP_A else FB_B  # FUNCTIONAL benefics (not natural)
    _BAD={3,6,8,12}
    def _dasha_strength(pl):
        if pl in ("Rahu","Ketu"):
            disp=SIGN_LORDS[P[pl]["sign"]]
            base=min(sb.get(disp,{}).get("ratio",1.0)/1.5,1.0)*100
            ben=disp in fb or disp==L(1); good=P[disp]["house"] not in _BAD
            tier=1.15 if (ben and good) else 0.95 if ben else 0.85 if good else 0.65
            return min(base*tier,100)
        s=min(sb.get(pl,{}).get("ratio",1.0)/1.5,1.0)*100
        if pl in fb or pl==L(1): s=min(s*1.15,100)
        return s
    by=int(dob[:4]); acc=tot=0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]:
        ov=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
        if ov<=0: continue
        acc+=_dasha_strength(d["planet"])*ov; tot+=ov
    fd=acc/tot if tot else 50
    ffb=sum(1 for p in fb if P[p]["house"] in KT)
    tv=c["ashtakavarga"]["totals"]; d60=calc_divisional_charts(P,lag)["D60"]
    fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    return [fd,dhana_yoga_score(c)[0],prosperity_yoga_score(c)[0],raja_yoga_score(c)[0],ffb,tv[ls],tv[(ls+9)%12],fd60]

F=np.array([feats(*r) for r in FAMOUS]); R=np.array([feats(*r) for r in ORD])
X=np.vstack([F,R]); y=np.array([1]*len(F)+[0]*len(R),float)
print("feature        FAMOUS  ORDINARY    lift")
for i,name in enumerate(FEAT):
    print(f"{name:12} {F[:,i].mean():8.2f} {R[:,i].mean():8.2f}  {F[:,i].mean()-R[:,i].mean():+7.2f}")

def fit(Xt,yt,l2=1.0,lr=0.2,it=3000):
    w=np.zeros(Xt.shape[1]);b=0.0
    for _ in range(it):
        p=1/(1+np.exp(-(Xt@w+b)));w-=lr*(Xt.T@(p-yt)/len(yt)+l2*w/len(yt));b-=lr*np.mean(p-yt)
    return w,b
def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))
def cvauc(cols):
    Xc=X[:,cols]; np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5); cvp=np.zeros(len(y))
    for i in range(5):
        te=folds[i];tr=np.concatenate([folds[j] for j in range(5) if j!=i])
        m,s=Xc[tr].mean(0),Xc[tr].std(0)+1e-9; w,b=fit((Xc[tr]-m)/s,y[tr]); cvp[te]=1/(1+np.exp(-(((Xc[te]-m)/s)@w+b)))
    return auc(cvp,y)
print(f"\nCV-AUC full 8-feature        = {cvauc(list(range(8))):.3f}")
print(f"CV-AUC YOGAS only (dhana/prosperity/raja) = {cvauc(YOGA_IDX):.3f}   (0.5 = no separation)")
print(f"CV-AUC NON-yoga (dasha/funcben/av/d60)    = {cvauc(NONYOGA_IDX):.3f}")
print(f"CV-AUC each yoga alone: dhana={cvauc([1]):.3f}  prosperity={cvauc([2]):.3f}  raja={cvauc([3]):.3f}")
