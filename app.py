import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FCF & Earnings Quality Analyser",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# CSS — Professional White Theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=DM+Serif+Display:ital@0;1&display=swap');

.stApp { background:#F7F8FC; color:#0F172A; font-family:'DM Sans',sans-serif; }

/* Geometric background */
.stApp::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background-image:
        radial-gradient(circle at 6% 10%,  rgba(29,78,216,0.055) 0%, transparent 40%),
        radial-gradient(circle at 94% 82%, rgba(5,150,105,0.045) 0%, transparent 36%),
        radial-gradient(circle at 52% 48%, rgba(124,58,237,0.025) 0%, transparent 55%);
}
.stApp::after {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background-image:
        linear-gradient(rgba(29,78,216,0.032) 1px, transparent 1px),
        linear-gradient(90deg, rgba(29,78,216,0.032) 1px, transparent 1px);
    background-size:52px 52px;
}
section[data-testid="stSidebar"], .main .block-container { position:relative; z-index:1; }
.block-container { padding-top:2rem !important; padding-bottom:3rem !important; }

/* Hero */
.hero {
    background:linear-gradient(118deg,#1E3A8A 0%,#1D4ED8 48%,#0EA5E9 100%);
    border-radius:18px; padding:2.8rem 3rem; margin-bottom:2rem;
    text-align:center; position:relative; overflow:hidden;
    box-shadow:0 8px 40px rgba(30,58,138,0.18);
}
.hero::before {
    content:''; position:absolute; width:360px; height:360px; border-radius:50%;
    border:1.5px solid rgba(255,255,255,0.09); top:-100px; left:-70px;
}
.hero::after {
    content:''; position:absolute; width:240px; height:240px; border-radius:50%;
    border:1.5px solid rgba(255,255,255,0.07); bottom:-75px; right:6%;
}
.hero h1 {
    font-family:'DM Serif Display',serif; font-size:2.25rem; font-weight:400;
    color:#fff; margin:0 0 0.55rem; letter-spacing:-0.4px;
    text-shadow:0 2px 14px rgba(0,0,0,0.14);
}
.hero p { color:rgba(255,255,255,0.76); font-size:0.95rem; margin:0; letter-spacing:0.02em; }

/* KPI Cards */
.kpi {
    background:#fff; border:1px solid #E2E8F0; border-radius:14px;
    padding:1.35rem 1.2rem 1.15rem; text-align:center;
    transition:all 0.22s ease; box-shadow:0 1px 6px rgba(15,23,42,0.05);
    position:relative; overflow:hidden;
}
.kpi::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background:linear-gradient(90deg,#1D4ED8,#0EA5E9); border-radius:14px 14px 0 0;
}
.kpi:hover { border-color:#BFDBFE; box-shadow:0 6px 24px rgba(29,78,216,0.10); transform:translateY(-3px); }
.kpi-val { font-size:1.8rem; font-weight:700; color:#1E3A8A; line-height:1.1; margin-bottom:0.25rem; }
.kpi-lbl { color:#64748B; font-size:0.70rem; text-transform:uppercase; letter-spacing:0.09em; font-weight:600; margin-top:0.2rem; }
.kpi-sub { font-size:0.72rem; margin-top:0.32rem; font-weight:500; }
.pos { color:#059669; } .neg { color:#DC2626; } .neu { color:#D97706; }

/* Section headers */
.sec {
    background:linear-gradient(90deg,#EFF6FF,#F8FAFC);
    border-left:4px solid #1D4ED8; padding:0.9rem 1.3rem;
    margin:2rem 0 1.2rem; border-radius:0 10px 10px 0;
    box-shadow:0 1px 4px rgba(29,78,216,0.06);
}
.sec h3 { color:#1E3A8A; font-size:1.0rem; font-weight:700; margin:0; }
.sec p  { color:#64748B; font-size:0.79rem; margin:0.2rem 0 0; }

/* Tables */
.mt { width:100%; border-collapse:separate; border-spacing:0; font-size:0.845rem;
      border-radius:10px; overflow:hidden; box-shadow:0 1px 8px rgba(15,23,42,0.07); }
.mt th { background:#1E3A8A; color:#fff; padding:0.72rem 1.05rem;
         text-align:left; font-weight:600; font-size:0.78rem; letter-spacing:0.04em; text-transform:uppercase; }
.mt td { padding:0.62rem 1.05rem; border-bottom:1px solid #F1F5F9; color:#0F172A;
         background:#fff; line-height:1.5; }
.mt tr:nth-child(even) td { background:#F8FAFC; }
.mt tr:last-child td { border-bottom:none; }
.mt tr:hover td { background:#EFF6FF; }
.mt-total td { background:#EFF6FF !important; font-weight:700 !important; border-top:2px solid #BFDBFE; }

/* Cards */
.flag-red {
    border-radius:12px; padding:1.25rem 1.5rem; margin:0.8rem 0;
    border:1px solid #FECACA; background:linear-gradient(135deg,#FFF5F5,#FEF2F2);
    box-shadow:0 1px 6px rgba(220,38,38,0.07);
}
.flag-red h4 { color:#B91C1C; margin:0 0 0.5rem; font-size:0.93rem; font-weight:700; }
.flag-red p  { color:#374151; margin:0; font-size:0.85rem; line-height:1.8; }
.flag-amber {
    border-radius:12px; padding:1.25rem 1.5rem; margin:0.8rem 0;
    border:1px solid #FDE68A; background:linear-gradient(135deg,#FFFBEB,#FEF3C7);
    box-shadow:0 1px 6px rgba(217,119,6,0.07);
}
.flag-amber h4 { color:#92400E; margin:0 0 0.5rem; font-size:0.93rem; font-weight:700; }
.flag-amber p  { color:#374151; margin:0; font-size:0.85rem; line-height:1.8; }
.flag-green {
    border-radius:12px; padding:1.25rem 1.5rem; margin:0.8rem 0;
    border:1px solid #A7F3D0; background:linear-gradient(135deg,#F0FDF4,#ECFDF5);
    box-shadow:0 1px 6px rgba(5,150,105,0.07);
}
.flag-green h4 { color:#065F46; margin:0 0 0.5rem; font-size:0.93rem; font-weight:700; }
.flag-green p  { color:#374151; margin:0; font-size:0.85rem; line-height:1.8; }

/* Insight box */
.insight {
    background:#EFF6FF; border:1px solid #BFDBFE; border-left:4px solid #2563EB;
    border-radius:0 10px 10px 0; padding:1.05rem 1.4rem; margin:1.1rem 0;
    font-size:0.875rem; line-height:1.85; color:#1E3A8A;
}
.insight strong { color:#1D4ED8; font-weight:700; }

/* Actual vs Implied callout */
.vs-box { display:flex; gap:1rem; margin:1rem 0; }
.vs-actual { flex:1; background:#EFF6FF; border:2px solid #1D4ED8; border-radius:12px; padding:1.2rem 1.4rem; text-align:center; }
.vs-implied { flex:1; background:#F0FDF4; border:2px solid #059669; border-radius:12px; padding:1.2rem 1.4rem; text-align:center; }
.vs-lbl { font-size:0.70rem; text-transform:uppercase; letter-spacing:0.09em; font-weight:700; margin-bottom:0.45rem; }
.vs-actual .vs-lbl { color:#1D4ED8; } .vs-implied .vs-lbl { color:#059669; }
.vs-num { font-size:2.1rem; font-weight:800; line-height:1; }
.vs-actual .vs-num { color:#1E3A8A; } .vs-implied .vs-num { color:#065F46; }
.vs-sub { font-size:0.77rem; margin-top:0.35rem; color:#64748B; }

/* Tabs */
div[data-testid="stTabs"] button {
    background:transparent !important; color:#64748B !important;
    border:none !important; border-bottom:2px solid transparent !important;
    padding:0.75rem 1.3rem !important; font-weight:600 !important; font-size:0.875rem !important;
}
div[data-testid="stTabs"] button:hover { color:#1D4ED8 !important; }
div[data-testid="stTabs"] button[aria-selected="true"] {
    color:#1D4ED8 !important; border-bottom:2px solid #1D4ED8 !important;
}

/* Sidebar */
.stSidebar > div { background:#fff; border-right:1px solid #E2E8F0; }
div[data-testid="stExpander"] { border:1px solid #E2E8F0; border-radius:10px; background:#fff; }
label { color:#374151 !important; font-weight:500 !important; }
div[data-testid="stFileUploader"] { border:2px dashed #BFDBFE; border-radius:12px; background:#F8FAFC; }

/* Footer */
.footer-bar {
    background:#fff; border-top:1px solid #E2E8F0; border-radius:12px;
    padding:1.2rem 2rem; text-align:center; margin-top:2.5rem;
    color:#64748B; font-size:0.80rem;
}
.footer-bar strong { color:#1D4ED8; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────
C = {
    "blue":"#1D4ED8", "sky":"#0EA5E9", "emerald":"#059669",
    "rose":"#DC2626", "amber":"#D97706", "violet":"#7C3AED",
    "navy":"#1E3A8A", "slate":"#64748B",
}

BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#0F172A", size=12),
    margin=dict(l=44, r=44, t=52, b=44),
    legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#E2E8F0", borderwidth=1),
    title_font=dict(family="DM Sans", color="#1E3A8A", size=14),
)

def sc(fig, h=380):
    fig.update_layout(**BASE, height=h)
    fig.update_xaxes(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0",
                     showline=True, linecolor="#E2E8F0")
    fig.update_yaxes(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0", showline=False)
    return fig


# ─────────────────────────────────────────────────────────────
# FORMATTERS
# ─────────────────────────────────────────────────────────────
nan = float("nan")

def fm(v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "N/A"
    if abs(v) >= 1000: return f"${v/1000:.1f}B"
    return f"${v:,.0f}M"

def fx(v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "N/A"
    return f"{v:.1f}×"

def fp(v, signed=False):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "N/A"
    s = "+" if signed and v > 0 else ""
    return f"{s}{v:.1f}%"

def fd(v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "N/A"
    return f"${v:.2f}"

def sdiv(a, b):
    try:
        if b == 0 or np.isnan(float(b)): return nan
        return float(a) / float(b)
    except Exception:
        return nan

def yoy(cur, prv):
    """Returns colored YoY badge HTML"""
    try:
        if prv is None or np.isnan(float(prv)) or float(prv) == 0: return ""
        pct = (float(cur) - float(prv)) / abs(float(prv)) * 100
        clr = "#059669" if pct >= 0 else "#DC2626"
        arrow = "▲" if pct >= 0 else "▼"
        return f"<span style='color:{clr};font-size:0.78rem;font-weight:600'>{arrow}&nbsp;{abs(pct):.1f}%</span>"
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────
# REQUIRED ROW LABELS
# ─────────────────────────────────────────────────────────────
REQUIRED = [
    "Revenue",
    "Net Income",
    "Depreciation & Amortisation",
    "Stock-Based Compensation (non-cash)",
    "Increase in Accounts Receivable",
    "Increase in Inventories",
    "Increase in Accounts Payable",
    "Increase in Deferred Revenue",
    "Capital Expenditures",
    "Acquisitions (cash paid)",
    "Total Debt",
    "Cash & Equivalents",
    "Total Equity",
    "Total Assets",
    "Shares Outstanding (millions)",
    "Share Price",
]


# ─────────────────────────────────────────────────────────────
# COMPUTATION ENGINE
# All Q8.1(a-f) and Q8.2(i-iv) computed here from raw inputs
# ─────────────────────────────────────────────────────────────
def parse(v):
    if v is None: return nan
    s = str(v).replace("$","").replace(",","").strip()
    if s in ("","N/A","n/a","-","–","nan"): return nan
    try: return float(s)
    except: return nan

def compute(df_raw, firm, jmult, acq_pct):
    df = df_raw.copy()
    df.columns = [str(c).strip() for c in df.columns]
    ic = df.columns[0]
    ycols = [c for c in df.columns[1:] if str(c).strip()]

    def g(item, yr):
        r = df[df[ic].str.strip() == item.strip()]
        return parse(r.iloc[0][yr]) if not r.empty else nan

    out = {"firm": firm, "years": ycols, "jmult": jmult, "acq_pct": acq_pct}

    for yr in ycols:
        # Raw inputs
        rev   = g("Revenue", yr)
        ni    = g("Net Income", yr)
        da    = g("Depreciation & Amortisation", yr)
        sbc   = g("Stock-Based Compensation (non-cash)", yr)
        d_ar  = g("Increase in Accounts Receivable", yr)
        d_inv = g("Increase in Inventories", yr)
        d_ap  = g("Increase in Accounts Payable", yr)
        d_dr  = g("Increase in Deferred Revenue", yr)
        capex = g("Capital Expenditures", yr)
        acq   = g("Acquisitions (cash paid)", yr)
        debt  = g("Total Debt", yr)
        cash  = g("Cash & Equivalents", yr)
        equity= g("Total Equity", yr)
        assets= g("Total Assets", yr)
        shares= g("Shares Outstanding (millions)", yr)
        price = g("Share Price", yr)

        # ── Q8.1(a) CFO — Indirect Method ─────────────────────────
        cfo     = ni + da + sbc - d_ar - d_inv + d_ap + d_dr
        cfo_adj = cfo - sbc          # Strip SBC as economic cost

        # ── Q8.1(b) FCFF ──────────────────────────────────────────
        fcff         = cfo - capex
        fcff_acq     = cfo - capex - acq   # Including acquisitions
        capex_pct    = sdiv(capex, cfo) * 100

        # ── Q8.1(c) FCFE — needs prior year debt; filled post-loop ─
        fcfe = nan; net_borrow = nan

        # ── Q8.1(d) Adjusted Net Income ───────────────────────────
        adj_ni      = ni - sbc
        sbc_pct_ni  = sdiv(sbc, ni) * 100
        sbc_reduc   = sdiv(sbc, ni) * 100   # same — reduction in real earnings

        # ── Q8.1(e) Accrual Ratio ─────────────────────────────────
        accrual_num   = ni - cfo
        accrual_ratio = sdiv(accrual_num, assets) * 100

        # ── Q8.1(f) Cash-to-Earnings ──────────────────────────────
        c2e     = sdiv(cfo, ni)
        c2e_adj = sdiv(cfo_adj, ni)

        # ── Q8.2(i) Organic Revenue ───────────────────────────────
        acq_rev     = rev * (acq_pct / 100)
        organic_rev = rev - acq_rev

        # ── Q8.2(ii) P/E ──────────────────────────────────────────
        eps     = sdiv(ni, shares)
        adj_eps = sdiv(adj_ni, shares)
        pe_rep  = sdiv(price, eps)
        pe_adj  = sdiv(price, adj_eps)

        # ── Q8.2(iii) EV / FCFF (ACTUAL market multiple) ──────────
        mkt_cap       = shares * price if not (np.isnan(shares) or np.isnan(price)) else nan
        net_debt      = debt - cash
        ev            = mkt_cap + net_debt
        ev_fcff_act   = sdiv(ev, fcff)

        # ── Q8.2(iv) IMPLIED Fair Value ───────────────────────────
        # Implied EV   = FCFF × Justified Multiple
        # Implied Eq   = Implied EV − Net Debt
        # Implied P/sh = Implied Equity / Shares
        imp_ev  = fcff * jmult
        imp_eq  = imp_ev - net_debt
        imp_ps  = sdiv(imp_eq, shares)
        premium = sdiv(price - imp_ps, imp_ps) * 100   # + = overvalued

        # Cash-collection gap
        cc_gap = d_ar - d_dr

        out[yr] = dict(
            # Raw
            rev=rev, ni=ni, da=da, sbc=sbc,
            d_ar=d_ar, d_inv=d_inv, d_ap=d_ap, d_dr=d_dr,
            capex=capex, acq=acq, debt=debt, cash=cash,
            equity=equity, assets=assets, shares=shares, price=price,
            # 8.1a
            cfo=cfo, cfo_adj=cfo_adj,
            # 8.1b
            fcff=fcff, fcff_acq=fcff_acq, capex_pct=capex_pct,
            # 8.1c (filled below)
            fcfe=fcfe, net_borrow=net_borrow,
            # 8.1d
            adj_ni=adj_ni, sbc_pct_ni=sbc_pct_ni, sbc_reduc=sbc_reduc,
            # 8.1e
            accrual_num=accrual_num, accrual_ratio=accrual_ratio,
            # 8.1f
            c2e=c2e, c2e_adj=c2e_adj,
            # 8.2i
            acq_rev=acq_rev, organic_rev=organic_rev,
            organic_growth=nan, rev_growth=nan,
            inorganic_contribution=nan, ar_growth=nan,
            # 8.2ii
            eps=eps, adj_eps=adj_eps, pe_rep=pe_rep, pe_adj=pe_adj,
            # 8.2iii
            mkt_cap=mkt_cap, net_debt=net_debt, ev=ev, ev_fcff_act=ev_fcff_act,
            # 8.2iv
            imp_ev=imp_ev, imp_eq=imp_eq, imp_ps=imp_ps, premium=premium,
            # misc
            cc_gap=cc_gap,
            cfo_growth=nan, fcff_growth=nan,
        )

    # ── YoY metrics (need two periods) ────────────────────────
    if len(ycols) >= 2:
        Y, Y2 = ycols[0], ycols[1]
        c, p = out[Y], out[Y2]

        c["rev_growth"]             = sdiv(c["rev"] - p["rev"], p["rev"]) * 100
        c["organic_growth"]         = sdiv(c["organic_rev"] - p["rev"], p["rev"]) * 100
        c["inorganic_contribution"] = c["rev_growth"] - c["organic_growth"]
        c["cfo_growth"]             = sdiv(c["cfo"] - p["cfo"], p["cfo"]) * 100
        c["fcff_growth"]            = sdiv(c["fcff"] - p["fcff"], p["fcff"]) * 100
        c["net_borrow"]             = c["debt"] - p["debt"]
        c["fcfe"]                   = c["fcff"] + c["net_borrow"]
        if p["d_ar"] != 0:
            c["ar_growth"]          = sdiv(c["d_ar"] - p["d_ar"], abs(p["d_ar"])) * 100

    return out


# ─────────────────────────────────────────────────────────────
# DEMO DATA (VelocityTech)
# ─────────────────────────────────────────────────────────────
DEMO = pd.DataFrame({
    "Item":    REQUIRED,
    "FY 2025": [5200,780,260,390,320,180,110,200,650,400,2000,900,3200,7800,600,52],
    "FY 2024": [3900,507,195,234,156, 78, 72,130,390,  0,1200,600,2600,5400,550,38],
})


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 FCF Analyser")
    st.markdown("Upload **any company's** Excel file to instantly compute every actual and implied metric.")
    st.markdown("---")

    uploaded = st.file_uploader(
        "📁 Upload Company Excel (.xlsx)",
        type=["xlsx","xls"],
        help="One sheet · First column = row labels · Other columns = years"
    )

    st.markdown("---")
    st.markdown("### ⚙️ Valuation Assumptions")
    jmult = st.slider(
        "Justified EV/FCFF Multiple (×)", 10, 60, 25, 1,
        help="Applied to FCFF to derive the IMPLIED fair value per share"
    )
    acq_pct = st.slider(
        "Acquisition-Driven Revenue (%)", 0, 50, 10, 1,
        help="% of latest-year revenue estimated to come from acquisitions"
    )

    st.markdown("---")
    st.markdown("### 📋 Required Row Labels")
    with st.expander("View all 16 required labels"):
        for item in REQUIRED:
            st.caption(f"• {item}")

    tmpl = pd.DataFrame({"Item":REQUIRED, "FY 20XX":[""]*len(REQUIRED), "FY 20YY":[""]*len(REQUIRED)})
    buf = io.BytesIO(); tmpl.to_excel(buf, index=False)
    st.download_button("⬇️ Download Blank Template", buf.getvalue(),
        file_name="company_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ─────────────────────────────────────────────────────────────
# LOAD & COMPUTE
# ─────────────────────────────────────────────────────────────
if uploaded:
    raw  = pd.read_excel(io.BytesIO(uploaded.read()), sheet_name=0)
    name = uploaded.name.replace(".xlsx","").replace(".xls","")
    demo = False
else:
    raw  = DEMO.copy()
    name = "VelocityTech Inc."
    demo = True

res = compute(raw, name, jmult, acq_pct)
yrs = res["years"]
Y   = yrs[0]
Y2  = yrs[1] if len(yrs) > 1 else None
d   = res[Y]
d2  = res[Y2] if Y2 else None


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <h1>📊 Free Cash Flow & Earnings Quality Analyser</h1>
    <p>Upload any company's raw financials · Actual CFO · FCFF · FCFE · Earnings Quality · Implied Valuation</p>
</div>
""", unsafe_allow_html=True)

if demo:
    st.info("**Demo Mode** — Showing VelocityTech Inc. Upload your own Excel from the sidebar to analyse any company.", icon="💡")

st.markdown(f"<h3 style='color:#1E3A8A;margin:0 0 1rem'>🏢 {name}</h3>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# KPI STRIP
# ─────────────────────────────────────────────────────────────
cols8 = st.columns(8)
KPIS = [
    ("CFO",              fm(d["cfo"]),          f"SBC-adj: {fm(d['cfo_adj'])}",        "neu"),
    ("FCFF",             fm(d["fcff"]),          f"Incl. Acq: {fm(d['fcff_acq'])}",    "pos" if (d["fcff"] or 0)>0 else "neg"),
    ("Adj Net Income",   fm(d["adj_ni"]),        f"Reported: {fm(d['ni'])}",            "neg" if (d["sbc_pct_ni"] or 0)>40 else "neu"),
    ("SBC / NI",         fp(d["sbc_pct_ni"]),   f"SBC: {fm(d['sbc'])}",                "neg" if (d["sbc_pct_ni"] or 0)>30 else "neu"),
    ("C/E Ratio",        fx(d["c2e"]),           f"SBC-adj: {fx(d['c2e_adj'])}",        "pos" if (d["c2e"] or 0)>=1 else "neg"),
    ("Accrual Ratio",    fp(d["accrual_ratio"]), "Neg = CFO > NI",                       "neu"),
    ("EV/FCFF Actual",   fx(d["ev_fcff_act"]),  f"EV: {fm(d['ev'])}",                   "neg" if (d["ev_fcff_act"] or 0)>35 else "pos"),
    ("Implied P/Share",  fd(d["imp_ps"]),        f"Market: {fd(d['price'])}",            "neg" if (d.get("premium") or 0)>20 else "pos"),
]
for col, (lbl, val, sub, cls) in zip(cols8, KPIS):
    with col:
        st.markdown(f"<div class='kpi'><div class='kpi-val'>{val}</div>"
                    f"<div class='kpi-lbl'>{lbl}</div>"
                    f"<div class='kpi-sub {cls}'>{sub}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 Cash Flow  (Q8.1 a–c)",
    "📐 Earnings Quality  (Q8.1 d–f)",
    "📈 Valuation  (Q8.2)",
    "🚨 Red Flags",
    "📋 Raw Data & Export",
])


# ══════════════════════════════════════════════════════════════
# TAB 1 — CASH FLOW
# ══════════════════════════════════════════════════════════════
with tab1:

    # ── Q8.1(a) CFO ──────────────────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.1(a) — Cash Flow from Operations (Indirect Method)</h3>"
        "<p>CFO = Net Income + D&A + SBC − ΔA/R − ΔInventories + ΔA/P + ΔDeferred Revenue</p></div>",
        unsafe_allow_html=True)

    def waterfall(data, yr_label):
        lbls = ["Net\nIncome", "+D&A", "+SBC", "−ΔA/R", "−ΔInv", "+ΔA/P", "+ΔDef\nRev", "= CFO"]
        vals = [data["ni"], data["da"], data["sbc"],
                -data["d_ar"], -data["d_inv"], data["d_ap"], data["d_dr"], data["cfo"]]
        meas = ["absolute","relative","relative","relative","relative","relative","relative","total"]
        fig = go.Figure(go.Waterfall(
            orientation="v", measure=meas, x=lbls, y=vals,
            connector=dict(line=dict(color="#BFDBFE", width=1.5, dash="dot")),
            increasing=dict(marker_color=C["emerald"]),
            decreasing=dict(marker_color=C["rose"]),
            totals=dict(marker_color=C["blue"]),
            text=[f"${abs(v):,.0f}M" for v in vals],
            textposition="outside",
        ))
        fig.update_layout(title=f"CFO Build-Up — {yr_label}", showlegend=False)
        return sc(fig, 400)

    if Y2:
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(waterfall(d,  Y),  use_container_width=True)
        with c2: st.plotly_chart(waterfall(d2, Y2), use_container_width=True)
    else:
        st.plotly_chart(waterfall(d, Y), use_container_width=True)

    # CFO table
    CFO_ROWS = [
        ("Net Income",                         "ni",      False, "black"),
        ("Add: Depreciation & Amortisation",   "da",      False, "green"),
        ("Add: Stock-Based Compensation",      "sbc",     False, "green"),
        ("Less: Increase in Accounts Rec.",    "d_ar",    True,  "red"),
        ("Less: Increase in Inventories",      "d_inv",   True,  "red"),
        ("Add: Increase in Accounts Payable",  "d_ap",    False, "green"),
        ("Add: Increase in Deferred Revenue",  "d_dr",    False, "green"),
        ("= Cash Flow from Operations (CFO)",  "cfo",     False, "total"),
        ("Less: SBC (real economic cost)",     "sbc",     True,  "red"),
        ("= SBC-Adjusted CFO",                 "cfo_adj", False, "total"),
    ]
    CMAP = {"black":"#0F172A","green":"#059669","red":"#DC2626","total":"#1D4ED8"}

    th = f"<table class='mt'><tr><th>Line Item</th><th>{Y} ($M)</th>"
    if Y2: th += f"<th>{Y2} ($M)</th><th>YoY Δ</th>"
    th += "</tr>"
    for lbl, key, neg, clr in CFO_ROWS:
        v1 = -d[key] if neg else d[key]
        v2 = (-d2[key] if neg else d2[key]) if d2 else None
        bold = clr == "total"
        rc = "mt-total" if bold else ""
        s  = f"color:{CMAP[clr]};font-weight:{'700' if bold else '400'}"
        th += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{v1:,.0f}</td>"
        if d2: th += f"<td style='{s}'>{v2:,.0f}</td><td>{yoy(v1,v2)}</td>"
        th += "</tr>"
    th += "</table>"
    st.markdown("<br>" + th, unsafe_allow_html=True)

    cfo_g_txt = f" CFO grew <strong>{fp(d.get('cfo_growth',nan))}</strong> YoY." if not np.isnan(d.get("cfo_growth",nan)) else ""
    st.markdown(f"""<div class='insight'>
    Reported CFO of <strong>{fm(d['cfo'])}</strong> includes <strong>{fm(d['sbc'])}</strong> of non-cash SBC —
    a real shareholder cost.{cfo_g_txt}
    Stripping SBC yields SBC-adjusted CFO of <strong>{fm(d['cfo_adj'])}</strong>.
    </div>""", unsafe_allow_html=True)

    # ── Q8.1(b) FCFF ─────────────────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.1(b) — Free Cash Flow to Firm (FCFF = CFO − CapEx)</h3></div>",
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        FCFF_ROWS = [
            ("Cash Flow from Operations", "cfo",      False, False),
            ("Less: Capital Expenditures","capex",     True,  False),
            ("= FCFF",                    "fcff",      False, True),
            ("Less: Acquisitions",        "acq",       True,  False),
            ("= FCFF incl. Acquisitions", "fcff_acq",  False, True),
            ("CapEx as % of CFO",         "capex_pct", False, False),
        ]
        h2 = f"<table class='mt'><tr><th>Item</th><th>{Y}</th>"
        if Y2: h2 += f"<th>{Y2}</th>"
        h2 += "</tr>"
        for lbl, key, neg, bold in FCFF_ROWS:
            v1 = -d[key] if neg else d[key]
            v2 = (-d2[key] if neg else d2[key]) if d2 else None
            pct = "capex_pct" in key
            fv = lambda v: (f"{v:.1f}%" if pct else f"{v:,.0f}")
            rc = "mt-total" if bold else ""
            s  = f"font-weight:{'700' if bold else '400'};color:{'#1D4ED8' if bold else '#0F172A'}"
            h2 += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{fv(v1)}</td>"
            if d2: h2 += f"<td style='{s}'>{fv(v2)}</td>"
            h2 += "</tr>"
        h2 += "</table>"
        st.markdown(h2, unsafe_allow_html=True)

    with c2:
        if Y2:
            fig = go.Figure()
            for lbl2, key2, clr2 in [("CFO","cfo",C["sky"]),("FCFF","fcff",C["blue"]),("FCFF incl.Acq","fcff_acq",C["violet"])]:
                fig.add_trace(go.Bar(name=lbl2, x=[Y,Y2], y=[d[key2],d2[key2]],
                                     marker_color=clr2, text=[fm(d[key2]),fm(d2[key2])], textposition="outside"))
            fig.update_layout(title="CFO vs FCFF vs FCFF incl. Acquisitions", barmode="group")
        else:
            fig = go.Figure(go.Bar(
                x=["CFO","SBC-Adj CFO","FCFF","FCFF incl.Acq"],
                y=[d["cfo"],d["cfo_adj"],d["fcff"],d["fcff_acq"]],
                marker_color=[C["sky"],C["amber"],C["blue"],C["violet"]],
                text=[fm(d["cfo"]),fm(d["cfo_adj"]),fm(d["fcff"]),fm(d["fcff_acq"])],
                textposition="outside"
            ))
            fig.update_layout(title="Cash Flow Metrics")
        st.plotly_chart(sc(fig, 360), use_container_width=True)

    # ── Q8.1(c) FCFE ─────────────────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.1(c) — Free Cash Flow to Equity (FCFE = FCFF + Net Borrowing)</h3>"
        "<p>Net Borrowing = Change in Total Debt between the two periods</p></div>",
        unsafe_allow_html=True)

    if not np.isnan(d.get("fcfe", nan)):
        c1, c2 = st.columns(2)
        with c1:
            h3 = f"<table class='mt'><tr><th>Item</th><th>{Y} ($M)</th></tr>"
            h3 += f"<tr><td>FCFF</td><td>{d['fcff']:,.0f}</td></tr>"
            h3 += f"<tr><td>Net Borrowing (ΔTotal Debt)</td><td>+{d['net_borrow']:,.0f}</td></tr>"
            h3 += f"<tr class='mt-total'><td style='color:#1D4ED8'>= FCFE</td><td style='color:#1D4ED8'>{d['fcfe']:,.0f}</td></tr>"
            h3 += "</table>"
            st.markdown(h3, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='insight'>
            <strong>FCFE of {fm(d['fcfe'])}</strong> exceeds FCFF because of <strong>{fm(d['net_borrow'])}</strong>
            in net new borrowings. Equity holders benefit from leverage, but this increases financial risk.
            {f"The new debt finances the {fm(d['acq'])} acquisition and general operations." if not np.isnan(d['acq']) and d['acq']>0 else ""}
            </div>""", unsafe_allow_html=True)
    else:
        st.info("FCFE requires two years of data so the change in Total Debt can be calculated. "
                "Upload an Excel with at least two year columns.", icon="ℹ️")


# ══════════════════════════════════════════════════════════════
# TAB 2 — EARNINGS QUALITY
# ══════════════════════════════════════════════════════════════
with tab2:

    # ── Q8.1(d) Adjusted NI ──────────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.1(d) — Adjusted Net Income (NI − SBC)</h3>"
        "<p>SBC is a real economic cost that GAAP excludes — stripping it reveals true earnings power</p></div>",
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        ANI_ROWS = [
            ("Reported Net Income",           "ni",         False, False),
            ("Less: Stock-Based Compensation","sbc",         True,  False),
            ("= Adjusted Net Income",         "adj_ni",      False, True),
            ("SBC as % of Reported NI",       "sbc_pct_ni",  False, False),
            ("Reduction in 'real' earnings",  "sbc_reduc",   False, False),
        ]
        h4 = f"<table class='mt'><tr><th>Item</th><th>{Y}</th>"
        if Y2: h4 += f"<th>{Y2}</th><th>YoY Δ</th>"
        h4 += "</tr>"
        for lbl, key, neg, bold in ANI_ROWS:
            v1 = -d[key] if neg else d[key]
            v2 = (-d2[key] if neg else d2[key]) if d2 else None
            pct = key in ("sbc_pct_ni","sbc_reduc")
            fv  = lambda v: (fp(v) if pct else fm(v))
            rc  = "mt-total" if bold else ""
            s   = f"font-weight:{'700' if bold else '400'};color:{'#1D4ED8' if bold else '#0F172A'}"
            h4 += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{fv(v1)}</td>"
            if d2: h4 += f"<td style='{s}'>{fv(v2)}</td><td>{yoy(v1,v2) if not pct else ''}</td>"
            h4 += "</tr>"
        h4 += "</table>"
        st.markdown(h4, unsafe_allow_html=True)

    with c2:
        if Y2:
            fig = go.Figure()
            for lbl2, key2, clr2 in [("Reported NI","ni",C["blue"]),("SBC (cost)","sbc",C["rose"]),("Adj NI","adj_ni",C["emerald"])]:
                fig.add_trace(go.Bar(name=lbl2, x=[Y,Y2], y=[d[key2],d2[key2]],
                                     marker_color=clr2, text=[fm(d[key2]),fm(d2[key2])], textposition="outside"))
            fig.update_layout(title="Reported NI vs SBC vs Adjusted NI", barmode="group")
        else:
            fig = go.Figure(go.Bar(
                x=["Reported NI","SBC","Adjusted NI"],
                y=[d["ni"],d["sbc"],d["adj_ni"]],
                marker_color=[C["blue"],C["rose"],C["emerald"]],
                text=[fm(d["ni"]),fm(d["sbc"]),fm(d["adj_ni"])],
                textposition="outside"
            ))
            fig.update_layout(title="Reported vs Adjusted Net Income")
        st.plotly_chart(sc(fig, 350), use_container_width=True)

    st.markdown(f"""<div class='insight'>
    <strong>SBC = {fp(d['sbc_pct_ni'])} of Reported NI.</strong>
    Adjusted NI is <strong>{fm(d['adj_ni'])}</strong> vs reported <strong>{fm(d['ni'])}</strong>
    — a <strong>{fp(d['sbc_reduc'])}</strong> reduction in "real" earnings.
    The company reports ${sdiv(d['ni'],d['sbc']):.2f} of GAAP profit for every $1 paid to employees in stock.
    </div>""", unsafe_allow_html=True)

    # ── Q8.1(e) Accrual Ratio ────────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.1(e) — Accrual Ratio = (Net Income − CFO) / Total Assets</h3>"
        "<p>Closer to 0 = higher earnings quality. Negative = CFO exceeds NI.</p></div>",
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        AR_ROWS = [
            ("Net Income ($M)",   "ni",            False),
            ("CFO ($M)",          "cfo",            False),
            ("NI − CFO ($M)",     "accrual_num",    False),
            ("Total Assets ($M)", "assets",         False),
            ("Accrual Ratio",     "accrual_ratio",  True),
        ]
        h5 = f"<table class='mt'><tr><th>Item</th><th>{Y}</th>"
        if Y2: h5 += f"<th>{Y2}</th>"
        h5 += "</tr>"
        for lbl, key, is_pct in AR_ROWS:
            v1 = d[key]; v2 = d2[key] if d2 else None
            bold = key == "accrual_ratio"
            fv = lambda v: (fp(v) if is_pct else f"{v:,.0f}")
            rc = "mt-total" if bold else ""
            s  = f"font-weight:{'700' if bold else '400'};color:{'#1D4ED8' if bold else '#0F172A'}"
            h5 += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{fv(v1)}</td>"
            if d2: h5 += f"<td style='{s}'>{fv(v2)}</td>"
            h5 += "</tr>"
        h5 += "</table>"
        st.markdown(h5, unsafe_allow_html=True)

    with c2:
        ar_val = d["accrual_ratio"]
        if not np.isnan(ar_val):
            col_g = C["emerald"] if abs(ar_val)<5 else C["amber"] if abs(ar_val)<12 else C["rose"]
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=ar_val,
                number={"suffix":"%","font":{"size":38,"color":col_g}},
                title={"text":"Accrual Ratio","font":{"size":14,"color":"#1E3A8A"}},
                gauge=dict(
                    axis=dict(range=[-20,20], tickcolor="#94A3B8",
                              tickfont=dict(color="#64748B")),
                    bar=dict(color=col_g), bgcolor="#F8FAFC",
                    bordercolor="#E2E8F0", borderwidth=1,
                    steps=[dict(range=[-20,20], color="#F1F5F9")],
                    threshold=dict(line=dict(color="#1D4ED8",width=2),thickness=0.75,value=0)
                )
            ))
            st.plotly_chart(sc(fig, 280), use_container_width=True)

    st.markdown(f"""<div class='insight'>
    <strong>Accrual Ratio = {fp(d['accrual_ratio'])}.</strong>
    A negative ratio superficially suggests high earnings quality (CFO exceeds NI).
    However, this is partly illusory — SBC ({fm(d['sbc'])}) inflates CFO as a non-cash add-back
    without reducing the accrual numerator. The true signal is muted.
    </div>""", unsafe_allow_html=True)

    # ── Q8.1(f) Cash-to-Earnings ─────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.1(f) — Cash-to-Earnings Ratio = CFO / Net Income</h3>"
        "<p>&gt;1.0× is healthy. SBC-adjusted version strips the non-cash add-back.</p></div>",
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        CE_ROWS = [
            ("CFO ($M)",                    "cfo",     False),
            ("Net Income ($M)",             "ni",      False),
            ("Cash-to-Earnings (Reported)", "c2e",     True),
            ("SBC-Adjusted CFO ($M)",       "cfo_adj", False),
            ("SBC-Adj Cash-to-Earnings",    "c2e_adj", True),
        ]
        h6 = f"<table class='mt'><tr><th>Item</th><th>{Y}</th>"
        if Y2: h6 += f"<th>{Y2}</th><th>YoY Δ</th>"
        h6 += "</tr>"
        for lbl, key, is_mult in CE_ROWS:
            v1 = d[key]; v2 = d2[key] if d2 else None
            bold = is_mult
            fv = lambda v: (fx(v) if is_mult else fm(v))
            rc = "mt-total" if bold else ""
            s  = f"font-weight:{'700' if bold else '400'};color:{'#1D4ED8' if bold else '#0F172A'}"
            h6 += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{fv(v1)}</td>"
            if d2: h6 += f"<td style='{s}'>{fv(v2)}</td><td>{yoy(v1,v2) if is_mult else ''}</td>"
            h6 += "</tr>"
        h6 += "</table>"
        st.markdown(h6, unsafe_allow_html=True)

    with c2:
        if Y2 and not np.isnan(d["c2e"]) and not np.isnan(d2["c2e"]):
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Reported C/E", x=[Y,Y2], y=[d["c2e"],d2["c2e"]],
                                 marker_color=C["blue"], text=[fx(d["c2e"]),fx(d2["c2e"])], textposition="outside"))
            fig.add_trace(go.Bar(name="SBC-Adj C/E",  x=[Y,Y2], y=[d["c2e_adj"],d2["c2e_adj"]],
                                 marker_color=C["amber"], text=[fx(d["c2e_adj"]),fx(d2["c2e_adj"])], textposition="outside"))
            fig.add_hline(y=1.0, line=dict(color=C["rose"],width=1.5,dash="dash"),
                          annotation_text="1.0× floor",annotation_position="bottom right")
            fig.update_layout(title="Reported vs SBC-Adjusted Cash-to-Earnings", barmode="group")
        else:
            col_g = C["emerald"] if (d["c2e"] or 0)>=1.5 else C["amber"] if (d["c2e"] or 0)>=1.0 else C["rose"]
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=d["c2e"] if not np.isnan(d["c2e"]) else 0,
                number={"suffix":"×","font":{"size":38,"color":col_g}},
                title={"text":"Cash-to-Earnings","font":{"size":14,"color":"#1E3A8A"}},
                gauge=dict(axis=dict(range=[0,3]),bar=dict(color=col_g),bgcolor="#F8FAFC",
                           bordercolor="#E2E8F0",borderwidth=1,steps=[dict(range=[0,3],color="#F1F5F9")],
                           threshold=dict(line=dict(color=C["rose"],width=2),thickness=0.75,value=1.0))
            ))
        st.plotly_chart(sc(fig, 340), use_container_width=True)

    det_txt = f"Down from {fx(d2['c2e'])} in {Y2}, a deteriorating trend." if d2 and not np.isnan(d2["c2e"]) and d["c2e"]<d2["c2e"] else ""
    st.markdown(f"""<div class='insight'>
    Reported C/E of <strong>{fx(d['c2e'])}</strong> looks healthy. {det_txt}
    SBC-adjusted C/E drops to <strong>{fx(d['c2e_adj'])}</strong> —
    once real comp costs are factored in, CFO and adjusted earnings are near one-for-one.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 — VALUATION (ACTUAL vs IMPLIED)
# ══════════════════════════════════════════════════════════════
with tab3:
    prem = d.get("premium", nan)

    st.markdown(
        "<div class='sec'><h3>Q8.2 — Actual Market Metrics vs Implied Fair Value</h3>"
        "<p>Adjust the Justified EV/FCFF Multiple in the sidebar — all implied numbers recalculate instantly</p></div>",
        unsafe_allow_html=True)

    # Big actual vs implied callout
    st.markdown(f"""
    <div class='vs-box'>
        <div class='vs-actual'>
            <div class='vs-lbl'>Actual Market EV / FCFF</div>
            <div class='vs-num'>{fx(d['ev_fcff_act'])}</div>
            <div class='vs-sub'>Market pays {fx(d['ev_fcff_act'])} per $1 of FCFF</div>
        </div>
        <div class='vs-implied'>
            <div class='vs-lbl'>Implied Fair Value @ {jmult}× Justified</div>
            <div class='vs-num'>{fd(d['imp_ps'])}</div>
            <div class='vs-sub'>vs market price of {fd(d['price'])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not np.isnan(prem):
        prem_clr = "#DC2626" if prem>0 else "#059669"
        prem_dir = "OVERVALUED" if prem>0 else "UNDERVALUED"
        st.markdown(f"""<div class='insight'>
        At a justified {jmult}×, implied fair value is <strong>{fd(d['imp_ps'])}</strong>
        vs market price <strong>{fd(d['price'])}</strong> —
        the stock appears <strong style='color:{prem_clr}'>{fp(abs(prem))} {prem_dir}</strong>
        {'(market price exceeds implied value)' if prem>0 else '(market price below implied value)'}.
        </div>""", unsafe_allow_html=True)

    # ── Q8.2(i) Organic Growth ───────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.2(i) — Organic vs Reported Revenue Growth</h3>"
        f"<p>Acquisition-driven revenue assumed at {acq_pct}% of {Y} revenue — adjust in sidebar</p></div>",
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        org_g = d.get("organic_growth", nan)
        rev_g = d.get("rev_growth", nan)
        inorg = d.get("inorganic_contribution", nan)
        ORG = [
            (f"Reported {Y} Revenue",                          fm(d["rev"]),         False),
            (f"Less: Acquired Revenue ({acq_pct}% assumed)",   fm(-d["acq_rev"]),    False),
            (f"= Organic {Y} Revenue",                         fm(d["organic_rev"]), True),
            (f"{Y2 or 'Prior Year'} Revenue (base)",           fm(d2["rev"]) if d2 else "—", False),
            ("Organic Revenue Growth Rate",                    fp(org_g),            False),
            ("Reported Revenue Growth Rate",                   fp(rev_g),            False),
            ("Inorganic Contribution (ppts)",                  fp(inorg),            False),
        ]
        h7 = "<table class='mt'><tr><th>Item</th><th>Value</th></tr>"
        for lbl, fmtv, bold in ORG:
            rc = "mt-total" if bold else ""
            s  = f"font-weight:{'700' if bold else '400'};color:{'#1D4ED8' if bold else '#0F172A'}"
            h7 += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{fmtv}</td></tr>"
        h7 += "</table>"
        st.markdown(h7, unsafe_allow_html=True)

    with c2:
        if not np.isnan(org_g) and not np.isnan(rev_g):
            fig = go.Figure(go.Bar(
                x=["Reported Growth","Organic Growth"],
                y=[rev_g, org_g],
                marker_color=[C["amber"], C["blue"]],
                text=[fp(rev_g), fp(org_g)],
                textposition="outside", width=0.45
            ))
            fig.update_layout(title="Reported vs Organic Revenue Growth", yaxis_title="%")
            st.plotly_chart(sc(fig, 320), use_container_width=True)

    # ── Q8.2(ii) P/E ─────────────────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.2(ii) — P/E Ratio: Reported vs SBC-Adjusted</h3>"
        "<p>SBC-adjusted P/E uses (NI − SBC) as the denominator</p></div>",
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        PE_ROWS = [
            ("Net Income ($M)",  d["ni"],     d["adj_ni"],  "fm"),
            ("EPS ($)",          d["eps"],    d["adj_eps"], "fd"),
            ("Share Price ($)",  d["price"],  d["price"],   "fd"),
            ("P/E Ratio",        d["pe_rep"], d["pe_adj"],  "fx"),
        ]
        h8 = "<table class='mt'><tr><th>Metric</th><th>Reported</th><th style='color:#DC2626'>SBC-Adjusted</th></tr>"
        for lbl, v_rep, v_adj, fmt_type in PE_ROWS:
            bold = "P/E" in lbl
            fv_fn = {"fm":fm,"fd":fd,"fx":fx}[fmt_type]
            rc = "mt-total" if bold else ""
            s  = f"font-weight:{'700' if bold else '400'}"
            h8 += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{fv_fn(v_rep)}</td>"
            h8 += f"<td style='{s};color:#DC2626'>{fv_fn(v_adj)}</td></tr>"
        h8 += "</table>"
        st.markdown(h8, unsafe_allow_html=True)

    with c2:
        if not np.isnan(d["pe_rep"]) and not np.isnan(d["pe_adj"]):
            fig = go.Figure(go.Bar(
                x=["Reported P/E", "SBC-Adjusted P/E"],
                y=[d["pe_rep"], d["pe_adj"]],
                marker_color=[C["blue"], C["rose"]],
                text=[fx(d["pe_rep"]), fx(d["pe_adj"])],
                textposition="outside", width=0.4
            ))
            fig.update_layout(title="Reported vs SBC-Adjusted P/E", yaxis_title="Multiple (×)")
            st.plotly_chart(sc(fig, 310), use_container_width=True)

    # ── Q8.2(iii) EV / FCFF ──────────────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.2(iii) — Enterprise Value / FCFF (Actual Market Multiple)</h3></div>",
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        EV_ROWS = [
            ("Market Cap (Shares × Price)",  fm(d["mkt_cap"])),
            ("+ Total Debt",                 fm(d["debt"])),
            ("− Cash & Equivalents",         fm(-d["cash"])),
            ("= Enterprise Value (EV)",      fm(d["ev"])),
            ("FCFF",                         fm(d["fcff"])),
            ("EV / FCFF (Actual)",           fx(d["ev_fcff_act"])),
        ]
        h9 = "<table class='mt'><tr><th>Item</th><th>Value</th></tr>"
        for lbl, fmtv in EV_ROWS:
            bold = "=" in lbl or "Actual" in lbl
            rc = "mt-total" if bold else ""
            s  = f"font-weight:{'700' if bold else '400'};color:{'#1D4ED8' if bold else '#0F172A'}"
            h9 += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{fmtv}</td></tr>"
        h9 += "</table>"
        st.markdown(h9, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class='insight'>
        At <strong>{fx(d['ev_fcff_act'])}</strong>, the market pays <strong>${d['ev_fcff_act']:.2f}
        for every $1 of free cash</strong> generated by {name}.
        High-growth tech companies rarely sustain EV/FCFF above 30–35×.
        This multiple embeds an assumption of sustained, compounding growth.
        </div>""", unsafe_allow_html=True)

    # ── Q8.2(iv) Implied Fair Value ──────────────────────────
    st.markdown(
        "<div class='sec'><h3>Q8.2(iv) — Implied Fair Value per Share</h3>"
        f"<p>Using Justified EV/FCFF = {jmult}× (adjust in sidebar to see sensitivity)</p></div>",
        unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        IV_ROWS = [
            ("FCFF ($M)",                                     fm(d["fcff"])),
            (f"× Justified EV/FCFF Multiple ({jmult}×)",     f"{jmult}×"),
            ("= Implied Enterprise Value ($M)",               fm(d["imp_ev"])),
            ("Less: Net Debt (Debt − Cash) ($M)",             fm(-d["net_debt"])),
            ("= Implied Equity Value ($M)",                   fm(d["imp_eq"])),
            (f"÷ Shares Outstanding ({d['shares']:.0f}M)",   f"{d['shares']:.0f}M"),
            ("= Implied Fair Value per Share",                fd(d["imp_ps"])),
            ("Current Market Price",                          fd(d["price"])),
            ("Premium / (Discount) to Implied Value",
             fp(prem, signed=True) + (" OVERVALUED" if not np.isnan(prem) and prem>0
                                       else " UNDERVALUED" if not np.isnan(prem) else "") if not np.isnan(prem) else "N/A"),
        ]
        hA = "<table class='mt'><tr><th>Step</th><th>Value</th></tr>"
        for lbl, fmtv in IV_ROWS:
            bold = "=" in lbl or "Premium" in lbl or "Market Price" in lbl
            is_prem = "Premium" in lbl
            clr = ("#DC2626" if not np.isnan(prem) and prem>0 else "#059669") if is_prem else ("#1D4ED8" if bold else "#0F172A")
            rc = "mt-total" if bold else ""
            s  = f"font-weight:{'700' if bold else '400'};color:{clr}"
            hA += f"<tr class='{rc}'><td style='{s}'>{lbl}</td><td style='{s}'>{fmtv}</td></tr>"
        hA += "</table>"
        st.markdown(hA, unsafe_allow_html=True)

    with c2:
        if not np.isnan(d["imp_ps"]):
            over = not np.isnan(prem) and prem > 0
            fig = go.Figure(go.Bar(
                x=["Market Price", f"Implied Value\n({jmult}× justified)"],
                y=[d["price"], d["imp_ps"]],
                marker_color=[C["rose"] if over else C["emerald"],
                              C["emerald"] if over else C["rose"]],
                text=[fd(d["price"]), fd(d["imp_ps"])],
                textposition="outside", width=0.45
            ))
            fig.update_layout(title="Market Price vs Implied Fair Value", yaxis_title="$ per Share")
            st.plotly_chart(sc(fig, 320), use_container_width=True)

    # Sensitivity table
    st.markdown(
        "<div class='sec'><h3>📊 Sensitivity — Implied Share Price at Different Multiples</h3></div>",
        unsafe_allow_html=True)

    sens = []
    for m in [10,15,20,25,30,35,40,50,60]:
        ie = d["fcff"] * m
        iq = ie - d["net_debt"]
        ip = sdiv(iq, d["shares"])
        pd_ = sdiv(d["price"] - ip, ip) * 100 if not np.isnan(ip) and ip > 0 else nan
        sens.append({
            "Multiple": f"{m}×",
            "Implied EV": f"${ie:,.0f}M",
            "Implied Price/Share": fd(ip),
            "vs Market": (f"+{pd_:.1f}% OV" if pd_>0 else f"{pd_:.1f}% UV") if not np.isnan(pd_) else "N/A",
        })
    hS = "<table class='mt'><tr><th>EV/FCFF Multiple</th><th>Implied EV</th><th>Implied Price/Share</th><th>vs Market Price</th></tr>"
    for row in sens:
        used = row["Multiple"] == f"{jmult}×"
        bg = "background:#FFFBEB;" if used else ""
        ov = "OV" in row["vs Market"]
        pc = "color:#DC2626;font-weight:700" if ov else "color:#059669;font-weight:700"
        hS += f"<tr style='{bg}'>"
        hS += f"<td style='font-weight:{'700' if used else '400'};color:{'#D97706' if used else '#0F172A'}'>{row['Multiple']}{'  ← used' if used else ''}</td>"
        hS += f"<td>{row['Implied EV']}</td>"
        hS += f"<td style='font-weight:{'700' if used else '400'}'>{row['Implied Price/Share']}</td>"
        hS += f"<td style='{pc}'>{row['vs Market']}</td>"
        hS += "</tr>"
    hS += "</table>"
    st.markdown(hS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 4 — RED FLAGS
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown(
        "<div class='sec'><h3>🚨 Forensic Red Flag Analysis</h3>"
        "<p>Auto-generated from computed metrics — dynamically updates for any uploaded company</p></div>",
        unsafe_allow_html=True)

    reds, ambers, greens = [], [], []

    # RF1: SBC > 30% of NI
    if not np.isnan(d["sbc_pct_ni"]) and d["sbc_pct_ni"] > 30:
        yr2t = f"Up from {fp(d2['sbc_pct_ni'])} in {Y2}. " if d2 and not np.isnan(d2.get("sbc_pct_ni",nan)) else ""
        reds.append((
            f"🔴 RF1 — SBC = {fp(d['sbc_pct_ni'])} of Net Income (Earnings Overstated)",
            f"SBC of {fm(d['sbc'])} equals {fp(d['sbc_pct_ni'])} of reported NI ({fm(d['ni'])}). "
            f"Adjusted NI is only {fm(d['adj_ni'])}. {yr2t}"
            f"Every $1 of GAAP profit is offset by ${sdiv(d['sbc'],d['ni']):.2f} of equity dilution."
        ))

    # RF2: AR growing faster than revenue
    ar_g = d.get("ar_growth", nan)
    rev_g = d.get("rev_growth", nan)
    if not np.isnan(ar_g) and not np.isnan(rev_g) and ar_g > rev_g * 1.25:
        reds.append((
            f"🔴 RF2 — AR Growing {fp(ar_g)} vs Revenue at {fp(rev_g)}",
            f"Revenue grew {fp(rev_g)} YoY but the AR increment grew {fp(ar_g)}. "
            f"An increasing share of revenue was recognised before cash collection — "
            f"aggressive revenue recognition or deteriorating customer credit. "
            f"Cash-collection gap (ΔAR − ΔDeferred Rev): {fm(d['cc_gap'])}."
        ))

    # RF3: EV/FCFF > 35×
    if not np.isnan(d["ev_fcff_act"]) and d["ev_fcff_act"] > 35:
        reds.append((
            f"🔴 RF3 — EV/FCFF = {fx(d['ev_fcff_act'])} vs Justified {jmult}× → {fp(abs(prem))} {'Overvalued' if not np.isnan(prem) and prem>0 else 'Undervalued'}",
            f"The market prices {name} at {fx(d['ev_fcff_act'])} FCFF — ${d['ev_fcff_act']:.2f} per $1 of free cash. "
            f"At a justified {jmult}× multiple, implied fair value is {fd(d['imp_ps'])}/share "
            f"vs market price of {fd(d['price'])}."
        ))

    # RF4: SBC-adj P/E > 60×
    if not np.isnan(d["pe_adj"]) and d["pe_adj"] > 60:
        reds.append((
            f"🔴 RF4 — SBC-Adjusted P/E = {fx(d['pe_adj'])} (Reported: {fx(d['pe_rep'])})",
            f"Reported P/E of {fx(d['pe_rep'])} doubles to {fx(d['pe_adj'])} once SBC is a real cost. "
            f"Peer-group P/Es of 30–40× for high-growth tech are already at the upper bound."
        ))

    # Amber: inorganic growth
    if not np.isnan(d.get("inorganic_contribution",nan)) and d["inorganic_contribution"] > 5:
        ambers.append((
            f"🟡 Inorganic Revenue Inflation — ~{fp(d['inorganic_contribution'])} from acquisitions",
            f"Reported growth of {fp(rev_g)} includes {fp(d['inorganic_contribution'])} from acquisitions "
            f"(at {acq_pct}% assumed). Organic growth is only {fp(d['organic_growth'])}. "
            f"Risk: market may be extrapolating headline growth into perpetuity."
        ))

    # Amber: C/E deteriorating
    if d2 and not np.isnan(d["c2e"]) and not np.isnan(d2["c2e"]) and d["c2e"] < d2["c2e"] and d["c2e_adj"] < 1.2:
        ambers.append((
            f"🟡 Cash-to-Earnings Deteriorating ({fx(d2['c2e'])} → {fx(d['c2e'])})",
            f"Reported C/E fell from {fx(d2['c2e'])} in {Y2} to {fx(d['c2e'])} in {Y}. "
            f"SBC-adjusted C/E is only {fx(d['c2e_adj'])} — barely above 1×."
        ))

    # Green signals
    if (d["fcff"] or 0) > 0:
        greens.append(("✅ Positive FCFF", f"FCFF of {fm(d['fcff'])} — firm generates free cash after capex."))
    if (d["accrual_ratio"] or 0) < 0:
        greens.append(("✅ Negative Accrual Ratio", f"CFO ({fm(d['cfo'])}) exceeds NI ({fm(d['ni'])})."))
    if (d["c2e"] or 0) >= 1.5:
        greens.append(("✅ C/E Above 1.5×", f"Reported C/E = {fx(d['c2e'])}."))

    total = len(reds) + len(ambers)
    if total == 0:
        st.success("No major red flags at current thresholds. Review individual tabs for detail.", icon="✅")
    else:
        st.markdown(f"#### ⚠️ {total} Risk Signal{'s' if total>1 else ''} Detected")

    for t, desc in reds:
        st.markdown(f"<div class='flag-red'><h4>{t}</h4><p>{desc}</p></div>", unsafe_allow_html=True)
    for t, desc in ambers:
        st.markdown(f"<div class='flag-amber'><h4>{t}</h4><p>{desc}</p></div>", unsafe_allow_html=True)
    if greens:
        st.markdown("#### ✅ Positive Signals")
        for t, desc in greens:
            st.markdown(f"<div class='flag-green'><h4>{t}</h4><p>{desc}</p></div>", unsafe_allow_html=True)

    # Scorecard
    st.markdown("<div class='sec'><h3>📋 Overall Assessment Scorecard</h3></div>", unsafe_allow_html=True)
    SC = [
        ("CFO ($M)",              fm(d["cfo"]),           fm(d2["cfo"]) if d2 else "—",           "Neutral — SBC-inflated"),
        ("SBC-Adjusted CFO ($M)", fm(d["cfo_adj"]),       fm(d2["cfo_adj"]) if d2 else "—",       "Real cash generation"),
        ("FCFF ($M)",             fm(d["fcff"]),           fm(d2["fcff"]) if d2 else "—",          "After capex"),
        ("Adj Net Income ($M)",   fm(d["adj_ni"]),         fm(d2["adj_ni"]) if d2 else "—",        "🔴 50% haircut" if (d["sbc_pct_ni"] or 0)>40 else "Moderate"),
        ("Accrual Ratio",         fp(d["accrual_ratio"]),  fp(d2["accrual_ratio"]) if d2 else "—","SBC-distorted signal"),
        ("Cash-to-Earnings",      fx(d["c2e"]),            fx(d2["c2e"]) if d2 else "—",           "🟡 Deteriorating" if d2 and (d["c2e"] or 99)<(d2.get("c2e") or 0) else "Stable"),
        ("Organic Revenue Growth",fp(d.get("organic_growth",nan)), "—",                             "Solid but below headline"),
        ("Reported P/E",          fx(d["pe_rep"]),         "—",                                     "🔴 Rich" if (d["pe_rep"] or 0)>35 else "Acceptable"),
        ("SBC-Adjusted P/E",      fx(d["pe_adj"]),         "—",                                     "🔴 Extreme" if (d["pe_adj"] or 0)>60 else "Elevated"),
        ("EV / FCFF (Actual)",    fx(d["ev_fcff_act"]),    "—",                                     "🔴 Overvalued" if (d["ev_fcff_act"] or 0)>40 else "Elevated"),
        ("Implied Fair Value/sh", fd(d["imp_ps"]),         "—",                                     f"🔴 {fp(prem)} premium" if not np.isnan(prem) and prem>20 else "Near fair value"),
    ]
    hSC = f"<table class='mt'><tr><th>Metric</th><th>{Y}</th><th>{Y2 or '—'}</th><th>Signal</th></tr>"
    for lbl, v1, v2, sig in SC:
        clr = "#DC2626" if "🔴" in sig else "#D97706" if "🟡" in sig else "#059669" if "✅" in sig else "#64748B"
        hSC += f"<tr><td>{lbl}</td><td style='font-weight:600'>{v1}</td><td>{v2}</td>"
        hSC += f"<td style='color:{clr};font-weight:600'>{sig}</td></tr>"
    hSC += "</table>"
    st.markdown(hSC, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 5 — RAW DATA & EXPORT
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<div class='sec'><h3>📋 Raw Input Data</h3><p>Exactly as read from your Excel file</p></div>",
                unsafe_allow_html=True)
    st.dataframe(raw, use_container_width=True)

    st.markdown("<div class='sec'><h3>📤 Full Computed Metrics — Download as Excel</h3></div>",
                unsafe_allow_html=True)
    exp_rows = []
    for yr in yrs:
        dyr = res[yr]
        exp_rows.append({
            "Firm": name, "Year": yr,
            "Revenue ($M)": dyr["rev"], "Net Income ($M)": dyr["ni"],
            "CFO ($M)": dyr["cfo"], "SBC-Adj CFO ($M)": dyr["cfo_adj"],
            "FCFF ($M)": dyr["fcff"], "FCFF incl Acq ($M)": dyr["fcff_acq"],
            "FCFE ($M)": dyr["fcfe"],
            "Adj Net Income ($M)": dyr["adj_ni"],
            "SBC % of NI": round(dyr["sbc_pct_ni"], 1),
            "Accrual Ratio (%)": round(dyr["accrual_ratio"], 2),
            "Cash-to-Earnings (×)": round(dyr["c2e"], 2) if not np.isnan(dyr["c2e"]) else None,
            "SBC-Adj C/E (×)": round(dyr["c2e_adj"], 2) if not np.isnan(dyr["c2e_adj"]) else None,
            "EPS ($)": round(dyr["eps"], 2) if not np.isnan(dyr["eps"]) else None,
            "SBC-Adj EPS ($)": round(dyr["adj_eps"], 2) if not np.isnan(dyr["adj_eps"]) else None,
            "Reported P/E (×)": round(dyr["pe_rep"], 1) if not np.isnan(dyr["pe_rep"]) else None,
            "SBC-Adj P/E (×)": round(dyr["pe_adj"], 1) if not np.isnan(dyr["pe_adj"]) else None,
            "EV ($M)": dyr["ev"],
            "EV/FCFF Actual (×)": round(dyr["ev_fcff_act"], 1) if not np.isnan(dyr["ev_fcff_act"]) else None,
            f"Implied EV @{jmult}× ($M)": round(dyr["imp_ev"], 0),
            f"Implied Price @{jmult}× ($)": round(dyr["imp_ps"], 2) if not np.isnan(dyr["imp_ps"]) else None,
            "Market Price ($)": dyr["price"],
            "Premium/(Discount) (%)": round(dyr["premium"], 1) if not np.isnan(dyr.get("premium", nan)) else None,
        })
    exp_df = pd.DataFrame(exp_rows)
    st.dataframe(exp_df, use_container_width=True)

    buf2 = io.BytesIO()
    with pd.ExcelWriter(buf2, engine="openpyxl") as w:
        exp_df.to_excel(w, sheet_name="Computed Metrics", index=False)
    st.download_button(
        "⬇️ Download Computed Metrics (Excel)",
        buf2.getvalue(),
        file_name=f"{name}_FCF_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer-bar'>
    <strong>FCF & Earnings Quality Analyser</strong> &nbsp;·&nbsp;
    Q8.1: CFO · FCFF · FCFE · Adjusted NI · Accrual Ratio · Cash-to-Earnings &nbsp;·&nbsp;
    Q8.2: Organic Growth · SBC-Adj P/E · EV/FCFF · Implied Fair Value &nbsp;·&nbsp;
    Upload any company to analyse
</div>
""", unsafe_allow_html=True)
