"""Moteur B : aire exacte de l'union des triangles de Kakeya, balayage en abscisse x, depuis les sommets.

Indépendant du moteur A (aucun import de lui) : il ne reprend pas les formules de section de l'énoncé.
Les triangles sont construits par leurs trois sommets (x_j, 0), (x_j + 1/n, 0), (x_j + j/n, 1). Le plan est
découpé en bandes verticales délimitées par les abscisses des sommets et des intersections d'arêtes obliques.
Dans une bande, la droite verticale x = m coupe chaque triangle en un segment dont les extrémités sont des
fonctions affines de x ; la longueur verticale de l'union est donc affine dans la bande et
largeur x longueur(milieu) est exact. Entiers de Python (grands) et Fraction seulement pour les cumuls.

Usage : python -I -X utf8 verif_b.py <offsets.txt> [<valeur revendiquée décimale>]
Code de sortie : 0 = format valide ET aire égale à la valeur revendiquée (arrondie au double), 1 sinon, 2 = usage.
"""

import re
import sys
from fractions import Fraction
from math import gcd

N_ATTENDU = 128


def lire(chaines, n_attendu=N_ATTENDU):
    """(liste de Fraction, erreurs). Règle de l'énoncé : chaînes décimales, <= 25 décimales, <= 4 chiffres entiers."""
    if not isinstance(chaines, list) or len(chaines) != n_attendu:
        return [], ["forme : nombre d'offsets"]
    err, xs = [], []
    for i, s in enumerate(chaines):
        if not isinstance(s, str):
            err.append(f"forme : offset {i} non chaîne")
            continue
        m = re.fullmatch(r"(-?)([0-9]+)(?:\.([0-9]*))?", s, flags=re.ASCII)
        if m is None:
            err.append(f"forme : offset {i} non décimal : {s!r}")
            continue
        signe, ent, dec = m.group(1), m.group(2), m.group(3) or ""
        if len(dec) > 25 or len(ent) > 4:
            err.append(f"forme : offset {i} hors limites ({len(ent)} chiffres entiers, {len(dec)} décimales)")
            continue
        v = Fraction(int(ent + dec), 10 ** len(dec))
        xs.append(-v if signe else v)
    return (xs if not err else []), err


def aire_par_abscisse(xs):
    n = len(xs)
    den = 1
    for x in xs:
        den = den // gcd(den, x.denominator) * x.denominator
    # abscisses multipliées par n*den : entières ; ordonnées 0 ou 1 (non mises à l'échelle)
    tri = []
    for j, x in enumerate(xs, start=1):
        ax = n * int(x * den)
        tri.append(((ax, 0), (ax + den, 0), (ax + j * den, 1)))
    # arêtes obliques (de y = 0 à y = 1) : x(y) = px + s*y
    obliques = []
    for A, B, C in tri:
        obliques.append((A[0], C[0] - A[0]))
        obliques.append((B[0], C[0] - B[0]))
    cass = set()
    for A, B, C in tri:
        for s in (A[0], B[0], C[0]):
            cass.add((s, 1))
    m = len(obliques)
    for a in range(m):
        pa, sa = obliques[a]
        for b in range(a + 1, m):
            pb, sb = obliques[b]
            if sa == sb:
                continue
            p, q = pb - pa, sa - sb            # y = p/q
            if q < 0:
                p, q = -p, -q
            if 0 <= p <= q:
                # x = pa + sa*p/q = (pa*q + sa*p)/q
                nu, de = pa * q + sa * p, q
                g = gcd(nu, de)
                cass.add((nu // g, de // g))
    abscisses = sorted(cass, key=lambda t: Fraction(t[0], t[1]))
    # facteur commun pour que les y soient entiers : M multiple de toutes les largeurs d'arête, den * ppcm(1..n)
    ppcm = 1
    for k in range(2, n + 1):
        ppcm = ppcm // gcd(ppcm, k) * k
    M = den * ppcm
    aretes = []  # par triangle : (xmin, xmax, [(Px, Py, Qx, Qy, dx) avec Px < Qx])
    for A, B, C in tri:
        es = []
        for P, Q in ((A, B), (A, C), (B, C)):
            if P[0] == Q[0]:
                continue
            if P[0] > Q[0]:
                P, Q = Q, P
            if M % (Q[0] - P[0]) != 0:
                raise ValueError("facteur commun M insuffisant : division non exacte")
            es.append((P[0], P[1], Q[0], Q[1], Q[0] - P[0]))
        aretes.append((min(A[0], B[0], C[0]), max(A[0], B[0], C[0]), es))
    aire = Fraction(0)
    echelle = n * den
    for (nl, dl), (nr, dr) in zip(abscisses, abscisses[1:]):
        xl, xr = Fraction(nl, dl), Fraction(nr, dr)
        mid = (xl + xr) / 2
        mp, mq = mid.numerator, mid.denominator
        iv = []
        for xmin, xmax, es in aretes:
            if not (xmin * mq < mp < xmax * mq):
                continue
            ys = []
            for Px, Py, Qx, Qy, dx in es:
                if Px * mq < mp < Qx * mq:
                    # y * (mq * M) = Py*mq*M + (Qy-Py)*(mp - Px*mq)*(M // dx)
                    ys.append(Py * mq * M + (Qy - Py) * (mp - Px * mq) * (M // dx))
            iv.append((min(ys), max(ys)))
        if not iv:
            continue
        iv.sort()
        tot = 0
        g0, d0 = iv[0]
        for g1, d1 in iv[1:]:
            if g1 > d0:
                tot += d0 - g0
                g0, d0 = g1, d1
            elif d1 > d0:
                d0 = d1
        tot += d0 - g0
        aire += (xr - xl) / echelle * Fraction(tot, mq * M)
    return aire, len(abscisses)


def decimal_tronque(f, chiffres):
    ent = f.numerator * 10 ** chiffres // f.denominator
    s = str(ent).rjust(chiffres + 1, "0")
    return s[:-chiffres] + "." + s[-chiffres:]


def evaluer(chaines, revendique=None, n_attendu=N_ATTENDU):
    xs, err = lire(chaines, n_attendu)
    if err:
        return "REJETÉ", None, err
    aire, nb = aire_par_abscisse(xs)
    msgs = [f"aire exacte = {decimal_tronque(aire, 40)}... (tronquée à 40 décimales ; fraction {aire.numerator}/{aire.denominator})",
            f"abscisses de rupture (sommets + croisements distincts) : {nb}"]
    if revendique is not None:
        d = float(aire)
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
    verdict, aire, msgs = evaluer(chaines, argv[1] if len(argv) > 1 else None)
    print(f"MOTEUR B : {verdict}")
    for m in msgs:
        print("  " + m)
    return 0 if verdict == "VALIDE" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
