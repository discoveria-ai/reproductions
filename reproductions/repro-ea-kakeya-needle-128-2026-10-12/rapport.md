# Reproduit — aire exacte de la réunion des 128 triangles de Kakeya, arrondie au double le plus proche (sortie de evaluate du vérificateur de la plateforme) = 0.10675394011230244

<!-- Généré par scripts/reproductions.py depuis rapport.json : ne pas éditer. -->

- Rapport : `repro-ea-kakeya-needle-128-2026-10-12` (format `discoveria-rapport-reproduction/1`), rejoué le 2026-10-12, publication : privee.
- Avancée : `ea-kakeya-needle-128`.
- Opérateur : DiscoverIA (agent Claude pour Antoine Olivier) — session Claude Code 2026-10-12-claude-code-55938116086b, sous-agent exécutant sur mandat de la session ; code écrit pour ce rejeu, indépendant de la plateforme EinsteinArena (son vérificateur public n'est utilisé que comme témoin).

## Revendication

Pour n = 128, les 128 décalages publiés (chaînes décimales à 25 décimales au plus) donnent, pour les triangles T_j = enveloppe convexe de (x_j, 0), (x_j + 1/128, 0), (x_j + j/128, 1), j = 1..128, une réunion d'aire 0,10675394011230244 (double renvoyé par le vérificateur public de la plateforme) : C_T(128) <= 0,10675394011230244, contre 0,107067 pour l'état de l'art cité par l'énoncé (la Station, août 2026). La valeur revendiquée est un double : on la note comme le rationnel dyadique exact de ce double.

> "agentName":"Ghazt","bestScore":0.10675394011230244

- Valeur revendiquée : `961554009820195/9007199254740992`
- Source : https://einsteinarena.com/api/solutions/best?problem_id=26&limit=1 @ `8a9e475f2c54b96d21b6bb385b04d55d559029a9ad96b83e92eddb9173609c29`

## Verdict

**Reproduit.** Les 128 décalages de la soumission 2608 ont été rejoués en rationnels exacts (Fraction de chaîne décimale, sans flottant) : l'aire exacte de la réunion des 128 triangles est 22598724902070159499743765877870160455101358423617701/211689843750000000000000000000000000000000000000000000, soit 0,10675394011230243302..., et son double est 0,10675394011230244, la valeur revendiquée. Deux moteurs de code distinct (balayage en hauteur, balayage en abscisse depuis les sommets) et le vérificateur public de la plateforme donnent la même fraction ; onze contrôles négatifs sont rejetés pour le motif attendu et les contrôles positifs passent. L'aire est exactement inférieure à 0,107067 (écart 3,13e-4), donc la construction établit C_T(128) <= 0,1067539401123025. L'égalité avec la revendication est celle de l'arrondi au double (la revendication est un double, voir écarts) ; le rejeu n'établit ni que ce soit un record de la littérature, ni l'optimalité, ni l'attribution à Ghazt.

## Portée

**Établi par le rejeu**
- Objet : pour j = 1..128, T_j = conv{(x_j, 0), (x_j + 1/128, 0), (x_j + j/128, 1)} ; quantité = aire de la réunion des T_j (énoncé de la plateforme, api/problems/kakeya-needle-128, sha256 7fd868a0...). Les 128 offsets de la soumission 2608 (agent Ghazt, 2026-10-06T05:03Z) sont 128 chaînes décimales conformes (au plus 25 décimales, au plus 4 chiffres entiers), lues par Fraction(chaîne), jamais par un flottant ; la forme canonique a le sha256 épinglé 8a9e475f... (3 648 octets).
- Aire exacte, rationnelle, sans approximation : 22598724902070159499743765877870160455101358423617701/211689843750000000000000000000000000000000000000000000 (dénominateur de 54 chiffres), soit 0,106753940112302433024700864412018634952114269... (45 décimales, tronquées). Trois calculs exacts donnent exactement la même fraction : moteur A, moteur B, et le vérificateur public de la plateforme exécuté comme témoin. Aucune partie non rationnelle : pas d'intervalle, pas de tolérance.
- La valeur revendiquée est un double : float(aire exacte) = 0,10675394011230244, égal à la valeur revendiquée (arrondi correct de CPython) ; l'aire exacte est dans [double - demi-ulp, double + demi-ulp] (test exact, demi-ulp = 2^-57) ; elle diffère du décimal affiché de -6,975e-18 (plus petite que lui).
- Bornes exactes : aire < 0,107067 (état de l'art cité, écart 3,131e-4, soit 0,292 %) et < 0,10706663656163481 (graine de la plateforme) ; donc la construction publiée établit C_T(128) <= 0,1067539401123025 (arrondi supérieur de l'aire), strictement sous 0,107067. Le classement public à quatre entrées est recalculé : Ghazt < CrossingPaths < JSAgent < Station dans l'ordre exact, et chaque score de l'API est le double de l'aire exacte recalculée.
- Deux moteurs de code distinct (A : balayage en hauteur, formules de section de l'énoncé ; B : balayage en abscisse depuis les sommets des triangles, sans ces formules, donc il valide aussi la formule) donnent la même fraction exacte ; différentiel A/B sur 80 cas aléatoires à petit n (offsets en huitièmes, croisements triples et triangles confondus) sans divergence ; valeurs analytiques n=1 (1/2), n=2 offsets égaux (3/8), 128 triangles disjoints (1/2) retrouvées exactement ; invariance par translation vérifiée.

**Supposé par la revendication, non prouvé**
- La définition : c'est celle de l'énoncé de la plateforme, marqué « Under active review ». Les sommets des triangles ont été comparés à la définition de la section 6.4 d'arXiv 2608.23691 (the Station) lue par un outil de résumé de page, non relue mot à mot ; le moteur B part de ces sommets et retrouve la même aire que les formules de section de l'énoncé.
- Le fichier de la solution : l'API n'est pas versionnée. La soumission 2608 est épinglée par le sha256 de la forme canonique de ses offsets (et non par un commit), identique à deux relevés à 3 minutes d'écart ; on se fie à la plateforme pour que ces offsets soient bien ceux soumis par Ghazt le 2026-10-06.
- La valeur revendiquée est le double publié, pas un rationnel : l'égalité établie est celle de l'arrondi au double de l'aire exacte, pas l'égalité entre l'aire exacte et le décimal 0,10675394011230244 (qui diffèrent de 7e-18).

**Cité, non reconstruit ici**
- Les valeurs citées : 0,107067 (la Station, arXiv 2608.23691 section 6.4), 0,114810 (AlphaEvolve) et 0,109148 (HorizonMath) sont lues, non reconstruites ; seule la graine de la plateforme, 0,10706663656163481, a été recalculée (elle égale le score de l'entrée 2563 de l'API).
- Que 0,10675394 soit un record au sens de la littérature : aucune recherche de littérature n'a été faite ; l'énoncé de la plateforme recommande de la faire avant de confirmer un record.
- L'attribution à l'agent Ghazt et la date de soumission : champs de l'API, non vérifiables ici.
- Aucune optimalité : le rejeu établit une borne supérieure sur C_T(128), pas la valeur de l'infimum ; aucune borne inférieure n'est en jeu.

## Exécution

- Environnement : Windows 11, Python 3.13.15 (bibliothèque standard seule pour les moteurs A et B ; shapely 2.1.2 pour le témoin flottant) ; interpréteur lancé avec -B -I ; solution extraite dans un dossier temporaire supprimé à la fin ; aucun réseau pendant le rejeu
- Commande : `python -B -I -X utf8 scripts/rejouer.py <dossier-téléchargement>/best.json <dossier-téléchargement>/problem.json <dossier-de-sortie-vide>`
- Début : 2026-10-12T19:55:13Z ; durée murale 80.21 s ; code de sortie 0

## Résultat

- Valeur obtenue : `961554009820195/9007199254740992` (rationnels-exacts)
- Égalité exacte avec la valeur revendiquée : oui
- Aire exacte de la réunion = 22598724902070159499743765877870160455101358423617701/211689843750000000000000000000000000000000000000000000 = 0,1067539401123024330247... (moteurs A et B et témoin de la plateforme, identiques).
- valeur_obtenue est le double de cette aire exacte, écrit comme rationnel dyadique (961554009820195/9007199254740992) : l'arithmétique est exacte (rationnels), l'égalité avec la valeur revendiquée est celle de l'arrondi au double, la revendication étant un double (voir portée et écarts).
- Hauteurs de rupture du moteur A : 21 736 ; abscisses de rupture du moteur B : 29 733 (balayages différents).
- Aire exacte - 0,10675394011230244 = -6,975e-18 ; |aire - double| = 3,713e-18 < demi-ulp 2^-57 (6,94e-18).
- Comparaisons exactes : aire < 0,107067 (écart 3,131e-4, 0,292 %) ; < 0,109148 (HorizonMath, 2,193 %) ; < 0,114810 (AlphaEvolve, 7,017 %).
- Témoin flottant (shapely, float64, non certifiant) : 0,10675394011230258, écart 1,4e-16 avec la valeur revendiquée.

## Contrôles

| Type | Réalisé | Attendu | Obtenu | Description |
|---|---|---|---|---|
| negatif | oui | echec | echec | Solution altérée, valeur revendiquée inchangée : offset 17 décalé de +1e-6 (N1), offsets 0 et 127 échangés (N2), offsets tous nuls (N3, aire 0,251953125), offsets dans l'ordre inverse (N4) : les deux moteurs rejettent chaque cas parce que l'aire exacte arrondie au double diffère, avec la même aire exacte dans A et B. |
| negatif | oui | echec | echec | Solution intacte, revendication plus basse : 0,1067 (N5) et un double plus bas, 0,10675394011230242 (N6) : rejetés par les deux moteurs ; le contrôle est donc sensible au dernier chiffre du double. |
| negatif | oui | echec | echec | Entrées hors format : 127 offsets (N7), 26 décimales (N8), nombre JSON au lieu d'une chaîne (N9), notation scientifique '1e-3' (N10), 5 chiffres entiers (N11) : rejetés par les deux moteurs pour le motif attendu. |
| controle-positif | oui | succes | succes | Le vérificateur peut accepter : n=1 (aire 1/2, P1), n=2 à offsets égaux (3/8 calculé à la main, P2), 128 triangles disjoints (1/2, P3), solution 2608 intacte (P4), les quatre entrées du classement public dont la graine de la Station, chaque score de l'API retrouvé comme double de l'aire exacte et ordre exact Ghazt < CrossingPaths < JSAgent < Station (P5), 80 cas aléatoires où A et B donnent la même fraction (P6). |
| controle-positif | oui | succes | succes | Témoin : le vérificateur public de la plateforme (texte sha256 4d7e8ddd..., lu avant exécution, lancé en python -I) calcule la même aire exacte que le moteur A et renvoie le même double. C'est le code du revendicateur : un témoin, pas un contrôle indépendant. |
| second-moteur | oui | succes | succes | Moteur B (balayage en abscisse depuis les sommets, sans import de A ni formules de section) : même verdict VALIDE et même fraction exacte que le moteur A. Écrit par le même opérateur et lisant la même forme canonique des offsets : indépendance de code et de méthode, pas d'auteur. |
| lean | non | — | — | Pas de certification Lean ; la revendication n'en porte pas. |
| horodatage | non | — | — | L'empreinte de ce rapport est horodatée après son figement (rapport.json.ots et MANIFEST.sha256 du dossier reproductions/) ; ce contrôle ne peut pas figurer dans le rapport sans changer son empreinte : à vérifier par stamp.py verify. |

## Écarts

- Le mandat demandait une URL épinglée sur un commit : impossible. Le dépôt togethercomputer/EinsteinArena-new-SOTA n'a pas de dossier kakeya ; la solution n'est que dans l'API EinsteinArena, qui n'est pas versionnée (la réponse brute change quand le classement change). Épinglage par le sha256 de la forme canonique des offsets, plus l'id de soumission 2608 et ses dates (artefacts/source.txt).
- La valeur revendiquée est un double. L'aire exacte (0,10675394011230243302...) n'est pas égale au décimal publié (0,10675394011230244) : elle l'est après arrondi au double, qui est ce que mesure le vérificateur de la plateforme. egalite_exacte est donc vrai au sens de l'arrondi du double, pas au sens de l'égalité de deux rationnels distincts ; ce choix peut être contesté.
- Limite de portée du score (I1) : un décalage de 1e-25 sur un offset change l'aire exacte de 8,9e-41 sans changer le double ; le score ne distingue pas deux solutions aussi proches, c'est pourquoi la fiche donne la fraction exacte.
- L'énoncé renvoie à « Section 4.4 of The Station » ; selon la lecture (par outil de résumé) de arXiv 2608.23691v2, la section 4.4 traite des mécanismes de la Station et le problème de Kakeya est en 6.4. Sans effet sur la valeur.
- L'énoncé et le vérificateur sont marqués « Under active review » par la plateforme ; le texte lu le 2026-10-12 (sha256 4d7e8ddd...) a pu changer depuis l'évaluation de la soumission (2026-10-06T05:15Z). Sans effet : le témoin exécuté donne la même aire exacte et le même double.
- Le vérificateur public accepte des espaces autour des offsets et un signe « + » ; nos moteurs sont plus stricts (chaîne décimale base 10 avec « - » facultatif). Aucun des 128 offsets n'en contient : sans effet.
- Le papier arXiv 2606.10402 (EinsteinArena, mai 2026) ne porte pas ce record, postérieur : l'objet vient de l'énoncé de l'API ; la valeur de référence 0,107067 vient d'arXiv 2608.23691.
- Le témoin flottant (shapely 2.1.2) dépend de la bibliothèque : l'empreinte de sortie_temoin_flottant.out peut changer avec sa version, sans effet sur le verdict qui repose sur l'arithmétique exacte.

## Artefacts

| Fichier | Rôle | sha256 |
|---|---|---|
| `scripts/verif_a.py` | moteur A : balayage en hauteur y ; sections affines [x_j + (j/n) y, x_j + 1/n + ((j-1)/n) y], croisements exacts, trapèzes, entiers Python | `9d9d255112aed117…` |
| `scripts/verif_b.py` | moteur B : balayage en abscisse x depuis les sommets des triangles (sans les formules de section), bandes délimitées par sommets et croisements d'arêtes, largeur x longueur(milieu), sans import de A | `d5bd619b5487522c…` |
| `scripts/controles.py` | contrôles négatifs N1-N11, information I1, positifs P1-P6 (analytiques, classement public, différentiel A/B), passés aux deux moteurs | `cd18ca8377eb2883…` |
| `scripts/rejouer.py` | lanceur : extrait la solution 2608, refuse si le sha256 canonique diffère, lance les sept étapes en python -B -I, écrit artefacts/*.out | `b5a6d719550e9158…` |
| `scripts/extraire.py` | extraction des 128 offsets de la réponse de l'API et écriture de la forme canonique (empreinte épinglée) | `6d688b3fad8a4ec2…` |
| `scripts/quantite.py` | aire exacte, encadrement par le demi-ulp du double, comparaisons exactes avec 0,107067 et les valeurs citées | `93a55362487f8f1c…` |
| `scripts/temoin_plateforme.py` | témoin : exécute le vérificateur public de la plateforme seulement si le sha256 de son texte est celui du texte lu (empreinte gravée ; sinon il n'exécute rien) et compare son aire exacte à celle du moteur A | `50b9e195a5150a3b…` |
| `scripts/temoin_flottant.py` | témoin flottant non certifiant (shapely/GEOS, float64) ; garde-fou de définition seulement | `b51b0e69dd11acf2…` |
| `scripts/empreintes.py` | sha256 et sha1 d'objet git d'un fichier (épinglage) | `bd3804108827edaa…` |
| `artefacts/source.txt` | URL, id de soumission, empreintes (réponse, forme canonique, énoncé, vérificateur) et limites de licence ; pas de commit possible | `3fc0662f27d8d91f…` |
| `artefacts/sortie_extraction.out` | extraction : id 2608, agent, date, score de l'API, 128 offsets, sha256 canonique | `868689ad58539643…` |
| `artefacts/sortie_moteur_a.out` | sortie du moteur A : VALIDE, aire exacte (fraction), égalité du double avec la valeur revendiquée | `02089b48f8acafaa…` |
| `artefacts/sortie_moteur_b.out` | sortie du moteur B : VALIDE, même fraction exacte que A | `e2b59dc6d209efc9…` |
| `artefacts/sortie_temoin_plateforme.out` | sortie du témoin (vérificateur de la plateforme) : même aire exacte que A, double égal à evaluate | `3d8e8e352a198338…` |
| `artefacts/sortie_temoin_flottant.out` | sortie du témoin flottant (dépend de la version de shapely : ne pas exiger l'identité octet à octet) | `4795159a36a83d10…` |
| `artefacts/sortie_quantite.out` | aire exacte, demi-ulp, comparaisons exactes avec les valeurs citées | `e9db3a1138b83404…` |
| `artefacts/sortie_controles.out` | tableau des contrôles : 11 rejets attendus, 1 information, 6 familles d'acceptation attendues, tous conformes | `c8b8e4bea1f4c4b5…` |

## À décider par Antoine

- Changer ou non le statut public de ea-kakeya-needle-128 (actuellement non-evalue) : une reproduction privée ne le change pas par elle-même.
- Publier ou non ce verdict.
- Faire ou non une recherche de littérature pour savoir si ce score était déjà publié (l'énoncé de la plateforme le recommande avant de confirmer un record).
