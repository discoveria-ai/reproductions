# Reproduit — nombre de mots d'un code binaire de longueur 16 corrigeant deux suppressions = 219

<!-- Généré par scripts/reproductions.py depuis rapport.json : ne pas éditer. -->

- Rapport : `repro-ea-two-deletion-code-16-2026-10-12` (format `discoveria-rapport-reproduction/1`), rejoué le 2026-10-12, publication : privee.
- Avancée : `ea-two-deletion-code-16`.
- Opérateur : DiscoverIA (agent Claude pour Antoine Olivier) — deuxième reproduction certifiée externe de DiscoverIA ; session Claude Code 2026-10-12-claude-code-55938116086b, sous-agent exécutant sur mandat de la session ; code écrit pour ce rejeu, indépendant de la plateforme EinsteinArena.

## Revendication

Il existe un code binaire de longueur 16 corrigeant deux suppressions, de 219 mots : 219 mots binaires de longueur 16, deux à deux distincts, tels que deux mots distincts n'aient aucun descendant commun, un descendant étant un mot de longueur 14 obtenu en supprimant deux positions. Soumission d'id 2605 de l'agent nightshift-dc16 sur la plateforme EinsteinArena, évaluée le 2026-10-05 (score 219), contre 215 pour le record public cité par l'énoncé de la plateforme (Weindel et Heckel, v2).

> "agentName":"nightshift-dc16","bestScore":219

- Valeur revendiquée : `219`
- Source : https://einsteinarena.com/api/solutions/best?problem_id=34&limit=4 @ `8fece05aec4a8ed9f4aac3b7078ad4f82f6b7e66ef9b4adc214077e835bea218`

## Verdict

**Reproduit.** Le code de 219 mots publié par l'API de la plateforme (solution d'id 2605, nightshift-dc16) a été rejoué sans flottant ni tolérance : 219 mots binaires de longueur 16 deux à deux distincts, boules de deux suppressions deux à deux disjointes (moteur A : 6 168 descendants distincts pour une somme de tailles de boules de 6 168 ; moteur B : plus longue sous-séquence commune au plus 13 sur les 23 871 paires, 4 599 à 13). Deux moteurs d'algorithmes distincts concordent, dix contrôles négatifs sont rejetés pour le motif attendu et avec les mêmes paires en conflit, et le vérificateur public de la plateforme accepte les mêmes mots. Le rejeu établit qu'un code de 219 mots existe ; il n'établit ni que 219 dépasse le record de la littérature, ni l'attribution à l'agent, ni l'optimalité.

## Portée

**Établi par le rejeu**
- Propriété vérifiée, exactement celle de l'énoncé de la plateforme : C est un ensemble de mots de {0,1}^16, deux à deux distincts, et D2(x) inter D2(y) est vide pour tous x != y de C, D2(x) étant l'ensemble des mots de longueur 14 obtenus en supprimant deux positions de x (120 choix de positions, descendants égaux regroupés). Pour deux mots de longueur 16, c'est équivalent à : aucune paire n'a de sous-séquence commune de longueur 14 (toute sous-séquence commune de longueur au moins 14 en contient une de longueur exactement 14, qui est un descendant des deux), c'est-à-dire plus longue sous-séquence commune (LCS) au plus 13 pour toute paire.
- Le fichier de réponse de l'API (sha256 8fece05a..., 16 964 octets), objet d'id 2605 (agent nightshift-dc16, score 219, createdAt 2026-10-05T00:13:01.889Z), contient exactement 219 chaînes de 16 caractères toutes dans {0,1}, toutes distinctes ; liste épinglée par son sha256 f8ac54a8b0910350a896e9524e6f74b753124d788b52ac0618ab6de34a13755b.
- Moteur A (énumération des descendants) : somme des tailles des 219 boules D2 = 6168 = nombre de descendants distincts utilisés (chaque seau de l'index inversé contient au plus un mot), donc boules deux à deux disjointes ; 0 paire en conflit ; 6168 <= 16384 = 2^14, la borne de comptage de l'énoncé. Tailles de boule de 3 à 94.
- Moteur B (LCS sur les 23 871 paires, sans énumération) : 0 paire avec LCS >= 14 ; LCS maximal exactement 13, atteint par 4 599 paires (la propriété est donc serrée sur ces paires, sans marge) ; répartition exacte des LCS dans artefacts/sortie_moteur_b.out. Aucun flottant, aucune tolérance, aucun tirage dans les deux moteurs.
- Les deux moteurs ont des algorithmes distincts et aucun import commun ; ils rendent les mêmes paires en conflit (ensemble vide ici) dans les 10 contrôles négatifs, y compris ceux à conflits multiples, et sur 40 codes aléatoires de 150 mots (16 805 paires en conflit au total, 0 désaccord).
- Le vérificateur public de la plateforme (champ verifier de l'API, 1 153 caractères, sha256 563cc3bc..., relu en entier avant d'être épinglé) a été exécuté tel quel sur les mêmes mots : accepté, score 219.0. C'est un recoupement par un outil (role outil), ni un tiers, ni un second moteur de ce rapport.

**Supposé par la revendication, non prouvé**
- Que l'API de la plateforme a servi la vraie soumission de l'agent nightshift-dc16 (id 2605) : le rejeu vérifie les mots reçus, pas leur provenance, et le dépôt GitHub new-SOTA n'a pas ce fichier (voir écarts).
- Que le dépôt de la plateforme n'a pas modifié le contenu de la solution d'id 2605 depuis le 2026-10-05 : seul le sha256 relevé le 2026-10-12 est épinglé (les deux relevés de 19:38Z et 19:40Z sont identiques, et la liste de mots est identique avec limit=4 et limit=10).

**Cité, non reconstruit ici**
- Que 219 dépasse le record public (215 de Weindel et Heckel v2, trouvé avec KaMIS, construction non publiée selon l'énoncé de la plateforme ; 208 pour le meilleur code reproductible, CPro1) : cité par l'énoncé de la plateforme, aucune recherche de littérature n'a été faite pour ce rapport. La plateforme marque elle-même l'énoncé et le vérificateur « Under active review ».
- L'attribution à l'agent nightshift-dc16 et la chronologie des soumissions (216 puis 218 mots par happy-gpt-astra-6 le 2026-10-03 ; 219 le 2026-10-05) : lues dans la réponse de l'API, non confirmées par une autre source.
- Aucune optimalité : le rejeu n'exclut pas 220 mots ou davantage ; la borne supérieure de programmation linéaire (487) citée par l'énoncé n'est pas en jeu.

## Exécution

- Environnement : Windows 11, Python 3.13.15 (bibliothèque standard seule) ; interpréteur lancé avec -I (mode isolé) ; réponse de l'API téléchargée dans un dossier séparé du code ; aucun réseau pendant le rejeu
- Commande : `python -I -X utf8 scripts/rejouer.py <dossier-téléchargement>/solutions_best_problem34_limit4.json <dossier-téléchargement>/problem_two-deletion-code-16.json <dossier-de-sortie>`
- Début : 2026-10-12T19:44:17Z ; durée murale 13.02 s ; code de sortie 0

## Résultat

- Valeur obtenue : `219` (entiers-exacts)
- Égalité exacte avec la valeur revendiquée : oui
- 219 mots binaires de longueur 16, deux à deux distincts ; 23 871 paires ; 0 paire en conflit (moteurs A et B).
- Moteur A : 6 168 descendants distincts = somme des tailles des boules ; occupation maximale d'un seau 1.
- Moteur B : LCS maximal 13 ; 4 599 paires à LCS 13 ; plus petit LCS observé 2 (1 paire).
- Vérificateur public de la plateforme : accepté, score 219.0.

## Contrôles

| Type | Réalisé | Attendu | Obtenu | Description |
|---|---|---|---|---|
| negatif | oui | echec | echec | Mot ajouté qui viole la propriété : 220e mot égal au mot 0 avec un bit inversé (N1, LCS 15, conflits avec les mots 0, 4 et 37) ; 220e mot à LCS exactement 14 avec le mot 10, obtenu par deux suppressions et deux insertions (N2 : 0000101100111111, 5 conflits) ; frontière {0^16, 0^14 11} (N10, LCS 14). Les deux moteurs rejettent avec exactement les mêmes paires en conflit. |
| negatif | oui | echec | echec | Doublon : 220e mot copie exacte du mot 7 (N3) ; mot 5 remplacé par le mot 6 avec un bit inversé, effectif inchangé 219 (N4, 6 conflits) : rejetés par les deux moteurs pour le motif attendu (doublon, puis descendant commun). |
| negatif | oui | echec | echec | Entrées hors format : mot de longueur 15 (N5), caractère 2 (N6), entier 101 à la place d'une chaîne (N7), 218 mots pour 219 revendiqués (N8), mot suivi d'une espace (N9) : rejetés par les deux moteurs. |
| controle-positif | oui | succes | succes | Le vérificateur peut accepter : fichier intact revendiqué 219 (P1), 218 premiers mots (P2), 100 premiers mots (P3), {0^16, 1^16} (P4), frontière {0^16, 0^13 111} à LCS exactement 13 (P5, LCS maximal observé par B = 13). Cohérences : suppression par bits (A) égale suppression par chaînes sur les 65 536 mots de 16 bits (C1, 0 désaccord) ; mêmes paires en conflit en A et B sur 40 codes aléatoires de 150 mots, graine 20261012 (C2, 0 désaccord ; test à graine fixe, pas une preuve d'équivalence). |
| second-moteur | oui | succes | succes | Moteur B (LCS par programmation dynamique sur chaque paire, sans énumérer les descendants, sans import de A) : même verdict VALIDE et même absence de conflit que le moteur A (énumération des descendants et index inversé). Écrit par le même opérateur : indépendance de code et d'algorithme, pas d'auteur. |
| lean | non | — | — | Pas de certification Lean ; la revendication n'en porte pas. |
| horodatage | non | — | — | L'empreinte de ce rapport est horodatée après son figement (rapport.json.ots et MANIFEST.sha256 du dossier reproductions/) ; ce contrôle ne peut pas figurer dans le rapport sans changer son empreinte : à vérifier par stamp.py verify. |

## Écarts

- Le mandat prévoyait une URL épinglée sur un commit du dépôt togethercomputer/EinsteinArena-new-SOTA : impossible, ce dépôt ne contient aucune solution de ce problème (16 dossiers à la tête de main c388c6f7, aucun chemin « deletion », branches kissing-number et add_heilbronn comprises). La source est l'API de la plateforme ; revendication.source.sha est donc le sha256 d'une réponse d'API, pas un commit git.
- L'URL de l'API n'est pas immuable : elle rend les meilleures solutions du moment. Le rejeu n'épingle pas la réponse entière mais la liste de mots de la solution 2605 (sha256 f8ac54a8...) ; si la plateforme retire cette solution de sa réponse ou la supprime, le rejeu public n'est plus possible faute de copie (les mots ne sont pas copiés ici, licence non établie).
- La date d'annonce de l'entrée est le 2026-10-03 (216 mots, happy-gpt-astra-6) ; le 219 de nightshift-dc16 date du 2026-10-05 : cohérent, sans effet sur la valeur.
- L'énoncé de la plateforme dit que 216 mots améliorerait le record publié au 2026-09-15 et que 209 à 215 améliorent la base reproductible (208) : le rejeu ne vérifie aucune de ces comparaisons.
- Les 3 autres solutions de la réponse (ids 2601, 2600, 2604 : 218, 216, 216 mots) n'ont pas été rejouées ; seule la solution d'id 2605 l'a été.
- Le test C2 (codes aléatoires) est à graine fixe : il appuie l'équivalence des deux moteurs mais ne la démontre pas ; l'équivalence LCS >= 14 et descendant commun est démontrée dans la portée (une sous-séquence commune de longueur >= 14 en contient une de longueur 14).

## Artefacts

| Fichier | Rôle | sha256 |
|---|---|---|
| `scripts/verif_a.py` | moteur A : entiers de 16 bits, 120 suppressions de deux positions par opérations sur les bits, index inversé 14 bits -> mots ; aucune LCS | `cd1d4459235cdf72…` |
| `scripts/verif_b.py` | moteur B : plus longue sous-séquence commune (programmation dynamique) sur chacune des 23 871 paires ; aucune énumération de descendants, aucun import de A | `55ff0dfe418c25b9…` |
| `scripts/verif_plateforme.py` | exécute tel quel le vérificateur public de la plateforme (texte épinglé par sha256) sur les mots ; outil, pas un second moteur | `6772bf43b257b01f…` |
| `scripts/controles.py` | contrôles négatifs N1-N10, positifs P1-P5, cohérences C1 (suppression bits = chaînes sur 65 536 mots) et C2 (codes aléatoires, mêmes paires en A et B) | `e49918002e75ae4f…` |
| `scripts/rejouer.py` | lanceur : vérifie le sha256 de la liste des mots, lance les quatre étapes en python -I, écrit les .out | `6da22f129ad46326…` |
| `scripts/empreintes.py` | sha256 et sha1 d'objet git d'un fichier (copie de celui de la fiche 604) | `bd3804108827edaa…` |
| `artefacts/source.txt` | source (API de la plateforme, pas de commit git), sha256 de la réponse, de la liste des mots et du vérificateur ; limites de licence | `9d8306dad8f6c8f9…` |
| `artefacts/sortie_moteur_a.out` | sortie du moteur A : VALIDE, 219 mots, 6168 descendants distincts, aucun conflit | `16841191bfa5c2f5…` |
| `artefacts/sortie_moteur_b.out` | sortie du moteur B : VALIDE, 23 871 paires, LCS maximal 13, répartition des LCS | `5ac95bf6ac0992b0…` |
| `artefacts/sortie_controles.out` | tableau des contrôles : 10 rejets attendus, 5 acceptations attendues, 2 cohérences, tous conformes | `90ebaf05c412864e…` |
| `artefacts/sortie_plateforme.out` | sortie du vérificateur public de la plateforme : ACCEPTÉ, score 219.0 | `96db4cf405a8cd1c…` |

## À décider par Antoine

- Changer ou non le statut public de ea-two-deletion-code-16 (actuellement non-evalue) : une reproduction privée ne le change pas par elle-même.
- Publier ou non ce verdict.
- Archiver ou non la réponse de l'API (archive externe, copie des 219 mots) pour que le rejeu survive à un retrait par la plateforme : action externe, à ne faire qu'avec l'accord d'Antoine ; la licence des mots n'est pas établie.
