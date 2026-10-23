# Reproduction : kissing number en dimension 11 = 604 (EinsteinArena)

Verdict : **reproduit**, en arithmétique entière exacte dans Z[√2]. Rapport : `rapport.json`
(format `discoveria-rapport-reproduction/1`, source unique), lisible dans `rapport.md` (généré).

Niveau N1 (rejeu privé de DiscoverIA). Le `rapport.md` figé qualifie le rejeu de « première reproduction certifiée externe de DiscoverIA » : mention antérieure à la décision du 2026-10-12 au soir, non corrigée car le fichier est haché ; ce niveau N1 fait foi.

- 604 vecteurs distincts, dimension 11, norme² commune exactement 36 ; 182 106 paires toutes à distance² ≥ 36 ;
  minimum exact = 36 (rapport 1), atteint par 19 704 paires. Cela donne 604 directions à 60° ou plus deux à deux.
- Deux moteurs de code distinct (`scripts/verif_a.py`, `scripts/verif_b.py`) concordent ; neuf contrôles négatifs
  (`scripts/controles.py`) sont rejetés pour le motif attendu.
- Non établi : que 604 soit le record connu, son optimalité, l'attribution aux agents (voir « Portée » dans `rapport.md`).

## La solution n'est pas dans ce dossier

Le dépôt des records n'a pas de licence : on ne garde que l'URL épinglée et les empreintes (`artefacts/source.txt`).
Fichier : `kissing-number/solutions/solution_n=604_d=11.json` du dépôt `togethercomputer/EinsteinArena-new-SOTA`,
commit `d97e89d1d01848e9393fc48061019a2a4b99d99f`, sha256 `0bde9ca2c434d7beb5af63a64a291498e8c264d9a5718b738e92dd70b9ba7761`.

## Rejouer

1. Télécharger dans un dossier vide, à part du code (fichier non fiable) :
   `https://raw.githubusercontent.com/togethercomputer/EinsteinArena-new-SOTA/d97e89d1d01848e9393fc48061019a2a4b99d99f/kissing-number/solutions/solution_n=604_d=11.json`
2. Depuis ce dossier, avec un dossier de sortie à part (sans lui, `artefacts/*.out` serait réécrit alors que leurs
   empreintes sont gravées dans `rapport.json`) :
   `python -I -X utf8 scripts/rejouer.py <chemin>/solution_n=604_d=11.json <dossier-de-sortie-vide>`
   (refuse un fichier dont le sha256 diffère ; code 0 si tout est conforme).
   Comparer ensuite les sha256 des `.out` obtenus à ceux de la liste « Artefacts » de `rapport.json`.
   Dépendances : Python 3.10+, numpy, sympy (moteur B seulement).

## Horodatage

L'empreinte de `rapport.json` est dans `../MANIFEST.sha256` et soumise le 2026-10-12 à 19:18Z à quatre calendriers OpenTimestamps (`rapport.json.ots`) ;
l'attestation Bitcoin n'est pas encore là (`stamp.py upgrade` la ajoutera).
Ne pas modifier `rapport.json` : l'empreinte change et la fiche n'est plus celle qui a été horodatée.
