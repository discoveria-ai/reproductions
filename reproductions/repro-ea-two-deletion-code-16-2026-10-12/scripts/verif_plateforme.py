"""Rejoue le vérificateur PUBLIC de la plateforme (champ `verifier` de l'API) sur les mots de la solution.

Ce n'est pas un des deux moteurs : c'est le code de la plateforme, relu et exécuté tel quel pour comparer son verdict
au nôtre. Il est refusé si son texte n'a pas le sha256 épinglé (relu le 2026-10-12). Il tourne en mode isolé (python -I),
sans réseau, avec la seule entrée `{"words": [...]}`.

Usage : python -I -X utf8 verif_plateforme.py <problem.json de l'API> <reponse_api.json> [--id 2605]
Code de sortie : 0 accepté (score rendu), 1 rejeté par le vérificateur, 2 fichier mal formé, 3 vérificateur modifié.
"""

import hashlib
import json
import sys

SHA256_VERIFICATEUR = "563cc3bc7d39bdc261dd6cff08eb634c03e149d59df8f0c7ceff5b3f68730325"


def main(argv):
    probleme, solutions = argv[0], argv[1]
    ident = int(argv[argv.index("--id") + 1]) if "--id" in argv else 2605
    texte = json.load(open(probleme, "rb"))["verifier"]
    h = hashlib.sha256(texte.encode("utf-8")).hexdigest()
    if h != SHA256_VERIFICATEUR:
        print(f"REFUS : sha256 du vérificateur {h} différent de l'empreinte épinglée {SHA256_VERIFICATEUR}")
        return 3
    cible = [s for s in json.load(open(solutions, "rb")) if s.get("id") == ident]
    if len(cible) != 1:
        print(f"fichier mal formé : {len(cible)} solution(s) d'id {ident}")
        return 2
    espace = {}
    exec(compile(texte, "verifier_plateforme", "exec"), espace)
    print(f"VÉRIFICATEUR PLATEFORME (sha256 {h}, {len(texte)} caractères), solution {ident}")
    try:
        score = espace["evaluate"]({"words": cible[0]["data"]["words"]})
    except ValueError as e:
        print(f"  REJETÉ : {e}")
        return 1
    print(f"  ACCEPTÉ : score {score}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
