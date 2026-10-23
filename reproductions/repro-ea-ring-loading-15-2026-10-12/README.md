# Reproduction : chargement d'anneau à 15 paires = 9/8 (EinsteinArena)

Verdict : **reproduit**, en rationnels exacts (`fractions.Fraction`, entiers, `sympy.Rational`). Rapport : `rapport.json`
(format `discoveria-rapport-reproduction/1`, source unique), lisible dans `rapport.md` (généré).

- Soumission 2576 (JSAgent-Ring15, 2026-09-12, score stocké 1.125) : les 32 768 choix adverses donnent un minimum des
  maxima exactement égal à **9/8**, atteint par 46 choix ; l'ancienne valeur (AlphaEvolve) est 40317937698944779/36028797018963968,
  l'écart exact est 214458947389685/36028797018963968 (environ 0,00595, estimé).
- Deux moteurs de code distinct (`scripts/verif_a.py`, `scripts/verif_b.py`, plus sympy) concordent ; treize contrôles
  négatifs et sept contrôles positifs (dont la valeur d'AlphaEvolve retrouvée exactement) sont conformes (`scripts/controles.py`).
- Non établi : que 9/8 soit un record au sens de la littérature (le papier arXiv 2606.10402 ne couvre pas ce problème),
  son optimalité, l'attribution ; l'énoncé de la plateforme est marqué « Under active review » (voir « Portée » dans `rapport.md`).

## La solution n'est pas dans ce dossier, et sa source n'est pas épinglable sur un commit

Le dépôt `togethercomputer/EinsteinArena-new-SOTA` n'a aucun fichier pour ce problème : la seule source est l'API de la plateforme
(modifiable). Aucune licence lisible : on ne garde que les URL et les empreintes (`artefacts/source.txt`).
Soumission 2576, sha256 canonique `3b9d1e3a1278889d29d6120e13db84a6cd45e20c4d2601f98c77a3c412425e80` (forme : `scripts/empreintes.py`).

## Rejouer

1. Télécharger dans un dossier vide, à part du code (données non fiables), avec le même nom de fichier :
   `https://einsteinarena.com/api/solutions/best?problem_id=30&limit=10` (enregistrer sous `best_limit10.json`) et
   `https://einsteinarena.com/api/problems/ring-loading-15` (enregistrer sous `problem.json`).
2. Depuis ce dossier, avec un dossier de sortie à part (sans lui, `artefacts/*.out` serait réécrit alors que leurs
   empreintes sont gravées dans `rapport.json`) :
   `python -B -I -X utf8 scripts/rejouer.py <chemin>/best_limit10.json <chemin>/problem.json <dossier-de-sortie-vide>`
   (refuse, code 3, si une des 7 soumissions n'a plus son sha256 canonique ou si l'énoncé a changé ; code 0 si tout est conforme ;
   durée environ 80 s). Comparer ensuite les sha256 des `.out` obtenus à ceux de la liste « Artefacts » de `rapport.json`.
   Dépendances : Python 3.10+ (3.13 testé), sympy (moteur B seulement).
3. Si la plateforme a révisé l'énoncé ou la liste, le refus est voulu : l'empreinte de la soumission 2576 ne dépend que de ses 15 paires et de son score.

## Horodatage

Empreinte soumise le 2026-10-12 à 4 calendriers OpenTimestamps ; attestation Bitcoin en attente. Ne pas modifier `rapport.json` : l'empreinte change et la fiche n'est plus celle qui a été horodatée.
