<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Master Portfolio Dashboard</title>
<style>
  :root{
    --bg:#0E141C; --bg2:#121A24; --surface:#161F2B; --line:#233246; --line2:#2b3b4f;
    --text:#e8edf3; --muted:#9fb0c4; --muted2:#7d8ea2; --accent:#2f6bff; --up:#4bd07a; --down:#e3595e; --gold:#e6b84a;
    --radius:14px; --mono:'Consolas',ui-monospace,monospace; --body:'Segoe UI',system-ui,Arial,sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--text);font-family:var(--body);font-size:15px;line-height:1.5;
       padding-bottom:env(safe-area-inset-bottom,0px)}
  .wrap{max-width:1240px;margin:0 auto;padding:0 14px 40px}
  a{color:var(--accent)}
  .btn{border:1px solid var(--line2);background:var(--bg2);color:var(--text);border-radius:9px;padding:8px 12px;
       font-size:13px;cursor:pointer;font-family:var(--body)}
  .btn:hover{border-color:var(--accent)}
  .btn.sm{padding:5px 10px;font-size:12px}
  .btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
  .btn.ghost{background:transparent}
  .btn.danger{color:var(--down);border-color:var(--down)}
  .owner-only{display:none}
  body.editor .owner-only{display:inline-flex}
  body.editor p.owner-only{display:block}
  .hide{display:none!important}

  header{padding:16px 0 10px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
  .logo{width:46px;height:46px;border-radius:11px;background:var(--accent);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:22px}
  .htxt h1{margin:0;font-size:22px}
  .htxt p{margin:2px 0 0;font-size:12.5px;color:var(--muted)}
  .hspace{flex:1}
  .lockbox{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--muted)}
  #syncDot{color:var(--up)}

  /* overview strip */
  .ovstrip{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:8px 0 4px}
  .ovcard{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:9px 10px;cursor:pointer}
  .ovcard.act{border-color:var(--accent)}
  .ovcard .k{font-size:11px;color:var(--muted);display:flex;align-items:center;gap:5px}
  .ovcard .k .dot{width:7px;height:7px;border-radius:50%;background:var(--muted2)}
  .ovcard.act .k .dot{background:var(--up)}
  .ovcard .v{font-size:14px;font-weight:700;margin-top:3px;font-family:var(--mono)}
  .ovcard .pl{font-size:11px;font-family:var(--mono)}

  /* tabs */
  .tabs{display:flex;gap:8px;margin:12px 0;flex-wrap:wrap}
  .tabs{display:flex;gap:10px;margin:14px 0;flex-wrap:wrap}
  .tab{background:var(--bg2);border:2px solid var(--line);border-radius:12px;padding:13px 22px;cursor:pointer;
       font-weight:700;font-size:17px;color:var(--text);display:flex;align-items:center;gap:10px;transition:.15s;min-width:120px}
  .tab:hover{transform:translateY(-1px)}
  .tab .tdot{width:12px;height:12px;border-radius:50%;flex:none}
  .tab .tname{line-height:1.1}
  .tab .tname small{display:block;font-size:11px;color:var(--muted2);font-weight:500;margin-top:2px}
  .tab.act{color:#fff}

  .panel{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;margin-bottom:14px}
  .p-head{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 16px;border-bottom:1px solid var(--line);flex-wrap:wrap}
  .p-title{font-weight:700;font-size:15px;display:flex;align-items:center;gap:9px}
  .p-title .bar{width:4px;height:17px;border-radius:2px;background:var(--accent)}
  .p-body{padding:14px 16px}
  .p-note{font-size:12px;color:var(--muted2);margin:8px 0 0}

  .summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
  .stat{background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:11px 13px}
  .stat .k{font-size:11.5px;color:var(--muted)}
  .stat .v{font-size:21px;font-weight:800;margin-top:3px;font-family:var(--mono)}
  .up{color:var(--up)} .down{color:var(--down)} .gold{color:var(--gold)}

  .inc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:10px}
  .inc-bar{height:14px;background:var(--line);border-radius:8px;overflow:hidden}
  .inc-bar span{display:block;height:100%;width:0;background:var(--accent);border-radius:8px;transition:width .4s}

  .scrollx{overflow-x:auto;-webkit-overflow-scrolling:touch}
  table{width:100%;border-collapse:collapse;min-width:640px}
  th{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted2);text-align:right;padding:7px 6px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--surface)}
  th.l,td.l{text-align:left}
  td{padding:8px 6px;border-bottom:1px solid var(--line);font-family:var(--mono);font-size:13px;text-align:right}
  tbody tr:hover{background:#1b2735}
  .sym b{font-family:var(--mono)} .sym span{display:block;font-size:10.5px;color:var(--muted2);font-family:var(--body)}
  .ic{background:none;border:1px solid var(--line2);border-radius:6px;color:var(--muted);cursor:pointer;padding:3px 7px;font-size:12px;margin-left:3px}
  .ic:hover{border-color:var(--accent);color:var(--text)}
  .ic.del:hover{border-color:var(--down);color:var(--down)}
  .empty{color:var(--muted2);text-align:center;padding:22px;font-size:13px}

  .form{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-bottom:12px}
  .form label{font-size:11px;color:var(--muted);display:flex;flex-direction:column;gap:3px}
  .form input,.form select,.modal input,.modal select{background:var(--bg2);border:1px solid var(--line2);border-radius:8px;padding:8px 9px;color:var(--text);font-size:13px;font-family:var(--body)}

  .modal-ov{position:fixed;inset:0;background:rgba(3,7,12,.72);display:none;align-items:center;justify-content:center;z-index:50;padding:14px}
  .modal-ov.show{display:flex}
  .modal{background:var(--surface);border:1px solid var(--line2);border-radius:14px;padding:18px;width:440px;max-width:94vw}
  .modal h3{margin:0 0 12px;font-size:16px}
  .modal .grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .modal label{font-size:11px;color:var(--muted);display:flex;flex-direction:column;gap:3px;margin-bottom:2px}
  .modal-btns{display:flex;justify-content:flex-end;gap:8px;margin-top:14px}
  .prev{font-size:13px;color:var(--muted);margin-top:8px;min-height:18px}

  .mc-box{background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:13.5px}
  .mc-row{display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px dashed var(--line)}
  .mc-row:last-child{border-bottom:none}
  select.msel{background:var(--bg2);border:1px solid var(--line2);border-radius:8px;padding:6px 10px;color:var(--text)}

  .disc{font-size:11.5px;color:var(--muted2);text-align:center;margin:18px 0;line-height:1.6}

  @media(max-width:820px){ .summary,.inc-grid{grid-template-columns:repeat(2,1fr)} .ovstrip{grid-template-columns:repeat(2,1fr)} .form{grid-template-columns:1fr 1fr} }
  @media(max-width:520px){ .summary,.inc-grid,.ovstrip,.form{grid-template-columns:1fr} .p-head{flex-wrap:wrap} .modal .grid2{grid-template-columns:1fr} .htxt h1{font-size:19px} }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="logo">M</div>
    <div class="htxt"><h1>Master Portfolio Dashboard</h1><p class="owner-only">All platforms · one place</p></div>
    <div class="hspace"></div>
    <div class="lockbox"><span id="syncDot">●</span> <span id="syncTxt">Connecting…</span>
      <button class="btn sm" id="lockBtn">🔓 Unlock</button></div>
  </header>

  <div class="ovstrip" id="ovStrip"></div>
  <div class="tabs" id="tabBar"></div>

  <div id="platformView">
  <!-- 5% target -->
  <section class="panel">
    <div class="p-head"><div class="p-title"><span class="bar" style="background:var(--up)"></span>🎯 5% Monthly Target &amp; Incentive <span id="tgtCcy" style="color:var(--muted2);font-weight:500;font-size:12px"></span></div>
      <button class="btn sm owner-only" id="setCapBtn">✎ Set Capital</button></div>
    <div class="p-body">
      <div class="inc-grid">
        <div class="stat"><div class="k">Capital (allocated by boss)</div><div class="v" id="incCap" style="cursor:pointer" title="Click to edit (owner)">—</div></div>
        <div class="stat"><div class="k">5% Monthly Target</div><div class="v" id="incTgt">—</div></div>
        <div class="stat"><div class="k">Realized (this month)</div><div class="v" id="incReal">—</div></div>
        <div class="stat"><div class="k">Incentive (5% of profit)</div><div class="v" id="incAmt">—</div></div>
      </div>
      <div class="inc-bar"><span id="incFill"></span></div>
      <p class="p-note" id="incNote"></p>
    </div>
  </section>

  <!-- portfolio -->
  <section class="panel">
    <div class="p-head">
      <div class="p-title"><span class="bar"></span>Portfolio &amp; P&amp;L <span id="pfCcy" style="color:var(--muted2);font-weight:500;font-size:12px"></span></div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn sm primary owner-only" id="addBuyBtn">＋ Add Buy</button>
        <button class="btn sm primary owner-only" id="impBuyBtn">⬆ Import Buys</button>
        <button class="btn sm primary owner-only" id="autoPxBtn" title="Live prices auto laao (Finnhub/Binance)" style="border-color:var(--up);color:var(--up)">🔄 Auto prices</button>
        <button class="btn sm primary owner-only" id="bulkBtn">⇊ Update prices</button>
      </div>
    </div>
    <div class="p-body">
      <div class="summary" style="margin-bottom:12px">
        <div class="stat"><div class="k">Invested</div><div class="v" id="sInv">—</div></div>
        <div class="stat"><div class="k">Current value</div><div class="v" id="sCur">—</div></div>
        <div class="stat"><div class="k">Total P&L (unrealized)</div><div class="v" id="sPl">—</div></div>
        <div class="stat"><div class="k">Realized P&L (booked)</div><div class="v" id="sRlz">—</div></div>
      </div>
      <div id="brokerSum" class="summary" style="margin-bottom:12px"></div>
      <div class="scrollx"><table id="pfTable">
        <thead><tr><th class="l">Stock</th><th>Qty</th><th>Buy</th><th>Current</th><th>Invested</th><th>Value</th><th>P/L</th><th>%</th><th class="l">Broker</th><th class="l">Date</th><th class="owner-only">Actions</th></tr></thead>
        <tbody id="pfBody"></tbody>
      </table></div>
      <div class="empty" id="pfEmpty">Abhi koi position nahi. <b>＋ Add Buy</b> se shuru karein.</div>
    </div>
  </section>

  <!-- sold history -->
  <section class="panel">
    <div class="p-head">
      <div class="p-title"><span class="bar" style="background:var(--gold)"></span>🧾 Sold History — Realized P&amp;L</div>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <span id="rlzTot" style="font-size:13px;font-weight:700"></span>
        <button class="btn sm" id="dlSaleBtn">⬇ Sale Journal</button>
        <button class="btn sm primary owner-only" id="impSellBtn">⬆ Import Sells</button>
        <button class="btn sm primary owner-only" id="addSellBtn">＋ Add Sell</button>
      </div>
    </div>
    <div class="p-body">
      <div class="scrollx"><table id="rlzTable">
        <thead><tr><th class="l">Date</th><th class="l">Stock</th><th>Qty</th><th>Buy</th><th>Sell</th><th>Invested</th><th>Sold for</th><th>Realized</th><th>%</th><th class="owner-only">Del</th></tr></thead>
        <tbody id="rlzBody"></tbody>
      </table></div>
      <div class="empty" id="rlzEmpty">Abhi koi sold record nahi.</div>
    </div>
  </section>

  <!-- monthly closure -->
  <section class="panel">
    <div class="p-head">
      <div class="p-title"><span class="bar" style="background:var(--accent)"></span>📅 Monthly Closure &amp; Report</div>
      <div style="display:flex;gap:8px;align-items:center">
        <select id="mcMonth" class="msel"></select>
        <button class="btn sm primary" id="mcPdf">⬇ PDF</button>
        <button class="btn sm" id="mcCsv">⬇ CSV</button>
      </div>
    </div>
    <div class="p-body"><div id="mcPrev"></div></div>
  </section>

  </div><!-- /platformView -->

  <div id="summaryView" class="hide">
    <section class="panel">
      <div class="p-head">
        <div class="p-title"><span class="bar" style="background:var(--gold)"></span>📊 All-Platforms Summary</div>
        <div style="display:flex;gap:8px;align-items:center">
          <select id="sumMonth" class="msel"></select>
          <button class="btn sm primary" id="sumPdf2">⬇ Download PDF</button>
        </div>
      </div>
      <div class="p-body"><div class="scrollx"><div id="sumTable"></div></div></div>
    </section>
  </div>

  <p class="disc owner-only">Master Portfolio Dashboard · view-only for management, editable with PIN · multi-platform.
    Realized P&amp;L, Monthly Closure &amp; 5% Target trades se bante hain. Prices manually update hoti hain.
    Sirf informational tool — investment advice nahi.</p>
</div>

<!-- ===== MODALS ===== -->
<div class="modal-ov" id="buyModal"><div class="modal">
  <h3 id="buyTitle">＋ Add Buy</h3>
  <div class="grid2">
    <label>Symbol *<input id="bSym" placeholder="e.g. AAPL"></label>
    <label>Qty *<input id="bQty" type="number" step="any" min="0"></label>
    <label>Buy price *<input id="bCost" type="number" step="any" min="0"></label>
    <label>Current price<input id="bCur" type="number" step="any" min="0"></label>
    <label>Broker / Platform<input id="bPlat" placeholder="e.g. KTrade / AHL"></label>
    <label>Date<input id="bDate" type="date"></label>
    <label>Notes<input id="bNotes" placeholder="optional"></label>
  </div>
  <div class="prev" id="buyPrev"></div>
  <div class="modal-btns"><button class="btn ghost" id="buyCancel">Cancel</button><button class="btn primary" id="buySave">✓ Save</button></div>
</div></div>

<div class="modal-ov" id="sellModal"><div class="modal">
  <h3>₨↓ Sell / Book</h3>
  <div class="prev" id="sellInfo"></div>
  <div class="grid2">
    <label>Qty to sell<input id="sQty" type="number" step="any" min="0"></label>
    <label>Sell price<input id="sPrice" type="number" step="any" min="0"></label>
  </div>
  <div class="prev" id="sellPrev"></div>
  <div class="modal-btns"><button class="btn ghost" id="sellCancel">Cancel</button><button class="btn primary" id="sellConfirm">✓ Confirm sell</button></div>
</div></div>

<div class="modal-ov" id="rlzModal"><div class="modal">
  <h3 id="rlzTitle">✎ Edit sell record</h3>
  <div class="grid2">
    <label>Date<input id="rDate" type="date"></label>
    <label>Symbol<input id="rSym"></label>
    <label>Qty<input id="rQty" type="number" step="any"></label>
    <label>Buy cost<input id="rCost" type="number" step="any"></label>
    <label>Sell price<input id="rSell" type="number" step="any"></label>
  </div>
  <div class="prev" id="rlzPrev"></div>
  <div class="modal-btns"><button class="btn ghost" id="rlzCancel">Cancel</button><button class="btn primary" id="rlzSave">✓ Save</button></div>
</div></div>

<div class="modal-ov" id="impBuyModal"><div class="modal" style="width:560px">
  <h3>⬆ Import Buys (bulk)</h3>
  <p style="font-size:12px;color:var(--muted)">Har line: <b>Date, Ticker, Qty, BuyCost, CurrentPrice</b> (current optional)<br>Misal: <span style="font-family:var(--mono)">2026-07-10, GFS, 15, 69.29, 72.00</span></p>
  <textarea id="impBuyText" style="width:100%;height:200px;background:var(--bg2);border:1px solid var(--line2);border-radius:8px;color:var(--text);padding:10px;font-family:var(--mono);font-size:12px"></textarea>
  <div class="prev" id="impBuyPrev"></div>
  <div class="modal-btns"><button class="btn ghost" id="impBuyCancel">Cancel</button><button class="btn primary" id="impBuyApply">Import</button></div>
</div></div>

<div class="modal-ov" id="impModal"><div class="modal" style="width:560px">
  <h3>⬆ Import Sells (bulk)</h3>
  <p style="font-size:12px;color:var(--muted)">Har line: <b>Date, Ticker, Qty, BuyCost, SellPrice</b><br>Misal: <span style="font-family:var(--mono)">2026-09-01, GPRO, 250, 0.82, 1.496</span></p>
  <textarea id="impText" style="width:100%;height:200px;background:var(--bg2);border:1px solid var(--line2);border-radius:8px;color:var(--text);padding:10px;font-family:var(--mono);font-size:12px"></textarea>
  <div class="prev" id="impPrev"></div>
  <div class="modal-btns"><button class="btn ghost" id="impCancel">Cancel</button><button class="btn primary" id="impApply">Import</button></div>
</div></div>

<div class="modal-ov" id="bulkModal"><div class="modal">
  <h3>⇊ Update prices</h3>
  <p style="font-size:12px;color:var(--muted)">Har line: <b>SYMBOL PRICE</b> — misal: <span style="font-family:var(--mono)">AAPL 232.5</span></p>
  <textarea id="bulkText" style="width:100%;height:150px;background:var(--bg2);border:1px solid var(--line2);border-radius:8px;color:var(--text);padding:10px;font-family:var(--mono);font-size:13px"></textarea>
  <div class="modal-btns"><button class="btn ghost" id="bulkCancel">Cancel</button><button class="btn primary" id="bulkApply">Apply</button></div>
</div></div>

<div class="modal-ov" id="pinModal"><div class="modal">
  <h3>🔒 Unlock editing</h3>
  <label style="font-size:12px;color:var(--muted)">PIN<input id="pinInput" type="password" style="width:100%;margin-top:4px"></label>
  <div class="modal-btns"><button class="btn ghost" id="pinCancel">Cancel</button><button class="btn primary" id="pinOk">Unlock</button></div>
</div></div>

<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-database-compat.js"></script>
<script>
/* ---------- Firebase ---------- */
const firebaseConfig={apiKey:"AIzaSyCKgRUYvRkIYKixL3PjxwuBjghqU6ULrbc",authDomain:"psx-dashboard-2b391.firebaseapp.com",
  databaseURL:"https://psx-dashboard-2b391-default-rtdb.asia-southeast1.firebasedatabase.app",projectId:"psx-dashboard-2b391",
  storageBucket:"psx-dashboard-2b391.firebasestorage.app",messagingSenderId:"481452462694",appId:"1:481452462694:web:f2ad12a4e542ec02fa53a7"};
let db=null;
try{ firebase.initializeApp(firebaseConfig); db=firebase.database(); }catch(e){ console.warn('fb',e); }
const ROOT='psxShared';
const OWNER_PIN='Inam7869';

/* ---------- Platforms ---------- */
const PLATFORMS=[
  {id:'PSX',name:'PSX',sub:'Pakistan · PKR',ccy:'PKR',sym:'Rs',color:'#4bd07a'},
  {id:'SARWA',name:'Sarwa',sub:'Global · USD',ccy:'USD',sym:'$',color:'#2f6bff'},
  {id:'IBKR',name:'IBKR',sub:'US stocks · USD',ccy:'USD',sym:'$',color:'#e6b84a'},
  {id:'BINANCE',name:'Binance',sub:'Crypto · USDT',ccy:'USDT',sym:'$',color:'#f0b90b'},
  {id:'MUBASHER',name:'Mubasher',sub:'Mubasher Capital · USD',ccy:'USD',sym:'$',color:'#a78bfa'},
];
const DEFAULT_PSX_TXLOG=[
  ["2026-03-13","BUY","BAFL",8600,996150.95],
  ["2026-03-13","BUY","FFC",1900,964171.8],
  ["2026-03-13","BUY","NBP",4000,985717.4],
  ["2026-03-13","BUY","OGDC",3500,984884.36],
  ["2026-03-13","BUY","PPL",4700,996514.96],
  ["2026-04-22","BUY","OGDC",200,65694.11],
  ["2026-06-11","BUY","FFC",800,446965.67],
  ["2026-06-11","BUY","JVDC",600,90759.29],
  ["2026-06-11","BUY","MCB",700,284651.66],
  ["2026-06-11","BUY","TPLP",18000,200650.6],
  ["2026-06-11","BUY","WAVESAPP",10500,100406.25],
  ["2026-07-13","BUY","ENGROH",1200,350403.48],
  ["2026-07-13","BUY","SYS",1672,250373.21],
  ["2026-07-13","BUY","ILP",478,50018.02],
  ["2026-07-13","BUY","NML",312,49923.98],
  ["2026-07-13","BUY","FFC",1140,650304.26],
  ["2026-07-13","BUY","MEBL",910,496004.07],
  ["2026-07-13","BUY","FCCL",3385,200229.15],
  ["2026-07-13","BUY","HUBC",2150,500715.67],
  ["2026-07-13","BUY","OGDC",1799,600983.35],
  ["2026-07-13","BUY","MCB",360,149293.49],
  ["2026-07-13","BUY","LUCK",849,400482.02],
  ["2026-07-13","BUY","UBL",1185,550195.02],
  ["2026-07-13","BUY","NBP",1720,349417.7],
  ["2026-07-13","BONUS","BAFL",8600,0],
  ["2026-07-14","SELL","NBP",4000,816733.44],
  ["2026-07-14","SELL","BAFL",17200,997509.18],
  ["2026-07-14","SELL","MCB",700,289094.14],
  ["2026-07-14","BUY","MEBL",4000,2192586.38],
  ["2026-07-14","BUY","MEBL",1945,1069636.17],
  ["2026-07-14","SELL","NBP",1720,355024.91],
  ["2026-07-14","SELL","MCB",360,148427.13],
  ["2026-07-14","SELL","UBL",1185,566100],
  ["2026-07-15","BUY","MIF",12016.7889,2000000],
  ["2026-07-30","BUY","FFC",266,150149.58],
  ["2026-07-30","BUY","MLCF",531,49994.79],
  ["2026-07-30","BUY","OGDC",317,99995.51],
  ["2026-07-30","BUY","LUCK",170,74748.22],
  ["2026-07-30","BUY","MARI",192,124822.95],
  ["2026-08-04","BUY","SEARL",10000,902537.38],
  ["2026-09-07","SELL","OGDC",3690,1216764.34],
  ["2026-09-07","SELL","PPL",4690,1057629.46],
  ["2026-09-07","SELL","TPLP",17990,260090.43],
  ["2026-09-14","BUY","DGKC",7500,1458096.2],
  ["2026-09-14","BUY","FFC",2800,1495660.37],
  ["2026-09-14","BUY","MLCF",15500,1462455.6],
  ["2026-09-14","BUY","SSGC",21000,497205.05],
  ["2026-09-18","SELL","MEBL",2855,1574132.68],
  ["2026-09-21","SELL","DGKC",7500,1477010.36],
  ["2026-09-21","SELL","FFC",5500,2933828.01],
  ["2026-09-21","SELL","MEBL",4000,2200577.64],
  ["2026-09-21","SELL","MLCF",15500,1465394.57],
  ["2026-09-21","SELL","SSGC",21000,505540.77],
  ["2026-09-21","BUY","HUBC",2000,409299.26],
  ["2026-09-21","BUY","MARI",500,318032.69],
  ["2026-09-21","BUY","POL",600,448372.11],
  ["2026-09-21","BUY","SOYASUP",3500,109902.11],
  ["2026-09-22","BUY","INIL",3000,492123],
  ["2026-09-22","BUY","DGKC",4000,792139],
  ["2026-09-22","BUY","APL",1000,579002],
  ["2026-09-22","BUY","OGDC",4000,1275160],
  ["2026-09-22","BUY","SSGC",25000,598755],
  ["2026-09-22","BUY","THCCL",5000,384387],
  ["2026-09-22","BUY","FFC",2500,1351390],
  ["2026-09-22","BUY","PAEL",13000,479661],
  ["2026-09-22","BUY","HCAR",1200,269292],
  ["2026-09-22","BUY","PPL",5000,1146500],
  ["2026-09-28","BUY","NRL",1000,550753.4],
  ["2026-09-28","BUY","PSO",1000,351690.6],
  ["2026-09-28","SELL","INIL",3000,504645.6],
  ["2026-09-28","SELL","PPL",5010,1157789.4],
  ["2026-09-28","SELL","SSGC",25000,603087.5],
  ["2026-09-28","SELL","TPLP",10,123.08],
  ["2026-09-28","SELL","NRL",1000,568100]
];
const PLATSEED={"SARWA":{"portfolio":[{"s":"GOOGL","qty":1,"cost":343.51,"cur":343.51,"platform":"","date":"2026-06-26","notes":""},{"s":"GFS","qty":15,"cost":69.2927,"cur":69.2927,"platform":"","date":"2026-07-10","notes":""},{"s":"NIO","qty":10,"cost":4.98,"cur":4.98,"platform":"","date":"2026-07-10","notes":""},{"s":"MNTS","qty":50,"cost":5.64,"cur":5.64,"platform":"","date":"2026-07-13","notes":""},{"s":"UBER","qty":20,"cost":75.5685,"cur":75.5685,"platform":"","date":"2026-07-13","notes":""},{"s":"ECL","qty":10,"cost":275.044,"cur":275.044,"platform":"","date":"2026-07-27","notes":""},{"s":"XYL","qty":5,"cost":121.14,"cur":121.14,"platform":"","date":"2026-07-27","notes":""},{"s":"BSX","qty":10,"cost":52.341,"cur":52.341,"platform":"","date":"2026-08-18","notes":""},{"s":"IAU","qty":15,"cost":83.6587,"cur":83.6587,"platform":"","date":"2026-08-20","notes":""},{"s":"HIMS","qty":15,"cost":30.8167,"cur":30.8167,"platform":"","date":"2026-08-27","notes":""},{"s":"AAOI","qty":12,"cost":108.455,"cur":108.455,"platform":"","date":"2026-08-27","notes":""},{"s":"NVO","qty":22,"cost":42.0723,"cur":42.0723,"platform":"","date":"2026-08-27","notes":""},{"s":"ALGN","qty":3,"cost":162.3933,"cur":162.3933,"platform":"","date":"2026-08-27","notes":""},{"s":"ZTS","qty":5,"cost":75.55,"cur":75.55,"platform":"","date":"2026-08-27","notes":""},{"s":"TSLA","qty":7,"cost":365.5043,"cur":365.5043,"platform":"","date":"2026-09-10","notes":""},{"s":"VRT","qty":5,"cost":259.226,"cur":259.226,"platform":"","date":"2026-09-10","notes":""},{"s":"DRD","qty":11,"cost":25.3109,"cur":25.3109,"platform":"","date":"2026-09-15","notes":""},{"s":"ISRG","qty":2,"cost":403.005,"cur":403.005,"platform":"","date":"2026-09-22","notes":""},{"s":"NXPI","qty":3,"cost":232.4,"cur":232.4,"platform":"","date":"2026-09-25","notes":""},{"s":"ZS","qty":7,"cost":199.0257,"cur":199.0257,"platform":"","date":"2026-09-28","notes":""},{"s":"OKTA","qty":5,"cost":198.244,"cur":198.244,"platform":"","date":"2026-09-28","notes":""},{"s":"ANET","qty":4,"cost":205.7425,"cur":205.7425,"platform":"","date":"2026-09-28","notes":""},{"s":"FTNT","qty":2,"cost":175.73,"cur":175.73,"platform":"","date":"2026-09-28","notes":""},{"s":"RBLX","qty":28,"cost":42.0986,"cur":42.0986,"platform":"","date":"2026-09-29","notes":""}],"realized":[{"date":"2026-08-26","s":"SPCX","qty":10,"cost":111.268,"sell":136.658,"pnl":253.9,"platform":""},{"date":"2026-08-26","s":"SKHY","qty":15,"cost":142.4667,"sell":159.0813,"pnl":249.22,"platform":""},{"date":"2026-08-27","s":"AMZN","qty":1,"cost":231.55,"sell":255.95,"pnl":24.4,"platform":""},{"date":"2026-08-27","s":"SKM","qty":5,"cost":34.6,"sell":39.4,"pnl":24.0,"platform":""},{"date":"2026-08-27","s":"MSFT","qty":3,"cost":388.63,"sell":503.6267,"pnl":344.99,"platform":""},{"date":"2026-08-27","s":"ACN","qty":3,"cost":140.6967,"sell":188.4067,"pnl":143.13,"platform":""},{"date":"2026-08-27","s":"AEM","qty":1,"cost":145.75,"sell":214.13,"pnl":68.38,"platform":""},{"date":"2026-09-01","s":"GPRO","qty":250,"cost":0.82,"sell":1.496,"pnl":169.0,"platform":""},{"date":"2026-09-03","s":"XE","qty":30,"cost":18.3357,"sell":18.2543,"pnl":-2.44,"platform":""},{"date":"2026-09-04","s":"BE","qty":5,"cost":206.946,"sell":235.41,"pnl":142.32,"platform":""},{"date":"2026-09-04","s":"EWY","qty":1,"cost":176.04,"sell":183.79,"pnl":7.75,"platform":""},{"date":"2026-09-04","s":"RKLB","qty":10,"cost":58.867,"sell":66.264,"pnl":73.97,"platform":""},{"date":"2026-09-08","s":"QCOM","qty":12,"cost":165.5333,"sell":177.415,"pnl":142.58,"platform":""},{"date":"2026-09-09","s":"MP","qty":10,"cost":57.193,"sell":55.551,"pnl":-16.42,"platform":""},{"date":"2026-09-09","s":"USAR","qty":200,"cost":18.2355,"sell":17.3466,"pnl":-177.78,"platform":""},{"date":"2026-09-09","s":"TENX","qty":100,"cost":2.06,"sell":2.145,"pnl":8.5,"platform":""},{"date":"2026-09-10","s":"IAUM","qty":14,"cost":41.857,"sell":44.29,"pnl":34.06,"platform":""},{"date":"2026-09-10","s":"AMBA","qty":10,"cost":64.461,"sell":67.732,"pnl":32.71,"platform":""},{"date":"2026-09-14","s":"PANW","qty":1,"cost":329.56,"sell":363.27,"pnl":33.71,"platform":""},{"date":"2026-09-14","s":"ADBE","qty":3,"cost":250.2133,"sell":262.6533,"pnl":37.32,"platform":""},{"date":"2026-09-15","s":"VLTO","qty":3,"cost":92.9533,"sell":96.4167,"pnl":10.39,"platform":""},{"date":"2026-09-17","s":"GNRC","qty":2.821,"cost":177.632,"sell":228.929,"pnl":144.71,"platform":""},{"date":"2026-09-17","s":"SYM","qty":30,"cost":41.253,"sell":44.3787,"pnl":93.77,"platform":""},{"date":"2026-09-17","s":"AZN","qty":5,"cost":158.856,"sell":164.826,"pnl":29.85,"platform":""},{"date":"2026-09-21","s":"ZS","qty":10,"cost":195.16,"sell":204.537,"pnl":93.77,"platform":""},{"date":"2026-09-22","s":"MCHP","qty":7,"cost":71.5186,"sell":75.0314,"pnl":24.59,"platform":""},{"date":"2026-09-25","s":"TSM","qty":1,"cost":431.96,"sell":452.09,"pnl":20.13,"platform":""},{"date":"2026-09-25","s":"ON","qty":10,"cost":73.724,"sell":77.246,"pnl":35.22,"platform":""},{"date":"2026-09-28","s":"NVDA","qty":17,"cost":221.9947,"sell":230.9112,"pnl":151.58,"platform":""},{"date":"2026-09-28","s":"COST","qty":0.11,"cost":928.545,"sell":921.09,"pnl":-0.82,"platform":""},{"date":"2026-09-29","s":"MCHP","qty":15,"cost":75.7687,"sell":79.3813,"pnl":54.19,"platform":""}]},"IBKR":{"portfolio":[{"s":"IAU","qty":2.5,"cost":87.71,"cur":78.59,"platform":"","date":"2026-09-04","notes":""},{"s":"SAIL","qty":64.5,"cost":21.91,"cur":20.72,"platform":"","date":"2026-09-25","notes":""}],"realized":[{"date":"2026-09-25","s":"ETN","qty":2,"cost":442.54,"sell":446.23,"pnl":7.38,"platform":""},{"date":"2026-09-25","s":"MA","qty":0.1,"cost":606.38,"sell":563.08,"pnl":-4.33,"platform":""},{"date":"2026-09-24","s":"RVTY","qty":3,"cost":142.45,"sell":145.24,"pnl":8.37,"platform":""},{"date":"2026-09-24","s":"SAIL","qty":7,"cost":21.5714,"sell":21.84,"pnl":1.88,"platform":""},{"date":"2026-09-23","s":"CRWD","qty":0.6,"cost":252.417,"sell":259.1,"pnl":4.01,"platform":""},{"date":"2026-09-23","s":"CARR","qty":4,"cost":54.8075,"sell":55.06,"pnl":1.01,"platform":""},{"date":"2026-09-21","s":"KLAC","qty":2,"cost":177.355,"sell":181.17,"pnl":7.63,"platform":""},{"date":"2026-09-21","s":"OUST","qty":8,"cost":35.0425,"sell":36.33,"pnl":10.3,"platform":""},{"date":"2026-09-21","s":"SBGSY","qty":8,"cost":67.2513,"sell":67.45,"pnl":1.59,"platform":""},{"date":"2026-09-17","s":"INTC","qty":5,"cost":105.402,"sell":106.68,"pnl":6.39,"platform":""},{"date":"2026-09-04","s":"NVDA","qty":0.531,"cost":229.849,"sell":233.54,"pnl":1.96,"platform":""}]},"MUBASHER":{"portfolio":[{"s":"AAOI","qty":12,"cost":113.04,"cur":106,"platform":"","date":"2026-08-27","notes":"Applied Optoelectronics"},{"s":"DRD","qty":39,"cost":25.56,"cur":24.39,"platform":"","date":"2026-09-16","notes":"DRDGold"}],"realized":[]},"BINANCE":{"portfolio":[],"realized":[{"date":"2026-08-26","s":"BTC","qty":0.13262,"cost":62725.23,"sell":80569.85,"pnl":2366.55,"platform":"Master"},{"date":"2026-09-18","s":"BTC","qty":0.14562,"cost":76089.77,"sell":79919.97,"pnl":557.75,"platform":"Master"},{"date":"2026-09-19","s":"ETH","qty":0.8269722,"cost":2418.44,"sell":2533.32,"pnl":95.0,"platform":"Master"}]}};
const DEFAULT_CAPITAL={PSX:8014683,IBKR:1525};
let active='PSX';
let canEdit=false;
const state={}; // state[id]={portfolio:[],realized:[]}
PLATFORMS.forEach(p=>state[p.id]={portfolio:[],realized:[],txlog:[],capital:0});

/* ---------- helpers ---------- */
const $=id=>document.getElementById(id);
function P(){ return PLATFORMS.find(p=>p.id===active); }
function money(n){ const s=P().sym; const v=Math.round(Number(n)||0); return s+' '+v.toLocaleString('en-US'); }
function money2(n){ const s=P().sym; return s+' '+(Number(n)||0).toLocaleString('en-US',{maximumFractionDigits:2}); }
function fmt(n){ return (Number(n)||0).toLocaleString('en-US',{maximumFractionDigits:4}); }
function cls(n){ return n>0?'up':(n<0?'down':''); }
function todayStr(){ return new Date().toISOString().slice(0,10); }
function nowYM(){ const d=new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0'); }
function toArr(v){ return Array.isArray(v)?v:(v?Object.values(v):[]); }

/* ---------- storage (Firebase per platform) ---------- */
function key(id,which){
  if(id==='PSX' && which!=='txlog') return `psxShared/k_psx_${which}`;   // SAME as live PSX dashboard
  return `psxShared/m_${id}_${which}`;   // psxShared root (Firebase rules allowed)
}
async function save(id,which){
  if(!db) return;
  try{ await db.ref(key(id,which)).set(state[id][which]); }catch(e){ console.warn('save',e); }
}
function subscribe(){
  if(!db){ $('syncTxt').textContent='Offline (no sync)'; $('syncDot').style.color='var(--down)'; return; }
  PLATFORMS.forEach(p=>{
    ['portfolio','realized','txlog'].forEach(which=>{
      db.ref(key(p.id,which)).on('value',snap=>{
        state[p.id][which]=toArr(snap.val());
        if(p.id===active) renderAll(); renderOverview();
      });
    });
    db.ref(key(p.id,'capital')).on('value',snap=>{ state[p.id].capital=+snap.val()||0; if(p.id===active){renderInc();renderMcMonths();} renderOverview(); });
  });
  // PSX robot prices (k_psx_overrides) — PSX tab auto-price
  db.ref('psxShared/k_psx_overrides').on('value',snap=>{ psxOverrides=snap.val()||{}; if(active==='PSX')renderAll(); renderOverview(); });
  $('syncTxt').textContent='Live · synced'; $('syncDot').style.color='var(--up)';
  // ---- SEED once: saara platform data Firebase mein (agar pehle na daala ho) ----
  db.ref('psxShared/m_seed_v2').once('value').then(async snap=>{
    if(snap.val()) return; // pehle se seeded
    try{
      for(const id in PLATSEED){
        const cur=(state[id]&&state[id].portfolio&&state[id].portfolio.length)||(state[id]&&state[id].realized&&state[id].realized.length);
        if(cur) continue; // us platform ka data pehle se hai to skip
        await db.ref(key(id,'portfolio')).set(PLATSEED[id].portfolio||[]);
        await db.ref(key(id,'realized')).set(PLATSEED[id].realized||[]);
      }
      await db.ref('psxShared/m_seed_v2').set(Date.now());
      console.log('seed done');
    }catch(e){ console.warn('seed warn',e); }
  }).catch(e=>console.warn('seed check',e));
  // ---- Capital seed (independent): default capital agar set nahi ----
  db.ref('psxShared/m_cap_seed_v1').once('value').then(async sn=>{
    if(sn.val()) return;
    try{ for(const cid in DEFAULT_CAPITAL){ const cs=await db.ref(key(cid,'capital')).once('value'); if(!cs.val()) await db.ref(key(cid,'capital')).set(DEFAULT_CAPITAL[cid]); }
      await db.ref('psxShared/m_cap_seed_v1').set(Date.now()); }catch(e){ console.warn('cap seed',e); }
  }).catch(()=>{});
}

/* ---------- computed ---------- */
let psxOverrides={};
function curOf(pos, id){ id=id||active;
  if(id==='PSX' && psxOverrides[pos.s]!=null && +psxOverrides[pos.s]>0) return +psxOverrides[pos.s];
  return (pos.cur!=null && pos.cur!=='')?+pos.cur:+pos.cost; }
function totals(id){
  const pf=state[id].portfolio, rl=state[id].realized;
  let inv=0,cur=0; pf.forEach(p=>{ inv+=p.qty*p.cost; cur+=p.qty*curOf(p,id); });
  const real=rl.reduce((a,r)=>a+(r.sell-r.cost)*r.qty,0);
  const realM=rl.filter(r=>String(r.date||'').slice(0,7)===nowYM()).reduce((a,r)=>a+(r.sell-r.cost)*r.qty,0);
  return {inv,cur,pl:cur-inv,real,realM};
}

/* ---------- overview strip ---------- */
function renderOverview(){
  $('ovStrip').innerHTML=PLATFORMS.map(p=>{
    const t=totals(p.id); const sym=p.sym; const on=p.id===active;
    return `<div class="ovcard ${on?'act':''}" data-tab="${p.id}" style="${on?`border-color:${p.color}`:''}">
      <div class="k"><span class="dot" style="background:${p.color}"></span>${p.name}</div>
      <div class="v">${sym} ${Math.round(t.cur).toLocaleString('en-US')}</div>
      <div class="pl ${cls(t.pl)}">${t.pl>=0?'+':''}${sym} ${Math.round(t.pl).toLocaleString('en-US')}</div>
    </div>`;
  }).join('');
  document.querySelectorAll('.ovcard').forEach(c=>c.onclick=()=>setTab(c.dataset.tab));
}

/* ---------- tabs ---------- */
function renderTabs(){
  const sOn=active==='SUMMARY';
  let html=`<div class="tab ${sOn?'act':''}" data-tab="SUMMARY" style="${sOn?'border-color:var(--gold);background:#e6b84a22;':''}">
    <span class="tdot" style="background:var(--gold)"></span>
    <span class="tname">📊 Summary<small>All platforms</small></span></div>`;
  html+=PLATFORMS.map(p=>{
    const on=p.id===active;
    const style=on?`border-color:${p.color};background:${p.color}22;`:'';
    return `<div class="tab ${on?'act':''}" data-tab="${p.id}" style="${style}">
      <span class="tdot" style="background:${p.color}"></span>
      <span class="tname">${p.name}<small>${p.sub}</small></span>
    </div>`;
  }).join('');
  $('tabBar').innerHTML=html;
  document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>setTab(t.dataset.tab));
}
function setTab(id){
  active=id; brokerFilter=null; renderTabs(); renderOverview();
  if(id==='SUMMARY'){ $('platformView').classList.add('hide'); $('summaryView').classList.remove('hide'); renderSummary(); }
  else { $('summaryView').classList.add('hide'); $('platformView').classList.remove('hide'); renderAll(); }
}
let brokerFilter=null;

/* ---------- render active platform ---------- */
function renderAll(){ renderPortfolio(); renderRealized(); renderInc(); renderMcMonths(); updateCcyLabels(); }
function updateCcyLabels(){ const c='('+P().ccy+')'; $('pfCcy').textContent=c; $('tgtCcy').textContent=c; }

function renderPortfolio(){
  const pf=state[active].portfolio;
  const t=totals(active);
  $('sInv').textContent=money(t.inv); $('sCur').textContent=money(t.cur);
  $('sPl').innerHTML=`<span class="${cls(t.pl)}">${t.pl>=0?'+':''}${money(t.pl)}</span>`;
  $('sRlz').innerHTML=`<span class="${cls(t.real)}">${t.real>=0?'+':''}${money(t.real)}</span>`;
  // broker/sub-account breakdown (group by platform field)
  const groups={};
  pf.forEach(p=>{ const g=p.platform||'—'; if(!groups[g])groups[g]={inv:0,cur:0,n:0}; groups[g].inv+=p.qty*p.cost; groups[g].cur+=p.qty*curOf(p,active); groups[g].n++; });
  const gk=Object.keys(groups);
  if(gk.length>1){
    $('brokerSum').style.display='';
    const allOn=!brokerFilter;
    let cards=`<div class="stat" data-broker="__all" style="cursor:pointer;${allOn?'border-color:var(--accent)':''}"><div class="k">All brokers · ${pf.length} pos</div><div class="v" style="font-size:15px">${money(t.cur)}</div><div style="font-size:12px;font-family:var(--mono)" class="${cls(t.pl)}">${t.pl>=0?'+':''}${money(t.pl)}</div></div>`;
    cards+=gk.map(g=>{const v=groups[g],pl=v.cur-v.inv,plp=v.inv?pl/v.inv*100:0;const on=brokerFilter===g;
      return `<div class="stat" data-broker="${g}" style="cursor:pointer;${on?'border-color:var(--accent)':''}"><div class="k">${g} · ${v.n} pos</div>
        <div class="v" style="font-size:15px">${money(v.cur)}</div>
        <div style="font-size:12px;font-family:var(--mono)" class="${cls(pl)}">${pl>=0?'+':''}${money(pl)} (${plp>=0?'+':''}${plp.toFixed(1)}%)</div></div>`;
    }).join('');
    $('brokerSum').innerHTML=cards;
    $('brokerSum').querySelectorAll('[data-broker]').forEach(el=>el.onclick=()=>{ const b=el.dataset.broker; brokerFilter=(b==='__all')?null:b; renderPortfolio(); });
  } else { $('brokerSum').style.display='none'; $('brokerSum').innerHTML=''; }
  if(!pf.length){ $('pfTable').style.display='none'; $('pfEmpty').style.display='block'; return; }
  $('pfTable').style.display=''; $('pfEmpty').style.display='none';
  $('pfBody').innerHTML=pf.map((p,i)=>{
    if(brokerFilter && (p.platform||'—')!==brokerFilter) return '';
    const c=curOf(p,active), inv=p.qty*p.cost, val=p.qty*c, pl=val-inv, plp=inv?pl/inv*100:0;
    return `<tr>
      <td class="l sym"><b>${p.s}</b>${p.notes?`<span>${p.notes}</span>`:''}</td>
      <td>${(+p.qty).toLocaleString('en-US')}</td>
      <td>${fmt(p.cost)}</td>
      <td>${fmt(c)}</td>
      <td>${money(inv)}</td>
      <td>${money(val)}</td>
      <td class="${cls(pl)}">${pl>=0?'+':''}${money(pl)}</td>
      <td class="${cls(pl)}">${plp>=0?'+':''}${plp.toFixed(1)}%</td>
      <td class="l" style="font-size:11px;color:var(--muted)">${p.platform||'—'}</td>
      <td class="l">${p.date||'—'}</td>
      <td class="owner-only"><button class="ic" data-sell="${i}">₨↓</button><button class="ic" data-edit="${i}">✎</button><button class="ic del" data-del="${i}">✕</button></td>
    </tr>`;
  }).join('');
}

function renderRealized(){
  const rl=state[active].realized;
  const tot=rl.reduce((a,r)=>a+(r.sell-r.cost)*r.qty,0);
  $('rlzTot').innerHTML=rl.length?`Total: <span class="${cls(tot)}">${tot>=0?'+':''}${money(tot)}</span>`:'';
  if(!rl.length){ $('rlzTable').style.display='none'; $('rlzEmpty').style.display='block'; return; }
  $('rlzTable').style.display=''; $('rlzEmpty').style.display='none';
  $('rlzBody').innerHTML=rl.map((r,i)=>{
    const inv=r.cost*r.qty, sold=r.sell*r.qty, pl=(r.sell-r.cost)*r.qty, roi=inv?pl/inv*100:0;
    return `<tr>
      <td class="l">${r.date||''}</td><td class="l sym"><b>${r.s}</b></td>
      <td>${(+r.qty).toLocaleString('en-US')}</td><td>${fmt(r.cost)}</td><td>${fmt(r.sell)}</td>
      <td>${money(inv)}</td><td>${money(sold)}</td>
      <td class="${cls(pl)}">${pl>=0?'+':''}${money(pl)}</td>
      <td class="${cls(pl)}">${roi>=0?'+':''}${roi.toFixed(1)}%</td>
      <td class="owner-only"><button class="ic" data-redit="${i}">✎</button><button class="ic del" data-rdel="${i}">✕</button></td>
    </tr>`;
  }).join('');
}

function renderInc(){
  const t=totals(active);
  const alloc=state[active].capital||0;
  const cap = alloc>0 ? alloc : t.inv;   // boss ka fixed capital (agar set) warna invested
  const real=t.realM, tgt=0.05*cap;
  const inc=real>0?0.05*real:0, pctT=tgt>0?real/tgt*100:0, capPct=cap>0?real/cap*100:0, remain=Math.max(0,tgt-real);
  $('incCap').textContent=money(cap); $('incTgt').textContent=money(tgt);
  $('incReal').innerHTML=`<span class="${cls(real)}">${real>=0?'+':''}${money(real)}</span>`;
  $('incAmt').innerHTML=`<span class="up">${money(inc)}</span>`;
  $('incFill').style.width=Math.max(0,Math.min(100,pctT))+'%';
  $('incFill').style.background=pctT>=100?'var(--up)':'var(--accent)';
  $('incNote').innerHTML=`<b>Is month</b> realized = capital ka <b>${capPct.toFixed(2)}%</b> · 5% target ka <b>${pctT.toFixed(0)}%</b>. `+
    (pctT>=100?`🎉 Target poora! (+${money(real-tgt)})`:`Baaki: <b style="color:var(--gold)">${money(remain)}</b>.`);
}

/* ---------- monthly closure ---------- */
function mcMonths(){
  const ds=[]; state[active].realized.forEach(r=>{ if(r.date) ds.push(String(r.date).slice(0,7)); });
  ds.sort();
  let start = ds.length ? ds[0] : nowYM();
  // start se current month tak continuous
  const [sy,sm]=start.split('-').map(Number);
  const now=new Date(); const ey=now.getFullYear(), em=now.getMonth()+1;
  const out=[]; let y=sy,m=sm;
  // agar start current se pehle nahi to kam se kam 6 month peeche se dikhao
  while(out.length<200 && (y<ey || (y===ey && m<=em))){ out.push(y+'-'+String(m).padStart(2,'0')); m++; if(m>12){m=1;y++;} }
  if(out.length<6){ // thode months guarantee karo
    let by=ey,bm=em;
    while(out.length<6){ bm--; if(bm<1){bm=12;by--;} const k=by+'-'+String(bm).padStart(2,'0'); if(!out.includes(k)) out.push(k); }
  }
  return [...new Set(out)].sort().reverse();
}
function mcLabel(ym){ const M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']; const [y,m]=ym.split('-'); return M[+m-1]+' '+y; }
function renderMcMonths(){
  const cur=$('mcMonth').value; const list=mcMonths();
  $('mcMonth').innerHTML=list.map(m=>`<option value="${m}">${mcLabel(m)}</option>`).join('')+`<option value="all">All months</option>`;
  if(cur && (list.includes(cur)||cur==='all')) $('mcMonth').value=cur;
  renderMcPrev();
}
function mcFromTxlog(ym){
  const tx=(state[active].txlog||[]).slice().sort((a,b)=> a[0]===b[0]?((a[1]==='SELL'?1:0)-(b[1]==='SELL'?1:0)):(a[0]<b[0]?-1:1));
  const inv={}; const val=()=>Object.values(inv).reduce((s,v)=>s+(v.q>1e-9?v.c:0),0);
  let opening=0,buysM=0,sellVal=0,realM=0,openCap=(ym==='all'); const sells=[];
  for(const t of tx){
    const [d,act,sym,qty,amt]=t; const mo=String(d).slice(0,7);
    if(ym!=='all' && !openCap && mo>=ym){ opening=val(); openCap=true; }
    if(ym!=='all' && mo>ym) break;
    const k=sym; if(!inv[k])inv[k]={q:0,c:0};
    const inM=(ym==='all')||(mo===ym);
    if(act==='BUY'){ inv[k].q+=qty; inv[k].c+=amt; if(inM)buysM+=amt; }
    else if(act==='BONUS'){ inv[k].q+=qty; }
    else if(act==='SELL'){ const avg=inv[k].q>0?inv[k].c/inv[k].q:0,co=avg*qty; inv[k].q-=qty; inv[k].c-=co;
      if(inM){ realM+=amt-co; sellVal+=amt; sells.push({date:d,s:sym,qty,cost:avg,sell:amt/qty,pnl:amt-co}); } }
  }
  const closing=val();
  const invList=Object.entries(inv).filter(([k,v])=>v.q>1e-9).map(([k,v])=>({s:k,qty:v.q,cost:v.c/v.q,val:v.c})).sort((a,b)=>b.val-a.val);
  // realized/sellVal realized-array se (broker-correct)
  const rl=state[active].realized;
  const rsel=ym==='all'?rl.slice():rl.filter(r=>String(r.date||'').slice(0,7)===ym);
  const realM2=rsel.reduce((a,r)=>a+(r.sell-r.cost)*r.qty,0);
  const sellVal2=rsel.reduce((a,r)=>a+r.sell*r.qty,0);
  const alloc=state[active].capital||0; const cap=alloc>0?alloc:closing, tgt=0.05*cap;
  return {sells:rsel,realM:realM2,sellVal:sellVal2,buysM,opening,closing,cap,tgt,inc:realM2>0?0.05*realM2:0,remain:Math.max(0,tgt-realM2),inv:invList,invTot:closing};
}
function mcData(ym){
  const tx=state[active].txlog||[];
  if(tx.length){
    const d=mcFromTxlog(ym);
    const liveClose=state[active].portfolio.reduce((a,p)=>a+p.qty*p.cost,0);
    if(Math.abs(d.closing-liveClose) < Math.max(2000, liveClose*0.02)){ d.exact=true; return d; } // 100% date-wise
  }
  // fallback (best-effort) — txlog khaali ho to
  const rl=state[active].realized, pf=state[active].portfolio;
  const sells=ym==='all'?rl.slice():rl.filter(r=>String(r.date||'').slice(0,7)===ym);
  const realM=sells.reduce((a,r)=>a+(r.sell-r.cost)*r.qty,0);
  const sellVal=sells.reduce((a,r)=>a+r.sell*r.qty,0);
  const costSold=sells.reduce((a,r)=>a+r.cost*r.qty,0);
  const closing=pf.reduce((a,p)=>a+p.qty*p.cost,0);
  const buysM=ym==='all'?closing:pf.filter(p=>String(p.date||'').slice(0,7)===ym).reduce((a,p)=>a+p.qty*p.cost,0);
  const opening=ym==='all'?0:Math.max(0, closing - buysM + costSold);
  const alloc=state[active].capital||0; const cap=alloc>0?alloc:closing, tgt=0.05*cap;
  return {sells,realM,sellVal,buysM,opening,closing,cap,tgt,inc:realM>0?0.05*realM:0,remain:Math.max(0,tgt-realM),
          inv:pf.map(p=>({s:p.s,qty:p.qty,cost:p.cost,val:p.qty*p.cost,platform:p.platform||''})), invTot:closing};
}
function renderMcPrev(){
  const ym=$('mcMonth').value; if(!ym)return; const d=mcData(ym);
  const capPct=d.cap?d.realM/d.cap*100:0;
  $('mcPrev').innerHTML=`<div class="mc-box">
    <div class="mc-row"><span>Month</span><b>${ym==='all'?'All months':mcLabel(ym)}</b></div>
    ${d.exact?`<div class="mc-row"><span>Opening inventory</span><b>${money(d.opening)}</b></div>
    <div class="mc-row"><span>Buys (month)</span><b>${money(d.buysM)}</b></div>`:''}
    <div class="mc-row"><span>Capital (invested)</span><b>${money(d.cap)}</b></div>
    <div class="mc-row"><span>Total Sale Value</span><b>${money(d.sellVal)}</b></div>
    <div class="mc-row"><span>5% Target</span><b>${money(d.tgt)}</b> <span style="color:var(--muted2)">(${capPct.toFixed(2)}% done)</span></div>
    <div class="mc-row"><span>Realized P&L (month)</span><b class="${cls(d.realM)}">${d.realM>=0?'+':''}${money(d.realM)}</b></div>
    <div class="mc-row"><span>Target remaining</span><b style="color:var(--gold);font-weight:800">${money(d.remain)}</b></div>
    <div class="mc-row"><span>Incentive (5%)</span><b class="up">${money(d.inc)}</b></div>
    <div class="mc-row"><span>Closing inventory</span><b>${d.inv.length} pos · ${money(d.closing)}</b></div>
  </div>${d.exact?'':'<p class="p-note">Opening / Buys sirf tab dikhte hain jab poora data Master ke through aaye (100% date-wise). Baaki sab exact hai.</p>'}`;
}

/* ---------- edit lock ---------- */
$('lockBtn').onclick=()=>{ if(canEdit){ canEdit=false; document.body.classList.remove('editor'); $('lockBtn').textContent='🔓 Unlock'; renderAll(); } else { $('pinInput').value=''; $('pinModal').classList.add('show'); setTimeout(()=>$('pinInput').focus(),50); } };
$('pinCancel').onclick=()=>$('pinModal').classList.remove('show');
$('pinOk').onclick=()=>{ if($('pinInput').value===OWNER_PIN){ canEdit=true; document.body.classList.add('editor'); $('lockBtn').textContent='🔒 Lock'; $('pinModal').classList.remove('show'); renderAll(); } else alert('Ghalat PIN'); };
$('pinInput').addEventListener('keydown',e=>{ if(e.key==='Enter')$('pinOk').click(); });

/* ---------- Add / Edit Buy ---------- */
let editIdx=-1;
function buyPrev(){ const q=+$('bQty').value||0,c=+$('bCost').value||0; $('buyPrev').textContent=q&&c?`Invested: ${money(q*c)}`:''; }
['bQty','bCost'].forEach(id=>$(id).addEventListener('input',buyPrev));
$('addBuyBtn').onclick=()=>{ if(!canEdit)return; editIdx=-1; $('buyTitle').textContent='＋ Add Buy';
  $('bSym').value='';$('bQty').value='';$('bCost').value='';$('bCur').value='';$('bPlat').value='';$('bDate').value=todayStr();$('bNotes').value=''; buyPrev(); $('buyModal').classList.add('show'); };
$('buyCancel').onclick=()=>$('buyModal').classList.remove('show');
$('buySave').onclick=async()=>{
  const s=$('bSym').value.trim().toUpperCase(),q=+$('bQty').value,c=+$('bCost').value;
  if(!s||!(q>0)||!(c>0)){ alert('Symbol, Qty, Buy price zaroori.'); return; }
  const rec={s,qty:q,cost:c,cur:($('bCur').value!==''?+$('bCur').value:c),platform:$('bPlat').value.trim(),date:$('bDate').value||todayStr(),notes:$('bNotes').value.trim()};
  if(editIdx>=0){ state[active].portfolio[editIdx]=rec; } else { state[active].portfolio.push(rec); await logTxn(active,rec.date,'BUY',rec.s,rec.qty,rec.qty*rec.cost); }
  await save(active,'portfolio'); $('buyModal').classList.remove('show'); renderAll();
};

/* ---------- portfolio row actions ---------- */
let sellIdx=-1;
$('pfBody').addEventListener('click',async e=>{
  if(!canEdit)return;
  const ed=e.target.closest('[data-edit]'), dl=e.target.closest('[data-del]'), sl=e.target.closest('[data-sell]');
  if(ed){ const i=+ed.dataset.edit; const p=state[active].portfolio[i]; editIdx=i; $('buyTitle').textContent='✎ Edit position';
    $('bSym').value=p.s;$('bQty').value=p.qty;$('bCost').value=p.cost;$('bCur').value=(p.cur!=null?p.cur:'');$('bPlat').value=p.platform||'';$('bDate').value=p.date||'';$('bNotes').value=p.notes||''; buyPrev(); $('buyModal').classList.add('show'); return; }
  if(dl){ const i=+dl.dataset.del; if(confirm('Ye position delete karein?')){ state[active].portfolio.splice(i,1); await save(active,'portfolio'); renderAll(); } return; }
  if(sl){ sellIdx=+sl.dataset.sell; const p=state[active].portfolio[sellIdx];
    $('sellInfo').textContent=`${p.s} — held ${(+p.qty).toLocaleString('en-US')} @ ${fmt(p.cost)}`;
    $('sQty').value=p.qty;$('sPrice').value=curOf(p); sellPrev(); $('sellModal').classList.add('show'); }
});
function sellPrev(){ if(sellIdx<0)return; const p=state[active].portfolio[sellIdx]; const q=+$('sQty').value||0,sp=+$('sPrice').value||0;
  const pl=(sp-p.cost)*q; $('sellPrev').innerHTML=q&&sp?`Realized: <b class="${cls(pl)}">${pl>=0?'+':''}${money(pl)}</b>`:''; }
['sQty','sPrice'].forEach(id=>$(id).addEventListener('input',sellPrev));
$('sellCancel').onclick=()=>$('sellModal').classList.remove('show');
$('sellConfirm').onclick=async()=>{
  if(sellIdx<0)return; const p=state[active].portfolio[sellIdx]; const q=+$('sQty').value,sp=+$('sPrice').value;
  if(!(q>0)||!(sp>0)||q>p.qty){ alert('Qty/price theek daalein (qty holding se zyada nahi).'); return; }
  const sd=todayStr();
  state[active].realized.unshift({date:sd,s:p.s,qty:q,cost:p.cost,sell:sp,pnl:(sp-p.cost)*q});
  if(q>=p.qty) state[active].portfolio.splice(sellIdx,1); else p.qty-=q;
  await logTxn(active,sd,'SELL',p.s,q,q*sp);
  await save(active,'portfolio'); await save(active,'realized'); $('sellModal').classList.remove('show'); renderAll();
};

/* ---------- sold history actions ---------- */
let rEdit=-1;
$('rlzBody').addEventListener('click',async e=>{
  if(!canEdit)return;
  const ed=e.target.closest('[data-redit]'), dl=e.target.closest('[data-rdel]');
  if(ed){ openRlz(+ed.dataset.redit); return; }
  if(dl){ const i=+dl.dataset.rdel; if(confirm('Record delete karein?')){ state[active].realized.splice(i,1); await save(active,'realized'); renderAll(); } }
});
function rlzPrev(){ const q=+$('rQty').value||0,c=+$('rCost').value||0,s=+$('rSell').value||0; const pl=(s-c)*q; $('rlzPrev').innerHTML=q?`Realized: <b class="${cls(pl)}">${pl>=0?'+':''}${money(pl)}</b>`:''; }
['rQty','rCost','rSell'].forEach(id=>$(id).addEventListener('input',rlzPrev));
function openRlz(i){ rEdit=i; const r=i>=0?state[active].realized[i]:{};
  $('rlzTitle').textContent=i>=0?'✎ Edit sell record':'＋ Add sell record';
  $('rDate').value=r.date||todayStr();$('rSym').value=r.s||'';$('rQty').value=r.qty||'';$('rCost').value=(r.cost!=null?r.cost:'');$('rSell').value=(r.sell!=null?r.sell:''); rlzPrev(); $('rlzModal').classList.add('show'); }
$('addSellBtn').onclick=()=>{ if(!canEdit)return; openRlz(-1); };
$('rlzCancel').onclick=()=>$('rlzModal').classList.remove('show');
$('rlzSave').onclick=async()=>{
  const s=$('rSym').value.trim().toUpperCase(),q=+$('rQty').value,c=+$('rCost').value,sp=+$('rSell').value;
  if(!s||!(q>0)||$('rCost').value===''||$('rSell').value===''){ alert('Sab fields theek daalein.'); return; }
  const rec={date:$('rDate').value||todayStr(),s,qty:q,cost:c,sell:sp,pnl:(sp-c)*q};
  if(rEdit>=0) state[active].realized[rEdit]=rec;
  else { state[active].realized.unshift(rec);
    await logTxn(active,rec.date,'SELL',s,q,q*sp);
    const idx=state[active].portfolio.findIndex(p=>p.s===s);
    if(idx>=0 && state[active].portfolio[idx].qty>=q){ if(state[active].portfolio[idx].qty===q) state[active].portfolio.splice(idx,1); else state[active].portfolio[idx].qty-=q; await save(active,'portfolio'); }
  }
  await save(active,'realized'); $('rlzModal').classList.remove('show'); renderAll();
};

/* ---------- bulk price ---------- */
$('bulkBtn').onclick=()=>{ if(!canEdit)return; $('bulkText').value=''; $('bulkModal').classList.add('show'); };$('bulkCancel').onclick=()=>$('bulkModal').classList.remove('show');
$('bulkApply').onclick=async()=>{
  const lines=$('bulkText').value.split('\n'); let n=0;
  lines.forEach(ln=>{ const m=ln.trim().replace(',',' ').split(/\s+/); if(m.length>=2){ const sym=m[0].toUpperCase(),pr=+m[1];
    if(sym&&pr>0){ state[active].portfolio.forEach(p=>{ if(p.s===sym){ p.cur=pr; n++; } }); } } });
  await save(active,'portfolio'); $('bulkModal').classList.remove('show'); renderAll(); alert(n+' prices update huin.');
};

/* ---------- sale journal CSV ---------- */
$('dlSaleBtn').onclick=()=>{
  const rl=state[active].realized; if(!rl.length){ alert('Koi sold record nahi.'); return; }
  const hdr=['S.No','Date','Symbol','Qty','Buy Price','Cost Basis','Sell Price','Net Proceeds','Realized P/L','ROI %'];
  const rows=rl.map((r,i)=>{ const inv=r.cost*r.qty,sold=r.sell*r.qty,pl=(r.sell-r.cost)*r.qty,roi=inv?pl/inv*100:0;
    return [i+1,r.date||'',r.s,r.qty,(+r.cost).toFixed(4),Math.round(inv),(+r.sell).toFixed(4),Math.round(sold),Math.round(pl),roi.toFixed(1)+'%']; });
  const csv=[hdr,...rows].map(row=>row.map(c=>`"${String(c).replace(/"/g,'""')}"`).join(',')).join('\r\n');
  dl(new Blob(['\ufeff'+csv],{type:'text/csv'}),`${active}-Sale-Journal.csv`);
};
function dl(blob,name){ const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); a.remove(); }

/* ---------- monthly closure export ---------- */
$('mcMonth').onchange=renderMcPrev;
$('mcCsv').onclick=()=>{
  const ym=$('mcMonth').value,d=mcData(ym),esc=v=>`"${String(v).replace(/"/g,'""')}"`;
  const L=[[active+' Monthly Closure',ym==='all'?'All':mcLabel(ym)],[],
    ['Opening Inventory',Math.round(d.opening)],['Buys (month)',Math.round(d.buysM)],['Realized P&L',Math.round(d.realM)],['Total Sale Value',Math.round(d.sellVal)],['Capital',Math.round(d.cap)],
    ['5% Target',Math.round(d.tgt)],['Target remaining',Math.round(d.remain)],['Incentive (5%)',Math.round(d.inc)],[],
    ['SELLS'],['Date','Symbol','Qty','Buy','Sell','Realized']];
  d.sells.forEach(r=>L.push([r.date||'',r.s,r.qty,(+r.cost).toFixed(4),(+r.sell).toFixed(4),Math.round((r.sell-r.cost)*r.qty)]));
  const csv=L.map(row=>row.map(esc).join(',')).join('\r\n');
  dl(new Blob(['\ufeff'+csv],{type:'text/csv'}),`${active}-Closure-${ym}.csv`);
};
$('mcPdf').onclick=()=>{
  const ym=$('mcMonth').value,d=mcData(ym),sym=P().sym,now=new Date();
  const rows=d.sells.map(r=>{const pl=(r.sell-r.cost)*r.qty,inv=r.cost*r.qty,roi=inv?pl/inv*100:0;
    return `<tr><td>${r.date||''}</td><td>${r.s}</td><td>${r.platform||'—'}</td><td style="text-align:right">${(+r.qty).toLocaleString()}</td><td style="text-align:right">${fmt(r.cost)}</td><td style="text-align:right">${fmt(r.sell)}</td><td style="text-align:right;color:${pl>=0?'#1a7f37':'#c1121f'}">${pl>=0?'+':''}${sym} ${Math.round(pl).toLocaleString()}</td><td style="text-align:right">${roi>=0?'+':''}${roi.toFixed(1)}%</td></tr>`;}).join('')||'<tr><td colspan="8" style="text-align:center;color:#888">Koi sell nahi</td></tr>';
  const inv=d.inv.map(x=>`<tr><td>${x.s}</td><td>${x.platform||'—'}</td><td style="text-align:right">${(+x.qty).toLocaleString()}</td><td style="text-align:right">${fmt(x.cost)}</td><td style="text-align:right">${sym} ${Math.round(x.val).toLocaleString()}</td></tr>`).join('');
  const w=window.open('','_blank'); if(!w){alert('Popup allow karein');return;}
  w.document.write(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>${active} Closure ${ym}</title><style>
    body{font-family:'Segoe UI',Arial;color:#1a1a1a;padding:30px 38px;font-size:13px}h1{color:#1a3d6d;font-size:19px;margin:0}
    .sub{color:#666;font-size:12px;margin:3px 0 14px}.cards{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}
    .card{flex:1;min-width:130px;border:1px solid #dcdcdc;border-radius:8px;padding:9px 11px}.card .k{font-size:11px;color:#666}.card .v{font-size:15px;font-weight:700;margin-top:2px}
    table{width:100%;border-collapse:collapse;margin:8px 0 16px;font-size:12px}th,td{border:1px solid #dcdcdc;padding:6px 8px;text-align:left}th{background:#eef2f7}
    h3{color:#1a3d6d;font-size:14px;margin:14px 0 5px}.foot{color:#999;font-size:10px;margin-top:20px;border-top:1px solid #e2e2e2;padding-top:7px}</style></head><body>
    <h1>${P().name} — Monthly Closure — ${ym==='all'?'All Months':mcLabel(ym)}</h1>
    <div class="sub">${P().ccy} · Generated ${now.toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'})}</div>
    <div class="cards">
      ${d.exact?`<div class="card"><div class="k">Opening Inventory</div><div class="v">${sym} ${Math.round(d.opening).toLocaleString()}</div></div>
      <div class="card"><div class="k">Buys (month)</div><div class="v">${sym} ${Math.round(d.buysM).toLocaleString()}</div></div>`:''}
      <div class="card"><div class="k">Capital (invested)</div><div class="v">${sym} ${Math.round(d.cap).toLocaleString()}</div></div>
      <div class="card"><div class="k">Total Sale Value</div><div class="v">${sym} ${Math.round(d.sellVal).toLocaleString()}</div></div>
    </div>
    <div class="cards">
      <div class="card"><div class="k">5% Target</div><div class="v">${sym} ${Math.round(d.tgt).toLocaleString()}</div></div>
      <div class="card"><div class="k">Realized P&L (month)</div><div class="v" style="color:${d.realM>=0?'#1a7f37':'#c1121f'}">${d.realM>=0?'+':''}${sym} ${Math.round(d.realM).toLocaleString()}</div></div>
      <div class="card"><div class="k">Target remaining</div><div class="v" style="color:#c79a2e">${sym} ${Math.round(d.remain).toLocaleString()}</div></div>
      <div class="card"><div class="k">Incentive (5%)</div><div class="v" style="color:#1a7f37">${sym} ${Math.round(d.inc).toLocaleString()}</div></div>
    </div>
    <h3>Sells booked (${d.sells.length})</h3>
    <table><thead><tr><th>Date</th><th>Stock</th><th>Platform</th><th style="text-align:right">Qty</th><th style="text-align:right">Buy</th><th style="text-align:right">Sell</th><th style="text-align:right">Realized</th><th style="text-align:right">ROI%</th></tr></thead><tbody>${rows}</tbody></table>
    <h3>Closing Inventory — carry-forward (${d.inv.length} pos · ${sym} ${Math.round(d.closing).toLocaleString()})</h3>
    <table><thead><tr><th>Stock</th><th>Platform</th><th style="text-align:right">Qty</th><th style="text-align:right">Avg Cost</th><th style="text-align:right">Cost Value</th></tr></thead><tbody>${inv}</tbody></table>
    <div class="foot">Realized = booked profit · Incentive = 5% of realized · Closing inventory carry-forward. Informational only, not investment advice.</div>
  </body></html>`);
  w.document.close(); w.focus(); setTimeout(()=>{try{w.print();}catch(e){}},500);
};


/* ---------- ALL-PLATFORMS SUMMARY ---------- */
function sumMonthList(){
  const ds=[]; PLATFORMS.forEach(p=>state[p.id].realized.forEach(r=>{ if(r.date) ds.push(String(r.date).slice(0,7)); }));
  ds.sort(); let start=ds.length?ds[0]:nowYM();
  const [sy,sm]=start.split('-').map(Number); const now=new Date(),ey=now.getFullYear(),em=now.getMonth()+1;
  const out=[]; let y=sy,m=sm; while(out.length<200&&(y<ey||(y===ey&&m<=em))){ out.push(y+'-'+String(m).padStart(2,'0')); m++; if(m>12){m=1;y++;} }
  let by=ey,bm=em; while(out.length<6){ bm--; if(bm<1){bm=12;by--;} const k=by+'-'+String(bm).padStart(2,'0'); if(!out.includes(k))out.push(k); }
  return [...new Set(out)].sort().reverse();
}
function mLabel(ym){ if(ym==='all')return'All Months'; const M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']; const[a,b]=ym.split('-'); return M[+b-1]+' '+a; }
function sumRows(ym){
  return PLATFORMS.map(p=>{
    const pf=state[p.id].portfolio, rl=state[p.id].realized;
    let inv=0,cur=0; pf.forEach(x=>{inv+=x.qty*x.cost;cur+=x.qty*((x.cur!=null&&x.cur!=='')?+x.cur:+x.cost);});
    const sells=ym==='all'?rl:rl.filter(r=>String(r.date||'').slice(0,7)===ym);
    const realM=sells.reduce((a,r)=>a+(r.sell-r.cost)*r.qty,0);
    const alloc=state[p.id].capital||0; const capBase=alloc>0?alloc:inv; const tgt=0.05*capBase;
    return {p,inv,cur,unpl:cur-inv,roi:inv?((cur-inv)/inv*100):0,realM,tgt,inc:realM>0?0.05*realM:0,remain:Math.max(0,tgt-realM),pos:pf.length};
  });
}
function renderSummary(){
  const cur=$('sumMonth').value; const list=sumMonthList();
  $('sumMonth').innerHTML=list.map(m=>`<option value="${m}">${mLabel(m)}</option>`).join('')+`<option value="all">All months</option>`;
  if(cur&&(list.includes(cur)||cur==='all'))$('sumMonth').value=cur;
  const ym=$('sumMonth').value||nowYM(); const rows=sumRows(ym);
  const money0=(sym,n)=>sym+' '+Math.round(n).toLocaleString('en-US');
  const body=rows.map(r=>{const sym=r.p.sym;
    return `<tr>
      <td class="l" style="font-weight:700"><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${r.p.color};margin-right:6px"></span>${r.p.name}</td>
      <td class="l">${r.p.ccy}</td>
      <td>${money0(sym,r.inv)}</td><td>${money0(sym,r.cur)}</td>
      <td class="${cls(r.unpl)}">${r.unpl>=0?'+':''}${money0(sym,r.unpl)}</td>
      <td class="${cls(r.roi)}">${r.roi>=0?'+':''}${r.roi.toFixed(1)}%</td>
      <td class="${cls(r.realM)}">${r.realM>=0?'+':''}${money0(sym,r.realM)}</td>
      <td>${money0(sym,r.tgt)}</td>
      <td style="color:var(--gold)">${money0(sym,r.remain)}</td>
      <td class="up">${money0(sym,r.inc)}</td>
      <td>${r.pos}</td></tr>`;
  }).join('');
  // currency subtotals
  const byC={}; rows.forEach(r=>{const c=r.p.ccy; byC[c]=byC[c]||{sym:r.p.sym,inv:0,cur:0,real:0}; byC[c].inv+=r.inv;byC[c].cur+=r.cur;byC[c].real+=r.realM;});
  const subs=Object.entries(byC).map(([c,v])=>{const roi=v.inv?((v.cur-v.inv)/v.inv*100):0;
    return `<tr style="background:#1b2735;font-weight:700">
    <td class="l">TOTAL</td><td class="l">${c}</td><td>${v.sym} ${Math.round(v.inv).toLocaleString()}</td><td>${v.sym} ${Math.round(v.cur).toLocaleString()}</td>
    <td class="${cls(v.cur-v.inv)}">${(v.cur-v.inv)>=0?'+':''}${v.sym} ${Math.round(v.cur-v.inv).toLocaleString()}</td>
    <td class="${cls(roi)}">${roi>=0?'+':''}${roi.toFixed(1)}%</td>
    <td class="${cls(v.real)}">${v.real>=0?'+':''}${v.sym} ${Math.round(v.real).toLocaleString()}</td><td colspan="4"></td></tr>`;}).join('');
  $('sumTable').innerHTML=`<table style="min-width:880px"><thead><tr>
    <th class="l">Platform</th><th class="l">Ccy</th><th>Invested</th><th>Current</th><th>Unrealized</th><th>ROI %</th><th>Realized (mo)</th><th>5% Target</th><th>Remaining</th><th>Incentive</th><th>Pos</th>
    </tr></thead><tbody>${body}${subs}</tbody></table>`;
}
$('sumMonth').onchange=renderSummary;

function generateSummaryPDF(ym){
  const rows=sumRows(ym), now=new Date();
  const f=(sym,n)=>sym+' '+Math.round(n).toLocaleString('en-US'), g=x=>x>=0?'#1a7f37':'#c1121f';
  const body=rows.map(r=>`<tr>
    <td style="font-weight:700"><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${r.p.color};margin-right:6px"></span>${r.p.name}</td>
    <td>${r.p.ccy}</td><td style="text-align:right">${f(r.p.sym,r.inv)}</td><td style="text-align:right">${f(r.p.sym,r.cur)}</td>
    <td style="text-align:right;color:${g(r.unpl)}">${r.unpl>=0?'+':''}${f(r.p.sym,r.unpl)}</td>
    <td style="text-align:right;color:${g(r.roi)}">${r.roi>=0?'+':''}${r.roi.toFixed(1)}%</td>
    <td style="text-align:right;color:${g(r.realM)}">${r.realM>=0?'+':''}${f(r.p.sym,r.realM)}</td>
    <td style="text-align:right">${f(r.p.sym,r.tgt)}</td><td style="text-align:right;color:#c79a2e">${f(r.p.sym,r.remain)}</td>
    <td style="text-align:right;color:#1a7f37">${f(r.p.sym,r.inc)}</td><td style="text-align:right">${r.pos}</td></tr>`).join('');
  const byC={}; rows.forEach(r=>{const c=r.p.ccy;byC[c]=byC[c]||{sym:r.p.sym,inv:0,cur:0,real:0};byC[c].inv+=r.inv;byC[c].cur+=r.cur;byC[c].real+=r.realM;});
  const subs=Object.entries(byC).map(([c,v])=>{const roi=v.inv?((v.cur-v.inv)/v.inv*100):0;
    return `<tr style="background:#eef2f7;font-weight:700"><td>TOTAL (${c})</td><td>${c}</td>
    <td style="text-align:right">${v.sym} ${Math.round(v.inv).toLocaleString()}</td><td style="text-align:right">${v.sym} ${Math.round(v.cur).toLocaleString()}</td>
    <td style="text-align:right;color:${g(v.cur-v.inv)}">${(v.cur-v.inv)>=0?'+':''}${v.sym} ${Math.round(v.cur-v.inv).toLocaleString()}</td>
    <td style="text-align:right;color:${g(roi)}">${roi>=0?'+':''}${roi.toFixed(1)}%</td>
    <td style="text-align:right;color:${g(v.real)}">${v.real>=0?'+':''}${v.sym} ${Math.round(v.real).toLocaleString()}</td><td colspan="4"></td></tr>`;}).join('');
  const w=window.open('','_blank'); if(!w){alert('Popup allow karein');return;}
  w.document.write(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>All-Platforms Summary ${ym}</title><style>
    body{font-family:'Segoe UI',Arial;color:#1a1a1a;padding:26px 32px;font-size:12.5px}h1{color:#1a3d6d;font-size:20px;margin:0}
    .sub{color:#666;font-size:12px;margin:3px 0 14px}table{width:100%;border-collapse:collapse;font-size:11.5px}
    th,td{border:1px solid #dcdcdc;padding:6px 7px;text-align:left}th{background:#1a3d6d;color:#fff;font-size:10.5px}
    .foot{color:#999;font-size:10px;margin-top:18px;border-top:1px solid #e2e2e2;padding-top:7px}</style></head><body>
    <h1>Master Portfolio — All-Platforms Summary</h1>
    <div class="sub">Month: <b>${mLabel(ym)}</b> · Generated ${now.toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'})}</div>
    <table><thead><tr><th>Platform</th><th>Ccy</th><th style="text-align:right">Invested</th><th style="text-align:right">Current</th><th style="text-align:right">Unrealized</th><th style="text-align:right">ROI %</th><th style="text-align:right">Realized (mo)</th><th style="text-align:right">5% Target</th><th style="text-align:right">Remaining</th><th style="text-align:right">Incentive</th><th style="text-align:right">Pos</th></tr></thead>
    <tbody>${body}${subs}</tbody></table>
    <div class="foot">Har platform apni currency mein. Realized = booked profit · Incentive = 5% of realized · Target = 5% of allocated capital (boss) — ya invested agar capital set nahi. Informational only, not investment advice.</div>
  </body></html>`);
  w.document.close(); w.focus(); setTimeout(()=>{try{w.print();}catch(e){}},500);
}
$('sumPdf2').onclick=()=>generateSummaryPDF($('sumMonth').value||nowYM());


/* ---------- transaction log (date-wise) ---------- */
async function logTxn(id,date,act,sym,qty,amt){
  if(!state[id].txlog) state[id].txlog=[];
  state[id].txlog.push([date,act,sym,+qty,+amt]);
  await save(id,'txlog');
}

/* ---------- Import Buys (bulk) ---------- */
function parseImpBuys(text){
  const out=[];
  text.split('\n').forEach(ln=>{
    ln=ln.trim(); if(!ln||/^date/i.test(ln))return;
    const c=ln.split(/[\t,]/).map(x=>x.replace(/\$/g,'').replace(/,/g,'').trim());
    if(c.length<4)return;
    const date=c[0], s=(c[1]||'').toUpperCase(), qty=+c[2], cost=+c[3];
    const cur=(c.length>=5 && c[4]!=='')?+c[4]:cost;
    const acc=(c.length>=6 && c[5]!=='')?c[5]:'';
    if(s && qty>0 && cost>0) out.push({s,qty,cost,cur,platform:acc,date,notes:''});
  });
  return out;
}
if($('impBuyBtn')){
  $('impBuyBtn').onclick=()=>{ if(!canEdit)return; $('impBuyText').value=''; $('impBuyPrev').textContent=''; $('impBuyModal').classList.add('show'); };
  $('impBuyText').addEventListener('input',()=>{ const r=parseImpBuys($('impBuyText').value); const inv=r.reduce((a,x)=>a+x.qty*x.cost,0); $('impBuyPrev').innerHTML=r.length?`${r.length} buys · Invested: <b>${money(inv)}</b>`:'Rows paste karein…'; });
  $('impBuyCancel').onclick=()=>$('impBuyModal').classList.remove('show');
  $('impBuyApply').onclick=async()=>{
    const r=parseImpBuys($('impBuyText').value);
    if(!r.length){ alert('Koi valid row nahi.'); return; }
    if(!confirm(`${r.length} buys import karein? Invested ${money(r.reduce((a,x)=>a+x.qty*x.cost,0))}`)) return;
    r.forEach(x=>state[active].portfolio.push(x));
    await save(active,'portfolio'); $('impBuyModal').classList.remove('show'); renderAll();
    alert(r.length+' buys import ho gayin.');
  };
}

/* ---------- Import Sells (bulk) ---------- */
function parseImpSells(text){
  const out=[];
  text.split('\n').forEach(ln=>{
    ln=ln.trim(); if(!ln||/^date/i.test(ln))return;
    const c=ln.split(/[\t,]/).map(x=>x.replace(/\$/g,'').replace(/,/g,'').trim());
    if(c.length<5)return;
    const date=c[0], s=(c[1]||'').toUpperCase(), qty=+c[2], cost=+c[3], sell=+c[4];
    const acc=(c.length>=6 && c[5]!=='')?c[5]:'';
    if(s && qty>0 && cost>=0 && sell>=0) out.push({date,s,qty,cost,sell,pnl:(sell-cost)*qty,platform:acc});
  });
  return out;
}
if($('impSellBtn')){
  $('impSellBtn').onclick=()=>{ if(!canEdit)return; $('impText').value=''; $('impPrev').textContent=''; $('impModal').classList.add('show'); };
  $('impText').addEventListener('input',()=>{ const r=parseImpSells($('impText').value); const tot=r.reduce((a,x)=>a+x.pnl,0); $('impPrev').innerHTML=r.length?`${r.length} sells · Realized: <b class="${cls(tot)}">${tot>=0?'+':''}${money(tot)}</b>`:'Rows paste karein…'; });
  $('impCancel').onclick=()=>$('impModal').classList.remove('show');
  $('impApply').onclick=async()=>{
    const r=parseImpSells($('impText').value);
    if(!r.length){ alert('Koi valid row nahi mili.'); return; }
    if(!confirm(`${r.length} sells import karein? Realized ${money(r.reduce((a,x)=>a+x.pnl,0))}`)) return;
    r.forEach(x=>state[active].realized.unshift(x));
    await save(active,'realized'); $('impModal').classList.remove('show'); renderAll();
    alert(r.length+' sells import ho gayin.');
  };
}


/* ---------- Set allocated capital (boss) ---------- */
async function editCapital(){
  if(!canEdit)return;
  const curv=state[active].capital||0;
  const v=prompt(`${P().name} ka allocated capital (boss se mila) — ${P().ccy}:`, curv||'');
  if(v===null)return;
  const num=+String(v).replace(/[^0-9.]/g,'');
  if(!(num>=0)){ alert('Theek number daalein.'); return; }
  state[active].capital=num;
  try{ await db.ref(key(active,'capital')).set(num); }catch(e){ console.warn(e); }
  renderInc(); renderMcMonths(); renderOverview();
  alert(`${P().name} capital set: ${money(num)}`);
}
if($('setCapBtn')) $('setCapBtn').onclick=editCapital;
if($('incCap')) $('incCap').onclick=()=>{ if(canEdit) editCapital(); };

/* ---------- AUTO PRICES (Finnhub US stocks + Binance crypto) ---------- */
let FINNHUB_KEY='dav0q29r01qrjdu8c6hgdav0q29r01qrjdu8c6i0';
if(db){ db.ref('psxShared/m_finnhub_key').once('value').then(sn=>{ if(sn.val()) FINNHUB_KEY=sn.val(); }).catch(()=>{}); }
async function autoPrices(){
  if(!canEdit)return;
  const pf=state[active].portfolio; if(!pf.length){ alert('Is tab mein koi holding nahi.'); return; }
  const isCrypto=(active==='BINANCE');
  if(active!=='PSX' && !isCrypto && !FINNHUB_KEY){
    const k=prompt('US stock prices ke liye FREE Finnhub API key daalein (finnhub.io par free account -> API key):','');
    if(k===null)return; const kk=(k||'').trim();
    if(!kk){ alert('Key zaroori hai US stocks ke liye.'); return; }
    FINNHUB_KEY=kk; try{ await db.ref('psxShared/m_finnhub_key').set(kk); }catch(e){}
  }
  const btn=$('autoPxBtn'); btn.textContent='⏳ Fetching…'; btn.disabled=true;
  let n=0, fail=0;
  for(const p of pf){
    try{
      let price=null;
      if(active==='PSX'){
        // PSX Terminal free API (CORS-proxy fallback ke saath)
        const urls=['https://psxterminal.com/api/ticks/REG/'+encodeURIComponent(p.s),
                    'https://corsproxy.io/?url='+encodeURIComponent('https://psxterminal.com/api/ticks/REG/'+p.s),
                    'https://api.allorigins.win/raw?url='+encodeURIComponent('https://psxterminal.com/api/ticks/REG/'+p.s)];
        for(const u of urls){
          try{ const r=await fetch(u); if(r.ok){ const j=await r.json(); const d=j.data||j;
            const px=d.price??d.last??d.c??d.close??d.ltp; if(+px>0){ price=+px; break; } } }catch(e){}
        }
      } else if(isCrypto){
        const sym=p.s.replace(/USDT$/,'')+'USDT';
        const r=await fetch('https://api.binance.com/api/v3/ticker/price?symbol='+sym);
        if(r.ok){ const j=await r.json(); if(+j.price>0) price=+j.price; }
      } else {
        const r=await fetch('https://finnhub.io/api/v1/quote?symbol='+encodeURIComponent(p.s)+'&token='+FINNHUB_KEY);
        if(r.ok){ const j=await r.json(); if(+j.c>0) price=+j.c; }
      }
      if(price>0){ p.cur=price; n++; } else fail++;
    }catch(e){ fail++; }
  }
  await save(active,'portfolio'); renderAll();
  btn.textContent='🔄 Auto prices'; btn.disabled=false;
  alert(n+' prices update huin'+(fail?(', '+fail+' nahi mili'):'')+'.');
}
if($('autoPxBtn')) $('autoPxBtn').onclick=autoPrices;

/* ---------- boot ---------- */
renderTabs(); renderOverview(); renderAll(); subscribe();
</script>
</body>
</html>
