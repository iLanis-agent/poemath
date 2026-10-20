# PoE Math

Power over Ethernet budget arithmetic. 12 devices at 6.5 W and 4 devices at 15.4 W draw 139.6 W in total, which is 58.2 percent of a 240 W switch budget.

## What it computes

Watts are typed with up to one decimal. Counts are whole numbers.

- **The budget truth** - total draw of two kinds of device (0 to 500 of each, 0.1 to 100 W each) against a budget (1 to 5000 W): the percent of the budget, and the watts spare or over.
- **The spare truth** - given a budget and what is drawn now, how many more devices of one wattage fit, and what is left after them.
- **The share truth** - the budget divided evenly over 1 to 500 ports, as an average only.

## Boundary

Arithmetic only. It has not seen any switch, device or cable. It does not know how a switch really shares its budget, the limit on each port, how devices negotiate power, or what is lost in the cable, and it gives no verdict that a switch can power the devices. Every number is the owner's own entry, for example from labels and data sheets.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact tenths of a watt).
- `oracle.py` - the Python mirror (Fractions, adds devices one at a time) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (169 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/poemath/
Repo: https://github.com/iLanis-agent/poemath
