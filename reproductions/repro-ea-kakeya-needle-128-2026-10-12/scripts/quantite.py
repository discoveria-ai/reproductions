"""Quantité exacte et comparaisons exactes : aire de l'union pour la solution 2608, face aux valeurs citées.

Usage : python -I -X utf8 quantite.py <offsets.txt> <dossier-des-moteurs>
Utilise le moteur A pour l'aire ; seules des comparaisons de rationnels exacts sont faites ici. Les seuls flottants
sont ceux de la revendication elle-même (un double), convertis ensuite en rationnels dyadiques exacts.
"""

import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

REVENDIQUE = "0.10675394011230244"
CITES = [
    ("état de l'art cité par l'énoncé (Station, août 2026)", "0.107067"),
    ("graine du classement (score de la Station sous ce vérificateur)", "0.10706663656163481"),
    ("AlphaEvolve cité par arXiv 2608.23691 §6.4", "0.114810"),
    ("HorizonMath cité par arXiv 2608.23691 §6.4", "0.109148"),
]


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    spec = importlib.util.spec_from_file_location("verif_a", Path(argv[1]) / "verif_a.py")
    A = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(A)
    lignes = Path(argv[0]).read_text(encoding="ascii").split("\n")[:-1]
    xs, err = A.lire_offsets(lignes)
    assert not err, err
    aire, _ = A.aire_exacte(xs)
    print(f"aire exacte = {aire.numerator}/{aire.denominator}")
    print(f"dénominateur : {len(str(aire.denominator))} chiffres ; aire = {A.decimal_tronque(aire, 45)}... (tronquée à 45 décimales)")
    d = float(aire)
    dd = Fraction(d)
    demi = Fraction(math.ulp(d)) / 2
    print(f"double le plus proche de l'aire exacte : {d!r} = {dd.numerator}/{dd.denominator}")
    print(f"demi-ulp (exact) : {demi.numerator}/{demi.denominator} ; |aire - double| = {float(abs(aire - dd)):.3e}")
    print(f"aire dans [double - demi-ulp, double + demi-ulp] : {dd - demi <= aire <= dd + demi}")
    print(f"double de la valeur revendiquée '{REVENDIQUE}' : {float(REVENDIQUE) == d}")
    decl = Fraction(REVENDIQUE)
    print(f"aire exacte - décimal revendiqué {REVENDIQUE} = {float(aire - decl):.3e} (négatif : l'aire exacte est plus petite)")
    print(f"aire exacte < décimal revendiqué : {aire < decl}")
    print(f"invariance par translation (offsets + 1/3 sur tous, exact) : ", end="")
    # décalage non décimal : on le fait sur les Fraction, sans passer par les chaînes
    aire2, _ = A.aire_exacte([x + Fraction(1, 3) for x in xs])
    print(aire2 == aire)
    for nom, s in CITES:
        v = Fraction(s)
        print(f"aire exacte < {s} ({nom}) : {aire < v} ; écart {float(v - aire):+.3e} ; gain relatif {float((v - aire) / v) * 100:.3f} %")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
