# Simulateur UVE — Guide Claude Code

## Contexte du projet

Simulateur Python d'**Unité de Valorisation Énergétique** (incinération de déchets avec récupération d'énergie).

```
constants.py   — constantes physiques, rendements, facteurs d'émissions
engine.py      — moteur de calcul (bilan énergétique, émissions, résidus, économie)
scenarios.py   — scénarios de test prêts à l'emploi
```

## Règles d'efficacité

### Code

- Toutes les modifications de constantes se font **uniquement dans `constants.py`** — jamais de valeurs numériques "en dur" dans `engine.py` ou `scenarios.py`.
- Les fonctions de calcul dans `engine.py` sont **pures** (pas d'effets de bord, pas d'I/O).
- Chaque nouvelle grandeur calculée doit être ajoutée dans le dataclass de résultat correspondant, pas retournée en vrac.
- Les unités sont **toujours précisées dans le nom de la variable** (`_mwh`, `_kg`, `_pct`, `_eur`).

### Scénarios

- Un nouveau scénario = une nouvelle fonction `scenario_<nom>()` dans `scenarios.py`.
- Chaque scénario documente son cas d'usage dans sa docstring.
- La fonction `executer_tous_les_scenarios()` doit toujours appeler tous les scénarios définis.

### Ajout de modules

Avant de créer un nouveau fichier :
1. Vérifier qu'il n'existe pas déjà une fonction adaptable dans `engine.py`.
2. Si un nouveau module est nécessaire, le nommer `<domaine>.py` (ex : `reseaux.py`, `optimisation.py`).

### Tests

Lancer les scénarios de validation avant tout commit :
```bash
python scenarios.py
```

Les valeurs de sortie attendues pour le scénario de référence (200 000 t/an, PCI 9.5 MJ/kg) :
- Électricité nette ≈ 120 000 MWh/an
- Rendement électrique net ≈ 14–18 %
- Rendement global ≈ 55–70 %
- Bilan net > 0 €/an

### Commandes utiles

```bash
# Lancer tous les scénarios
python scenarios.py

# Lancer un scénario isolé
python -c "from scenarios import scenario_reference; from engine import afficher_rapport; afficher_rapport(scenario_reference())"

# Vérifier la syntaxe
python -m py_compile constants.py engine.py scenarios.py
```

## Grandeurs physiques clés

| Symbole | Description | Unité |
|---------|-------------|-------|
| PCI | Pouvoir Calorifique Inférieur | MJ/kg |
| η_élec | Rendement électrique net | % |
| η_global | Rendement électrique + chaleur | % |
| Qv | Débit vapeur | t/an |
| REFIOM | Résidus d'épuration des fumées d'incinération des ordures ménagères | t/an |
