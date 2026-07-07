#!/usr/bin/env python3
"""
PSX Price Robot (v2)
--------------------
Every run it fetches from the official PSX Data Portal and writes to your
Firebase Realtime Database (dashboard reads it live, for everyone):

  * ALL stock prices + day change%      -> k_psx_overrides
  * Index membership per stock          -> k_psx_universe   (for KSE100/KMI30 tabs)
  * ALL indices (KSE100, KMI30, ...)    -> k_psx_indices
  * KSE-100 value + change              -> k_psx_kse , k_psx_kseChg
  * Rolling high per stock (for dips)   -> k_psx_hi

No secrets needed: DB URL is public and rules allow writes to 'psxShared'.
"""

import re
import sys
import requests
from bs4 import BeautifulSoup

DB = "https://psx-dashboard-2b391-default-rtdb.asia-southeast1.firebasedatabase.app"
MARKET_WATCH = "https://dps.psx.com.pk/market-watch"
INDICES = "https://dps.psx.com.pk/indices"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; psx-dashboard-bot/2.0)"}


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

    overrides, universe, day_high = {}, {}, {}
    for tr in rows:
        tds = tr.find_all("td")
        # SYMBOL,SECTOR,LISTED IN,LDCP,OPEN,HIGH,LOW,CURRENT,CHANGE,CHANGE(%),VOLUME
        if len(tds) < 10:
            continue
        sym = tds[0].get_text(strip=True).upper()
        if not re.match(r"^[A-Z][A-Z0-9]{1,11}$", sym):
            continue
        listed = tds[2].get_text(strip=True)
        ldcp = to_num(tds[3].get_text())
        high = to_num(tds[5].get_text())
        current = to_num(tds[7].get_text())
        chg_pct = to_num(tds[9].get_text())

        price = current if (current and current > 0) else ldcp
        if price is None or price <= 0:
            continue
        overrides[sym] = {"p": round(price, 2), "c": round(chg_pct or 0.0, 2)}
        universe[sym] = listed  # e.g. "ALLSHR,KMI30,KSE100"
        day_high[sym] = max(x for x in [high, current, ldcp] if x) or price
    return overrides, universe, day_high


def fetch_indices():
    r = requests.get(INDICES, headers=HEADERS, timeout=45)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    rows = soup.select("table tbody tr") or soup.find_all("tr")
    indices = {}
    for tr in rows:
        tds = tr.find_all("td")
        # Index, High, Low, Current, Change, % Change
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


def main():
    overrides, universe, day_high = fetch_market()
    print(f"Parsed {len(overrides)} symbols from market-watch.")
    if len(overrides) < 50:
        print("Too few symbols — site may have changed. Aborting.")
        sys.exit(1)

    put_json("/psxShared/k_psx_overrides.json", overrides)
    put_json("/psxShared/k_psx_universe.json", universe)
    print("Wrote prices + universe.")

    # rolling high (for dip alerts) — merge with what we've seen before
    try:
        hi = get_json("/psxShared/k_psx_hi.json", {}) or {}
        for s, h in day_high.items():
            prev = hi.get(s, 0) or 0
            hi[s] = round(max(prev, h), 2)
        put_json("/psxShared/k_psx_hi.json", hi)
        print(f"Updated rolling highs for {len(hi)} symbols.")
    except Exception as e:
        print("hi warn:", e)

    # indices
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

    print("Done.")


if __name__ == "__main__":
    main()
