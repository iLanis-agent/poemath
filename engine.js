// PoE Math engine: Power over Ethernet budget arithmetic. Total draw against a switch budget, how many more devices fit, and the even share per port. Watts in exact tenths.
function _w(t, err, lo, hi) { // watts text with up to one decimal, returned as tenths
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,5})(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < lo * 10 || v > hi * 10) throw new Error(err);
  return v;
}
function _n(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,4}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _plural(n, one, many) { return n + " " + (n === 1 ? one : many); }
function _t(v) { // tenths to text, trailing .0 dropped
  var s = String(Math.floor(v / 10)), f = v % 10;
  return f === 0 ? s : s + "." + f;
}
var _BERR = "the budget must be from 1 to 5000 W";
var _DERR = "the watts per device must be from 0.1 to 100 W";
var _CERR = "the device count must be a whole number from 0 to 500";

function budgetTruth(budget, countA, wattsA, countB, wattsB) {
  var b = _w(budget, _BERR, 1, 5000);
  var ca = _n(countA, _CERR, 0, 500), wa = _w(wattsA, _DERR, 0.1, 100);
  var cb = _n(countB, _CERR, 0, 500), wb = _w(wattsB, _DERR, 0.1, 100);
  if (ca + cb === 0) throw new Error("add at least 1 device");
  var draw = ca * wa + cb * wb, g = [];
  if (ca) g.push(_plural(ca, "device", "devices") + " at " + _t(wa) + " W");
  if (cb) g.push(_plural(cb, "device", "devices") + " at " + _t(wb) + " W");
  var pct = Math.floor((2 * draw * 1000 + b) / (2 * b)), p = _t(pct) ;
  var tail;
  if (draw < b) tail = "leaving " + _t(b - draw) + " W spare";
  else if (draw === b) tail = "with nothing spare";
  else tail = "which is " + _t(draw - b) + " W over the budget";
  return "Total draw is " + _t(draw) + " W from " + g.join(" and ") + ". Against a budget of " + _t(b) + " W that is " + p + " percent, " + tail + ".";
}
function spareTruth(budget, drawNow, perDevice) {
  var b = _w(budget, _BERR, 1, 5000);
  var d = _w(drawNow, "the current draw must be from 0 to 5000 W", 0, 5000);
  var w = _w(perDevice, _DERR, 0.1, 100);
  if (d > b) return "The draw of " + _t(d) + " W is already " + _t(d - b) + " W over the budget of " + _t(b) + " W, so no more devices of " + _t(w) + " W fit.";
  var spare = b - d, k = Math.floor(spare / w), left = spare - k * w;
  if (k === 0) return "With a budget of " + _t(b) + " W and " + _t(d) + " W drawn, " + _t(spare) + " W is spare. That is less than one device of " + _t(w) + " W.";
  return "With a budget of " + _t(b) + " W and " + _t(d) + " W drawn, " + _t(spare) + " W is spare. That fits " + _plural(k, "more device", "more devices") + " of " + _t(w) + " W (" + _t(k * w) + " W), leaving " + _t(left) + " W.";
}
function shareTruth(budget, ports) {
  var b = _w(budget, _BERR, 1, 5000);
  var p = _n(ports, "the ports must be a whole number from 1 to 500", 1, 500);
  var s = Math.floor((2 * b + p) / (2 * p));
  return "A budget of " + _t(b) + " W shared evenly over " + _plural(p, "port", "ports") + " is " + _t(s) + " W a port. That is only the average. It says nothing about what any one port is allowed to draw.";
}
