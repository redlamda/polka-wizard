"""
POLKA WIZARD v3 — Tarification Contract Logistics
Basé sur Polka V202541 · OCP Morocco · Dachser CL
Lancement : streamlit run polka_wizard.py
"""

import streamlit as st
import pandas as pd
from copy import deepcopy
import json

st.set_page_config(
    page_title="Polka Wizard — Tarification",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── THÈME CLAIR & LISIBLE ────────────────────────────────
st.markdown("""
<style>
/* Corps principal */
.stApp { background: #f0f2f8; color: #1a1d2e; font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1rem; max-width: 1280px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1e2240;
    color: #e8eaf6;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label { color: #c5cae9 !important; }
[data-testid="stSidebar"] p { color: #9fa8da; }

/* Titres étape */
.step-hdr {
    background: linear-gradient(135deg, #1e2240, #2a3060);
    border-left: 5px solid #5c7cff;
    border-radius: 0 14px 14px 0;
    padding: 16px 22px;
    margin-bottom: 22px;
    color: white;
}
.step-num  { font-size: 11px; color: #8899ff; text-transform: uppercase; letter-spacing: 1px; }
.step-ttl  { font-size: 22px; font-weight: 800; margin: 4px 0; }
.step-dsc  { font-size: 13px; color: #aab4d8; }

/* Boîte d'aide */
.help-box {
    background: #e8edff;
    border-left: 4px solid #5c7cff;
    border-radius: 0 10px 10px 0;
    padding: 11px 15px;
    font-size: 12.5px;
    color: #2a3060;
    margin: 6px 0 14px 0;
    line-height: 1.65;
}

/* Cartes résultat */
.kpi-row { display: flex; gap: 14px; flex-wrap: wrap; margin: 14px 0; }
.kpi { background: white; border: 1px solid #dce3f5; border-radius: 12px;
       padding: 16px 20px; flex: 1; min-width: 160px; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
.kpi-lbl { font-size: 11px; color: #6b7bad; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 5px; }
.kpi-val { font-size: 22px; font-weight: 800; }
.kpi-sub { font-size: 11px; color: #8892b0; margin-top: 3px; }
.green  { color: #0d9e6e; }
.red    { color: #d63c4a; }
.blue   { color: #2952d9; }
.orange { color: #d97706; }

/* Alertes */
.alert-ok   { background: #d1fae5; border: 1px solid #6ee7b7; border-radius: 8px;
               padding: 10px 14px; font-size: 13px; color: #065f46; margin: 8px 0; }
.alert-warn { background: #fff3cd; border: 1px solid #fcd34d; border-radius: 8px;
               padding: 10px 14px; font-size: 13px; color: #92400e; margin: 8px 0; }
.alert-info { background: #dbeafe; border: 1px solid #93c5fd; border-radius: 8px;
               padding: 10px 14px; font-size: 13px; color: #1e40af; margin: 8px 0; }

/* Section */
.sec { font-size: 14px; font-weight: 700; color: #2a3060;
       border-bottom: 2px solid #c5cdf5; padding-bottom: 5px; margin: 20px 0 10px 0; }

/* Process flow */
.proc-box {
    background: white; border: 2px solid #c5cdf5;
    border-radius: 12px; padding: 14px 16px; margin: 6px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.proc-title { font-weight: 700; color: #1e2240; font-size: 14px; margin-bottom: 6px; }
.proc-step  { background: #f0f4ff; border-radius: 6px; padding: 5px 10px;
               font-size: 12px; color: #2a3060; margin: 3px 0; display: inline-block; }
.proc-arrow { color: #5c7cff; font-size: 18px; margin: 0 6px; }
.badge-active   { background: #d1fae5; color: #065f46; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 700; }
.badge-inactive { background: #f3f4f6; color: #9ca3af; padding: 2px 8px; border-radius: 10px; font-size: 11px; }

/* Inputs lisibles */
.stNumberInput > label { color: #2a3060 !important; font-weight: 600; }
.stTextInput > label   { color: #2a3060 !important; font-weight: 600; }
.stSlider > label      { color: #2a3060 !important; font-weight: 600; }
.stCheckbox > label    { color: #2a3060 !important; font-weight: 600; }
.stSelectbox > label   { color: #2a3060 !important; font-weight: 600; }

/* Tableau */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Boutons navigation */
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #2952d9, #5c7cff) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ── DONNÉES OCP ──────────────────────────────────────────
OCP = {
    # Projet
    "projet": "OCP", "chef_projet": "Reda Lamdarhri Kachani",
    "agence": "MA-Mohammedia (580)", "pays": "Maroc", "wms": "MIKADO",
    # Params globaux
    "jours_ouvres": 272, "taux_interet": 9.0, "marge_cible": 10.0,
    "reserve_op": 10.0, "taux_panne": 5.0, "alloc_wms": 2.2,
    "batteries_li": True, "prime_fret": 15.0, "prime_colis": 5.0,
    "taux_change_mad": 10.84,
    # Entrepôt
    "surface_m2": 4039.74, "hauteur_m": 10.0, "emplacements_brut": 4211,
    "taux_utilisation": 95.0,
    "loyer_m2_mois": 5.22, "taxe_communale": 10.5, "charge_locative": 2.0,
    "cout_rack_ppl": 30.0, "amort_rack": 12,
    "cout_secu_m2": 12.0, "amort_secu": 10,
    "cout_cable_m2": 10.5, "amort_cable": 5,
    # Personnel ETP
    "fte_cariste": 3.30, "fte_chargeur": 1.57, "fte_dechargeur": 0.85,
    "fte_ctrl": 0.50, "fte_picker": 0.0, "fte_coord": 0.0, "fte_chef": 0.0,
    "fte_admin_in": 1.0, "fte_admin_out": 0.0, "fte_svc_client": 0.0, "fte_resp": 0.0,
    "sal_op": 13829, "sal_adm": 18628,
    # Engins
    "qt_fm": 2.79, "prix_fm": 10606,
    "qt_rt8": 3.42, "prix_rt8": 44619,
    "qt_rt8m": 0.0, "prix_rt8m": 31089,
    "qt_tp": 0.0,  "prix_tp": 375,
    "qt_cf": 0.0,  "prix_cf": 22644,
    "qt_ph": 0.0,  "prix_ph": 11956,
    "qt_ae": 0.0,  "prix_ae": 95000,
    "qt_bal": 0.0, "prix_bal": 24990,
    # Volumes
    "empl_vendus": 4000,
    "vol_in_pal": 70720, "vol_out_pal": 70720,
    "vol_in_livr": 0, "vol_out_cmd": 0,
    "vol_charg_cam": 0, "vol_charg_pal": 0,
    "cout_it": 2182,
    # Productivités (pal/h productif)
    "prod_dech": 37.63, "prod_stock": 34.02,
    "prod_prel": 27.69, "prod_charg": 32.19,
    # Tarifs réels OCP
    "tarif_stock_mois": 6.58, "tarif_in": 2.562, "tarif_out": 2.929,
    "ca_reel": 704163.52, "cout_reel": 643522.45,
    "profit_reel": 60641.07, "marge_reelle": 8.61,
}

VIERGE = deepcopy(OCP)
for k in ["projet","chef_projet","agence","pays","wms"]: VIERGE[k] = ""
for k in ["surface_m2","emplacements_brut","loyer_m2_mois","vol_in_pal","vol_out_pal","empl_vendus"]: VIERGE[k] = 0.0
for k in ["fte_cariste","fte_chargeur","fte_dechargeur","fte_ctrl","fte_picker",
          "fte_coord","fte_chef","fte_admin_in","fte_admin_out","fte_svc_client","fte_resp"]: VIERGE[k] = 0.0
for k in ["qt_fm","qt_rt8","qt_rt8m","qt_tp","qt_cf","qt_ph","qt_ae","qt_bal"]: VIERGE[k] = 0.0
VIERGE["cout_it"] = 0

def init():
    if "d"      not in st.session_state: st.session_state.d = deepcopy(OCP)
    if "step"   not in st.session_state: st.session_state.step = 1
    if "preset" not in st.session_state: st.session_state.preset = "ocp"

init()
d = st.session_state.d

# ── CALCUL ───────────────────────────────────────────────
def calc(d):
    r = {}
    # Entrepôt
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

    # Personnel
    TC = 0.333
    pers_op  = (d["fte_cariste"] + d["fte_chargeur"] + d["fte_dechargeur"] +
                d["fte_ctrl"] + d["fte_picker"]) * d["sal_op"] * (1+TC)
    pers_adm = (d["fte_admin_in"] + d["fte_admin_out"] + d["fte_svc_client"] +
                d["fte_coord"] + d["fte_chef"] + d["fte_resp"]) * d["sal_adm"] * (1+TC)
    pers_tot = pers_op + pers_adm
    fte_op   = d["fte_cariste"]+d["fte_chargeur"]+d["fte_dechargeur"]+d["fte_ctrl"]+d["fte_picker"]
    fte_adm  = d["fte_admin_in"]+d["fte_admin_out"]+d["fte_svc_client"]+d["fte_coord"]+d["fte_chef"]+d["fte_resp"]
    r.update({"pers_op": pers_op, "pers_adm": pers_adm, "pers_tot": pers_tot,
               "fte_op": fte_op, "fte_adm": fte_adm, "fte_tot": fte_op+fte_adm})

    # Engins
    engins_cout = (d["qt_fm"]*d["prix_fm"] + d["qt_rt8"]*d["prix_rt8"] +
                   d["qt_rt8m"]*d["prix_rt8m"] + d["qt_tp"]*d["prix_tp"] +
                   d["qt_cf"]*d["prix_cf"] + d["qt_ph"]*d["prix_ph"] +
                   d["qt_ae"]*d["prix_ae"] + d["qt_bal"]*d["prix_bal"])
    r["engins_cout"] = engins_cout
    r["engins_qt"]   = d["qt_fm"]+d["qt_rt8"]+d["qt_rt8m"]+d["qt_tp"]+d["qt_cf"]+d["qt_ph"]+d["qt_ae"]+d["qt_bal"]

    # IT
    wms_alloc = (pers_op + engins_cout) * d["alloc_wms"]/100
    it_tot    = d["cout_it"] + wms_alloc
    r.update({"wms_alloc": wms_alloc, "it_tot": it_tot})

    # Total coûts
    cout_tot = cout_wh + pers_tot + engins_cout + it_tot
    r["cout_tot"] = cout_tot

    # Coûts unitaires
    v_in  = max(d["vol_in_pal"], 1)
    v_out = max(d["vol_out_pal"], 1)
    v_tot = v_in + v_out
    proc_in  = (pers_op + engins_cout) * v_in  / v_tot
    proc_out = (pers_op + engins_cout) * v_out / v_tot
    cu_in    = proc_in  / v_in
    cu_out   = proc_out / v_out
    cu_stock = cout_wh / 12 / max(d["empl_vendus"], 1)
    r.update({"proc_in": proc_in, "proc_out": proc_out,
               "cu_in": cu_in, "cu_out": cu_out, "cu_stock": cu_stock})

    # Tarifs recommandés
    m = d["marge_cible"] / 100
    r["prix_stock"]  = cu_stock / (1-m) if m < 1 else 0
    r["prix_in"]     = cu_in    / (1-m) if m < 1 else 0
    r["prix_out"]    = cu_out   / (1-m) if m < 1 else 0
    r["prix_stock_an"] = r["prix_stock"] * 12

    # CA & résultat
    ca_s = d["empl_vendus"] * r["prix_stock"] * 12
    ca_i = d["vol_in_pal"]  * r["prix_in"]
    ca_o = d["vol_out_pal"] * r["prix_out"]
    ca   = ca_s + ca_i + ca_o
    profit = ca - cout_tot
    r.update({"ca_s": ca_s, "ca_i": ca_i, "ca_o": ca_o,
               "ca": ca, "profit": profit,
               "marge": profit/ca*100 if ca > 0 else 0})

    # Seuil
    couts_fixes = cout_wh + pers_adm + it_tot
    tmv = (ca_i+ca_o - pers_op - engins_cout) / (ca_i+ca_o) if (ca_i+ca_o) > 0 else 0
    r["seuil"] = couts_fixes / tmv if tmv > 0 else 0
    return r

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 10px;'>
      <div style='font-size:32px;'>📦</div>
      <div style='font-size:16px;font-weight:800;color:#e8eaf6;'>Polka Wizard v3</div>
      <div style='font-size:11px;color:#7986cb;'>Contract Logistics · Dachser</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    preset = st.radio("🗂️ Jeu de données",
                      ["OCP Morocco (réel)", "Nouveau projet (vierge)"],
                      key="preset_radio")
    if preset == "OCP Morocco (réel)" and st.session_state.preset != "ocp":
        st.session_state.d = deepcopy(OCP); st.session_state.preset = "ocp"; st.rerun()
    elif preset == "Nouveau projet (vierge)" and st.session_state.preset != "vierge":
        st.session_state.d = deepcopy(VIERGE); st.session_state.preset = "vierge"; st.rerun()

    st.divider()
    STEPS = [(1,"🏭","Projet & Entrepôt"),(2,"⚙️","Paramètres"),
             (3,"👷","Personnel"),(4,"🏗️","Engins"),
             (5,"📊","Volumes"),(6,"🔀","Processus"),
             (7,"💶","Tarifs"),(8,"📉","Sensibilité")]
    for num, icon, label in STEPS:
        active = st.session_state.step == num
        bg  = "#2952d9" if active else "transparent"
        col = "white"  if active else "#9fa8da"
        fw  = "700"    if active else "400"
        st.markdown(f"""<div style='padding:8px 12px;border-radius:8px;background:{bg};margin:2px 0;'>
            <span style='color:{col};font-weight:{fw};font-size:13px;'>{icon} {label}</span></div>""",
            unsafe_allow_html=True)
        if st.button(f"{icon} {label}", key=f"nav_{num}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.step = num; st.rerun()

    st.divider()
    try:
        r = calc(st.session_state.d)
        mc = "#4ade80" if r["marge"] >= d["marge_cible"] else "#f87171"
        st.markdown(f"""<div style='font-size:12px;color:#c5cae9;'>
          <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2a3060;'>
            <span>CA estimé</span><span style='color:#818cf8;font-weight:700;'>{r['ca']:,.0f} €</span></div>
          <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2a3060;'>
            <span>Coûts</span><span style='color:#fbbf24;font-weight:700;'>{r['cout_tot']:,.0f} €</span></div>
          <div style='display:flex;justify-content:space-between;padding:4px 0;'>
            <span>Marge</span><span style='color:{mc};font-weight:700;'>{r['marge']:.2f}%</span></div>
        </div>""", unsafe_allow_html=True)
    except: pass

# ── HELPERS ──────────────────────────────────────────────
def hdr(num, icon, title, desc):
    st.markdown(f"""<div class='step-hdr'>
      <div class='step-num'>ÉTAPE {num} / 8</div>
      <div class='step-ttl'>{icon} {title}</div>
      <div class='step-dsc'>{desc}</div></div>""", unsafe_allow_html=True)

def info(txt):
    st.markdown(f"<div class='help-box'>ℹ️ {txt}</div>", unsafe_allow_html=True)

def ok(txt):   st.markdown(f"<div class='alert-ok'>✅ {txt}</div>",   unsafe_allow_html=True)
def warn(txt): st.markdown(f"<div class='alert-warn'>⚠️ {txt}</div>", unsafe_allow_html=True)
def hint(txt): st.markdown(f"<div class='alert-info'>💡 {txt}</div>", unsafe_allow_html=True)

def nav(step):
    c1, _, c3 = st.columns([1,5,1])
    with c1:
        if step > 1 and st.button("← Retour", use_container_width=True, key=f"back_{step}"):
            st.session_state.step = step-1; st.rerun()
    with c3:
        lbl = "Suivant →" if step < 8 else "🔄 Début"
        if st.button(lbl, type="primary", use_container_width=True, key=f"next_{step}"):
            st.session_state.step = (step+1) if step < 8 else 1; st.rerun()

def num(label, val, mn=0.0, mx=999999.0, step=1.0, key=None, help=None, fmt="%.2f"):
    """Wrapper number_input sans format spécial pour éviter bug sprintf"""
    return st.number_input(label, min_value=float(mn), max_value=float(mx),
                           value=float(val), step=float(step), key=key, help=help)

def num_int(label, val, mn=0, mx=999999, step=1, key=None, help=None):
    return st.number_input(label, min_value=int(mn), max_value=int(mx),
                           value=int(val), step=int(step), key=key, help=help)

# ════════════════════════════════════════════════════════
# ÉTAPE 1 — PROJET & ENTREPÔT
# ════════════════════════════════════════════════════════
if st.session_state.step == 1:
    hdr(1,"🏭","Projet & Entrepôt","Informations du contrat et caractéristiques physiques du site.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>🏢 Identification du projet</div>", unsafe_allow_html=True)
        info("Onglet <strong>Branch's Basic Data</strong> · Ces champs identifient le client et le site Dachser.")
        d["projet"]      = st.text_input("Client / Projet", value=d["projet"])
        d["chef_projet"] = st.text_input("Chef de projet", value=d["chef_projet"])
        d["agence"]      = st.text_input("Agence Dachser", value=d["agence"], help="Ex: MA-Mohammedia (580)")
        d["pays"]        = st.text_input("Pays", value=d["pays"])
        d["wms"]         = st.text_input("WMS utilisé", value=d["wms"], help="OCP = MIKADO")

        st.markdown("<div class='sec'>📐 Dimensions</div>", unsafe_allow_html=True)
        info("Onglet <strong>Key figures / Warehouse</strong> · OCP WH0010 : 4 040 m² · 10 m · 4 211 emplacements · 95% utilisation → 4 000 nets")
        d["surface_m2"]        = num("Surface nette (m²)", d["surface_m2"], step=50.0, key="s_m2", help="Hors bureaux · OCP = 4 039,74 m²")
        d["hauteur_m"]         = num("Hauteur utile (m)", d["hauteur_m"], mn=3.0, mx=30.0, step=0.5, key="haut", help="Hauteur libre sous poutre · OCP = 10 m")
        d["emplacements_brut"] = num_int("Emplacements palettes (brut)", d["emplacements_brut"], step=10, key="empl_b", help="OCP = 4 211 emplacements")
        d["taux_utilisation"]  = num("Taux d'utilisation (%)", d["taux_utilisation"], mn=50.0, mx=100.0, step=1.0, key="taux_u", help="OCP = 95% → 4 000 empl. nets")

        empl_nets = round(d["emplacements_brut"] * d["taux_utilisation"] / 100)
        vol = d["surface_m2"] * d["hauteur_m"]
        densite = d["emplacements_brut"] / max(d["surface_m2"], 1)
        st.markdown(f"""<div class='kpi-row'>
          <div class='kpi'><div class='kpi-lbl'>Emplacements nets</div><div class='kpi-val blue'>{empl_nets:,}</div></div>
          <div class='kpi'><div class='kpi-lbl'>Volume m³</div><div class='kpi-val blue'>{vol:,.0f}</div></div>
          <div class='kpi'><div class='kpi-lbl'>Densité</div><div class='kpi-val blue'>{densite:.2f} pal/m²</div></div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='sec'>💰 Loyer & charges</div>", unsafe_allow_html=True)
        info("""Onglet <strong>Warehouse Costs</strong> · OCP Maroc : loyer = 56,58 MAD/m²/mois (÷ 10,84 = 5,22 €).
        Taxes spécifiques Maroc : taxe communale 10,5% + charges locatives 2%.""")
        d["loyer_m2_mois"]   = num("Loyer (€/m²/mois)", d["loyer_m2_mois"], step=0.1, key="loy", help="OCP = 5,22 €/m²/mois")
        d["taux_change_mad"] = num("Taux de change MAD/€", d["taux_change_mad"], mn=1.0, mx=30.0, step=0.1, key="fx", help="1 € = X MAD · OCP = 10,84 au 12/02/2026")
        d["taxe_communale"]  = num("Taxe communale (%)", d["taxe_communale"], mn=0.0, mx=50.0, step=0.5, key="tax_com", help="OCP Maroc = 10,5% · France = 0%")
        d["charge_locative"] = num("Charges locatives (%)", d["charge_locative"], mn=0.0, mx=20.0, step=0.5, key="chg_loc", help="OCP = 2%")

        st.markdown("<div class='sec'>🔧 Investissements amortis</div>", unsafe_allow_html=True)
        info("""Formule Polka : <strong>Annuité = Investissement × (taux_intérêt + 1/durée)</strong>
        Onglet <strong>Warehouse Costs</strong> : Racking PPL · Safety/Security · Cabling.""")

        c1i, c2i = st.columns(2)
        with c1i:
            d["cout_rack_ppl"] = num("Racks (€/empl.)", d["cout_rack_ppl"], step=1.0, key="rack_p", help="OCP = 30 €/empl.")
            d["cout_secu_m2"]  = num("Sécurité (€/m²)", d["cout_secu_m2"], step=0.5, key="secu_m", help="OCP = 12 €/m²")
            d["cout_cable_m2"] = num("Câblage (€/m²)", d["cout_cable_m2"], step=0.5, key="cab_m", help="OCP = 10,5 €/m²")
        with c2i:
            d["amort_rack"]  = num_int("Amort. racks (ans)", d["amort_rack"], mn=1, mx=30, key="am_r", help="Polka = 12 ans")
            d["amort_secu"]  = num_int("Amort. sécu (ans)", d["amort_secu"], mn=1, mx=20, key="am_s", help="Polka = 10 ans")
            d["amort_cable"] = num_int("Amort. câblage (ans)", d["amort_cable"], mn=1, mx=15, key="am_c", help="Polka = 5 ans")

        r = calc(d)
        st.markdown(f"""<div class='kpi-row'>
          <div class='kpi'><div class='kpi-lbl'>Loyer annuel (charges)</div><div class='kpi-val blue'>{r['loyer_tot']:,.0f} €</div></div>
          <div class='kpi'><div class='kpi-lbl'>Racks + Sécu + Câblage</div><div class='kpi-val orange'>{r['rack_an']+r['secu_an']+r['cable_an']:,.0f} €</div></div>
          <div class='kpi'><div class='kpi-lbl'>Total entrepôt / an</div><div class='kpi-val blue'>{r['cout_wh']:,.0f} €</div></div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.preset == "ocp":
            hint("Coût entrepôt OCP Polka réel = <strong>358 678 €/an</strong>")
    nav(1)

# ════════════════════════════════════════════════════════
# ÉTAPE 2 — PARAMÈTRES
# ════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    hdr(2,"⚙️","Paramètres Polka","Hypothèses financières et opérationnelles — onglet Branch's Basic Data.")
    info("Ces paramètres s'appliquent à <strong>tous les calculs</strong>. Valeurs OCP Polka V202541 pré-remplies.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>📅 Paramètres opérationnels</div>", unsafe_allow_html=True)
        d["jours_ouvres"] = num_int("Jours ouvrés / an", d["jours_ouvres"], mn=200, mx=365, key="jours",
                                    help="OCP = 272 j (5j/sem, hors fériés Maroc) · France ≈ 220 j")
        d["reserve_op"]   = num("Réserve opérationnelle (%)", d["reserve_op"], mn=0.0, mx=30.0, step=1.0, key="res_op",
                                 help="Déduit des emplacements bruts (zones tampon/défaillantes) · OCP = 10%")
        d["taux_panne"]   = num("Taux de défaillance engins (%)", d["taux_panne"], mn=0.0, mx=30.0, step=0.5, key="panne",
                                 help="% temps d'arrêt technique · Polka = 5%")
        d["batteries_li"] = st.checkbox("Batteries lithium-ion (LI)", value=bool(d["batteries_li"]),
                                         help="OCP = Oui · Évite les engins de substitution pendant recharge")
        if d["batteries_li"]: ok("LI activé — pas de doublement du parc pour recharge")
        else: warn("Batteries classiques — prévoir engins de substitution")

    with col2:
        st.markdown("<div class='sec'>💰 Paramètres financiers</div>", unsafe_allow_html=True)
        d["taux_interet"] = num("Taux d'intérêt interne (%)", d["taux_interet"], mn=0.0, mx=30.0, step=0.5, key="ti",
                                 help="Inclus dans l'annuité des investissements · Dachser standard = 9%")
        d["marge_cible"]  = num("🎯 Marge cible (%)", d["marge_cible"], mn=0.0, mx=30.0, step=0.5, key="marge_c",
                                 help="Objectif de marge nette du contrat · Polka = 10% · OCP réel = 8,61%")
        d["alloc_wms"]    = num("Allocation WMS + Innovation Fund (%)", d["alloc_wms"], mn=0.0, mx=10.0, step=0.1, key="wms_a",
                                 help="% des coûts variables → IT & Innovation Dachser · Polka = 2,2%")
        st.markdown("<div class='sec'>🚚 Primes transport</div>", unsafe_allow_html=True)
        d["prime_fret"]   = num("Prime risque fret (%)", d["prime_fret"], mn=0.0, mx=50.0, step=0.5, key="p_fret",
                                 help="Responsabilité civile marchandises palettes · Polka = 15%")
        d["prime_colis"]  = num("Prime risque colis (%)", d["prime_colis"], mn=0.0, mx=50.0, step=0.5, key="p_col",
                                 help="Responsabilité civile marchandises colis · Polka = 5%")
    nav(2)

# ════════════════════════════════════════════════════════
# ÉTAPE 3 — PERSONNEL
# ════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    hdr(3,"👷","Cockpit Personnel","Effectifs ETP et coûts salariaux — onglet Cockpit Personnel.")
    info("""Polka calcule les ETP à partir des volumes et productivités (<strong>Prods simplifiées</strong>).
    Formule : <strong>Coût = ETP × Salaire brut × (1 + 33% charges)</strong>.
    Admin OCP : 18 628 € brut → 24 819 € total chargé (HO 1,3% + RHO 31,9% inclus).""")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("<div class='sec'>🔵 Logistics Operatives — salaire brut OCP = 13 829 €/an</div>", unsafe_allow_html=True)
        STAFF_OP = [
            ("fte_cariste", "🚛 Cariste (Forklift Driver)",
             "Reach Trucks & Fast Movers · ETP Polka calculé = 3,29 → alloué OCP = 3,30"),
            ("fte_chargeur", "📦 Chargeur (Loader)",
             "Chargement camions sortie · ETP = 1,56 → 1,57"),
            ("fte_dechargeur", "📥 Déchargeur (Unloader)",
             "Déchargement camions réception · ETP = 0,84 → 0,85"),
            ("fte_ctrl", "🔍 Contrôleur réception",
             "Contrôle qualitatif/quantitatif · ETP = 0,49 → 0,50"),
            ("fte_picker", "🛒 Préparateur commandes (Picker)",
             "Picking colis · OCP = 0 (pas de picking détail)"),
        ]
        for k, lbl, tip in STAFF_OP:
            c1, c2 = st.columns([2, 1])
            with c1: d[k] = num(lbl, d[k], mn=0.0, mx=30.0, step=0.01, key=f"op_{k}", help=tip)
            with c2:
                cout = d[k] * d["sal_op"] * 1.333
                st.metric("Coût/an", f"{cout:,.0f} €")

        d["sal_op"] = num_int("💶 Salaire brut opérationnel (€/an)", d["sal_op"], mn=0, mx=100000, step=100,
                               key="sal_op_v", help="OCP = 13 829 €/an · France logistique ≈ 22 000-28 000 €")

        st.markdown("<div class='sec'>🟡 Office Employees — salaire brut OCP = 18 628 €/an</div>", unsafe_allow_html=True)
        STAFF_ADM = [
            ("fte_admin_in",  "📋 Admin. réception (Inbound Admin)",  "OCP = 1,00 ETP · Coût total Polka = 24 819 €/an"),
            ("fte_admin_out", "📤 Admin. expédition",                  "OCP = 0"),
            ("fte_svc_client","📞 Service client",                     "OCP = 0"),
            ("fte_coord",     "👥 Coordinateur équipe",                "OCP = 0"),
            ("fte_chef",      "🔧 Chef d'équipe (Shift Leader)",       "OCP = 0"),
            ("fte_resp",      "🏆 Responsable entrepôt",               "OCP = 0"),
        ]
        for k, lbl, tip in STAFF_ADM:
            c1, c2 = st.columns([2, 1])
            with c1: d[k] = num(lbl, d[k], mn=0.0, mx=20.0, step=0.01, key=f"adm_{k}", help=tip)
            with c2:
                cout = d[k] * d["sal_adm"] * 1.333
                st.metric("Coût/an", f"{cout:,.0f} €")

        d["sal_adm"] = num_int("💶 Salaire brut admin/encadrement (€/an)", d["sal_adm"], mn=0, mx=200000, step=100,
                                key="sal_adm_v", help="OCP = 18 628 €/an brut · Coût chargé total = 24 819 €")

    with col2:
        r = calc(d)
        st.markdown("<div class='sec'>📊 Récapitulatif</div>", unsafe_allow_html=True)
        st.markdown(f"""<div class='kpi-row' style='flex-direction:column;'>
          <div class='kpi'><div class='kpi-lbl'>ETP total</div><div class='kpi-val blue'>{r['fte_tot']:.2f}</div><div class='kpi-sub'>Op: {r['fte_op']:.2f} · Adm: {r['fte_adm']:.2f}</div></div>
          <div class='kpi'><div class='kpi-lbl'>Coût opérationnels</div><div class='kpi-val orange'>{r['pers_op']:,.0f} €</div></div>
          <div class='kpi'><div class='kpi-lbl'>Coût admin/encadr.</div><div class='kpi-val orange'>{r['pers_adm']:,.0f} €</div></div>
          <div class='kpi'><div class='kpi-lbl'>TOTAL personnel</div><div class='kpi-val blue'>{r['pers_tot']:,.0f} €</div></div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.preset == "ocp":
            hint("Personnel OCP Polka réel = <strong>148 419 €</strong>")

        st.markdown("<div class='sec'>📈 Productivités site OCP</div>", unsafe_allow_html=True)
        info("Onglet <strong>Prods simplifiées</strong> — mesures réelles OCP Mohammedia")
        d["prod_dech"]  = num("Déchargement (pal/h)", d["prod_dech"], step=1.0, key="pd1", help="OCP = 37,63 pal/h productive · ETP calculé = 1,34")
        d["prod_stock"] = num("Mise en stock (pal/h)", d["prod_stock"], step=1.0, key="pd2", help="OCP = 34,02 pal/h · ETP = 1,48")
        d["prod_prel"]  = num("Prélèvement (pal/h)", d["prod_prel"], step=1.0, key="pd3", help="OCP = 27,69 pal/h · ETP = 1,82")
        d["prod_charg"] = num("Chargement (pal/h)", d["prod_charg"], step=1.0, key="pd4", help="OCP = 32,19 pal/h · ETP = 1,56")
    nav(3)

# ════════════════════════════════════════════════════════
# ÉTAPE 4 — ENGINS
# ════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    hdr(4,"🏗️","Cockpit Engins","Parc d'engins alloué au contrat — onglet Cockpit Industrial Trucks.")
    info("""OCP : <strong>2,79 Fast Mover + 3,42 Reach Truck >8m = 6,21 engins · 56 074 €/an</strong>
    Prix = tarifs catalogue Polka Industrial Trucks. Mode <em>Rent</em> = location annuelle.""")

    ENGINS = [
        ("qt_fm",  "prix_fm",  "⚡ Fast Mover (FZ0040)",        "Rent",  10606, "Déchargement & chargement camions · OCP = 2,79 · 10 606 €/an · Prod: 37,63 pal/h dech · 32,19 pal/h charg"),
        ("qt_rt8", "prix_rt8", "🔝 Reach Truck > 8m (FZ0085)",  "Rent",  44619, "Stockage & prélèvement grande hauteur · OCP = 3,42 · 44 619 €/an · Prod: 34,02 mise stock · 27,69 prélèv"),
        ("qt_rt8m","prix_rt8m","🔼 Reach Truck ≤ 8m (FZ0080)",  "Rent",  31089, "Chariot standard hauteur ≤ 8m · OCP = 0 (entrepôt > 8m) · 31 089 €/an"),
        ("qt_tp",  "prix_tp",  "🤲 Transpalette manuel (FZ0010)","Buy",    375,  "Manutention sol · OCP = 0 · Achat 375 €"),
        ("qt_cf",  "prix_cf",  "🔄 Chariot frontal (FZ0070)",   "Rent",  22644, "Grande capacité · OCP = 0 · 22 644 €/an"),
        ("qt_ph",  "prix_ph",  "📋 Préparateur horiz. (FZ0050)","Rent",  11956, "Picking colis sol · OCP = 0 · 11 956 €/an"),
        ("qt_ae",  "prix_ae",  "↔️ Allée étroite (FZ0090)",     "Rent",  95000, "Haute densité · OCP = 0 · 95 000 €/an"),
        ("qt_bal", "prix_bal", "🧹 Balayeuse (FZ0100)",         "Buy",   24990, "Entretien sol · OCP = 0 · Achat 24 990 €"),
    ]

    total_qt = 0; total_cout = 0
    for i, (qk, pk, lbl, mode, prix_ref, tip) in enumerate(ENGINS):
        active = d[qk] > 0
        with st.expander(f"{'🟢' if active else '⚫'} {lbl} — {d[qk]:.2f} unités", expanded=active):
            st.caption(f"_{tip}_")
            c1, c2, c3 = st.columns([2,2,1])
            with c1: d[qk] = num("Quantité", d[qk], mn=0.0, mx=50.0, step=0.01, key=f"qt_{qk}_{i}")
            with c2: d[pk] = num_int(f"€/engin/an ({mode})", d[pk], mn=0, mx=500000, step=100, key=f"px_{pk}_{i}")
            with c3: st.metric("Total", f"{d[qk]*d[pk]:,.0f} €")
            total_qt += d[qk]; total_cout += d[qk]*d[pk]

    st.divider()
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("Parc total", f"{total_qt:.2f} engins")
    with c2: st.metric("Coût engins/an", f"{total_cout:,.0f} €")
    with c3: st.metric("Coût moyen/engin", f"{total_cout/max(total_qt,1):,.0f} €/an")
    if st.session_state.preset == "ocp":
        hint("Coût engins OCP Polka réel = <strong>56 074 €</strong>")
    nav(4)

# ════════════════════════════════════════════════════════
# ÉTAPE 5 — VOLUMES & PROCESSUS
# ════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    hdr(5,"📊","Volumes & Processus","Quantités annuelles — onglets Register Quantity Data et UO.")
    info("""Onglet <strong>UO</strong> : Budget prévisionnel OCP par activité et unité d'oeuvre.
    OCP actif : <strong>Stockage + FP Inbound (MF1070) + FP Outbound (MF4010)</strong>.""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>🏭 Stockage</div>", unsafe_allow_html=True)
        info("OCP : 4 000 empl. × 6,58 €/mois × 12 = <strong>315 840 € CA stockage</strong> (déficitaire : coûts = 358 678 €)")
        d["empl_vendus"] = num_int("Emplacements vendus contractuellement", d["empl_vendus"], step=10, key="ev",
                                    help="OCP = 4 000 empl. (100% occupation)")
        empl_nets = round(d["emplacements_brut"] * d["taux_utilisation"] / 100)
        taux_occ = d["empl_vendus"] / max(empl_nets, 1) * 100
        if taux_occ > 100: warn(f"Occupation {taux_occ:.1f}% > capacité nette ({empl_nets:,} empl.)")
        elif taux_occ > 85: ok(f"Occupation {taux_occ:.1f}% — niveau optimal")
        else: hint(f"Occupation {taux_occ:.1f}% / {empl_nets:,} empl. nets")

        st.markdown("<div class='sec'>📥 Flux entrants — FP Inbound</div>", unsafe_allow_html=True)
        info("MF1070 = Stock-in Inbound Pallets · OCP = 70 720 pal/an = <strong>260 pal/jour</strong>")
        d["vol_in_pal"]  = num_int("Palettes mises en stock / an (MF1070)", d["vol_in_pal"], step=100, key="vi1",
                                    help="OCP UO : 70 720 pal × 2,03 € process + 13,84 €/livr = 181 200 € budget réception")
        d["vol_in_livr"] = num_int("Livraisons / camions reçus / an (MF1010)", d["vol_in_livr"], step=1, key="vi2",
                                    help="OCP UO : 2 720 livraisons/an × 13,84 €/livr · Non facturé séparément ici")

        st.markdown("<div class='sec'>🖥️ IT & WMS</div>", unsafe_allow_html=True)
        d["cout_it"] = num_int("Coûts IT fixes / an (€)", d["cout_it"], step=100, key="cit",
                                help="OCP = 2 182 €/an · WMS MIKADO global = 17 277 € réparti entre clients")

    with col2:
        st.markdown("<div class='sec'>📤 Flux sortants — FP Outbound</div>", unsafe_allow_html=True)
        info("MF4010 = Full Pallets · OCP = 70 720 pal/an (flux symétrique aux entrées)")
        d["vol_out_pal"] = num_int("Palettes complètes expédiées / an (MF4010)", d["vol_out_pal"], step=100, key="vo1",
                                    help="OCP UO : 70 720 pal × 2,03 € process + 4 597 ordres × 13,84 € = 207 172 € budget expé.")
        d["vol_out_cmd"] = num_int("Ordres de sortie / an (MF4020)", d["vol_out_cmd"], step=10, key="vo2",
                                    help="OCP UO = 4 597 ordres/an · non facturé séparément")

        st.markdown("<div class='sec'>🚛 Chargement camions — FP Loading</div>", unsafe_allow_html=True)
        info("OCP = 0 volume séparé · Le chargement est inclus dans le tarif sortie palette (ETP = 1,56)")
        d["vol_charg_cam"] = num_int("Chargements camions / an (MF5010)", d["vol_charg_cam"], step=1, key="vc1",
                                      help="OCP = 0 (inclus dans le tarif sortie)")
        d["vol_charg_pal"] = num_int("Palettes chargées / an (MF5020)", d["vol_charg_pal"], step=100, key="vc2",
                                      help="OCP = 0")

        if d["vol_in_pal"] > 0 or d["vol_out_pal"] > 0:
            j = max(d["jours_ouvres"], 1)
            st.markdown(f"""<div class='kpi-row' style='margin-top:16px;'>
              <div class='kpi'><div class='kpi-lbl'>Entrées / jour</div><div class='kpi-val blue'>{d['vol_in_pal']/j:.1f} pal/j</div></div>
              <div class='kpi'><div class='kpi-lbl'>Sorties / jour</div><div class='kpi-val blue'>{d['vol_out_pal']/j:.1f} pal/j</div></div>
              <div class='kpi'><div class='kpi-lbl'>Total mvts / jour</div><div class='kpi-val blue'>{(d['vol_in_pal']+d['vol_out_pal'])/j:.1f} pal/j</div></div>
            </div>""", unsafe_allow_html=True)
    nav(5)

# ════════════════════════════════════════════════════════
# ÉTAPE 6 — VISUALISATION PROCESSUS
# ════════════════════════════════════════════════════════
elif st.session_state.step == 6:
    hdr(6,"🔀","Design des Processus","Visualisation du flux logistique OCP — onglets Process Design & Prods simplifiées.")
    info("Cette vue reproduit la logique de l'onglet <strong>Process Design</strong> de Polka — sous-processus actifs OCP avec productivités réelles.")

    # Calcul ETP par processus
    j = max(d["jours_ouvres"], 1)
    vol_in  = d["vol_in_pal"]
    vol_out = d["vol_out_pal"]
    taux_charge = 0.40  # 40% taux moyen appliqué OCP

    def etp_process(vol_j, prod_h, taux=taux_charge):
        """ETP = (Volume/j ÷ Prod/h) × (1 + taux_charge) / (8h/j)"""
        if prod_h <= 0: return 0
        h_prod = vol_j / prod_h
        return h_prod * (1 + taux) / 8

    etp_dech  = etp_process(vol_in/j, d["prod_dech"])
    etp_stock = etp_process(vol_in/j, d["prod_stock"])
    etp_prel  = etp_process(vol_out/j, d["prod_prel"])
    etp_charg = etp_process(vol_out/j, d["prod_charg"])

    st.markdown("### 📦 Flux Entrant — FP Inbound (TP1020 + TP1120 + TP1220)")

    st.markdown(f"""
    <div style='display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin:14px 0;'>
      <div class='proc-box' style='flex:1;min-width:180px;border-top:4px solid #2952d9;'>
        <div class='proc-title'>🚛 TP1020 · Déchargement camion</div>
        <div class='proc-step'>Drive camion → zone réception</div>
        <div class='proc-step'>Prise palette (Fast Mover)</div>
        <div class='proc-step'>Contrôle dommages & quantités</div>
        <div class='proc-step'>Mesure température</div>
        <div style='margin-top:8px;font-size:12px;color:#2952d9;font-weight:700;'>
          {d['prod_dech']:.1f} pal/h (prod.) · ETP calculé : {etp_dech:.2f}
        </div>
        <div style='margin-top:4px;'><span class='badge-active'>ACTIF OCP</span> <span style='font-size:11px;color:#6b7bad;'>MF1020</span></div>
      </div>
      <div style='font-size:28px;color:#5c7cff;'>→</div>
      <div class='proc-box' style='flex:1;min-width:180px;border-top:4px solid #0891b2;'>
        <div class='proc-title'>🔍 TP1120 · Contrôle & étiquetage</div>
        <div class='proc-step'>Scan SSCC + saisie WMS MIKADO</div>
        <div class='proc-step'>Impression étiquette MIKADO</div>
        <div class='proc-step'>Création articles nouveaux</div>
        <div class='proc-step'>Gestion BBD/lot (si applicable)</div>
        <div style='margin-top:8px;font-size:12px;color:#0891b2;font-weight:700;'>
          266 pal/h (prod.) · ETP calculé : 0,27
        </div>
        <div style='margin-top:4px;'><span class='badge-active'>ACTIF OCP</span> <span style='font-size:11px;color:#6b7bad;'>MF1070</span></div>
      </div>
      <div style='font-size:28px;color:#5c7cff;'>→</div>
      <div class='proc-box' style='flex:1;min-width:180px;border-top:4px solid #059669;'>
        <div class='proc-title'>📦 TP1220 · Mise en stock</div>
        <div class='proc-step'>Scan SSCC + lecture emplacement cible</div>
        <div class='proc-step'>Levée chargée (Reach Truck >8m)</div>
        <div class='proc-step'>Drive zone réception → rack</div>
        <div class='proc-step'>Pose palette · Confirmation WMS</div>
        <div style='margin-top:8px;font-size:12px;color:#059669;font-weight:700;'>
          {d['prod_stock']:.1f} pal/h (prod.) · ETP calculé : {etp_stock:.2f}
        </div>
        <div style='margin-top:4px;'><span class='badge-active'>ACTIF OCP</span> <span style='font-size:11px;color:#6b7bad;'>MF1070</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📤 Flux Sortant — FP Outbound (TP4010) + Chargement (TP5020)")

    st.markdown(f"""
    <div style='display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin:14px 0;'>
      <div class='proc-box' style='flex:1;min-width:180px;border-top:4px solid #d97706;'>
        <div class='proc-title'>🔽 TP4010 · Prélèvement palette</div>
        <div class='proc-step'>Sélection ordre sur terminal</div>
        <div class='proc-step'>Drive rack → emplacement cible</div>
        <div class='proc-step'>Levée non chargée · Prise palette</div>
        <div class='proc-step'>Drive → zone I-Point</div>
        <div class='proc-step'>Impression BL + étiquette expé.</div>
        <div class='proc-step'>Dépôt zone outbound</div>
        <div style='margin-top:8px;font-size:12px;color:#d97706;font-weight:700;'>
          {d['prod_prel']:.1f} pal/h (prod.) · ETP calculé : {etp_prel:.2f}
        </div>
        <div style='margin-top:4px;'><span class='badge-active'>ACTIF OCP</span> <span style='font-size:11px;color:#6b7bad;'>MF4010</span></div>
      </div>
      <div style='font-size:28px;color:#5c7cff;'>→</div>
      <div class='proc-box' style='flex:1;min-width:180px;border-top:4px solid #dc2626;'>
        <div class='proc-title'>🚛 TP5020 · Chargement camion</div>
        <div class='proc-step'>Login procédure chargement I-Point</div>
        <div class='proc-step'>Vérification zone outbound</div>
        <div class='proc-step'>Scan étiquette expédition</div>
        <div class='proc-step'>Prise palette (Fast Mover)</div>
        <div class='proc-step'>Drive zone outbound → camion</div>
        <div class='proc-step'>Fermeture remorque + BL</div>
        <div style='margin-top:8px;font-size:12px;color:#dc2626;font-weight:700;'>
          {d['prod_charg']:.1f} pal/h (prod.) · ETP calculé : {etp_charg:.2f}
        </div>
        <div style='margin-top:4px;'><span class='badge-active'>ACTIF OCP</span> <span style='font-size:11px;color:#6b7bad;'>MF5020</span></div>
      </div>
      <div style='font-size:28px;color:#5c7cff;'>→</div>
      <div class='proc-box' style='flex:1;min-width:180px;border-top:4px solid #6b7280;opacity:0.6;'>
        <div class='proc-title'>🔄 Processus non actifs OCP</div>
        <div class='proc-step' style='background:#f3f4f6;color:#9ca3af;'>Picking colis (TP2xxx)</div>
        <div class='proc-step' style='background:#f3f4f6;color:#9ca3af;'>Palettes mixtes (TP2020)</div>
        <div class='proc-step' style='background:#f3f4f6;color:#9ca3af;'>VAS / conditionnement</div>
        <div class='proc-step' style='background:#f3f4f6;color:#9ca3af;'>Réapprovisionnement</div>
        <div style='margin-top:8px;'><span class='badge-inactive'>INACTIF OCP</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Tableau récap ETP par processus
    st.markdown("### 📊 ETP calculés par processus (Prods simplifiées OCP)")
    proc_df = pd.DataFrame({
        "Processus": ["Déchargement camion (TP1020)","Contrôle & étiquetage (TP1120)","Mise en stock (TP1220)","Prélèvement palette (TP4010)","Chargement camion (TP5020)","TOTAL"],
        "Prod. pal/h": [d["prod_dech"], 266.0, d["prod_stock"], d["prod_prel"], d["prod_charg"], "—"],
        "Vol/jour": [f"{vol_in/j:.0f}", f"{vol_in/j:.0f}", f"{vol_in/j:.0f}", f"{vol_out/j:.0f}", f"{vol_out/j:.0f}", "—"],
        "ETP calculé": [f"{etp_dech:.2f}", "0.27", f"{etp_stock:.2f}", f"{etp_prel:.2f}", f"{etp_charg:.2f}", f"{etp_dech+0.27+etp_stock+etp_prel+etp_charg:.2f}"],
        "ETP alloué OCP": ["1.34","0.27","1.48","1.82","1.56","6.47"],
        "Engin": ["Fast Mover","—","Reach Truck >8m","Reach Truck >8m","Fast Mover","—"],
        "Statut": ["✅ Actif","✅ Actif","✅ Actif","✅ Actif","✅ Actif","—"],
    })
    st.dataframe(proc_df, use_container_width=True, hide_index=True)

    # Layout entrepôt simplifié
    st.markdown("### 🗺️ Schéma flux entrepôt OCP (WH0010)")
    st.markdown("""
    <div style='background:white;border:2px solid #c5cdf5;border-radius:14px;padding:20px;font-family:monospace;font-size:12px;line-height:1.8;'>
      <div style='display:grid;grid-template-columns:1fr 3fr 1fr;gap:10px;'>
        <div style='background:#dbeafe;border:2px dashed #3b82f6;border-radius:8px;padding:12px;text-align:center;'>
          <div style='font-weight:700;color:#1e40af;'>📥 ZONE RÉCEPTION</div>
          <div style='color:#3b82f6;font-size:11px;'>Quais entrants<br>Contrôle & étiquetage<br>Tampon entrée</div>
        </div>
        <div style='background:#f0fdf4;border:2px solid #22c55e;border-radius:8px;padding:12px;text-align:center;'>
          <div style='font-weight:700;color:#15803d;font-size:14px;'>🏭 ZONE STOCKAGE — 4 040 m² · 10m hauteur</div>
          <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-top:8px;'>
            <div style='background:#bbf7d0;border-radius:4px;padding:4px;text-align:center;font-size:10px;'>RACK A<br>Reach Truck</div>
            <div style='background:#bbf7d0;border-radius:4px;padding:4px;text-align:center;font-size:10px;'>RACK B<br>>8m</div>
            <div style='background:#bbf7d0;border-radius:4px;padding:4px;text-align:center;font-size:10px;'>RACK C<br>Fast Mover</div>
            <div style='background:#bbf7d0;border-radius:4px;padding:4px;text-align:center;font-size:10px;'>RACK D<br>allées</div>
          </div>
          <div style='margin-top:8px;font-size:11px;color:#166534;'>4 211 empl. bruts · 4 000 empl. nets (95%) · 1,04 pal/m²</div>
        </div>
        <div style='background:#fef3c7;border:2px dashed #f59e0b;border-radius:8px;padding:12px;text-align:center;'>
          <div style='font-weight:700;color:#92400e;'>📤 ZONE EXPÉDITION</div>
          <div style='color:#b45309;font-size:11px;'>Quais sortants<br>I-Point BL/étiquettes<br>Tampon sortie</div>
        </div>
      </div>
      <div style='display:flex;justify-content:space-around;margin-top:12px;'>
        <div style='text-align:center;font-size:11px;color:#6b7bad;'>⚡ Fast Mover × 2,79<br>Déchargement · Chargement</div>
        <div style='text-align:center;font-size:11px;color:#6b7bad;'>🔝 Reach Truck >8m × 3,42<br>Mise en stock · Prélèvement</div>
        <div style='text-align:center;font-size:11px;color:#6b7bad;'>🖥️ WMS MIKADO<br>Pilotage tous processus</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    nav(6)

# ════════════════════════════════════════════════════════
# ÉTAPE 7 — CALCUL TARIFS
# ════════════════════════════════════════════════════════
elif st.session_state.step == 7:
    hdr(7,"💶","Calcul des Tarifs","Tarifs recommandés selon la logique Polka — avec simulateur interactif.")

    r = calc(d)
    m_ok = r["marge"] >= d["marge_cible"]

    # KPIs principaux
    mc = "green" if m_ok else "red"
    st.markdown(f"""<div class='kpi-row'>
      <div class='kpi'><div class='kpi-lbl'>CA estimé</div><div class='kpi-val blue'>{r['ca']:,.0f} €</div></div>
      <div class='kpi'><div class='kpi-lbl'>Coûts totaux</div><div class='kpi-val orange'>{r['cout_tot']:,.0f} €</div></div>
      <div class='kpi'><div class='kpi-lbl'>Bénéfice</div><div class='kpi-val {"green" if r["profit"]>0 else "red"}'>{r['profit']:,.0f} €</div></div>
      <div class='kpi'><div class='kpi-lbl'>Marge réelle</div><div class='kpi-val {mc}'>{r['marge']:.2f}%</div><div class='kpi-sub'>Objectif : {d['marge_cible']:.1f}%</div></div>
    </div>""", unsafe_allow_html=True)

    if m_ok: ok(f"Marge {r['marge']:.2f}% ≥ objectif {d['marge_cible']:.1f}%")
    else:
        gap = (d["marge_cible"]/100 - r["marge"]/100) * r["ca"]
        warn(f"Marge {r['marge']:.2f}% < objectif {d['marge_cible']:.1f}% — Manque {gap:,.0f} €/an")

    st.markdown("---")
    st.markdown("### 💶 Tarifs recommandés")
    info("Formule Polka : <strong>Prix = Coût unitaire ÷ (1 − marge cible)</strong> · Ajustez les tarifs ci-dessous pour simuler différents scénarios.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**🏭 Stockage (WH0010)**")
        st.caption(f"Coût min : {r['cu_stock']:.4f} €/empl./mois · Recommandé : {r['prix_stock']:.4f} €")
        px_s = num("€ / empl. / mois", r["prix_stock"], mn=0.0, mx=100.0, step=0.01, key="pxs")
        ca_s = d["empl_vendus"] * px_s * 12
        mg_s = (ca_s - r["cout_wh"]) / ca_s * 100 if ca_s > 0 else 0
        col = "green" if mg_s >= 0 else "red"
        st.markdown(f"""<div class='kpi'>
          <div class='kpi-lbl'>CA stockage annuel</div>
          <div class='kpi-val {col}'>{ca_s:,.0f} €</div>
          <div class='kpi-sub'>Marge : {mg_s:.2f}% · {px_s*12:.2f} €/an/empl.</div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.preset == "ocp":
            st.caption(f"OCP réel = {d['tarif_stock_mois']:.2f} €/mois → {d['tarif_stock_mois']*d['empl_vendus']*12:,.0f} €/an")

    with col2:
        st.markdown("**📥 Entrée palette (MF1070)**")
        st.caption(f"Coût min : {r['cu_in']:.4f} € · Recommandé : {r['prix_in']:.4f} €")
        px_i = num("€ / palette entrante", r["prix_in"], mn=0.0, mx=50.0, step=0.01, key="pxi")
        ca_i = d["vol_in_pal"] * px_i
        mg_i = (ca_i - r["proc_in"]) / ca_i * 100 if ca_i > 0 else 0
        col = "green" if mg_i >= 0 else "red"
        st.markdown(f"""<div class='kpi'>
          <div class='kpi-lbl'>CA entrées annuel</div>
          <div class='kpi-val {col}'>{ca_i:,.0f} €</div>
          <div class='kpi-sub'>Marge : {mg_i:.2f}% · {d['vol_in_pal']:,} pal × {px_i:.4f} €</div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.preset == "ocp":
            st.caption(f"OCP réel = {d['tarif_in']:.3f} €/pal → {d['tarif_in']*d['vol_in_pal']:,.0f} €/an")

    with col3:
        st.markdown("**📤 Sortie palette (MF4010)**")
        st.caption(f"Coût min : {r['cu_out']:.4f} € · Recommandé : {r['prix_out']:.4f} €")
        px_o = num("€ / palette sortante", r["prix_out"], mn=0.0, mx=50.0, step=0.01, key="pxo")
        ca_o = d["vol_out_pal"] * px_o
        mg_o = (ca_o - r["proc_out"]) / ca_o * 100 if ca_o > 0 else 0
        col = "green" if mg_o >= 0 else "red"
        st.markdown(f"""<div class='kpi'>
          <div class='kpi-lbl'>CA sorties annuel</div>
          <div class='kpi-val {col}'>{ca_o:,.0f} €</div>
          <div class='kpi-sub'>Marge : {mg_o:.2f}% · {d['vol_out_pal']:,} pal × {px_o:.4f} €</div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.preset == "ocp":
            st.caption(f"OCP réel = {d['tarif_out']:.3f} €/pal → {d['tarif_out']*d['vol_out_pal']:,.0f} €/an")

    st.markdown("---")
    st.markdown("### 🧩 Décomposition des coûts")
    cost_df = pd.DataFrame({
        "Poste": ["🏭 Loyer (charges incluses)","🔧 Investissements amortis","👷 Personnel opérationnel",
                   "📋 Personnel admin/encadr.","🏗️ Engins manutention","🖥️ IT & WMS","━ TOTAL"],
        "€/an":  [f"{r['loyer_tot']:,.0f}", f"{r['rack_an']+r['secu_an']+r['cable_an']:,.0f}",
                   f"{r['pers_op']:,.0f}", f"{r['pers_adm']:,.0f}", f"{r['engins_cout']:,.0f}",
                   f"{r['it_tot']:,.0f}", f"{r['cout_tot']:,.0f}"],
        "Part":  [f"{r['loyer_tot']/max(r['cout_tot'],1)*100:.1f}%",
                   f"{(r['rack_an']+r['secu_an']+r['cable_an'])/max(r['cout_tot'],1)*100:.1f}%",
                   f"{r['pers_op']/max(r['cout_tot'],1)*100:.1f}%",
                   f"{r['pers_adm']/max(r['cout_tot'],1)*100:.1f}%",
                   f"{r['engins_cout']/max(r['cout_tot'],1)*100:.1f}%",
                   f"{r['it_tot']/max(r['cout_tot'],1)*100:.1f}%","100%"],
    })
    st.dataframe(cost_df, use_container_width=True, hide_index=True)

    if st.session_state.preset == "ocp":
        st.markdown("### 🔄 Comparatif OCP réel vs calculé (Polka V202541)")
        cmp = pd.DataFrame({
            "": ["Stockage/empl./mois","Entrée palette","Sortie palette","CA total","Coûts","Bénéfice","Marge"],
            "OCP réel Polka": [f"{d['tarif_stock_mois']:.2f} €",f"{d['tarif_in']:.3f} €",f"{d['tarif_out']:.3f} €",
                                f"{d['ca_reel']:,.0f} €",f"{d['cout_reel']:,.0f} €",f"{d['profit_reel']:,.0f} €",f"{d['marge_reelle']:.2f}%"],
            "Wizard calculé": [f"{r['prix_stock']:.2f} €",f"{r['prix_in']:.3f} €",f"{r['prix_out']:.3f} €",
                                f"{r['ca']:,.0f} €",f"{r['cout_tot']:,.0f} €",f"{r['profit']:,.0f} €",f"{r['marge']:.2f}%"],
        })
        st.dataframe(cmp, use_container_width=True, hide_index=True)

    st.markdown("---")
    export = {"Projet": d["projet"], "Site": d["agence"],
              "CA_total": round(r["ca"],2), "Couts_totaux": round(r["cout_tot"],2),
              "Benefice": round(r["profit"],2), "Marge_pct": round(r["marge"],2),
              "Prix_stockage_mois": round(r["prix_stock"],4),
              "Prix_entree_palette": round(r["prix_in"],4),
              "Prix_sortie_palette": round(r["prix_out"],4),
              "ETP_total": round(r["fte_tot"],2)}
    st.download_button("⬇️ Export JSON", json.dumps(export,indent=2,ensure_ascii=False),
                        f"polka_{d['projet'] or 'projet'}.json","application/json",type="primary")
    nav(7)

# ════════════════════════════════════════════════════════
# ÉTAPE 8 — SENSIBILITÉ
# ════════════════════════════════════════════════════════
elif st.session_state.step == 8:
    hdr(8,"📉","Analyse de Sensibilité","Impact des variations sur la marge · Seuil de rentabilité · Scénarios.")

    r = calc(d)

    st.markdown("### 📊 Tableau de sensibilité ±20%")
    rows = []
    for v in [-20,-15,-10,-5,0,5,10,15,20]:
        f = 1 + v/100
        dv = deepcopy(d); dv["vol_in_pal"]=int(d["vol_in_pal"]*f); dv["vol_out_pal"]=int(d["vol_out_pal"]*f)
        rv = calc(dv)
        dl = deepcopy(d); dl["loyer_m2_mois"] = d["loyer_m2_mois"]*f
        rl = calc(dl)
        ds = deepcopy(d); ds["sal_op"]=int(d["sal_op"]*f); ds["sal_adm"]=int(d["sal_adm"]*f)
        rs = calc(ds)
        rows.append({"Variation":f"{v:+d}%",
                     "Marge/volumes":f"{rv['marge']:.2f}%","Profit volumes":f"{rv['profit']:,.0f} €",
                     "Marge/loyer":f"{rl['marge']:.2f}%","Profit loyer":f"{rl['profit']:,.0f} €",
                     "Marge/salaires":f"{rs['marge']:.2f}%","Profit salaires":f"{rs['profit']:,.0f} €"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🎛️ Simulateur de scénario")
    c1,c2,c3,c4 = st.columns(4)
    with c1: sv = st.slider("📦 Volumes (%)", -50, 50, 0, 5, key="sl_v")
    with c2: sl = st.slider("🏭 Loyer (%)", -50, 100, 0, 5, key="sl_l")
    with c3: ss = st.slider("👷 Salaires (%)", -30, 50, 0, 5, key="sl_s")
    with c4: sm = st.slider("🎯 Marge cible (%)", 0, 25, int(d["marge_cible"]), 1, key="sl_m")

    dsim = deepcopy(d)
    dsim["vol_in_pal"]  = int(d["vol_in_pal"] * (1+sv/100))
    dsim["vol_out_pal"] = int(d["vol_out_pal"] * (1+sv/100))
    dsim["loyer_m2_mois"] = d["loyer_m2_mois"] * (1+sl/100)
    dsim["sal_op"]  = int(d["sal_op"]  * (1+ss/100))
    dsim["sal_adm"] = int(d["sal_adm"] * (1+ss/100))
    dsim["marge_cible"] = float(sm)
    rsim = calc(dsim)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("CA simulé",     f"{rsim['ca']:,.0f} €",       delta=f"{rsim['ca']-r['ca']:+,.0f} €")
    with c2: st.metric("Coûts simulés", f"{rsim['cout_tot']:,.0f} €", delta=f"{rsim['cout_tot']-r['cout_tot']:+,.0f} €", delta_color="inverse")
    with c3: st.metric("Bénéfice simulé",f"{rsim['profit']:,.0f} €",  delta=f"{rsim['profit']-r['profit']:+,.0f} €")
    with c4: st.metric("Marge simulée", f"{rsim['marge']:.2f}%",      delta=f"{rsim['marge']-r['marge']:+.2f}%")

    if rsim["marge"] >= dsim["marge_cible"]:
        ok(f"Objectif {dsim['marge_cible']:.1f}% atteint dans ce scénario !")
    else:
        gap = (dsim["marge_cible"]/100 - rsim["marge"]/100) * rsim["ca"]
        warn(f"Manque {gap:,.0f} €/an pour atteindre {dsim['marge_cible']:.1f}%")

    st.markdown("---")
    st.markdown("### 📍 Seuil de rentabilité (Point mort)")
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("CA seuil", f"{r['seuil']:,.0f} €", help="CA minimum pour couvrir les coûts fixes")
    with c2: st.metric("CA actuel", f"{r['ca']:,.0f} €")
    with c3:
        cushion = (r["ca"] - r["seuil"]) / max(r["ca"],1) * 100
        st.metric("Marge de sécurité", f"{cushion:.1f}%",
                  delta="✅ Solide" if cushion > 20 else ("⚠️ Correct" if cushion > 5 else "🔴 Fragile"))
    nav(8)

st.markdown("""<div style='text-align:center;padding:14px 0 4px;color:#9ca3af;font-size:11px;
     border-top:1px solid #e5e7eb;margin-top:20px;'>
  Polka Wizard v3 · Polka V202541 · OCP Morocco · Dachser Contract Logistics
</div>""", unsafe_allow_html=True)
