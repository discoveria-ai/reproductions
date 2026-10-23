# Reproduit — score A(u, v) du chargement d'anneau à 15 paires = 1.125

<!-- Généré par scripts/reproductions.py depuis rapport.json : ne pas éditer. -->

- Rapport : `repro-ea-ring-loading-15-2026-10-12` (format `discoveria-rapport-reproduction/1`), rejoué le 2026-10-12, publication : privee.
- Avancée : `ea-ring-loading-15`.
- Opérateur : DiscoverIA (agent Claude pour Antoine Olivier) — deuxième reproduction certifiée externe de DiscoverIA ; session Claude Code 2026-10-12-claude-code-55938116086b, sous-agent exécutant sur mandat de la session ; code écrit pour ce rejeu, indépendant de la plateforme EinsteinArena.

## Revendication

Problème de chargement d'anneau à 15 paires (EinsteinArena, problème 30) : on choisit 15 paires (u_i, v_i) de rationnels positifs ou nuls avec u_i + v_i <= 1 ; pour chacun des 2^15 = 32 768 choix z_i dans {v_i, -u_i}, on calcule le maximum sur k = 1..15 de |somme des k premiers z_i - somme des suivants| ; le score A(u, v) est le minimum de ces maxima, à maximiser. La soumission 2576 de l'agent JSAgent-Ring15 (2026-09-12) porte le score stocké 1.125, que nous lisons comme 9/8 ; l'ancienne valeur publiée est celle de la construction d'AlphaEvolve, 40317937698944779/36028797018963968 (environ 1.1190475684692773).

> "agentName":"JSAgent-Ring15","score":1.125

- Valeur revendiquée : `9/8`
- Source : https://einsteinarena.com/api/solutions/best?problem_id=30&limit=10 @ `3b9d1e3a1278889d29d6120e13db84a6cd45e20c4d2601f98c77a3c412425e80`

## Verdict

**Reproduit.** La soumission 2576 (15 paires rationnelles) a été rejouée en arithmétique rationnelle exacte, sans flottant : les 32 768 choix adverses donnent un minimum des maxima exactement égal à 9/8, soit la valeur revendiquée (flottant stocké 1.125), strictement supérieure à l'ancienne valeur 40317937698944779/36028797018963968 de l'écart 214458947389685/36028797018963968. Deux moteurs de code distinct et sympy concordent (même valeur, mêmes 46 choix minimaux) ; treize contrôles négatifs sont rejetés pour le motif attendu et sept contrôles positifs passent, dont la valeur d'AlphaEvolve retrouvée exactement. Le rejeu établit que l'instance vaut 9/8 sous la définition de l'énoncé de la plateforme (« Under active review ») ; il n'établit ni que 9/8 est un record au sens de la littérature, ni une optimalité, ni l'attribution.

## Portée

**Établi par le rejeu**
- La soumission 2576 (JSAgent-Ring15, sha256 canonique 3b9d1e3a1278889d29d6120e13db84a6cd45e20c4d2601f98c77a3c412425e80, lue sur l'API le 2026-10-12 à 19:38Z) contient exactement 15 paires de chaînes rationnelles qui respectent toutes les règles de format de la plateforme (chaîne de 1 à 80 caractères, décimal ou fraction, numérateur et dénominateur réduits sur 64 bits au plus) et u + v <= 1 ; dénominateur commun 16.
- Les 32 768 choix adverses ont été énumérés en arithmétique exacte par deux moteurs de code distinct (A : fractions.Fraction ; B : entiers au dénominateur commun 16, plus un recalcul complet sympy.Rational) : le minimum des maxima vaut exactement 9/8, atteint par 46 choix, avec la même liste de masques (sha256 f524c05fce6b86c8293e975c32847c71ee4e6785c0fc40f0b62052a54bd8ac52) dans A, B et sympy.
- 9/8 est égal à la valeur revendiquée 1.125 (lue comme 9/8) et supérieur strictement à l'ancienne valeur 40317937698944779/36028797018963968 : l'écart exact est 214458947389685/36028797018963968 (environ 0.00595, estimé en décimal), soit un rapport d'environ 1.0053.
- Contrôle positif indépendant du code : la soumission 2566 (AlphaEvolve) donne exactement 40317937698944779/36028797018963968, nombre que l'énoncé de la plateforme cite ; pour les sept soumissions lues, float(valeur exacte) égale le score stocké ; trois invariances exactes du problème (échange u/v, renversement de l'ordre, homogénéité) sont vérifiées par les deux moteurs.

**Supposé par la revendication, non prouvé**
- La revendication publique est le flottant stocké 1.125 ; nous le lisons comme 9/8. Beaucoup de rationnels s'arrondissent à ce flottant : ce qui est établi est que la valeur exacte de la soumission est 9/8, pas autre chose.
- La définition du problème est celle de l'énoncé de la plateforme, qui la marque « Under active review » (exactitude mathématique, robustesse du vérificateur) ; elle n'a pas été comparée à la littérature (borne supérieure 13/10 de Däubel, notebook d'AlphaEvolve, problème 61 du dépôt d'AlphaEvolve).
- Notre définition est équivalente au texte du vérificateur de la plateforme tel que nous l'avons lu (k de 1 à 15, critère |2 P_k - T|, pire cas initialisé à 0, mêmes règles de format) ; cette équivalence est établie par lecture, le code téléchargé n'a pas été exécuté.
- Les 15 paires lues sur l'API sont bien celles soumises : l'hébergeur est cru, l'empreinte ne fait que figer ce qui a été lu (source modifiable et non épinglable sur un commit, voir écarts).

**Cité, non reconstruit ici**
- Que 9/8 soit un record au sens de la littérature : aucune recherche de littérature n'a été faite ; le papier arXiv 2606.10402 v2 ne mentionne pas ce problème (estimé : texte intégral parcouru par résumé automatique, pas par recherche exacte) et le record est postérieur au papier.
- Que cette instance à 15 paires minore la constante du chargement d'anneau (intervalle cité dans l'énoncé : environ 1.119047568 à 1.3) : lu sur l'énoncé, non redémontré ; la borne supérieure 1.3 n'est pas examinée, et aucune optimalité n'est en jeu.
- L'ancienne valeur d'AlphaEvolve est recalculée à partir de la soumission 2566 de l'API, pas du notebook d'origine d'AlphaEvolve, non lu.
- L'attribution à l'agent JSAgent-Ring15 et la chronologie (2026-09-12) : lues sur l'API, non comparées à une autre source ; le vérificateur de la plateforme n'a pas été exécuté.

## Exécution

- Environnement : Windows 11, Python 3.13.15, sympy 1.14.0 ; interpréteur lancé avec -I (mode isolé) et -B ; données téléchargées dans un dossier séparé du code ; aucun réseau pendant le rejeu
- Commande : `python -B -I -X utf8 scripts/rejouer.py <dossier-téléchargement>/best_limit10.json <dossier-téléchargement>/problem.json <dossier-de-sortie-vide>`
- Début : 2026-10-12T19:44:51Z ; durée murale 80.5 s ; code de sortie 0

## Résultat

- Valeur obtenue : `9/8` (rationnels-exacts)
- Égalité exacte avec la valeur revendiquée : oui
- 15 paires valides ; 32 768 choix énumérés ; minimum exact des maxima = 9/8 = 1.125 (moteurs A et B, et sympy sur les 32 768 choix).
- 46 choix atteignent le minimum (même nombre et même liste triée de masques dans A, B et sympy ; bit i du masque = 1 si z_i = -u_i).
- Ancienne valeur : 40317937698944779/36028797018963968 ; 9/8 - ancienne = 214458947389685/36028797018963968 > 0.
- Autres soumissions, valeurs exactes : GPT-Explorer 2574 = 47/42, Wilhelmina 2593 = 1266637395197951/1125899906842624 (inférieure à 9/8 d'environ 9e-16) et 2592 = 79164837199871/70368744177664, AlphaEvolve 2566 = 40317937698944779/36028797018963968.

## Contrôles

| Type | Réalisé | Attendu | Obtenu | Description |
|---|---|---|---|---|
| negatif | oui | echec | echec | Entrées hors format rejetées par les deux moteurs pour le motif attendu : 14 paires (N1), paire (1/2, 3/4) avec u + v > 1 (N2), valeur négative -7/16 (N3), nombre JSON 0.25 au lieu d'une chaîne (N4), dénominateur 2^65 (N5), texte non rationnel 1/4.5 (N6). |
| negatif | oui | echec | echec | Configurations valides modifiées ou voisines dont la valeur exacte n'est pas 9/8, identique dans A et B, strictement inférieure à 9/8 : paire 4 changée en (1/4, 1/8) donne 1 (N7), paire 1 changée en (999999/1000000, 0) donne 1124999/1000000 (N8), paire 7 réduite de 1e-9 donne 1124999999/1000000000 (N9), soumission 2593 de Wilhelmina (score stocké 1.1249999999999991) donne 1266637395197951/1125899906842624 (N10), soumissions 2574 (47/42, N11) et 2566 d'AlphaEvolve (N12), quinze paires nulles donne 0 (N13). La revendication 9/8 est refusée pour chacune. |
| controle-positif | oui | succes | succes | Valeurs connues hors de notre code : la soumission 2566 d'AlphaEvolve donne exactement la valeur citée par l'énoncé (P2) ; float(valeur exacte) = score stocké pour les 7 soumissions (P3) ; la soumission 2576 donne 9/8 (P1). Invariances exactes : échange u/v (P4) et renversement de l'ordre (P5) laissent 9/8, division par 2 donne 9/16 (P6), division par 3 de la soumission 2574 donne 47/126 (P7). |
| second-moteur | oui | succes | succes | Moteur B (analyse des chaînes à la main, entiers au dénominateur commun 16, parcours en profondeur, critère |2 P_k - T| ; recalcul complet sympy.Rational par itertools.product ; aucun import de A) : même verdict VALIDE, même valeur exacte 9/8, mêmes 46 choix minimaux et même liste de masques que le moteur A (fractions.Fraction, préfixe et suffixe séparés). Écrit par le même opérateur : indépendance de code, pas d'auteur. |
| lean | non | — | — | Pas de certification Lean ; la revendication n'en porte pas. |
| horodatage | non | — | — | L'empreinte de ce rapport est horodatée après son figement (rapport.json.ots et MANIFEST.sha256 du dossier reproductions/) ; ce contrôle ne peut pas figurer dans le rapport sans changer son empreinte : à vérifier par stamp.py verify. |

## Écarts

- Source non épinglable sur un commit : le dépôt togethercomputer/EinsteinArena-new-SOTA ne contient aucun fichier de ce problème (arbre complet listé le 2026-10-12, tête de main c388c6f7) ; la seule source est l'API de la plateforme, modifiable. On épingle par sha256 canonique de chaque soumission (artefacts/source.txt) et par sha256 de l'énoncé (4573 octets, 49f4427e30688fa67b37a10e50f1b33d6656d32cb00a67d9f1b50fed73bf5a9a) ; le sha256 du corps de la réponse (985f7062...) change dès qu'une nouvelle soumission arrive.
- La plateforme marque l'énoncé et le vérificateur « Under active review » (lu le 2026-10-12) : ils peuvent être révisés après ce rejeu ; l'énoncé et le vérificateur lus sont figés par leur sha256.
- Le vérificateur de la plateforme n'a pas été exécuté (code téléchargé, non fiable) ; il a été lu en entier et ses règles reproduites dans le moteur A. Le score stocké est le flottant float(9/8) = 1.125, identique à notre valeur exacte arrondie.
- Le papier arXiv 2606.10402 ne couvre pas ce problème : la définition et la valeur revendiquée viennent de l'API seule (l'énoncé du mandat citait le papier ; sa v2 n'en parle pas, estimé).
- La solution (15 paires) n'est pas copiée dans la fiche : les données de l'API n'ont aucune licence lisible ; on garde URL et empreintes.
- Le résultat est une configuration à 46 pires cas égaux : le minimum 9/8 est atteint par 46 des 32 768 choix, sans incidence sur la valeur.

## Artefacts

| Fichier | Rôle | sha256 |
|---|---|---|
| `scripts/verif_a.py` | moteur A : fractions.Fraction, préfixe et suffixe séparés, 32 768 choix, règles de format de la plateforme | `9d998ff6df1c05e0…` |
| `scripts/verif_b.py` | moteur B : entiers au dénominateur commun, parcours en profondeur, critère |2 P_k - T|, recalcul complet sympy.Rational ; sans import de A | `130bd17fba12e437…` |
| `scripts/controles.py` | contrôles négatifs N1-N13 et positifs P1-P7, passés aux deux moteurs | `b57f1528165f93f7…` |
| `scripts/rejouer.py` | lanceur : vérifie les sha256 canoniques des soumissions et le sha256 de l'énoncé, lance les trois étapes en python -I, écrit artefacts/*.out | `83343950e9f022ae…` |
| `scripts/empreintes.py` | sha256 d'un fichier et sha256 canonique d'une soumission de l'API (épinglage de la source) | `954ffdd0bf2f7e8c…` |
| `artefacts/source.txt` | URL, empreintes, date de lecture et limites de la source (API non épinglable sur un commit) ; solution non copiée | `131abedcdf3080ba…` |
| `artefacts/sortie_moteur_a.out` | sortie du moteur A : VALIDE, valeur exacte 9/8, 46 masques minimaux | `11e9d70eca1d1b12…` |
| `artefacts/sortie_moteur_b.out` | sortie du moteur B : VALIDE, 9/8, mêmes 46 masques, concordance sympy | `4f45c66b4b37b79e…` |
| `artefacts/sortie_controles.out` | tableau des contrôles : 13 négatifs et 7 positifs, tous conformes | `70a830404dcb273c…` |

## À décider par Antoine

- Changer ou non le statut public de ea-ring-loading-15 (actuellement non-evalue) : une reproduction privée ne le change pas par elle-même.
- Publier ou non ce verdict.
