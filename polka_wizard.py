"""
╔══════════════════════════════════════════════════════════════════════════════╗
║        POLKA WIZARD — Outil de tarification logistique                      ║
║        Basé sur le modèle Polka V202541 · OCP Morocco                       ║
║        Lancez avec : streamlit run polka_wizard.py                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import math
import json
from copy import deepcopy

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Polka Wizard — Tarification Logistique",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; color: #e8eaf6; }
    .block-container { padding-top: 1.5rem; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2e3250; }
    [data-testid="stSidebar"] .stRadio label { font-size: 13px; }
    
    /* Cards */
    .wizard-card {
        background: #1a1d27;
        border: 1px solid #2e3250;
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 16px;
    }
    .kpi-row { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 18px; }
    .kpi-box {
        flex: 1; min-width: 150px;
        background: #222638;
        border: 1px solid #2e3250;
        border-radius: 12px;
        padding: 16px 18px;
        text-align: center;
    }
    .kpi-label { font-size: 11px; color: #7b82a8; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px; }
    .kpi-value { font-size: 22px; font-weight: 800; }
    .kpi-sub { font-size: 11px; color: #7b82a8; margin-top: 4px; }
    
    /* Step header */
    .step-header {
        background: linear-gradient(135deg, #1a1d27, #222638);
        border: 1px solid #2e3250;
        border-left: 4px solid #4f7cff;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 22px;
    }
    .step-number { font-size: 11px; color: #4f7cff; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }
    .step-title { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
    .step-desc { font-size: 13px; color: #7b82a8; }
    
    /* Result block */
    .result-block {
        background: #0d1f3c;
        border: 1px solid #1e3a6e;
        border-radius: 12px;
        padding: 18px 22px;
        margin-top: 12px;
    }
    .result-positive { color: #22d3a0; }
    .result-negative { color: #ff5c6a; }
    .result-neutral { color: #4f7cff; }
    
    /* Warning box */
    .warn-box {
        background: rgba(255,181,71,0.08);
        border: 1px solid rgba(255,181,71,0.3);
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 13px;
        color: #ffb547;
        margin: 10px 0;
    }
    .ok-box {
        background: rgba(34,211,160,0.08);
        border: 1px solid rgba(34,211,160,0.3);
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 13px;
        color: #22d3a0;
        margin: 10px 0;
    }
    
    /* Section title */
    h2 { color: #e8eaf6 !important; }
    h3 { color: #c5cae9 !important; font-size: 15px !important; }
    
    /* Streamlit overrides */
    .stNumberInput > div > div > input { background: #222638; color: #e8eaf6; border-color: #2e3250; }
    .stSelectbox > div > div { background: #222638; color: #e8eaf6; }
    .stTextInput > div > div > input { background: #222638; color: #e8eaf6; }
    div[data-testid="metric-container"] { background: #222638; border: 1px solid #2e3250; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# DEFAULT DATA (OCP Morocco Polka V202541)
# ─────────────────────────────────────────────────────────
OCP_DEFAULTS = {
    # Projet
    "project_name": "OCP",
    "project_leader": "Reda Lamdarhri Kachani",
    "site": "MA-Mohammedia (580)",
    "country": "Maroc",
    "wms": "MIKADO",
    # Paramètres globaux
    "working_days": 272,
    "interest_rate": 0.09,
    "target_margin": 0.10,
    "op_reserve": 0.10,
    "equip_failure_rate": 0.05,
    "wms_allocation": 0.022,
    "li_batteries": True,
    "freight_risk_premium": 0.15,
    "parcel_risk_premium": 0.05,
    # Entrepôt
    "warehouse_area_m2": 4039.74,
    "warehouse_height_m": 10.0,
    "total_locations": 4211,
    "target_utilization": 0.95,
    "rent_per_m2_month": 5.219,
    "racking_cost_ppl": 30.0,
    # Personnel (ETP alloués OCP)
    "forklift_driver": 3.3,
    "loader": 1.57,
    "unloader": 0.85,
    "inbound_controller": 0.5,
    "inbound_admin": 1.0,
    "picker": 0.0,
    "team_coordinator": 0.0,
    "shift_leader": 0.0,
    "warehouse_manager": 0.0,
    "outbound_admin": 0.0,
    # Salaires annuels bruts (€)
    "salary_forklift": 13829,
    "salary_loader": 13829,
    "salary_unloader": 13829,
    "salary_controller": 13829,
    "salary_admin": 18628,
    "salary_picker": 13829,
    "salary_coordinator": 22000,
    "salary_shift_leader": 25000,
    "salary_manager": 45000,
    "social_charges_rate": 0.33,
    # Engins (quantités allouées OCP)
    "fast_mover_qty": 2.79,
    "reach_truck_8m_qty": 0.0,
    "reach_truck_gt8m_qty": 3.42,
    "hand_pallet_qty": 0.0,
    "front_loader_qty": 0.0,
    "order_picker_qty": 0.0,
    "narrow_aisle_qty": 0.0,
    # Prix engins (location annuelle €)
    "fast_mover_price": 10606,
    "reach_truck_8m_price": 31089,
    "reach_truck_gt8m_price": 44619,
    "hand_pallet_price": 375,
    "front_loader_price": 22644,
    "order_picker_price": 11956,
    "narrow_aisle_price": 95000,
    # Volumes & processus
    "storage_locations_sold": 4000,
    "inbound_pallets_year": 70720,
    "outbound_pallets_year": 70720,
    "inbound_loose_units": 0,
    "outbound_loose_units": 0,
    "trucks_loaded_year": 0,
    # Autres coûts fixes
    "it_costs_year": 2182,
    "other_fixed_costs": 0,
    "allocation_wms_pct": 0.022,
}

EMPTY_DEFAULTS = {k: (0 if isinstance(v, (int, float)) and k not in
    ["working_days","interest_rate","target_margin","op_reserve","equip_failure_rate",
     "wms_allocation","freight_risk_premium","parcel_risk_premium","target_utilization",
     "warehouse_height_m","social_charges_rate"]
    else v if isinstance(v, str) or isinstance(v, bool) else v)
    for k, v in OCP_DEFAULTS.items()}

# Reset strings to empty
for k in ["project_name","project_leader","site","country","wms"]:
    EMPTY_DEFAULTS[k] = ""
# Keep sensible minimums
EMPTY_DEFAULTS["working_days"] = 250
EMPTY_DEFAULTS["interest_rate"] = 0.09
EMPTY_DEFAULTS["target_margin"] = 0.10
EMPTY_DEFAULTS["op_reserve"] = 0.10
EMPTY_DEFAULTS["equip_failure_rate"] = 0.05
EMPTY_DEFAULTS["wms_allocation"] = 0.022
EMPTY_DEFAULTS["warehouse_height_m"] = 10.0
EMPTY_DEFAULTS["target_utilization"] = 0.95
EMPTY_DEFAULTS["social_charges_rate"] = 0.33
EMPTY_DEFAULTS["rent_per_m2_month"] = 0.0
EMPTY_DEFAULTS["racking_cost_ppl"] = 30.0

# ─────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────
def init_state():
    if "d" not in st.session_state:
        st.session_state.d = deepcopy(OCP_DEFAULTS)
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "preset" not in st.session_state:
        st.session_state.preset = "OCP Morocco (défaut)"

init_state()
d = st.session_state.d

# ─────────────────────────────────────────────────────────
# CORE CALCULATIONS
# ─────────────────────────────────────────────────────────
def calc_all(d):
    r = {}

    # ── Entrepôt ──
    net_locations = d["total_locations"] * d["target_utilization"]
    r["net_locations"] = net_locations
    volume_m3 = d["warehouse_area_m2"] * d["warehouse_height_m"]
    r["volume_m3"] = volume_m3

    # Coût entrepôt annuel = loyer/m²/mois * 12 * surface + racks + sécurité + câblage
    rent_year = d["rent_per_m2_month"] * 12 * d["warehouse_area_m2"]
    racking_invest = d["racking_cost_ppl"] * d["total_locations"]
    racking_annual = racking_invest * (d["interest_rate"] + 1/12)  # annuité simplifiée
    safety_invest = d["warehouse_area_m2"] * 12
    safety_annual = safety_invest * (d["interest_rate"] + 1/10)
    cabling_invest = d["warehouse_area_m2"] * 10.5
    cabling_annual = cabling_invest * (d["interest_rate"] + 1/5)
    warehouse_cost_total = rent_year + racking_annual + safety_annual + cabling_annual
    r["warehouse_cost_total"] = warehouse_cost_total
    r["rent_year"] = rent_year
    r["racking_annual"] = racking_annual

    # Coût net par emplacement/mois
    cost_per_location_month = warehouse_cost_total / 12 / max(net_locations, 1)
    r["cost_per_location_month"] = cost_per_location_month

    # ── Personnel ──
    def emp_cost(qty, salary):
        if qty == 0: return 0
        gross = salary * qty
        social = gross * d["social_charges_rate"]
        return gross + social

    personnel_costs = {
        "Cariste": emp_cost(d["forklift_driver"], d["salary_forklift"]),
        "Chargeur": emp_cost(d["loader"], d["salary_loader"]),
        "Déchargeur": emp_cost(d["unloader"], d["salary_unloader"]),
        "Contrôleur réception": emp_cost(d["inbound_controller"], d["salary_controller"]),
        "Administration réception": emp_cost(d["inbound_admin"], d["salary_admin"]),
        "Préparateur commandes": emp_cost(d["picker"], d["salary_picker"]),
        "Coordinateur équipe": emp_cost(d["team_coordinator"], d["salary_coordinator"]),
        "Chef d'équipe": emp_cost(d["shift_leader"], d["salary_shift_leader"]),
        "Responsable entrepôt": emp_cost(d["warehouse_manager"], d["salary_manager"]),
        "Admin sortie": emp_cost(d["outbound_admin"], d["salary_admin"]),
    }
    total_pers_cost = sum(personnel_costs.values())
    total_fte = (d["forklift_driver"] + d["loader"] + d["unloader"] +
                 d["inbound_controller"] + d["inbound_admin"] + d["picker"] +
                 d["team_coordinator"] + d["shift_leader"] + d["warehouse_manager"] +
                 d["outbound_admin"])
    r["personnel_costs"] = personnel_costs
    r["total_pers_cost"] = total_pers_cost
    r["total_fte"] = total_fte

    # ── Engins ──
    truck_costs = {
        "Fast Mover": d["fast_mover_qty"] * d["fast_mover_price"],
        "Reach Truck ≤8m": d["reach_truck_8m_qty"] * d["reach_truck_8m_price"],
        "Reach Truck >8m": d["reach_truck_gt8m_qty"] * d["reach_truck_gt8m_price"],
        "Transpalette manuel": d["hand_pallet_qty"] * d["hand_pallet_price"],
        "Chariot frontal": d["front_loader_qty"] * d["front_loader_price"],
        "Préparateur horizontal": d["order_picker_qty"] * d["order_picker_price"],
        "Chariot allée étroite": d["narrow_aisle_qty"] * d["narrow_aisle_price"],
    }
    total_truck_cost = sum(truck_costs.values())
    r["truck_costs"] = truck_costs
    r["total_truck_cost"] = total_truck_cost

    # ── Processus variables ──
    # Temps process estimé = ETP opérationnel * jours * 8h * productivité
    # Coût à l'unité = coût personnel opérationnel / volume
    op_fte = (d["forklift_driver"] + d["loader"] + d["unloader"] +
              d["inbound_controller"] + d["picker"])
    op_pers_cost = sum([
        personnel_costs["Cariste"], personnel_costs["Chargeur"],
        personnel_costs["Déchargeur"], personnel_costs["Contrôleur réception"],
        personnel_costs["Préparateur commandes"],
    ])
    admin_pers_cost = total_pers_cost - op_pers_cost

    # Attribution des coûts aux processus
    inbound_vol = max(d["inbound_pallets_year"], 1)
    outbound_vol = max(d["outbound_pallets_year"], 1)
    total_vol = inbound_vol + outbound_vol

    # Part inbound/outbound
    inbound_share = inbound_vol / total_vol if total_vol > 0 else 0.5
    outbound_share = outbound_vol / total_vol if total_vol > 0 else 0.5

    # Coût process inbound = part variable selon volume
    inbound_proc_cost = (op_pers_cost + total_truck_cost * inbound_share) * inbound_share
    outbound_proc_cost = (op_pers_cost + total_truck_cost * outbound_share) * outbound_share

    # Coût unitaire par palette
    cost_per_inbound_pallet = inbound_proc_cost / inbound_vol
    cost_per_outbound_pallet = outbound_proc_cost / outbound_vol
    r["inbound_proc_cost"] = inbound_proc_cost
    r["outbound_proc_cost"] = outbound_proc_cost
    r["cost_per_inbound_pallet"] = cost_per_inbound_pallet
    r["cost_per_outbound_pallet"] = cost_per_outbound_pallet

    # ── Coûts IT & autres fixes ──
    it_alloc = total_pers_cost * d["allocation_wms_pct"]
    r["it_cost_total"] = d["it_costs_year"] + it_alloc

    # ── TOTAL COÛTS ──
    total_costs = (warehouse_cost_total + total_pers_cost +
                   total_truck_cost + d["it_costs_year"] +
                   d["other_fixed_costs"])
    # Allocation HO/RHO (approximée à 1.3% + 31.9% pers. admin)
    r["total_costs"] = total_costs

    # ── TARIFS RECOMMANDÉS ──
    # Formule : Prix = Coût_unitaire / (1 - marge_cible)
    margin = d["target_margin"]

    # Entreposage
    wh_cost_per_loc_year = warehouse_cost_total / max(d["storage_locations_sold"], 1)
    price_storage = wh_cost_per_loc_year / (1 - margin)
    r["price_storage_per_loc_year"] = price_storage
    r["price_storage_per_loc_month"] = price_storage / 12
    r["wh_cost_per_loc_year"] = wh_cost_per_loc_year

    # Entrées marchandises
    price_inbound = cost_per_inbound_pallet / (1 - margin) if inbound_vol > 0 else 0
    r["price_inbound_pallet"] = price_inbound
    r["price_inbound_pallet_min"] = cost_per_inbound_pallet
    r["price_inbound_pallet_max"] = price_inbound * 1.15

    # Sorties marchandises
    price_outbound = cost_per_outbound_pallet / (1 - margin) if outbound_vol > 0 else 0
    r["price_outbound_pallet"] = price_outbound
    r["price_outbound_pallet_min"] = cost_per_outbound_pallet
    r["price_outbound_pallet_max"] = price_outbound * 1.15

    # ── CHIFFRE D'AFFAIRES SIMULÉ ──
    ca_storage = d["storage_locations_sold"] * price_storage
    ca_inbound = d["inbound_pallets_year"] * price_inbound
    ca_outbound = d["outbound_pallets_year"] * price_outbound
    ca_total = ca_storage + ca_inbound + ca_outbound
    r["ca_storage"] = ca_storage
    r["ca_inbound"] = ca_inbound
    r["ca_outbound"] = ca_outbound
    r["ca_total"] = ca_total

    # ── PROFIT & MARGE ──
    profit = ca_total - total_costs
    margin_pct = profit / ca_total if ca_total > 0 else 0
    r["profit"] = profit
    r["margin_pct"] = margin_pct

    # ── SENSIBILITÉ ──
    # Impact +/-10% volume sur marge
    ca_vol_plus10 = (d["storage_locations_sold"] * price_storage +
                     d["inbound_pallets_year"] * 1.1 * price_inbound +
                     d["outbound_pallets_year"] * 1.1 * price_outbound)
    ca_vol_minus10 = (d["storage_locations_sold"] * price_storage +
                      d["inbound_pallets_year"] * 0.9 * price_inbound +
                      d["outbound_pallets_year"] * 0.9 * price_outbound)
    r["profit_vol_plus10"] = ca_vol_plus10 - total_costs
    r["profit_vol_minus10"] = ca_vol_minus10 - total_costs
    r["margin_vol_plus10"] = r["profit_vol_plus10"] / ca_vol_plus10 if ca_vol_plus10 > 0 else 0
    r["margin_vol_minus10"] = r["profit_vol_minus10"] / ca_vol_minus10 if ca_vol_minus10 > 0 else 0

    # Impact +/-5% salaires
    cost_sal_plus5 = total_costs + total_pers_cost * 0.05
    cost_sal_minus5 = total_costs - total_pers_cost * 0.05
    r["margin_sal_plus5"] = (ca_total - cost_sal_plus5) / ca_total if ca_total > 0 else 0
    r["margin_sal_minus5"] = (ca_total - cost_sal_minus5) / ca_total if ca_total > 0 else 0

    # Seuil de rentabilité
    fixed_costs = warehouse_cost_total + admin_pers_cost + d["it_costs_year"] + d["other_fixed_costs"]
    variable_margin_rate = (ca_inbound + ca_outbound - op_pers_cost - total_truck_cost) / (ca_inbound + ca_outbound) if (ca_inbound + ca_outbound) > 0 else 0
    r["breakeven_ca"] = fixed_costs / variable_margin_rate if variable_margin_rate > 0 else 0
    r["fixed_costs"] = fixed_costs

    return r

# ─────────────────────────────────────────────────────────
# SIDEBAR — Navigation & preset
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 12px;'>
      <div style='font-size:28px;'>📦</div>
      <div style='font-size:16px;font-weight:700;color:#e8eaf6;'>Polka Wizard</div>
      <div style='font-size:11px;color:#7b82a8;'>Tarification Logistique</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Preset selector
    preset = st.radio("🗂️ Données de départ", [
        "OCP Morocco (défaut)",
        "Nouveau projet (vierge)"
    ], key="preset_radio")

    if preset != st.session_state.get("preset"):
        st.session_state.preset = preset
        if preset == "OCP Morocco (défaut)":
            st.session_state.d = deepcopy(OCP_DEFAULTS)
        else:
            st.session_state.d = deepcopy(EMPTY_DEFAULTS)
        st.rerun()

    st.divider()

    # Steps navigation
    st.markdown("**📋 Étapes du wizard**")
    steps = [
        ("1", "Projet & Entrepôt"),
        ("2", "Personnel"),
        ("3", "Engins"),
        ("4", "Volumes & Processus"),
        ("5", "Calcul des Tarifs"),
        ("6", "Analyse de Sensibilité"),
    ]
    for num, label in steps:
        active = st.session_state.step == int(num)
        color = "#4f7cff" if active else "#7b82a8"
        bg = "rgba(79,124,255,0.1)" if active else "transparent"
        st.markdown(f"""
        <div style='padding:8px 10px;border-radius:8px;background:{bg};
             border-left:3px solid {color};margin:4px 0;cursor:pointer;'>
          <span style='color:{color};font-weight:{"700" if active else "400"};font-size:13px;'>
            {'▶ ' if active else '  '}{num}. {label}
          </span>
        </div>""", unsafe_allow_html=True)
        if st.button(f"→ {label}", key=f"nav_{num}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.step = int(num)
            st.rerun()

    st.divider()

    # Quick summary
    try:
        res = calc_all(st.session_state.d)
        st.markdown("**📊 Résumé rapide**")
        m_color = "#22d3a0" if res["margin_pct"] >= 0.08 else "#ff5c6a"
        st.markdown(f"""
        <div style='font-size:12px;'>
          <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2e3250;'>
            <span style='color:#7b82a8;'>CA estimé</span>
            <span style='font-weight:700;color:#4f7cff;'>{res['ca_total']:,.0f} €</span>
          </div>
          <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #2e3250;'>
            <span style='color:#7b82a8;'>Coûts totaux</span>
            <span style='font-weight:700;color:#ffb547;'>{res['total_costs']:,.0f} €</span>
          </div>
          <div style='display:flex;justify-content:space-between;padding:4px 0;'>
            <span style='color:#7b82a8;'>Marge</span>
            <span style='font-weight:700;color:{m_color};'>{res['margin_pct']:.1%}</span>
          </div>
        </div>""", unsafe_allow_html=True)
    except:
        pass

# ─────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────
def fmt_eur(v):
    return f"{v:,.2f} €"

def fmt_k(v):
    return f"{v/1000:,.1f}k €"

def nav_buttons(step):
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if step > 1:
            if st.button("← Précédent", use_container_width=True):
                st.session_state.step = step - 1
                st.rerun()
    with col3:
        if step < 6:
            if st.button("Suivant →", type="primary", use_container_width=True):
                st.session_state.step = step + 1
                st.rerun()
        else:
            if st.button("🔄 Recommencer", use_container_width=True):
                st.session_state.step = 1
                st.rerun()

# ─────────────────────────────────────────────────────────
# STEP 1 — PROJET & ENTREPÔT
# ─────────────────────────────────────────────────────────
if st.session_state.step == 1:
    st.markdown("""
    <div class='step-header'>
      <div class='step-number'>ÉTAPE 1 / 6</div>
      <div class='step-title'>🏭 Données Projet & Entrepôt</div>
      <div class='step-desc'>Renseignez les informations de base du projet et les caractéristiques physiques de l'entrepôt.</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏢 Informations du projet")
        d["project_name"] = st.text_input("Nom du projet / Client", value=d["project_name"])
        d["project_leader"] = st.text_input("Chef de projet", value=d["project_leader"])
        d["site"] = st.text_input("Site / Agence", value=d["site"])
        d["country"] = st.text_input("Pays", value=d["country"])
        d["wms"] = st.text_input("Système WMS", value=d["wms"])

        st.markdown("#### ⚙️ Paramètres financiers")
        d["working_days"] = st.number_input("Jours ouvrés / an", min_value=200, max_value=365,
                                              value=int(d["working_days"]), step=1)
        d["interest_rate"] = st.number_input("Taux d'intérêt interne (%)", min_value=0.0, max_value=0.3,
                                               value=float(d["interest_rate"]), step=0.005, format="%.3f")
        d["target_margin"] = st.slider("🎯 Marge cible (%)", min_value=0.0, max_value=0.3,
                                        value=float(d["target_margin"]), step=0.005, format="%.1%")
        d["op_reserve"] = st.number_input("Réserve opérationnelle (%)", min_value=0.0, max_value=0.3,
                                           value=float(d["op_reserve"]), step=0.01, format="%.2f")
        d["social_charges_rate"] = st.number_input("Taux charges sociales (%)", min_value=0.0, max_value=0.8,
                                                    value=float(d["social_charges_rate"]), step=0.01, format="%.2f")

    with col2:
        st.markdown("#### 📐 Caractéristiques entrepôt")
        d["warehouse_area_m2"] = st.number_input("Surface totale (m²)", min_value=0.0, max_value=100000.0,
                                                   value=float(d["warehouse_area_m2"]), step=10.0)
        d["warehouse_height_m"] = st.number_input("Hauteur (m)", min_value=3.0, max_value=30.0,
                                                    value=float(d["warehouse_height_m"]), step=0.5)
        d["total_locations"] = st.number_input("Emplacements palettes (brut)", min_value=0, max_value=100000,
                                                value=int(d["total_locations"]), step=10)
        d["target_utilization"] = st.slider("Taux d'utilisation cible (%)", min_value=0.5, max_value=1.0,
                                             value=float(d["target_utilization"]), step=0.01, format="%.0%")

        net_loc = int(d["total_locations"] * d["target_utilization"])
        st.markdown(f"""
        <div class='result-block'>
          <div style='font-size:12px;color:#7b82a8;'>→ Emplacements nets utilisables</div>
          <div style='font-size:22px;font-weight:800;color:#22d3a0;'>{net_loc:,}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("#### 💰 Coûts immobiliers")
        d["rent_per_m2_month"] = st.number_input("Loyer / m² / mois (€)", min_value=0.0, max_value=50.0,
                                                   value=float(d["rent_per_m2_month"]), step=0.1, format="%.3f")
        d["racking_cost_ppl"] = st.number_input("Coût racks / emplacement palette (€ achat)", min_value=0.0,
                                                  max_value=500.0, value=float(d["racking_cost_ppl"]), step=5.0)
        d["allocation_wms_pct"] = st.number_input("Allocation WMS + Innovation Fund (%)", min_value=0.0,
                                                    max_value=0.1, value=float(d["allocation_wms_pct"]),
                                                    step=0.001, format="%.3f")

        # Preview coût entrepôt
        rent_y = d["rent_per_m2_month"] * 12 * d["warehouse_area_m2"]
        rack_y = d["racking_cost_ppl"] * d["total_locations"] * (d["interest_rate"] + 1/12)
        wh_total = rent_y + rack_y
        st.markdown(f"""
        <div class='result-block'>
          <div style='font-size:12px;color:#7b82a8;'>→ Estimation coût entrepôt annuel</div>
          <div style='font-size:20px;font-weight:800;color:#4f7cff;'>{wh_total:,.0f} €</div>
          <div style='font-size:11px;color:#7b82a8;'>Loyer : {rent_y:,.0f} € · Racks : {rack_y:,.0f} €</div>
        </div>""", unsafe_allow_html=True)

    nav_buttons(1)

# ─────────────────────────────────────────────────────────
# STEP 2 — PERSONNEL
# ─────────────────────────────────────────────────────────
elif st.session_state.step == 2:
    st.markdown("""
    <div class='step-header'>
      <div class='step-number'>ÉTAPE 2 / 6</div>
      <div class='step-title'>👷 Cockpit Personnel</div>
      <div class='step-desc'>Définissez les effectifs (ETP) et les salaires annuels bruts par poste.</div>
    </div>""", unsafe_allow_html=True)

    STAFF = [
        ("forklift_driver", "salary_forklift", "🚛 Cariste (Forklift driver)", "Opérationnel"),
        ("loader", "salary_loader", "📦 Chargeur (Loader)", "Opérationnel"),
        ("unloader", "salary_unloader", "📥 Déchargeur (Unloader)", "Opérationnel"),
        ("inbound_controller", "salary_controller", "🔍 Contrôleur réception (Inbound controller)", "Opérationnel"),
        ("picker", "salary_picker", "🛒 Préparateur commandes (Picker)", "Opérationnel"),
        ("inbound_admin", "salary_admin", "📋 Administration réception", "Administratif"),
        ("outbound_admin", "salary_admin", "📤 Administration expédition", "Administratif"),
        ("team_coordinator", "salary_coordinator", "👥 Coordinateur équipe", "Encadrement"),
        ("shift_leader", "salary_shift_leader", "🔧 Chef d'équipe (Shift Leader)", "Encadrement"),
        ("warehouse_manager", "salary_manager", "🏆 Responsable entrepôt", "Management"),
    ]

    st.markdown("#### Effectifs & Salaires par poste")
    st.caption("ETP = Équivalent Temps Plein · Les coûts incluent les charges sociales")

    total_fte_preview = 0
    total_cost_preview = 0

    for fte_key, sal_key, label, cat in STAFF:
        with st.expander(f"{label}  —  {'🟢' if d[fte_key] > 0 else '⚫'}  {d[fte_key]} ETP", expanded=d[fte_key] > 0):
            c1, c2, c3 = st.columns([2, 2, 2])
            with c1:
                d[fte_key] = st.number_input(f"ETP alloués", min_value=0.0, max_value=50.0,
                                              value=float(d[fte_key]), step=0.1,
                                              key=f"fte_{fte_key}", format="%.2f")
            with c2:
                d[sal_key] = st.number_input(f"Salaire brut annuel (€)", min_value=0, max_value=200000,
                                              value=int(d[sal_key]), step=500,
                                              key=f"sal_{sal_key}_{fte_key}")
            with c3:
                cost_emp = d[fte_key] * d[sal_key] * (1 + d["social_charges_rate"])
                st.metric(f"Coût total ({cat})", f"{cost_emp:,.0f} €")
            total_fte_preview += d[fte_key]
            total_cost_preview += d[fte_key] * d[sal_key] * (1 + d["social_charges_rate"])

    # Summary
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("👷 Effectif total", f"{total_fte_preview:.2f} ETP")
    with c2:
        st.metric("💰 Coût personnel annuel", f"{total_cost_preview:,.0f} €")
    with c3:
        st.metric("💰 Coût par ETP/an", f"{total_cost_preview/max(total_fte_preview,1):,.0f} €")
    with c4:
        cost_per_day = total_cost_preview / max(d["working_days"], 1)
        st.metric("📅 Coût/jour ouvré", f"{cost_per_day:,.0f} €")

    if total_fte_preview == 0:
        st.markdown("<div class='warn-box'>⚠️ Aucun effectif renseigné — les coûts personnel seront nuls.</div>",
                    unsafe_allow_html=True)

    nav_buttons(2)

# ─────────────────────────────────────────────────────────
# STEP 3 — ENGINS
# ─────────────────────────────────────────────────────────
elif st.session_state.step == 3:
    st.markdown("""
    <div class='step-header'>
      <div class='step-number'>ÉTAPE 3 / 6</div>
      <div class='step-title'>🏗️ Cockpit Engins de Manutention</div>
      <div class='step-desc'>Définissez le parc d'engins, les quantités allouées et leurs coûts annuels (location ou amortissement).</div>
    </div>""", unsafe_allow_html=True)

    TRUCKS = [
        ("fast_mover_qty", "fast_mover_price", "⚡ Fast Mover", "Location", "Chariot rapide pour opérations courantes", "FG0025"),
        ("reach_truck_8m_qty", "reach_truck_8m_price", "🔼 Reach Truck ≤ 8m", "Location", "Chariot élévateur pour racks standards", "FG0030"),
        ("reach_truck_gt8m_qty", "reach_truck_gt8m_price", "🔝 Reach Truck > 8m", "Location", "Chariot grande hauteur (>8m)", "FG0030"),
        ("hand_pallet_qty", "hand_pallet_price", "🤲 Transpalette manuel", "Achat", "Manutention simple au sol", "FG0010"),
        ("front_loader_qty", "front_loader_price", "🔄 Chariot frontal", "Location", "Chargement / déchargement camions", "FG0030"),
        ("order_picker_qty", "order_picker_price", "📋 Préparateur horizontal", "Location", "Préparation de commandes au sol", "FG0020"),
        ("narrow_aisle_qty", "narrow_aisle_price", "↔️ Chariot allée étroite", "Location", "Densification stockage allées étroites", "FG0030"),
    ]

    total_trucks_preview = 0
    total_truck_cost_preview = 0

    for qty_key, price_key, label, mode, desc, group in TRUCKS:
        with st.expander(f"{label}  —  {'🟢' if d[qty_key] > 0 else '⚫'}  {d[qty_key]} unités", expanded=d[qty_key] > 0):
            st.caption(f"_{desc}_ · Mode : {mode}")
            c1, c2, c3 = st.columns([2, 2, 2])
            with c1:
                d[qty_key] = st.number_input("Quantité allouée", min_value=0.0, max_value=50.0,
                                              value=float(d[qty_key]), step=0.1,
                                              key=f"trk_{qty_key}", format="%.2f")
            with c2:
                label_price = f"Coût annuel par unité (€) · {mode}"
                d[price_key] = st.number_input(label_price, min_value=0, max_value=500000,
                                                value=int(d[price_key]), step=100,
                                                key=f"tp_{price_key}_{qty_key}")
            with c3:
                cost = d[qty_key] * d[price_key]
                st.metric("Coût total annuel", f"{cost:,.0f} €")
            total_trucks_preview += d[qty_key]
            total_truck_cost_preview += d[qty_key] * d[price_key]

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🏗️ Parc total", f"{total_trucks_preview:.2f} engins")
    with c2:
        st.metric("💰 Coût engins annuel", f"{total_truck_cost_preview:,.0f} €")
    with c3:
        st.metric("💰 Coût moyen / engin", f"{total_truck_cost_preview/max(total_trucks_preview,1):,.0f} €")

    # Taux de panne
    st.markdown("#### 🔧 Paramètres de maintenance")
    c1, c2 = st.columns(2)
    with c1:
        d["equip_failure_rate"] = st.number_input("Taux de défaillance équipements (%)",
                                                    min_value=0.0, max_value=0.3,
                                                    value=float(d["equip_failure_rate"]),
                                                    step=0.01, format="%.2f")
    with c2:
        d["li_batteries"] = st.checkbox("Batteries lithium-ion (LI) pour chariots électriques",
                                         value=bool(d["li_batteries"]))
    if d["li_batteries"]:
        st.markdown("<div class='ok-box'>✓ Batteries LI activées — coûts de recharge réduits</div>",
                    unsafe_allow_html=True)

    nav_buttons(3)

# ─────────────────────────────────────────────────────────
# STEP 4 — VOLUMES & PROCESSUS
# ─────────────────────────────────────────────────────────
elif st.session_state.step == 4:
    st.markdown("""
    <div class='step-header'>
      <div class='step-number'>ÉTAPE 4 / 6</div>
      <div class='step-title'>📊 Volumes & Processus Logistiques</div>
      <div class='step-desc'>Renseignez les volumes annuels par processus — ils servent de base au calcul des tarifs unitaires.</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📦 Volumes de stockage")
        d["storage_locations_sold"] = st.number_input("Emplacements palettes vendus (annuel)",
                                                        min_value=0, max_value=100000,
                                                        value=int(d["storage_locations_sold"]), step=10)
        net_loc = d["total_locations"] * d["target_utilization"]
        occ_rate = d["storage_locations_sold"] / max(net_loc, 1) * 100
        if occ_rate > 100:
            st.markdown(f"<div class='warn-box'>⚠️ Dépassement capacité ! {occ_rate:.1f}% > 100%</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ok-box'>✓ Occupation : {occ_rate:.1f}% des emplacements nets ({net_loc:.0f})</div>",
                        unsafe_allow_html=True)

        st.markdown("#### 🚛 Autres coûts fixes")
        d["it_costs_year"] = st.number_input("Coûts IT annuels (€)", min_value=0, max_value=500000,
                                              value=int(d["it_costs_year"]), step=100)
        d["other_fixed_costs"] = st.number_input("Autres coûts fixes annuels (€)", min_value=0,
                                                   max_value=500000, value=int(d["other_fixed_costs"]), step=100)

    with col2:
        st.markdown("#### 🔄 Flux entrants (Inbound)")
        d["inbound_pallets_year"] = st.number_input("Palettes mises en stock / an",
                                                      min_value=0, max_value=2000000,
                                                      value=int(d["inbound_pallets_year"]), step=100)
        d["inbound_loose_units"] = st.number_input("Unités vrac entrantes / an", min_value=0,
                                                    max_value=10000000, value=int(d["inbound_loose_units"]), step=100)

        st.markdown("#### 🔄 Flux sortants (Outbound)")
        d["outbound_pallets_year"] = st.number_input("Palettes complètes expédiées / an",
                                                       min_value=0, max_value=2000000,
                                                       value=int(d["outbound_pallets_year"]), step=100)
        d["outbound_loose_units"] = st.number_input("Unités vrac sortantes / an", min_value=0,
                                                     max_value=10000000, value=int(d["outbound_loose_units"]), step=100)
        d["trucks_loaded_year"] = st.number_input("Chargements camions / an", min_value=0,
                                                   max_value=100000, value=int(d["trucks_loaded_year"]), step=10)

    # Preview volumes
    st.divider()
    st.markdown("#### 📈 Résumé des volumes renseignés")
    total_inbound = d["inbound_pallets_year"] + d["inbound_loose_units"]
    total_outbound = d["outbound_pallets_year"] + d["outbound_loose_units"]

    vol_data = {
        "Processus": ["Stockage (emplacements)", "Entrées palettes", "Sorties palettes",
                       "Entrées vrac", "Sorties vrac", "Chargements camions"],
        "Volume annuel": [d["storage_locations_sold"], d["inbound_pallets_year"],
                           d["outbound_pallets_year"], d["inbound_loose_units"],
                           d["outbound_loose_units"], d["trucks_loaded_year"]],
        "Unité": ["Emplacements", "Palettes", "Palettes", "Unités", "Unités", "Camions"]
    }
    df_vol = pd.DataFrame(vol_data)
    df_vol = df_vol[df_vol["Volume annuel"] > 0]
    if not df_vol.empty:
        st.dataframe(df_vol, use_container_width=True, hide_index=True)

    # Palettes/jour
    if d["inbound_pallets_year"] > 0:
        ppp_day = d["inbound_pallets_year"] / d["working_days"]
        st.markdown(f"**→ Débit journalier estimé :** {ppp_day:.1f} palettes/jour en entrée · {d['outbound_pallets_year']/d['working_days']:.1f} palettes/jour en sortie")

    nav_buttons(4)

# ─────────────────────────────────────────────────────────
# STEP 5 — CALCUL DES TARIFS
# ─────────────────────────────────────────────────────────
elif st.session_state.step == 5:
    st.markdown("""
    <div class='step-header'>
      <div class='step-number'>ÉTAPE 5 / 6</div>
      <div class='step-title'>💶 Calcul Automatique des Tarifs</div>
      <div class='step-desc'>Tarifs recommandés calculés à partir de vos données — avec marge cible intégrée.</div>
    </div>""", unsafe_allow_html=True)

    res = calc_all(d)

    # ── KPIs principaux ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 CA estimé", f"{res['ca_total']:,.0f} €",
                  delta=f"Cible marge {d['target_margin']:.0%}")
    with col2:
        st.metric("💸 Coûts totaux", f"{res['total_costs']:,.0f} €")
    with col3:
        profit_delta = "✅" if res["margin_pct"] >= d["target_margin"] else "⚠️ Sous objectif"
        st.metric("💰 Bénéfice estimé", f"{res['profit']:,.0f} €", delta=profit_delta)
    with col4:
        m_color = "#22d3a0" if res["margin_pct"] >= d["target_margin"] else "#ff5c6a"
        st.metric("📊 Marge réelle", f"{res['margin_pct']:.2%}")

    # Alerte marge
    if res["margin_pct"] < d["target_margin"]:
        st.markdown(f"""
        <div class='warn-box'>
          ⚠️ La marge calculée ({res['margin_pct']:.2%}) est inférieure à l'objectif ({d['target_margin']:.0%}).
          Voir les suggestions d'optimisation ci-dessous.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='ok-box'>
          ✅ Objectif de marge atteint ! {res['margin_pct']:.2%} ≥ {d['target_margin']:.0%}
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── TARIFS RECOMMANDÉS ──
    st.markdown("### 💶 Tarifs recommandés")
    st.caption("Calculés sur la base : **Prix = Coût unitaire ÷ (1 − marge cible)**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""<div style='background:#0d1f3c;border:1px solid #1e3a6e;border-radius:12px;padding:18px;'>
        <div style='font-size:12px;color:#7b82a8;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:10px;'>🏭 Entreposage</div>""",
        unsafe_allow_html=True)

        price_s = st.number_input("Prix / emplacement / an (€)",
                                   min_value=0.0, max_value=1000.0,
                                   value=round(float(res["price_storage_per_loc_year"]), 2),
                                   step=0.1, key="price_storage_custom", format="%.2f")
        price_s_m = price_s / 12
        ca_s = d["storage_locations_sold"] * price_s
        cost_s = res["warehouse_cost_total"]
        margin_s = (ca_s - cost_s) / ca_s if ca_s > 0 else 0

        st.markdown(f"""
        <div style='font-size:12px;color:#7b82a8;margin-top:8px;'>→ {price_s_m:.2f} € / mois / emplacement</div>
        <div style='font-size:11px;color:#7b82a8;'>Coût min. recommandé : {res['wh_cost_per_loc_year']:,.2f} €/emp./an</div>
        <div style='font-size:14px;font-weight:700;margin-top:8px;color:{"#22d3a0" if margin_s >= 0 else "#ff5c6a"};'>
          CA : {ca_s:,.0f} € · Marge : {margin_s:.1%}
        </div></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div style='background:#0d1f3c;border:1px solid #1e3a6e;border-radius:12px;padding:18px;'>
        <div style='font-size:12px;color:#7b82a8;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:10px;'>📥 Entrées marchandises</div>""",
        unsafe_allow_html=True)

        price_i = st.number_input("Prix / palette entrante (€)",
                                   min_value=0.0, max_value=100.0,
                                   value=round(float(res["price_inbound_pallet"]), 3),
                                   step=0.01, key="price_inbound_custom", format="%.3f")
        ca_i = d["inbound_pallets_year"] * price_i
        cost_i = res["inbound_proc_cost"]
        margin_i = (ca_i - cost_i) / ca_i if ca_i > 0 else 0

        st.markdown(f"""
        <div style='font-size:11px;color:#7b82a8;margin-top:8px;'>
          Seuil min. : {res['price_inbound_pallet_min']:,.3f} €&nbsp;&nbsp;|&nbsp;&nbsp;Cible : {res['price_inbound_pallet']:,.3f} €
        </div>
        <div style='font-size:14px;font-weight:700;margin-top:8px;color:{"#22d3a0" if margin_i >= 0 else "#ff5c6a"};'>
          CA : {ca_i:,.0f} € · Marge : {margin_i:.1%}
        </div></div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div style='background:#0d1f3c;border:1px solid #1e3a6e;border-radius:12px;padding:18px;'>
        <div style='font-size:12px;color:#7b82a8;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:10px;'>📤 Sorties marchandises</div>""",
        unsafe_allow_html=True)

        price_o = st.number_input("Prix / palette sortante (€)",
                                   min_value=0.0, max_value=100.0,
                                   value=round(float(res["price_outbound_pallet"]), 3),
                                   step=0.01, key="price_outbound_custom", format="%.3f")
        ca_o = d["outbound_pallets_year"] * price_o
        cost_o = res["outbound_proc_cost"]
        margin_o = (ca_o - cost_o) / ca_o if ca_o > 0 else 0

        st.markdown(f"""
        <div style='font-size:11px;color:#7b82a8;margin-top:8px;'>
          Seuil min. : {res['price_outbound_pallet_min']:,.3f} €&nbsp;&nbsp;|&nbsp;&nbsp;Cible : {res['price_outbound_pallet']:,.3f} €
        </div>
        <div style='font-size:14px;font-weight:700;margin-top:8px;color:{"#22d3a0" if margin_o >= 0 else "#ff5c6a"};'>
          CA : {ca_o:,.0f} € · Marge : {margin_o:.1%}
        </div></div>""", unsafe_allow_html=True)

    st.divider()

    # ── DÉCOMPOSITION DES COÛTS ──
    st.markdown("### 🧩 Décomposition des coûts")
    cost_detail = pd.DataFrame({
        "Poste de coût": ["Entrepôt (loyer + racks)", "Personnel", "Engins de manutention",
                           "IT & WMS", "Autres coûts fixes"],
        "Montant annuel (€)": [round(res["warehouse_cost_total"]), round(res["total_pers_cost"]),
                                round(res["total_truck_cost"]), round(res["it_cost_total"]),
                                d["other_fixed_costs"]],
        "Part (%)": [
            res["warehouse_cost_total"]/max(res["total_costs"],1)*100,
            res["total_pers_cost"]/max(res["total_costs"],1)*100,
            res["total_truck_cost"]/max(res["total_costs"],1)*100,
            res["it_cost_total"]/max(res["total_costs"],1)*100,
            d["other_fixed_costs"]/max(res["total_costs"],1)*100,
        ]
    })
    cost_detail["Part (%)"] = cost_detail["Part (%)"].map(lambda x: f"{x:.1f}%")
    cost_detail["Montant annuel (€)"] = cost_detail["Montant annuel (€)"].map(lambda x: f"{x:,}")
    st.dataframe(cost_detail, use_container_width=True, hide_index=True)

    # ── TARIFS CUSTOM vs OCP ──
    if st.session_state.preset == "OCP Morocco (défaut)":
        st.markdown("### 🔄 Comparaison avec tarifs OCP réels")
        cmp = pd.DataFrame({
            "Prestation": ["Entreposage / emp. / an", "Entrée palette", "Sortie palette"],
            "Tarif OCP réel (€)": [f"{6.58*12:.2f}", "2.562", "2.929"],
            "Tarif calculé (€)": [
                f"{res['price_storage_per_loc_year']:.2f}",
                f"{res['price_inbound_pallet']:.3f}",
                f"{res['price_outbound_pallet']:.3f}",
            ],
            "Écart": [
                f"{res['price_storage_per_loc_year'] - 6.58*12:+.2f} €",
                f"{res['price_inbound_pallet'] - 2.562:+.3f} €",
                f"{res['price_outbound_pallet'] - 2.929:+.3f} €",
            ]
        })
        st.dataframe(cmp, use_container_width=True, hide_index=True)

    # ── SUGGESTIONS D'OPTIMISATION ──
    if res["margin_pct"] < d["target_margin"]:
        gap = (d["target_margin"] - res["margin_pct"]) * res["ca_total"]
        st.markdown("### 💡 Suggestions pour atteindre la marge cible")
        st.markdown(f"""
        <div class='warn-box'>
          Manque à gagner : <strong>{gap:,.0f} €</strong> pour atteindre {d['target_margin']:.0%} de marge.<br><br>
          <strong>Options d'optimisation :</strong><br>
          • Augmenter le tarif d'entreposage de {gap/max(d['storage_locations_sold'],1):.2f} €/emp./an<br>
          • Ou augmenter le tarif palette entrante de {gap/max(d['inbound_pallets_year'],1):.3f} €/palette<br>
          • Ou réduire les coûts personnel de {gap/max(res['total_pers_cost'],1)*100:.1f}%<br>
          • Ou combiner les trois leviers proportionnellement
        </div>""", unsafe_allow_html=True)

    nav_buttons(5)

# ─────────────────────────────────────────────────────────
# STEP 6 — ANALYSE DE SENSIBILITÉ
# ─────────────────────────────────────────────────────────
elif st.session_state.step == 6:
    st.markdown("""
    <div class='step-header'>
      <div class='step-number'>ÉTAPE 6 / 6</div>
      <div class='step-title'>📉 Analyse de Sensibilité & Scénarios</div>
      <div class='step-desc'>Simulez l'impact de variations sur vos résultats financiers — marge, rentabilité, seuil.</div>
    </div>""", unsafe_allow_html=True)

    res = calc_all(d)

    # ── TABLEAU DE SENSIBILITÉ ──
    st.markdown("### 📊 Impact des variables sur la marge")

    variations = [-20, -15, -10, -5, 0, +5, +10, +15, +20]
    sens_rows = []
    for v in variations:
        factor = 1 + v/100
        # Volumes
        d_vol = deepcopy(d)
        d_vol["inbound_pallets_year"] = int(d["inbound_pallets_year"] * factor)
        d_vol["outbound_pallets_year"] = int(d["outbound_pallets_year"] * factor)
        r_vol = calc_all(d_vol)

        # Salaires
        d_sal = deepcopy(d)
        for sk in ["salary_forklift","salary_loader","salary_unloader","salary_controller",
                   "salary_admin","salary_picker","salary_coordinator","salary_shift_leader","salary_manager"]:
            d_sal[sk] = int(d[sk] * factor)
        r_sal = calc_all(d_sal)

        # Loyer
        d_rent = deepcopy(d)
        d_rent["rent_per_m2_month"] = d["rent_per_m2_month"] * factor
        r_rent = calc_all(d_rent)

        sens_rows.append({
            "Variation": f"{v:+d}%",
            "Marge (volumes)": f"{r_vol['margin_pct']:.2%}",
            "Profit (volumes) €": f"{r_vol['profit']:,.0f}",
            "Marge (salaires)": f"{r_sal['margin_pct']:.2%}",
            "Profit (salaires) €": f"{r_sal['profit']:,.0f}",
            "Marge (loyer)": f"{r_rent['margin_pct']:.2%}",
            "Profit (loyer) €": f"{r_rent['profit']:,.0f}",
        })

    df_sens = pd.DataFrame(sens_rows)
    st.dataframe(df_sens, use_container_width=True, hide_index=True)

    st.divider()

    # ── SCÉNARIOS CUSTOM ──
    st.markdown("### 🎛️ Simulateur de scénarios")
    st.caption("Modifiez les paramètres ci-dessous pour simuler un scénario spécifique")

    c1, c2, c3 = st.columns(3)
    with c1:
        sim_vol_pct = st.slider("📦 Variation volumes (%)", -50, 50, 0, 5)
    with c2:
        sim_sal_pct = st.slider("👷 Variation salaires (%)", -30, 50, 0, 5)
    with c3:
        sim_rent_pct = st.slider("🏭 Variation loyer (%)", -50, 100, 0, 5)

    d_sim = deepcopy(d)
    d_sim["inbound_pallets_year"] = int(d["inbound_pallets_year"] * (1 + sim_vol_pct/100))
    d_sim["outbound_pallets_year"] = int(d["outbound_pallets_year"] * (1 + sim_vol_pct/100))
    d_sim["rent_per_m2_month"] = d["rent_per_m2_month"] * (1 + sim_rent_pct/100)
    for sk in ["salary_forklift","salary_loader","salary_unloader","salary_controller",
               "salary_admin","salary_picker","salary_coordinator","salary_shift_leader","salary_manager"]:
        d_sim[sk] = int(d[sk] * (1 + sim_sal_pct/100))

    r_sim = calc_all(d_sim)
    r_base = calc_all(d)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        delta_ca = r_sim["ca_total"] - r_base["ca_total"]
        st.metric("CA Simulé", f"{r_sim['ca_total']:,.0f} €", delta=f"{delta_ca:+,.0f} €")
    with col2:
        delta_cost = r_sim["total_costs"] - r_base["total_costs"]
        st.metric("Coûts Simulés", f"{r_sim['total_costs']:,.0f} €", delta=f"{delta_cost:+,.0f} €", delta_color="inverse")
    with col3:
        delta_profit = r_sim["profit"] - r_base["profit"]
        st.metric("Bénéfice Simulé", f"{r_sim['profit']:,.0f} €", delta=f"{delta_profit:+,.0f} €")
    with col4:
        delta_margin = r_sim["margin_pct"] - r_base["margin_pct"]
        st.metric("Marge Simulée", f"{r_sim['margin_pct']:.2%}", delta=f"{delta_margin:+.2%}")

    m_color = "#22d3a0" if r_sim["margin_pct"] >= d["target_margin"] else "#ff5c6a"
    status = "✅ Objectif atteint" if r_sim["margin_pct"] >= d["target_margin"] else f"⚠️ Manque {(d['target_margin']-r_sim['margin_pct'])*r_sim['ca_total']:,.0f} €"
    st.markdown(f"<div class='result-block'><span style='font-size:14px;color:{m_color};font-weight:700;'>{status}</span></div>",
                unsafe_allow_html=True)

    st.divider()

    # ── SEUIL DE RENTABILITÉ ──
    st.markdown("### 📍 Seuil de rentabilité (Point mort)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CA seuil", f"{res['breakeven_ca']:,.0f} €",
                  help="CA minimum pour couvrir tous les coûts fixes")
    with col2:
        st.metric("CA actuel", f"{res['ca_total']:,.0f} €")
    with col3:
        cushion = (res["ca_total"] - res["breakeven_ca"]) / max(res["ca_total"],1) * 100
        st.metric("Marge de sécurité", f"{cushion:.1f}%",
                  delta="✅ Solide" if cushion > 20 else "⚠️ Faible")

    st.divider()

    # ── EXPORT RÉSUMÉ ──
    st.markdown("### 📤 Export du résumé")
    summary = {
        "Projet": d["project_name"],
        "Site": d["site"],
        "CA annuel estimé": round(res["ca_total"], 2),
        "Coûts totaux": round(res["total_costs"], 2),
        "Bénéfice": round(res["profit"], 2),
        "Marge (%)": round(res["margin_pct"] * 100, 2),
        "Prix entreposage / emp. / an": round(res["price_storage_per_loc_year"], 2),
        "Prix entrée palette": round(res["price_inbound_pallet"], 3),
        "Prix sortie palette": round(res["price_outbound_pallet"], 3),
        "Effectifs totaux (ETP)": round(res["total_fte"], 2),
        "Coût personnel total": round(res["total_pers_cost"], 2),
        "Coût engins total": round(res["total_truck_cost"], 2),
        "Coût entrepôt total": round(res["warehouse_cost_total"], 2),
    }
    summary_json = json.dumps(summary, indent=2, ensure_ascii=False)
    st.download_button(
        label="⬇️ Télécharger le résumé JSON",
        data=summary_json,
        file_name=f"polka_tarifs_{d['project_name'].replace(' ','_') or 'projet'}.json",
        mime="application/json",
        type="primary"
    )

    # CSV cost breakdown
    rows_csv = [
        ["Poste", "Montant (€)"],
        ["Loyer entrepôt", round(res["rent_year"])],
        ["Racks & aménagement", round(res["racking_annual"])],
        ["Personnel total", round(res["total_pers_cost"])],
        ["Engins manutention", round(res["total_truck_cost"])],
        ["IT & WMS", round(res["it_cost_total"])],
        ["Autres fixes", d["other_fixed_costs"]],
        ["TOTAL COÛTS", round(res["total_costs"])],
        ["CA estimé", round(res["ca_total"])],
        ["BÉNÉFICE", round(res["profit"])],
        ["MARGE %", f"{res['margin_pct']:.2%}"],
    ]
    csv_str = "\n".join([";".join(map(str, r)) for r in rows_csv])
    st.download_button(
        label="⬇️ Télécharger la décomposition CSV",
        data=csv_str,
        file_name=f"polka_couts_{d['project_name'].replace(' ','_') or 'projet'}.csv",
        mime="text/csv"
    )

    nav_buttons(6)

# ─────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:20px 0 10px;color:#4a5178;font-size:12px;border-top:1px solid #2e3250;margin-top:30px;'>
  Polka Wizard · Basé sur Polka V202541 · OCP Morocco · Contract Logistics
</div>
""", unsafe_allow_html=True)
