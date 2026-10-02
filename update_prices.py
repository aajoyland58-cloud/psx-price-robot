#!/usr/bin/env python3
"""PSX price robot — TradingView scanner API se live prices Firebase mein (k_psx_overrides).
PSX dashboard + Master PSX tab dono isi se prices lete hain."""
import requests, time

DB = "https://psx-dashboard-2b391-default-rtdb.asia-southeast1.firebasedatabase.app"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
           "Content-Type": "application/json",
           "Origin": "https://www.tradingview.com",
           "Referer": "https://www.tradingview.com/"}

def get_json(path, default):
    try:
        r = requests.get(DB + path, timeout=30)
        if r.ok and r.text and r.text != "null":
            return r.json()
    except Exception as e:
        print("GET warn:", e)
    return default

def put_json(path, data):
    r = requests.put(DB + path, json=data, timeout=45)
    r.raise_for_status()

def fetch_tradingview(syms):
    """TradingView scanner — ek hi call mein saare PSX symbols."""
    out = {}
    tickers = ["PSX:" + s for s in syms]
    body = {"symbols": {"tickers": tickers, "query": {"types": []}},
            "columns": ["close", "change"]}
    try:
        r = requests.post("https://scanner.tradingview.com/pakistan/scan",
                          json=body, headers=HEADERS, timeout=30)
        print("TradingView HTTP", r.status_code)
        if r.ok:
            data = r.json().get("data", [])
            for item in data:
                s = item.get("s", "")           # "PSX:OGDC"
                d = item.get("d", [])
                sym = s.split(":")[-1]
                if sym and d and d[0] and float(d[0]) > 0:
                    out[sym] = {"p": round(float(d[0]), 2),
                                "c": round(float(d[1]) if len(d) > 1 and d[1] is not None else 0.0, 2)}
        else:
            print("TradingView body:", r.text[:200])
    except Exception as e:
        print("TradingView error:", e)
    return out

def main():
    pf = get_json("/psxShared/k_psx_portfolio.json", [])
    rows = pf if isinstance(pf, list) else (list(pf.values()) if pf else [])
    syms = sorted({(p.get("s") or "").upper() for p in rows if isinstance(p, dict) and p.get("s")})
    syms = [s for s in syms if s not in {"MIF"}]
    print(f"Portfolio symbols: {len(syms)} -> {syms}")
    if not syms:
        print("No PSX symbols found. Exiting.")
        return

    prices = fetch_tradingview(syms)
    overrides = get_json("/psxShared/k_psx_overrides.json", {}) or {}
    n = 0; fail = []
    for s in syms:
        if s in prices:
            overrides[s] = prices[s]; n += 1
            print(f"  {s}: {prices[s]['p']}")
        else:
            fail.append(s)

    put_json("/psxShared/k_psx_overrides.json", overrides)
    put_json("/psxShared/k_psx_updated.json", int(time.time()))
    print(f"Updated {n}/{len(syms)} PSX prices via TradingView.")
    if fail:
        print("Not found:", ", ".join(fail))

if __name__ == "__main__":
    main()
