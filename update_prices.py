#!/usr/bin/env python3
"""PSX Price Robot — prices, names, indices, fund NAV, 52-week high/low, freshness.
   v2.1 — faster & timeout-safe 52-week fetch (won't hang the workflow)."""

import re
import sys
import time
import requests
from bs4 import BeautifulSoup

DB = "https://psx-dashboard-2b391-default-rtdb.asia-southeast1.firebasedatabase.app"
MARKET_WATCH = "https://dps.psx.com.pk/market-watch"
INDICES = "https://dps.psx.com.pk/indices"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; psx-dashboard-bot/2.1)"}

# ---- 52-week fetch controls (NEW) ----
W52_PER_REQ_TIMEOUT = 8      # per-symbol network timeout (was 20)
W52_TIME_BUDGET = 180        # max seconds the whole 52w step may run, then stop cleanly
W52_MAX_RETRIES = 1          # quick retry on a failed call, then move on


def to_num(text):
    if text is None:
        return None
    t = text.replace(",", "").replace("%", "").strip()
    try:
        return float(t)
    except ValueError:
        return None


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
    return r.status_code


def fetch_market():
    r = requests.get(MARKET_WATCH, headers=HEADERS, timeout=45)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("table tbody tr") or soup.find_all("tr")

    overrides, universe, day_high, sectors = {}, {}, {}, {}
    for tr in rows:
        tds = tr.find_all("td")
        if len(tds) < 10:
            continue
        sym = tds[0].get_text(strip=True).upper()
        if not re.match(r"^[A-Z][A-Z0-9]{1,11}$", sym):
            continue
        sector = tds[1].get_text(strip=True)
        listed = tds[2].get_text(strip=True)
        ldcp = to_num(tds[3].get_text())
        high = to_num(tds[5].get_text())
        current = to_num(tds[7].get_text())
        chg_pct = to_num(tds[9].get_text())

        price = current if (current and current > 0) else ldcp
        if price is None or price <= 0:
            continue
        overrides[sym] = {"p": round(price, 2), "c": round(chg_pct or 0.0, 2)}
        universe[sym] = listed
        if sector:
            sectors[sym] = sector
        day_high[sym] = max(x for x in [high, current, ldcp] if x) or price
    return overrides, universe, day_high, sectors


def fetch_indices():
    r = requests.get(INDICES, headers=HEADERS, timeout=45)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("table tbody tr") or soup.find_all("tr")
    indices = {}
    for tr in rows:
        tds = tr.find_all("td")
        if len(tds) < 6:
            continue
        name = tds[0].get_text(strip=True).upper()
        if not re.match(r"^[A-Z][A-Z0-9]{2,12}$", name):
            continue
        current = to_num(tds[3].get_text())
        change = to_num(tds[4].get_text())
        pct = to_num(tds[5].get_text())
        if current is None:
            continue
        indices[name] = {"v": current, "c": change or 0.0, "p": pct or 0.0}
    return indices


SYMBOLS_URL = "https://dps.psx.com.pk/symbols"
MUFAP_NAV = "https://www.mufap.com.pk/nav-report.php"
FUND_MAP = {"MIF": "MEEZAN ISLAMIC FUND"}


def fetch_fund_navs():
    navs = {}
    try:
        r = requests.get(MUFAP_NAV, headers=HEADERS, timeout=45)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        rowdata = []
        for tr in soup.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue
            name = tds[0].get_text(" ", strip=True).upper()
            if not name:
                continue
            for td in tds[1:]:
                val = to_num(td.get_text())
                if val is not None and val > 0:
                    rowdata.append((name, val))
                    break
        for sym, target in FUND_MAP.items():
            for name, val in rowdata:
                if target in name:
                    navs[sym] = round(val, 4)
                    break
    except Exception as e:
        print("nav fetch warn:", e)
    return navs


EOD_URL = "https://dps.psx.com.pk/timeseries/eod/{}"


def fetch_52w(symbols):
    """Timeout-safe: reuses one session, short per-request timeout, and stops
    cleanly once the overall time budget is hit so it never hangs the workflow."""
    out = {}
    cutoff = time.time() - 365 * 24 * 3600
    sess = requests.Session()
    sess.headers.update(HEADERS)
    done = 0
    started = time.time()
    stopped_early = False

    for i, sym in enumerate(symbols):
        # NEW: overall time budget guard
        if time.time() - started > W52_TIME_BUDGET:
            stopped_early = True
            print(f"52-week time budget ({W52_TIME_BUDGET}s) reached at "
                  f"{i}/{len(symbols)} — stopping cleanly.")
            break

        data = None
        for attempt in range(W52_MAX_RETRIES + 1):
            try:
                r = sess.get(EOD_URL.format(sym), timeout=W52_PER_REQ_TIMEOUT)
                if r.ok:
                    data = r.json()
                break
            except Exception:
                if attempt >= W52_MAX_RETRIES:
                    data = None
                # else: quick retry once

        if not data:
            continue
        rows = data.get("data") if isinstance(data, dict) else data
        if not rows:
            continue
        hi = lo = None
        for row in rows:
            if not isinstance(row, (list, tuple)) or len(row) < 2:
                continue
            ts, px = row[0], row[1]
            if ts is None or px is None:
                continue
            t = ts / 1000 if ts > 1e12 else ts
            if t < cutoff:
                continue
            try:
                px = float(px)
            except (TypeError, ValueError):
                continue
            if px <= 0:
                continue
            hi = px if hi is None else max(hi, px)
            lo = px if lo is None else min(lo, px)
        if hi:
            out[sym] = {"h": round(hi, 2), "l": round(lo, 2)}
            done += 1

    print(f"52-week computed for {done}/{len(symbols)} symbols"
          f"{' (partial — time budget)' if stopped_early else ''}.")
    return out


def fetch_names():
    names = {}
    try:
        r = requests.get(SYMBOLS_URL, headers=HEADERS, timeout=45)
        r.raise_for_status()
        data = r.json()
        rows = data if isinstance(data, list) else data.get("data", data.get("symbols", []))
        for it in rows:
            if not isinstance(it, dict):
                continue
            sym = (it.get("symbol") or it.get("Symbol") or it.get("sym") or "").upper()
            nm = it.get("name") or it.get("Name") or it.get("companyName") or it.get("company") or ""
            if sym and nm:
                names[sym] = nm.strip()
    except Exception as e:
        print("names warn:", e)
    return names


def main():
    overrides, universe, day_high, sectors = fetch_market()
    print(f"Parsed {len(overrides)} symbols from market-watch.")
    if len(overrides) < 50:
        print("Too few symbols — aborting.")
        sys.exit(1)

    put_json("/psxShared/k_psx_overrides.json", overrides)
    put_json("/psxShared/k_psx_universe.json", universe)
    print("Wrote prices + universe.")

    try:
        names = fetch_names()
        meta = {}
        for s in overrides.keys():
            entry = {}
            if names.get(s):
                entry["n"] = names[s]
            if sectors.get(s):
                entry["s"] = sectors[s]
            if entry:
                meta[s] = entry
        if meta:
            put_json("/psxShared/k_psx_meta.json", meta)
            print(f"Wrote meta for {len(meta)} symbols.")
    except Exception as e:
        print("meta warn:", e)

    try:
        hi = get_json("/psxShared/k_psx_hi.json", {}) or {}
        for s, h in day_high.items():
            prev = hi.get(s, 0) or 0
            hi[s] = round(max(prev, h), 2)
        put_json("/psxShared/k_psx_hi.json", hi)
        print(f"Updated rolling highs for {len(hi)} symbols.")
    except Exception as e:
        print("hi warn:", e)

    try:
        idx = fetch_indices()
        if idx:
            put_json("/psxShared/k_psx_indices.json", idx)
            if "KSE100" in idx:
                put_json("/psxShared/k_psx_kse.json", idx["KSE100"]["v"])
                put_json("/psxShared/k_psx_kseChg.json", idx["KSE100"]["c"])
            print(f"Wrote {len(idx)} indices.")
    except Exception as e:
        print("indices warn:", e)

    try:
        fnavs = fetch_fund_navs()
        if fnavs:
            put_json("/psxShared/k_psx_navs.json", fnavs)
            print(f"Wrote fund NAVs: {fnavs}")
        else:
            print("No fund NAVs parsed.")
    except Exception as e:
        print("navs warn:", e)

    try:
        last52 = get_json("/psxShared/k_psx_52w_updated.json", 0) or 0
        if time.time() - float(last52) > 20 * 3600:
            w52 = fetch_52w(list(overrides.keys()))
            if len(w52) >= 50:
                put_json("/psxShared/k_psx_52w.json", w52)
                put_json("/psxShared/k_psx_52w_updated.json", int(time.time()))
                print(f"Wrote 52-week high/low for {len(w52)} symbols.")
            else:
                print(f"52-week fetch too few ({len(w52)}) — kept old.")
        else:
            print("52-week data fresh (<20h) — skipped.")
    except Exception as e:
        print("52w warn:", e)

    try:
        put_json("/psxShared/k_psx_updated.json", int(time.time()))
        print("Wrote last-update timestamp.")
    except Exception as e:
        print("updated warn:", e)

    print("Done.")


if __name__ == "__main__":
    main()
