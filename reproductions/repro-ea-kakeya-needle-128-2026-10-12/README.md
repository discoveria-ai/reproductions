# Reproduction : aiguille de Kakeya discrétisée n = 128, aire 0,10675394011230244 (EinsteinArena)

Verdict : **reproduit**, en rationnels exacts (offsets lus par `Fraction(chaîne)`, aucun flottant dans le calcul). Rapport :
`rapport.json` (format `discoveria-rapport-reproduction/1`, source unique), lisible dans `rapport.md` (généré).

- Aire exacte de la réunion des 128 triangles de la soumission 2608 (agent Ghazt, 2026-10-06) :
  `22598724902070159499743765877870160455101358423617701/211689843750000000000000000000000000000000000000000000`
  = 0,1067539401123024330247... Trois calculs exacts donnent la même fraction : moteur A (balayage en hauteur),
  moteur B (balayage en abscisse depuis les sommets) et le vérificateur public de la plateforme exécuté comme témoin.
- Son double est 0,10675394011230244 = la valeur revendiquée. Exactement inférieure à 0,107067 (la Station) : C_T(128) <= 0,1067539401123025.
- Onze contrôles négatifs rejetés pour le motif attendu ; positifs analytiques (n=1, n=2, 128 triangles disjoints),
  classement public à quatre entrées recalculé (ordre exact), différentiel A/B sur 80 cas aléatoires.
- Réserve à lire : la revendication est un double. L'égalité établie est celle de l'arrondi au double de l'aire exacte
  (qui diffère du décimal publié de 7e-18) ; voir « Écarts » dans `rapport.md`.
- Non établi : que ce soit un record de la littérature (aucune recherche faite), l'optimalité, l'attribution à Ghazt.

## La solution n'est pas dans ce dossier, et il n'y a pas de commit

Aucun dossier kakeya dans le dépôt `EinsteinArena-new-SOTA` : la solution n'existe que dans l'API EinsteinArena, non versionnée
et sans licence indiquée. On ne garde que l'URL et les empreintes (`artefacts/source.txt`).
URL : `https://einsteinarena.com/api/solutions/best?problem_id=26&limit=1` (entrée d'id 2608 tant qu'elle est au rang 1 ;
sinon `limit=4` ou plus) ; épinglage par le sha256 de la forme canonique des 128 offsets :
`8a9e475f2c54b96d21b6bb385b04d55d559029a9ad96b83e92eddb9173609c29`. Énoncé : `https://einsteinarena.com/api/problems/kakeya-needle-128`.

## Rejouer

1. Télécharger dans un dossier vide, à part du code (réponses non fiables) :
   `https://einsteinarena.com/api/solutions/best?problem_id=26&limit=4` → `best.json` ;
   `https://einsteinarena.com/api/problems/kakeya-needle-128` → `problem.json`.
2. Depuis ce dossier, avec un dossier de sortie à part (sans lui, `artefacts/*.out` serait réécrit alors que leurs empreintes
   sont gravées dans `rapport.json`) :
   `python -B -I -X utf8 scripts/rejouer.py <chemin>/best.json <chemin>/problem.json <dossier-de-sortie-vide>`
   (refuse si les offsets de la soumission 2608 n'ont pas le sha256 canonique épinglé ; code 0 si tout est conforme ; environ une minute).
   Comparer ensuite les sha256 des `.out` à ceux de `rapport.json`. `sortie_temoin_flottant.out` dépend de la version de shapely
   (témoin non certifiant) ; `controles.py` utilise toutes les entrées de `best.json` (P5) : avec `limit=1` le `.out` des contrôles diffère.
   Dépendances : Python 3.10+ ; shapely seulement pour le témoin flottant (absent : le témoin le dit et passe).

## Horodatage

Empreinte soumise le 2026-10-12 à 4 calendriers OpenTimestamps ; attestation Bitcoin en attente.
Ne pas modifier `rapport.json` : l'empreinte change et la fiche n'est plus celle qui a été horodatée.
`entree-reproductions.json` contient l'objet à ajouter à `reproductions[]` de l'entrée `ea-kakeya-needle-128` de `data/avancees.json`.
