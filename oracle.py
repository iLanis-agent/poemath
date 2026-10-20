#!/usr/bin/env python3
# PoE Math oracle - mirrors engine.js with Fractions: watts are exact decimals, devices are added to the switch one at a time until the budget would be passed, and rounding is done with Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

BERR = "the budget must be from 1 to 5000 W"
DERR = "the watts per device must be from 0.1 to 100 W"
CERR = "the device count must be a whole number from 0 to 500"

def watts(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    m = re.fullmatch(r"([0-9]{1,5})(?:\.([0-9]))?", t)
    if not m: raise ValueError(err)
    v = F(m[1]) + (F(int(m[2]), 10) if m[2] else 0)
    if not F(str(lo)) <= v <= F(str(hi)): raise ValueError(err)
    return v
def cnt(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def pl(n, a, b): return f"{n} {a if n == 1 else b}"
def txt(v):  # exact tenths value to text
    assert (v * 10).denominator == 1
    t = int(v * 10); ip, fp = divmod(t, 10)
    return f"{ip}.{fp}" if fp else str(ip)
def half_up_tenths(fr):
    return F(int((Decimal(fr.numerator) / Decimal(fr.denominator) * 10).quantize(Decimal("1"), rounding=ROUND_HALF_UP)), 10)

def budget(b, ca, wa, cb, wb):
    b = watts(b, BERR, 1, 5000); ca = cnt(ca, CERR, 0, 500); wa = watts(wa, DERR, F(1, 10), 100)
    cb = cnt(cb, CERR, 0, 500); wb = watts(wb, DERR, F(1, 10), 100)
    if ca + cb == 0: raise ValueError("add at least 1 device")
    draw = sum([wa] * ca) + sum([wb] * cb)
    g = []
    if ca: g.append(f"{pl(ca,'device','devices')} at {txt(wa)} W")
    if cb: g.append(f"{pl(cb,'device','devices')} at {txt(wb)} W")
    pct = half_up_tenths(draw / b * 100)
    if draw < b: tail = f"leaving {txt(b - draw)} W spare"
    elif draw == b: tail = "with nothing spare"
    else: tail = f"which is {txt(draw - b)} W over the budget"
    return f"Total draw is {txt(draw)} W from {' and '.join(g)}. Against a budget of {txt(b)} W that is {txt(pct)} percent, {tail}."
def spare(b, d, w):
    b = watts(b, BERR, 1, 5000); d = watts(d, "the current draw must be from 0 to 5000 W", 0, 5000); w = watts(w, DERR, F(1, 10), 100)
    if d > b: return f"The draw of {txt(d)} W is already {txt(d - b)} W over the budget of {txt(b)} W, so no more devices of {txt(w)} W fit."
    k = 0; load = d
    while load + w <= b: load += w; k += 1
    if k == 0: return f"With a budget of {txt(b)} W and {txt(d)} W drawn, {txt(b - d)} W is spare. That is less than one device of {txt(w)} W."
    return f"With a budget of {txt(b)} W and {txt(d)} W drawn, {txt(b - d)} W is spare. That fits {pl(k,'more device','more devices')} of {txt(w)} W ({txt(k * w)} W), leaving {txt(b - load)} W."
def share(b, p):
    b = watts(b, BERR, 1, 5000); p = cnt(p, "the ports must be a whole number from 1 to 500", 1, 500)
    return f"A budget of {txt(b)} W shared evenly over {pl(p,'port','ports')} is {txt(half_up_tenths(b / p))} W a port. That is only the average. It says nothing about what any one port is allowed to draw."

FNS = {"budgetTruth": budget, "spareTruth": spare, "shareTruth": share}

def cases():
    c = []
    for a in [("240","12","6.5","4","15.4"),("60","4","15","0","5"),("60","1","60","0","5"),("60","0","5","1","60"),("60","2","30","0","1"),("60","2","30.1","0","1"),("60","3","20","1","0.1"),("1","1","0.1","0","0.1"),("5000","500","100","500","100"),("5000","500","10","0","0.1"),
              ("370","24","15.4","0","30"),("370","8","30","8","15.4"),("123.4","7","7.7","3","9.9"),("100","1","99.9","0","1"),("100","1","100","0","1"),("100","1","100","1","0.1"),
              ("0","1","5","0","5"),("5001","1","5","0","5"),("100","0","5","0","5"),("100","501","5","0","5"),("100","1","0","0","5"),("100","1","100.1","0","5"),("100","1","5","0","101"),("x","1","5","0","5"),("100","1.5","5","0","5"),("100","1","5.55","0","5"),("100","1","","0","5"),(" 100 "," 2 "," 5.5 "," 1 "," 6 "),("100","-1","5","0","5"),("1.5","1","0.5","1","0.5")]:
        c.append(("budgetTruth", list(a)))
    for a in [("240","131.6","15"),("240","239","15"),("240","250","15"),("240","240","15"),("240","225","15"),("240","0","100"),("5000","0","0.1"),("5000","5000","0.1"),("5000","4999.9","0.1"),("60","45","15"),("60","45.1","15"),("100","33.3","33.3"),
              ("0","5","5"),("100","5001","5"),("100","-1","5"),("100","5","0"),("100","5","100.5"),("100","x","5"),("100","","5"),(" 100 "," 20 "," 5 ")]:
        c.append(("spareTruth", list(a)))
    for a in [("240","24"),("100","3"),("100","7"),("370","48"),("1","500"),("1","1"),("5000","1"),("5000","500"),("0.5","1"),("2.5","3"),("60","8"),
              ("0","24"),("5001","24"),("240","0"),("240","501"),("240","2.5"),("x","24"),("240",""),(" 240 "," 24 ")]:
        c.append(("shareTruth", list(a)))
    r = random.Random(704)
    def w(hi): return f"{r.randint(1, hi*10)/10:.1f}".rstrip("0").rstrip(".") if r.random() < .6 else str(r.randint(1, hi))
    for _ in range(40): c.append(("budgetTruth", [w(5000), str(r.randint(0, 100)), w(100), str(r.randint(0, 100)), w(100)]))
    for _ in range(35):
        b = r.randint(10, 20000) / 10
        c.append(("spareTruth", [f"{b:.1f}", f"{r.randint(0, int(b*10))/10:.1f}", w(100)]))
    for _ in range(25): c.append(("shareTruth", [w(5000), str(r.randint(1, 500))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
