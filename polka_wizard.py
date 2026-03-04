"""
POLKA MUP — Outil de Cotation Logistique
Version 7 — Wizard professionnel avec calculs transparents
"""
import streamlit as st

st.set_page_config(page_title="Polka MUP", page_icon="📦", layout="wide",
                   initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════════════════════
# STYLE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0e1a; color: #dde3f0; }
.main .block-container { padding: 0 2rem 3rem 2rem; max-width: 1320px; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }

/* ── Header ── */
.mup-header {
  background: linear-gradient(90deg,#0d1224 0%,#111827 100%);
  border-bottom: 1px solid #1e2a45;
  padding: 14px 32px;
  display: flex; align-items: center; justify-content: space-between;
  margin: -1rem -2rem 0 -2rem; margin-bottom: 0;
}
.mup-logo { font-size:1.4rem; font-weight:700; color:#fff; letter-spacing:-0.5px; }
.mup-logo span { color:#3b82f6; }
.mup-project { text-align:right; }
.mup-project .name { font-size:0.92rem; font-weight:600; color:#e2e8f0; }
.mup-project .sub  { font-size:0.72rem; color:#64748b; margin-top:1px; }

/* ── Sticky KPI bar ── */
.kpi-bar {
  display:grid; grid-template-columns:repeat(5,1fr);
  background:#0d1224; border-bottom:1px solid #1e2a45;
  margin: 0 -2rem 1.5rem -2rem; padding: 0 2rem;
}
.kpi-cell { padding:10px 16px; border-right:1px solid #1e2a45; }
.kpi-cell:last-child { border-right:none; }
.kpi-lbl { font-size:0.62rem; text-transform:uppercase; letter-spacing:1.2px; color:#64748b; margin-bottom:2px; }
.kpi-val { font-family:'JetBrains Mono',monospace; font-size:1.2rem; font-weight:600; color:#e2e8f0; }
.kpi-val.up   { color:#22c55e; }
.kpi-val.down { color:#ef4444; }
.kpi-val.blue { color:#3b82f6; }
.kpi-sub { font-size:0.68rem; color:#475569; margin-top:1px; }

/* ── Step wizard nav ── */
.wizard-nav {
  display:flex; align-items:center; gap:0; margin-bottom:2rem;
  background:#0d1224; border:1px solid #1e2a45; border-radius:10px; overflow:hidden; padding:6px;
  gap:4px;
}
.wstep {
  flex:1; text-align:center; padding:8px 4px; border-radius:7px;
  font-size:0.72rem; font-weight:500; color:#475569; cursor:pointer;
  transition:all .15s; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.wstep.done { color:#64748b; }
.wstep.done:hover { background:#1e2a45; color:#94a3b8; }
.wstep.active { background:#3b82f6; color:#fff; font-weight:600; }
.wstep .dot { display:inline-block; width:6px; height:6px; border-radius:50%; margin-right:5px; vertical-align:middle; }
.wstep.active .dot { background:#fff; }
.wstep.done .dot { background:#22c55e; }
.wstep.todo .dot { background:#1e2a45; }
.wstep.todo { color:#334155; }

/* ── Main layout: left = form, right = calc panel ── */
.step-grid { display:grid; grid-template-columns:1fr 400px; gap:1.5rem; align-items:start; }

/* ── Form card ── */
.form-card {
  background:#0d1224; border:1px solid #1e2a45; border-radius:12px;
  padding:1.6rem 1.8rem;
}
.form-section { margin-bottom:1.4rem; }
.form-section-title {
  font-size:0.68rem; text-transform:uppercase; letter-spacing:1.5px;
  color:#3b82f6; font-weight:600; margin-bottom:1rem;
  padding-bottom:8px; border-bottom:1px solid #1e2a45;
}

/* ── Calc panel ── */
.calc-panel {
  background:#060b14; border:1px solid #1e2a45; border-radius:12px;
  padding:1.4rem; position:sticky; top:0;
}
.calc-panel-title {
  font-size:0.65rem; text-transform:uppercase; letter-spacing:1.5px;
  color:#64748b; font-weight:600; margin-bottom:1rem;
}
.calc-block {
  background:#0d1224; border:1px solid #1e2a45; border-radius:8px;
  padding:10px 12px; margin-bottom:8px;
}
.calc-label { font-size:0.7rem; color:#64748b; margin-bottom:4px; }
.calc-formula { font-size:0.72rem; color:#94a3b8; font-family:'JetBrains Mono',monospace; margin-bottom:6px; line-height:1.5; }
.calc-result {
  font-size:1.1rem; font-weight:600; font-family:'JetBrains Mono',monospace;
  color:#e2e8f0;
}
.calc-result.highlight { color:#3b82f6; }
.calc-result.green { color:#22c55e; }
.calc-result.red   { color:#ef4444; }
.calc-total {
  border-top:1px solid #1e2a45; padding-top:10px; margin-top:6px;
  display:flex; justify-content:space-between; align-items:center;
}
.calc-total-label { font-size:0.75rem; color:#94a3b8; font-weight:500; }
.calc-total-value { font-size:1.3rem; font-weight:700; font-family:'JetBrains Mono',monospace; color:#3b82f6; }

/* ── Inputs ── */
.stNumberInput input, .stTextInput input, .stSelectbox > div {
  background:#060b14 !important; border:1px solid #1e2a45 !important;
  border-radius:7px !important; color:#dde3f0 !important;
  font-family:'JetBrains Mono',monospace !important; font-size:0.88rem !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
  border-color:#3b82f6 !important;
  box-shadow:0 0 0 3px rgba(59,130,246,.12) !important;
}
label { font-size:0.76rem !important; color:#94a3b8 !important; font-weight:500 !important; }

/* ── Table in process/price steps ── */
.trow { display:grid; gap:6px; padding:6px 0; border-bottom:1px solid #1e2a45; align-items:center; }
.trow:last-child { border-bottom:none; }
.tcell { font-size:0.8rem; }
.tcell.mono { font-family:'JetBrains Mono',monospace; font-size:0.8rem; }
.tcell.dim  { color:#475569; }
.thdr { font-size:0.62rem; text-transform:uppercase; letter-spacing:1px; color:#475569; font-weight:600; }

/* ── Progress arrow ── */
.prog-arrow {
  display:flex; gap:0; align-items:center; margin-bottom:1.5rem; flex-wrap:nowrap;
}
.prog-seg {
  flex:1; height:4px; background:#1e2a45; margin-right:2px; border-radius:2px;
  transition:background .3s;
}
.prog-seg.done   { background:#22c55e; }
.prog-seg.active { background:#3b82f6; }

/* ── Nav buttons ── */
.stButton > button {
  border-radius:8px !important; font-size:0.84rem !important; font-weight:600 !important;
  padding:8px 24px !important;
}
.stButton > button[kind="primary"] {
  background:linear-gradient(135deg,#3b82f6,#2563eb) !important;
  border:none !important; color:#fff !important;
  box-shadow:0 2px 12px rgba(59,130,246,.35) !important;
}
.stButton > button:not([kind="primary"]) {
  background:#0d1224 !important; border:1px solid #1e2a45 !important; color:#64748b !important;
}
.stButton > button:not([kind="primary"]):hover {
  border-color:#3b82f6 !important; color:#3b82f6 !important;
}

/* ── Radio pills ── */
.stRadio > label { display:none !important; }
.stRadio [data-baseweb="radio"] > div:first-child {
  border-color:#3b82f6 !important;
}

/* ── Checkboxes ── */
.stCheckbox { margin:0 !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
  background:#0d1224 !important; border:1px solid #1e2a45 !important;
  border-radius:8px !important; padding:10px 14px !important;
}

/* ── Divider ── */
hr { border-color:#1e2a45 !important; margin:.8rem 0 !important; }

/* ── Badge ── */
.badge { display:inline-block; padding:1px 8px; border-radius:4px; font-size:0.65rem; font-weight:600; text-transform:uppercase; letter-spacing:.5px; }
.badge-blue  { background:rgba(59,130,246,.15); color:#3b82f6; border:1px solid rgba(59,130,246,.25); }
.badge-green { background:rgba(34,197,94,.15);  color:#22c55e; border:1px solid rgba(34,197,94,.25); }
.badge-red   { background:rgba(239,68,68,.15);  color:#ef4444; border:1px solid rgba(239,68,68,.25); }
.badge-gray  { background:rgba(100,116,139,.15);color:#94a3b8; border:1px solid rgba(100,116,139,.25); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DEFAULTS — AKZO NOBEL reference (exact MUP Excel 2021 values)
# ══════════════════════════════════════════════════════════════════════════════
_D = dict(
    project="AKZO NOBEL", customer="AKZO NOBEL",
    branch="MA-Mohammedia (580)", project_leader="Tayeb Sbihi",
    country="Maroc", country_org="Morocco",
    business_unit="ELS", sector="Peintures & Revêtements",
    working_days=272, target_margin=20.0, interest_rate=9.0, contract_years=3,
    wms="MIKADO", wms_alloc_pct=1.7, ho_alloc_pct=0.8625,
    exchange_rate=0.094, term_payment=30, failure_rate=5.0, social_pct=14.2,
    wh_surface=1600.0, wh_height=10.0, gross_loc=1741.0, op_reserve_pct=10.0,
    rent_mad=44.5, charges_mad=3.5, taxes_mad=5.04,
    racking_ppl=35.0, racking_qty=1741.0,
    security_m2=5.0, cabling_m2=5.0,
    lower_shelf_qty=110.0, lower_shelf_price=38.0,
    grating_qty=550.0, grating_price=20.0,
    invest_years=12.0, avg_pal=1772.0,
)

_PERSONNEL = [
    # en, fr, qty, salary, cat (OP/ADM/MGT)
    ("Picker",                      "Préparateur de commandes",     1,    7964, "OP"),
    ("Forklift driver",             "Cariste",                       1,    7964, "OP"),
    ("Loader",                      "Chargeur / Déchargeur",         1,    6500, "OP"),
    ("Inbound controller",          "Contrôleur réception",          0,    6500, "OP"),
    ("WH skilled employee",         "Agent logistique qualifié",     0,   13722, "OP"),
    ("Team leader (operative)",     "Team leader opérationnel",      0,   13722, "OP"),
    ("Team leader (admin)",         "Team leader administratif",     1,   13722, "ADM"),
    ("Stock manager",               "Gestionnaire de stock",         0.5, 13722, "ADM"),
    ("Site assistant",              "Assistant de site",             0,    9818, "ADM"),
    ("Inbound admin",               "Administratif entrée",          0,   13722, "ADM"),
    ("Outbound admin",              "Administratif sortie",          0,   13722, "ADM"),
    ("Operations manager",          "Responsable opérations",       0.15, 31000, "MGT"),
    ("CL-Consultant / DEWO",        "Consultant CL / DEWO",         0.20, 25000, "MGT"),
    ("Contract logistics manager",  "Directeur logistique",          0,   65243, "MGT"),
]

_TRUCKS = [
    # code, en, fr, qty, mode, price_incl_bat, depr_years
    ("FZ0010","Hand Pallet Truck",          "Transpalette manuel",         0,"Purchase",    375,  6),
    ("FZ0020","Picking Trolley",            "Chariot de picking",          0,"Purchase",    700,  6),
    ("FZ0040","Fast Mover",                 "Fast Mover",                  1,"External Rent",12732,6),
    ("FZ0050","Horizontal Order Picker",    "Préparateur horizontal",      1,"External Rent",14279,6),
    ("FZ0060","Vertical Order Picker 1.2m", "Préparateur vertical 1.2m",  0,"External Rent",14230,6),
    ("FZ0070","Front Loader",               "Chariot frontal",             0,"External Rent",27716,6),
    ("FZ0080","Reach Truck ≤ 8m",           "Chariot rétractable ≤ 8m",   0,"External Rent",37188,6),
    ("FZ0085","Reach Truck > 8m",           "Chariot rétractable > 8m",   1,"External Rent",50718,6),
    ("FZ0090","Narrow-Aisle Truck",         "Chariot allée étroite",       0,"External Rent",103000,6),
    ("FZ0100","Floor Sweeper",              "Autolaveuse",                 0,"External Rent", 21500,8),
]

# code, en, fr, grp, billing_en, billing_fr, vol, prod_gross, prod_net, cost_unit_eur, price_default_eur
_PROCESSES = [
    ("WE1", "Inbound Full Pallet",           "Réception Palette Homogène",       "inbound",    "Delivered Inbound - Pallets","Palettes entrée",       2733,  49.49, 42.56, 1.8007, 2.2509),
    ("WE2", "Inbound Mixed Pallet",          "Réception Palette Hétérogène",     "inbound",    "Stock-in Inbound - Pallets", "Palettes stockées",     1275,  30.67, 26.38, 2.3463, 2.9329),
    ("WE4", "Retour Vrac",                   "Retour Vrac",                       "inbound",    "Picking Unit Loose",         "Colis vrac",            3245, 124.33,106.92, 0.2906, 0.3632),
    ("KO1", "Picking ASC",                   "Picking ASC",                       "picking",    "Picks",                      "Picks ASC",            45131, 155.54,133.77, 0.4214, 0.5268),
    ("KO2", "Picking MPY & Powder",          "Picking MPY & Poudre",              "picking",    "Picks",                      "Picks MPY/Poudre",      9529,  46.99, 40.41, 0.6510, 0.8137),
    ("UL1", "Replenishment Picking ASC",     "Réappro. Picking ASC",              "relocation", "Partial Relocation Pallets", "Palettes réappro.",     5319,  16.48, 14.18, 0.0,    0.0),
    ("UL2", "Replenishment Picking MPY",     "Réappro. Picking MPY & Poudre",    "relocation", "Relocation Pallets",         "Palettes relocation",    243,  16.82, 14.47, 0.0,    0.0),
    ("AV1", "Outbound Full Pallet",          "Sortie Palette Complète",           "outbound",   "Full Pallets",               "Palettes complètes",    2613,  24.09, 20.72, 1.4333, 1.7916),
    ("VL1", "Loading Pallets",               "Chargement Palettes",               "loading",    "Loaded Pallet",              "Palettes chargées",     3713,  25.22, 21.69, 1.0626, 1.3283),
    ("VL4", "Loading Parcels (Loose)",       "Chargement Colis Vrac",             "loading",    "Loose Loaded Cartons",       "Colis chargés vrac",    6869,  48.49, 41.71, 0.5526, 0.6907),
]


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def _init():
    if "mup_ready" in st.session_state:
        return
    st.session_state.mup_ready = True
    st.session_state.step    = 0
    st.session_state.lang    = "FR"
    st.session_state.cur     = "EUR"   # EUR | MAD
    st.session_state.period  = "ANN"   # ANN | MON
    for k, v in _D.items():
        st.session_state[k] = v
    st.session_state.personnel = [
        {"en":r[0],"fr":r[1],"qty":r[2],"salary":r[3],"cat":r[4]} for r in _PERSONNEL
    ]
    st.session_state.trucks = [
        {"code":r[0],"en":r[1],"fr":r[2],"qty":r[3],
         "mode":r[4],"price":r[5],"depr_years":r[6]} for r in _TRUCKS
    ]
    st.session_state.processes = [
        {"code":r[0],"en":r[1],"fr":r[2],"group":r[3],
         "b_en":r[4],"b_fr":r[5],"active":True,
         "volume":r[6],"prod_gross":r[7],"prod_net":r[8],
         "cost_unit":r[9],"price":r[10]} for r in _PROCESSES
    ]
    st.session_state.price_storage   = 7.64
    st.session_state.cost_storage    = 6.064
    st.session_state.price_fixed     = 6228.92
    st.session_state.cost_fixed      = 4983.14

_init()

s   = st.session_state
L   = lambda fr, en: fr if s.lang == "FR" else en
SYM = lambda: "MAD" if s.cur == "MAD" else "€"
FX  = lambda: s.exchange_rate    # 1 MAD = FX €  →  1 € = 1/FX MAD
PDV = lambda: 12 if s.period == "MON" else 1
PL  = lambda: L("Mensuel","Monthly") if s.period == "MON" else L("Annuel","Annual")

def to_cur(eur):
    return eur / FX() if s.cur == "MAD" and FX() > 0 else eur
def from_cur(v):
    return v * FX() if s.cur == "MAD" else v
def fmt(eur_annual, dec=0):
    v = to_cur(eur_annual) / PDV()
    return f"{v:,.{dec}f} {SYM()}" if dec else f"{v:,.0f} {SYM()}"
def fmt_u(eur, dec=4):
    v = to_cur(eur)
    return f"{v:,.{dec}f} {SYM()}"


# ══════════════════════════════════════════════════════════════════════════════
# ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def net_loc():
    return round(s.gross_loc * (1 - s.op_reserve_pct / 100))

def inv_annual(total, r_pct, years, maint_pct=1.0):
    if total <= 0 or years <= 0: return 0
    r = r_pct / 100
    return total / years + total * r * (years + 1) / (2 * years) + total * maint_pct / 100

def calc_wh():
    surf = s.wh_surface
    rent_eur_m2 = (s.rent_mad + s.charges_mad + s.taxes_mad) * s.exchange_rate
    r, dy = s.interest_rate, s.invest_years
    return {
        "rent":     surf * rent_eur_m2 * 12,
        "office":   100  * rent_eur_m2 * 12 + inv_annual(1.85*1364, r, 12, 1),
        "racking":  inv_annual(s.racking_ppl * s.racking_qty, r, dy, 1),
        "security": inv_annual(s.security_m2 * surf,  r, 5, 1),
        "cabling":  inv_annual(s.cabling_m2  * surf,  r, 5, 1),
        "shelves":  inv_annual(s.lower_shelf_qty * s.lower_shelf_price, r, dy, 1),
        "grating":  inv_annual(s.grating_qty * s.grating_price, r, dy, 1),
    }

def calc_pers():
    sc = s.social_pct / 100
    var = fix = fte = 0.0
    for p in s.personnel:
        q = p["qty"]
        if q <= 0: continue
        cost = p["salary"] * q * (1 + sc)
        fte += q
        if p["cat"] == "OP": var += cost
        else:                 fix += cost
    return {"var": var, "fix": fix, "total": var + fix, "fte": fte}

def calc_trucks_total():
    total = 0.0
    for tk in s.trucks:
        if tk["qty"] > 0:
            total += inv_annual(tk["price"] * tk["qty"], s.interest_rate, tk["depr_years"], 2.0)
    return total

def calc_ps():
    nl = net_loc()
    lines = []
    total_ca = total_cost = 0.0
    # Storage
    ca_s = s.price_storage * nl * 12; co_s = s.cost_storage * nl * 12
    lines.append({"name": L("Stockage","Storage"), "vol": nl*12, "price": s.price_storage,
                  "cost_u": s.cost_storage, "ca": ca_s, "cost": co_s})
    # Fixed
    ca_f = s.price_fixed * 12; co_f = s.cost_fixed * 12
    lines.append({"name": L("Forfait fixe","Fixed Lump Sum"), "vol": 12, "price": s.price_fixed,
                  "cost_u": s.cost_fixed, "ca": ca_f, "cost": co_f})
    total_ca += ca_s + ca_f; total_cost += co_s + co_f
    # Processes
    for p in s.processes:
        if not p["active"]: continue
        ca = p["price"] * p["volume"]; co = p["cost_unit"] * p["volume"]
        lines.append({"code": p["code"],
                      "name": p["fr"] if s.lang=="FR" else p["en"],
                      "unit": p["b_fr"] if s.lang=="FR" else p["b_en"],
                      "vol": p["volume"], "price": p["price"],
                      "cost_u": p["cost_unit"], "ca": ca, "cost": co})
        total_ca += ca; total_cost += co
    wms_c = total_ca * s.wms_alloc_pct / 100
    ho_c  = total_ca * s.ho_alloc_pct  / 100
    total_cost_all = total_cost + wms_c + ho_c
    profit = total_ca - total_cost_all
    margin = profit / total_ca * 100 if total_ca > 0 else 0
    return {"lines": lines, "total_ca": total_ca, "total_cost_proc": total_cost,
            "wms": wms_c, "ho": ho_c, "total_cost": total_cost_all,
            "profit": profit, "margin": margin}

def calc_all():
    wh = calc_wh(); wh["total"] = sum(wh.values())
    pe = calc_pers(); tk = calc_trucks_total(); ps = calc_ps()
    return wh, pe, tk, ps


# ══════════════════════════════════════════════════════════════════════════════
# STEP DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════
STEPS = [
    L("Projet",         "Project"),
    L("Paramètres",     "Parameters"),
    L("Entrepôt",       "Warehouse"),
    L("Personnel",      "Personnel"),
    L("Engins",         "Trucks"),
    L("Processus",      "Processes"),
    L("Grille tarif.",  "Price Sheet"),
    L("Résultats",      "Results"),
]

STEP_ICONS = ["📋","⚙️","🏭","👷","🚜","⚡","💶","📊"]


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT — HEADER + KPI + WIZARD NAV
# ══════════════════════════════════════════════════════════════════════════════
wh_r, pe_r, tk_r, ps_r = calc_all()

st.markdown(f"""
<div class="mup-header">
  <div class="mup-logo">📦 Polka <span>MUP</span>
    <span style="font-size:.75rem;font-weight:400;color:#475569;margin-left:10px">Multi-User Pricing Tool</span>
  </div>
  <div class="mup-project">
    <div class="name">{s.project} &nbsp;·&nbsp; {s.customer}</div>
    <div class="sub">{s.branch} &nbsp;·&nbsp; {s.country} &nbsp;·&nbsp; {s.business_unit}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Controls row — language, currency, period
ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([1.5, 2, 2.5, 3])
with ctrl1:
    lang_v = st.radio("", ["FR","EN"], horizontal=True, index=0 if s.lang=="FR" else 1, key="_l")
    if lang_v != s.lang: s.lang = lang_v; st.rerun()
with ctrl2:
    cur_v = st.radio("", ["EUR (€)","MAD (درهم)"], horizontal=True, index=0 if s.cur=="EUR" else 1, key="_c")
    new_c = "EUR" if cur_v.startswith("EUR") else "MAD"
    if new_c != s.cur: s.cur = new_c; st.rerun()
with ctrl3:
    per_v = st.radio("", [L("Annuel","Annual"), L("Mensuel","Monthly")], horizontal=True, index=0 if s.period=="ANN" else 1, key="_p")
    new_p = "ANN" if per_v in ("Annuel","Annual") else "MON"
    if new_p != s.period: s.period = new_p; st.rerun()
with ctrl4:
    rate_info = f"1 € = {1/FX():.2f} MAD" if s.cur=="MAD" else f"1 MAD = {FX():.4f} €"
    mc = "up" if ps_r["margin"] >= s.target_margin else "down"
    st.caption(f"{rate_info}  ·  {L('Vue','View')}: **{PL()}**  ·  {L('Marge','Margin')}: **{ps_r['margin']:.1f}%** {'✅' if mc=='up' else '❌'}")

# KPI Bar
m_color = "up" if ps_r["margin"] >= s.target_margin else "down"
st.markdown(f"""
<div class="kpi-bar">
  <div class="kpi-cell">
    <div class="kpi-lbl">CA {PL()}</div>
    <div class="kpi-val blue">{fmt(ps_r['total_ca'])}</div>
    <div class="kpi-sub">Stockage: {fmt(ps_r['lines'][0]['ca'])}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-lbl">{L('Coûts','Costs')} {PL()}</div>
    <div class="kpi-val">{fmt(ps_r['total_cost'])}</div>
    <div class="kpi-sub">WH+Pers+Engins: {fmt(wh_r['total']+pe_r['total']+tk_r)}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-lbl">{L('Profit','Profit')} {PL()}</div>
    <div class="kpi-val {m_color}">{fmt(ps_r['profit'])}</div>
    <div class="kpi-sub">{L('Cible','Target')}: {fmt(ps_r['total_ca']*s.target_margin/100)}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-lbl">{L('Marge réelle','Actual Margin')}</div>
    <div class="kpi-val {m_color}">{ps_r['margin']:.2f}%</div>
    <div class="kpi-sub">{L('Cible','Target')} {s.target_margin:.1f}% {'✅' if ps_r['margin']>=s.target_margin else '❌'}</div>
  </div>
  <div class="kpi-cell">
    <div class="kpi-lbl">{L('Emplacements nets','Net Locations')} · FTE</div>
    <div class="kpi-val">{net_loc():,}</div>
    <div class="kpi-sub">{L('sur','of')} {s.gross_loc:.0f} {L('bruts','gross')} · {pe_r['fte']:.2f} FTE</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Progress bar
segs = "".join([
    f'<div class="prog-seg {"done" if i < s.step else "active" if i == s.step else ""}"></div>'
    for i in range(len(STEPS))
])
st.markdown(f'<div class="prog-arrow">{segs}</div>', unsafe_allow_html=True)

# Step wizard nav
step_html = ""
for i, (icon, label) in enumerate(zip(STEP_ICONS, STEPS)):
    if i < s.step: cls = "wstep done"
    elif i == s.step: cls = "wstep active"
    else: cls = "wstep todo"
    step_html += f'<div class="{cls}"><span class="dot"></span>{icon} {label}</div>'
st.markdown(f'<div class="wizard-nav">{step_html}</div>', unsafe_allow_html=True)

# Clickable step buttons (invisible overlay via columns trick)
nav_cols = st.columns(len(STEPS))
for i, col in enumerate(nav_cols):
    with col:
        if st.button("​", key=f"_snav_{i}", help=STEPS[i], use_container_width=True):  # zero-width space
            s.step = i; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS FOR STEPS
# ══════════════════════════════════════════════════════════════════════════════
def nav_btns(step_idx):
    _, prev_col, _, next_col, _ = st.columns([3, 1, 2, 1, 3])
    with prev_col:
        if step_idx > 0:
            if st.button(f"← {L('Retour','Back')}", use_container_width=True, key=f"prev_{step_idx}"):
                s.step -= 1; st.rerun()
    with next_col:
        if step_idx < len(STEPS) - 1:
            label = L("Suivant","Next") + " →"
            if st.button(label, use_container_width=True, type="primary", key=f"next_{step_idx}"):
                s.step += 1; st.rerun()

def calc_block_html(label, formula, result, color="highlight"):
    return f"""
    <div class="calc-block">
      <div class="calc-label">{label}</div>
      <div class="calc-formula">{formula}</div>
      <div class="calc-result {color}">{result}</div>
    </div>"""

def calc_total_html(label, value):
    return f"""
    <div class="calc-total">
      <span class="calc-total-label">{label}</span>
      <span class="calc-total-value">{value}</span>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
# STEP 0 — PROJET
# ══════════════════════════════════════════════════════════════════════════════
if s.step == 0:
    left, right = st.columns([1.4, 1])
    with left:
        st.markdown('<div class="form-section-title">📋 ' + L("Informations Projet","Project Information") + '</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            s.project        = st.text_input(L("Nom du projet","Project Name"),               value=s.project)
            s.customer       = st.text_input(L("Client","Customer"),                           value=s.customer)
            s.project_leader = st.text_input(L("Chef de projet","Project Leader"),            value=s.project_leader)
            s.branch         = st.text_input(L("Agence (code)","Branch (code)"),              value=s.branch)
        with c2:
            s.country_org    = st.text_input(L("Organisation pays","Country Organisation"),   value=s.country_org)
            s.country        = st.text_input(L("Pays","Country"),                             value=s.country)
            s.business_unit  = st.text_input(L("Business Unit","Business Unit"),              value=s.business_unit)
            s.sector         = st.text_input(L("Secteur","Sector"),                           value=s.sector)
    with right:
        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="calc-panel-title">ℹ️ ' + L("À propos de cet outil","About this tool") + '</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:0.8rem;color:#94a3b8;line-height:1.7">
        <b style="color:#3b82f6">Polka MUP</b> — Multi-User Pricing Tool<br><br>
        {L(
        "Cet outil reproduit fidèlement la méthodologie du fichier MUP Excel. Il calcule le coût complet d'un entrepôt logistique et génère une grille tarifaire précise.",
        "This tool faithfully reproduces the MUP Excel methodology. It computes the full cost of a logistics warehouse and generates an accurate price sheet."
        )}<br><br>
        <b style="color:#e2e8f0">{L("Les 8 étapes :","The 8 steps:")}</b><br>
        📋 {L("Identification du projet","Project identification")}<br>
        ⚙️ {L("Paramètres financiers","Financial parameters")}<br>
        🏭 {L("Coûts entrepôt","Warehouse costs")}<br>
        👷 {L("Coûts personnel","Personnel costs")}<br>
        🚜 {L("Coûts engins","Truck costs")}<br>
        ⚡ {L("Volumes & productivités","Volumes & productivities")}<br>
        💶 {L("Grille tarifaire","Price sheet")}<br>
        📊 {L("Résultats & analyse","Results & analysis")}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    nav_btns(0)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — PARAMÈTRES
# ══════════════════════════════════════════════════════════════════════════════
elif s.step == 1:
    left, right = st.columns([1.4, 1])
    with left:
        st.markdown('<div class="form-section-title">⚙️ ' + L("Paramètres Généraux","General Parameters") + '</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            s.working_days   = st.number_input(L("Jours ouvrés / an","Yearly Working Days"),            value=float(s.working_days),   min_value=1.0,   max_value=365.0, step=1.0)
            s.target_margin  = st.number_input(L("Marge cible %","Target Profit Margin %"),             value=float(s.target_margin),  min_value=0.0,   max_value=100.0, step=0.5)
            s.interest_rate  = st.number_input(L("Taux d'intérêt interne %","Internal Interest Rate %"),value=float(s.interest_rate),  min_value=0.0,   max_value=50.0,  step=0.1, format="%.2f")
            s.contract_years = st.number_input(L("Durée contrat (ans)","Contract Years"),               value=float(s.contract_years), min_value=1.0,   max_value=20.0,  step=1.0)
        with c2:
            s.wms            = st.text_input(L("Système WMS","WMS"),                                    value=s.wms)
            s.wms_alloc_pct  = st.number_input(L("Allocation WMS %","WMS Allocation %"),                value=float(s.wms_alloc_pct),  min_value=0.0,   max_value=10.0,  step=0.1, format="%.2f")
            s.ho_alloc_pct   = st.number_input(L("Allocation HO %","HO Allocation %"),                  value=float(s.ho_alloc_pct),   min_value=0.0,   max_value=5.0,   step=0.01, format="%.4f")
            s.term_payment   = st.number_input(L("Délai paiement (jours)","Payment Terms (days)"),      value=float(s.term_payment),   min_value=0.0,   max_value=180.0, step=1.0)
        with c3:
            s.exchange_rate  = st.number_input(L("Taux de change (1 MAD = ? €)","Exchange Rate (1 MAD = ? €)"), value=float(s.exchange_rate), min_value=0.001, max_value=1.0, step=0.001, format="%.4f")
            s.failure_rate   = st.number_input(L("Taux de panne engins %","Equipment Failure Rate %"),  value=float(s.failure_rate),   min_value=0.0,   max_value=50.0, step=0.5)
            s.social_pct     = st.number_input(L("Charges sociales %","Social Charges %"),              value=float(s.social_pct),     min_value=0.0,   max_value=100.0, step=0.1, format="%.1f")

    with right:
        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="calc-panel-title">🔢 ' + L("Impact sur la marge","Margin Impact") + '</div>', unsafe_allow_html=True)
        target_profit = ps_r["total_ca"] * s.target_margin / 100
        wms_cost  = ps_r["total_ca"] * s.wms_alloc_pct / 100
        ho_cost   = ps_r["total_ca"] * s.ho_alloc_pct  / 100
        st.markdown(
            calc_block_html(
                L("Profit cible","Target Profit"),
                f"CA × {s.target_margin:.1f}% = {fmt(ps_r['total_ca'])} × {s.target_margin:.1f}%",
                fmt(target_profit), "green"
            ) +
            calc_block_html(
                L("Coût WMS alloué","WMS Allocated Cost"),
                f"CA × {s.wms_alloc_pct:.2f}% = {fmt(ps_r['total_ca'])} × {s.wms_alloc_pct:.2f}%",
                fmt(wms_cost)
            ) +
            calc_block_html(
                L("Coût HO alloué","HO Allocated Cost"),
                f"CA × {s.ho_alloc_pct:.4f}% = {fmt(ps_r['total_ca'])} × {s.ho_alloc_pct:.4f}%",
                fmt(ho_cost)
            ) +
            calc_block_html(
                L("Taux de change","Exchange Rate"),
                f"1 MAD = {s.exchange_rate:.4f} €\n1 € = {1/FX():.2f} MAD",
                f"1 € = {1/FX():.2f} MAD", "highlight"
            ),
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    nav_btns(1)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — ENTREPÔT
# ══════════════════════════════════════════════════════════════════════════════
elif s.step == 2:
    wh = calc_wh(); wh["total"] = sum(wh.values())
    rent_eur_m2 = (s.rent_mad + s.charges_mad + s.taxes_mad) * s.exchange_rate

    left, right = st.columns([1.4, 1])
    with left:
        st.markdown('<div class="form-section-title">📐 ' + L("Dimensions & Emplacements","Dimensions & Locations") + '</div>', unsafe_allow_html=True)
        d1, d2, d3, d4 = st.columns(4)
        s.wh_surface      = d1.number_input(L("Surface (m²)","Surface (m²)"),         value=float(s.wh_surface),      min_value=0.0, step=10.0)
        s.wh_height       = d2.number_input(L("Hauteur (m)","Height (m)"),             value=float(s.wh_height),       min_value=0.0, step=0.5, format="%.1f")
        s.gross_loc       = d3.number_input(L("Empl. bruts","Gross Locations"),        value=float(s.gross_loc),       min_value=0.0, step=1.0)
        s.op_reserve_pct  = d4.number_input(L("Réserve op. %","Reserve %"),            value=float(s.op_reserve_pct),  min_value=0.0, max_value=50.0, step=0.5)
        s.avg_pal         = d1.number_input(L("Palettes moy. en stock","Avg Pallets"), value=float(s.avg_pal),         min_value=0.0, step=10.0)
        s.invest_years    = d2.number_input(L("Amortissement (ans)","Depreciation"),   value=float(s.invest_years),    min_value=1.0, max_value=30.0, step=1.0)

        st.markdown('<div class="form-section-title" style="margin-top:1rem">💰 ' + L("Loyer & Charges","Rent & Charges") + '</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        s.rent_mad        = r1.number_input(L("Loyer (MAD/m²/mois)","Rent (MAD/m²/mo)"),     value=float(s.rent_mad),     min_value=0.0, step=0.5, format="%.2f")
        s.charges_mad     = r2.number_input(L("Charges (MAD/m²/mois)","Charges (MAD/m²/mo)"),value=float(s.charges_mad),  min_value=0.0, step=0.1, format="%.2f")
        s.taxes_mad       = r3.number_input(L("Taxes / Idilité","Taxes / Idilité"),           value=float(s.taxes_mad),    min_value=0.0, step=0.01, format="%.3f")

        st.markdown('<div class="form-section-title" style="margin-top:1rem">🔧 ' + L("Investissements Entrepôt","Warehouse Investments") + '</div>', unsafe_allow_html=True)
        i1, i2, i3, i4 = st.columns(4)
        s.racking_ppl         = i1.number_input(L("Rayonnage €/PPL","Racking €/PPL"),    value=float(s.racking_ppl),         min_value=0.0, step=1.0)
        s.racking_qty         = i2.number_input(L("Rayonnage qté","Racking qty"),         value=float(s.racking_qty),         min_value=0.0, step=1.0)
        s.security_m2         = i3.number_input(L("Sécurité €/m²","Security €/m²"),       value=float(s.security_m2),         min_value=0.0, step=0.5)
        s.cabling_m2          = i4.number_input(L("Câblage €/m²","Cabling €/m²"),         value=float(s.cabling_m2),          min_value=0.0, step=0.5)
        s.lower_shelf_qty     = i1.number_input(L("Étagères qté","Shelves qty"),           value=float(s.lower_shelf_qty),     min_value=0.0, step=1.0)
        s.lower_shelf_price   = i2.number_input(L("Étagères €/pc","Shelves €/pc"),         value=float(s.lower_shelf_price),   min_value=0.0, step=1.0)
        s.grating_qty         = i3.number_input(L("Caillebotis qté","Grating qty"),        value=float(s.grating_qty),         min_value=0.0, step=1.0)
        s.grating_price       = i4.number_input(L("Caillebotis €/pc","Grating €/pc"),      value=float(s.grating_price),       min_value=0.0, step=1.0)

    with right:
        wh = calc_wh(); wh["total"] = sum(wh.values())
        rent_mad_total = s.rent_mad + s.charges_mad + s.taxes_mad
        rent_eur_m2 = rent_mad_total * s.exchange_rate
        nl = net_loc()

        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="calc-panel-title">🏭 ' + L("Calcul détaillé des coûts","Detailed Cost Calculation") + f' ({PL()})</div>', unsafe_allow_html=True)

        st.markdown(
            calc_block_html(
                L("Emplacements nets vendables","Net Sellable Locations"),
                f"{s.gross_loc:.0f} × (1 − {s.op_reserve_pct:.0f}%)",
                f"{nl:,} PPL", "highlight"
            ) +
            calc_block_html(
                L("Loyer total","Total Rent"),
                f"{rent_mad_total:.2f} MAD × {s.exchange_rate:.4f} × {s.wh_surface:.0f}m² × 12",
                fmt(wh["rent"])
            ) +
            calc_block_html(
                L("Rayonnage (amort.)","Racking (depreciation)"),
                f"{s.racking_ppl:.0f}€ × {s.racking_qty:.0f} PPL\n÷ {s.invest_years:.0f} ans + intérêts {s.interest_rate:.1f}%",
                fmt(wh["racking"])
            ) +
            calc_block_html(
                L("Sécurité + Câblage","Security + Cabling"),
                f"({s.security_m2:.0f} + {s.cabling_m2:.0f}) €/m² × {s.wh_surface:.0f}m²\n÷ 5 ans + intérêts",
                fmt(wh["security"] + wh["cabling"])
            ) +
            calc_block_html(
                L("Bureaux + Équipement","Office + Equipment"),
                f"100 m² × {rent_eur_m2:.4f} €/m²/mois × 12 + amort.",
                fmt(wh["office"])
            ) +
            calc_block_html(
                L("Étagères + Caillebotis","Shelves + Grating"),
                f"{s.lower_shelf_qty:.0f} × {s.lower_shelf_price:.0f}€ + {s.grating_qty:.0f} × {s.grating_price:.0f}€",
                fmt(wh["shelves"] + wh["grating"])
            ) +
            calc_total_html(f"TOTAL {L('Entrepôt','Warehouse')} ({PL()})", fmt(wh["total"])),
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    nav_btns(2)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — PERSONNEL
# ══════════════════════════════════════════════════════════════════════════════
elif s.step == 3:
    pe = calc_pers()
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown('<div class="form-section-title">👷 ' + L("Personnel","Personnel") + '</div>', unsafe_allow_html=True)
        sc_val = st.number_input(L("Charges sociales %","Social Charges %"), value=float(s.social_pct), min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key="sc_input")
        s.social_pct = sc_val

        sc = s.social_pct / 100
        cat_labels = {"OP":"🔵","ADM":"🟡","MGT":"🔴"}
        cat_names  = {"OP": L("Opérationnels","Operatives"),
                      "ADM": L("Bureau / Admin","Office / Admin"),
                      "MGT": L("Management","Management")}
        prev_cat = None
        hcols = st.columns([3, 1, 1.8, 0.9, 0.9, 1.6])
        for c, lb in zip(hcols, [L("Rôle","Role"), "FTE", L("Salaire brut (€)","Gross Salary (€)"),
                                   L("Abs.%","Ill.%"), L("Cgs","Hol."),
                                   L(f"Coût ({SYM()})","Cost ({SYM()})")]):
            c.markdown(f"<div style='font-size:.63rem;text-transform:uppercase;letter-spacing:1px;color:#475569;font-weight:600'>{lb}</div>", unsafe_allow_html=True)

        for i, p in enumerate(s.personnel):
            if p["cat"] != prev_cat:
                st.markdown(f"<div style='margin:6px 0 3px 0;font-size:.7rem;font-weight:600;color:#94a3b8'>{cat_labels[p['cat']]} {cat_names[p['cat']]}</div>", unsafe_allow_html=True)
                prev_cat = p["cat"]
            role = p["fr"] if s.lang == "FR" else p["en"]
            cols = st.columns([3, 1, 1.8, 0.9, 0.9, 1.6])
            cols[0].markdown(f"<div style='font-size:.8rem;padding:3px 0;color:#c8d0e0'>{role}</div>", unsafe_allow_html=True)
            p["qty"]    = cols[1].number_input("", value=float(p["qty"]),    key=f"pq_{i}", min_value=0.0, max_value=20.0, step=0.25,  label_visibility="collapsed")
            p["salary"] = cols[2].number_input("", value=float(p["salary"]), key=f"ps_{i}", min_value=0.0, step=100.0,     label_visibility="collapsed")
            if p["cat"] != "MGT":
                p.setdefault("illness",  4.97)
                p.setdefault("holidays", 25)
                ill = cols[3].number_input("", value=float(p["illness"]),  key=f"pi_{i}", min_value=0.0, max_value=50.0, step=0.1, format="%.1f", label_visibility="collapsed")
                hol = cols[4].number_input("", value=float(p["holidays"]), key=f"ph_{i}", min_value=0.0, max_value=60.0, step=1.0, label_visibility="collapsed")
                p["illness"] = ill; p["holidays"] = hol
            else:
                cols[3].markdown("<div style='color:#334155;font-size:.8rem;padding:3px 0'>—</div>", unsafe_allow_html=True)
                cols[4].markdown("<div style='color:#334155;font-size:.8rem;padding:3px 0'>—</div>", unsafe_allow_html=True)
            annual = p["salary"] * p["qty"] * (1 + sc) if p["qty"] > 0 else 0
            cols[5].markdown(f"<div style='font-size:.78rem;font-family:JetBrains Mono,monospace;color:#dde3f0;padding:3px 0'>{fmt(annual)}</div>", unsafe_allow_html=True)

    with right:
        pe = calc_pers()
        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="calc-panel-title">👷 ' + L("Calcul des coûts personnel","Personnel Cost Calculation") + f' ({PL()})</div>', unsafe_allow_html=True)

        op_fte  = sum(p["qty"] for p in s.personnel if p["cat"]=="OP")
        adm_fte = sum(p["qty"] for p in s.personnel if p["cat"]=="ADM")
        mgt_fte = sum(p["qty"] for p in s.personnel if p["cat"]=="MGT")
        st.markdown(
            calc_block_html(
                L("Formule coût annuel","Annual Cost Formula"),
                f"Salaire brut × ETP × (1 + {s.social_pct:.1f}%)",
                L("Par rôle, somme ci-dessous","Per role, summed below")
            ) +
            calc_block_html(
                L("🔵 Opérationnels (variable)","🔵 Operatives (variable)"),
                f"{op_fte:.2f} FTE × salaire moyen × (1+{s.social_pct:.1f}%)",
                fmt(pe["var"]), "highlight"
            ) +
            calc_block_html(
                L("🟡 Bureau + 🔴 Management (fixe)","🟡 Office + 🔴 Management (fixed)"),
                f"{adm_fte:.2f} + {mgt_fte:.2f} = {adm_fte+mgt_fte:.2f} FTE fixes",
                fmt(pe["fix"])
            ) +
            calc_block_html(
                L("Répartition fixe / variable","Fixed / Variable Split"),
                f"Variable: {pe['var']/pe['total']*100:.1f}%  ·  Fixe: {pe['fix']/pe['total']*100:.1f}%" if pe["total"] > 0 else "—",
                f"Total FTE: {pe['fte']:.2f}", "highlight"
            ) +
            calc_total_html(f"TOTAL {L('Personnel','Personnel')} ({PL()})", fmt(pe["total"])),
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    nav_btns(3)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — ENGINS
# ══════════════════════════════════════════════════════════════════════════════
elif s.step == 4:
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown('<div class="form-section-title">🚜 ' + L("Engins de manutention","Industrial Trucks") + '</div>', unsafe_allow_html=True)
        hcols = st.columns([3.2, 0.7, 2, 1.8, 1.4, 1.8])
        for c, lb in zip(hcols, [L("Engin","Truck"), L("Qté","Qty"),
                                   L("Location/Achat","Rent/Purchase"),
                                   L("Prix total (€)","Total Price (€)"),
                                   L("Amort.","Depr."),
                                   L(f"Coût/an ({SYM()})","Annual Cost ({SYM()})")]):
            c.markdown(f"<div style='font-size:.63rem;text-transform:uppercase;letter-spacing:1px;color:#475569;font-weight:600'>{lb}</div>", unsafe_allow_html=True)

        total_tk = 0.0
        for i, tk in enumerate(s.trucks):
            name = tk["fr"] if s.lang == "FR" else tk["en"]
            cols = st.columns([3.2, 0.7, 2, 1.8, 1.4, 1.8])
            cols[0].markdown(f"<div style='font-size:.78rem;padding:3px 0'><span style='color:#475569;font-size:.65rem'>{tk['code']}</span> {name}</div>", unsafe_allow_html=True)
            tk["qty"]       = cols[1].number_input("", value=float(tk["qty"]),       key=f"tq_{i}", min_value=0.0, max_value=20.0, step=0.5, label_visibility="collapsed")
            tk["mode"]      = cols[2].selectbox("",   ["External Rent","Purchase"],   key=f"tm_{i}", index=0 if tk["mode"]=="External Rent" else 1, label_visibility="collapsed")
            tk["price"]     = cols[3].number_input("", value=float(tk["price"]),      key=f"tp_{i}", min_value=0.0, step=100.0, label_visibility="collapsed")
            tk["depr_years"]= cols[4].number_input("", value=float(tk["depr_years"]), key=f"td_{i}", min_value=1.0, max_value=20.0, step=1.0, label_visibility="collapsed")
            annual = inv_annual(tk["price"] * tk["qty"], s.interest_rate, tk["depr_years"], 2.0) if tk["qty"] > 0 else 0.0
            total_tk += annual
            cols[5].markdown(f"<div style='font-size:.78rem;font-family:JetBrains Mono,monospace;color:{'#22c55e' if annual>0 else '#334155'};padding:3px 0'>{fmt(annual) if tk['qty']>0 else '—'}</div>", unsafe_allow_html=True)

    with right:
        total_tk = calc_trucks_total()
        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="calc-panel-title">🚜 ' + L("Calcul des coûts engins","Truck Cost Calculation") + f' ({PL()})</div>', unsafe_allow_html=True)

        active_trucks = [tk for tk in s.trucks if tk["qty"] > 0]
        formula_lines = []
        for tk in active_trucks:
            invest = tk["price"] * tk["qty"]
            ann = inv_annual(invest, s.interest_rate, tk["depr_years"], 2.0)
            formula_lines.append(f"{tk['code']}: {tk['qty']:.0f}×{tk['price']:,.0f}€ → {fmt(ann)}")

        formula_str = "\n".join(formula_lines) if formula_lines else L("Aucun engin alloué","No trucks allocated")

        st.markdown(
            calc_block_html(
                L("Formule annualisation","Annualisation Formula"),
                f"Invest ÷ {s.interest_rate:.0f}ans + intérêts ({s.interest_rate:.1f}%)\n+ maintenance (2%)",
                L("Voir détail par engin →","See detail per truck →")
            ) +
            calc_block_html(
                L("Détail par engin alloué","Detail per allocated truck"),
                formula_str,
                f"{len(active_trucks)} {L('engin(s) actif(s)','active truck(s)')}", "highlight"
            ) +
            calc_total_html(f"TOTAL {L('Engins','Trucks')} ({PL()})", fmt(total_tk)),
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    nav_btns(4)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — PROCESSUS & VOLUMES
# ══════════════════════════════════════════════════════════════════════════════
elif s.step == 5:
    wd = s.working_days
    group_labels = {
        "inbound":    L("📥 Réception (Inbound)","📥 Inbound"),
        "picking":    L("🎯 Préparation (Picking)","🎯 Picking"),
        "relocation": L("🔄 Réapprovisionnement","🔄 Relocation"),
        "outbound":   L("📤 Sortie Palette Complète","📤 Outbound Full Pallet"),
        "loading":    L("🚛 Chargement","🚛 Loading"),
    }

    left, right = st.columns([1.4, 1])
    with left:
        cur_grp = None
        hcols = st.columns([0.5, 3.5, 1.3, 2.5, 1.4, 1.4, 1.2])
        for c, lb in zip(hcols, ["✓", L("Processus","Process"), L("Volume/an","Vol/year"),
                                   L("Unité","Unit"), L("Prod.brute/h","Gross/h"),
                                   L("Prod.nette/h","Net/h"), L("h/jour","h/day")]):
            c.markdown(f"<div style='font-size:.63rem;text-transform:uppercase;letter-spacing:1px;color:#475569;font-weight:600'>{lb}</div>", unsafe_allow_html=True)

        for i, proc in enumerate(s.processes):
            if proc["group"] != cur_grp:
                cur_grp = proc["group"]
                st.markdown(f"<div style='margin:8px 0 2px 0;font-size:.72rem;font-weight:600;color:#3b82f6'>{group_labels[cur_grp]}</div>", unsafe_allow_html=True)

            pk   = f"proc_{i}"
            name = proc["fr"] if s.lang == "FR" else proc["en"]
            unit = proc["b_fr"] if s.lang == "FR" else proc["b_en"]
            cols = st.columns([0.5, 3.5, 1.3, 2.5, 1.4, 1.4, 1.2])
            proc["active"]     = cols[0].checkbox("", value=proc["active"], key=f"pa_{pk}", label_visibility="collapsed")
            color = "#dde3f0" if proc["active"] else "#334155"
            cols[1].markdown(f"<div style='font-size:.78rem;padding:3px 0;color:{color}'>{name}</div>", unsafe_allow_html=True)
            if proc["active"]:
                proc["volume"]     = cols[2].number_input("", value=float(proc["volume"]),     key=f"pv_{pk}", min_value=0.0, step=100.0, label_visibility="collapsed")
                cols[3].markdown(f"<div style='font-size:.72rem;color:#64748b;padding:4px 0'>{unit}</div>", unsafe_allow_html=True)
                proc["prod_gross"] = cols[4].number_input("", value=float(proc["prod_gross"]), key=f"pg_{pk}", min_value=0.1, step=1.0, format="%.2f", label_visibility="collapsed")
                proc["prod_net"]   = cols[5].number_input("", value=float(proc["prod_net"]),   key=f"pn_{pk}", min_value=0.1, step=1.0, format="%.2f", label_visibility="collapsed")
                h_day = proc["volume"] / wd / proc["prod_net"] if wd > 0 and proc["prod_net"] > 0 else 0
                cols[6].markdown(f"<div style='font-size:.78rem;font-family:JetBrains Mono,monospace;color:#3b82f6;padding:3px 0'>{h_day:.2f}h</div>", unsafe_allow_html=True)
            else:
                for c in cols[2:]: c.markdown("<div style='color:#1e2a45;font-size:.8rem;padding:3px 0'>—</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="calc-panel-title">⚡ ' + L("Analyse des charges","Workload Analysis") + '</div>', unsafe_allow_html=True)
        total_h_day = 0.0
        for proc in s.processes:
            if proc["active"] and proc["prod_net"] > 0 and wd > 0:
                h = proc["volume"] / wd / proc["prod_net"]
                total_h_day += h
        needed_fte = total_h_day / 7.5 if total_h_day > 0 else 0  # ~7.5h paid per day

        st.markdown(
            calc_block_html(
                L("Charge journalière totale","Total Daily Workload"),
                L(f"Σ (Volume annuel ÷ {wd:.0f} jours ÷ prod. nette)",
                  f"Σ (Annual volume ÷ {wd:.0f} days ÷ net productivity)"),
                f"{total_h_day:.2f} h/jour", "highlight"
            ) +
            calc_block_html(
                L("FTE opérationnels estimés","Estimated Operative FTE"),
                f"{total_h_day:.2f}h ÷ 7.5h/ETP/jour",
                f"≈ {needed_fte:.2f} FTE", "green" if needed_fte <= pe_r["fte"] else "down"
            ) +
            calc_block_html(
                L("FTE alloués (étape 4)","Allocated FTE (step 4)"),
                L("Opérationnels dans Cockpit Personnel",
                  "Operatives in Cockpit Personnel"),
                f"{sum(p['qty'] for p in s.personnel if p['cat']=='OP'):.2f} FTE OP"
            ),
            unsafe_allow_html=True
        )
        # Process summary table
        st.markdown(f"<div style='font-size:.65rem;text-transform:uppercase;letter-spacing:1px;color:#475569;margin-top:10px;margin-bottom:6px'>{L('Processus actifs','Active Processes')}</div>", unsafe_allow_html=True)
        for proc in s.processes:
            if not proc["active"]: continue
            name = proc["fr"] if s.lang == "FR" else proc["en"]
            h = proc["volume"] / wd / proc["prod_net"] if wd > 0 and proc["prod_net"] > 0 else 0
            st.markdown(f"<div style='display:flex;justify-content:space-between;font-size:.72rem;padding:2px 0;border-bottom:1px solid #1e2a45'><span style='color:#94a3b8'>{name[:28]}</span><span style='font-family:JetBrains Mono,monospace;color:#3b82f6'>{h:.2f}h</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    nav_btns(5)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — GRILLE TARIFAIRE
# ══════════════════════════════════════════════════════════════════════════════
elif s.step == 6:
    nl = net_loc()

    left, right = st.columns([1.4, 1])
    with left:
        st.markdown(f'<div class="form-section-title">💶 {L("Grille Tarifaire","Price Sheet")} — {PL()} · {SYM()}</div>', unsafe_allow_html=True)

        # Column headers
        hcols = st.columns([2.8, 2, 1.3, 1.8, 1.8, 1.4])
        for c, lb in zip(hcols, [
            L("Ligne","Line"), L("Unité de facturation","Billing Unit"),
            L("Volume","Volume"),
            L(f"Coût unit. ({SYM()})","Unit Cost ({SYM()})"),
            L(f"Prix vente ({SYM()})","Selling Price ({SYM()})"),
            L("Marge %","Margin %"),
        ]):
            c.markdown(f"<div style='font-size:.63rem;text-transform:uppercase;letter-spacing:1px;color:#475569;font-weight:600'>{lb}</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        def prow(label, unit, volume, cost_eur, price_eur_key, price_eur_val, row_i, is_ss=False):
            cols = st.columns([2.8, 2, 1.3, 1.8, 1.8, 1.4])
            cols[0].markdown(f"<div style='font-size:.8rem;padding:3px 0'>{label}</div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div style='font-size:.72rem;color:#64748b;padding:4px 0'>{unit}</div>", unsafe_allow_html=True)
            cols[2].markdown(f"<div style='font-size:.78rem;font-family:JetBrains Mono,monospace;color:#94a3b8;padding:3px 0'>{volume:,}</div>", unsafe_allow_html=True)
            cols[3].markdown(f"<div style='font-size:.78rem;font-family:JetBrains Mono,monospace;color:#475569;padding:3px 0'>{fmt_u(cost_eur)}</div>", unsafe_allow_html=True)
            # Price input in display currency
            disp = to_cur(price_eur_val)
            new_disp = cols[4].number_input("", value=float(disp), key=f"price_{row_i}",
                                             min_value=0.0, step=0.01 if s.cur=="EUR" else 0.1,
                                             format="%.4f" if s.cur=="EUR" else "%.3f",
                                             label_visibility="collapsed")
            new_eur = from_cur(new_disp)
            # Compute CA and margin
            ca   = new_eur * volume
            cost = cost_eur * volume
            margin_v = (ca - cost) / ca * 100 if ca > 0 else 0
            m_col = "#22c55e" if margin_v >= s.target_margin else "#ef4444"
            cols[5].markdown(f"<div style='font-size:.78rem;font-family:JetBrains Mono,monospace;color:{m_col};font-weight:600;padding:3px 0'>{margin_v:.1f}%</div>", unsafe_allow_html=True)
            return new_eur, ca, cost

        row_i = 0
        # Storage
        new_ps, ca_s, co_s = prow(L("Stockage","Storage"),
                                    L("Emplacement/mois","Location/month"),
                                    nl*12, s.cost_storage, "storage_price", s.price_storage, row_i)
        s.price_storage = new_ps; row_i += 1

        # Fixed
        new_pf, ca_f, co_f = prow(L("Forfait fixe mensuel","Fixed Monthly Lump Sum"),
                                    L("Mois","Month"),
                                    12, s.cost_fixed, "fixed_price", s.price_fixed, row_i)
        s.price_fixed = new_pf; row_i += 1

        st.markdown("<div style='border-top:1px solid #1e2a45;margin:4px 0'></div>", unsafe_allow_html=True)

        # Processes
        for proc in s.processes:
            if not proc["active"]: continue
            name = proc["fr"] if s.lang == "FR" else proc["en"]
            unit = proc["b_fr"] if s.lang == "FR" else proc["b_en"]
            new_pp, _, _ = prow(name, unit, proc["volume"],
                                 proc["cost_unit"], f"proc_{proc['code']}", proc["price"], row_i)
            proc["price"] = new_pp; row_i += 1

    with right:
        ps = calc_ps()
        st.markdown('<div class="calc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="calc-panel-title">💶 ' + L("Analyse de la grille","Price Sheet Analysis") + f' ({PL()} · {SYM()})</div>', unsafe_allow_html=True)

        wms_c = ps["total_ca"] * s.wms_alloc_pct / 100
        ho_c  = ps["total_ca"] * s.ho_alloc_pct  / 100
        m_color = "green" if ps["margin"] >= s.target_margin else "down"

        # Top process by CA
        proc_lines = sorted([l for l in ps["lines"] if l.get("code")], key=lambda x: x["ca"], reverse=True)
        top_line   = proc_lines[0] if proc_lines else None

        st.markdown(
            calc_block_html(
                L("CA processus variables","Variable Process Revenue"),
                L(f"Σ prix × volume, {len(proc_lines)} processus actifs",
                  f"Σ price × volume, {len(proc_lines)} active processes"),
                fmt(sum(l["ca"] for l in proc_lines)), "highlight"
            ) +
            calc_block_html(
                L("Stockage + Forfait fixe","Storage + Fixed"),
                f"{fmt(ps['lines'][0]['ca'])} + {fmt(ps['lines'][1]['ca'])}",
                fmt(ps["lines"][0]["ca"] + ps["lines"][1]["ca"])
            ) +
            calc_block_html(
                L("WMS + HO (% du CA)","WMS + HO (% of Revenue)"),
                f"{s.wms_alloc_pct:.2f}% + {s.ho_alloc_pct:.4f}% × CA",
                fmt(wms_c + ho_c)
            ) +
            calc_block_html(
                L("Marge réalisée","Achieved Margin"),
                f"(CA - Coûts) ÷ CA × 100\nCible: {s.target_margin:.1f}%",
                f"{ps['margin']:.2f}%", m_color
            ) +
            calc_total_html(f"CA TOTAL {L('','Revenue')} ({PL()})", fmt(ps["total_ca"])),
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    nav_btns(6)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 7 — RÉSULTATS
# ══════════════════════════════════════════════════════════════════════════════
elif s.step == 7:
    wh, pe, tk, ps = calc_all()
    target = s.target_margin
    margin = ps["margin"]
    gap    = margin - target

    # Success/error banner
    if margin >= target:
        st.success(f"✅ {L('Marge réalisée','Actual Margin')} **{margin:.2f}%** ≥ {L('Cible','Target')} **{target:.1f}%** — {L('Projet rentable ✓','Profitable project ✓')}")
    else:
        st.error(f"❌ {L('Marge réalisée','Actual Margin')} **{margin:.2f}%** < {L('Cible','Target')} **{target:.1f}%** — {L('Réviser les tarifs','Revise pricing')} ({gap:+.2f}%)")

    st.markdown("---")

    # Top KPIs
    st.markdown(f"<div style='font-size:.65rem;text-transform:uppercase;letter-spacing:1.5px;color:#3b82f6;font-weight:600;margin-bottom:.8rem'>{L('INDICATEURS CLÉS','KEY METRICS')} — {PL()} · {SYM()}</div>", unsafe_allow_html=True)
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric(L("Chiffre d'affaires","Revenue"),     fmt(ps["total_ca"]))
    k2.metric(L("Coûts totaux","Total Costs"),        fmt(ps["total_cost"]))
    k3.metric(L("Profit","Profit"),                   fmt(ps["profit"]),    delta=f"{gap:+.2f}%", delta_color="normal" if gap>=0 else "inverse")
    k4.metric(L("Marge réelle","Actual Margin"),      f"{margin:.2f}%")
    k5.metric(L("Marge cible","Target Margin"),       f"{target:.1f}%")
    k6.metric(L("Emplacements nets","Net Locations"), f"{net_loc():,} PPL")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    # ── COST BREAKDOWN ──
    with col_a:
        st.markdown(f"<div style='font-size:.65rem;text-transform:uppercase;letter-spacing:1.5px;color:#3b82f6;font-weight:600;margin-bottom:.8rem'>{L('DÉCOMPOSITION DES COÛTS','COST BREAKDOWN')} ({PL()} · {SYM()})</div>", unsafe_allow_html=True)
        total_costs = ps["total_cost"]
        cost_rows = [
            ("🏭", L("Entrepôt","Warehouse"),     wh["total"],   "#3b82f6"),
            ("👷", L("Personnel","Personnel"),    pe["total"],   "#8b5cf6"),
            ("🚜", L("Engins","Trucks"),           tk,            "#06b6d4"),
            ("💻", "WMS",                          ps["wms"],     "#f59e0b"),
            ("🏢", "HO",                           ps["ho"],      "#10b981"),
        ]
        for icon, label, val, color in cost_rows:
            pct = val / total_costs * 100 if total_costs > 0 else 0
            pct_ca = val / ps["total_ca"] * 100 if ps["total_ca"] > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:12px">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="font-size:.82rem">{icon} {label}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:.82rem;color:#e2e8f0">{fmt(val)} <span style="color:#475569;font-size:.72rem">({pct_ca:.1f}% CA)</span></span>
              </div>
              <div style="background:#1e2a45;border-radius:3px;height:5px;overflow:hidden">
                <div style="background:{color};height:100%;width:{min(pct*1.2,100):.1f}%;border-radius:3px;transition:width .4s"></div>
              </div>
              <div style="font-size:.65rem;color:#475569;margin-top:2px">{pct:.1f}% {L('des coûts','of costs')}</div>
            </div>""", unsafe_allow_html=True)

        # Full cost reconciliation
        st.markdown(f"""
        <div style="background:#060b14;border:1px solid #1e2a45;border-radius:8px;padding:12px;margin-top:8px">
          <div style="font-size:.65rem;text-transform:uppercase;letter-spacing:1px;color:#475569;margin-bottom:8px">{L('RÉCONCILIATION','RECONCILIATION')}</div>
          <div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:3px"><span style="color:#94a3b8">CA</span><span style="font-family:JetBrains Mono,monospace;color:#3b82f6">{fmt(ps['total_ca'])}</span></div>
          <div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:3px"><span style="color:#94a3b8">− Coûts</span><span style="font-family:JetBrains Mono,monospace;color:#e2e8f0">− {fmt(total_costs)}</span></div>
          <div style="border-top:1px solid #1e2a45;margin:6px 0"></div>
          <div style="display:flex;justify-content:space-between;font-size:.9rem;font-weight:700"><span style="color:#94a3b8">=  Profit</span><span style="font-family:JetBrains Mono,monospace;color:{'#22c55e' if ps['profit']>=0 else '#ef4444'}">{fmt(ps['profit'])}</span></div>
          <div style="display:flex;justify-content:space-between;font-size:.78rem;margin-top:4px"><span style="color:#94a3b8">Marge</span><span style="font-family:JetBrains Mono,monospace;color:{'#22c55e' if margin>=target else '#ef4444'};font-weight:600">{margin:.2f}% {L('vs cible','vs target')} {target:.1f}%</span></div>
        </div>""", unsafe_allow_html=True)

    # ── REVENUE BREAKDOWN ──
    with col_b:
        st.markdown(f"<div style='font-size:.65rem;text-transform:uppercase;letter-spacing:1.5px;color:#3b82f6;font-weight:600;margin-bottom:.8rem'>{L('DÉTAIL DU CA','REVENUE BREAKDOWN')} ({PL()} · {SYM()})</div>", unsafe_allow_html=True)
        lines_sorted = sorted(ps["lines"], key=lambda x: x["ca"], reverse=True)
        for line in lines_sorted:
            ca_v = line["ca"]
            pct  = ca_v / ps["total_ca"] * 100 if ps["total_ca"] > 0 else 0
            cost_line = line["cost"]
            margin_line = (ca_v - cost_line) / ca_v * 100 if ca_v > 0 else 0
            mc = "#22c55e" if margin_line >= target else "#ef4444"
            st.markdown(f"""
            <div style="margin-bottom:10px">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                <span style="font-size:.78rem;color:#c8d0e0">{line['name']}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;color:#3b82f6">{fmt(ca_v)}</span>
              </div>
              <div style="background:#1e2a45;border-radius:3px;height:4px;overflow:hidden">
                <div style="background:#22c55e;height:100%;width:{min(pct*1.5,100):.1f}%;border-radius:3px"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:.65rem;color:#475569;margin-top:2px">
                <span>{pct:.1f}% CA</span>
                <span style="color:{mc}">marge: {margin_line:.1f}%</span>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── RATIOS ──
    st.markdown(f"<div style='font-size:.65rem;text-transform:uppercase;letter-spacing:1.5px;color:#3b82f6;font-weight:600;margin-bottom:.8rem'>{L('RATIOS EFFICACITÉ','EFFICIENCY RATIOS')}</div>", unsafe_allow_html=True)
    r1, r2, r3, r4, r5 = st.columns(5)
    surf = s.wh_surface; fte = pe["fte"]
    r1.metric("CA / m²",                                    fmt(ps["total_ca"] / surf) if surf > 0 else "—")
    r2.metric(L("CA / emplacement","CA / Location"),         fmt(ps["total_ca"] / net_loc()) if net_loc() > 0 else "—")
    r3.metric(L("Coût / m²","Cost / m²"),                   fmt(ps["total_cost"] / surf) if surf > 0 else "—")
    r4.metric(L("Profit / FTE","Profit / FTE"),             fmt(ps["profit"] / fte) if fte > 0 else "—")
    r5.metric(L("CA / FTE","Revenue / FTE"),                fmt(ps["total_ca"] / fte) if fte > 0 else "—")

    st.markdown("---")

    # ── PROJECT CARD ──
    st.markdown(f"<div style='font-size:.65rem;text-transform:uppercase;letter-spacing:1.5px;color:#3b82f6;font-weight:600;margin-bottom:.8rem'>{L('FICHE PROJET','PROJECT CARD')}</div>", unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    def info_card(title, rows):
        cells = "".join([f"<div style='margin-bottom:6px'><div style='font-size:.65rem;color:#475569'>{k}</div><div style='font-size:.85rem;font-weight:500;color:#e2e8f0'>{v}</div></div>" for k,v in rows])
        return f"""<div style="background:#060b14;border:1px solid #1e2a45;border-radius:8px;padding:14px">
        <div style="font-size:.62rem;text-transform:uppercase;letter-spacing:1.2px;color:#3b82f6;font-weight:600;margin-bottom:10px">{title}</div>
        {cells}</div>"""
    pc1.markdown(info_card(L("Identification","Identification"), [
        (L("Projet","Project"), s.project), (L("Client","Customer"), s.customer), (L("Secteur","Sector"), s.sector)
    ]), unsafe_allow_html=True)
    pc2.markdown(info_card(L("Localisation","Location"), [
        (L("Agence","Branch"), s.branch), (L("Pays","Country"), s.country), (L("Chef de projet","Project Leader"), s.project_leader)
    ]), unsafe_allow_html=True)
    pc3.markdown(info_card(L("Paramètres clés","Key Parameters"), [
        (L("WMS · Jours ouvrés","WMS · Working Days"), f"{s.wms} · {s.working_days:.0f}j"),
        (L("Contrat · Marge cible","Contract · Target Margin"), f"{s.contract_years:.0f} {L('ans','years')} · {target:.1f}%"),
        (L("Surface · Empl. nets","Surface · Net Loc."), f"{surf:.0f} m² · {net_loc():,} PPL"),
    ]), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    nav_btns(7)
