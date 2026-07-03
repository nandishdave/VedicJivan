"""Graded Dhana-Yoga score (connection x lords x dignity x house), ranked top->bottom
for all 128 charts + a sample low-ranked breakdown + does it improve the famous-vs-ordinary CV-AUC?"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES, _get_dignity
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

_C=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]; _BEN={"Jupiter","Venus","Mercury"}
KT={1,4,5,7,9,10}; CAMP_A={9,10,6,1,2,5}; FB_A={"Saturn","Venus","Mercury"}; FB_B={"Sun","Moon","Mars","Jupiter"}
_DP={"Exalted":100,"Moolatrikona":85,"Own Sign":75,"Friendly Sign":55,"Neutral Sign":45,"Enemy Sign":25,"Debilitated":5}
# --- Dhana-yoga rubric ---
DIGF={"Exalted":1.0,"Moolatrikona":0.9,"Own Sign":0.8,"Friendly Sign":0.6,"Neutral Sign":0.45,"Enemy Sign":0.25,"Debilitated":0.1}
CONN={"parivartana":10,"conjunction":8,"inherent":7,"mutual_aspect":6,"aspect":3}
MONEY=[1,2,5,9,11]; CORE={1,2,11}
def hfac(h):
    if h in (1,2,4,5,9,10,11): return 1.0
    if h==7: return 0.75
    if h==3: return 0.5
    return 0.35

def build(dob,tob,lat,lon):
    return build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon)

def dhana(c, verbose=False):
    P,lag=c["planets"],c["lagna"]; asp=c["graha_drishti"]["planet_aspects"]; ls=lag["sign"]
    def L(h): return SIGN_LORDS[(ls+h-1)%12]
    lord={h:L(h) for h in MONEY}; owns={}
    for h in MONEY: owns.setdefault(lord[h],set()).add(h)
    dg=lambda p: DIGF.get(_get_dignity(p,P[p]["sign"]),0.45)
    total=0.0; rows=[]
    for p,hs in owns.items():                              # single planet owning >=2 money houses
        if len(hs)>=2:
            cc=len(hs & CORE); mult=1.0 if cc>=2 else (0.7 if cc==1 else 0.5)
            sc=CONN["inherent"]*mult*dg(p)*hfac(P[p]["house"]); total+=sc
            rows.append((f"{p} owns {'&'.join(map(str,sorted(hs)))}","inherent",round(dg(p),2),P[p]["house"],round(sc,2)))
    pls=list(owns.keys())
    for i in range(len(pls)):
        for j in range(i+1,len(pls)):
            a,b=pls[i],pls[j]
            if SIGN_LORDS[P[a]["sign"]]==b and SIGN_LORDS[P[b]["sign"]]==a: t="parivartana"
            elif P[a]["house"]==P[b]["house"]: t="conjunction"
            elif (P[b]["house"] in asp.get(a,[])) and (P[a]["house"] in asp.get(b,[])): t="mutual_aspect"
            elif (P[b]["house"] in asp.get(a,[])) or (P[a]["house"] in asp.get(b,[])): t="aspect"
            else: t=None
            if not t: continue
            ca,cb=owns[a]&CORE,owns[b]&CORE
            mult=1.0 if (ca and cb) else (0.7 if (ca or cb) else 0.5)
            dig=(dg(a)+dg(b))/2
            hf=hfac(P[a]["house"]) if t=="conjunction" else (hfac(P[a]["house"])+hfac(P[b]["house"]))/2
            sc=CONN[t]*mult*dig*hf; total+=sc
            rows.append((f"{a}({'&'.join(map(str,sorted(owns[a])))}) - {b}({'&'.join(map(str,sorted(owns[b])))})",t,round(dig,2),f"{P[a]['house']}/{P[b]['house']}",round(sc,2)))
    return (total,rows) if verbose else total

def feats(c):                                              # 7-vector, wealth slot = dhana
    P,lag,sb=c["planets"],c["lagna"],c["shadbala"]; asp=c["graha_drishti"]["planet_aspects"]; ls=lag["sign"]
    def L(h): return SIGN_LORDS[(ls+h-1)%12]
    dob=c.get("_dob"); tob=c.get("_tob"); by=int(dob[:4]); acc=tot=0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]:
        ov=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
        if ov<=0: continue
        s=min(sb.get(d["planet"],{}).get("ratio",1.0)/1.5,1.0)*100
        if d["planet"] in _BEN or d["planet"]==L(1): s=min(s*1.15,100)
        acc+=s*ov; tot+=ov
    fd=acc/tot if tot else 50
    def samb(a,b):
        if a==b or P[a]["house"]==P[b]["house"]: return True
        if P[b]["house"] in asp.get(a,[]) or P[a]["house"] in asp.get(b,[]): return True
        return SIGN_LORDS[P[a]["sign"]]==b and SIGN_LORDS[P[b]["sign"]]==a
    tri=list({L(1),L(5),L(9)}); par={p:p for p in tri}
    def fn(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for i in range(len(tri)):
        for j in range(i+1,len(tri)):
            if samb(tri[i],tri[j]): par[fn(tri[i])]=fn(tri[j])
    sz={}
    for p in tri: sz[fn(p)]=sz.get(fn(p),0)+1
    ft=max(sz.values()); fb=FB_A if ls in CAMP_A else FB_B
    ffb=sum(1 for p in fb if P[p]["house"] in KT); tv=c["ashtakavarga"]["totals"]
    d60=calc_divisional_charts(P,lag)["D60"]; fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    return [fd,dhana(c),ft,ffb,tv[ls],tv[(ls+9)%12],fd60]

ALL=[(n,*r,1) for n,r in zip(FNAMES,FAMOUS)]+[(n,*r,0) for n,r in zip(ONAMES,ORD)]
charts=[]
for n,dob,tob,lat,lon,fam in ALL:
    c=build(dob,tob,lat,lon); c["_dob"],c["_tob"]=dob,tob; charts.append((n,fam,c))
dh=np.array([dhana(c) for _,_,c in charts])
X=np.array([feats(c) for _,_,c in charts]); y=np.array([f for _,f,_ in charts],float); names=[n for n,_,_ in charts]

print("===== DHANA-YOGA RANKING (all 128, top -> bottom) =====")
order=np.argsort(-dh)
for rk,k in enumerate(order,1):
    print(f"{rk:>3}  {dh[k]:6.2f}  {'★' if y[k] else ' '}  {names[k]}")

print("\n===== SAMPLE ORDINARY CHART (lowest-ranked) — dhana breakdown =====")
ks=int(order[-1]); _,rows=dhana(charts[ks][2],verbose=True)
print(f"{'link':32} {'type':13} {'dig':>4} {'house':>6} {'score':>6}")
for r in rows: print(f"{r[0]:32} {r[1]:13} {r[2]:>4} {str(r[3]):>6} {r[4]:>6}")
print(f"TOTAL dhana = {dh[ks]:.2f}  (rank {list(order).index(ks)+1}/128)")

print("\n===== DOES IT HELP THE MODEL? =====")
FEAT=["dasha_20_50","dhana_yoga","trikona","func_ben_KT","av_1st","av_10th","d60_str"]
print(f"dhana lift: FAMOUS {dh[y==1].mean():.2f} vs ORDINARY {dh[y==0].mean():.2f}  (+{dh[y==1].mean()-dh[y==0].mean():.2f})")
def fit(Xt,yt,l2=1.0,lr=0.2,it=3000):
    w=np.zeros(Xt.shape[1]);b=0.0
    for _ in range(it):
        p=1/(1+np.exp(-(Xt@w+b)));w-=lr*(Xt.T@(p-yt)/len(yt)+l2*w/len(yt));b-=lr*np.mean(p-yt)
    return w,b
def auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos])
np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5); cvp=np.zeros(len(y))
for i in range(5):
    te=folds[i];tr=np.concatenate([folds[j] for j in range(5) if j!=i])
    m,s=X[tr].mean(0),X[tr].std(0)+1e-9; w,b=fit((X[tr]-m)/s,y[tr]); cvp[te]=1/(1+np.exp(-(((X[te]-m)/s)@w+b)))
print(f"CV-AUC with dhana_yoga (replacing wealth_2_11) = {auc(cvp,y):.3f}   [old wealth_2_11 was 0.554]")
mu,sd=X.mean(0),X.std(0)+1e-9; w,b=fit((X-mu)/sd,y)
print("full-data weights:")
for i in np.argsort(-np.abs(w)): print(f"   {FEAT[i]:12} {w[i]:+.2f}")
