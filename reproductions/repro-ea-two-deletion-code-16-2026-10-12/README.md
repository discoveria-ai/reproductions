# Reproduction : code corrigeant deux suppressions, longueur 16 = 219 mots (EinsteinArena)

Verdict : **reproduit**, sans flottant ni tolérance. Rapport : `rapport.json` (format `discoveria-rapport-reproduction/1`,
source unique), lisible dans `rapport.md` (généré). `entree-reproductions.json` est l'objet à ajouter à
`reproductions[]` de l'entrée `ea-two-deletion-code-16` de `data/avancees.json` (fusion faite par la session principale).

- Propriété : 219 mots de {0,1}^16 deux à deux distincts, tels que deux mots distincts n'aient aucun descendant commun de
  longueur 14 (suppression de deux positions) ; pour des mots de longueur 16, c'est équivalent à : plus longue
  sous-séquence commune au plus 13 pour toute paire.
- Moteur A (énumération des descendants, index inversé) : 6 168 descendants distincts, somme des boules 6 168, aucun conflit.
  Moteur B (LCS sur les 23 871 paires) : LCS maximal 13, atteint par 4 599 paires, aucun conflit. Vérificateur public de la
  plateforme : accepté, score 219.0 (outil, pas un tiers).
- Dix contrôles négatifs (dont mots ajoutés violant la propriété et doublon) rejetés avec les mêmes paires en A et B.
- Non établi : que 219 dépasse le record de la littérature (215), l'attribution à nightshift-dc16, l'optimalité.

## La solution n'est pas dans ce dossier, et pas sur GitHub

Le dépôt `togethercomputer/EinsteinArena-new-SOTA` n'a pas ce problème : la source est l'API de la plateforme
(`artefacts/source.txt`). Les mots ne sont pas copiés (licence non établie). L'URL de l'API n'est pas immuable : on épingle
la liste des 219 mots de la solution d'id 2605 par son sha256 `f8ac54a8b0910350a896e9524e6f74b753124d788b52ac0618ab6de34a13755b`.
Limite : si la plateforme retire cette solution, le rejeu public n'est plus possible tant qu'une copie n'a pas été archivée
(décision d'Antoine, voir `a_decider`).

## Rejouer

1. Télécharger dans un dossier vide, à part du code (données non fiables) :
   `https://einsteinarena.com/api/solutions/best?problem_id=34&limit=4` (ou avec une autre limite, tant que l'id 2605 y figure)
   et `https://einsteinarena.com/api/problems/two-deletion-code-16`.
2. Depuis ce dossier, avec un dossier de sortie à part (sans lui, `artefacts/*.out` serait réécrit alors que leurs empreintes
   sont gravées dans `rapport.json`) :
   `python -I -X utf8 scripts/rejouer.py <solutions.json> <problem.json> <dossier-de-sortie-vide>`
   (refuse si la liste de mots ou le texte du vérificateur diffère de l'empreinte épinglée ; code 0 si tout est conforme).
   Comparer ensuite les sha256 des `.out` à ceux de la liste « Artefacts » de `rapport.json`.
   Dépendances : Python 3.10+, bibliothèque standard seule.

## Horodatage

Empreinte soumise le 2026-10-12 à 4 calendriers OpenTimestamps ; attestation Bitcoin en attente.
Ne pas modifier `rapport.json` : son empreinte (certificat) figure dans `entree-reproductions.json`.
