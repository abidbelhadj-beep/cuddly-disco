"""Scénarios de test pour le simulateur UVE."""

from engine import IntrantDechet, simuler, afficher_rapport


def scenario_reference():
    """UVE 200 000 t/an — ordures ménagères standard."""
    intrant = IntrantDechet(
        tonnage_annuel=200_000,
        pci_mj_kg=9.5,
        humidite_pct=30.0,
        description="UVE référence — OM 200 kt/an",
    )
    return simuler(intrant)


def scenario_haut_pci():
    """UVE avec déchets industriels banals à haut PCI."""
    intrant = IntrantDechet(
        tonnage_annuel=80_000,
        pci_mj_kg=14.0,
        humidite_pct=15.0,
        description="UVE déchets industriels — 80 kt/an",
    )
    return simuler(intrant, part_electricite=0.35, part_chaleur=0.50)


def scenario_cogeneraion_optimisee():
    """UVE en cogénération maximisant l'export de chaleur réseau."""
    intrant = IntrantDechet(
        tonnage_annuel=150_000,
        pci_mj_kg=10.2,
        humidite_pct=28.0,
        description="UVE cogénération réseau chaleur urbain",
    )
    return simuler(intrant, part_electricite=0.20, part_chaleur=0.70)


def scenario_humide():
    """UVE traitant des déchets très humides (boues + OM)."""
    intrant = IntrantDechet(
        tonnage_annuel=120_000,
        pci_mj_kg=7.0,
        humidite_pct=45.0,
        description="UVE déchets humides — mix boues/OM",
    )
    return simuler(intrant)


def executer_tous_les_scenarios():
    scenarios = [
        scenario_reference,
        scenario_haut_pci,
        scenario_cogeneraion_optimisee,
        scenario_humide,
    ]

    for fn in scenarios:
        res = fn()
        afficher_rapport(res)


if __name__ == "__main__":
    executer_tous_les_scenarios()
