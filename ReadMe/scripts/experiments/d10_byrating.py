# -*- coding: utf-8 -*-
"""Does the RICH D10 (Lagna-lord + 10th-lord connection/strength + career composite)
revive on ACCURATE-time charts? Solo-AUC of each D10 career metric across
ALL/AA/AA+A/B+C, AND whether adding d10_career lifts the 8-factor composite on the
AA+A famous subset. This is the cut d10_rich.py never ran (it cut by geography only).
Famous vs ordinary(96). No Shadbala -> fast."""
import json, numpy as np
from collections import Counter
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _GOOD = {1, 4, 5, 7, 9, 10}
FEAT = ["rahu", "d60", "av10", "av1", "upa", "raja", "dhana", "av11",
        "d10_laglord_dig", "d10_10lord_dig", "d10_10lord_place", "d10_laglord_place",
        "d10_10th_occ", "d10_career", "d10_lag10_conn"]

def _pw(links):
    w = {}
    for lk in links:
        for p in lk.get("planets", []): w[p] = w.get(p, 0.0) + lk["score"]
    return w
def _act(dl, by, wd, a, b):
    tot = acc = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
        if ov <= 0: continue
        tot += ov; acc += wd.get(d["planet"], 0.0) * ov
    return acc / tot if tot else 0.0

def feats(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * dispf
    dv = calc_divisional_charts(P, lag); D60, D10 = dv["D60"], dv["D10"]
    d60c = float(np.mean([_DP.get(_get_dignity(pl, D60[pl]), 45) for pl in _C]))
    tv = c["ashtakavarga"]["totals"]; av10, av1, av11 = tv[(ls + 9) % 12], tv[ls], tv[(ls + 10) % 12]
    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        tot += ov
        if P[d["planet"]]["house"] in _OCC: occ += ov
    upa = occ / tot if tot else 0.0
    rl = _act(dl, by, _pw(raja_yoga_score(c)[1]), 50, 80); dhl = _act(dl, by, _pw(dhana_yoga_score(c)[1]), 50, 80)
    # ---- RICH D10 ----
    d10_lag = D10["Lagna"]; laglord = SIGN_LORDS[d10_lag]
    tenth_sign = (d10_lag + 9) % 12; tenlord = SIGN_LORDS[tenth_sign]
    def dig(pl): return _DP.get(_get_dignity(pl, D10[pl]), 45)
    def house_in_d10(pl): return ((D10[pl] - d10_lag) % 12) + 1
    def place(pl):
        h = house_in_d10(pl); return 100.0 if h in _GOOD else 40.0 if h in _BAD else 60.0
    d10_laglord_dig = dig(laglord); d10_10lord_dig = dig(tenlord)
    d10_10lord_place = place(tenlord); d10_laglord_place = place(laglord)
    occs = [pl for pl in _C if D10[pl] == tenth_sign]
    d10_10th_occ = float(np.mean([dig(pl) for pl in occs])) if occs else 45.0
    d10_career = 0.35 * d10_10lord_dig + 0.2 * d10_10lord_place + 0.2 * d10_laglord_dig \
        + 0.1 * d10_laglord_place + 0.15 * d10_10th_occ
    # explicit LAGNA<->10th-lord CONNECTION: conjunct, or lord placed in a kendra/trikona from D10 lagna,
    # or lagna-lord and 10th-lord conjunct/mutual — the "yoga" reading rather than raw strength.
    ll_h = house_in_d10(laglord); tl_h = house_in_d10(tenlord)
    conn = 0.0
    if D10[laglord] == D10[tenlord]: conn += 1.0            # lagna-lord & 10th-lord conjunct
    if tl_h in _GOOD: conn += 1.0                           # 10th-lord in kendra/trikona
    if ll_h in {1, 10}: conn += 1.0                         # lagna-lord in 1st/10th
    return [rahu, d60c, av10, av1, upa, rl, dhl, av11,
            d10_laglord_dig, d10_10lord_dig, d10_10lord_place, d10_laglord_place,
            d10_10th_occ, d10_career, conn]

def rating(p):
    r = str(p.get("rating", "")).strip().upper(); return r if r in ("AA", "A", "B", "C") else "?"

FR = [(feats(p), rating(p)) for p in FAM]
RR = [feats(p) for p in ORDD]
RT = np.array([x[1] for x in FR])
F = np.array([x[0] for x in FR]); R = np.array(RR)
print(f"famous={len(FR)} ordinary={len(RR)}  ratings={dict(Counter(RT))}")

def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
SUBS = [("ALL", np.ones(len(FR), bool)), ("AA", RT == "AA"),
        ("AA+A", np.isin(RT, ["AA", "A"])), ("B+C", np.isin(RT, ["B", "C"]))]

print("\nSolo-AUC of each D10 career metric per birth-time subset (look for monotonic lift C->AA):")
print(f"  {'metric':18} " + "  ".join(f"{nm:>6}" for nm, _ in SUBS))
for i in range(8, 15):
    rcol = R[:, i]; row = []
    for nm, m in SUBS:
        fcol = F[m, i]
        row.append(f"{auc(fcol, rcol):.3f}" if m.sum() >= 15 else "  -  ")
    print(f"  {FEAT[i]:18} " + "  ".join(f"{v:>6}" for v in row))

# Composite: does d10_career / d10_lag10_conn lift the 8-factor on the AA+A famous subset?
def cv(Fm, Rm, cols, seed=7):
    X = np.vstack([Fm[:, cols], Rm[:, cols]]); y = np.array([1]*len(Fm)+[0]*len(Rm), float)
    np.random.seed(seed); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5)
    s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr]==1].mean(0) - X[tr][y[tr]==0].mean(0))
        m, sd = X[tr].mean(0), X[tr].std(0)+1e-9
        s[te] = (((X[te]-m)/sd)*sg).sum(1)
    return auc(s[y==1], s[y==0])
base = list(range(8))
print("\nComposite lift on famous subsets (ordinary = full 96):")
for nm, m in SUBS:
    if m.sum() < 20: continue
    Fm = F[m]
    b8 = cv(Fm, R, base)
    bc = cv(Fm, R, base + [13])
    bk = cv(Fm, R, base + [14])
    print(f"  {nm:6} n={m.sum():3d}  8f={b8:.3f}  +d10_career={bc:+.3f}->{bc:.3f}  +lag10_conn={bk:.3f}")
