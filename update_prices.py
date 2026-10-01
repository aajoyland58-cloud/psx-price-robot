#!/usr/bin/env python3
"""PSX price robot — daily close prices to Firebase (k_psx_overrides).
Primary: PSX DPS EOD endpoint. Fallback: PSX Terminal API. Read by PSX dashboard + Master PSX tab."""
import requests, time

DB = "https://psx-dashboard-2b391-default-rtdb.asia-southeast1.firebasedatabase.app"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
           "Accept": "application/json,text/plain,*/*",
           "Referer": "https://dps.psx.com.pk/"}
SESS = requests.Session(); SESS.headers.update(HEADERS)

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

def fetch_eod(sym):
    """Latest close from PSX DPS EOD timeseries."""
    try:
        r = SESS.get(f"https://dps.psx.com.pk/timeseries/eod/{sym}", timeout=25)
        if not r.ok:
            return None
        j = r.json()
        rows = j.get("data") if isinstance(j, dict) else j
        if not rows:
            return None
        best_ts, best_px = -1, None
        for row in rows:
            if isinstance(row, (list, tuple)) and len(row) >= 2 and row[0] is not None and row[1] is not None:
                try:
                    ts = float(row[0]); px = float(row[1])
                except (TypeError, ValueError):
                    continue
                if px > 0 and ts > best_ts:
                    best_ts, best_px = ts, px
        return best_px
    except Exception:
        return None

def fetch_terminal(sym):
    try:
        r = SESS.get(f"https://psxterminal.com/api/ticks/REG/{sym}", timeout=20)
        if r.ok:
            j = r.json(); d = j.get("data", j) if isinstance(j, dict) else j
            if isinstance(d, dict):
                for k in ("price","last","c","close","ltp","currentPrice","lastPrice"):
                    if d.get(k) not in (None, ""):
                        try: return float(d[k])
                        except (TypeError, ValueError): pass
    except Exception:
        pass
    return None

def main():
    pf = get_json("/psxShared/k_psx_portfolio.json", [])
    rows = pf if isinstance(pf, list) else (list(pf.values()) if pf else [])
    syms = sorted({(p.get("s") or "").upper() for p in rows if isinstance(p, dict) and p.get("s")})
    syms = [s for s in syms if s not in {"MIF"}]
    print(f"Portfolio symbols: {len(syms)} -> {syms}")
    if not syms:
        print("No PSX symbols found in k_psx_portfolio. Robot exiting.")
        return

    overrides = get_json("/psxShared/k_psx_overrides.json", {}) or {}
    n = 0; fail = []
    for s in syms:
        px = fetch_eod(s)
        src = "EOD"
        if not (px and px > 0):
            px = fetch_terminal(s); src = "Terminal"
        if px and px > 0:
            overrides[s] = {"p": round(px, 2), "c": 0.0}
            n += 1
            print(f"  {s}: {px} ({src})")
        else:
            fail.append(s)
        time.sleep(0.4)

    put_json("/psxShared/k_psx_overrides.json", overrides)
    put_json("/psxShared/k_psx_updated.json", int(time.time()))
    print(f"Updated {n}/{len(syms)} PSX prices.")
    if fail:
        print("Not found:", ", ".join(fail))

if __name__ == "__main__":
    main()
