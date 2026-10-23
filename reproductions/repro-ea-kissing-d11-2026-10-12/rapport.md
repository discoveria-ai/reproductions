# Reproduit — nombre de vecteurs d'une configuration de contact valide en dimension 11 = 604

<!-- Généré par scripts/reproductions.py depuis rapport.json : ne pas éditer. -->

- Rapport : `repro-ea-kissing-d11-2026-10-12` (format `discoveria-rapport-reproduction/1`), rejoué le 2026-10-12, publication : privee.
- Avancée : `ea-kissing-number-d11`.
- Opérateur : DiscoverIA (agent Claude pour Antoine Olivier) — première reproduction certifiée externe de DiscoverIA ; session Claude Code 2026-10-12-claude-code-55938116086b, sous-agent exécutant sur mandat de la session ; code écrit pour ce rejeu, indépendant de la plateforme EinsteinArena.

## Revendication

Il existe 604 sphères unité non chevauchantes tangentes à une sphère unité centrale en dimension 11, c'est-à-dire 604 vecteurs de même norme dont les angles deux à deux sont au moins 60 degrés (borne inférieure du nombre de contact en dimension 11 : 604, contre 593 pour AlphaEvolve). La configuration publiée est un fichier de 604 vecteurs à coordonnées dans Z[sqrt 2], mis à l'échelle de sorte que la norme au carré vaut 36.

> improved the best known lower bound from 593 to 604

- Valeur revendiquée : `604`
- Source : https://raw.githubusercontent.com/togethercomputer/EinsteinArena-new-SOTA/d97e89d1d01848e9393fc48061019a2a4b99d99f/kissing-number/solutions/solution_n=604_d=11.json @ `d97e89d1d01848e9393fc48061019a2a4b99d99f`

## Verdict

**Reproduit.** La configuration publiée de 604 vecteurs en dimension 11 a été rejouée en arithmétique entière exacte dans Z[sqrt 2], sans flottant ni tolérance : 604 vecteurs distincts de même norme^2 36 et 182 106 paires toutes à distance^2 >= 36, minimum exactement 36, atteint par 19 704 paires. Deux moteurs de code distinct concordent, et neuf contrôles négatifs sont rejetés pour le motif attendu. Le rejeu établit la borne inférieure 604 du nombre de contact en dimension 11 ; il n'établit ni que 604 est le record connu, ni son optimalité, ni l'attribution aux agents.

## Portée

**Établi par le rejeu**
- Le fichier publié (sha256 0bde9ca2c434d7beb5af63a64a291498e8c264d9a5718b738e92dd70b9ba7761, 42 551 octets, commit d97e89d1) contient exactement 604 vecteurs de 22 entiers, soit 11 coordonnées a + b sqrt 2 (lecture : coordonnée k = v[2k] + v[2k+1] sqrt 2), tous distincts.
- Norme au carré de chacun des 604 vecteurs égale à 36 + 0 sqrt 2, exactement.
- Pour chacune des 182 106 paires, distance^2 - 36 >= 0 dans Z[sqrt 2], par signes décidés en entiers ; distance^2 minimale exacte = 36 (égale à la norme^2, rapport 1), atteinte par 19 704 paires ; la plus petite valeur suivante est 54 - 12 sqrt 2 (environ 37,03, estimé) ; 22 valeurs distinctes de distance^2, dont 16 avec une partie en sqrt 2 non nulle.
- Donc, pour des vecteurs de même norme, distance^2 >= norme^2 équivaut à produit scalaire <= norme^2 / 2, soit un angle d'au moins 60 degrés : 604 directions deux à deux à 60 degrés ou plus en dimension 11, donc un nombre de contact >= 604 dans R^11.
- Deux moteurs de code distinct (A : paires (a, b) et signes par cas ; B : Gram numpy en int64, signe par la norme du corps, sympy sur les 22 valeurs) donnent le même verdict, le même minimum exact et le même nombre de paires à égalité.

**Supposé par la revendication, non prouvé**
- La lecture du format : la description du fichier écrit « p_{2k} + q_{2k+1} sqrt 2 » ; nous lisons les paires (v[2k], v[2k+1]), seule lecture compatible avec 22 entiers pour 11 coordonnées. Les 108 vecteurs à partie en sqrt 2 non nulle montrent que ces parties sont réellement utilisées.
- Le fichier téléchargé est bien celui du dépôt à ce commit : épinglé par sha256 et par le sha1 d'objet git c7c87ab5 (identique à l'API GitHub), mais on se fie à l'hébergeur pour l'intégrité du dépôt.

**Cité, non reconstruit ici**
- Que 604 soit la meilleure borne connue et dépasse 593 (AlphaEvolve) et 592 (Ganzhinov) : lu sur le papier arXiv 2606.10402 v2, non rejoué ici ; aucune recherche de littérature n'a été faite pour ce rapport.
- L'attribution à des agents (alpha_omega_agents, KawaiiCorgi, agent non nommé), la chronologie des soumissions et la construction de l'annexe B du papier : non comparées au fichier.
- Aucune optimalité : le rejeu n'exclut ni 605 ni davantage ; une borne supérieure n'est pas en jeu.
- Le vérificateur public de la plateforme : il ne peut plus recevoir cette configuration (voir écarts) ; il n'a pas été exécuté.

## Exécution

- Environnement : Windows 11, Python 3.13.15, numpy 2.5.2, sympy 1.14.0 ; interpréteur lancé avec -I (mode isolé) ; solution téléchargée dans un dossier séparé du code ; aucun réseau pendant le rejeu
- Commande : `python -I -X utf8 scripts/rejouer.py <dossier-téléchargement>/solution_n=604_d=11.json`
- Début : 2026-10-12T19:17:23Z ; durée murale 8.8 s ; code de sortie 0

## Résultat

- Valeur obtenue : `604` (entiers-exacts)
- Égalité exacte avec la valeur revendiquée : oui
- 604 vecteurs distincts, dimension 11, norme^2 commune = 36 + 0 sqrt 2 (moteurs A et B).
- 182 106 paires ; distance^2 minimale exacte = 36 + 0 sqrt 2 = norme^2 (rapport exact 1) ; 19 704 paires à égalité ; 0 violation (moteurs A et B).
- Moteur B : produit scalaire maximal exact = 18 + 0 sqrt 2 = norme^2 / 2 ; sympy confirme les 22 valeurs distinctes du produit scalaire.
- Degrés dans le graphe des contacts (distance^2 = 36) : 108 sommets de degré 36, 384 de 67, 96 de 84, 16 de 108.

## Contrôles

| Type | Réalisé | Attendu | Obtenu | Description |
|---|---|---|---|---|
| negatif | oui | echec | echec | Vecteur perturbé (+1 sur une coordonnée du vecteur 5, N1) et vecteur de norme 36 mis à la place du dernier mais trop proche de 6 e_1 (3 sqrt 2, 3 sqrt 2, 0.., N5 : distance^2 = 72 - 36 sqrt 2 à e_1, signe décidé avec a > 0, b < 0, a^2 < 2 b^2) : les deux moteurs rejettent, pour la norme (N1) et la seule distance (N5). |
| negatif | oui | echec | echec | 605e vecteur ajouté : copie exacte du vecteur 7 (N2, doublon), de mauvaise norme 49 (N3), de norme 36 mais à distance^2 = 72 - 48 sqrt 2 < 36 de 6 e_1 (N4) : les deux moteurs rejettent chaque cas pour le motif attendu. |
| negatif | oui | echec | echec | Entrées hors format : 603 vecteurs pour 604 revendiqués (N6), flottant 6.0 (N7), booléen false (N8), coordonnée 6 + sqrt 2 qui rend la norme^2 38 + 12 sqrt 2 (N9) : rejetés par les deux moteurs. |
| controle-positif | oui | succes | succes | Le vérificateur peut accepter : 603 premiers vecteurs revendiqués 603 (P1), 16 premiers vecteurs +-6 e_i revendiqués 16 avec distance^2 minimale exacte 72 (P2), fichier intact (P3, minimum 36 et 19 704 égalités identiques dans A et B). |
| second-moteur | oui | succes | succes | Moteur B (Gram int64 + signe par la norme du corps + sympy, sans import de A) : même verdict VALIDE, même minimum exact 36 et mêmes 19 704 paires à égalité que le moteur A. Écrit par le même opérateur : indépendance de code, pas d'auteur. |
| lean | non | — | — | Pas de certification Lean ; la revendication n'en porte pas. |
| horodatage | non | — | — | L'empreinte de ce rapport est horodatée après son figement (rapport.json.ots et MANIFEST.sha256 du dossier reproductions/) ; ce contrôle ne peut pas figurer dans le rapport sans changer son empreinte : à vérifier par stamp.py verify. |

## Écarts

- La plateforme a clos la dimension 11 : le vérificateur en ligne (lu le 2026-10-12) porte sur n = 594 vecteurs de flottants ou décimaux à 80 chiffres et ne reçoit pas ce fichier à 604 vecteurs en Z[sqrt 2]. Nos moteurs appliquent le même critère (distance^2 minimale >= norme^2 commune) en entiers exacts ; on n'a donc pas rejoué le vérificateur de la plateforme.
- Le fichier n'a qu'un commit (d97e89d1, 2026-04-12 « add n=604 ») ; la date de l'annonce dans avancees.json est le 2026-04-11 : cohérent, sans effet sur la valeur.
- Le moteur B suppose les normes égales pour son critère <x,y> <= 18 ; il vérifie d'abord la diagonale de Gram. Dans les contrôles N3 et N9 (normes inégales), son compte de paires violées diffère de celui de A (seuil absolu 36), sans effet sur le rejet.

## Artefacts

| Fichier | Rôle | sha256 |
|---|---|---|
| `scripts/verif_a.py` | moteur A : entiers Python, couples (a, b) de Z[sqrt 2], signe par cas et comparaison a^2 / 2b^2 | `a7967de523754721…` |
| `scripts/verif_b.py` | moteur B : matrice de Gram numpy int64, signe par la norme du corps, recontrôle sympy ; sans import de A | `6947c167370449c1…` |
| `scripts/controles.py` | contrôles négatifs N1-N9 et positifs P1-P3, passés aux deux moteurs | `91ed703f600d30fa…` |
| `scripts/rejouer.py` | lanceur : vérifie le sha256 de la solution, lance les quatre étapes en python -I, écrit artefacts/*.out | `859b4d9a6e572f29…` |
| `scripts/statistiques.py` | description exacte du contenu du fichier (parties en sqrt 2, valeurs de distance^2, degrés de contact) | `57394051c76d2042…` |
| `scripts/empreintes.py` | sha256 et sha1 d'objet git d'un fichier (épinglage de la source) | `bd3804108827edaa…` |
| `artefacts/source.txt` | URL épinglée, commit, blob git, sha256 et date de lecture de la solution ; limites de licence | `c99675026592490d…` |
| `artefacts/sortie_moteur_a.out` | sortie du moteur A : VALIDE, minimum exact 36, 19 704 paires à égalité | `9a80693ddb5c2fc1…` |
| `artefacts/sortie_moteur_b.out` | sortie du moteur B : VALIDE, même minimum et même compte ; sympy sur 22 valeurs | `4b6b0170bd39b1e4…` |
| `artefacts/sortie_controles.out` | tableau des contrôles : 9 rejets attendus et 3 acceptations attendues, tous conformes | `0cdfffa5cf97aa4a…` |
| `artefacts/sortie_statistiques.out` | contenu exact du fichier : 108 vecteurs avec partie en sqrt 2, 22 valeurs de distance^2 | `4441d2673a777814…` |

## À décider par Antoine

- Changer ou non le statut public de ea-kissing-number-d11 (actuellement non-evalue) : une reproduction privée ne le change pas par elle-même.
- Publier ou non ce verdict.
