# Constantes physiques et opérationnelles pour le simulateur UVE

# --- Pouvoir Calorifique ---
PCI_ORDURES_MENAGERES = 9.5        # MJ/kg - valeur typique OM françaises
PCI_DECHETS_INDUSTRIELS = 14.0     # MJ/kg
PCI_BOUES_STEP = 3.5               # MJ/kg (après séchage partiel ~70% MS)

# --- Rendements énergétiques ---
RENDEMENT_CHAUDIERE = 0.82         # Rendement thermique chaudière
RENDEMENT_TURBINE_VAPEUR = 0.88    # Rendement isentropique turbine
RENDEMENT_ALTERNATEUR = 0.97       # Rendement alternateur
RENDEMENT_ELECTRIQUE_GLOBAL = RENDEMENT_CHAUDIERE * RENDEMENT_TURBINE_VAPEUR * RENDEMENT_ALTERNATEUR

RENDEMENT_CHALEUR_RESEAU = 0.90    # Rendement injection réseau chaleur

# --- Paramètres vapeur ---
PRESSION_VAPEUR_BAR = 40.0         # Pression vapeur en sortie chaudière (bar)
TEMPERATURE_VAPEUR_C = 400.0       # Température vapeur surchauffée (°C)
ENTHALPIE_VAPEUR_KJ_KG = 3214.0    # Enthalpie vapeur à 40 bar / 400°C (kJ/kg)
ENTHALPIE_EAU_ALIM_KJ_KG = 420.0  # Enthalpie eau d'alimentation (kJ/kg)
ENTHALPIE_UTILE_KJ_KG = ENTHALPIE_VAPEUR_KJ_KG - ENTHALPIE_EAU_ALIM_KJ_KG  # kJ/kg

# --- Paramètres de combustion ---
RATIO_AIR_STOECHIO = 6.0           # kg air / kg déchet (rapport stoechiométrique)
EXCES_AIR = 1.8                    # Facteur d'excès d'air typique UVE
RATIO_AIR_REEL = RATIO_AIR_STOECHIO * EXCES_AIR  # kg air / kg déchet

TEMPERATURE_FOUR_MIN_C = 850.0     # Température minimale réglementaire (°C)
TEMPERATURE_FOUR_NOM_C = 950.0     # Température nominale de fonctionnement (°C)
DUREE_SEJOUR_GAZ_S = 2.0           # Durée de séjour des gaz à 850°C (secondes)

# --- Facteurs d'émissions (g/tonne de déchet traité) ---
EMISSION_CO2_G_T = 800_000         # CO2 (dont fraction biogénique ~50%)
EMISSION_NOX_G_T = 1_500           # NOx (après SCR)
EMISSION_SO2_G_T = 200             # SO2 (après laveur)
EMISSION_HCL_G_T = 100             # HCl (après laveur)
EMISSION_POUSSIERE_G_T = 50        # Poussières (après filtres manches)
EMISSION_DIOXINES_NG_T = 0.05      # Dioxines/Furannes ng I-TEQ/Nm³ (valeur limite = 0.1)

# --- Résidus solides ---
TAUX_MACHEFER_PCT = 20.0           # % masse mâchefers / déchet entrant
TAUX_REFIOM_PCT = 3.5              # % masse REFIOM / déchet entrant
TAUX_CENDRES_VOL_PCT = 0.5         # % masse cendres volantes / déchet entrant

# --- Paramètres économiques ---
PRIX_ELECTRICITE_EUR_MWH = 70.0    # €/MWh électricité vendue
PRIX_CHALEUR_EUR_MWH = 35.0        # €/MWh chaleur réseau
COUT_TRAITEMENT_DECHET_EUR_T = 120.0  # €/tonne (gate fee)
COUT_ELIMINATION_REFIOM_EUR_T = 350.0  # €/tonne REFIOM (stockage classe I)
COUT_VALORISATION_MACHEFER_EUR_T = -15.0  # €/tonne (négatif = recette)

# --- Capacité et disponibilité ---
HEURES_AN = 8_760                  # heures/an
DISPONIBILITE_NOM = 0.88           # Taux de disponibilité nominale
HEURES_FONCTIONNEMENT_AN = int(HEURES_AN * DISPONIBILITE_NOM)  # ~7 709 h/an
