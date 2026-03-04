import streamlit as st
import math

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Polka MUP — Scientific Costing Wizard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE STRINGS
# ─────────────────────────────────────────────────────────────────────────────
LANG = {
    "EN": {
        "step_labels": [
            "1 · Project Info",
            "2 · Branch Basic Data",
            "3 · Warehouse",
            "4 · Personnel",
            "5 · Industrial Trucks",
            "6 · Processes & Volumes",
            "7 · Price Sheet",
            "8 · Results",
        ],
        "s1_title": "Project Information",
        "s1_project": "Project", "s1_branch": "Branch",
        "s1_project_leader": "Project Leader", "s1_country_org": "Country Organisation",
        "s1_country": "Country", "s1_date": "Data Period",
        "s1_business_unit": "Business Unit", "s1_customer": "Customer Name",
        "s1_sector": "Sector / Description",
        "s2_title": "Branch Basic Data",
        "s2_working_days": "Yearly Working Days",
        "s2_interest_rate": "Internal Interest Rate (for Investments) %",
        "s2_target_margin": "Target Profit Margin %",
        "s2_wms": "Warehouse Management System (WMS)",
        "s2_wms_alloc": "WMS Allocation %",
        "s2_fluctuation": "Fluctuation Rate %",
        "s2_deduction_reserve": "Deduction of the Operative Reserve %",
        "s2_failure_rate": "Failure Rate of the Equipment %",
        "s2_exchange_rate": "Exchange Rate (1 MAD = ? EUR)",
        "s2_contract_years": "Contract Period in Years",
        "s2_ho_alloc": "HO Allocation %",
        "s2_term_payment": "Term of Payment in Days",
        "s2_domino_alloc": "DOMINO Allocation per Parcel (Code P1) %",
        "s2_premium_order": "Premium Rate per Order (€)",
        "s3_title": "Warehouse",
        "s3_wh_surface": "Warehouse Surface (m²)",
        "s3_wh_height": "Warehouse Height (m)",
        "s3_gross_loc": "No. of Gross Pallet Locations",
        "s3_ded_zone": "Deduction Inbound/Outbound Zone",
        "s3_ded_unusable": "Deduction Unusable Locations",
        "s3_op_reserve": "Operative Reserve %",
        "s3_net_loc": "Net Pallet Locations (Sellable)",
        "s3_rent_mad": "Rent (MAD/m²/month)",
        "s3_charges": "Additional Charges (MAD/m²/month)",
        "s3_idilite": "Tax / Idilité (MAD/m²/month)",
        "s3_total_rent_mad": "Total Rent (MAD/m²/month)",
        "s3_total_rent_eur": "Total Rent (€/m²/month)",
        "s3_racking_ppl": "Racking System (€/PPL)",
        "s3_racking_qty": "Racking Quantity (PPL)",
        "s3_security": "Security (€/m²)",
        "s3_cabling": "Cabling (€/m²)",
        "s3_lower_shelf_qty": "Lower Shelves (pieces)",
        "s3_lower_shelf_price": "Lower Shelf price (€/piece)",
        "s3_grating_qty": "Caillebotis (pieces)",
        "s3_grating_price": "Caillebotis (€/piece)",
        "s3_invest_depr_years": "Depreciation Years",
        "s3_peak_pal": "Peak Pallet Need",
        "s3_avg_pal": "Average Pallet Need",
        "s4_title": "Personnel",
        "s4_op_title": "Logistics Operatives",
        "s4_adm_title": "Office / Administrative",
        "s4_mgmt_title": "Management",
        "s4_role": "Role", "s4_qty": "Qty (FTE)", "s4_salary": "Gross Annual Salary (€)",
        "s4_illness": "Illness %", "s4_holidays": "Holidays (days)",
        "s4_weekly_h": "Weekly h", "s4_allowance": "Allowance %",
        "s5_title": "Industrial Trucks",
        "s5_truck": "Truck Type", "s5_qty": "Qty",
        "s5_rent_purchase": "Rent / Purchase",
        "s5_price": "Price incl. Battery (€)",
        "s5_battery": "Battery Change (€)",
        "s5_depr_years": "Depr. Years",
        "s6_title": "Processes & Volumes",
        "s6_inbound_title": "Inbound",
        "s6_picking_title": "Picking",
        "s6_relocation_title": "Relocation",
        "s6_outbound_title": "Removal of Full Pallets",
        "s6_loading_title": "Loading",
        "s6_storage_title": "Storage",
        "s6_active": "Active", "s6_volume": "Annual Volume",
        "s6_unit": "Unit", "s6_pg": "Per h (Productive)", "s6_pn": "Per h (Payed)",
        "s7_title": "Price Sheet",
        "s7_storage_price": "Storage Price (€/location/month)",
        "s7_fixed_monthly": "Fixed Monthly Lump Sum (€/month)",
        "s7_process": "Process", "s7_unit": "Billing Unit",
        "s7_price": "Price per Unit (€)", "s7_volume": "Volume",
        "s7_ca": "Annual Turnover (€)", "s7_cost": "Annual Cost (€)", "s7_margin": "Margin %",
        "s8_title": "Results & Summary",
        "s8_ca": "Total Annual Turnover (€)", "s8_cost": "Total Annual Costs (€)",
        "s8_profit": "Profit (€)", "s8_margin": "Profit Margin %",
        "s8_target": "Target Margin %", "s8_gap": "Gap vs Target",
        "btn_next": "Next →", "btn_prev": "← Back", "btn_calc": "Calculate",
        "sb_hint": "💡 Pre-filled from AKZO NOBEL reference project (MUP 2021)",
        "cost_wh": "Warehouse", "cost_pers": "Personnel", "cost_trucks": "Industrial Trucks",
        "annual_rent": "Annual Rent", "racking": "Racking", "security_cabling": "Security + Cabling",
        "other_inv": "Other Investments", "total": "TOTAL",
        "net_locations": "Net Pallet Locations", "avg_storage": "Average Pallets in Storage",
        "social_charges": "Social Charges %",
        "variable_costs": "Variable Costs", "fixed_costs": "Fixed Costs",
        "cost_breakdown": "Cost Breakdown", "revenue_breakdown": "Revenue Breakdown",
        "project_summary": "Project Summary",
    },
    "FR": {
        "step_labels": [
            "1 · Infos Projet",
            "2 · Données de Base",
            "3 · Entrepôt",
            "4 · Personnel",
            "5 · Engins",
            "6 · Processus & Volumes",
            "7 · Grille Tarifaire",
            "8 · Résultats",
        ],
        "s1_title": "Informations Projet",
        "s1_project": "Projet", "s1_branch": "Agence",
        "s1_project_leader": "Chef de Projet", "s1_country_org": "Organisation Pays",
        "s1_country": "Pays", "s1_date": "Période des Données",
        "s1_business_unit": "Business Unit", "s1_customer": "Nom du Client",
        "s1_sector": "Secteur / Description",
        "s2_title": "Données de Base Agence",
        "s2_working_days": "Jours Ouvrés / An",
        "s2_interest_rate": "Taux d'Intérêt Interne %",
        "s2_target_margin": "Marge Cible %",
        "s2_wms": "Système WMS",
        "s2_wms_alloc": "Allocation WMS %",
        "s2_fluctuation": "Taux de Fluctuation %",
        "s2_deduction_reserve": "Déduction Réserve Opérative %",
        "s2_failure_rate": "Taux de Panne des Engins %",
        "s2_exchange_rate": "Taux de Change (1 MAD = ? EUR)",
        "s2_contract_years": "Durée du Contrat (années)",
        "s2_ho_alloc": "Allocation HO %",
        "s2_term_payment": "Délai de Paiement (jours)",
        "s2_domino_alloc": "Allocation DOMINO par Colis (Code P1) %",
        "s2_premium_order": "Taux de Prime par Commande (€)",
        "s3_title": "Entrepôt",
        "s3_wh_surface": "Surface Entrepôt (m²)",
        "s3_wh_height": "Hauteur Entrepôt (m)",
        "s3_gross_loc": "Nb d'Emplacements Bruts",
        "s3_ded_zone": "Déduction Zone Entrée/Sortie",
        "s3_ded_unusable": "Déduction Empl. Non Utilisables",
        "s3_op_reserve": "Réserve Opérative %",
        "s3_net_loc": "Emplacements Nets (Vendables)",
        "s3_rent_mad": "Loyer (MAD/m²/mois)",
        "s3_charges": "Charges (MAD/m²/mois)",
        "s3_idilite": "Idilité/Taxes (MAD/m²/mois)",
        "s3_total_rent_mad": "Loyer Total (MAD/m²/mois)",
        "s3_total_rent_eur": "Loyer Total (€/m²/mois)",
        "s3_racking_ppl": "Rayonnage (€/emplacement)",
        "s3_racking_qty": "Quantité Rayonnage (PPL)",
        "s3_security": "Sécurité (€/m²)",
        "s3_cabling": "Câblage (€/m²)",
        "s3_lower_shelf_qty": "Étagères Basses (pièces)",
        "s3_lower_shelf_price": "Étagères Basses (€/pièce)",
        "s3_grating_qty": "Caillebotis (pièces)",
        "s3_grating_price": "Caillebotis (€/pièce)",
        "s3_invest_depr_years": "Durée d'Amortissement (ans)",
        "s3_peak_pal": "Besoin Max Palettes",
        "s3_avg_pal": "Besoin Moyen Palettes",
        "s4_title": "Personnel",
        "s4_op_title": "Opérationnels Logistiques",
        "s4_adm_title": "Administratifs / Bureau",
        "s4_mgmt_title": "Management",
        "s4_role": "Rôle", "s4_qty": "Qté (ETP)", "s4_salary": "Salaire Brut Annuel (€)",
        "s4_illness": "Absence %", "s4_holidays": "Congés (jours)",
        "s4_weekly_h": "Heures Hebdo", "s4_allowance": "Tolérance %",
        "s5_title": "Engins de Manutention",
        "s5_truck": "Type d'Engin", "s5_qty": "Qté",
        "s5_rent_purchase": "Location / Achat",
        "s5_price": "Prix incl. Batterie (€)",
        "s5_battery": "Batterie Rechange (€)",
        "s5_depr_years": "Amort. (ans)",
        "s6_title": "Processus & Volumes",
        "s6_inbound_title": "Réception (Inbound)",
        "s6_picking_title": "Préparation (Picking)",
        "s6_relocation_title": "Réapprovisionnement",
        "s6_outbound_title": "Sortie Palette Complète",
        "s6_loading_title": "Chargement (Loading)",
        "s6_storage_title": "Stockage",
        "s6_active": "Actif", "s6_volume": "Volume Annuel",
        "s6_unit": "Unité", "s6_pg": "Prod. Brute / h", "s6_pn": "Prod. Nette / h (Payée)",
        "s7_title": "Grille Tarifaire",
        "s7_storage_price": "Tarif Stockage (€/emplacement/mois)",
        "s7_fixed_monthly": "Forfait Fixe Mensuel (€/mois)",
        "s7_process": "Processus", "s7_unit": "Unité de Facturation",
        "s7_price": "Tarif Unitaire (€)", "s7_volume": "Volume",
        "s7_ca": "CA Annuel (€)", "s7_cost": "Coût Annuel (€)", "s7_margin": "Marge %",
        "s8_title": "Résultats & Synthèse",
        "s8_ca": "CA Total Annuel (€)", "s8_cost": "Coûts Totaux Annuels (€)",
        "s8_profit": "Profit (€)", "s8_margin": "Marge Réelle %",
        "s8_target": "Marge Cible %", "s8_gap": "Écart vs Cible",
        "btn_next": "Suivant →", "btn_prev": "← Retour", "btn_calc": "Calculer",
        "sb_hint": "💡 Pré-rempli depuis le projet référence AKZO NOBEL (MUP 2021)",
        "cost_wh": "Entrepôt", "cost_pers": "Personnel", "cost_trucks": "Engins",
        "annual_rent": "Loyer Annuel", "racking": "Rayonnage", "security_cabling": "Sécu + Câblage",
        "other_inv": "Autres Investissements", "total": "TOTAL",
        "net_locations": "Emplacements Nets", "avg_storage": "Palettes Moyennes en Stock",
        "social_charges": "Charges Sociales %",
        "variable_costs": "Coûts Variables", "fixed_costs": "Coûts Fixes",
        "cost_breakdown": "Décomposition des Coûts", "revenue_breakdown": "Détail du CA",
        "project_summary": "Fiche Projet",
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# REFERENCE DATA — AKZO NOBEL (exact values from MUP Excel)
# ─────────────────────────────────────────────────────────────────────────────
AKZO = {
    "project": "AKZO NOBEL", "branch": "MA-Mohammedia (580)",
    "project_leader": "Tayeb Sbihi", "country_org": "Morocco",
    "country": "Marocco", "business_unit": "ELS",
    "customer": "AKZO NOBEL", "sector": "Peintures & Revêtements",
    "working_days": 272, "interest_rate": 9.0, "target_margin": 20.0,
    "wms": "MIKADO", "wms_alloc": 1.7, "fluctuation": 0.0,
    "deduction_reserve": 10.0, "failure_rate": 5.0,
    "exchange_rate": 0.094, "contract_years": 3,
    "ho_alloc": 0.8625, "term_payment": 30,
    "domino_alloc": 1.7, "premium_order": 0.15,
    "wh_surface": 1600, "wh_height": 10.0,
    "gross_loc": 1741, "ded_zone": 0, "ded_unusable": 0,
    "op_reserve": 10.0, "net_loc": 1567,
    "rent_mad": 44.5, "charges_mad": 3.5, "idilite_mad": 5.04,
    "total_rent_mad": 53.04, "total_rent_eur": 5.1772322,
    "racking_ppl": 35.0, "racking_qty": 1741,
    "security_eur_m2": 5.0, "cabling_eur_m2": 5.0,
    "lower_shelf_qty": 110, "lower_shelf_price": 38.0,
    "grating_qty": 550, "grating_price": 20.0,
    "invest_depr_years": 12, "peak_pal": 2413, "avg_pal": 1772,
    "social_charges_pct": 14.2,
}

AKZO_PERSONNEL_OP = [
    {"role_en": "Picker",             "role_fr": "Préparateur",           "qty": 1,   "salary": 7964,  "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "allowance": 9.0, "pct_fixed": 0.0},
    {"role_en": "Forklift driver",    "role_fr": "Cariste",               "qty": 1,   "salary": 7964,  "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "allowance": 9.0, "pct_fixed": 0.0},
    {"role_en": "Loader",             "role_fr": "Chargeur",              "qty": 1,   "salary": 6500,  "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "allowance": 9.0, "pct_fixed": 0.0},
    {"role_en": "Unloader",           "role_fr": "Déchargeur",            "qty": 0,   "salary": 6500,  "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "allowance": 9.0, "pct_fixed": 0.0},
    {"role_en": "Inbound controller", "role_fr": "Contrôleur Réception",  "qty": 0,   "salary": 6500,  "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "allowance": 9.0, "pct_fixed": 0.0},
    {"role_en": "Warehouse Skilled Employee", "role_fr": "Agent Logistique Qualifié", "qty": 0, "salary": 13722, "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "allowance": 9.0, "pct_fixed": 0.0},
    {"role_en": "Team Leader (Process Relevant)", "role_fr": "Team Leader (Opérationnel)", "qty": 0, "salary": 13722, "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "allowance": 9.0, "pct_fixed": 0.0},
]

AKZO_PERSONNEL_ADM = [
    {"role_en": "Team Leader (Not Process Relevant)", "role_fr": "Team Leader (Encadrement)", "qty": 1,   "salary": 13722, "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "pct_fixed": 1.0},
    {"role_en": "Stock manager",                      "role_fr": "Gestionnaire de Stock",     "qty": 0.5, "salary": 13722, "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "pct_fixed": 1.0},
    {"role_en": "Site assistant",                     "role_fr": "Assistant de Site",         "qty": 0,   "salary": 9818,  "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "pct_fixed": 1.0},
    {"role_en": "Inbound Administration",             "role_fr": "Administratif Entrée",      "qty": 0,   "salary": 13722, "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "pct_fixed": 1.0},
    {"role_en": "Outbound Administration",            "role_fr": "Administratif Sortie",      "qty": 0,   "salary": 13722, "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "pct_fixed": 1.0},
    {"role_en": "Outbound controller",                "role_fr": "Contrôleur Sortie",         "qty": 0,   "salary": 6500,  "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "pct_fixed": 1.0},
    {"role_en": "HSE Manager",                        "role_fr": "Responsable HSE",           "qty": 0,   "salary": 13722, "illness": 4.97, "holidays": 25, "weekly_h": 44, "paid_h": 8, "pct_fixed": 1.0},
]

AKZO_PERSONNEL_MGMT = [
    {"role_en": "Operations Manager",         "role_fr": "Responsable Opérations", "qty": 0.15, "salary": 31000, "pct_fixed": 1.0},
    {"role_en": "CL-Consultant / DEWO",       "role_fr": "Consultant CL / DEWO",   "qty": 0.20, "salary": 25000, "pct_fixed": 1.0},
    {"role_en": "Contract Logistics Manager", "role_fr": "Directeur Logistique",   "qty": 0.0,  "salary": 65243, "pct_fixed": 1.0},
]

AKZO_TRUCKS = [
    {"code": "FZ0010", "name_en": "Hand Pallet Truck",              "name_fr": "Transpalette Manuel",          "qty": 0, "rent_purchase": "Purchase",      "price": 375,       "battery": 0,    "depr_years": 6, "pct_fixed": 1.0},
    {"code": "FZ0020", "name_en": "Picking Trolley",                "name_fr": "Chariot de Picking",           "qty": 0, "rent_purchase": "Purchase",      "price": 700,       "battery": 0,    "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0030", "name_en": "Double-Deck Loader",             "name_fr": "Chargeur Double Plateau",      "qty": 0, "rent_purchase": "External Rent", "price": 9344,      "battery": 2126, "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0040", "name_en": "Fast Mover",                     "name_fr": "Fast Mover",                   "qty": 1, "rent_purchase": "External Rent", "price": 10606.05,  "battery": 2126, "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0050", "name_en": "Horizontal Order Picker",        "name_fr": "Préparateur Horizontal",       "qty": 1, "rent_purchase": "External Rent", "price": 11956.35,  "battery": 2323, "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0060", "name_en": "Vertical Order Picker 1.20m",    "name_fr": "Préparateur Vertical 1.20m",   "qty": 0, "rent_purchase": "External Rent", "price": 11664.45,  "battery": 2566, "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0070", "name_en": "Front Loader",                   "name_fr": "Chariot Frontal",              "qty": 0, "rent_purchase": "External Rent", "price": 22644.3,   "battery": 5072, "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0080", "name_en": "Reach Truck <= 8m Lift Height",  "name_fr": "Chariot Rétractable ≤ 8m",    "qty": 0, "rent_purchase": "External Rent", "price": 31089.45,  "battery": 6099, "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0085", "name_en": "Reach Truck > 8m Lift Height",   "name_fr": "Chariot Rétractable > 8m",    "qty": 1, "rent_purchase": "External Rent", "price": 44618.70,  "battery": 6099, "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0090", "name_en": "Narrow-Aisle Truck",             "name_fr": "Chariot Allée Étroite",        "qty": 0, "rent_purchase": "External Rent", "price": 95000,     "battery": 8000, "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0100", "name_en": "Floor Sweeper (wet)",            "name_fr": "Autolaveuse",                  "qty": 0, "rent_purchase": "External Rent", "price": 21500,     "battery": 0,    "depr_years": 8, "pct_fixed": 0.5},
    {"code": "FZ0110", "name_en": "Floor Sweeper (dry)",            "name_fr": "Balayeuse",                    "qty": 0, "rent_purchase": "External Rent", "price": 15650,     "battery": 0,    "depr_years": 8, "pct_fixed": 0.5},
    {"code": "FZ0120", "name_en": "Clamp Truck",                    "name_fr": "Chariot à Pince",              "qty": 0, "rent_purchase": "External Rent", "price": 0,         "battery": 0,    "depr_years": 6, "pct_fixed": 0.5},
    {"code": "FZ0130", "name_en": "Nacelle (Work Platform)",        "name_fr": "Nacelle",                      "qty": 0, "rent_purchase": "External Rent", "price": 0,         "battery": 0,    "depr_years": 6, "pct_fixed": 0.5},
]

AKZO_PROCESSES = [
    # INBOUND
    {"code": "WE1",  "group": "inbound",    "name_en": "Inbound Full Pallet (Unloading not double-stacked)", "name_fr": "Réception Palette Homogène (Déchargement)", "active": True,  "volume": 2733,  "unit_en": "Delivered Inbound - Pallets", "unit_fr": "Palettes Entrée",          "prod_gross": 49.49,  "prod_net": 42.56},
    {"code": "WE1s", "group": "inbound",    "name_en": "Stock-in Full Pallet (Stocking Without Transfer Zone)", "name_fr": "Mise en Stock Palette Homogène",         "active": True,  "volume": 2733,  "unit_en": "Stock-in Inbound - Pallets", "unit_fr": "Palettes Mise en Stock",   "prod_gross": 30.67,  "prod_net": 26.38},
    {"code": "WE2",  "group": "inbound",    "name_en": "Inbound Mixed Pallet (Unloading)",                    "name_fr": "Réception Palette Hétérogène",             "active": True,  "volume": 255,   "unit_en": "Delivered Inbound - Pallets","unit_fr": "Palettes Hétérogènes",     "prod_gross": 49.49,  "prod_net": 42.56},
    {"code": "WE2s", "group": "inbound",    "name_en": "Separation of Mixed Pallets",                         "name_fr": "Constitution Palette Homogène (Séparation)","active": True, "volume": 8925,  "unit_en": "Picking Unit Inbound Loose", "unit_fr": "Colis Éclatés",            "prod_gross": 220.83, "prod_net": 189.91},
    {"code": "WE4",  "group": "inbound",    "name_en": "Retour Vrac (Loose Unloading)",                       "name_fr": "Retour Vrac (Déchargement Vrac)",          "active": True,  "volume": 3245,  "unit_en": "Picking Unit Inbound Loose", "unit_fr": "Colis Vrac",               "prod_gross": 124.33, "prod_net": 106.92},
    # PICKING
    {"code": "KO1",  "group": "picking",    "name_en": "Picking ASC (Picking Pallet - Manual Wrapping)",      "name_fr": "Picking ASC (Colis/Article)",              "active": True,  "volume": 45131, "unit_en": "Picks",                      "unit_fr": "Picks",                    "prod_gross": 155.54, "prod_net": 133.77},
    {"code": "KO2",  "group": "picking",    "name_en": "Picking MPY & Powder (Picking Pallet - Manual Wrapping)","name_fr": "Picking MPY & Poudre",                 "active": True,  "volume": 9529,  "unit_en": "Picks",                      "unit_fr": "Picks",                    "prod_gross": 46.99,  "prod_net": 40.41},
    # RELOCATION
    {"code": "UL1",  "group": "relocation", "name_en": "Replenishment Picking ASC (Partial Reloc. by Forklift Without TZ)", "name_fr": "Réappro. Picking ASC (Relocation Partielle)", "active": True, "volume": 5319,  "unit_en": "Partial Relocation Pallets", "unit_fr": "Palettes Réappro",         "prod_gross": 16.48,  "prod_net": 14.18},
    {"code": "UL2",  "group": "relocation", "name_en": "Replenishment Picking MPY & POWDER (Reloc. Without TZ)","name_fr": "Réappro. Picking MPY (Relocation Sans ZT)", "active": True, "volume": 243,   "unit_en": "Relocation Pallets",         "unit_fr": "Palettes Relocation",      "prod_gross": 16.82,  "prod_net": 14.47},
    # OUTBOUND
    {"code": "AV1",  "group": "outbound",   "name_en": "Outbound Full Pallet (Without Transfer Zone)",        "name_fr": "Sortie Palette Complète (Sans Zone Transit)", "active": True, "volume": 2613,  "unit_en": "Full Pallets",               "unit_fr": "Palettes Complètes",       "prod_gross": 24.09,  "prod_net": 20.72},
    # LOADING
    {"code": "VL1",  "group": "loading",    "name_en": "Loading Pallets (Loading Pallets not Double-Stacked)", "name_fr": "Chargement Palettes",                      "active": True,  "volume": 3713,  "unit_en": "Loaded Pallet",              "unit_fr": "Palettes Chargées",        "prod_gross": 25.22,  "prod_net": 21.69},
    {"code": "VL4",  "group": "loading",    "name_en": "Loading Parcels (Loose Loading)",                     "name_fr": "Chargement Colis (Chargement Vrac)",       "active": True,  "volume": 6869,  "unit_en": "Loose Loaded Cartons",       "unit_fr": "Colis Chargés",            "prod_gross": 48.49,  "prod_net": 41.71},
]

AKZO_PRICES = [
    {"code": "storage", "name_en": "Warehouse Costs — Storage",       "name_fr": "Coûts Entrepôt — Stockage",        "billing_en": "Pallet Location / Month", "billing_fr": "Emplacement / Mois",      "price": 7.64,    "cost_unit": 6.0636},
    {"code": "fixed",   "name_en": "Fixed Costs — Monthly Lump Sum",  "name_fr": "Coûts Fixes — Forfait Mensuel",    "billing_en": "Month",                   "billing_fr": "Mois",                    "price": 6228.92, "cost_unit": 4983.14},
    {"code": "WE1",     "name_en": "Inbound Full Pallet",              "name_fr": "Réception Palette Homogène",       "billing_en": "Delivered Inbound - Pallets","billing_fr": "Palette",               "price": 2.2509,  "cost_unit": 1.8007},
    {"code": "WE2",     "name_en": "Inbound Mixed Pallet",             "name_fr": "Réception Palette Hétérogène",     "billing_en": "Stock-in Inbound - Pallets","billing_fr": "Palette Stockée",        "price": 2.9329,  "cost_unit": 2.3463},
    {"code": "WE4",     "name_en": "Retour Vrac",                      "name_fr": "Retour Vrac",                      "billing_en": "Picking Unit Inbound Loose","billing_fr": "Unité Vrac",             "price": 0.3632,  "cost_unit": 0.2906},
    {"code": "KO1",     "name_en": "Picking ASC",                      "name_fr": "Picking ASC",                      "billing_en": "Picks",                   "billing_fr": "Picks",                   "price": 0.5268,  "cost_unit": 0.4214},
    {"code": "KO2",     "name_en": "Picking MPY & Powder",             "name_fr": "Picking MPY & Poudre",             "billing_en": "Picks",                   "billing_fr": "Picks",                   "price": 0.8137,  "cost_unit": 0.6510},
    {"code": "AV1",     "name_en": "Full Pallet Removal",              "name_fr": "Sortie Palette Complète",          "billing_en": "Full Pallets",            "billing_fr": "Palettes Complètes",      "price": 1.7916,  "cost_unit": 1.4333},
    {"code": "VL1",     "name_en": "Loading Pallets",                  "name_fr": "Chargement Palettes",              "billing_en": "Loaded Pallet",           "billing_fr": "Palette Chargée",         "price": 1.3283,  "cost_unit": 1.0626},
    {"code": "VL4",     "name_en": "Loading Parcels",                  "name_fr": "Chargement Colis",                 "billing_en": "Loose Loaded Cartons",    "billing_fr": "Colis Chargé",            "price": 0.6907,  "cost_unit": 0.5526},
]

# ─────────────────────────────────────────────────────────────────────────────
# CALCULATION ENGINE (mirrors MUP Excel formulas)
# ─────────────────────────────────────────────────────────────────────────────

def calc_net_locations(gross, ded_zone, ded_unusable, op_reserve_pct):
    avail = gross - ded_zone - ded_unusable
    return round(avail * (1 - op_reserve_pct / 100))

def calc_invest_annual(invest_total, interest_rate_pct, depr_years, maintenance_pct=1.0):
    """Annual cost of an investment: depreciation + average interest + maintenance."""
    r = interest_rate_pct / 100
    depr = invest_total / depr_years
    interest = invest_total * r * (depr_years + 1) / (2 * depr_years)
    maintenance = invest_total * maintenance_pct / 100
    return depr + interest + maintenance

def calc_warehouse_costs(d):
    surf = d.get("wh_surface", 1600)
    rent_eur = d.get("total_rent_eur", 5.177)
    r = d.get("interest_rate", 9.0)
    dy = d.get("invest_depr_years", 12)

    # Office (100 m²) rent + office equipment
    office_rent = 100 * rent_eur * 12
    office_equip_invest = 1.85 * 1364  # 1.85 FTE admin × 1364€
    office_equip_annual = calc_invest_annual(office_equip_invest, r, 12, 1.0)
    office_total = office_rent + office_equip_annual

    # Warehouse rent
    wh_rent = surf * rent_eur * 12

    # Racking
    rack_invest = d.get("racking_ppl", 35) * d.get("racking_qty", 1741)
    rack_annual = calc_invest_annual(rack_invest, r, dy, 1.0)

    # Security
    sec_invest = d.get("security_eur_m2", 5) * surf
    sec_annual = calc_invest_annual(sec_invest, r, 5, 1.0)

    # Cabling
    cab_invest = d.get("cabling_eur_m2", 5) * surf
    cab_annual = calc_invest_annual(cab_invest, r, 5, 1.0)

    # Lower shelves
    ls_invest = d.get("lower_shelf_qty", 110) * d.get("lower_shelf_price", 38)
    ls_annual = calc_invest_annual(ls_invest, r, dy, 1.0) if ls_invest > 0 else 0

    # Caillebotis
    gr_invest = d.get("grating_qty", 550) * d.get("grating_price", 20)
    gr_annual = calc_invest_annual(gr_invest, r, dy, 1.0) if gr_invest > 0 else 0

    total = office_total + wh_rent + rack_annual + sec_annual + cab_annual + ls_annual + gr_annual
    return {
        "office": office_total,
        "rent": wh_rent,
        "racking": rack_annual,
        "security": sec_annual,
        "cabling": cab_annual,
        "shelves": ls_annual,
        "grating": gr_annual,
        "total": total,
    }

def calc_truck_annual(price, battery, qty, rent_purchase, depr_years, interest_rate):
    """MUP formula: for rented trucks, annualise total investment."""
    if qty == 0:
        return 0
    invest = (price + battery) * qty
    return calc_invest_annual(invest, interest_rate, depr_years, 2.0)

def calc_personnel_annual(salary, qty, social_pct):
    return salary * qty * (1 + social_pct / 100)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0
if "lang" not in st.session_state:
    st.session_state.lang = "FR"
if "currency" not in st.session_state:
    st.session_state.currency = "EUR"
if "period" not in st.session_state:
    st.session_state.period = "annual"   # "annual" | "monthly"
if "d" not in st.session_state:
    st.session_state.d = {}

def T(key):
    return LANG[st.session_state.lang].get(key, key)

def SL():
    return LANG[st.session_state.lang]["step_labels"]

def get(key, default=None):
    if key in st.session_state.d:
        return st.session_state.d[key]
    if key in AKZO:
        return AKZO[key]
    return default

def put(key, val):
    st.session_state.d[key] = val

# ── Currency helpers ──
def cur_symbol():
    return "MAD" if st.session_state.currency == "MAD" else "€"

def cur_rate():
    """Return the MAD→EUR conversion factor. If currency=MAD, no conversion (factor=1/fx to go EUR→MAD)."""
    fx = float(get("exchange_rate", 0.094))
    if st.session_state.currency == "MAD":
        return 1.0 / fx if fx > 0 else 10.638  # EUR→MAD
    return 1.0  # already in EUR

def to_display(eur_value):
    """Convert an EUR value to display currency."""
    return eur_value * cur_rate()

def from_display(display_value):
    """Convert a display-currency value back to EUR (for storage)."""
    r = cur_rate()
    return display_value / r if r != 0 else display_value

def fmt_cur(eur_value, decimals=0):
    """Format a EUR value in display currency."""
    v = to_display(eur_value)
    sym = cur_symbol()
    if decimals == 0:
        return f"{v:,.0f} {sym}"
    else:
        return f"{v:,.{decimals}f} {sym}"

def cur_label(base_label):
    """Replace € symbol in a label with the active currency symbol."""
    sym = cur_symbol()
    return base_label.replace("€", sym).replace("EUR", sym)

def period_factor():
    """1 for annual, 1/12 for monthly."""
    return 1.0 if st.session_state.period == "annual" else 1.0 / 12.0

def period_label():
    """Human label for selected period."""
    lang = st.session_state.lang
    if st.session_state.period == "annual":
        return "Annuel" if lang == "FR" else "Annual"
    return "Mensuel" if lang == "FR" else "Monthly"

def fmt_period(eur_annual, decimals=0):
    """Format a EUR annual value → display currency × period factor."""
    v = to_display(eur_annual * period_factor())
    sym = cur_symbol()
    if decimals == 0:
        return f"{v:,.0f} {sym}"
    return f"{v:,.{decimals}f} {sym}"

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📦 Polka MUP Wizard")

    lang = st.radio("🌐 Language / Langue", ["FR", "EN"], horizontal=True,
                    index=0 if st.session_state.lang == "FR" else 1)
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        st.rerun()

    currency = st.radio("💱 Devise / Currency", ["EUR (€)", "MAD (درهم)"], horizontal=True,
                        index=0 if st.session_state.currency == "EUR" else 1)
    new_cur = "EUR" if currency.startswith("EUR") else "MAD"
    if new_cur != st.session_state.currency:
        st.session_state.currency = new_cur
        st.rerun()

    period_choice = st.radio(
        "📅 Vue / View",
        ["Annuel / Annual", "Mensuel / Monthly"],
        horizontal=True,
        index=0 if st.session_state.period == "annual" else 1
    )
    new_period = "annual" if period_choice.startswith("Annuel") else "monthly"
    if new_period != st.session_state.period:
        st.session_state.period = new_period
        st.rerun()

    # Show live exchange rate info
    fx = float(get("exchange_rate", 0.094))
    if st.session_state.currency == "MAD":
        st.caption(f"1 € = {1/fx:,.2f} MAD  (taux : {fx:.4f})")
    else:
        st.caption(f"1 MAD = {fx:.4f} €")

    st.markdown("---")
    for i, label in enumerate(SL()):
        is_cur = i == st.session_state.step
        if st.button(
            ("▶ " if is_cur else "  ") + label,
            key=f"nav_{i}", use_container_width=True,
            type="primary" if is_cur else "secondary"
        ):
            st.session_state.step = i
            st.rerun()

    st.markdown("---")
    st.info(T("sb_hint"))

# ─────────────────────────────────────────────────────────────────────────────
# NAV + PROGRESS
# ─────────────────────────────────────────────────────────────────────────────
def nav(step_idx, total=8):
    c1, _, c2 = st.columns([1, 4, 1])
    with c1:
        if step_idx > 0:
            if st.button(T("btn_prev"), use_container_width=True):
                st.session_state.step -= 1; st.rerun()
    with c2:
        if step_idx < total - 1:
            if st.button(T("btn_next"), use_container_width=True, type="primary"):
                st.session_state.step += 1; st.rerun()

def prog(i, total=8):
    st.progress((i + 1) / total, text=f"**{SL()[i]}** — {i+1}/{total}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — PROJECT INFO
# ─────────────────────────────────────────────────────────────────────────────
def step1():
    st.header(f"📋  {T('s1_title')}")
    prog(0)
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        for k, lk in [("project", "s1_project"), ("customer", "s1_customer"),
                      ("project_leader", "s1_project_leader"), ("branch", "s1_branch"),
                      ("business_unit", "s1_business_unit")]:
            put(k, st.text_input(T(lk), value=str(get(k, ""))))
    with c2:
        for k, lk in [("country_org", "s1_country_org"), ("country", "s1_country"),
                      ("sector", "s1_sector")]:
            put(k, st.text_input(T(lk), value=str(get(k, ""))))
        put("data_period", str(st.date_input(T("s1_date"))))
    nav(0)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — BRANCH BASIC DATA
# ─────────────────────────────────────────────────────────────────────────────
def step2():
    st.header(f"⚙️  {T('s2_title')}")
    prog(1)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        put("working_days",       st.number_input(T("s2_working_days"),       value=float(get("working_days", 272)),   min_value=1.0,   max_value=365.0, step=1.0))
        put("interest_rate",      st.number_input(T("s2_interest_rate"),      value=float(get("interest_rate", 9.0)),  min_value=0.0,   max_value=50.0,  step=0.1,  format="%.2f"))
        put("target_margin",      st.number_input(T("s2_target_margin"),      value=float(get("target_margin", 20.0)), min_value=0.0,   max_value=100.0, step=0.5,  format="%.1f"))
        put("contract_years",     st.number_input(T("s2_contract_years"),     value=float(get("contract_years", 3)),   min_value=1.0,   max_value=20.0,  step=1.0))
    with c2:
        put("wms",                st.text_input(T("s2_wms"),   value=str(get("wms", "MIKADO"))))
        put("wms_alloc",          st.number_input(T("s2_wms_alloc"),          value=float(get("wms_alloc", 1.7)),      min_value=0.0,   max_value=10.0,  step=0.1,  format="%.2f"))
        put("fluctuation",        st.number_input(T("s2_fluctuation"),        value=float(get("fluctuation", 0.0)),    min_value=0.0,   max_value=50.0,  step=0.1,  format="%.1f"))
        put("deduction_reserve",  st.number_input(T("s2_deduction_reserve"),  value=float(get("deduction_reserve", 10.0)), min_value=0.0, max_value=50.0, step=0.5))
        put("failure_rate",       st.number_input(T("s2_failure_rate"),       value=float(get("failure_rate", 5.0)),   min_value=0.0,   max_value=50.0,  step=0.5))
    with c3:
        put("exchange_rate",      st.number_input(T("s2_exchange_rate"),      value=float(get("exchange_rate", 0.094)),min_value=0.001, max_value=1.0,   step=0.001,format="%.4f"))
        put("ho_alloc",           st.number_input(T("s2_ho_alloc"),           value=float(get("ho_alloc", 0.8625)),    min_value=0.0,   max_value=5.0,   step=0.01, format="%.4f"))
        put("term_payment",       st.number_input(T("s2_term_payment"),       value=float(get("term_payment", 30)),    min_value=0.0,   max_value=180.0, step=1.0))
        put("domino_alloc",       st.number_input(T("s2_domino_alloc"),       value=float(get("domino_alloc", 1.7)),   min_value=0.0,   max_value=10.0,  step=0.1,  format="%.2f"))
        put("premium_order",      st.number_input(T("s2_premium_order"),      value=float(get("premium_order", 0.15)), min_value=0.0,   max_value=10.0,  step=0.01, format="%.2f"))
    nav(1)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — WAREHOUSE
# ─────────────────────────────────────────────────────────────────────────────
def step3():
    st.header(f"🏭  {T('s3_title')}")
    prog(2)
    st.markdown("---")
    r = float(get("interest_rate", 9.0))
    fx = float(get("exchange_rate", 0.094))

    st.subheader("📐 Dimensions")
    c1, c2, c3 = st.columns(3)
    with c1:
        surf = st.number_input(T("s3_wh_surface"), value=float(get("wh_surface", 1600)), min_value=0.0, step=10.0); put("wh_surface", surf)
        h    = st.number_input(T("s3_wh_height"),  value=float(get("wh_height", 10.0)),  min_value=0.0, step=0.5, format="%.1f"); put("wh_height", h)
    with c2:
        gross = st.number_input(T("s3_gross_loc"),   value=float(get("gross_loc", 1741)), min_value=0.0, step=1.0); put("gross_loc", gross)
        ded_z = st.number_input(T("s3_ded_zone"),    value=float(get("ded_zone", 0)),     min_value=0.0, step=1.0); put("ded_zone", ded_z)
        ded_u = st.number_input(T("s3_ded_unusable"),value=float(get("ded_unusable", 0)), min_value=0.0, step=1.0); put("ded_unusable", ded_u)
    with c3:
        op_res = st.number_input(T("s3_op_reserve"), value=float(get("op_reserve", 10.0)), min_value=0.0, max_value=50.0, step=0.5); put("op_reserve", op_res)
        net = calc_net_locations(gross, ded_z, ded_u, op_res); put("net_loc", net)
        st.metric(T("s3_net_loc"), f"{net:,} PPL")
        st.metric("Volume (m³)", f"{surf * h:,.0f} m³")

    st.subheader(f"💰 {T('s3_rent_mad')} / Loyer")
    c4, c5, c6 = st.columns(3)
    with c4:
        loyer   = st.number_input(T("s3_rent_mad"),  value=float(get("rent_mad", 44.5)),     min_value=0.0, step=0.5,  format="%.2f"); put("rent_mad", loyer)
        charges = st.number_input(T("s3_charges"),   value=float(get("charges_mad", 3.5)),   min_value=0.0, step=0.1,  format="%.2f"); put("charges_mad", charges)
        idilite = st.number_input(T("s3_idilite"),   value=float(get("idilite_mad", 5.04)),  min_value=0.0, step=0.01, format="%.3f"); put("idilite_mad", idilite)
    with c5:
        total_mad = loyer + charges + idilite; put("total_rent_mad", total_mad)
        st.metric(T("s3_total_rent_mad"), f"{total_mad:.3f} MAD/m²/mois")
        total_eur = total_mad * fx; put("total_rent_eur", total_eur)
        disp_rent = total_eur if st.session_state.currency == "EUR" else total_eur / fx
        st.metric(T("s3_total_rent_eur"), f"{to_display(total_eur):.4f} {cur_symbol()}/m²/mois")
    with c6:
        st.metric(T("annual_rent"), fmt_period(surf * total_eur * 12))
        st.metric("Office rent (100m²)", fmt_period(100 * total_eur * 12))

    st.subheader(f"🔧 Investments")
    c7, c8, c9 = st.columns(3)
    with c7:
        r_ppl  = from_display(st.number_input(cur_label(T("s3_racking_ppl")),   value=to_display(float(get("racking_ppl", 35.0))), min_value=0.0, step=max(0.1, round(cur_rate(),1)))); put("racking_ppl", r_ppl)
        r_qty  = st.number_input(T("s3_racking_qty"),   value=float(get("racking_qty", 1741)), min_value=0.0, step=1.0); put("racking_qty", r_qty)
        sec    = from_display(st.number_input(cur_label(T("s3_security")),       value=to_display(float(get("security_eur_m2", 5.0))), min_value=0.0, step=max(0.1, round(cur_rate(),1)))); put("security_eur_m2", sec)
        cab    = from_display(st.number_input(cur_label(T("s3_cabling")),        value=to_display(float(get("cabling_eur_m2", 5.0))),  min_value=0.0, step=max(0.1, round(cur_rate(),1)))); put("cabling_eur_m2", cab)
    with c8:
        ls_q   = st.number_input(T("s3_lower_shelf_qty"),  value=float(get("lower_shelf_qty", 110)),  min_value=0.0, step=1.0); put("lower_shelf_qty", ls_q)
        ls_p   = from_display(st.number_input(cur_label(T("s3_lower_shelf_price")), value=to_display(float(get("lower_shelf_price", 38.0))), min_value=0.0, step=max(0.5, round(cur_rate(),0)))); put("lower_shelf_price", ls_p)
        gr_q   = st.number_input(T("s3_grating_qty"),   value=float(get("grating_qty", 550)),   min_value=0.0, step=1.0); put("grating_qty", gr_q)
        gr_p   = from_display(st.number_input(cur_label(T("s3_grating_price")), value=to_display(float(get("grating_price", 20.0))), min_value=0.0, step=max(0.5, round(cur_rate(),0)))); put("grating_price", gr_p)
    with c9:
        dy     = st.number_input(T("s3_invest_depr_years"), value=float(get("invest_depr_years", 12)), min_value=1.0, max_value=30.0, step=1.0); put("invest_depr_years", dy)
        pk     = st.number_input(T("s3_peak_pal"), value=float(get("peak_pal", 2413)), min_value=0.0, step=10.0); put("peak_pal", pk)
        av     = st.number_input(T("s3_avg_pal"),  value=float(get("avg_pal", 1772)),  min_value=0.0, step=10.0); put("avg_pal", av)

    wh = calc_warehouse_costs(st.session_state.d); put("wh_detail", wh); put("wh_total", wh["total"])
    st.markdown("---")
    st.subheader(f"📊 {T('total')} — {T('cost_wh')}  *({period_label()} · {cur_symbol()})*")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("🏗 " + T("annual_rent"),         fmt_period(wh['rent']))
    m2.metric("📦 " + T("racking"),             fmt_period(wh['racking']))
    m3.metric("🔐 " + T("security_cabling"),    fmt_period(wh['security'] + wh['cabling']))
    m4.metric("🏠 Office+Equip",                fmt_period(wh['office']))
    m5.metric(f"📋 {T('total')}",               fmt_period(wh['total']))
    nav(2)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — PERSONNEL
# ─────────────────────────────────────────────────────────────────────────────
def step4():
    st.header(f"👷  {T('s4_title')}")
    prog(3)
    st.markdown("---")
    lang = st.session_state.lang
    sc = st.number_input(T("social_charges"), value=float(get("social_charges_pct", AKZO["social_charges_pct"])), min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
    put("social_charges_pct", sc)

    # ─ OPERATIVES ─
    st.subheader(f"🔵 {T('s4_op_title')}")
    if "personnel_op" not in st.session_state.d:
        st.session_state.d["personnel_op"] = [dict(p) for p in AKZO_PERSONNEL_OP]

    cols_h = st.columns([3, 1.2, 1.8, 1.2, 1.2, 1.5, 1.5])
    for c, lbl in zip(cols_h, [T("s4_role"), T("s4_qty"), cur_label(T("s4_salary")), T("s4_illness"), T("s4_holidays"), T("s4_weekly_h"), T("s4_allowance")]):
        c.markdown(f"**{lbl}**")

    total_op_var = 0
    for i, p in enumerate(st.session_state.d["personnel_op"]):
        cols = st.columns([3, 1.2, 1.8, 1.2, 1.2, 1.5, 1.5])
        cols[0].markdown(f"*{p['role_fr'] if lang == 'FR' else p['role_en']}*")
        p["qty"]       = cols[1].number_input("", value=float(p.get("qty", 0)),        key=f"op_q_{i}",  min_value=0.0, max_value=20.0, step=0.5,    label_visibility="collapsed")
        sal_disp = to_display(float(p.get("salary", 0))); new_sal = cols[2].number_input("", value=sal_disp, key=f"op_s_{i}", min_value=0.0, step=round(cur_rate()*100,0) or 100.0, label_visibility="collapsed"); p["salary"] = from_display(new_sal)
        p["illness"]   = cols[3].number_input("", value=float(p.get("illness", 4.97)), key=f"op_il_{i}", min_value=0.0, max_value=50.0, step=0.1,  format="%.2f", label_visibility="collapsed")
        p["holidays"]  = cols[4].number_input("", value=float(p.get("holidays", 25)),  key=f"op_h_{i}",  min_value=0.0, max_value=50.0, step=1.0,    label_visibility="collapsed")
        p["weekly_h"]  = cols[5].number_input("", value=float(p.get("weekly_h", 44)),  key=f"op_w_{i}",  min_value=0.0, max_value=60.0, step=1.0,    label_visibility="collapsed")
        p["allowance"] = cols[6].number_input("", value=float(p.get("allowance", 9.0)),key=f"op_a_{i}",  min_value=0.0, max_value=50.0, step=0.5,    label_visibility="collapsed")
        if p["qty"] > 0 and p["salary"] > 0:
            total_op_var += calc_personnel_annual(p["salary"], p["qty"], sc)

    # ─ OFFICE ─
    st.subheader(f"🟡 {T('s4_adm_title')}")
    if "personnel_adm" not in st.session_state.d:
        st.session_state.d["personnel_adm"] = [dict(p) for p in AKZO_PERSONNEL_ADM]

    cols_h2 = st.columns([3, 1.2, 1.8, 1.2, 1.2, 1.5])
    for c, lbl in zip(cols_h2, [T("s4_role"), T("s4_qty"), cur_label(T("s4_salary")), T("s4_illness"), T("s4_holidays"), T("s4_weekly_h")]):
        c.markdown(f"**{lbl}**")

    total_adm_fix = 0
    for i, p in enumerate(st.session_state.d["personnel_adm"]):
        cols = st.columns([3, 1.2, 1.8, 1.2, 1.2, 1.5])
        cols[0].markdown(f"*{p['role_fr'] if lang == 'FR' else p['role_en']}*")
        p["qty"]      = cols[1].number_input("", value=float(p.get("qty", 0)),        key=f"adm_q_{i}",  min_value=0.0, max_value=10.0, step=0.25,   label_visibility="collapsed")
        sal_disp_adm = to_display(float(p.get("salary", 0))); new_sal_adm = cols[2].number_input("", value=sal_disp_adm, key=f"adm_s_{i}", min_value=0.0, step=max(1.0, round(cur_rate()*100, 0)), label_visibility="collapsed"); p["salary"] = from_display(new_sal_adm)
        p["illness"]  = cols[3].number_input("", value=float(p.get("illness", 4.97)), key=f"adm_il_{i}", min_value=0.0, max_value=50.0, step=0.1, format="%.2f", label_visibility="collapsed")
        p["holidays"] = cols[4].number_input("", value=float(p.get("holidays", 25)),  key=f"adm_h_{i}",  min_value=0.0, max_value=50.0, step=1.0,    label_visibility="collapsed")
        p["weekly_h"] = cols[5].number_input("", value=float(p.get("weekly_h", 44)),  key=f"adm_w_{i}",  min_value=0.0, max_value=60.0, step=1.0,    label_visibility="collapsed")
        if p["qty"] > 0 and p["salary"] > 0:
            total_adm_fix += calc_personnel_annual(p["salary"], p["qty"], sc)

    # ─ MANAGEMENT ─
    st.subheader(f"🔴 {T('s4_mgmt_title')}")
    if "personnel_mgmt" not in st.session_state.d:
        st.session_state.d["personnel_mgmt"] = [dict(p) for p in AKZO_PERSONNEL_MGMT]

    cols_h3 = st.columns([3, 1.5, 2])
    for c, lbl in zip(cols_h3, [T("s4_role"), T("s4_qty"), cur_label(T("s4_salary"))]):
        c.markdown(f"**{lbl}**")

    total_mgmt_fix = 0
    for i, p in enumerate(st.session_state.d["personnel_mgmt"]):
        cols = st.columns([3, 1.5, 2])
        cols[0].markdown(f"*{p['role_fr'] if lang == 'FR' else p['role_en']}*")
        p["qty"]    = cols[1].number_input("", value=float(p.get("qty", 0)),    key=f"mgmt_q_{i}", min_value=0.0, max_value=5.0, step=0.05, format="%.2f", label_visibility="collapsed")
        sal_disp_mgmt = to_display(float(p.get("salary", 0))); new_sal_mgmt = cols[2].number_input("", value=sal_disp_mgmt, key=f"mgmt_s_{i}", min_value=0.0, step=max(1.0, round(cur_rate()*100, 0)), label_visibility="collapsed"); p["salary"] = from_display(new_sal_mgmt)
        if p["qty"] > 0 and p["salary"] > 0:
            total_mgmt_fix += calc_personnel_annual(p["salary"], p["qty"], sc)

    total_var = total_op_var
    total_fix = total_adm_fix + total_mgmt_fix
    total_pers = total_var + total_fix
    total_fte = (
        sum(p.get("qty", 0) for p in st.session_state.d["personnel_op"]) +
        sum(p.get("qty", 0) for p in st.session_state.d["personnel_adm"]) +
        sum(p.get("qty", 0) for p in st.session_state.d["personnel_mgmt"])
    )
    put("personnel_var", total_var); put("personnel_fix", total_fix)
    put("personnel_total", total_pers); put("personnel_fte", total_fte)

    st.markdown("---")
    pc1, pc2, pc3, pc4 = st.columns(4)
    pc1.metric("👥 Total FTE", f"{total_fte:.2f}")
    pc2.metric(T("variable_costs") + f" ({period_label()})", fmt_period(total_var))
    pc3.metric(T("fixed_costs") + f" ({period_label()})",    fmt_period(total_fix))
    pc4.metric(f"💰 {T('total')} ({period_label()})",        fmt_period(total_pers))
    nav(3)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — INDUSTRIAL TRUCKS
# ─────────────────────────────────────────────────────────────────────────────
def step5():
    st.header(f"🚜  {T('s5_title')}")
    prog(4)
    st.markdown("---")
    lang = st.session_state.lang
    r = float(get("interest_rate", 9.0))

    if "trucks" not in st.session_state.d:
        st.session_state.d["trucks"] = [dict(t) for t in AKZO_TRUCKS]

    # Header row
    hc = st.columns([3.5, 0.8, 1.8, 1.8, 1.5, 1.2, 1.8])
    sym = cur_symbol()
    for c, lbl in zip(hc, [T("s5_truck"), T("s5_qty"), T("s5_rent_purchase"),
                            f"{T('s5_price')} ({sym})", f"{T('s5_battery')} ({sym})",
                            T("s5_depr_years"), f"Annual Cost ({sym})"]):
        c.markdown(f"**{lbl}**")

    total_trucks = 0
    for i, tk in enumerate(st.session_state.d["trucks"]):
        name = tk["name_fr"] if lang == "FR" else tk["name_en"]
        cols = st.columns([3.5, 0.8, 1.8, 1.8, 1.5, 1.2, 1.8])
        cols[0].markdown(f"*{name}* `{tk['code']}`")
        tk["qty"]           = cols[1].number_input("", value=float(tk.get("qty", 0)),          key=f"tk_q_{i}",  min_value=0.0, max_value=20.0, step=0.5,    label_visibility="collapsed")
        tk["rent_purchase"] = cols[2].selectbox("",   ["External Rent", "Purchase"],            key=f"tk_rp_{i}", index=0 if tk.get("rent_purchase") == "External Rent" else 1, label_visibility="collapsed")
        tk["price"]         = from_display(cols[3].number_input("", value=to_display(float(tk.get("price", 0))),   key=f"tk_pr_{i}", min_value=0.0, step=max(1.0, round(cur_rate()*100,0)), label_visibility="collapsed"))
        tk["battery"]       = from_display(cols[4].number_input("", value=to_display(float(tk.get("battery", 0))), key=f"tk_ba_{i}", min_value=0.0, step=max(1.0, round(cur_rate()*100,0)), label_visibility="collapsed"))
        tk["depr_years"]    = cols[5].number_input("", value=float(tk.get("depr_years", 6)),    key=f"tk_dy_{i}", min_value=1.0, max_value=20.0, step=1.0,    label_visibility="collapsed")
        annual = calc_truck_annual(tk["price"], tk["battery"], tk["qty"], tk["rent_purchase"], tk["depr_years"], r)
        tk["annual_cost"] = annual
        cols[6].markdown(f"**{fmt_period(annual)}**" if tk["qty"] > 0 else "—")
        total_trucks += annual

    put("trucks_total", total_trucks)
    st.markdown("---")
    st.metric(f"🚜 {T('s5_title')} — {T('total')} ({period_label()})", fmt_period(total_trucks))
    nav(4)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — PROCESSES & VOLUMES
# ─────────────────────────────────────────────────────────────────────────────
def step6():
    st.header(f"⚡  {T('s6_title')}")
    prog(5)
    st.markdown("---")
    lang = st.session_state.lang
    wd = float(get("working_days", 272))

    if "processes" not in st.session_state.d:
        st.session_state.d["processes"] = [dict(p) for p in AKZO_PROCESSES]

    groups = [
        ("inbound",    f"📥 {T('s6_inbound_title')}"),
        ("picking",    f"🎯 {T('s6_picking_title')}"),
        ("relocation", f"🔄 {T('s6_relocation_title')}"),
        ("outbound",   f"📤 {T('s6_outbound_title')}"),
        ("loading",    f"🚛 {T('s6_loading_title')}"),
    ]

    for grp_code, grp_label in groups:
        st.subheader(grp_label)
        hc = st.columns([0.6, 3.8, 1.5, 2.5, 1.5, 1.5, 1.2])
        for c, lb in zip(hc, [T("s6_active"), T("s6_process"), T("s6_volume"), T("s6_unit"), T("s6_pg"), T("s6_pn"), "h/day"]):
            c.markdown(f"**{lb}**")

        for i, proc in enumerate(st.session_state.d["processes"]):
            if proc["group"] != grp_code:
                continue
            pk = f"{grp_code}_{i}"
            name = proc["name_fr"] if lang == "FR" else proc["name_en"]
            unit = proc["unit_fr"] if lang == "FR" else proc["unit_en"]
            cols = st.columns([0.6, 3.8, 1.5, 2.5, 1.5, 1.5, 1.2])
            proc["active"] = cols[0].checkbox("", value=proc.get("active", True), key=f"p_a_{pk}", label_visibility="collapsed")
            cols[1].markdown(f"*{name}*")
            if proc["active"]:
                proc["volume"]     = cols[2].number_input("", value=float(proc.get("volume", 0)),     key=f"p_v_{pk}",  min_value=0.0, step=100.0, label_visibility="collapsed")
                cols[3].markdown(f"*{unit}*")
                proc["prod_gross"] = cols[4].number_input("", value=float(proc.get("prod_gross", 0)), key=f"p_pg_{pk}", min_value=0.1, step=0.5, format="%.2f", label_visibility="collapsed")
                proc["prod_net"]   = cols[5].number_input("", value=float(proc.get("prod_net", 0)),   key=f"p_pn_{pk}", min_value=0.1, step=0.5, format="%.2f", label_visibility="collapsed")
                h_day = (proc["volume"] / wd) / proc["prod_net"] if wd > 0 and proc["prod_net"] > 0 else 0
                cols[6].markdown(f"**{h_day:.2f}**")
            else:
                for c in cols[2:]: c.markdown("—")

    st.subheader(f"🏬 {T('s6_storage_title')}")
    s1, s2 = st.columns(2)
    s1.metric(T("avg_storage"),   f"{get('avg_pal', 1772):,.0f} PPL")
    s2.metric(T("net_locations"), f"{get('net_loc', 1567):,.0f} PPL")
    nav(5)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — PRICE SHEET
# ─────────────────────────────────────────────────────────────────────────────
def step7():
    st.header(f"💶  {T('s7_title')}")
    prog(6)
    st.markdown("---")
    lang = st.session_state.lang
    net_loc = int(get("net_loc", 1567))
    target  = float(get("target_margin", 20.0)) / 100

    if "prices" not in st.session_state.d:
        st.session_state.d["prices"] = [dict(p) for p in AKZO_PRICES]

    # Volume map from processes
    vol_map = {proc["code"]: proc.get("volume", 0)
               for proc in st.session_state.d.get("processes", AKZO_PROCESSES)
               if proc.get("active", True)}

    st.markdown(f"*{T('net_locations')} : **{net_loc:,} PPL***")

    # Header
    hc = st.columns([3, 2, 1.5, 1.8, 1.8, 1.8, 1.5])
    sym = cur_symbol()
    pl  = period_label()
    for c, lb in zip(hc, [T("s7_process"), T("s7_unit"), T("s7_volume"),
                          f"{T('s7_price')} ({sym})", f"{T('s7_ca')} ({pl} · {sym})",
                          f"{T('s7_cost')} ({pl} · {sym})", T("s7_margin")]):
        c.markdown(f"**{lb}**")

    total_ca = 0; total_cost = 0
    for i, p in enumerate(st.session_state.d["prices"]):
        code = p["code"]
        name = p["name_fr"] if lang == "FR" else p["name_en"]
        unit = p["billing_fr"] if lang == "FR" else p["billing_en"]

        # Determine volume display and volume for calculation
        if code == "storage":
            vol = net_loc; vol_disp = f"{net_loc:,} × 12"
        elif code == "fixed":
            vol = 12; vol_disp = "12"
        else:
            vol = vol_map.get(code, 0); vol_disp = f"{vol:,.0f}"

        cols = st.columns([3, 2, 1.5, 1.8, 1.8, 1.8, 1.5])
        cols[0].markdown(f"*{name}*")
        cols[1].markdown(f"*{unit}*")
        cols[2].markdown(f"{vol_disp}")

        # Price input: show in display currency, store in EUR
        price_eur = float(p.get("price", 0))
        price_display = to_display(price_eur)
        new_price_display = cols[3].number_input("", value=price_display, key=f"pr_{i}",
                                                 min_value=0.0, step=0.0001 if st.session_state.currency == "EUR" else 0.001,
                                                 format="%.4f" if st.session_state.currency == "EUR" else "%.3f",
                                                 label_visibility="collapsed")
        # Convert back to EUR for storage
        p["price"] = from_display(new_price_display)

        # CA
        if code == "storage":
            ca = p["price"] * net_loc * 12
            cost = p.get("cost_unit", 6.064) * net_loc * 12
        elif code == "fixed":
            ca = p["price"] * 12
            cost = p.get("cost_unit", 4983) * 12
        else:
            ca = p["price"] * vol
            cost = p.get("cost_unit", p["price"] * 0.8) * vol

        profit = ca - cost
        margin = profit / ca * 100 if ca > 0 else 0

        cols[4].markdown(f"**{fmt_period(ca)}**")
        cols[5].markdown(f"{fmt_period(cost)}")
        color = "green" if margin > 0 else "red"
        cols[6].markdown(f":{color}[**{margin:.1f}%**]")

        p["ca"] = ca; p["cost"] = cost
        total_ca += ca; total_cost += cost

    # Allocations
    wms_pct = float(get("wms_alloc", 1.7)) / 100
    ho_pct  = float(get("ho_alloc", 0.8625)) / 100
    wms_cost = total_ca * wms_pct
    ho_cost  = total_ca * ho_pct

    put("total_ca", total_ca); put("wms_cost", wms_cost); put("ho_cost", ho_cost)

    st.markdown("---")
    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric(f"CA {pl}" if lang == "FR" else f"Turnover {pl}", fmt_period(total_ca))
    rc2.metric("Coûts Processus" if lang == "FR" else "Process Costs", fmt_period(total_cost))
    rc3.metric("WMS + HO", fmt_period(wms_cost + ho_cost))
    ind_profit = total_ca - total_cost - wms_cost - ho_cost
    ind_margin = ind_profit / total_ca * 100 if total_ca > 0 else 0
    rc4.metric("Marge Indicative" if lang == "FR" else "Indicative Margin", f"{ind_margin:.1f}%",
               delta=f"{ind_margin - float(get('target_margin', 20)):.1f}% vs cible")
    nav(6)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 — RESULTS
# ─────────────────────────────────────────────────────────────────────────────
def step8():
    st.header(f"📊  {T('s8_title')}")
    prog(7)
    st.markdown("---")
    lang = st.session_state.lang
    d = st.session_state.d

    target    = float(get("target_margin", 20.0))
    total_ca  = d.get("total_ca", 0)
    wh_total  = d.get("wh_total", 0)
    per_total = d.get("personnel_total", 0)
    tr_total  = d.get("trucks_total", 0)
    wms_cost  = d.get("wms_cost", total_ca * float(get("wms_alloc", 1.7)) / 100)
    ho_cost   = d.get("ho_cost", total_ca * float(get("ho_alloc", 0.8625)) / 100)

    total_costs = wh_total + per_total + tr_total + wms_cost + ho_cost
    profit      = total_ca - total_costs
    margin      = profit / total_ca * 100 if total_ca > 0 else 0
    gap         = margin - target

    # ── KPIs ──
    pl = period_label()
    st.subheader("🎯 " + ("Key Metrics" if lang == "EN" else "Indicateurs Clés") + f"  *— {pl} · {cur_symbol()}*")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(T("s8_ca"),     fmt_period(total_ca))
    k2.metric(T("s8_cost"),   fmt_period(total_costs))
    k3.metric(T("s8_profit"), fmt_period(profit))
    k4.metric(T("s8_margin"), f"{margin:.2f}%", delta=f"{gap:+.2f}% vs {target:.1f}%",
              delta_color="normal" if gap >= 0 else "inverse")

    if margin >= target:
        st.success(f"✅ {'Margin' if lang == 'EN' else 'Marge'} {margin:.2f}% ≥ {'Target' if lang == 'EN' else 'Cible'} {target:.1f}%")
    else:
        st.error(f"❌ {'Margin' if lang == 'EN' else 'Marge'} {margin:.2f}% < {'Target' if lang == 'EN' else 'Cible'} {target:.1f}%")

    # ── Cost Breakdown ──
    st.subheader("💰 " + T("cost_breakdown") + f"  *({pl} · {cur_symbol()})*")
    items = [
        (T("cost_wh"),    wh_total,  "🏭"),
        (T("cost_pers"),  per_total, "👷"),
        (T("cost_trucks"),tr_total,  "🚜"),
        ("WMS",           wms_cost,  "💻"),
        ("HO Alloc",      ho_cost,   "🏢"),
    ]
    bc = st.columns(len(items))
    for c, (label, val, icon) in zip(bc, items):
        pct_cost = val / total_costs * 100 if total_costs > 0 else 0
        pct_ca   = val / total_ca * 100 if total_ca > 0 else 0
        c.metric(f"{icon} {label}", fmt_period(val), delta=f"{pct_ca:.1f}% CA")

    # ── Revenue Breakdown ──
    st.subheader("📈 " + T("revenue_breakdown") + f"  *({pl} · {cur_symbol()})*")
    lines = []
    for p in d.get("prices", AKZO_PRICES):
        ca_v = p.get("ca", 0)
        if ca_v > 0:
            name = p.get("name_fr" if lang == "FR" else "name_en", p.get("name_en", ""))
            pct  = ca_v / total_ca * 100 if total_ca > 0 else 0
            lines.append((name, ca_v, pct))
    lines.sort(key=lambda x: x[1], reverse=True)
    r_cols = st.columns([3, 2, 1])
    r_cols[0].markdown("**Ligne / Line**")
    r_cols[1].markdown(f"**CA ({pl} · {cur_symbol()})**")
    r_cols[2].markdown("**%**")
    for name, ca_v, pct in lines:
        rc = st.columns([3, 2, 1])
        rc[0].markdown(f"*{name}*"); rc[1].markdown(fmt_period(ca_v)); rc[2].markdown(f"{pct:.1f}%")

    # ── Cost per m² and per location ──
    st.subheader("🔢 " + ("Efficiency Ratios" if lang == "EN" else "Ratios d'Efficacité"))
    surf = float(get("wh_surface", 1600)); net_loc = float(get("net_loc", 1567))
    rat1, rat2, rat3, rat4 = st.columns(4)
    rat1.metric("CA/m²",          fmt_period(total_ca / surf) if surf > 0 else "—")
    rat2.metric("CA/emplacement" if lang == "FR" else "CA/location", fmt_period(total_ca / net_loc) if net_loc > 0 else "—")
    rat3.metric("Coût/m²" if lang == "FR" else "Cost/m²", fmt_period(total_costs / surf) if surf > 0 else "—")
    rat4.metric("Profit/FTE",     fmt_period(profit / float(get('personnel_fte', 4.85))) if get("personnel_fte", 4.85) > 0 else "—")

    # ── Project Card ──
    st.markdown("---")
    st.subheader("📋 " + T("project_summary"))
    pi1, pi2, pi3 = st.columns(3)
    pi1.markdown(f"**{'Projet' if lang == 'FR' else 'Project'}:** {d.get('project', '—')}\n\n**{'Client' if lang == 'FR' else 'Customer'}:** {d.get('customer', '—')}\n\n**{'Secteur' if lang == 'FR' else 'Sector'}:** {d.get('sector', '—')}")
    pi2.markdown(f"**{'Agence' if lang == 'FR' else 'Branch'}:** {d.get('branch', '—')}\n\n**{'Chef de Projet' if lang == 'FR' else 'Project Leader'}:** {d.get('project_leader', '—')}\n\n**{'Pays' if lang == 'FR' else 'Country'}:** {d.get('country', '—')}")
    pi3.markdown(f"**{'Jours Ouvrés' if lang == 'FR' else 'Working Days'}:** {get('working_days', 272)}\n\n**WMS:** {get('wms', 'MIKADO')}\n\n**{'Marge Cible' if lang == 'FR' else 'Target Margin'}:** {target:.1f}%")
    nav(7)

# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────
[step1, step2, step3, step4, step5, step6, step7, step8][st.session_state.step]()
