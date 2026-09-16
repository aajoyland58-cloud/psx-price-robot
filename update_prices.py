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
import time
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

NEWS_RSS = ("https://news.google.com/rss/search?"
            "q=KSE-100%20OR%20%22Pakistan%20Stock%20Exchange%22%20market"
            "&hl=en-PK&gl=PK&ceid=PK:en")


def fetch_news():
    """Latest KSE-100 / PSX news headlines from Google News RSS -> list."""
    out = []
    try:
        r = requests.get(NEWS_RSS, headers=HEADERS, timeout=30)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub = (item.findtext("pubDate") or "").strip()
            if title:
                out.append({"t": title, "u": link, "d": pub})
            if len(out) >= 6:
                break
    except Exception as e:
        print("news warn:", e)
    return out

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

    overrides, universe, day_high, sectors = {}, {}, {}, {}
    for tr in rows:
        tds = tr.find_all("td")
        # SYMBOL,SECTOR,LISTED IN,LDCP,OPEN,HIGH,LOW,CURRENT,CHANGE,CHANGE(%),VOLUME
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
        universe[sym] = listed  # e.g. "ALLSHR,KMI30,KSE100"
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


SYMBOLS_URL = "https://dps.psx.com.pk/symbols"

MUFAP_NAV = "https://www.mufap.com.pk/nav-report.php"
# dashboard symbol -> MUFAP fund name (substring match, UPPERCASE). Add more funds here.
FUND_MAP = {"MIF": "MEEZAN ISLAMIC FUND"}


def fetch_fund_navs():
    """Mutual-fund NAVs from MUFAP daily report -> {SYM: nav}. Best-effort."""
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
    """Per symbol, fetch EOD history from PSX and compute true 52-week high/low.
    Heavy (one request per symbol) — call at most once per day."""
    out = {}
    cutoff = time.time() - 365 * 24 * 3600
    sess = requests.Session()
    sess.headers.update(HEADERS)
    done = 0
    for sym in symbols:
        try:
            r = sess.get(EOD_URL.format(sym), timeout=20)
            if not r.ok:
                continue
            data = r.json()
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
        except Exception:
            continue
    print(f"52-week computed for {done}/{len(symbols)} symbols.")
    return out


def fetch_names():
    """PSX symbols endpoint -> {SYM: company name}. Best-effort (defensive)."""
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
        print("Too few symbols — site may have changed. Aborting.")
        sys.exit(1)

    put_json("/psxShared/k_psx_overrides.json", overrides)
    put_json("/psxShared/k_psx_universe.json", universe)
    print("Wrote prices + universe.")

    # company names + sectors -> k_psx_meta  {SYM:{n:name, s:sector}}
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
            print(f"Wrote meta (names/sectors) for {len(meta)} symbols "
                  f"({len(names)} names, {len(sectors)} sectors).")
    except Exception as e:
        print("meta warn:", e)

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

    # mutual-fund NAVs (MUFAP) -> k_psx_navs  (e.g. Meezan Islamic Fund)
    try:
        fnavs = fetch_fund_navs()
        if fnavs:
            put_json("/psxShared/k_psx_navs.json", fnavs)
            print(f"Wrote fund NAVs: {fnavs}")
        else:
            print("No fund NAVs parsed (funds stay on manual value).")
    except Exception as e:
        print("navs warn:", e)

    # 52-week high/low (real, from EOD history) -> k_psx_52w  · once per ~day (heavy)
    try:
        last52 = get_json("/psxShared/k_psx_52w_updated.json", 0) or 0
        if time.time() - float(last52) > 20 * 3600:
            w52 = fetch_52w(list(overrides.keys()))
            if len(w52) >= 50:
                put_json("/psxShared/k_psx_52w.json", w52)
                put_json("/psxShared/k_psx_52w_updated.json", int(time.time()))
                print(f"Wrote 52-week high/low for {len(w52)} symbols.")
            else:
                print(f"52-week fetch too few ({len(w52)}) — kept old data.")
        else:
            print("52-week data fresh (<20h) — skipped.")
    except Exception as e:
        print("52w warn:", e)

    # market news headlines (Google News RSS) -> k_psx_news  (auto "why" reasons)
    try:
        news = fetch_news()
        if news:
            put_json("/psxShared/k_psx_news.json", news)
            print(f"Wrote {len(news)} news headlines.")
        else:
            print("No news parsed.")
    except Exception as e:
        print("news warn:", e)

    # last-update timestamp (epoch seconds, UTC) — dashboard staleness check
    try:
        put_json("/psxShared/k_psx_updated.json", int(time.time()))
        print("Wrote last-update timestamp.")
    except Exception as e:
        print("updated warn:", e)

    print("Done.")


if __name__ == "__main__":
    main()
