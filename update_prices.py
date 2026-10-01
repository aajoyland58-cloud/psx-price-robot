#!/usr/bin/env python3
"""PSX price robot — fetches live prices from PSX Terminal API and writes to Firebase.
Both the PSX standalone dashboard and the Master PSX tab read these (k_psx_overrides)."""
import requests, time, sys

DB = "https://psx-dashboard-2b391-default-rtdb.asia-southeast1.firebasedatabase.app"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
           "Accept": "application/json"}

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

def fetch_tick(sym):
    """Return (price, changePct) from PSX Terminal, or (None,None)."""
    for attempt in range(2):
        try:
            r = requests.get(f"https://psxterminal.com/api/ticks/REG/{sym}", headers=HEADERS, timeout=20)
            if r.ok:
                j = r.json()
                d = j.get("data", j) if isinstance(j, dict) else j
                if isinstance(d, dict):
                    price = None
                    for k in ("price", "last", "c", "close", "ltp", "currentPrice", "lastPrice"):
                        if d.get(k) not in (None, ""):
                            try: price = float(d[k]); break
                            except (TypeError, ValueError): pass
                    chg = 0.0
                    for k in ("changePercent", "change_pct", "changePct", "pctChange", "change"):
                        if d.get(k) not in (None, ""):
                            try: chg = float(d[k]); break
                            except (TypeError, ValueError): pass
                    if price and price > 0:
                        return price, chg
            time.sleep(1.5)
        except Exception:
            time.sleep(1.5)
    return None, None

def main():
    pf = get_json("/psxShared/k_psx_portfolio.json", [])
    rows = pf if isinstance(pf, list) else (list(pf.values()) if pf else [])
    syms = sorted({(p.get("s") or "").upper() for p in rows if isinstance(p, dict) and p.get("s")})
    # mutual funds / non-PSX-terminal symbols skip (NAV manual)
    SKIP = {"MIF"}
    syms = [s for s in syms if s not in SKIP]
    if not syms:
        print("No PSX symbols in portfolio."); return

    overrides = get_json("/psxShared/k_psx_overrides.json", {}) or {}
    n = 0; fail = []
    for s in syms:
        price, chg = fetch_tick(s)
        if price and price > 0:
            overrides[s] = {"p": round(price, 2), "c": round(chg or 0.0, 2)}
            n += 1
        else:
            fail.append(s)
        time.sleep(0.35)

    put_json("/psxShared/k_psx_overrides.json", overrides)
    put_json("/psxShared/k_psx_updated.json", int(time.time()))
    print(f"Updated {n}/{len(syms)} PSX prices via PSX Terminal.")
    if fail:
        print("Not found:", ", ".join(fail))

if __name__ == "__main__":
    main()
