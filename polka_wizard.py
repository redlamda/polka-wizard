"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║   POLKA WIZARD v2 — Outil de tarification Contract Logistics                    ║
║   Basé sur Polka V202541 · OCP Morocco · Dachser CL                             ║
║   Lancement : streamlit run polka_wizard.py                                     ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
from copy import deepcopy
import json

st.set_page_config(
    page_title="Polka Wizard — Tarification Logistique",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp { background-color: #0f1117; color: #e8eaf6; }
.block-container { padding-top: 1.2rem; max-width: 1200px; }
[data-testid="stSidebar"] { background-color: #13161f; border-right: 1px solid #252840; }
.step-hdr { background: #13161f; border-left: 4px solid #4f7cff;
            border-radius: 0 12px 12px 0; padding: 14px 20px; margin-bottom: 20px; }
.step-num { font-size: 11px; color: #4f7cff; text-transform: uppercase; letter-spacing: 0.8px; }
.step-title { font-size: 20px; font-weight: 800; margin: 3px 0; }
.step-desc { font-size: 13px; color: #7b82a8; }
.help-box { background: rgba(79,124,255,0.07); border: 1px solid rgba(79,124,255,0.25);
            border-radius: 10px; padding: 12px 15px; font-size: 12px; color: #a0aacc;
            margin: 8px 0 14px 0; line-height: 1.6; }
.help-box strong { color: #c5cae9; }
.res-card { background: #13161f; border: 1px solid #252840;
            border-radius: 12px; padding: 16px 18px; margin: 8px 0; }
.res-green { color: #22d3a0; font-size: 20px; font-weight: 800; }
.res-red   { color: #ff5c6a; font-size: 20px; font-weight: 800; }
.res-blue  { color: #4f7cff; font-size: 20px; font-weight: 800; }
.res-label { font-size: 11px; color: #7b82a8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.res-sub   { font-size: 11px; color: #7b82a8; margin-top: 3px; }
.warn  { background: rgba(255,181,71,0.08); border: 1px solid rgba(255,181,71,0.3);
         border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #ffb547; margin: 8px 0; }
.ok    { background: rgba(34,211,160,0.08); border: 1px solid rgba(34,211,160,0.3);
         border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #22d3a0; margin: 8px 0; }
.info  { background: rgba(79,124,255,0.08); border: 1px solid rgba(79,124,255,0.3);
         border-radius: 8px; padding: 10px 14px; font-size: 13px; color: #7b9fff; margin: 8px 0; }
.sec-title { font-size: 14px; font-weight: 700; color: #c5cae9;
             border-bottom: 1px solid #252840; padding-bottom: 6px; margin: 18px 0 10px 0; }
</style>
""", unsafe_allow_html=True)

# ── DONNÉES OCP RÉELLES ──────────────────────────────────
OCP = {
    "projet": "OCP", "chef_projet": "Reda Lamdarhri Kachani",
    "agence": "MA-Mohammedia (580)", "pays": "Maroc", "wms": "MIKADO",
    "jours_ouvres": 272, "taux_interet": 0.09, "marge_cible": 0.10,
    "reserve_op": 0.10, "taux_panne": 0.05, "alloc_wms": 0.022,
    "batteries_li": True, "prime_risque_fret": 0.15, "prime_risque_colis": 0.05,
    "surface_m2": 4039.74, "hauteur_m": 10.0, "emplacements_brut": 4211,
    "taux_utilisation": 0.95,
    "loyer_m2_mois": 5.2194, "cout_rack_ppl": 30.0, "duree_amort_rack": 12,
    "cout_secu_lump": 12.0, "duree_amort_secu": 10,
    "cout_cablage_lump": 10.5, "duree_amort_cable": 5,
    "taux_taxe_communale": 0.105, "taux_charge_locative": 0.02,
    "fte_cariste": 3.30, "fte_chargeur": 1.57, "fte_dechargeur": 0.85,
    "fte_ctrl_reception": 0.50, "fte_prep_cmd": 0.00,
    "fte_coord_equipe": 0.00, "fte_chef_equipe": 0.00,
    "fte_admin_reception": 1.00, "fte_admin_expedition": 0.00,
    "fte_service_client": 0.00, "fte_resp_entrepot": 0.00,
    "salaire_operationnel": 13829, "salaire_admin": 18628,
    "qt_fast_mover": 2.79, "qt_reach_truck_gt8m": 3.42,
    "qt_reach_truck_lte8m": 0.00, "qt_transpalette": 0.00,
    "qt_chariot_frontal": 0.00, "qt_prep_horiz": 0.00,
    "qt_allee_etroite": 0.00, "qt_balayeuse": 0.00,
    "prix_fast_mover": 10606, "prix_reach_gt8m": 44619,
    "prix_reach_lte8m": 31089, "prix_transpalette": 375,
    "prix_chariot_frontal": 22644, "prix_prep_horiz": 11956,
    "prix_allee_etroite": 95000, "prix_balayeuse": 24990,
    "emplacements_vendus": 4000, "vol_entrees_palettes": 70720,
    "vol_sorties_palettes": 70720, "vol_livraisons": 0,
    "vol_sorties_cmd": 0, "vol_chargements": 0,
    "vol_palettes_chargees": 0, "vol_vrac_entree": 0, "vol_vrac_sortie": 0,
    "prod_dechargement_h": 37.63, "prod_mise_en_stock_h": 34.02,
    "prod_prelevement_h": 27.69, "prod_chargement_h": 32.19,
    "cout_it_annuel": 2182,
    "tarif_reel_stockage_mois": 6.58,
    "tarif_reel_entree_palette": 2.562,
    "tarif_reel_sortie_palette": 2.929,
    "ca_reel_total": 704163.52, "cout_reel_total": 643522.45,
    "profit_reel": 60641.07, "marge_reelle": 0.0861,
}

VIERGE = deepcopy(OCP)
for k in ["projet","chef_projet","agence","pays","wms"]:
    VIERGE[k] = ""
for k in ["surface_m2","emplacements_brut","loyer_m2_mois",
          "vol_entrees_palettes","vol_sorties_palettes","emplacements_vendus"]:
    VIERGE[k] = 0.0
for k in ["fte_cariste","fte_chargeur","fte_dechargeur","fte_ctrl_reception",
          "fte_prep_cmd","fte_coord_equipe","fte_chef_equipe",
          "fte_admin_reception","fte_admin_expedition","fte_service_client","fte_resp_entrepot"]:
    VIERGE[k] = 0.0
for k in ["qt_fast_mover","qt_reach_truck_gt8m","qt_reach_truck_lte8m","qt_transpalette",
          "qt_chariot_frontal","qt_prep_horiz","qt_allee_etroite","qt_balayeuse"]:
    VIERGE[k] = 0.0
VIERGE["cout_it_annuel"] = 0

def init():
    if "d" not in st.session_state:
        st.session_state.d = deepcopy(OCP)
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "preset" not in st.session_state:
        st.session_state.preset = "ocp"

init()
d = st.session_state.d

# ── MOTEUR DE CALCUL ──────────────────────────────────────
def calculer(d):
    r = {}
    empl_nets = round(d["emplacements_brut"] * d["taux_utilisation"])
    r["empl_nets"] = empl_nets
    r["volume_m3"] = d["surface_m2"] * d["hauteur_m"]
    loyer_an = d["loyer_m2_mois"] * 12 * d["surface_m2"]
    loyer_total = loyer_an * (1 + d["taux_charge_locative"] + d["taux_taxe_communale"])
    r["loyer_an"] = loyer_an
    r["loyer_total"] = loyer_total
    invest_rack = d["cout_rack_ppl"] * d["emplacements_brut"]
    cout_rack_an = invest_rack * (d["taux_interet"] + 1 / max(d["duree_amort_rack"], 1))
    r["cout_rack_an"] = cout_rack_an
    invest_secu = d["cout_secu_lump"] * d["surface_m2"]
    cout_secu_an = invest_secu * (d["taux_interet"] + 1 / max(d["duree_amort_secu"], 1))
    r["cout_secu_an"] = cout_secu_an
    invest_cable = d["cout_cablage_lump"] * d["surface_m2"]
    cout_cable_an = invest_cable * (d["taux_interet"] + 1 / max(d["duree_amort_cable"], 1))
    r["cout_cable_an"] = cout_cable_an
    cout_entrepot = loyer_total + cout_rack_an + cout_secu_an + cout_cable_an
    r["cout_entrepot"] = cout_entrepot

    TAUX_CH = 0.333
    pers = {
        "Cariste":             d["fte_cariste"]          * d["salaire_operationnel"] * (1 + TAUX_CH),
        "Chargeur":            d["fte_chargeur"]          * d["salaire_operationnel"] * (1 + TAUX_CH),
        "Déchargeur":          d["fte_dechargeur"]        * d["salaire_operationnel"] * (1 + TAUX_CH),
        "Ctrl réception":      d["fte_ctrl_reception"]    * d["salaire_operationnel"] * (1 + TAUX_CH),
        "Préparateur cmd":     d["fte_prep_cmd"]          * d["salaire_operationnel"] * (1 + TAUX_CH),
        "Coordinateur":        d["fte_coord_equipe"]      * d["salaire_admin"]        * (1 + TAUX_CH),
        "Chef équipe":         d["fte_chef_equipe"]       * d["salaire_admin"]        * (1 + TAUX_CH),
        "Admin réception":     d["fte_admin_reception"]   * d["salaire_admin"]        * (1 + TAUX_CH),
        "Admin expédition":    d["fte_admin_expedition"]  * d["salaire_admin"]        * (1 + TAUX_CH),
        "Service client":      d["fte_service_client"]    * d["salaire_admin"]        * (1 + TAUX_CH),
        "Resp. entrepôt":      d["fte_resp_entrepot"]     * d["salaire_admin"]        * (1 + TAUX_CH),
    }
    cout_pers_total = sum(pers.values())
    fte_op  = (d["fte_cariste"] + d["fte_chargeur"] + d["fte_dechargeur"] +
               d["fte_ctrl_reception"] + d["fte_prep_cmd"])
    fte_adm = (d["fte_admin_reception"] + d["fte_admin_expedition"] +
               d["fte_service_client"] + d["fte_coord_equipe"] +
               d["fte_chef_equipe"] + d["fte_resp_entrepot"])
    cout_pers_op  = pers["Cariste"] + pers["Chargeur"] + pers["Déchargeur"] + pers["Ctrl réception"] + pers["Préparateur cmd"]
    cout_pers_adm = cout_pers_total - cout_pers_op
    r["pers"] = pers
    r["cout_pers_total"] = cout_pers_total
    r["cout_pers_op"]    = cout_pers_op
    r["cout_pers_adm"]   = cout_pers_adm
    r["fte_total"]       = fte_op + fte_adm
    r["fte_op"]          = fte_op
    r["fte_adm"]         = fte_adm

    engins = {
        "Fast Mover":           d["qt_fast_mover"]        * d["prix_fast_mover"],
        "Reach Truck >8m":      d["qt_reach_truck_gt8m"]  * d["prix_reach_gt8m"],
        "Reach Truck ≤8m":      d["qt_reach_truck_lte8m"] * d["prix_reach_lte8m"],
        "Transpalette":         d["qt_transpalette"]       * d["prix_transpalette"],
        "Chariot frontal":      d["qt_chariot_frontal"]    * d["prix_chariot_frontal"],
        "Préparateur horiz.":   d["qt_prep_horiz"]         * d["prix_prep_horiz"],
        "Allée étroite":        d["qt_allee_etroite"]      * d["prix_allee_etroite"],
        "Balayeuse":            d["qt_balayeuse"]          * d["prix_balayeuse"],
    }
    cout_engins = sum(engins.values())
    r["engins"] = engins
    r["cout_engins"] = cout_engins
    r["qt_engins_total"] = sum([d["qt_fast_mover"], d["qt_reach_truck_gt8m"], d["qt_reach_truck_lte8m"],
                                 d["qt_transpalette"], d["qt_chariot_frontal"], d["qt_prep_horiz"],
                                 d["qt_allee_etroite"], d["qt_balayeuse"]])

    cout_wms_alloc = (cout_pers_op + cout_engins) * d["alloc_wms"]
    cout_it_total  = d["cout_it_annuel"] + cout_wms_alloc
    r["cout_wms_alloc"] = cout_wms_alloc
    r["cout_it_total"]  = cout_it_total

    cout_total = cout_entrepot + cout_pers_total + cout_engins + cout_it_total
    r["cout_total"] = cout_total

    vol_in  = max(d["vol_entrees_palettes"], 1)
    vol_out = max(d["vol_sorties_palettes"], 1)
    vol_tot = vol_in + vol_out
    share_in  = vol_in  / vol_tot
    share_out = vol_out / vol_tot
    cout_proc_in  = (cout_pers_op + cout_engins) * share_in
    cout_proc_out = (cout_pers_op + cout_engins) * share_out
    r["cout_proc_in"]  = cout_proc_in
    r["cout_proc_out"] = cout_proc_out
    r["cu_entree"]     = cout_proc_in  / vol_in
    r["cu_sortie"]     = cout_proc_out / vol_out

    empl_v = max(d["emplacements_vendus"], 1)
    r["cu_stockage_mois"] = cout_entrepot / 12 / empl_v

    m = d["marge_cible"]
    r["prix_stockage_mois"]  = r["cu_stockage_mois"] / (1 - m) if m < 1 else 0
    r["prix_stockage_an"]    = r["prix_stockage_mois"] * 12
    r["prix_entree_palette"] = r["cu_entree"]        / (1 - m) if m < 1 else 0
    r["prix_sortie_palette"] = r["cu_sortie"]        / (1 - m) if m < 1 else 0
    r["prix_entree_min"]     = r["cu_entree"]
    r["prix_sortie_min"]     = r["cu_sortie"]
    r["prix_stockage_min"]   = r["cu_stockage_mois"]

    ca_s = d["emplacements_vendus"] * r["prix_stockage_mois"] * 12
    ca_i = d["vol_entrees_palettes"] * r["prix_entree_palette"]
    ca_o = d["vol_sorties_palettes"] * r["prix_sortie_palette"]
    ca_total = ca_s + ca_i + ca_o
    profit   = ca_total - cout_total
    r["ca_stockage"] = ca_s
    r["ca_in"]       = ca_i
    r["ca_out"]      = ca_o
    r["ca_total"]    = ca_total
    r["profit"]      = profit
    r["marge_calc"]  = profit / ca_total if ca_total > 0 else 0

    ca_vp10 = (ca_s + d["vol_entrees_palettes"]*1.1*r["prix_entree_palette"] + d["vol_sorties_palettes"]*1.1*r["prix_sortie_palette"])
    ca_vm10 = (ca_s + d["vol_entrees_palettes"]*0.9*r["prix_entree_palette"] + d["vol_sorties_palettes"]*0.9*r["prix_sortie_palette"])
    r["profit_vol_p10"] = ca_vp10 - cout_total
    r["profit_vol_m10"] = ca_vm10 - cout_total
    r["marge_vol_p10"]  = r["profit_vol_p10"] / ca_vp10 if ca_vp10 > 0 else 0
    r["marge_vol_m10"]  = r["profit_vol_m10"] / ca_vm10 if ca_vm10 > 0 else 0

    couts_fixes = cout_entrepot + cout_pers_adm + cout_it_total
    taux_mv = (ca_i + ca_o - cout_pers_op - cout_engins) / (ca_i + ca_o) if (ca_i + ca_o) > 0 else 0
    r["seuil_rentabilite"] = couts_fixes / taux_mv if taux_mv > 0 else 0
    r["couts_fixes"] = couts_fixes
    return r

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:14px 0 10px;'>
      <div style='font-size:28px;'>📦</div>
      <div style='font-size:15px;font-weight:800;color:#e8eaf6;'>Polka Wizard v2</div>
      <div style='font-size:11px;color:#7b82a8;'>Contract Logistics · Dachser</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    preset = st.radio("🗂️ Jeu de données", ["OCP Morocco (réel)", "Nouveau projet (vierge)"])
    if preset == "OCP Morocco (réel)" and st.session_state.preset != "ocp":
        st.session_state.d = deepcopy(OCP); st.session_state.preset = "ocp"; st.rerun()
    elif preset == "Nouveau projet (vierge)" and st.session_state.preset != "vierge":
        st.session_state.d = deepcopy(VIERGE); st.session_state.preset = "vierge"; st.rerun()

    st.divider()
    STEPS = [(1,"🏭 Projet & Entrepôt"),(2,"⚙️ Paramètres Polka"),
             (3,"👷 Personnel"),(4,"🏗️ Engins"),(5,"📊 Volumes"),
             (6,"💶 Calcul Tarifs"),(7,"📉 Sensibilité")]
    for num, label in STEPS:
        active = st.session_state.step == num
        col = "#4f7cff" if active else "#55597a"
        bg  = "rgba(79,124,255,0.12)" if active else "transparent"
        st.markdown(f"""<div style='padding:7px 10px;border-radius:7px;background:{bg};
            border-left:3px solid {col};margin:3px 0;'>
            <span style='color:{col};font-weight:{"700" if active else "400"};font-size:12px;'>{label}</span></div>""",
            unsafe_allow_html=True)
        if st.button(f"{label}", key=f"nb_{num}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.step = num; st.rerun()

    st.divider()
    try:
        res = calculer(st.session_state.d)
        mc = "#22d3a0" if res["marge_calc"] >= d["marge_cible"] else "#ff5c6a"
        st.markdown(f"""<div style='font-size:12px;'>
          <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #252840;'>
            <span style='color:#7b82a8;'>CA estimé</span><span style='color:#4f7cff;font-weight:700;'>{res['ca_total']:,.0f} €</span></div>
          <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #252840;'>
            <span style='color:#7b82a8;'>Coûts</span><span style='color:#ffb547;font-weight:700;'>{res['cout_total']:,.0f} €</span></div>
          <div style='display:flex;justify-content:space-between;padding:4px 0;'>
            <span style='color:#7b82a8;'>Marge</span><span style='color:{mc};font-weight:700;'>{res['marge_calc']:.2%}</span></div>
        </div>""", unsafe_allow_html=True)
    except: pass

def hdr(num, icon, title, desc):
    st.markdown(f"""<div class='step-hdr'>
      <div class='step-num'>ÉTAPE {num} / 7</div>
      <div class='step-title'>{icon} {title}</div>
      <div class='step-desc'>{desc}</div></div>""", unsafe_allow_html=True)

def help_box(txt):
    st.markdown(f"<div class='help-box'>ℹ️ {txt}</div>", unsafe_allow_html=True)

def nav(step):
    c1, _, c3 = st.columns([1,5,1])
    with c1:
        if step > 1 and st.button("← Retour", use_container_width=True):
            st.session_state.step = step - 1; st.rerun()
    with c3:
        lbl = "Suivant →" if step < 7 else "🔄 Recommencer"
        if st.button(lbl, type="primary", use_container_width=True):
            st.session_state.step = (step + 1) if step < 7 else 1; st.rerun()

# ════════════════════════════════════════════════════════
# ÉTAPE 1 — PROJET & ENTREPÔT
# ════════════════════════════════════════════════════════
if st.session_state.step == 1:
    hdr(1, "🏭", "Données Projet & Entrepôt",
        "Informations du contrat et caractéristiques physiques du site logistique.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec-title'>🏢 Identification du projet</div>", unsafe_allow_html=True)
        help_box("""Correspond à l'onglet <strong>Branch's Basic Data</strong> du fichier Polka.
        Ces données identifient le client, le site Dachser et l'équipe en charge du contrat.""")
        d["projet"]      = st.text_input("Nom du projet / Client", value=d["projet"], help="Nom commercial du client · ex : OCP, Renault…")
        d["chef_projet"] = st.text_input("Chef de projet", value=d["chef_projet"])
        d["agence"]      = st.text_input("Agence / Site Dachser", value=d["agence"], help="Code agence · ex : MA-Mohammedia (580)")
        d["pays"]        = st.text_input("Pays", value=d["pays"])
        d["wms"]         = st.text_input("Système WMS", value=d["wms"], help="WMS utilisé sur site · OCP = MIKADO")

        st.markdown("<div class='sec-title'>📐 Dimensions de l'entrepôt</div>", unsafe_allow_html=True)
        help_box("""Données issues des onglets <strong>Warehouse</strong> et <strong>Key figures</strong>.
        <br><strong>OCP WH0010 :</strong> 4 040 m² · hauteur 10 m · 4 211 emplacements bruts · 95% utilisation → 4 000 empl. nets.
        <br>Le taux d'utilisation reflète la déduction de la réserve opérationnelle (zones tampon, couloirs).""")
        d["surface_m2"]         = st.number_input("Surface nette (m²)", min_value=0.0, value=float(d["surface_m2"]), step=50.0,
                                      help="Surface de stockage hors bureaux · OCP = 4 039,74 m²")
        d["hauteur_m"]          = st.number_input("Hauteur utile (m)", min_value=3.0, max_value=30.0, value=float(d["hauteur_m"]), step=0.5,
                                      help="Hauteur libre sous poutre · OCP = 10 m → nécessite Reach Truck >8m")
        d["emplacements_brut"]  = st.number_input("Emplacements palettes (brut)", min_value=0, value=int(d["emplacements_brut"]), step=10,
                                      help="Nombre total d'emplacements dans les racks · OCP = 4 211")
        d["taux_utilisation"]   = st.slider("Taux d'utilisation cible", min_value=0.5, max_value=1.0,
                                      value=float(d["taux_utilisation"]), step=0.01, format="%.0%",
                                      help="OCP = 95% · Polka déduit 10% de réserve op. → 4 211 × 95% = 4 000 empl. nets")
        empl_nets = int(d["emplacements_brut"] * d["taux_utilisation"])
        vol = d["surface_m2"] * d["hauteur_m"]
        st.markdown(f"""<div class='res-card'><div style='display:flex;gap:20px;flex-wrap:wrap;'>
          <div><div class='res-label'>Emplacements nets</div><div class='res-blue'>{empl_nets:,}</div></div>
          <div><div class='res-label'>Volume m³</div><div class='res-blue'>{vol:,.0f}</div></div>
          <div><div class='res-label'>Densité</div><div class='res-blue'>{d["emplacements_brut"]/max(d["surface_m2"],1):.2f} pal/m²</div></div>
        </div></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='sec-title'>💰 Coûts immobiliers</div>", unsafe_allow_html=True)
        help_box("""Données de l'onglet <strong>Warehouse Costs</strong> + notes OCP locales dans <strong>Warehouse</strong>.
        <br>Le loyer OCP est calculé depuis le MAD (1 MAD = 0,0922 € au 12/02/2026).
        <br>Prix m² brut MAD = 56,58 MAD/m²/mois → 5,22 €/m²/mois.
        <br>Taxes Maroc spécifiques : taxe communale 10,5% + charges locatives 2%.""")
        d["loyer_m2_mois"]         = st.number_input("Loyer / m² / mois (€)", min_value=0.0, value=float(d["loyer_m2_mois"]), step=0.1, format="%.4f",
                                          help="OCP = 5,2194 €/m²/mois (56,58 MAD × 0,0922)")
        d["taux_taxe_communale"]   = st.number_input("Taxe communale (%)", min_value=0.0, max_value=0.5, value=float(d["taux_taxe_communale"]), step=0.005, format="%.3f",
                                          help="Taxe locale sur le bail · OCP Maroc = 10,5% · France = 0%")
        d["taux_charge_locative"]  = st.number_input("Charges locatives (%)", min_value=0.0, max_value=0.2, value=float(d["taux_charge_locative"]), step=0.005, format="%.3f",
                                          help="Charges annexes au loyer · OCP = 2% · Très variable selon les baux")

        st.markdown("<div class='sec-title'>🔧 Investissements amortis (formule Polka)</div>", unsafe_allow_html=True)
        help_box("""Formule Polka pour chaque investissement :
        <br><code>Annuité = Investissement × (taux_intérêt + 1/durée_amort)</code>
        <br>Cette formule intègre le coût d'opportunité du capital (taux = 9%) dans l'annuité.
        <br>Données issues directement de l'onglet <strong>Warehouse Costs</strong> Polka.""")
        d["cout_rack_ppl"]      = st.number_input("Coût racks / emplacement (€ achat)", min_value=0.0, value=float(d["cout_rack_ppl"]), step=1.0,
                                      help="Racking System PPL · OCP Polka = 30 €/emplacement")
        d["duree_amort_rack"]   = st.number_input("Amortissement racks (années)", min_value=1, max_value=30, value=int(d["duree_amort_rack"]),
                                      help="Polka standard = 12 ans")
        d["cout_secu_lump"]     = st.number_input("Sécurité / vidéo (€/m²)", min_value=0.0, value=float(d["cout_secu_lump"]), step=0.5,
                                      help="Safety/Security Lump Sum · OCP Polka = 12 €/m²")
        d["duree_amort_secu"]   = st.number_input("Amortissement sécurité (années)", min_value=1, max_value=20, value=int(d["duree_amort_secu"]),
                                      help="Polka = 10 ans")
        d["cout_cablage_lump"]  = st.number_input("Câblage réseau (€/m²)", min_value=0.0, value=float(d["cout_cablage_lump"]), step=0.5,
                                      help="Cabling Lump Sum · OCP Polka = 10,5 €/m²")
        d["duree_amort_cable"]  = st.number_input("Amortissement câblage (années)", min_value=1, max_value=15, value=int(d["duree_amort_cable"]),
                                      help="Polka = 5 ans")

        loyer_t = d["loyer_m2_mois"] * 12 * d["surface_m2"] * (1 + d["taux_taxe_communale"] + d["taux_charge_locative"])
        rack_a  = d["cout_rack_ppl"] * d["emplacements_brut"] * (d["taux_interet"] + 1/max(d["duree_amort_rack"],1))
        st.markdown(f"""<div class='res-card'>
          <div class='res-label'>Estimation coût entrepôt annuel</div>
          <div class='res-blue'>{loyer_t+rack_a:,.0f} €</div>
          <div class='res-sub'>Loyer charges incluses : {loyer_t:,.0f} € · Racks : {rack_a:,.0f} €</div>
        </div>""", unsafe_allow_html=True)
    nav(1)

# ════════════════════════════════════════════════════════
# ÉTAPE 2 — PARAMÈTRES POLKA
# ════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    hdr(2, "⚙️", "Paramètres & Hypothèses Polka",
        "Paramètres financiers et opérationnels pilotant l'ensemble des calculs du modèle.")

    help_box("""Ces paramètres correspondent à l'onglet <strong>Branch's Basic Data</strong> du fichier Polka.
    Ils s'appliquent à tous les calculs : coûts entrepôt, personnel, engins et tarifs.
    <strong>Ne les modifier que si le contexte du site le justifie.</strong>""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec-title'>📅 Paramètres opérationnels</div>", unsafe_allow_html=True)
        d["jours_ouvres"] = st.number_input("Jours ouvrés / an", min_value=200, max_value=365, value=int(d["jours_ouvres"]),
                                help="OCP = 272 jours (5j/semaine, hors fériés Maroc) · France standard ≈ 220 jours")
        d["reserve_op"]   = st.number_input("Réserve opérationnelle (%)", min_value=0.0, max_value=0.3, value=float(d["reserve_op"]), step=0.01, format="%.2f",
                                help="Déduit des emplacements bruts pour couvrir zones défaillantes/tampons · Polka OCP = 10%")
        d["taux_panne"]   = st.number_input("Taux de défaillance engins (%)", min_value=0.0, max_value=0.3, value=float(d["taux_panne"]), step=0.01, format="%.2f",
                                help="% de temps d'arrêt technique des engins · Polka = 5% · Impacte le besoin en engins de substitution")
        d["batteries_li"] = st.checkbox("Batteries lithium-ion (LI) pour engins électriques", value=bool(d["batteries_li"]),
                                help="OCP = Oui · Élimine le besoin d'engins de rechange pendant la recharge · Réduit le parc nécessaire")
        if d["batteries_li"]:
            st.markdown("<div class='ok'>✓ LI activé — pas de doublement du parc pour la recharge</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='sec-title'>💰 Paramètres financiers</div>", unsafe_allow_html=True)
        d["taux_interet"] = st.number_input("Taux d'intérêt interne Dachser (%)", min_value=0.0, max_value=0.3, value=float(d["taux_interet"]), step=0.005, format="%.3f",
                                help="Appliqué dans la formule d'annuité des investissements · Polka Dachser standard = 9%")
        d["marge_cible"]  = st.slider("🎯 Marge cible (%)", min_value=0.0, max_value=0.30, value=float(d["marge_cible"]), step=0.005, format="%.1%",
                                help="Objectif de marge nette · Polka = 10% · OCP réel = 8,61% (légèrement sous objectif côté stockage)")
        d["alloc_wms"]    = st.number_input("Allocation WMS + Innovation Fund (%)", min_value=0.0, max_value=0.10, value=float(d["alloc_wms"]), step=0.001, format="%.3f",
                                help="% des coûts variables alloué au WMS (MIKADO) et fonds innovation Dachser · Polka = 2,2%")

        st.markdown("<div class='sec-title'>🚚 Primes de risque transport</div>", unsafe_allow_html=True)
        help_box("Primes appliquées sur les coûts de transport pour couvrir la responsabilité civile marchandises.")
        d["prime_risque_fret"]  = st.number_input("Prime risque fret - palettes (%)", min_value=0.0, max_value=0.5, value=float(d["prime_risque_fret"]), step=0.01, format="%.2f",
                                      help="Risk Premium Transport Liability (Freight shipments) · Polka = 15%")
        d["prime_risque_colis"] = st.number_input("Prime risque colis (%)", min_value=0.0, max_value=0.5, value=float(d["prime_risque_colis"]), step=0.01, format="%.2f",
                                      help="Risk Premium Transport Liability (Parcel shipments) · Polka = 5%")
    nav(2)

# ════════════════════════════════════════════════════════
# ÉTAPE 3 — PERSONNEL
# ════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    hdr(3, "👷", "Cockpit Personnel",
        "Effectifs ETP par poste et coûts salariaux — onglet Cockpit Personnel de Polka.")

    help_box("""Polka calcule automatiquement les ETP nécessaires à partir des volumes et productivités (<strong>Prods simplifiées</strong>).
    Les valeurs OCP ci-dessous sont les ETP alloués après arrondi.
    <br><strong>Formule coût :</strong> ETP × Salaire brut × (1 + taux charges sociales ~33%)
    <br>Pour les administratifs, Polka ajoute les allocations <strong>HO (1,3%)</strong> et <strong>RHO/RCO (31,9%)</strong> → coût total admin OCP = 24 819 €/ETP/an.""")

    with st.expander("📈 Productivités mesurées sur site OCP (onglet Prods simplifiées)", expanded=False):
        help_box("""Ces productivités ont été mesurées et validées sur le site OCP Mohammedia.
        Elles pilotent le calcul automatique des ETP dans Polka.
        <br>Taux de charge appliqué : 40% (MUP Polka = 22%, taux site réel = 30%, taux moyen retenu = 40%).""")
        c1,c2,c3,c4 = st.columns(4)
        with c1: d["prod_dechargement_h"]  = st.number_input("Déchargement (pal/h prod.)",  value=float(d["prod_dechargement_h"]),  step=1.0, help="ETP calculé Polka = 1,34 · OCP = 37,63 pal/h productive (43,82 pal/h brute)")
        with c2: d["prod_mise_en_stock_h"] = st.number_input("Mise en stock (pal/h prod.)", value=float(d["prod_mise_en_stock_h"]), step=1.0, help="ETP calculé Polka = 1,48 · OCP = 34,02 pal/h productive")
        with c3: d["prod_prelevement_h"]   = st.number_input("Prélèvement (pal/h prod.)",   value=float(d["prod_prelevement_h"]),   step=1.0, help="ETP calculé Polka = 1,82 · OCP = 27,69 pal/h productive")
        with c4: d["prod_chargement_h"]    = st.number_input("Chargement (pal/h prod.)",    value=float(d["prod_chargement_h"]),    step=1.0, help="ETP calculé Polka = 1,56 · OCP = 32,19 pal/h productive")

    st.markdown("<div class='sec-title'>🔵 Opérationnels — Logistics Operatives (salaire brut = 13 829 €/an OCP)</div>", unsafe_allow_html=True)
    help_box("Coût chargé estimé ≈ <strong>18 390 €/ETP/an</strong> (salaire 13 829 € × 1,333 charges)")

    STAFF_OP = [
        ("fte_cariste",        "🚛 Cariste\n(Forklift Driver)",
         "Conduit Reach Trucks et Fast Movers · Mise en stock et prélèvement\nETP calculé Polka = 3,29 → alloué OCP = 3,30"),
        ("fte_chargeur",       "📦 Chargeur\n(Loader)",
         "Chargement des camions à la sortie\nETP calculé Polka = 1,56 → alloué OCP = 1,57"),
        ("fte_dechargeur",     "📥 Déchargeur\n(Unloader)",
         "Déchargement des camions entrants\nETP calculé Polka = 0,84 → alloué OCP = 0,85"),
        ("fte_ctrl_reception", "🔍 Contrôleur récep.\n(Inbound Ctrl)",
         "Contrôle qualitatif et quantitatif des marchandises reçues\nETP calculé Polka = 0,49 → alloué OCP = 0,50"),
        ("fte_prep_cmd",       "🛒 Prépar. commandes\n(Picker)",
         "Picking colis et préparation commandes détail\nOCP = 0 ETP (pas de picking colis sur ce site)"),
    ]
    cols = st.columns(len(STAFF_OP))
    for i, (key, label, tip) in enumerate(STAFF_OP):
        with cols[i]:
            d[key] = st.number_input(label, min_value=0.0, max_value=30.0, value=float(d[key]),
                         step=0.01, key=f"op_{key}", format="%.2f", help=tip)
            cost = d[key] * d["salaire_operationnel"] * 1.333
            st.caption(f"→ {cost:,.0f} €/an")

    d["salaire_operationnel"] = st.number_input("💶 Salaire brut annuel opérationnels (€/an)",
                                    min_value=0, max_value=100000, value=int(d["salaire_operationnel"]), step=100,
                                    help="Gross Salary/Wage per year · Polka OCP Logistics Operatives = 13 829 €/an brut · France ≈ 22 000-28 000 €")

    st.markdown("<div class='sec-title'>🟡 Encadrement & Administratifs — Office Employees (salaire brut = 18 628 €/an OCP)</div>", unsafe_allow_html=True)
    help_box("""Coût total chargé Polka = <strong>24 819 €/ETP/an</strong>
    (brut 18 628 € + congés/maladie 1 946 € + charges sociales 5 206 € + HO 1,3% + RHO/RCO 31,9%)
    <br><strong>OCP : 1 ETP Administration Réception uniquement</strong> → tous les autres = 0.""")

    STAFF_ADM = [
        ("fte_admin_reception",  "📋 Admin. réception\n(Inbound Admin)",
         "Gestion administrative des réceptions · Saisie WMS\nOCP = 1,00 ETP · Coût Polka total = 24 819 €/an"),
        ("fte_admin_expedition", "📤 Admin. expédition\n(Outbound Admin)",
         "Gestion administrative des expéditions · OCP = 0 ETP"),
        ("fte_service_client",   "📞 Service client\n(Customer Service)",
         "Relation client, réclamations · OCP = 0 ETP"),
        ("fte_coord_equipe",     "👥 Coordinateur équipe\n(Team Coordinator)",
         "Coordination des équipes (non process) · OCP = 0 ETP"),
        ("fte_chef_equipe",      "🔧 Chef d'équipe\n(Shift Leader)",
         "Encadrement de quart · OCP = 0 ETP"),
        ("fte_resp_entrepot",    "🏆 Resp. entrepôt\n(WH Manager)",
         "Responsable du site logistique · OCP = 0 ETP"),
    ]
    cols2 = st.columns(3)
    for i, (key, label, tip) in enumerate(STAFF_ADM):
        with cols2[i % 3]:
            d[key] = st.number_input(label, min_value=0.0, max_value=20.0, value=float(d[key]),
                         step=0.01, key=f"adm_{key}", format="%.2f", help=tip)
            cost = d[key] * d["salaire_admin"] * 1.333
            st.caption(f"→ {cost:,.0f} €/an")

    d["salaire_admin"] = st.number_input("💶 Salaire brut annuel admin/encadrement (€/an)",
                            min_value=0, max_value=200000, value=int(d["salaire_admin"]), step=100,
                            help="Polka OCP Office Employees = 18 628 €/an brut · Coût total chargé = 24 819 €/an après HO+RHO")

    res_p = calculer(d)
    st.divider()
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("ETP total", f"{res_p['fte_total']:.2f}")
    with c2: st.metric("ETP opérationnels", f"{res_p['fte_op']:.2f}")
    with c3: st.metric("ETP admin/encadr.", f"{res_p['fte_adm']:.2f}")
    with c4: st.metric("Coût personnel/an", f"{res_p['cout_pers_total']:,.0f} €")
    if st.session_state.preset == "ocp":
        st.markdown(f"<div class='info'>ℹ️ Coût personnel OCP réel Polka = <strong>148 419 €</strong> · Votre calcul : {res_p['cout_pers_total']:,.0f} €</div>", unsafe_allow_html=True)
    nav(3)

# ════════════════════════════════════════════════════════
# ÉTAPE 4 — ENGINS
# ════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    hdr(4, "🏗️", "Cockpit Engins de Manutention",
        "Parc d'engins alloué au contrat — onglet Cockpit Industrial Trucks.")

    help_box("""Polka calcule automatiquement le nombre d'engins nécessaires à partir des volumes et des productivités.
    <br><strong>OCP : 2,79 Fast Mover + 3,42 Reach Truck >8m = 6,21 engins · 56 074 €/an</strong>
    <br>Mode <em>External Rent</em> = location annuelle · Mode <em>Purchase</em> = achat amorti sur la durée de vie.
    <br>Les prix sont issus de la table <strong>Industrial Trucks</strong> du fichier Polka (tarifs catalogue Dachser).""")

    ENGINS_DEF = [
        ("qt_fast_mover",        "prix_fast_mover",      "⚡ Fast Mover (FZ0040)",
         "External Rent", 10606,
         """Chariot basse levée à grande vitesse · Déchargement et chargement camions.
         OCP : 2,79 unités · Location = 10 606 €/an/engin.
         Productivité mesurée OCP : 37,63 pal/h déchargement · 32,19 pal/h chargement."""),
        ("qt_reach_truck_gt8m",  "prix_reach_gt8m",      "🔝 Reach Truck > 8m (FZ0085)",
         "External Rent", 44619,
         """Chariot élévateur grande hauteur (>8m) · Mise en stock et prélèvement en rack haute.
         OCP : 3,42 unités · Location = 44 619 €/an/engin.
         Productivité OCP : 34,02 pal/h mise en stock · 27,69 pal/h prélèvement."""),
        ("qt_reach_truck_lte8m", "prix_reach_lte8m",     "🔼 Reach Truck ≤ 8m (FZ0080)",
         "External Rent", 31089,
         "Chariot élévateur standard (≤8m) · OCP = 0 (entrepôt >8m nécessite FZ0085) · Location = 31 089 €/an"),
        ("qt_transpalette",      "prix_transpalette",     "🤲 Transpalette manuel (FZ0010)",
         "Achat", 375,
         "Manutention manuelle au sol · Très faible coût · OCP = 0 · Achat = 375 €"),
        ("qt_chariot_frontal",   "prix_chariot_frontal",  "🔄 Chariot frontal (FZ0070)",
         "External Rent", 22644,
         "Chargement/déchargement à grande capacité · OCP = 0 · Location = 22 644 €/an"),
        ("qt_prep_horiz",        "prix_prep_horiz",       "📋 Préparateur horizontal (FZ0050)",
         "External Rent", 11956,
         "Picking colis au sol · OCP = 0 (pas de picking colis) · Location = 11 956 €/an"),
        ("qt_allee_etroite",     "prix_allee_etroite",    "↔️ Allée étroite (FZ0090)",
         "External Rent", 95000,
         "Stockage haute densité · OCP = 0 · Location = 95 000 €/an (très spécialisé)"),
        ("qt_balayeuse",         "prix_balayeuse",        "🧹 Balayeuse sol (FZ0100)",
         "Achat", 24990,
         "Entretien sol entrepôt · OCP = 0 · Achat = 24 990 €"),
    ]

    total_qt = 0; total_cout = 0
    for qt_key, prix_key, label, mode, prix_ref, tip in ENGINS_DEF:
        active = d[qt_key] > 0
        with st.expander(f"{'🟢' if active else '⚫'}  {label}  —  {d[qt_key]:.2f} unités", expanded=active):
            st.caption(f"_Mode Polka : **{mode}** · Prix référence catalogue : {prix_ref:,} €_")
            st.markdown(f"<div class='help-box'>{tip}</div>", unsafe_allow_html=True)
            c1,c2,c3 = st.columns([2,2,2])
            with c1:
                d[qt_key] = st.number_input("Quantité allouée", min_value=0.0, max_value=50.0,
                                value=float(d[qt_key]), step=0.01, key=f"qt_{qt_key}", format="%.2f",
                                help="Calculé automatiquement par Polka selon volumes + productivités")
            with c2:
                d[prix_key] = st.number_input(f"Coût annuel / engin (€) · {mode}",
                                min_value=0, max_value=500000, value=int(d[prix_key]), step=100,
                                key=f"px_{prix_key}", help="Tarif catalogue Industrial Trucks Polka")
            with c3:
                st.metric("Coût total annuel", f"{d[qt_key]*d[prix_key]:,.0f} €")
            total_qt   += d[qt_key]
            total_cout += d[qt_key] * d[prix_key]

    st.divider()
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("Parc total", f"{total_qt:.2f} engins")
    with c2: st.metric("Coût engins annuel", f"{total_cout:,.0f} €")
    with c3: st.metric("Coût moyen / engin", f"{total_cout/max(total_qt,1):,.0f} €/an")
    if st.session_state.preset == "ocp":
        st.markdown(f"<div class='info'>ℹ️ Coût engins OCP réel Polka = <strong>56 074 €</strong> · Votre calcul : {total_cout:,.0f} €</div>", unsafe_allow_html=True)
    nav(4)

# ════════════════════════════════════════════════════════
# ÉTAPE 5 — VOLUMES & PROCESSUS
# ════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    hdr(5, "📊", "Volumes & Processus Logistiques",
        "Quantités annuelles par processus — onglets Register Quantity Data et Price Sheet.")

    help_box("""Les volumes sont saisis dans <strong>Register Quantity Data</strong> et servent de base au calcul des ETP et des coûts unitaires.
    <br><strong>OCP : 3 processus actifs</strong> — Stockage WH0010, Entrées palettes FP inbound (MF1070), Sorties palettes FP outbound (MF4010).
    <br>Tous les autres processus existent dans Polka mais ont un volume = 0 pour OCP.""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec-title'>🏭 Stockage (Warehouse Costs · WH0010)</div>", unsafe_allow_html=True)
        help_box("""Prestation facturée au nombre d'emplacements palettes réservés contractuellement.
        <br><strong>OCP :</strong> 4 000 emplacements vendus sur 4 000 nets = 100% d'occupation annuelle.
        <br>Price Sheet : 4 000 empl. × 6,58 €/mois × 12 = <strong>315 840 € CA stockage</strong>.
        <br>⚠️ Le stockage est déficitaire chez OCP (-42 838 €) — compensé par les processus.""")
        d["emplacements_vendus"] = st.number_input("Emplacements palettes vendus / an",
                                      min_value=0, max_value=100000, value=int(d["emplacements_vendus"]), step=10,
                                      help="Nombre d'emplacements réservés contractuellement · OCP = 4 000 empl.")
        empl_nets = int(d["emplacements_brut"] * d["taux_utilisation"])
        taux_occ = d["emplacements_vendus"] / max(empl_nets, 1) * 100
        if taux_occ > 100:
            st.markdown(f"<div class='warn'>⚠️ {taux_occ:.1f}% > capacité nette ({empl_nets:,} empl.)</div>", unsafe_allow_html=True)
        elif taux_occ > 85:
            st.markdown(f"<div class='ok'>✓ Occupation : {taux_occ:.1f}% · Niveau optimal</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='info'>ℹ️ Occupation : {taux_occ:.1f}% / {empl_nets:,} empl. nets</div>", unsafe_allow_html=True)

        st.markdown("<div class='sec-title'>📥 Flux entrants — FP Inbound</div>", unsafe_allow_html=True)
        help_box("""<strong>MF1070 = Stock-in Inbound Pallets</strong> · Quantité principale facturée à l'entrée.
        <br>Processus OCP : TP1020 Déchargement camion + TP1120 Contrôle réception + TP1220 Mise en stock sans zone transfert.
        <br><strong>OCP = 70 720 pal/an → 260 pal/jour</strong>""")
        d["vol_entrees_palettes"] = st.number_input("Palettes mises en stock / an (MF1070)",
                                        min_value=0, max_value=2000000, value=int(d["vol_entrees_palettes"]), step=100,
                                        help="Stock-in Inbound Pallets · Principal volume facturé à l'entrée · OCP = 70 720 pal/an")
        d["vol_livraisons"] = st.number_input("Livraisons / camions reçus / an (MF1010)",
                                  min_value=0, max_value=100000, value=int(d["vol_livraisons"]), step=1,
                                  help="Delivery · Nombre de camions arrivants · OCP = 0 (non facturé séparément)")
        d["vol_vrac_entree"] = st.number_input("Unités vrac entrantes / an (MF1040)",
                                   min_value=0, max_value=10000000, value=int(d["vol_vrac_entree"]), step=100,
                                   help="Picking Unit Inbound Loose · Unités individuelles dépotées · OCP = 0")

        st.markdown("<div class='sec-title'>🖥️ Coûts IT & WMS</div>", unsafe_allow_html=True)
        d["cout_it_annuel"] = st.number_input("Coûts IT fixes annuels (€)",
                                  min_value=0, max_value=500000, value=int(d["cout_it_annuel"]), step=100,
                                  help="Fix Costs IT · OCP = 2 182 €/an (WMS MIKADO). Coût WMS global Polka = 17 277 €/an réparti entre tous les clients")

    with col2:
        st.markdown("<div class='sec-title'>📤 Flux sortants — FP Outbound</div>", unsafe_allow_html=True)
        help_box("""<strong>MF4010 = Full Pallets</strong> · Palettes complètes prélevées et expédiées.
        <br>Processus OCP : TP4010 Outbound Full Pallet Without Transfer Zone.
        <br><strong>OCP = 70 720 pal/an</strong> (flux symétrique aux entrées — tout ce qui entre ressort)""")
        d["vol_sorties_palettes"] = st.number_input("Palettes complètes expédiées / an (MF4010)",
                                        min_value=0, max_value=2000000, value=int(d["vol_sorties_palettes"]), step=100,
                                        help="Full Pallets · Volume principal facturé à la sortie · OCP = 70 720 pal/an")
        d["vol_sorties_cmd"] = st.number_input("Ordres de sortie / an (MF4020)",
                                   min_value=0, max_value=500000, value=int(d["vol_sorties_cmd"]), step=10,
                                   help="Full Pallet Order · Nombre de lignes de commande · OCP = 0 (non facturé séparément)")
        d["vol_vrac_sortie"] = st.number_input("Cartons vrac chargés / an (MF5040)",
                                   min_value=0, max_value=10000000, value=int(d["vol_vrac_sortie"]), step=100,
                                   help="Loose Loaded Cartons · OCP = 0")

        st.markdown("<div class='sec-title'>🚛 Chargement camions — FP Loading</div>", unsafe_allow_html=True)
        help_box("""<strong>MF5020 = Loaded Pallets</strong> · Palettes chargées physiquement sur le camion à la sortie.
        <br>Processus OCP : TP5020 Loading Pallets not Double-Stacked (32,19 pal/h productive).
        <br><strong>OCP = 0</strong> : le chargement est inclus dans le tarif sortie, non facturé séparément.""")
        d["vol_palettes_chargees"] = st.number_input("Palettes chargées sur camion / an (MF5020)",
                                         min_value=0, max_value=2000000, value=int(d["vol_palettes_chargees"]), step=100,
                                         help="Loaded Pallets · OCP = 0 (inclus dans le prix de sortie palette)")
        d["vol_chargements"] = st.number_input("Chargements camions / an (MF5010)",
                                   min_value=0, max_value=100000, value=int(d["vol_chargements"]), step=1,
                                   help="Loading of Trucks · OCP = 0")

    if d["vol_entrees_palettes"] > 0 or d["vol_sorties_palettes"] > 0:
        j = max(d["jours_ouvres"], 1)
        st.divider()
        st.markdown(f"""<div class='res-card'><div style='display:flex;gap:30px;flex-wrap:wrap;'>
          <div><div class='res-label'>Entrées / jour</div><div class='res-blue'>{d["vol_entrees_palettes"]/j:.1f} pal/j</div></div>
          <div><div class='res-label'>Sorties / jour</div><div class='res-blue'>{d["vol_sorties_palettes"]/j:.1f} pal/j</div></div>
          <div><div class='res-label'>Total mouvements / jour</div><div class='res-blue'>{(d["vol_entrees_palettes"]+d["vol_sorties_palettes"])/j:.1f} pal/j</div></div>
          <div><div class='res-label'>Jours ouvrés / an</div><div class='res-blue'>{j}</div></div>
        </div></div>""", unsafe_allow_html=True)
    nav(5)

# ════════════════════════════════════════════════════════
# ÉTAPE 6 — CALCUL DES TARIFS
# ════════════════════════════════════════════════════════
elif st.session_state.step == 6:
    hdr(6, "💶", "Calcul Automatique des Tarifs",
        "Tarifs recommandés selon la logique Polka — décomposition complète des coûts.")

    res = calculer(d)
    m_ok = res["marge_calc"] >= d["marge_cible"]
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("CA estimé", f"{res['ca_total']:,.0f} €")
    with c2: st.metric("Coûts totaux", f"{res['cout_total']:,.0f} €")
    with c3: st.metric("Bénéfice", f"{res['profit']:,.0f} €", delta="✅ Objectif" if m_ok else "⚠️ Sous objectif")
    with c4: st.metric("Marge réelle", f"{res['marge_calc']:.2%}")

    if m_ok:
        st.markdown(f"<div class='ok'>✅ Marge calculée {res['marge_calc']:.2%} ≥ objectif {d['marge_cible']:.0%}</div>", unsafe_allow_html=True)
    else:
        gap = (d["marge_cible"] - res["marge_calc"]) * res["ca_total"]
        st.markdown(f"<div class='warn'>⚠️ Marge {res['marge_calc']:.2%} &lt; objectif {d['marge_cible']:.0%} · Manque : {gap:,.0f} €/an</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 💶 Tarifs recommandés")
    help_box("""<strong>Formule Polka :</strong> Prix = Coût_unitaire ÷ (1 − marge_cible)
    <br>Les tarifs sont ajustables — les marges se recalculent en temps réel.
    <br><strong>Seuil min</strong> = coût unitaire (marge = 0%) · <strong>Recommandé</strong> = coût ÷ (1 − 10%)""")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown("**🏭 Stockage (WH0010)**")
        st.caption(f"Coût/empl./mois : {res['cu_stockage_mois']:.4f} € · Min : {res['prix_stockage_min']:.4f} €")
        px_s = st.number_input("€ / emplacement / mois", min_value=0.0, max_value=100.0,
                    value=round(float(res["prix_stockage_mois"]),4), step=0.01, key="px_s", format="%.4f",
                    help=f"Recommandé : {res['prix_stockage_mois']:.4f} € · OCP réel : {d['tarif_reel_stockage_mois']:.2f} €/mois")
        ca_s = d["emplacements_vendus"] * px_s * 12
        mg_s = (ca_s - res["cout_entrepot"]) / ca_s if ca_s > 0 else 0
        col = "#22d3a0" if mg_s >= 0 else "#ff5c6a"
        st.markdown(f"""<div class='res-card'>
          <div class='res-label'>CA stockage annuel</div><div style='color:{col};font-size:18px;font-weight:700;'>{ca_s:,.0f} €</div>
          <div class='res-sub'>Marge : {mg_s:.2%} · {px_s*12:.2f} €/an/empl.</div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.preset == "ocp":
            st.caption(f"OCP réel = {d['tarif_reel_stockage_mois']:.2f} €/mois → CA = {d['tarif_reel_stockage_mois']*d['emplacements_vendus']*12:,.0f} €")

    with col2:
        st.markdown("**📥 Entrées palettes (MF1070)**")
        st.caption(f"Coût unitaire : {res['cu_entree']:.4f} € · Min : {res['prix_entree_min']:.4f} €")
        px_i = st.number_input("€ / palette entrante", min_value=0.0, max_value=50.0,
                    value=round(float(res["prix_entree_palette"]),4), step=0.001, key="px_i", format="%.4f",
                    help=f"Recommandé : {res['prix_entree_palette']:.4f} € · OCP réel : {d['tarif_reel_entree_palette']:.3f} €")
        ca_i = d["vol_entrees_palettes"] * px_i
        mg_i = (ca_i - res["cout_proc_in"]) / ca_i if ca_i > 0 else 0
        col = "#22d3a0" if mg_i >= 0 else "#ff5c6a"
        st.markdown(f"""<div class='res-card'>
          <div class='res-label'>CA entrées palettes</div><div style='color:{col};font-size:18px;font-weight:700;'>{ca_i:,.0f} €</div>
          <div class='res-sub'>Marge : {mg_i:.2%} · {d['vol_entrees_palettes']:,} pal × {px_i:.4f} €</div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.preset == "ocp":
            st.caption(f"OCP réel = {d['tarif_reel_entree_palette']:.3f} €/pal → CA = {d['tarif_reel_entree_palette']*d['vol_entrees_palettes']:,.0f} €")

    with col3:
        st.markdown("**📤 Sorties palettes (MF4010)**")
        st.caption(f"Coût unitaire : {res['cu_sortie']:.4f} € · Min : {res['prix_sortie_min']:.4f} €")
        px_o = st.number_input("€ / palette sortante", min_value=0.0, max_value=50.0,
                    value=round(float(res["prix_sortie_palette"]),4), step=0.001, key="px_o", format="%.4f",
                    help=f"Recommandé : {res['prix_sortie_palette']:.4f} € · OCP réel : {d['tarif_reel_sortie_palette']:.3f} €")
        ca_o = d["vol_sorties_palettes"] * px_o
        mg_o = (ca_o - res["cout_proc_out"]) / ca_o if ca_o > 0 else 0
        col = "#22d3a0" if mg_o >= 0 else "#ff5c6a"
        st.markdown(f"""<div class='res-card'>
          <div class='res-label'>CA sorties palettes</div><div style='color:{col};font-size:18px;font-weight:700;'>{ca_o:,.0f} €</div>
          <div class='res-sub'>Marge : {mg_o:.2%} · {d['vol_sorties_palettes']:,} pal × {px_o:.4f} €</div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.preset == "ocp":
            st.caption(f"OCP réel = {d['tarif_reel_sortie_palette']:.3f} €/pal → CA = {d['tarif_reel_sortie_palette']*d['vol_sorties_palettes']:,.0f} €")

    st.divider()
    st.markdown("### 🧩 Décomposition des coûts (Cost Split-up Polka)")
    cost_df = pd.DataFrame({
        "Poste de coût": ["🏭 Loyer charges incluses","🔧 Racks + Sécurité + Câblage",
                           "👷 Personnel opérationnel","📋 Personnel admin/encadr.",
                           "🏗️ Engins de manutention","🖥️ IT & WMS","━ TOTAL COÛTS"],
        "Montant (€)": [f"{res['loyer_total']:,.0f}",
                         f"{res['cout_rack_an']+res['cout_secu_an']+res['cout_cable_an']:,.0f}",
                         f"{res['cout_pers_op']:,.0f}", f"{res['cout_pers_adm']:,.0f}",
                         f"{res['cout_engins']:,.0f}", f"{res['cout_it_total']:,.0f}",
                         f"{res['cout_total']:,.0f}"],
        "Part": [f"{res['loyer_total']/max(res['cout_total'],1)*100:.1f}%",
                  f"{(res['cout_rack_an']+res['cout_secu_an']+res['cout_cable_an'])/max(res['cout_total'],1)*100:.1f}%",
                  f"{res['cout_pers_op']/max(res['cout_total'],1)*100:.1f}%",
                  f"{res['cout_pers_adm']/max(res['cout_total'],1)*100:.1f}%",
                  f"{res['cout_engins']/max(res['cout_total'],1)*100:.1f}%",
                  f"{res['cout_it_total']/max(res['cout_total'],1)*100:.1f}%",
                  "100,0%"],
    })
    st.dataframe(cost_df, use_container_width=True, hide_index=True)

    if st.session_state.preset == "ocp":
        st.markdown("### 🔄 Comparatif avec les tarifs réels OCP (Price Sheet Polka V202541)")
        cmp = pd.DataFrame({
            "Prestation": ["Stockage / empl. / mois","Entrée palette","Sortie palette",
                           "CA total","Coûts totaux","Bénéfice","Marge"],
            "OCP réel Polka": [f"{d['tarif_reel_stockage_mois']:.2f} €",f"{d['tarif_reel_entree_palette']:.3f} €",
                                f"{d['tarif_reel_sortie_palette']:.3f} €",f"{d['ca_reel_total']:,.0f} €",
                                f"{d['cout_reel_total']:,.0f} €",f"{d['profit_reel']:,.0f} €",f"{d['marge_reelle']:.2%}"],
            "Calculé Wizard": [f"{res['prix_stockage_mois']:.2f} €",f"{res['prix_entree_palette']:.3f} €",
                                f"{res['prix_sortie_palette']:.3f} €",f"{res['ca_total']:,.0f} €",
                                f"{res['cout_total']:,.0f} €",f"{res['profit']:,.0f} €",f"{res['marge_calc']:.2%}"],
        })
        st.dataframe(cmp, use_container_width=True, hide_index=True)

    st.divider()
    export = {"Projet": d["projet"],"Site": d["agence"],"CA_total": round(res["ca_total"],2),
              "Couts_totaux": round(res["cout_total"],2),"Benefice": round(res["profit"],2),
              "Marge_pct": round(res["marge_calc"]*100,2),
              "Prix_stockage_mois": round(res["prix_stockage_mois"],4),
              "Prix_entree_palette": round(res["prix_entree_palette"],4),
              "Prix_sortie_palette": round(res["prix_sortie_palette"],4),
              "ETP_total": round(res["fte_total"],2), "Cout_personnel": round(res["cout_pers_total"],2),
              "Cout_engins": round(res["cout_engins"],2), "Cout_entrepot": round(res["cout_entrepot"],2)}
    st.download_button("⬇️ Télécharger résultats JSON", json.dumps(export,indent=2,ensure_ascii=False),
                        f"polka_{d['projet'] or 'projet'}.json","application/json",type="primary")
    nav(6)

# ════════════════════════════════════════════════════════
# ÉTAPE 7 — SENSIBILITÉ
# ════════════════════════════════════════════════════════
elif st.session_state.step == 7:
    hdr(7, "📉", "Analyse de Sensibilité & Scénarios",
        "Impact des variations sur la marge — seuil de rentabilité et simulateur de scénarios.")

    res = calculer(d)

    st.markdown("### 📊 Tableau de sensibilité (±20%)")
    help_box("""Simule l'effet d'une variation de ±20% sur trois leviers :
    <strong>Volumes</strong> (palettes IN/OUT), <strong>Loyer</strong> (m²/mois), <strong>Salaires</strong> (bruts annuels).
    Les coûts fixes restent constants dans chaque simulation.""")

    rows = []
    for v in [-20,-15,-10,-5,0,5,10,15,20]:
        f = 1 + v/100
        dv = deepcopy(d); dv["vol_entrees_palettes"]=int(d["vol_entrees_palettes"]*f); dv["vol_sorties_palettes"]=int(d["vol_sorties_palettes"]*f)
        rv = calculer(dv)
        dl = deepcopy(d); dl["loyer_m2_mois"]=d["loyer_m2_mois"]*f
        rl = calculer(dl)
        ds = deepcopy(d); ds["salaire_operationnel"]=int(d["salaire_operationnel"]*f); ds["salaire_admin"]=int(d["salaire_admin"]*f)
        rs = calculer(ds)
        rows.append({"Variation":f"{v:+d}%",
                     "Marge (volumes)":f"{rv['marge_calc']:.2%}","Profit volumes (€)":f"{rv['profit']:,.0f}",
                     "Marge (loyer)":f"{rl['marge_calc']:.2%}","Profit loyer (€)":f"{rl['profit']:,.0f}",
                     "Marge (salaires)":f"{rs['marge_calc']:.2%}","Profit salaires (€)":f"{rs['profit']:,.0f}"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 🎛️ Simulateur de scénario personnalisé")
    c1,c2,c3,c4 = st.columns(4)
    with c1: sv = st.slider("📦 Volumes (%)", -50, 50, 0, 5)
    with c2: sl = st.slider("🏭 Loyer (%)", -50, 100, 0, 5)
    with c3: ss = st.slider("👷 Salaires (%)", -30, 50, 0, 5)
    with c4: sm = st.slider("🎯 Marge cible (%)", 0, 25, int(d["marge_cible"]*100), 1)

    dsim = deepcopy(d)
    dsim["vol_entrees_palettes"]  = int(d["vol_entrees_palettes"]  * (1+sv/100))
    dsim["vol_sorties_palettes"]  = int(d["vol_sorties_palettes"]  * (1+sv/100))
    dsim["loyer_m2_mois"]         = d["loyer_m2_mois"] * (1+sl/100)
    dsim["salaire_operationnel"]  = int(d["salaire_operationnel"]  * (1+ss/100))
    dsim["salaire_admin"]         = int(d["salaire_admin"]         * (1+ss/100))
    dsim["marge_cible"]           = sm/100
    rsim = calculer(dsim)
    rbase = calculer(d)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("CA simulé",       f"{rsim['ca_total']:,.0f} €",    delta=f"{rsim['ca_total']-rbase['ca_total']:+,.0f} €")
    with c2: st.metric("Coûts simulés",   f"{rsim['cout_total']:,.0f} €",  delta=f"{rsim['cout_total']-rbase['cout_total']:+,.0f} €", delta_color="inverse")
    with c3: st.metric("Bénéfice simulé", f"{rsim['profit']:,.0f} €",      delta=f"{rsim['profit']-rbase['profit']:+,.0f} €")
    with c4: st.metric("Marge simulée",   f"{rsim['marge_calc']:.2%}",     delta=f"{rsim['marge_calc']-rbase['marge_calc']:+.2%}")

    mc2 = "#22d3a0" if rsim["marge_calc"] >= dsim["marge_cible"] else "#ff5c6a"
    msg = "✅ Objectif atteint" if rsim["marge_calc"] >= dsim["marge_cible"] else f"⚠️ Manque {(dsim['marge_cible']-rsim['marge_calc'])*rsim['ca_total']:,.0f} €/an pour atteindre {dsim['marge_cible']:.0%}"
    st.markdown(f"<div class='res-card'><span style='color:{mc2};font-weight:700;font-size:14px;'>{msg}</span></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📍 Seuil de rentabilité (Point mort)")
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("CA au seuil", f"{res['seuil_rentabilite']:,.0f} €", help="CA minimum pour couvrir tous les coûts fixes")
    with c2: st.metric("CA actuel",   f"{res['ca_total']:,.0f} €")
    with c3:
        cushion = (res["ca_total"] - res["seuil_rentabilite"]) / max(res["ca_total"],1) * 100
        st.metric("Marge de sécurité", f"{cushion:.1f}%",
                  delta="✅ Solide" if cushion > 20 else ("⚠️ Correct" if cushion > 5 else "🔴 Fragile"))
    nav(7)

st.markdown("""<div style='text-align:center;padding:16px 0 6px;color:#2d3155;font-size:11px;
     border-top:1px solid #1a1d2e;margin-top:20px;'>
  Polka Wizard v2 · Modèle Polka V202541 · OCP Morocco · Dachser Contract Logistics
</div>""", unsafe_allow_html=True)
