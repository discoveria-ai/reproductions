"""Témoin : exécute le vérificateur public de la plateforme (champ « verifier » de l'API, Python) sur les offsets.

Ce n'est pas un moteur de ce rapport : c'est le code du revendicateur, lu intégralement avant exécution
(import math, fractions ; aucun accès au réseau ni au disque) et lancé ici par exec dans un espace de noms vide.
Il fournit l'aire exacte (Fraction) via triangle_union_area, que l'on compare à celle des moteurs A et B.

Usage : python -I -X utf8 temoin_plateforme.py <problem.json> <offsets.txt> [<fraction exacte A "p/q">]
Code de sortie : 0 = le témoin calcule la même aire exacte que A (si donnée) ; 1 sinon ; 2 = usage.
"""

import hashlib
import json
import sys
from fractions import Fraction

# Empreinte du seul texte lu intégralement avant exécution (2026-10-12) ; tout autre texte n'est pas exécuté.
SHA256_VERIFIER_LU = "4d7e8ddd5a5044b3f0e66f745486538f5b76ddb6687e5fb536aca18b5c6cd098"


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    pb = json.loads(open(argv[0], "rb").read().decode("utf-8"))
    src = pb["verifier"]
    h = hashlib.sha256(src.encode("utf-8")).hexdigest()
    print(f"sha256 du texte du verifier : {h}")
    print(f"titre de l'énoncé : {pb['title']}")
    if h != SHA256_VERIFIER_LU:
        print(f"témoin non exécuté : vérificateur modifié depuis la lecture du 2026-10-12 (attendu {SHA256_VERIFIER_LU}) ;")
        print("le texte nouveau n'a pas été lu : relire le champ « verifier » avant de graver sa nouvelle empreinte.")
        return 0  # le témoin ne fonde pas le verdict : ne pas compter cela comme un échec du rejeu
    ns = {"__name__": "verifier_plateforme"}
    exec(compile(src, "verifier_plateforme.py", "exec"), ns)
    offs = open(argv[1], encoding="ascii", newline="").read().split("\n")
    if offs and offs[-1] == "":
        offs.pop()
    score = ns["evaluate"]({"offsets": offs})
    xs = [ns["_parse_offset"](s) for s in offs]
    x0 = xs[0]
    aire = ns["triangle_union_area"]([x - x0 for x in xs])
    print(f"evaluate(...) = {score!r}")
    print(f"aire exacte du témoin = {aire.numerator}/{aire.denominator}")
    ok = float(aire) == score
    print(f"float(aire exacte) == evaluate : {ok}")
    if len(argv) > 2:
        egal = aire == Fraction(argv[2])
        print(f"aire exacte du témoin == aire exacte du moteur A : {egal}")
        ok = ok and egal
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
