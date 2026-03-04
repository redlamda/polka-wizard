"""
POLKA WIZARD v4 — Tarification Contract Logistics
Benchmark 3 clients : OCP · AKZO Nobel · BASF Agriculture
Site : MA-Mohammedia (580) · Dachser CL
"""
import streamlit as st
import pandas as pd
from copy import deepcopy
import json

st.set_page_config(page_title="Polka Wizard", page_icon="📦", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp{background:#f0f4fb;color:#1a1d2e;font-family:'Inter',sans-serif}
.block-container{padding-top:1rem;max-width:1300px}
[data-testid="stSidebar"]{background:#1e2240;color:#e8eaf6}
[data-testid="stSidebar"] label,[data-testid="stSidebar"] .stRadio label{color:#c5cae9!important}
[data-testid="stSidebar"] p{color:#9fa8da}
.step-hdr{background:linear-gradient(135deg,#1e2240,#2a3060);border-left:5px solid #5c7cff;
 border-radius:0 14px 14px 0;padding:14px 20px;margin-bottom:18px;color:white}
.step-num{font-size:11px;color:#8899ff;text-transform:uppercase;letter-spacing:1px}
.step-ttl{font-size:21px;font-weight:800;margin:3px 0}
.step-dsc{font-size:13px;color:#aab4d8}
.help-box{background:#e8edff;border-left:4px solid #5c7cff;border-radius:0 10px 10px 0;
 padding:10px 14px;font-size:12.5px;color:#2a3060;margin:5px 0 12px 0;line-height:1.6}
.kpi-row{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}
.kpi{background:white;border:1px solid #dce3f5;border-radius:12px;padding:14px 18px;
 flex:1;min-width:150px;box-shadow:0 2px 6px rgba(0,0,0,.05)}
.kpi-lbl{font-size:11px;color:#6b7bad;text-transform:uppercase;letter-spacing:.6px;margin-bottom:4px}
.kpi-val{font-size:21px;font-weight:800}
.kpi-sub{font-size:11px;color:#8892b0;margin-top:2px}
.green{color:#0d9e6e}.red{color:#d63c4a}.blue{color:#2952d9}.orange{color:#d97706}.purple{color:#7c3aed}
.alert-ok{background:#d1fae5;border:1px solid #6ee7b7;border-radius:8px;padding:9px 13px;
 font-size:13px;color:#065f46;margin:7px 0}
.alert-warn{background:#fff3cd;border:1px solid #fcd34d;border-radius:8px;padding:9px 13px;
 font-size:13px;color:#92400e;margin:7px 0}
.alert-info{background:#dbeafe;border:1px solid #93c5fd;border-radius:8px;padding:9px 13px;
 font-size:13px;color:#1e40af;margin:7px 0}
.sec{font-size:14px;font-weight:700;color:#2a3060;border-bottom:2px solid #c5cdf5;
 padding-bottom:4px;margin:18px 0 8px 0}
.bm-card{background:white;border:1px solid #dce3f5;border-radius:12px;padding:14px 16px;
 margin:6px 0;box-shadow:0 2px 6px rgba(0,0,0,.04)}
.bm-ttl{font-size:13px;font-weight:700;color:#1e2240;margin-bottom:6px}
.tag{display:inline-block;padding:2px 9px;border-radius:10px;font-size:11px;font-weight:700;margin:2px}
.tag-ocp{background:#dbeafe;color:#1e40af}
.tag-akzo{background:#fce7f3;color:#9d174d}
.tag-basf{background:#dcfce7;color:#166534}
.tag-avg{background:#f3f4f6;color:#374151}
stNumberInput>label,stTextInput>label,stSlider>label,stCheckbox>label,stSelectbox>label{
 color:#2a3060!important;font-weight:600}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# DONNÉES BENCHMARK — 3 CLIENTS
# ═══════════════════════════════════════════════════
BENCHMARK = {
    "OCP": {
        "label": "OCP Morocco",
        "secteur": "Fertilisants / Phosphates",
        "annee": 2026,
        "tag": "tag-ocp",
        # Site
        "surface_m2": 4039.74, "hauteur_m": 10.0,
        "emplacements_brut": 4211, "emplacements_nets": 4000, "taux_utilisation": 95.0,
        # Loyer (MAD → €, taxe 10.5% + charge 2%)
        "loyer_m2_mois": 5.22, "taxe_charges_pct": 12.5, "taux_change": 10.84,
        # Investissements (€/unité · durée amort)
        "rack_ppl": 30.0, "amort_rack": 12,
        "secu_m2": 12.0,  "amort_secu": 10,
        "cable_m2": 10.5, "amort_cable": 5,
        # ETP précis (Cockpit Personnel)
        "fte": {"cariste": 3.30, "chargeur": 1.57, "dechargeur": 0.85,
                "ctrl": 0.50, "picker": 0.0, "admin_in": 1.0, "admin_out": 0.0,
                "team_ldr": 0.0, "ops_mgr": 0.0, "stock_mgr": 0.0},
        "fte_op_total": 6.22, "fte_adm_total": 1.0,
        # Salaires bruts annuels (€)
        "sal_op": 13829, "sal_adm": 18628, "charges_soc": 33.3,
        "ho_pct": 0.863, "rho_pct": 5.3,
        # Engins alloués (qt · €/an)
        "engins": [("Fast Mover FZ0040", 2.79, 10606),
                   ("Reach Truck >8m FZ0085", 3.42, 44619)],
        "engins_qt": 6.21, "engins_cout": 56074,
        # Volumes annuels actifs
        "vol_in_pal": 70720, "vol_out_pal": 70720,
        "vol_picks": 0, "vol_colis": 0,
        "empl_vendus": 4000,
        # Productivités (pal/h productif)
        "prod_dech": 37.63, "prod_stock": 34.02,
        "prod_prel": 27.69, "prod_charg": 32.19,
        # IT
        "cout_it": 2182, "alloc_wms_pct": 2.2, "wms": "MIKADO",
        # Financiers
        "jours": 272, "taux_interet": 9.0, "marge_cible": 10.0, "taux_fluctuation": 0.0,
        # Tarifs réels facturés
        "tarif_stock_mois": 6.58, "tarif_in": 2.562, "tarif_out": 2.929,
        "tarif_fixe_mois": 0.0,
        # Résultats financiers Polka
        "ca": 704164, "couts": 643523, "profit": 60641, "marge_pct": 8.61,
        "ca_stock": 315840, "ca_in": 181167, "ca_out": 207156,
        "cout_wh": 358678, "cout_pers": 148419, "cout_engins": 56074, "cout_it_total": 11243,
        # Processus actifs
        "processus": ["FP Inbound (MF1070)", "Storage (WH0010)", "FP Outbound (MF4010)",
                      "FP Loading (MF5020)"],
        "processus_inactifs": ["Picking colis", "Palettes mixtes", "VAS", "Réappro"],
    },
    "AKZO": {
        "label": "AKZO Nobel",
        "secteur": "Peintures & Revêtements",
        "annee": 2021,
        "tag": "tag-akzo",
        "surface_m2": 1600.0, "hauteur_m": 10.0,
        "emplacements_brut": 2413, "emplacements_nets": 2172, "taux_utilisation": 90.0,
        "loyer_m2_mois": 5.177, "taxe_charges_pct": 12.5, "taux_change": 10.6,
        "rack_ppl": 35.0, "amort_rack": 12,
        "secu_m2": 5.0, "amort_secu": 12,
        "cable_m2": 5.0, "amort_cable": 12,
        "fte": {"cariste": 1.0, "chargeur": 1.0, "dechargeur": 0.0, "picker": 1.0,
                "ctrl": 0.0, "admin_in": 0.0, "admin_out": 0.0,
                "team_ldr": 1.0, "ops_mgr": 0.15, "stock_mgr": 0.5},
        "fte_op_total": 3.0, "fte_adm_total": 1.85,
        "sal_op": 13722, "sal_adm": 13722, "charges_soc": 14.2,
        "ho_pct": 0.863, "rho_pct": 5.3,
        "engins": [("Fast Mover FZ0040", 1.0, 10606),
                   ("Horizontal Order Picker FZ0050", 1.0, 11956),
                   ("Reach Truck >8m FZ0085", 1.0, 44619)],
        "engins_qt": 3.0, "engins_cout": 21730,
        "vol_in_pal": 4008, "vol_out_pal": 2613,
        "vol_picks": 54660, "vol_colis": 6869,
        "empl_vendus": 2172,
        "prod_dech": 32.31, "prod_stock": 26.38,
        "prod_prel": 20.72, "prod_charg": 21.69,
        "cout_it": 0, "alloc_wms_pct": 1.7, "wms": "MIKADO",
        "jours": 272, "taux_interet": 9.0, "marge_cible": 20.0, "taux_fluctuation": 0.0,
        "tarif_stock_mois": 7.644, "tarif_in": 2.238, "tarif_out": 1.783,
        "tarif_picks": 0.548, "tarif_colis": 0.686,
        "tarif_fixe_mois": 6222.66,
        "ca": 330812, "couts": 279247, "profit": 51565, "marge_pct": 15.59,
        "ca_stock": 199245, "ca_in": 11009, "ca_out": 36270,
        "cout_wh": 123827, "cout_pers": 55906, "cout_engins": 21730, "cout_it_total": 5000,
        "processus": ["FP Inbound (MF1020)", "Stock-in Inbound (MF1070)", "Retour vrac (MF1040)",
                      "Picking ASC colis (MF2070)", "Picking MPY Powder (MF2070)",
                      "FP Outbound (MF4010)", "Loading palettes (MF5020)", "Loading colis (MF5040)"],
        "processus_inactifs": ["Réappro (inactif)", "Livraisons (KT1010=0)"],
    },
    "BASF": {
        "label": "BASF Agriculture",
        "secteur": "Produits agrochimiques",
        "annee": 2024,
        "tag": "tag-basf",
        "surface_m2": 2040.0, "hauteur_m": 10.0,
        "emplacements_brut": 1764, "emplacements_nets": 1588, "taux_utilisation": 90.0,
        "loyer_m2_mois": 6.590, "taxe_charges_pct": 12.5, "taux_change": 10.49,
        "rack_ppl": 43.0, "amort_rack": 12,
        "secu_m2": 12.0, "amort_secu": 12,
        "cable_m2": 10.5, "amort_cable": 12,
        "fte": {"cariste": 1.0, "chargeur": 0.4, "dechargeur": 0.2, "picker": 0.4,
                "ctrl": 0.0, "admin_in": 0.25, "admin_out": 0.25,
                "team_ldr": 0.0, "ops_mgr": 0.0, "stock_mgr": 0.0},
        "fte_op_total": 2.0, "fte_adm_total": 0.5,
        "sal_op": 10524, "sal_adm": 10524, "charges_soc": 11.9,
        "ho_pct": 0.863, "rho_pct": 5.3,
        "engins": [("Hand Pallet Truck FZ0010", 1.0, 375),
                   ("Front Loader FZ0070", 0.5, 8866),
                   ("Reach Truck >8m FZ0085", 0.5, 11897)],
        "engins_qt": 2.0, "engins_cout": 10913,
        "vol_in_pal": 1954, "vol_out_pal": 293,
        "vol_picks": 79723, "vol_colis": 4690,
        "empl_vendus": 1588,
        "prod_dech": 28.48, "prod_stock": 24.76,
        "prod_prel": 0.0, "prod_charg": 12.87,
        "cout_it": 3100, "alloc_wms_pct": 2.11, "wms": "MIKADO",
        "jours": 272, "taux_interet": 9.0, "marge_cible": 8.0, "taux_fluctuation": 14.57,
        "tarif_stock_mois": 12.293, "tarif_in": 0.639, "tarif_out": 0.448,
        "tarif_picks": 0.100, "tarif_colis": 0.183,
        "tarif_fixe_mois": 4617.28,
        "ca": 314900, "couts": 289708, "profit": 25192, "marge_pct": 8.0,
        "ca_stock": 234260, "ca_in": 1249, "ca_out": 716,
        "cout_wh": 191243, "cout_pers": 34089, "cout_engins": 10913, "cout_it_total": 3100,
        "processus": ["FP Inbound (MF1070)", "Storage WH0010", "Picking box (MF2070)",
                      "Picking parcels (MF2110)", "Replenishment (MF3010)",
                      "FP Outbound (MF4010)", "Loading pallets (MF5020)", "Loading boxes (MF5040)"],
        "processus_inactifs": ["Fast Mover (0)", "Livraisons (KT1010=0)"],
    },
}

# ═══════════════════════════════════════════════════
# PRESETS WIZARD
# ═══════════════════════════════════════════════════
def make_preset(b):
    return {
        "projet": b["label"], "agence": "MA-Mohammedia (580)", "wms": b.get("wms","MIKADO"),
        "jours_ouvres": b["jours"], "taux_interet": b["taux_interet"],
        "marge_cible": b["marge_cible"], "alloc_wms": b["alloc_wms_pct"],
        "taux_panne": 5.0, "batteries_li": True, "prime_fret": 15.0, "prime_colis": 5.0,
        "taux_change_mad": b["taux_change"],
        "surface_m2": b["surface_m2"], "hauteur_m": b["hauteur_m"],
        "emplacements_brut": b["emplacements_brut"], "taux_utilisation": b["taux_utilisation"],
        "loyer_m2_mois": b["loyer_m2_mois"], "taxe_communale": 10.5, "charge_locative": 2.0,
        "cout_rack_ppl": b["rack_ppl"], "amort_rack": b["amort_rack"],
        "cout_secu_m2": b["secu_m2"], "amort_secu": b["amort_secu"],
        "cout_cable_m2": b["cable_m2"], "amort_cable": b["amort_cable"],
        "fte_cariste": b["fte"].get("cariste",0), "fte_chargeur": b["fte"].get("chargeur",0),
        "fte_dechargeur": b["fte"].get("dechargeur",0), "fte_ctrl": b["fte"].get("ctrl",0),
        "fte_picker": b["fte"].get("picker",0),
        "fte_admin_in": b["fte"].get("admin_in",0), "fte_admin_out": b["fte"].get("admin_out",0),
        "fte_coord": b["fte"].get("team_ldr",0), "fte_chef": b["fte"].get("ops_mgr",0),
        "fte_resp": b["fte"].get("stock_mgr",0),
        "sal_op": b["sal_op"], "sal_adm": b["sal_adm"],
        "qt_fm":   b["engins"][0][1] if len(b["engins"])>0 else 0,
        "prix_fm": b["engins"][0][2] if len(b["engins"])>0 else 10606,
        "qt_rt8":  next((e[1] for e in b["engins"] if "8m" in e[0] and ">" in e[0]),0),
        "prix_rt8": 44619,
        "qt_rt8m": 0, "prix_rt8m": 31089,
        "qt_tp":  next((e[1] for e in b["engins"] if "Hand Pallet" in e[0]),0),
        "prix_tp": 375,
        "qt_cf":  next((e[1] for e in b["engins"] if "Front Loader" in e[0]),0),
        "prix_cf": next((e[2] for e in b["engins"] if "Front Loader" in e[0]),22644),
        "qt_ph":   next((e[1] for e in b["engins"] if "Order Picker" in e[0]),0),
        "prix_ph": 11956, "qt_ae": 0, "prix_ae": 95000, "qt_bal": 0, "prix_bal": 24990,
        "empl_vendus": b["empl_vendus"],
        "vol_in_pal": b["vol_in_pal"], "vol_out_pal": b["vol_out_pal"],
        "vol_picks": b.get("vol_picks",0), "vol_colis": b.get("vol_colis",0),
        "vol_in_livr": 0, "vol_out_cmd": 0, "vol_charg_cam": 0, "vol_charg_pal": 0,
        "cout_it": b["cout_it"],
        "prod_dech": b["prod_dech"], "prod_stock": b["prod_stock"],
        "prod_prel": b["prod_prel"], "prod_charg": b["prod_charg"],
        "tarif_stock_mois": b.get("tarif_stock_mois",0),
        "tarif_in": b.get("tarif_in",0), "tarif_out": b.get("tarif_out",0),
    }

PRESETS = {k: make_preset(v) for k, v in BENCHMARK.items()}
PRESETS["vierge"] = deepcopy(PRESETS["OCP"])
for k in ["emplacements_brut","surface_m2","loyer_m2_mois","vol_in_pal","vol_out_pal","empl_vendus"]:
    PRESETS["vierge"][k] = 0

def init():
    if "d" not in st.session_state: st.session_state.d = deepcopy(PRESETS["OCP"])
    if "step" not in st.session_state: st.session_state.step = 1
    if "preset" not in st.session_state: st.session_state.preset = "OCP"
init()
d = st.session_state.d

# ═══════════════════════════════════════════════════
# CALCUL
# ═══════════════════════════════════════════════════
def calc(d):
    r = {}
    empl_nets = round(d["emplacements_brut"] * d["taux_utilisation"] / 100)
    r["empl_nets"] = empl_nets
    ti = d["taux_interet"] / 100
    loyer = d["loyer_m2_mois"] * 12 * d["surface_m2"]
    loyer_tot = loyer * (1 + d["taxe_communale"]/100 + d["charge_locative"]/100)
    rack_an  = d["cout_rack_ppl"] * d["emplacements_brut"] * (ti + 1/max(d["amort_rack"],1))
    secu_an  = d["cout_secu_m2"] * d["surface_m2"] * (ti + 1/max(d["amort_secu"],1))
    cable_an = d["cout_cable_m2"] * d["surface_m2"] * (ti + 1/max(d["amort_cable"],1))
    cout_wh = loyer_tot + rack_an + secu_an + cable_an
    r.update({"loyer_tot": loyer_tot, "rack_an": rack_an, "secu_an": secu_an,
               "cable_an": cable_an, "cout_wh": cout_wh})
    TC = 0.333
    pers_op  = (d["fte_cariste"]+d["fte_chargeur"]+d["fte_dechargeur"]+
                d["fte_ctrl"]+d["fte_picker"]) * d["sal_op"] * (1+TC)
    pers_adm = (d["fte_admin_in"]+d["fte_admin_out"]+
                d["fte_coord"]+d["fte_chef"]+d["fte_resp"]) * d["sal_adm"] * (1+TC)
    pers_tot = pers_op + pers_adm
    fte_op  = d["fte_cariste"]+d["fte_chargeur"]+d["fte_dechargeur"]+d["fte_ctrl"]+d["fte_picker"]
    fte_adm = d["fte_admin_in"]+d["fte_admin_out"]+d["fte_coord"]+d["fte_chef"]+d["fte_resp"]
    r.update({"pers_op": pers_op, "pers_adm": pers_adm, "pers_tot": pers_tot,
               "fte_op": fte_op, "fte_adm": fte_adm, "fte_tot": fte_op+fte_adm})
    engins_cout = (d["qt_fm"]*d["prix_fm"]+d["qt_rt8"]*d["prix_rt8"]+
                   d["qt_rt8m"]*d["prix_rt8m"]+d["qt_tp"]*d["prix_tp"]+
                   d["qt_cf"]*d["prix_cf"]+d["qt_ph"]*d["prix_ph"]+
                   d["qt_ae"]*d["prix_ae"]+d["qt_bal"]*d["prix_bal"])
    r["engins_cout"] = engins_cout
    wms_alloc = (pers_op + engins_cout) * d["alloc_wms"]/100
    it_tot = d["cout_it"] + wms_alloc
    r.update({"wms_alloc": wms_alloc, "it_tot": it_tot})
    cout_tot = cout_wh + pers_tot + engins_cout + it_tot
    r["cout_tot"] = cout_tot
    v_in = max(d["vol_in_pal"],1); v_out = max(d["vol_out_pal"],1); v_tot = v_in+v_out
    proc_in  = (pers_op+engins_cout)*v_in/v_tot
    proc_out = (pers_op+engins_cout)*v_out/v_tot
    cu_in    = proc_in/v_in; cu_out = proc_out/v_out
    cu_stock = cout_wh/12/max(d["empl_vendus"],1)
    r.update({"proc_in": proc_in, "proc_out": proc_out,
               "cu_in": cu_in, "cu_out": cu_out, "cu_stock": cu_stock})
    m = d["marge_cible"]/100
    r["prix_stock"] = cu_stock/(1-m) if m<1 else 0
    r["prix_in"]    = cu_in/(1-m)    if m<1 else 0
    r["prix_out"]   = cu_out/(1-m)   if m<1 else 0
    ca_s = d["empl_vendus"]*r["prix_stock"]*12
    ca_i = d["vol_in_pal"]*r["prix_in"]
    ca_o = d["vol_out_pal"]*r["prix_out"]
    ca   = ca_s+ca_i+ca_o
    profit = ca-cout_tot
    r.update({"ca_s": ca_s,"ca_i": ca_i,"ca_o": ca_o,
               "ca": ca,"profit": profit,"marge": profit/ca*100 if ca>0 else 0})
    couts_fixes = cout_wh+pers_adm+it_tot
    tmv = (ca_i+ca_o-pers_op-engins_cout)/(ca_i+ca_o) if (ca_i+ca_o)>0 else 0
    r["seuil"] = couts_fixes/tmv if tmv>0 else 0
    return r

# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:14px 0 8px'>
      <div style='font-size:28px'>📦</div>
      <div style='font-size:15px;font-weight:800;color:#e8eaf6'>Polka Wizard v4</div>
      <div style='font-size:11px;color:#7986cb'>MA-Mohammedia · Dachser CL</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    preset_label = st.selectbox("🗂️ Jeu de données",
        ["OCP Morocco (réel 2026)", "AKZO Nobel (réel 2021)",
         "BASF Agriculture (réel 2024)", "Nouveau projet (vierge)"])
    preset_map = {"OCP Morocco (réel 2026)": "OCP", "AKZO Nobel (réel 2021)": "AKZO",
                  "BASF Agriculture (réel 2024)": "BASF", "Nouveau projet (vierge)": "vierge"}
    pk = preset_map[preset_label]
    if pk != st.session_state.preset:
        st.session_state.d = deepcopy(PRESETS[pk])
        st.session_state.preset = pk; st.rerun()

    st.divider()
    STEPS = [(1,"🏭","Entrepôt"),(2,"⚙️","Paramètres"),(3,"👷","Personnel"),
             (4,"🏗️","Engins"),(5,"📊","Volumes"),(6,"🔀","Processus"),
             (7,"💶","Tarifs"),(8,"📉","Sensibilité"),(9,"📋","Benchmark")]
    for num, icon, label in STEPS:
        active = st.session_state.step == num
        if st.button(f"{icon} {num}. {label}", key=f"nav_{num}",
                     use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.step = num; st.rerun()

    st.divider()
    try:
        r = calc(st.session_state.d)
        mc = "#4ade80" if r["marge"] >= d["marge_cible"] else "#f87171"
        st.markdown(f"""<div style='font-size:12px;color:#c5cae9'>
          <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2a3060'>
            <span>CA estimé</span><span style='color:#818cf8;font-weight:700'>{r['ca']:,.0f} €</span></div>
          <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2a3060'>
            <span>Coûts</span><span style='color:#fbbf24;font-weight:700'>{r['cout_tot']:,.0f} €</span></div>
          <div style='display:flex;justify-content:space-between;padding:4px 0'>
            <span>Marge</span><span style='color:{mc};font-weight:700'>{r['marge']:.2f}%</span></div>
        </div>""", unsafe_allow_html=True)
    except: pass

# ═══════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════
def hdr(num, icon, title, desc):
    st.markdown(f"""<div class='step-hdr'>
      <div class='step-num'>ÉTAPE {num} / 9</div>
      <div class='step-ttl'>{icon} {title}</div>
      <div class='step-dsc'>{desc}</div></div>""", unsafe_allow_html=True)

def info(txt): st.markdown(f"<div class='help-box'>ℹ️ {txt}</div>", unsafe_allow_html=True)
def ok(txt):   st.markdown(f"<div class='alert-ok'>✅ {txt}</div>", unsafe_allow_html=True)
def warn(txt): st.markdown(f"<div class='alert-warn'>⚠️ {txt}</div>", unsafe_allow_html=True)
def hint(txt): st.markdown(f"<div class='alert-info'>💡 {txt}</div>", unsafe_allow_html=True)

def nav(step):
    c1,_,c3 = st.columns([1,5,1])
    with c1:
        if step>1 and st.button("← Retour", use_container_width=True, key=f"back_{step}"):
            st.session_state.step=step-1; st.rerun()
    with c3:
        lbl = "Suivant →" if step<9 else "🔄 Début"
        if st.button(lbl, type="primary", use_container_width=True, key=f"next_{step}"):
            st.session_state.step=(step+1) if step<9 else 1; st.rerun()

def num(label, val, mn=0.0, mx=999999.0, step=1.0, key=None, help=None):
    return st.number_input(label, min_value=float(mn), max_value=float(mx),
                           value=float(val), step=float(step), key=key, help=help)

def num_int(label, val, mn=0, mx=999999, step=1, key=None, help=None):
    return st.number_input(label, min_value=int(mn), max_value=int(mx),
                           value=int(val), step=int(step), key=key, help=help)

def bm_badges():
    """Render 3 client badges with key metrics inline"""
    cols = st.columns(3)
    colors = {"OCP":"#dbeafe","AKZO":"#fce7f3","BASF":"#dcfce7"}
    tcolors = {"OCP":"#1e40af","AKZO":"#9d174d","BASF":"#166534"}
    for i,(k,b) in enumerate(BENCHMARK.items()):
        with cols[i]:
            st.markdown(f"""<div style='background:{colors[k]};border-radius:10px;
              padding:12px 14px;border:1px solid {tcolors[k]}22'>
              <div style='font-weight:800;color:{tcolors[k]};font-size:13px'>{b["label"]}</div>
              <div style='font-size:11px;color:{tcolors[k]}99;margin-bottom:6px'>{b["secteur"]} · {b["annee"]}</div>
              <div style='font-size:12px;color:#374151'>
                CA : <b>{b["ca"]:,} €</b> · Marge : <b>{b["marge_pct"]:.1f}%</b><br>
                {b["surface_m2"]:,.0f} m² · {b["emplacements_brut"]:,} empl. · {b["fte_op_total"]+b["fte_adm_total"]:.1f} ETP
              </div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# ÉTAPES 1–8 (reprises de v3 avec ajout benchmark hints)
# ═══════════════════════════════════════════════════
step = st.session_state.step

if step == 1:
    hdr(1,"🏭","Projet & Entrepôt","Informations du contrat et caractéristiques physiques du site.")
    bm_badges()
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>🏢 Identification</div>", unsafe_allow_html=True)
        d["projet"]      = st.text_input("Client / Projet", value=d.get("projet",""))
        d["agence"]      = st.text_input("Agence Dachser", value=d.get("agence",""))
        d["wms"]         = st.text_input("WMS utilisé", value=d.get("wms","MIKADO"))

        st.markdown("<div class='sec'>📐 Dimensions</div>", unsafe_allow_html=True)
        info("OCP 4 040m² · AKZO 1 600m² · BASF 2 040m² — tous à 10m de hauteur, MA-Mohammedia")
        d["surface_m2"]        = num("Surface nette (m²)", d["surface_m2"], step=50.0, key="s_m2")
        d["hauteur_m"]         = num("Hauteur utile (m)", d["hauteur_m"], mn=3.0, mx=30.0, step=0.5, key="haut")
        d["emplacements_brut"] = num_int("Emplacements palettes (brut)", d["emplacements_brut"], step=10, key="empl_b")
        d["taux_utilisation"]  = num("Taux utilisation (%)", d["taux_utilisation"], mn=50.0, mx=100.0, step=1.0, key="taux_u",
                                     help="OCP=95% | AKZO=90% | BASF=90%")
        empl_nets = round(d["emplacements_brut"]*d["taux_utilisation"]/100)
        densite   = d["emplacements_brut"]/max(d["surface_m2"],1)
        st.markdown(f"""<div class='kpi-row'>
          <div class='kpi'><div class='kpi-lbl'>Empl. nets</div><div class='kpi-val blue'>{empl_nets:,}</div></div>
          <div class='kpi'><div class='kpi-lbl'>Volume m³</div><div class='kpi-val blue'>{d["surface_m2"]*d["hauteur_m"]:,.0f}</div></div>
          <div class='kpi'><div class='kpi-lbl'>Densité pal/m²</div><div class='kpi-val blue'>{densite:.2f}</div></div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='sec'>💰 Loyer & charges (Maroc)</div>", unsafe_allow_html=True)
        info("Loyer MAD/m²/mois ÷ taux change. <b>Taxe communale 10,5% + Charges locatives 2%</b> spécifiques Maroc.<br>"
             "OCP 5,22€ (56,58 MAD÷10,84) · AKZO 5,18€ · BASF 6,59€")
        d["loyer_m2_mois"]   = num("Loyer (€/m²/mois)", d["loyer_m2_mois"], step=0.1, key="loy")
        d["taux_change_mad"] = num("Taux MAD/€", d["taux_change_mad"], mn=1.0, mx=30.0, step=0.1, key="fx",
                                   help="OCP=10.84 · AKZO=10.6 · BASF=10.49")
        d["taxe_communale"]  = num("Taxe communale (%)", d["taxe_communale"], mn=0.0, mx=50.0, step=0.5, key="tax")
        d["charge_locative"] = num("Charges locatives (%)", d["charge_locative"], mn=0.0, mx=20.0, step=0.5, key="chg")

        st.markdown("<div class='sec'>🔧 Investissements</div>", unsafe_allow_html=True)
        info("Annuité Polka = Invst × (taux + 1/durée). OCP rack 30€/PPL·12ans | AKZO 35€/PPL | BASF 43€/PPL (plus cher = petite qté)")
        c1i,c2i = st.columns(2)
        with c1i:
            d["cout_rack_ppl"] = num("Racks (€/empl.)", d["cout_rack_ppl"], step=1.0, key="rack_p")
            d["cout_secu_m2"]  = num("Sécurité (€/m²)", d["cout_secu_m2"], step=0.5, key="secu_m")
            d["cout_cable_m2"] = num("Câblage (€/m²)", d["cout_cable_m2"], step=0.5, key="cab_m")
        with c2i:
            d["amort_rack"]  = num_int("Amort. racks (ans)", d["amort_rack"], mn=1, mx=30, key="am_r")
            d["amort_secu"]  = num_int("Amort. sécu (ans)", d["amort_secu"], mn=1, mx=20, key="am_s")
            d["amort_cable"] = num_int("Amort. câblage (ans)", d["amort_cable"], mn=1, mx=15, key="am_c")
        r = calc(d)
        st.markdown(f"""<div class='kpi-row'>
          <div class='kpi'><div class='kpi-lbl'>Loyer annuel (chargé)</div><div class='kpi-val blue'>{r['loyer_tot']:,.0f} €</div></div>
          <div class='kpi'><div class='kpi-lbl'>Investissements/an</div><div class='kpi-val orange'>{r['rack_an']+r['secu_an']+r['cable_an']:,.0f} €</div></div>
          <div class='kpi'><div class='kpi-lbl'>Total entrepôt</div><div class='kpi-val blue'>{r['cout_wh']:,.0f} €</div></div>
        </div>""", unsafe_allow_html=True)
        hint("Coût entrepôt : OCP <b>358 678€</b> · AKZO <b>123 827€</b> · BASF <b>191 243€</b>")
    nav(1)

elif step == 2:
    hdr(2,"⚙️","Paramètres Polka","Hypothèses financières et opérationnelles.")
    bm_badges()
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>📅 Opérationnel</div>", unsafe_allow_html=True)
        d["jours_ouvres"] = num_int("Jours ouvrés / an", d["jours_ouvres"], mn=200, mx=365, key="jours",
                                    help="3 clients = 272 j (5j/sem Maroc)")
        d["reserve_op"]   = num("Réserve opérationnelle (%)", d.get("reserve_op",10.0), mn=0.0, mx=30.0, step=1.0, key="res_op")
        d["taux_panne"]   = num("Taux défaillance engins (%)", d["taux_panne"], mn=0.0, mx=30.0, step=0.5, key="panne",
                                 help="Polka standard = 5%")
        d["batteries_li"] = st.checkbox("Batteries lithium-ion", value=bool(d["batteries_li"]),
                                         help="OCP & AKZO = Oui | BASF = Non")
        if d["batteries_li"]: ok("LI — pas de doublement parc")
        else: warn("Batteries classiques — prévoir engins substitution")
    with col2:
        st.markdown("<div class='sec'>💰 Financier</div>", unsafe_allow_html=True)
        d["taux_interet"] = num("Taux d'intérêt interne (%)", d["taux_interet"], mn=0.0, mx=30.0, step=0.5, key="ti",
                                 help="3 clients = 9% (Dachser standard)")
        d["marge_cible"]  = num("🎯 Marge cible (%)", d["marge_cible"], mn=0.0, mx=30.0, step=0.5, key="marge_c",
                                 help="OCP=10% · AKZO=20% · BASF=8%")
        d["alloc_wms"]    = num("Allocation WMS + Innovation (%)", d["alloc_wms"], mn=0.0, mx=10.0, step=0.1, key="wms_a",
                                 help="OCP=2.2% · AKZO=1.7% · BASF=2.11%")
        info("Marge réelle obtenue : OCP <b>8,61%</b> (obj.10%) · AKZO <b>15,59%</b> (obj.20%) · BASF <b>8,0%</b> (obj.8%)")
    nav(2)

elif step == 3:
    hdr(3,"👷","Cockpit Personnel","Effectifs ETP par rôle et coûts salariaux.")
    info("Charges sociales Maroc ≈ <b>33%</b> (simplification Polka — vs. 14% AKZO, 12% BASF selon les fiches).<br>"
         "OCP : sal. op. 13 829€ · AKZO : 13 722€ · BASF : 10 524€ (salaires bruts annuels en €)")
    col1,col2 = st.columns([3,2])
    with col1:
        st.markdown("<div class='sec'>🔵 Logistics Operatives</div>", unsafe_allow_html=True)
        STAFF_OP = [
            ("fte_cariste","🚛 Cariste (Forklift driver)","OCP=3.30 · AKZO=1.00 · BASF=1.00"),
            ("fte_chargeur","📦 Chargeur (Loader)","OCP=1.57 · AKZO=1.00 · BASF=0.40"),
            ("fte_dechargeur","📥 Déchargeur (Unloader)","OCP=0.85 · AKZO=0 · BASF=0.20"),
            ("fte_ctrl","🔍 Contrôleur réception","OCP=0.50 · AKZO=0 · BASF=0"),
            ("fte_picker","🛒 Préparateur (Picker)","OCP=0 · AKZO=1.00 · BASF=0.40"),
        ]
        for k,lbl,tip in STAFF_OP:
            c1,c2 = st.columns([2,1])
            with c1: d[k] = num(lbl, d[k], mn=0.0, mx=30.0, step=0.01, key=f"op_{k}", help=tip)
            with c2: st.metric("€/an", f"{d[k]*d['sal_op']*1.333:,.0f}")
        d["sal_op"] = num_int("💶 Salaire brut opérationnel (€/an)", d["sal_op"], mn=0, mx=100000, step=100, key="sal_op_v")

        st.markdown("<div class='sec'>🟡 Office Employees</div>", unsafe_allow_html=True)
        STAFF_ADM = [
            ("fte_admin_in","📋 Admin. réception","OCP=1.00 · AKZO=0 · BASF=0.25"),
            ("fte_admin_out","📤 Admin. expédition","OCP=0 · AKZO=0 · BASF=0.25"),
            ("fte_coord","👥 Chef d'équipe (Team Leader)","OCP=0 · AKZO=1.00 · BASF=0"),
            ("fte_chef","🔧 Ops Manager","OCP=0 · AKZO=0.15 · BASF=0"),
            ("fte_resp","📊 Stock Manager","OCP=0 · AKZO=0.50 · BASF=0"),
        ]
        for k,lbl,tip in STAFF_ADM:
            c1,c2 = st.columns([2,1])
            with c1: d[k] = num(lbl, d[k], mn=0.0, mx=20.0, step=0.01, key=f"adm_{k}", help=tip)
            with c2: st.metric("€/an", f"{d[k]*d['sal_adm']*1.333:,.0f}")
        d["sal_adm"] = num_int("💶 Salaire brut admin (€/an)", d["sal_adm"], mn=0, mx=200000, step=100, key="sal_adm_v")

    with col2:
        r = calc(d)
        st.markdown("<div class='sec'>📊 Résumé</div>", unsafe_allow_html=True)
        st.markdown(f"""<div class='kpi-row' style='flex-direction:column'>
          <div class='kpi'><div class='kpi-lbl'>ETP total</div><div class='kpi-val blue'>{r['fte_tot']:.2f}</div>
            <div class='kpi-sub'>Op: {r['fte_op']:.2f} · Adm: {r['fte_adm']:.2f}</div></div>
          <div class='kpi'><div class='kpi-lbl'>Personnel opérat.</div><div class='kpi-val orange'>{r['pers_op']:,.0f} €</div></div>
          <div class='kpi'><div class='kpi-lbl'>Personnel admin.</div><div class='kpi-val orange'>{r['pers_adm']:,.0f} €</div></div>
          <div class='kpi'><div class='kpi-lbl'>TOTAL personnel</div><div class='kpi-val blue'>{r['pers_tot']:,.0f} €</div></div>
        </div>""", unsafe_allow_html=True)
        hint("Coût pers. réel :<br>OCP <b>148 419€</b> (7.22 ETP)<br>AKZO <b>55 906€</b> (4.85 ETP)<br>BASF <b>34 089€</b> (2.50 ETP)")
        st.markdown("<div class='sec'>📈 Productivités</div>", unsafe_allow_html=True)
        info("OCP / AKZO / BASF — pal/h productif")
        prod_df = pd.DataFrame({
            "Process":["Déchargement","Mise en stock","Prélèvement","Chargement"],
            "OCP":[37.63,34.02,27.69,32.19],
            "AKZO":[32.31,26.38,20.72,21.69],
            "BASF":[28.48,24.76,"—",12.87],
        })
        st.dataframe(prod_df, use_container_width=True, hide_index=True)
        d["prod_dech"]  = num("Déchargement (pal/h)", d["prod_dech"], step=1.0, key="pd1")
        d["prod_stock"] = num("Mise en stock (pal/h)", d["prod_stock"], step=1.0, key="pd2")
        d["prod_prel"]  = num("Prélèvement (pal/h)", d["prod_prel"], step=1.0, key="pd3")
        d["prod_charg"] = num("Chargement (pal/h)", d["prod_charg"], step=1.0, key="pd4")
    nav(3)

elif step == 4:
    hdr(4,"🏗️","Cockpit Engins","Parc d'engins alloué — catalogue Polka Industrial Trucks.")
    info("Même catalogue Polka pour les 3 clients. Les prix varient selon négociation/configuration locale.<br>"
         "OCP 6.21 eng · 56 074€ | AKZO 3 eng · 21 730€ | BASF 2 eng · 10 913€")

    ENGINS = [
        ("qt_fm","prix_fm","⚡ Fast Mover (FZ0040)","External Rent",10606,
         "OCP=2.79 · AKZO=1 · BASF=0 | Décharg./charg. camions"),
        ("qt_rt8","prix_rt8","🔝 Reach Truck >8m (FZ0085)","External Rent",44619,
         "OCP=3.42 · AKZO=1 · BASF=0.5 | Stock./prélèv. grande haut."),
        ("qt_rt8m","prix_rt8m","🔼 Reach Truck ≤8m (FZ0080)","External Rent",31089,
         "OCP=0 · AKZO=0 · BASF=0"),
        ("qt_tp","prix_tp","🤲 Transpalette manuel (FZ0010)","Purchase",375,
         "OCP=0 · AKZO=0 · BASF=1 | Manutention sol"),
        ("qt_cf","prix_cf","🔄 Chariot frontal (FZ0070)","External Rent",22644,
         "OCP=0 · AKZO=0 · BASF=0.5 (8 866€/an configuré)"),
        ("qt_ph","prix_ph","📋 Préparateur horiz. (FZ0050)","External Rent",11956,
         "OCP=0 · AKZO=1 · BASF=0"),
        ("qt_ae","prix_ae","↔️ Allée étroite (FZ0090)","External Rent",95000,
         "Aucun des 3 clients"),
        ("qt_bal","prix_bal","🧹 Balayeuse (FZ0100)","Purchase",24990,
         "Aucun des 3 clients"),
    ]
    total_qt=0; total_cout=0
    for i,(qk,pk,lbl,mode,prix_ref,tip) in enumerate(ENGINS):
        active = d[qk]>0
        with st.expander(f"{'🟢' if active else '⚫'} {lbl} — {d[qk]:.2f} unités", expanded=active):
            st.caption(f"_{tip}_")
            c1,c2,c3 = st.columns([2,2,1])
            with c1: d[qk] = num("Quantité allouée", d[qk], mn=0.0, mx=50.0, step=0.01, key=f"qt_{qk}_{i}")
            with c2: d[pk] = num_int(f"€/engin/an ({mode})", d[pk], mn=0, mx=500000, step=100, key=f"px_{pk}_{i}")
            with c3: st.metric("Total", f"{d[qk]*d[pk]:,.0f} €")
        total_qt+=d[qk]; total_cout+=d[qk]*d[pk]

    c1,c2,c3 = st.columns(3)
    with c1: st.metric("Parc total", f"{total_qt:.2f} engins")
    with c2: st.metric("Coût/an", f"{total_cout:,.0f} €")
    with c3: st.metric("Coût moyen/engin", f"{total_cout/max(total_qt,1):,.0f} €/an")
    nav(4)

elif step == 5:
    hdr(5,"📊","Volumes & IT","Quantités annuelles par processus — onglet UO.")
    info("OCP : flux pal. symétrique (70 720 in = 70 720 out) · AKZO : multi-process + picking<br>"
         "BASF : volume très faible palettes (1 954 in, 293 out) + <b>75 000 picks/an</b>")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>🏭 Stockage</div>", unsafe_allow_html=True)
        d["empl_vendus"] = num_int("Emplacements vendus", d["empl_vendus"], step=10, key="ev",
                                    help="OCP=4000 · AKZO=2172 · BASF=1588")
        empl_nets = round(d["emplacements_brut"]*d["taux_utilisation"]/100)
        taux_occ = d["empl_vendus"]/max(empl_nets,1)*100
        if taux_occ>100: warn(f"Occupation {taux_occ:.1f}% > capacité ({empl_nets:,})")
        elif taux_occ>85: ok(f"Occupation {taux_occ:.1f}% — optimal")
        else: hint(f"Occupation {taux_occ:.1f}% / {empl_nets:,} nets")

        st.markdown("<div class='sec'>📥 Entrées</div>", unsafe_allow_html=True)
        d["vol_in_pal"]  = num_int("Palettes mises en stock / an", d["vol_in_pal"], step=100, key="vi1",
                                    help="OCP=70 720 · AKZO=4 008 · BASF=1 954")
        d["vol_in_livr"] = num_int("Livraisons camions / an", d["vol_in_livr"], step=1, key="vi2")

        st.markdown("<div class='sec'>🖥️ IT & WMS</div>", unsafe_allow_html=True)
        d["cout_it"] = num_int("Coûts IT fixes / an (€)", d["cout_it"], step=100, key="cit",
                                help="OCP=2182€ · AKZO≈0 · BASF=3100€ (WMS MIKADO partagé)")
        d["alloc_wms"] = num("Allocation WMS+Innovation (%)", d["alloc_wms"], mn=0.0, mx=10.0, step=0.1, key="wms_pct",
                              help="OCP=2.2% · AKZO=1.7% · BASF=2.11%")

    with col2:
        st.markdown("<div class='sec'>📤 Sorties palettes</div>", unsafe_allow_html=True)
        d["vol_out_pal"] = num_int("Palettes complètes expédiées / an", d["vol_out_pal"], step=100, key="vo1",
                                    help="OCP=70 720 · AKZO=2 613 · BASF=293")
        d["vol_out_cmd"] = num_int("Ordres de sortie / an", d["vol_out_cmd"], step=10, key="vo2")

        st.markdown("<div class='sec'>🛒 Picking & colis</div>", unsafe_allow_html=True)
        info("AKZO : 45 131 picks ASC + 9 529 picks MPY = <b>54 660/an</b><br>"
             "BASF : 75 034 picks box + 4 690 colis = <b>79 724/an</b><br>OCP : 0 (pas de picking)")
        d["vol_picks"] = num_int("Picks / an (colis ou articles)", d.get("vol_picks",0), step=100, key="vpicks",
                                  help="OCP=0 · AKZO=54660 · BASF=79724")
        d["vol_colis"]  = num_int("Colis expédiés / an", d.get("vol_colis",0), step=100, key="vcolis",
                                   help="OCP=0 · AKZO=6869 · BASF=4690")

        if d["vol_in_pal"]>0 or d["vol_out_pal"]>0:
            j = max(d["jours_ouvres"],1)
            st.markdown(f"""<div class='kpi-row' style='margin-top:14px'>
              <div class='kpi'><div class='kpi-lbl'>Entrées/jour</div><div class='kpi-val blue'>{d['vol_in_pal']/j:.1f}</div></div>
              <div class='kpi'><div class='kpi-lbl'>Sorties/jour</div><div class='kpi-val blue'>{d['vol_out_pal']/j:.1f}</div></div>
              <div class='kpi'><div class='kpi-lbl'>Picks/jour</div><div class='kpi-val purple'>{d.get("vol_picks",0)/j:.1f}</div></div>
            </div>""", unsafe_allow_html=True)
    nav(5)

elif step == 6:
    hdr(6,"🔀","Design des Processus","Flux logistiques et sous-processus actifs par client.")

    j = max(d["jours_ouvres"],1)
    taux_charge = 0.40

    def etp_proc(vol_j, prod_h, tc=taux_charge):
        if prod_h<=0: return 0
        return (vol_j/prod_h)*(1+tc)/8

    etp_dech  = etp_proc(d["vol_in_pal"]/j, d["prod_dech"])
    etp_stock = etp_proc(d["vol_in_pal"]/j, d["prod_stock"])
    etp_prel  = etp_proc(d["vol_out_pal"]/j, d["prod_prel"])
    etp_charg = etp_proc(d["vol_out_pal"]/j, d["prod_charg"])

    # Processus actifs selon preset
    pk = st.session_state.preset
    if pk in BENCHMARK:
        b = BENCHMARK[pk]
        st.markdown(f"**Client actuel : {b['label']} · {b['secteur']}**")
        proc_actifs = b["processus"]
        proc_inactifs = b["processus_inactifs"]
    else:
        proc_actifs = ["FP Inbound","Storage","FP Outbound"]
        proc_inactifs = []

    c1,c2 = st.columns([2,1])
    with c1:
        st.markdown("<div class='sec'>✅ Processus actifs</div>", unsafe_allow_html=True)
        for p in proc_actifs:
            st.markdown(f"<span style='background:#d1fae5;color:#065f46;padding:4px 12px;border-radius:8px;"
                        f"font-size:12px;font-weight:700;display:inline-block;margin:3px'>{p}</span>",
                        unsafe_allow_html=True)
        if proc_inactifs:
            st.markdown("<div class='sec' style='margin-top:14px'>❌ Non actifs</div>", unsafe_allow_html=True)
            for p in proc_inactifs:
                st.markdown(f"<span style='background:#f3f4f6;color:#9ca3af;padding:4px 12px;border-radius:8px;"
                            f"font-size:12px;display:inline-block;margin:3px'>{p}</span>",
                            unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='sec'>ETP calculés</div>", unsafe_allow_html=True)
        etp_df = pd.DataFrame({
            "Processus":["Décharg.","Mise stock","Prélèv.","Chargmt","TOTAL"],
            "ETP calc.":[f"{etp_dech:.2f}",f"{etp_stock:.2f}",f"{etp_prel:.2f}",f"{etp_charg:.2f}",
                         f"{etp_dech+etp_stock+etp_prel+etp_charg:.2f}"],
        })
        st.dataframe(etp_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🔄 Comparaison processus actifs — 3 clients")
    proc_cmp = pd.DataFrame({
        "Process":["FP Inbound (pal)","Stock-in palettes","Picking colis/art.","Picking parcels",
                   "Réappro (pal)","FP Outbound (pal)","Loading palettes","Loading colis"],
        "Code":["MF1020/1070","MF1070","MF2070","MF2110","MF3010","MF4010","MF5020","MF5040"],
        "OCP":["✅ 70 720","✅ 70 720","❌ 0","❌ 0","❌ 0","✅ 70 720","✅ 70 720","❌ 0"],
        "AKZO":["✅ 2 733","✅ 1 275","✅ 54 660","❌ 0","❌ 0","✅ 2 613","✅ 3 713","✅ 6 869"],
        "BASF":["✅ 1 954","❌ 0","✅ 75 034","✅ 4 690","✅ 1 661","✅ 293","✅ 1 856","✅ 4 690"],
    })
    st.dataframe(proc_cmp, use_container_width=True, hide_index=True)

    st.markdown("### 🗺️ Flux entrepôt (site MA-Mohammedia)")
    st.markdown("""
    <div style='background:white;border:2px solid #c5cdf5;border-radius:14px;padding:18px;font-size:12px'>
      <div style='display:grid;grid-template-columns:1fr 3fr 1fr;gap:10px'>
        <div style='background:#dbeafe;border:2px dashed #3b82f6;border-radius:8px;padding:10px;text-align:center'>
          <b style='color:#1e40af'>📥 RÉCEPTION</b><br>
          <span style='color:#3b82f6'>Quais entrants<br>Contrôle & étiquetage<br>Tampon entrée</span>
        </div>
        <div style='background:#f0fdf4;border:2px solid #22c55e;border-radius:8px;padding:10px;text-align:center'>
          <b style='color:#15803d'>🏭 STOCKAGE WH0010</b><br>
          <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:6px'>
            <div style='background:#bbf7d0;border-radius:4px;padding:3px;font-size:10px'>OCP<br>4 040m²<br>4 211 PPL</div>
            <div style='background:#fce7f3;border-radius:4px;padding:3px;font-size:10px'>AKZO<br>1 600m²<br>2 413 PPL</div>
            <div style='background:#dcfce7;border-radius:4px;padding:3px;font-size:10px'>BASF<br>2 040m²<br>1 764 PPL</div>
          </div>
          <div style='margin-top:6px;font-size:11px;color:#166534'>WMS MIKADO · 10m hauteur · MA-Mohammedia</div>
        </div>
        <div style='background:#fef3c7;border:2px dashed #f59e0b;border-radius:8px;padding:10px;text-align:center'>
          <b style='color:#92400e'>📤 EXPÉDITION</b><br>
          <span style='color:#b45309'>Quais sortants<br>I-Point BL<br>Zone colis (AKZO/BASF)</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    nav(6)

elif step == 7:
    hdr(7,"💶","Calcul des Tarifs","Tarifs recommandés et comparaison avec les 3 clients réels.")
    r = calc(d)
    m_ok = r["marge"] >= d["marge_cible"]
    mc = "green" if m_ok else "red"
    st.markdown(f"""<div class='kpi-row'>
      <div class='kpi'><div class='kpi-lbl'>CA estimé</div><div class='kpi-val blue'>{r['ca']:,.0f} €</div></div>
      <div class='kpi'><div class='kpi-lbl'>Coûts totaux</div><div class='kpi-val orange'>{r['cout_tot']:,.0f} €</div></div>
      <div class='kpi'><div class='kpi-lbl'>Bénéfice</div><div class='kpi-val {"green" if r["profit"]>0 else "red"}'>{r['profit']:,.0f} €</div></div>
      <div class='kpi'><div class='kpi-lbl'>Marge</div><div class='kpi-val {mc}'>{r['marge']:.2f}%</div>
        <div class='kpi-sub'>Obj. {d["marge_cible"]:.1f}%</div></div>
    </div>""", unsafe_allow_html=True)

    if m_ok: ok(f"Marge {r['marge']:.2f}% ≥ objectif {d['marge_cible']:.1f}%")
    else:
        gap = (d["marge_cible"]/100 - r["marge"]/100) * r["ca"]
        warn(f"Marge {r['marge']:.2f}% < objectif — Manque {gap:,.0f} €/an")

    st.markdown("---")
    st.markdown("### 💶 Tarifs recommandés (ajustables)")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown("**🏭 Stockage (€/empl./mois)**")
        px_s = num("Prix stockage", r["prix_stock"], mn=0.0, mx=100.0, step=0.01, key="pxs")
        ca_s = d["empl_vendus"]*px_s*12
        mg_s = (ca_s-r["cout_wh"])/ca_s*100 if ca_s>0 else 0
        st.markdown(f"""<div class='kpi'><div class='kpi-lbl'>CA stockage</div>
          <div class='kpi-val {"green" if mg_s>=0 else "red"}'>{ca_s:,.0f} €</div>
          <div class='kpi-sub'>Marge : {mg_s:.2f}%</div></div>""", unsafe_allow_html=True)
        hint(f"OCP={BENCHMARK['OCP']['tarif_stock_mois']:.2f}€ · AKZO={BENCHMARK['AKZO']['tarif_stock_mois']:.2f}€ · BASF={BENCHMARK['BASF']['tarif_stock_mois']:.2f}€")
    with col2:
        st.markdown("**📥 Entrée (€/palette)**")
        px_i = num("Prix entrée", r["prix_in"], mn=0.0, mx=50.0, step=0.01, key="pxi")
        ca_i = d["vol_in_pal"]*px_i
        mg_i = (ca_i-r["proc_in"])/ca_i*100 if ca_i>0 else 0
        st.markdown(f"""<div class='kpi'><div class='kpi-lbl'>CA entrées</div>
          <div class='kpi-val {"green" if mg_i>=0 else "red"}'>{ca_i:,.0f} €</div>
          <div class='kpi-sub'>Marge : {mg_i:.2f}%</div></div>""", unsafe_allow_html=True)
        hint(f"OCP={BENCHMARK['OCP']['tarif_in']:.3f}€ · AKZO={BENCHMARK['AKZO']['tarif_in']:.3f}€ · BASF={BENCHMARK['BASF']['tarif_in']:.3f}€")
    with col3:
        st.markdown("**📤 Sortie (€/palette)**")
        px_o = num("Prix sortie", r["prix_out"], mn=0.0, mx=50.0, step=0.01, key="pxo")
        ca_o = d["vol_out_pal"]*px_o
        mg_o = (ca_o-r["proc_out"])/ca_o*100 if ca_o>0 else 0
        st.markdown(f"""<div class='kpi'><div class='kpi-lbl'>CA sorties</div>
          <div class='kpi-val {"green" if mg_o>=0 else "red"}'>{ca_o:,.0f} €</div>
          <div class='kpi-sub'>Marge : {mg_o:.2f}%</div></div>""", unsafe_allow_html=True)
        hint(f"OCP={BENCHMARK['OCP']['tarif_out']:.3f}€ · AKZO={BENCHMARK['AKZO']['tarif_out']:.3f}€ · BASF={BENCHMARK['BASF']['tarif_out']:.3f}€")

    st.markdown("---")
    st.markdown("### 🧩 Décomposition des coûts")
    cost_df = pd.DataFrame({
        "Poste":["🏭 Loyer chargé","🔧 Investissements","👷 Personnel op.","📋 Personnel adm.","🏗️ Engins","🖥️ IT","TOTAL"],
        "€/an":[f"{r['loyer_tot']:,.0f}",f"{r['rack_an']+r['secu_an']+r['cable_an']:,.0f}",
                f"{r['pers_op']:,.0f}",f"{r['pers_adm']:,.0f}",f"{r['engins_cout']:,.0f}",
                f"{r['it_tot']:,.0f}",f"{r['cout_tot']:,.0f}"],
        "Part":[f"{r['loyer_tot']/max(r['cout_tot'],1)*100:.1f}%",
                f"{(r['rack_an']+r['secu_an']+r['cable_an'])/max(r['cout_tot'],1)*100:.1f}%",
                f"{r['pers_op']/max(r['cout_tot'],1)*100:.1f}%",
                f"{r['pers_adm']/max(r['cout_tot'],1)*100:.1f}%",
                f"{r['engins_cout']/max(r['cout_tot'],1)*100:.1f}%",
                f"{r['it_tot']/max(r['cout_tot'],1)*100:.1f}%","100%"],
        "OCP réel":["284 648€","74 030€","~112 k€","~36 k€","56 074€","11 243€","643 523€"],
        "AKZO réel":["~99 k€","24 k€","23 810€","32 096€","21 730€","~5 k€","279 247€"],
        "BASF réel":["~161 k€","30 k€","5 454€","28 635€","10 913€","3 100€","289 708€"],
    })
    st.dataframe(cost_df, use_container_width=True, hide_index=True)

    export = {"Projet":d.get("projet",""), "CA":round(r["ca"],2), "Couts":round(r["cout_tot"],2),
              "Profit":round(r["profit"],2), "Marge_pct":round(r["marge"],2),
              "Prix_stock":round(r["prix_stock"],4),"Prix_in":round(r["prix_in"],4),"Prix_out":round(r["prix_out"],4)}
    st.download_button("⬇️ Export JSON", json.dumps(export,indent=2,ensure_ascii=False),
                        f"polka_{d.get('projet','projet')}.json","application/json",type="primary")
    nav(7)

elif step == 8:
    hdr(8,"📉","Analyse de Sensibilité","Impact des variations · Seuil de rentabilité · Scénarios.")
    r = calc(d)

    st.markdown("### 📊 Tableau de sensibilité ±20%")
    rows=[]
    for v in [-20,-15,-10,-5,0,5,10,15,20]:
        f=1+v/100
        dv=deepcopy(d); dv["vol_in_pal"]=int(d["vol_in_pal"]*f); dv["vol_out_pal"]=int(d["vol_out_pal"]*f)
        rv=calc(dv)
        dl=deepcopy(d); dl["loyer_m2_mois"]=d["loyer_m2_mois"]*f; rl=calc(dl)
        ds=deepcopy(d); ds["sal_op"]=int(d["sal_op"]*f); ds["sal_adm"]=int(d["sal_adm"]*f); rs=calc(ds)
        rows.append({"Var":f"{v:+d}%",
                     "Marge/vol":f"{rv['marge']:.2f}%","Profit vol":f"{rv['profit']:,.0f}€",
                     "Marge/loyer":f"{rl['marge']:.2f}%","Profit loyer":f"{rl['profit']:,.0f}€",
                     "Marge/sal":f"{rs['marge']:.2f}%","Profit sal":f"{rs['profit']:,.0f}€"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🎛️ Simulateur")
    c1,c2,c3,c4 = st.columns(4)
    with c1: sv=st.slider("📦 Volumes (%)",-50,50,0,5,key="sl_v")
    with c2: sl=st.slider("🏭 Loyer (%)",-50,100,0,5,key="sl_l")
    with c3: ss=st.slider("👷 Salaires (%)",-30,50,0,5,key="sl_s")
    with c4: sm=st.slider("🎯 Marge cible (%)",0,25,int(d["marge_cible"]),1,key="sl_m")
    dsim=deepcopy(d)
    dsim["vol_in_pal"]=int(d["vol_in_pal"]*(1+sv/100))
    dsim["vol_out_pal"]=int(d["vol_out_pal"]*(1+sv/100))
    dsim["loyer_m2_mois"]=d["loyer_m2_mois"]*(1+sl/100)
    dsim["sal_op"]=int(d["sal_op"]*(1+ss/100)); dsim["sal_adm"]=int(d["sal_adm"]*(1+ss/100))
    dsim["marge_cible"]=float(sm); rsim=calc(dsim)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("CA simulé",f"{rsim['ca']:,.0f}€",f"{rsim['ca']-r['ca']:+,.0f}€")
    with c2: st.metric("Coûts simulés",f"{rsim['cout_tot']:,.0f}€",f"{rsim['cout_tot']-r['cout_tot']:+,.0f}€",delta_color="inverse")
    with c3: st.metric("Bénéfice simulé",f"{rsim['profit']:,.0f}€",f"{rsim['profit']-r['profit']:+,.0f}€")
    with c4: st.metric("Marge simulée",f"{rsim['marge']:.2f}%",f"{rsim['marge']-r['marge']:+.2f}%")

    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("Seuil rentabilité",f"{r['seuil']:,.0f}€")
    with c2: st.metric("CA actuel",f"{r['ca']:,.0f}€")
    with c3:
        cushion=(r["ca"]-r["seuil"])/max(r["ca"],1)*100
        st.metric("Marge sécurité",f"{cushion:.1f}%",
                  delta="✅ Solide" if cushion>20 else ("⚠️" if cushion>5 else "🔴 Fragile"))
    nav(8)

# ═══════════════════════════════════════════════════
# ÉTAPE 9 — BENCHMARK COMPLET
# ═══════════════════════════════════════════════════
elif step == 9:
    hdr(9,"📋","Benchmark 3 Clients","Comparaison exhaustive OCP · AKZO Nobel · BASF Agriculture — Polka Dachser Maroc.")

    r_calc = calc(d)
    pk = st.session_state.preset

    # ── Tableau synthèse général ──────────────────
    st.markdown("### 🏆 Synthèse financière")
    bm_badges()

    fin_df = pd.DataFrame({
        "Indicateur":["CA total (€)","Coûts totaux (€)","Bénéfice (€)","Marge réelle (%)","Marge cible (%)","Écart marge"],
        "OCP 2026":[f"{BENCHMARK['OCP']['ca']:,}",f"{BENCHMARK['OCP']['couts']:,}",
                    f"{BENCHMARK['OCP']['profit']:,}",f"{BENCHMARK['OCP']['marge_pct']:.2f}%","10.0%","-1.39%"],
        "AKZO 2021":[f"{BENCHMARK['AKZO']['ca']:,}",f"{BENCHMARK['AKZO']['couts']:,}",
                     f"{BENCHMARK['AKZO']['profit']:,}",f"{BENCHMARK['AKZO']['marge_pct']:.2f}%","20.0%","-4.41%"],
        "BASF 2024":[f"{BENCHMARK['BASF']['ca']:,}",f"{BENCHMARK['BASF']['couts']:,}",
                     f"{BENCHMARK['BASF']['profit']:,}",f"{BENCHMARK['BASF']['marge_pct']:.2f}%","8.0%","0.0%"],
        "Votre projet":[f"{r_calc['ca']:,.0f}",f"{r_calc['cout_tot']:,.0f}",
                        f"{r_calc['profit']:,.0f}",f"{r_calc['marge']:.2f}%",f"{d['marge_cible']:.1f}%",
                        f"{r_calc['marge']-d['marge_cible']:+.2f}%"],
    })
    st.dataframe(fin_df, use_container_width=True, hide_index=True)

    # ── Entrepôt ──────────────────────────────────
    st.markdown("### 🏭 Benchmark Entrepôt")
    wh_df = pd.DataFrame({
        "Paramètre":["Surface (m²)","Hauteur (m)","Emplacements bruts","Emplacements nets","Taux utilisation",
                     "Loyer €/m²/mois","Coût WH total/an","€/m²/mois total","Rack/PPL (€)","Durée amort rack"],
        "OCP":["4 040","10","4 211","4 000","95%","5.22€","358 678€","7.40€/m²","30€","12 ans"],
        "AKZO":["1 600","10","2 413","2 172","90%","5.18€","123 827€","6.45€/m²","35€","12 ans"],
        "BASF":["2 040","10","1 764","1 588","90%","6.59€","191 243€","7.81€/m²","43€","12 ans"],
        "Insight":["OCP = plus grand site","Même hauteur 3 clients","OCP densité = 1.04/m²","BASF = plus faible densité",
                   "90-95% standard Maroc","Loyer BASF +26% vs OCP","Coût/m²: BASF>OCP>AKZO",
                   "Coût WH/m²/mois","Prix rack inversé à taille","Amort. identique"],
    })
    st.dataframe(wh_df, use_container_width=True, hide_index=True)

    # ── Personnel ─────────────────────────────────
    st.markdown("### 👷 Benchmark Personnel")
    pers_df = pd.DataFrame({
        "Rôle":["Cariste (Forklift)","Chargeur (Loader)","Déchargeur","Picker/Préparateur","Contrôleur",
                "Admin Réception","Admin Expédition","Team Leader","Ops Manager","Stock Manager",
                "TOTAL ETP opérat.","TOTAL ETP admin","ETP TOTAL","Coût total personnel","Coût/ETP moyen"],
        "OCP":["3.30","1.57","0.85","0","0.50","1.00","0","0","0","0",
               "6.22","1.00","7.22","148 419€","~20 556€"],
        "AKZO":["1.00","1.00","0","1.00","0","0","0","1.00","0.15","0.50",
                "3.00","1.85","4.85","55 906€","~11 526€"],
        "BASF":["1.00","0.40","0.20","0.40","0","0.25","0.25","0","0","0",
                "2.00","0.50","2.50","34 089€","~13 636€"],
        "Sal. op. brut":["13 829€/an","13 829€/an","13 829€/an","—","13 829€/an",
                         "—","—","—","—","—","—","—","—","—","—"],
    })
    st.dataframe(pers_df, use_container_width=True, hide_index=True)

    # ── Engins ────────────────────────────────────
    st.markdown("### 🏗️ Benchmark Engins")
    eng_df = pd.DataFrame({
        "Engin":["Fast Mover (FZ0040)","Reach Truck >8m (FZ0085)","Reach Truck ≤8m (FZ0080)",
                 "H. Order Picker (FZ0050)","Front Loader (FZ0070)","Hand Pallet (FZ0010)",
                 "TOTAL qt. engins","TOTAL coût engins/an"],
        "Prix catalogue":[" 10 606€/an","44 619€/an","31 089€/an","11 956€/an","22 644€/an","375€ achat","—","—"],
        "OCP":["2.79","3.42","0","0","0","0","6.21","56 074€"],
        "AKZO":["1.00","1.00","0","1.00","0","0","3.00","21 730€"],
        "BASF":["0","0.50*","0","0","0.50*","1.00","2.00","10 913€"],
        "Note":["—","—","—","—","BASF=8 866€ (configuré)","—","—","*BASF prix négocié différent"],
    })
    st.dataframe(eng_df, use_container_width=True, hide_index=True)

    # ── Volumes & Tarifs ──────────────────────────
    st.markdown("### 📊 Volumes annuels & Tarifs comparés")
    vol_df = pd.DataFrame({
        "Métrique":["Empl. vendus","Vol. entrée palettes","Vol. sortie palettes","Picks/an","Colis/an",
                    "Tarif stockage (€/empl./mois)","Tarif entrée (€/pal)","Tarif sortie (€/pal)",
                    "Tarif forfait fixe (€/mois)","CA/m² (€/an)","CA/empl. vendu (€/an)"],
        "OCP":["4 000","70 720","70 720","0","0",
               "6.58€","2.562€","2.929€","0€",f"{BENCHMARK['OCP']['ca']/4040:.0f}€",
               f"{BENCHMARK['OCP']['ca']/4000:.0f}€"],
        "AKZO":["2 172","4 008","2 613","54 660","6 869",
                "7.644€","2.238€","1.783€","6 222.66€",f"{BENCHMARK['AKZO']['ca']/1600:.0f}€",
                f"{BENCHMARK['AKZO']['ca']/2172:.0f}€"],
        "BASF":["1 588","1 954","293","79 724","4 690",
                "12.293€","0.639€","0.448€","4 617.28€",f"{BENCHMARK['BASF']['ca']/2040:.0f}€",
                f"{BENCHMARK['BASF']['ca']/1588:.0f}€"],
        "Insight":["OCP = plein régime","OCP = gros volume","OCP = flux symétrique","Picking = BASF dominant",
                   "—","BASF 2× OCP (volumes faibles)","OCP > AKZO > BASF (volumes)","Idem",
                   "BASF/AKZO ont un forfait","OCP 174€ · AKZO 207€ · BASF 154€","Revenu par emplacement"],
    })
    st.dataframe(vol_df, use_container_width=True, hide_index=True)

    # ── Productivités ─────────────────────────────
    st.markdown("### ⚡ Productivités comparées (pal/h productif)")
    prod_df = pd.DataFrame({
        "Processus":["Déchargement camion","Mise en stock palette","Prélèvement palette","Chargement camion"],
        "OCP (2026)":[37.63,34.02,27.69,32.19],
        "AKZO (2021)":[32.31,26.38,20.72,21.69],
        "BASF (2024)":[28.48,24.76,"n/a (picking box)",12.87],
        "Tendance":["OCP+16% vs BASF","OCP+37% vs BASF","OCP > tous","OCP+150% vs BASF"],
    })
    st.dataframe(prod_df, use_container_width=True, hide_index=True)
    hint("OCP a les meilleures productivités — effet volume (flux élevé = apprentissage et optimisation des allées).<br>"
         "BASF : activité principalement <b>picking box</b> (188,77 colis/h) non comparée ici.")

    # ── Paramètres globaux ────────────────────────
    st.markdown("### ⚙️ Paramètres Polka comparés")
    param_df = pd.DataFrame({
        "Paramètre":["Jours ouvrés/an","Taux d'intérêt interne","Marge cible","Alloc. WMS+Innovation",
                     "Taux fluctuation","Taux déduction réserve","Batteries LI","WMS","Taux change MAD/€"],
        "OCP":["272 j","9%","10%","2.20%","0%","10%","Oui","MIKADO","10.84"],
        "AKZO":["272 j","9%","20%","1.70%","0%","10%","Oui","MIKADO","10.60"],
        "BASF":["272 j","9%","8%","2.11%","14.57%","10%","Non","MIKADO","10.49"],
        "Note":["Identique","Identique","Objectif différent","Quasi-identique",
                "BASF intègre turn-over","Identique","Impacte parc engins","Identique","Évolution MAD stable"],
    })
    st.dataframe(param_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 💡 Enseignements clés du benchmark")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("""
**📦 Structure des coûts (part du CA)**
| Poste | OCP | AKZO | BASF |
|-------|-----|------|------|
| Entrepôt | 51% | 37% | 61% |
| Personnel | 21% | 17% | 11% |
| Engins | 8% | 7% | 3% |
| IT | 2% | 2% | 1% |
| **Marge** | **9%** | **16%** | **8%** |
""")
    with col2:
        st.markdown("""
**🎯 Facteurs clés de succès identifiés**

- **Volume = levier principal** : OCP (141K pal/an) a les meilleurs coûts unitaires et productivités. BASF (2 247 pal/an) est 5× plus cher/pal
- **Tarif stockage inverse au volume** : BASF facture 12.29€/empl./mois vs 6.58€ OCP — logique car coûts fixes élevés ramenés sur peu d'emplacements
- **Forfait fixe = stabilité** : AKZO et BASF ont un forfait mensuel (~4-6K€) — protège la marge en cas de baisse d'activité
- **Picking enrichit le CA** : BASF tire 90% de son CA du picking/stockage sur 2 040m² contre 100% palettes pour OCP
- **AKZO = seul client rentable à l'objectif** : 15.6% réel vs 20% cible — écart gérable
        """)
    nav(9)

st.markdown("""<div style='text-align:center;padding:12px 0 4px;color:#9ca3af;font-size:11px;
 border-top:1px solid #e5e7eb;margin-top:18px'>
  Polka Wizard v4 · Benchmark OCP · AKZO Nobel · BASF Agriculture · Dachser CL Maroc
</div>""", unsafe_allow_html=True)
