"""Témoin flottant, NON certifiant : aire de l'union par la bibliothèque GEOS (shapely, float64).

Sert seulement de garde-fou grossier contre une erreur de définition (par exemple triangle mal orienté) : la
tolérance est de 1e-9. Il ne participe pas au verdict ; sans shapely il écrit ABSENT et sort avec le code 0.

Usage : python -I -X utf8 temoin_flottant.py <offsets.txt>
Code de sortie : 0 = accord à 1e-9 (ou shapely absent) ; 1 = écart.
"""

import sys
from fractions import Fraction


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    try:
        import shapely
        from shapely.geometry import Polygon
        from shapely.ops import unary_union
    except ImportError:
        print("shapely ABSENT : témoin non exécuté")
        return 0
    lignes = open(argv[0], encoding="ascii", newline="").read().split("\n")[:-1]
    n = len(lignes)
    polys = []
    for j, s in enumerate(lignes, start=1):
        x = float(Fraction(s))
        polys.append(Polygon([(x, 0.0), (x + 1.0 / n, 0.0), (x + j / n, 1.0)]))
    aire = unary_union(polys).area
    print(f"shapely {shapely.__version__} : aire flottante de l'union = {aire!r}")
    ref = 0.10675394011230244
    print(f"écart avec la valeur revendiquée = {aire - ref:+.3e} (tolérance 1e-9, flottants : indicatif seulement)")
    return 0 if abs(aire - ref) < 1e-9 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
