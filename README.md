# DiscoverIA : reproductions rejouables

Quatre reproductions de résultats AlphaEvolve de la plateforme EinsteinArena, rejouées en arithmétique exacte pour [DiscoverIA](https://discoveria.ai). Chaque dossier contient le rapport (`rapport.json`, source unique, et `rapport.md`, généré), les scripts de rejeu (`scripts/`) et les sorties conservées (`artefacts/`).

| Dossier | Résultat rejoué |
|---|---|
| `reproductions/repro-ea-kakeya-needle-128-2026-10-12` | aiguille de Kakeya discrétisée, n = 128 |
| `reproductions/repro-ea-kissing-d11-2026-10-12` | nombre de contact (kissing number), dimension 11, 604 sphères |
| `reproductions/repro-ea-ring-loading-15-2026-10-12` | chargement d'anneau à 15 paires, 9/8 |
| `reproductions/repro-ea-two-deletion-code-16-2026-10-12` | code corrigeant deux suppressions, longueur 16, 219 mots |

Chaque `README.md` de dossier donne les étapes de rejeu et ce qui reste non établi.

## Vérifier que rien n'a bougé

Les `rapport.json` sont horodatés (OpenTimestamps, fichier `.ots` voisin) et leur empreinte SHA-256 est gravée dans `reproductions/MANIFEST.sha256` (ajout seulement). Depuis la racine du dépôt :

```bash
cd reproductions && awk '!/^#/ && NF {print $1"  "$2}' MANIFEST.sha256 | sha256sum -c --ignore-missing
```

Les 4 lignes `rapport.json` doivent afficher `OK`. Le manifeste liste une cinquième reproduction qui n'est pas publiée ici : `--ignore-missing` l'ignore.

## À lire avant d'exécuter un script

- Les fichiers de ce dépôt sont figés octet pour octet : leurs empreintes sont dans les rapports. Ne les modifiez pas ; copiez un dossier avant de l'exécuter.
- Lancez les scripts dans un dossier vide, à part, avec un dossier de sortie séparé : sans lui, un rejeu réécrit `artefacts/*.out`, dont les empreintes sont gravées.
- `temoin_plateforme.py` et `verif_plateforme.py` exécutent le vérificateur de la plateforme, passé en argument. N'exécutez que du code que vous avez lu, de préférence dans un environnement isolé.
- Les solutions soumises à EinsteinArena ne sont pas copiées ici (la plateforme n'indique aucune licence) : chaque `artefacts/source.txt` donne l'adresse et l'empreinte à rejouer.

## Licences

- Code (`scripts/*.py`) : Apache-2.0, voir `LICENSE`. Les scripts étant figés, l'avis de licence est ici et non dans les fichiers.
- Données et textes (rapports, README, sorties) : CC BY 4.0 avec mention « DiscoverIA », voir `LICENSE-DATA`. Les sources citées gardent leurs licences propres.

Contact : contact@discoveria.ai
