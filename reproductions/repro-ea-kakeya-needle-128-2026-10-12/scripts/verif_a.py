"""Moteur A : aire exacte de l'union des triangles de Kakeya, balayage en hauteur y, entiers Python.

Objet (énoncé de la plateforme, api/problems/kakeya-needle-128) : pour j = 1..n et un décalage x_j,
T_j = enveloppe convexe de (x_j, 0), (x_j + 1/n, 0), (x_j + j/n, 1) ; quantité = aire de la réunion des T_j.
A la hauteur y la section de T_j est [x_j + (j/n) y, x_j + 1/n + ((j-1)/n) y] : deux droites affines en y.
La longueur de l'union est affine entre deux hauteurs où deux droites se croisent ; l'aire est la somme des
trapèzes. Tout est en rationnels exacts : les offsets sont lus par Fraction(chaîne), jamais par un flottant.

Usage : python -I -X utf8 verif_a.py <offsets.txt> [<valeur revendiquée décimale>]
        (offsets.txt : une chaîne décimale par ligne ; donnée non fiable, lue comme du texte)
Code de sortie : 0 = format valide ET aire égale à la valeur revendiquée (arrondie au double), 1 sinon, 2 = usage.
"""

import re
import sys
from fractions import Fraction
from math import gcd

N_ATTENDU = 128
MAX_DEC = 25
MAX_ENT = 4
MOTIF = re.compile(r"-?[0-9]+(\.[0-9]*)?")


def lire_offsets(chaines, n_attendu=N_ATTENDU):
    """Retourne (liste de Fraction, liste d'erreurs de forme). Format strict : chaîne décimale base 10."""
    erreurs = []
    if not isinstance(chaines, list) or len(chaines) != n_attendu:
        return [], [f"forme : {n_attendu} chaînes attendues, reçu {len(chaines) if isinstance(chaines, list) else type(chaines).__name__}"]
    xs = []
    for i, s in enumerate(chaines):
        if not isinstance(s, str):
            erreurs.append(f"forme : offset {i} n'est pas une chaîne ({type(s).__name__})")
            continue
        if not MOTIF.fullmatch(s) or not s.isascii():
            erreurs.append(f"forme : offset {i} n'est pas une chaîne décimale base 10 : {s!r}")
            continue
        t = s[1:] if s.startswith("-") else s
        ent, _, dec = t.partition(".")
        if len(dec) > MAX_DEC:
            erreurs.append(f"forme : offset {i} a {len(dec)} décimales (> {MAX_DEC})")
            continue
        if len(ent) > MAX_ENT:
            erreurs.append(f"forme : offset {i} a {len(ent)} chiffres entiers (> {MAX_ENT})")
            continue
        xs.append(Fraction(s))
    return (xs if not erreurs else []), erreurs


def aire_exacte(xs):
    """Aire exacte (Fraction) de la réunion des triangles T_j(x_j), j = 1..n = len(xs)."""
    n = len(xs)
    x0 = xs[0]
    xs = [x - x0 for x in xs]  # invariance par translation, comme la plateforme
    den = 1
    for x in xs:
        den = den // gcd(den, x.denominator) * x.denominator
    X = [int(x * den) for x in xs]
    # coordonnées multipliées par n*den : droite = (pente, ordonnée) entières
    gauche = [(den * j, n * X[j - 1]) for j in range(1, n + 1)]
    droite = [(den * (j - 1), n * X[j - 1] + den) for j in range(1, n + 1)]
    droites = gauche + droite
    # hauteurs de croisement dans ]0,1[ : y = (c_b - c_a) / (s_a - s_b)
    pts = set()
    m = len(droites)
    for a in range(m):
        sa, ca = droites[a]
        for b in range(a + 1, m):
            sb, cb = droites[b]
            ds = sa - sb
            if ds == 0:
                continue
            p = cb - ca
            if ds < 0:
                p, ds = -p, -ds
            if 0 < p < ds:
                g = gcd(p, ds)
                pts.add((p // g, ds // g))
    hauteurs = [(0, 1)] + sorted(pts, key=lambda t: Fraction(t[0], t[1])) + [(1, 1)]

    def longueur(p, q):
        """Longueur de l'union à la hauteur p/q, numérateur entier sur q * n * den."""
        iv = sorted((gauche[k][0] * p + gauche[k][1] * q, droite[k][0] * p + droite[k][1] * q) for k in range(n))
        tot = 0
        g0, d0 = iv[0]
        for g1, d1 in iv[1:]:
            if g1 > d0:
                tot += d0 - g0
                g0, d0 = g1, d1
            elif d1 > d0:
                d0 = d1
        return tot + d0 - g0

    echelle = n * den
    aire = Fraction(0)
    y_prec, u_prec = Fraction(0), Fraction(longueur(0, 1), echelle)
    for p, q in hauteurs[1:]:
        y = Fraction(p, q)
        u = Fraction(longueur(p, q), q * echelle)
        aire += (u_prec + u) * (y - y_prec) / 2
        y_prec, u_prec = y, u
    return aire, len(hauteurs)


def decimal_tronque(f, chiffres):
    """Écriture décimale de f >= 0 tronquée à `chiffres` décimales, en entiers."""
    ent = f.numerator * 10 ** chiffres // f.denominator
    s = str(ent).rjust(chiffres + 1, "0")
    return s[:-chiffres] + "." + s[-chiffres:]


def evaluer(chaines, revendique=None, n_attendu=N_ATTENDU):
    """Retourne (verdict, aire ou None, messages)."""
    xs, erreurs = lire_offsets(chaines, n_attendu)
    if erreurs:
        return "REJETÉ", None, erreurs
    aire, nb = aire_exacte(xs)
    msgs = [f"aire exacte = {decimal_tronque(aire, 40)}... (tronquée à 40 décimales ; fraction {aire.numerator}/{aire.denominator})",
            f"hauteurs de rupture (croisements distincts + extrémités) : {nb}"]
    if revendique is not None:
        d = float(aire)  # arrondi correct de CPython (division entière exacte)
        ok = d == float(revendique)
        msgs.append(f"float(aire exacte) = {d!r} ; valeur revendiquée = {float(revendique)!r} ; égalité : {ok}")
        if not ok:
            return "REJETÉ", aire, msgs + ["l'aire exacte arrondie au double diffère de la valeur revendiquée"]
    return "VALIDE", aire, msgs


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    chaines = open(argv[0], encoding="ascii", newline="").read().split("\n")
    if chaines and chaines[-1] == "":
        chaines.pop()
    revendique = argv[1] if len(argv) > 1 else None
    verdict, aire, msgs = evaluer(chaines, revendique)
    print(f"MOTEUR A : {verdict}")
    for m in msgs:
        print("  " + m)
    return 0 if verdict == "VALIDE" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
