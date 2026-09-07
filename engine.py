"""Moteur de calcul du simulateur UVE."""

from dataclasses import dataclass, field
from typing import Optional
import constants as C


@dataclass
class IntrantDechet:
    tonnage_annuel: float          # tonnes/an
    pci_mj_kg: float = C.PCI_ORDURES_MENAGERES
    humidite_pct: float = 30.0     # % humidité
    description: str = "Ordures ménagères"


@dataclass
class ResultatEnergetique:
    energie_thermique_mwh: float
    production_vapeur_t: float
    electricite_produite_mwh: float
    chaleur_reseau_mwh: float
    consommation_auxiliaires_mwh: float
    electricite_nette_mwh: float


@dataclass
class ResultatEmissions:
    co2_tonnes: float
    nox_kg: float
    so2_kg: float
    hcl_kg: float
    poussiere_kg: float
    dioxines_ng_iteq: float


@dataclass
class ResultatResidus:
    machefers_tonnes: float
    refiom_tonnes: float
    cendres_vol_tonnes: float


@dataclass
class BilanEconomique:
    recette_electricite_eur: float
    recette_chaleur_eur: float
    recette_traitement_eur: float
    cout_elimination_refiom_eur: float
    recette_machefer_eur: float
    bilan_net_eur: float


@dataclass
class ResultatSimulation:
    intrant: IntrantDechet
    energetique: ResultatEnergetique
    emissions: ResultatEmissions
    residus: ResultatResidus
    economique: BilanEconomique
    rendement_electrique_pct: float
    rendement_global_pct: float


def _pci_effectif(intrant: IntrantDechet) -> float:
    """Corrige le PCI en tenant compte de l'humidité (MJ/kg brut)."""
    correction_humidite = 2.5 * (intrant.humidite_pct / 100.0)
    return max(0.0, intrant.pci_mj_kg - correction_humidite)


def calculer_energetique(
    intrant: IntrantDechet,
    part_electricite: float = 0.30,
    part_chaleur: float = 0.55,
    taux_auxiliaires: float = 0.08,
) -> ResultatEnergetique:
    """
    Calcule le bilan énergétique de l'UVE.

    part_electricite : fraction de l'énergie thermique convertie en électricité
    part_chaleur     : fraction convertie en chaleur réseau
    taux_auxiliaires : consommation propre en % de la production brute
    """
    pci_eff = _pci_effectif(intrant)
    energie_thermique_mj = intrant.tonnage_annuel * 1_000 * pci_eff  # MJ
    energie_thermique_mwh = energie_thermique_mj / 3_600

    # MJ → kJ (* 1000) puis kg → t (/ 1000) : les facteurs s'annulent
    production_vapeur_t = (
        energie_thermique_mj * C.RENDEMENT_CHAUDIERE / C.ENTHALPIE_UTILE_KJ_KG
    )

    electricite_brute_mwh = energie_thermique_mwh * part_electricite * C.RENDEMENT_ELECTRIQUE_GLOBAL
    chaleur_reseau_mwh = energie_thermique_mwh * part_chaleur * C.RENDEMENT_CHALEUR_RESEAU

    consommation_aux_mwh = electricite_brute_mwh * taux_auxiliaires
    electricite_nette_mwh = electricite_brute_mwh - consommation_aux_mwh

    return ResultatEnergetique(
        energie_thermique_mwh=round(energie_thermique_mwh, 1),
        production_vapeur_t=round(production_vapeur_t, 0),
        electricite_produite_mwh=round(electricite_brute_mwh, 1),
        chaleur_reseau_mwh=round(chaleur_reseau_mwh, 1),
        consommation_auxiliaires_mwh=round(consommation_aux_mwh, 1),
        electricite_nette_mwh=round(electricite_nette_mwh, 1),
    )


def calculer_emissions(intrant: IntrantDechet) -> ResultatEmissions:
    t = intrant.tonnage_annuel
    return ResultatEmissions(
        co2_tonnes=round(t * C.EMISSION_CO2_G_T / 1e6, 1),
        nox_kg=round(t * C.EMISSION_NOX_G_T / 1e3, 1),
        so2_kg=round(t * C.EMISSION_SO2_G_T / 1e3, 1),
        hcl_kg=round(t * C.EMISSION_HCL_G_T / 1e3, 1),
        poussiere_kg=round(t * C.EMISSION_POUSSIERE_G_T / 1e3, 1),
        dioxines_ng_iteq=round(t * C.EMISSION_DIOXINES_NG_T, 4),
    )


def calculer_residus(intrant: IntrantDechet) -> ResultatResidus:
    t = intrant.tonnage_annuel
    return ResultatResidus(
        machefers_tonnes=round(t * C.TAUX_MACHEFER_PCT / 100, 1),
        refiom_tonnes=round(t * C.TAUX_REFIOM_PCT / 100, 1),
        cendres_vol_tonnes=round(t * C.TAUX_CENDRES_VOL_PCT / 100, 1),
    )


def calculer_economique(
    intrant: IntrantDechet,
    energetique: ResultatEnergetique,
    residus: ResultatResidus,
) -> BilanEconomique:
    recette_elec = energetique.electricite_nette_mwh * C.PRIX_ELECTRICITE_EUR_MWH
    recette_chaleur = energetique.chaleur_reseau_mwh * C.PRIX_CHALEUR_EUR_MWH
    recette_traitement = intrant.tonnage_annuel * C.COUT_TRAITEMENT_DECHET_EUR_T
    cout_refiom = residus.refiom_tonnes * C.COUT_ELIMINATION_REFIOM_EUR_T
    recette_machefer = residus.machefers_tonnes * abs(C.COUT_VALORISATION_MACHEFER_EUR_T)

    bilan = recette_elec + recette_chaleur + recette_traitement + recette_machefer - cout_refiom

    return BilanEconomique(
        recette_electricite_eur=round(recette_elec, 0),
        recette_chaleur_eur=round(recette_chaleur, 0),
        recette_traitement_eur=round(recette_traitement, 0),
        cout_elimination_refiom_eur=round(cout_refiom, 0),
        recette_machefer_eur=round(recette_machefer, 0),
        bilan_net_eur=round(bilan, 0),
    )


def simuler(intrant: IntrantDechet, **kwargs) -> ResultatSimulation:
    """Point d'entrée principal : calcule l'ensemble du bilan UVE."""
    energetique = calculer_energetique(intrant, **kwargs)
    emissions = calculer_emissions(intrant)
    residus = calculer_residus(intrant)
    economique = calculer_economique(intrant, energetique, residus)

    pci_eff = _pci_effectif(intrant)
    energie_totale_kwh = intrant.tonnage_annuel * 1_000 * pci_eff / 3.6  # kWh
    rendement_elec = (
        energetique.electricite_nette_mwh * 1_000 / energie_totale_kwh * 100
        if energie_totale_kwh > 0 else 0.0
    )
    rendement_global = (
        (energetique.electricite_nette_mwh + energetique.chaleur_reseau_mwh)
        * 1_000 / energie_totale_kwh * 100
        if energie_totale_kwh > 0 else 0.0
    )

    return ResultatSimulation(
        intrant=intrant,
        energetique=energetique,
        emissions=emissions,
        residus=residus,
        economique=economique,
        rendement_electrique_pct=round(rendement_elec, 2),
        rendement_global_pct=round(rendement_global, 2),
    )


def afficher_rapport(res: ResultatSimulation) -> None:
    e = res.energetique
    em = res.emissions
    r = res.residus
    ec = res.economique

    print(f"\n{'='*60}")
    print(f"  BILAN UVE — {res.intrant.description}")
    print(f"  Tonnage traité : {res.intrant.tonnage_annuel:,.0f} t/an")
    print(f"{'='*60}")

    print("\n[ENERGIE]")
    print(f"  Énergie thermique entrante : {e.energie_thermique_mwh:>12,.0f} MWh/an")
    print(f"  Production vapeur          : {e.production_vapeur_t:>12,.0f} t/an")
    print(f"  Électricité brute          : {e.electricite_produite_mwh:>12,.0f} MWh/an")
    print(f"  Chaleur réseau             : {e.chaleur_reseau_mwh:>12,.0f} MWh/an")
    print(f"  Consommation auxiliaires   : {e.consommation_auxiliaires_mwh:>12,.0f} MWh/an")
    print(f"  Électricité nette          : {e.electricite_nette_mwh:>12,.0f} MWh/an")
    print(f"  Rendement électrique net   : {res.rendement_electrique_pct:>11.1f} %")
    print(f"  Rendement global           : {res.rendement_global_pct:>11.1f} %")

    print("\n[EMISSIONS]")
    print(f"  CO2                        : {em.co2_tonnes:>12,.1f} t/an")
    print(f"  NOx                        : {em.nox_kg:>12,.1f} kg/an")
    print(f"  SO2                        : {em.so2_kg:>12,.1f} kg/an")
    print(f"  HCl                        : {em.hcl_kg:>12,.1f} kg/an")
    print(f"  Poussières                 : {em.poussiere_kg:>12,.1f} kg/an")

    print("\n[RESIDUS]")
    print(f"  Mâchefers                  : {r.machefers_tonnes:>12,.1f} t/an")
    print(f"  REFIOM                     : {r.refiom_tonnes:>12,.1f} t/an")
    print(f"  Cendres volantes           : {r.cendres_vol_tonnes:>12,.1f} t/an")

    print("\n[ECONOMIE]")
    print(f"  Recettes électricité       : {ec.recette_electricite_eur:>12,.0f} €/an")
    print(f"  Recettes chaleur           : {ec.recette_chaleur_eur:>12,.0f} €/an")
    print(f"  Recettes traitement        : {ec.recette_traitement_eur:>12,.0f} €/an")
    print(f"  Recettes mâchefers         : {ec.recette_machefer_eur:>12,.0f} €/an")
    print(f"  Coût REFIOM                : {ec.cout_elimination_refiom_eur:>12,.0f} €/an")
    print(f"  BILAN NET                  : {ec.bilan_net_eur:>12,.0f} €/an")
    print(f"{'='*60}\n")
