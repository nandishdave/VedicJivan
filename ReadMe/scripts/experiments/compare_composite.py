"""Test the COMPOSITE / co-occurrence hypothesis: do famous charts stack MORE of
the 8 factors at once, and is there multiplicative synergy a linear model misses?
  1. strong-factor COUNT per chart (how many of 8 are elevated) - famous vs ordinary
  2. CV-AUC of that count (orientation+threshold learned per fold)
  3. CV-AUC linear 8-feature (baseline) vs 8-feature + all pairwise INTERACTIONS
"""
import json
import numpy as np
from itertools import combinations
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
ORD=[(p["birth"]["date"],p["birth"]["time"],p["birth"]["lat"],p["birth"]["lon"]) for p in ORD_DATA]
_C=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]; _BEN={"Jupiter","Venus","Mercury"}
KT={1,4,5,7,9,10}; CAMP_A={9,10,6,1,2,5}; FB_A={"Saturn","Venus","Mercury"}; FB_B={"Sun","Moon","Mars","Jupiter"}
_DP={"Exalted":100,"Moolatrikona":85,"Own Sign":75,"Friendly Sign":55,"Neutral Sign":45,"Enemy Sign":25,"Debilitated":5}

def feats(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon); P,lag,sb=c["planets"],c["lagna"],c["shadbala"]
    ls=lag["sign"]
    def L(h): return SIGN_LORDS[(ls+h-1)%12]
    by=int(dob[:4]); acc=tot=0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]:
        ov=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
        if ov<=0: continue
        s=min(sb.get(d["planet"],{}).get("ratio",1.0)/1.5,1.0)*100
        if d["planet"] in _BEN or d["planet"]==L(1): s=min(s*1.15,100)
        acc+=s*ov; tot+=ov
    fd=acc/tot if tot else 50
    fb=FB_A if ls in CAMP_A else FB_B; ffb=sum(1 for p in fb if P[p]["house"] in KT)
    tv=c["ashtakavarga"]["totals"]; d60=calc_divisional_charts(P,lag)["D60"]
    fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    return [fd,dhana_yoga_score(c)[0],prosperity_yoga_score(c)[0],raja_yoga_score(c)[0],ffb,tv[ls],tv[(ls+9)%12],fd60]

F=np.array([feats(*r) for r in FAMOUS]); R=np.array([feats(*r) for r in ORD])
X=np.vstack([F,R]); y=np.array([1]*len(F)+[0]*len(R),float)

def fit(Xt,yt,l2=1.0,lr=0.2,it=4000):
    w=np.zeros(Xt.shape[1]);b=0.0
    for _ in range(it):
        p=1/(1+np.exp(-(Xt@w+b)));w-=lr*(Xt.T@(p-yt)/len(yt)+l2*w/len(yt));b-=lr*np.mean(p-yt)
    return w,b
def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))
np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5)

# ---- 1) IN-SAMPLE strong-factor count (oriented famous-positive by full-data lift) ----
sign=np.sign(F.mean(0)-R.mean(0)); mu,sd=X.mean(0),X.std(0)+1e-9
Z=((X-mu)/sd)*sign                      # oriented z: higher = more famous-like
for thr in (0.0,0.5,1.0):
    cnt=(Z>thr).sum(1)
    fc,oc=cnt[y==1],cnt[y==0]
    print(f"strong-factor count (z>{thr}): FAMOUS mean={fc.mean():.2f}  ORDINARY mean={oc.mean():.2f}  "
          f"| P(>=5): fam={np.mean(fc>=5):.2f} ord={np.mean(oc>=5):.2f}")

# ---- 2) CV-AUC of the strong-count (orientation+scale learned per fold) ----
def cv_count(thr):
    cvp=np.zeros(len(y))
    for i in range(5):
        te=folds[i];tr=np.concatenate([folds[j] for j in range(5) if j!=i])
        sg=np.sign(X[tr][y[tr]==1].mean(0)-X[tr][y[tr]==0].mean(0))
        m,s=X[tr].mean(0),X[tr].std(0)+1e-9
        cvp[te]=(((X[te]-m)/s*sg)>thr).sum(1)
    return auc(cvp,y)
print(f"\nCV-AUC strong-count (z>0.0) = {cv_count(0.0):.3f}")
print(f"CV-AUC strong-count (z>0.5) = {cv_count(0.5):.3f}")

# ---- 3) linear vs interaction model ----
def cv_model(build):
    cvp=np.zeros(len(y))
    for i in range(5):
        te=folds[i];tr=np.concatenate([folds[j] for j in range(5) if j!=i])
        Xtr,Xte=build(X[tr]),build(X[te])
        m,s=Xtr.mean(0),Xtr.std(0)+1e-9; w,b=fit((Xtr-m)/s,y[tr]); cvp[te]=1/(1+np.exp(-(((Xte-m)/s)@w+b)))
    return auc(cvp,y)
def linear(A): return A
def inter(A):
    cols=[A];
    for a,b in combinations(range(A.shape[1]),2): cols.append((A[:,a]*A[:,b])[:,None])
    return np.hstack(cols)
print(f"\nCV-AUC linear 8-feature            = {cv_model(linear):.3f}")
print(f"CV-AUC 8-feature + 28 interactions = {cv_model(inter):.3f}   (does synergy help?)")
