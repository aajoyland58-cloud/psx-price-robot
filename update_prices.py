#!/usr/bin/env python3
# PSX price robot — fetches live PSX prices and writes to Firebase (k_psx_overrides)
import json, time, urllib.request

FB = "https://psx-dashboard-2b391-default-rtdb.asia-southeast1.firebasedatabase.app"

def http_get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")

def http_post(url, payload, timeout=30):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data,
          headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")

def http_put(url, payload, timeout=20):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data,
          headers={"Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")

def get_symbols():
    """Read current PSX holdings from Firebase; skip MIF (mutual fund)."""
    try:
        pf = json.loads(http_get(FB + "/psxShared/k_psx_portfolio.json") or "[]") or []
        syms = sorted({str(h.get("s", "")).upper() for h in pf
                       if h.get("s") and str(h.get("s")).upper() != "MIF"})
        return [s for s in syms if s]
    except Exception as e:
        print("symbol read failed:", e)
        return []

def fetch_prices(symbols):
    """Fetch last prices from the TradingView scanner for PSX."""
    out = {}
    if not symbols:
        return out
    url = "https://scanner.tradingview.com/pakistan/scan"
    payload = {"symbols": {"tickers": ["PSX:" + s for s in symbols], "query": {"types": []}},
               "columns": ["close"]}
    try:
        res = json.loads(http_post(url, payload))
        for row in res.get("data", []):
            sym = str(row.get("s", "")).split(":")[-1].upper()
            vals = row.get("d", [])
            if sym and vals and vals[0]:
                out[sym] = {"p": float(vals[0])}
    except Exception as e:
        print("TradingView fetch failed:", e)
    return out

def main():
    syms = get_symbols()
    print("symbols:", len(syms))
    ov = fetch_prices(syms)
    if ov:
        http_put(FB + "/psxShared/k_psx_overrides.json", ov)
        http_put(FB + "/psxShared/k_psx_updated.json", int(time.time() * 1000))
        print(f"{len(ov)} PSX prices updated")
    else:
        print("no prices fetched — overrides left unchanged")

if __name__ == "__main__":
    main()
