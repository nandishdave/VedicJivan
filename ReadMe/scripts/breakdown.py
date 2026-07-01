"""Show the work: learned per-feature weights + line-by-line why Oprah=96.8 and Jung=9.1.
Reproduces the EXACT cross-val fold model that scored each of them."""
import json
import numpy as np

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FNAMES = ["Obama","Trump","JFK","Hillary Clinton","Bill Clinton","GW Bush","Reagan","Hitler","Churchill",
    "Queen Elizabeth II","Charles III","Diana","Prince William","Prince Harry","Marilyn Monroe","Elvis",
    "Michael Jackson","Madonna","Oprah","Taylor Swift","Angelina Jolie","Jim Morrison","Kurt Cobain",
    "Einstein","Carl Jung","Freud","Darwin","Tesla","Muhammad Ali","John Lennon","McCartney","Hendrix"]
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
ONAMES = [p["name"] for p in ORD_DATA]
ORD = [(p["birth"]["date"],p["birth"]["time"],p["birth"]["lat"],p["birth"]["lon"]) for p in ORD_DATA]

FEAT = ["dasha_20_50","wealth_2_11","trikona","func_ben_KT","av_1st","av_10th","d60_str"]
_C=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]; _BEN={"Jupiter","Venus","Mercury"}
KT={1,4,5,7,9,10}; CAMP_A={9,10,6,1,2,5}; FB_A={"Saturn","Venus","Mercury"}; FB_B={"Sun","Moon","Mars","Jupiter"}
_DP={"Exalted":100,"Moolatrikona":85,"Own Sign":75,"Friendly Sign":55,"Neutral Sign":45,"Enemy Sign":25,"Debilitated":5}
def samb(a,b,P,asp):
    if a==b or P[a]["house"]==P[b]["house"]: return True
    if P[b]["house"] in asp.get(a,[]) or P[a]["house"] in asp.get(b,[]): return True
    return SIGN_LORDS[P[a]["sign"]]==b and SIGN_LORDS[P[b]["sign"]]==a
def feats(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon); P,lag,sb=c["planets"],c["lagna"],c["shadbala"]
    asp=c["graha_drishti"]["planet_aspects"]; ls=lag["sign"]
    def L(h): return SIGN_LORDS[(ls+h-1)%12]
    by=int(dob[:4]); acc=tot=0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]:
        ov=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
        if ov<=0: continue
        s=min(sb.get(d["planet"],{}).get("ratio",1.0)/1.5,1.0)*100
        if d["planet"] in _BEN or d["planet"]==L(1): s=min(s*1.15,100)
        acc+=s*ov; tot+=ov
    fd=acc/tot if tot else 50; l2,l11=L(2),L(11)
    fw=sum([l2!=l11 and SIGN_LORDS[P[l2]["sign"]]==l11 and SIGN_LORDS[P[l11]["sign"]]==l2,
            l2!=l11 and P[l2]["house"]==P[l11]["house"],P[l2]["house"]==11,P[l11]["house"]==2,
            P[l2]["house"]==P["Rahu"]["house"] or P[l11]["house"]==P["Rahu"]["house"]])
    tri=list({L(1),L(5),L(9)}); par={p:p for p in tri}
    def fn(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for i in range(len(tri)):
        for j in range(i+1,len(tri)):
            if samb(tri[i],tri[j],P,asp): par[fn(tri[i])]=fn(tri[j])
    sz={}
    for p in tri: sz[fn(p)]=sz.get(fn(p),0)+1
    ft=max(sz.values()); fb=FB_A if ls in CAMP_A else FB_B
    ffb=sum(1 for p in fb if P[p]["house"] in KT); tv=c["ashtakavarga"]["totals"]
    d60=calc_divisional_charts(P,lag)["D60"]; fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    return [fd,fw,ft,ffb,tv[ls],tv[(ls+9)%12],fd60]

F=np.array([feats(*r) for r in FAMOUS],float); R=np.array([feats(*r) for r in ORD],float)
X=np.vstack([F,R]); y=np.array([1]*len(F)+[0]*len(R),float); names=FNAMES+ONAMES
def fit(Xt,yt,l2=1.0,lr=0.2,it=3000):
    w=np.zeros(Xt.shape[1]);b=0.0
    for _ in range(it):
        p=1/(1+np.exp(-(Xt@w+b)));w-=lr*(Xt.T@(p-yt)/len(yt)+l2*w/len(yt));b-=lr*np.mean(p-yt)
    return w,b

# ---- headline: full-data learned weights (the model's "importance" of each vital) ----
mu,sd=X.mean(0),X.std(0)+1e-9; w,b=fit((X-mu)/sd,y)
print("LEARNED WEIGHTS (standardized — how hard the model leans on each vital)")
for i in np.argsort(-np.abs(w)):
    arrow="pushes FAMOUS up" if w[i]>0 else "pushes DOWN"
    print(f"  {FEAT[i]:12} weight={w[i]:+.2f}   {arrow}")
print(f"  (baseline bias b={b:+.2f})")

# ---- reproduce the exact CV fold that scored each target, then break it down ----
np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5)
foldof={}
for fi,fo in enumerate(folds):
    for k in fo: foldof[k]=fi
def breakdown(name):
    k=names.index(name); fi=foldof[k]
    tr=np.concatenate([folds[j] for j in range(5) if j!=fi])
    m,s=X[tr].mean(0),X[tr].std(0)+1e-9; wf,bf=fit((X[tr]-m)/s,y[tr])
    z=(X[k]-m)/s; contrib=wf*z; logit=contrib.sum()+bf; score=100/(1+np.exp(-logit))
    print(f"\n=== {name}  (scored in fold {fi}, model trained on the other {len(tr)} charts) ===")
    print(f"{'vital':12} {'raw':>7} {'grp-avg':>8} {'z':>6} {'weight':>7} {'contrib':>8}")
    for i in range(len(FEAT)):
        print(f"{FEAT[i]:12} {X[k][i]:7.2f} {m[i]:8.2f} {z[i]:+6.2f} {wf[i]:+7.2f} {contrib[i]:+8.2f}")
    print(f"{'SUM contrib':12} {contrib.sum():+43.2f}")
    print(f"{'+ baseline':12} {bf:+43.2f}")
    print(f"{'= logit':12} {logit:+43.2f}")
    print(f"SCORE = 100/(1+e^-logit) = {score:.1f}")
breakdown("Oprah")
breakdown("Carl Jung")
