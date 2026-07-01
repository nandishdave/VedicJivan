"""Per-chart famous-likeness score (cross-validated) + full ranking of famous
vs ordinary, so we can SEE the famous out-scoring."""
import json
import numpy as np

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score, prosperity_yoga_score
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
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
def samb(a,b,P,asp):
    if a==b or P[a]["house"]==P[b]["house"]: return True
    if P[b]["house"] in asp.get(a,[]) or P[a]["house"] in asp.get(b,[]): return True
    return SIGN_LORDS[P[a]["sign"]]==b and SIGN_LORDS[P[b]["sign"]]==a
def feats(dob,tob,lat,lon):
    c=build_muhurta_chart(dob=dob,tob=tob,lat=lat,lon=lon); P,lag,sb=c["planets"],c["lagna"],c["shadbala"]
    asp=c["graha_drishti"]["planet_aspects"]; ls=lag["sign"]
    def L(h): return SIGN_LORDS[(ls+h-1)%12]
    fb=FB_A if ls in CAMP_A else FB_B  # FUNCTIONAL benefics for this lagna (NOT natural)
    by=int(dob[:4]); acc=tot=0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"],dob,tob)["dashas"]:
        ov=max(0,min(int(d["end_date"][:4])-by,50)-max(int(d["start_date"][:4])-by,20))
        if ov<=0: continue
        s=min(sb.get(d["planet"],{}).get("ratio",1.0)/1.5,1.0)*100
        # Bonus only if the dasha lord is a FUNCTIONAL benefic for this lagna (or the
        # Lagnesh) — e.g. Jupiter (3rd+6th lord) is a functional MALEFIC for Libra.
        if d["planet"] in fb or d["planet"]==L(1): s=min(s*1.15,100)
        acc+=s*ov; tot+=ov
    fd=acc/tot if tot else 50
    fw=dhana_yoga_score(c)[0]       # graded Dhana yoga (strict 1/2/11 wealth)
    fp=prosperity_yoga_score(c)[0]  # graded Prosperity yoga (5/9 fortune extension)
    ft=raja_yoga_score(c)[0]  # graded Raja yoga (replaces crude trikona-clustering)
    ffb=sum(1 for p in fb if P[p]["house"] in KT); tv=c["ashtakavarga"]["totals"]
    d60=calc_divisional_charts(P,lag)["D60"]; fd60=np.mean([_DP.get(_get_dignity(p,d60[p]),45) for p in _C])
    return [fd,fw,fp,ft,ffb,tv[ls],tv[(ls+9)%12],fd60]

F=np.array([feats(*r) for r in FAMOUS],float); R=np.array([feats(*r) for r in ORD],float)
X=np.vstack([F,R]); y=np.array([1]*len(F)+[0]*len(R),float)
names=FNAMES+ONAMES; labels=["★"]*len(F)+[" "]*len(R)
def _auc(sc,yy):
    pos=sc[yy==1];neg=sc[yy==0];return float(np.mean([np.mean(p>neg)+0.5*np.mean(p==neg) for p in pos]))

# ---- COMPOSITE score: how many of the 8 strong-chart factors a chart stacks ----
# Orient each factor famous-positive, standardise, count the elevated ones (z>0).
# This co-occurrence count separates fame better than the weighted linear model.
sign=np.sign(F.mean(0)-R.mean(0)); mu,sd=X.mean(0),X.std(0)+1e-9
Z=((X-mu)/sd)*sign
count=(Z>0).sum(1).astype(float)   # 0..8 strong factors stacked
zsum=Z.sum(1)                      # continuous composite (tie-break within a count)
order=np.lexsort((-zsum,-count))   # rank by strong-count, then by composite z-sum

# Honest out-of-sample check: CV-AUC of the count (orientation learned per fold).
np.random.seed(7); idx=np.random.permutation(len(y)); folds=np.array_split(idx,5); cvc=np.zeros(len(y))
for i in range(5):
    te=folds[i]; tr=np.concatenate([folds[j] for j in range(5) if j!=i])
    sg=np.sign(X[tr][y[tr]==1].mean(0)-X[tr][y[tr]==0].mean(0)); m,s=X[tr].mean(0),X[tr].std(0)+1e-9
    cvc[te]=(((X[te]-m)/s*sg)>0).sum(1)

print("RANK  STRONG  COMPOSITE  WHO   NAME")
for rank,k in enumerate(order,1):
    print(f"{rank:>3}    {int(count[k])}/8   {zsum[k]:+7.2f}    {labels[k]}    {names[k]}")
topN=20; tf=sum(1 for k in order[:topN] if labels[k]=="★")
print(f"\n★ = famous ({len(F)}), blank = ordinary ({len(R)})")
print(f"Famous mean strong-count={count[y==1].mean():.2f}  |  Ordinary mean={count[y==0].mean():.2f}")
print(f"Top {topN}: {tf} famous / {topN-tf} ordinary  |  famous median rank={np.median([list(order).index(i)+1 for i in range(len(F))]):.0f} of {len(y)}")
print(f"CV-AUC of the composite strong-count = {_auc(cvc,y):.3f}  (linear 8-feature was 0.485; 0.5=chance)")
