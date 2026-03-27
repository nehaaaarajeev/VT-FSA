# 📊 FCF & Earnings Quality Analyser — Streamlit Dashboard

A forensic financial analysis dashboard for **Q8: Free Cash Flow & Earnings Quality**.

Analyses any firm's financials from a simple Excel upload and computes **actual** and **implied** metrics across all four questions (8.1a–f and 8.2).

---

## 🎯 What the Dashboard Does

Upload **any firm's Excel file** (matching the template format) and instantly get:

| Section | Metrics |
|---------|---------|
| 💰 Cash Flow | CFO build-up (waterfall), FCFF, FCFE, SBC-adjusted CFO |
| 📐 Earnings Quality | Accrual Ratio, Cash-to-Earnings, SBC burden, AR vs Revenue growth |
| 📈 Valuation | EV/FCFF (actual vs justified), P/E (reported vs SBC-adjusted), Implied Fair Value |
| 🚨 Red Flags | Auto-detected forensic signals with dynamic thresholds |
| 📋 Export | Full computed metrics table downloadable as Excel |

---

## 🚀 Run Locally

```bash
# 1. Clone / download
cd VelocityTech_Dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repo
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Select repo → `app.py` → Deploy

---

## 📁 File Structure

```
VelocityTech_Dashboard/
├── app.py                          ← Main Streamlit dashboard (~700 lines)
├── requirements.txt
├── README.md
├── VelocityTech_Solved_Model.xlsx  ← Fully-solved Excel workbook (5 sheets, 146 formulas)
├── .streamlit/
│   └── config.toml                 ← Dark navy theme
```

---

## 📂 Excel Model — `VelocityTech_Solved_Model.xlsx`

| Sheet | Description |
|-------|-------------|
| **Input Data** | Raw source financials (blue = hardcoded inputs) |
| **Computed Metrics** | All Q8.1(a–f) formulas auto-linked to Input Data |
| **Valuation** | Q8.2 — EV, P/E, implied fair value (adjustable assumptions) |
| **Red Flag Analysis** | Forensic scorecard auto-linked to computed sheets |
| **Template (Upload)** | Blank template — fill and upload to the dashboard |

> **Formula conventions:** Blue text = hardcoded input · Black = formula · Yellow background = key assumption

---

## 📋 Dashboard Upload Format

Your Excel must have **one sheet** with these exact row labels in column A:

| Required Row Labels |
|---|
| Revenue |
| Net Income |
| Depreciation & Amortisation |
| Stock-Based Compensation (non-cash) |
| Increase in Accounts Receivable |
| Increase in Inventories |
| Increase in Accounts Payable |
| Increase in Deferred Revenue |
| Capital Expenditures |
| Acquisitions (cash paid) |
| Total Debt |
| Cash & Equivalents |
| Total Equity |
| Total Assets |
| Shares Outstanding (millions) |
| Share Price |

> ⬇️ Use the **"Template (Upload)"** sheet in `VelocityTech_Solved_Model.xlsx` or download the blank template directly from the dashboard sidebar.

---

## 🔑 Key Formulas Implemented

### Q8.1(a) — CFO (Indirect Method)
```
CFO = Net Income + D&A + SBC − ΔA/R − ΔInventories + ΔA/P + ΔDeferred Revenue
SBC-Adjusted CFO = CFO − SBC
```

### Q8.1(b) — FCFF
```
FCFF = CFO − CapEx
FCFF incl. Acquisitions = FCFF − Acquisitions
```

### Q8.1(c) — FCFE
```
FCFE = FCFF + Net Borrowing (= FCFF + ΔTotal Debt)
```

### Q8.1(d) — Adjusted Net Income
```
Adjusted NI = Net Income − SBC
SBC % of NI = SBC / Net Income
```

### Q8.1(e) — Accrual Ratio
```
Accrual Ratio = (Net Income − CFO) / Total Assets
```

### Q8.1(f) — Cash-to-Earnings
```
C/E = CFO / Net Income
SBC-Adjusted C/E = SBC-Adjusted CFO / Net Income
```

### Q8.2 — Valuation
```
EV = Market Cap + Total Debt − Cash
EV/FCFF = EV / FCFF
Reported P/E = Share Price / EPS
SBC-Adjusted P/E = Share Price / (Adjusted NI / Shares)
Implied EV = FCFF × Justified Multiple
Implied Equity Value = Implied EV − Net Debt
Implied Price/Share = Implied Equity Value / Shares
```

---

## ⚙️ Sidebar Controls

| Control | Description |
|---------|-------------|
| **File upload** | Upload one or more Excel files (multi-firm comparison) |
| **Justified EV/FCFF Multiple** | Slide to change sustainable valuation multiple (default 25×) |
| **Acquired Revenue %** | % of latest revenue from acquisitions (for organic growth calculation) |

---

## 🛠 Tech Stack

- **Streamlit** — dashboard framework
- **Plotly** — waterfall charts, gauges, bar charts, heatmaps
- **openpyxl** — Excel read/write
- **pandas / numpy** — data processing
- **scipy** — not used here (pure financial formulas)

---

*VelocityTech Inc. Forensic Analysis | Group 8 | Due: 31 March*
