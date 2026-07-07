#!/usr/bin/env python3
"""
PSX Price Robot
---------------
Fetches current prices + day change% for ALL PSX symbols from the official
PSX Data Portal market-watch page, and writes them into your Firebase
Realtime Database. Your dashboard reads this automatically (live, for everyone
incl. your boss) — no manual typing needed.

Runs on a schedule via GitHub Actions (see .github/workflows/prices.yml).
No secrets needed: your DB URL is public and rules already allow writes to
the 'psxShared' node.
"""

import re
import sys
import requests
from bs4 import BeautifulSoup

# ---- your Firebase Realtime Database ----
DB = "https://psx-dashboard-2b391-default-rtdb.asia-southeast1.firebasedatabase.app"
OVERRIDES_PATH = "/psxShared/k_psx_overrides.json"   # matches the dashboard's storage key

MARKET_WATCH = "https://dps.psx.com.pk/market-watch"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; psx-dashboard-bot/1.0)"}


def to_num(text):
    if text is None:
        return None
    t = text.replace(",", "").replace("%", "").strip()
    try:
        return float(t)
    except ValueError:
        return None


def fetch_prices():
    r = requests.get(MARKET_WATCH, headers=HEADERS, timeout=45)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tbody tr") or soup.find_all("tr")
    overrides = {}

    for tr in rows:
        tds = tr.find_all("td")
        # Columns: SYMBOL,SECTOR,LISTED IN,LDCP,OPEN,HIGH,LOW,CURRENT,CHANGE,CHANGE(%),VOLUME
        if len(tds) < 10:
            continue
        sym = tds[0].get_text(strip=True).upper()
        if not re.match(r"^[A-Z][A-Z0-9]{1,11}$", sym):
            continue
        ldcp = to_num(tds[3].get_text())
        current = to_num(tds[7].get_text())
        chg_pct = to_num(tds[9].get_text())

        price = current if (current and current > 0) else ldcp
        if price is None or price <= 0:
            continue
        overrides[sym] = {"p": round(price, 2), "c": round(chg_pct or 0.0, 2)}

    return overrides


def main():
    overrides = fetch_prices()
    print(f"Parsed {len(overrides)} symbols from PSX market-watch.")

    # safety: don't overwrite with a broken/empty scrape
    if len(overrides) < 50:
        print("Too few symbols parsed — site structure may have changed. Aborting.")
        sys.exit(1)

    resp = requests.put(DB + OVERRIDES_PATH, json=overrides, timeout=45)
    resp.raise_for_status()
    print(f"OK: wrote {len(overrides)} prices to Firebase (HTTP {resp.status_code}).")


if __name__ == "__main__":
    main()
