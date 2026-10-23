"""Moteur B : second vérificateur, indépendant du moteur A (aucun import commun, autre critère, autre signe).

Différences avec A :
  - critère : matrice de Gram. Chaque vecteur x = P + Q*sqrt 2 (P, Q vecteurs entiers de Z^11) ;
    <x,y> = (P.P' + 2 Q.Q') + (P.Q' + Q.P') sqrt 2, calculé par produits matriciels numpy en int64
    (garde de dépassement vérifiée). Pour deux vecteurs de norme^2 N, ||x-y||^2 >= N <=> <x,y> <= N/2 ;
    B calcule d'abord la diagonale de Gram et exige qu'elle vaille (36, 0) partout, puis teste <x,y> <= 18.
  - signe de a + b sqrt 2 : par la norme du corps N = a^2 - 2 b^2 et le conjugué : N > 0 => signe(a),
    N < 0 => signe(b), N = 0 => (a, b) = (0, 0).
  - lecture : le texte brut après "vectors" ne doit contenir que chiffres, signes, crochets, virgules et blancs
    (donc ni point décimal ni exposant).
  - recontrôle sympy : chaque valeur distincte de <x,y> est retestée par sympy (arithmétique algébrique exacte).

Usage : python -I -X utf8 verif_b.py <solution.json> [--n 604] [--norme2 36] [--sans-sympy]
Code de sortie : 0 valide, 1 rejeté, 2 fichier mal formé.
"""

import argparse
import json
import re
import sys

import numpy as np

DIM = 11
PLAFOND = 1 << 20  # |coordonnée| max pour garantir l'absence de dépassement int64 dans les produits


def signe_conj(a, b):
    """Signe exact de a + b*sqrt 2 via la norme N = a^2 - 2 b^2 (a, b entiers Python)."""
    if a == 0 and b == 0:
        return 0
    n = a * a - 2 * b * b
    if n > 0:  # x et son conjugué ont même signe, a = (x + conj x)/2
        return 1 if a > 0 else -1
    return 1 if b > 0 else -1  # n < 0 (n = 0 impossible hors (0,0)) : x > conj x <=> b > 0


def charger(chemin):
    brut = open(chemin, "rb").read().decode("utf-8")
    i = brut.index('"vectors"')
    corps = brut[i + len('"vectors"'):]
    if not re.fullmatch(r"[\s:\[\],0-9\-}]*", corps):
        raise ValueError("le tableau des vecteurs contient autre chose que des entiers décimaux")
    return json.loads(brut)


def verifier(data, n_attendu=604, norme2=36, avec_sympy=True):
    res = {"moteur": "B", "valide": False, "raisons": []}
    try:
        if data.get("n") != n_attendu or data.get("dim") != DIM:
            raise ValueError("en-tête n/dim")
        vecs = data["vectors"]
        if len(vecs) != n_attendu or any(len(v) != 2 * DIM for v in vecs):
            raise ValueError("dimensions du tableau")
        if any(isinstance(x, bool) or not isinstance(x, int) for v in vecs for x in v):
            raise ValueError("entrée non entière")
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        res["raisons"].append(f"forme : {e}")
        return res
    M = np.array(vecs, dtype=np.int64)
    if np.abs(M).max() >= PLAFOND:
        res["raisons"].append("forme : coordonnée trop grande pour la garde int64")
        return res
    n = M.shape[0]
    res["n"] = n
    P, Q = M[:, 0::2], M[:, 1::2]  # P : parties rationnelles, Q : parties en sqrt 2
    GA = P @ P.T + 2 * (Q @ Q.T)
    GB = P @ Q.T + Q @ P.T
    # distinctes
    if len({tuple(r) for r in M.tolist()}) != n:
        res["raisons"].append("vecteurs non distincts")
    diag = {(int(GA[i, i]), int(GB[i, i])) for i in range(n)}
    res["normes2_distinctes"] = sorted(diag)
    if diag != {(norme2, 0)}:
        res["raisons"].append(f"diagonale de Gram différente de ({norme2}, 0) : {sorted(diag)[:5]}")
    # seuil : <x,y> <= norme2/2, soit (norme2/2 - A) + (-B) sqrt 2 >= 0 ; norme2 pair requis pour rester entier
    if norme2 % 2:
        res["raisons"].append("norme2 impair non géré par le critère <x,y> <= N/2")
        return res
    h = norme2 // 2
    iu = np.triu_indices(n, k=1)
    A = GA[iu].tolist()
    B = GB[iu].tolist()
    valeurs = {}
    for a, b in zip(A, B):
        valeurs[(a, b)] = valeurs.get((a, b), 0) + 1
    res["paires_totales"] = len(A)
    res["valeurs_distinctes_gram"] = len(valeurs)
    egalites = violations = 0
    for (a, b), c in valeurs.items():
        s = signe_conj(h - a, -b)  # signe de h - <x,y>
        if s == 0 or (a, b) == (h, 0):
            egalites += c
        if s < 0:
            violations += c
    res["paires_a_egalite"] = egalites
    res["violations"] = violations
    # produit scalaire maximal exact (donc distance^2 minimale = 2*norme2 - 2*max)
    tete = None
    for (a, b) in valeurs:
        if tete is None or signe_conj(a - tete[0], b - tete[1]) > 0:
            tete = (a, b)
    res["gram_max"] = tete
    res["distance2_min"] = (2 * norme2 - 2 * tete[0], -2 * tete[1])
    if violations:
        res["raisons"].append(f"{violations} paire(s) avec <x,y> > {h}")
    if avec_sympy:
        import sympy
        r2 = sympy.sqrt(2)
        faux = [ab for ab in valeurs if not (h - ab[0] - ab[1] * r2 >= 0)]
        res["sympy_valeurs_testees"] = len(valeurs)
        res["sympy_valeurs_violees"] = len(faux)
        if bool(faux) != bool(violations):
            res["raisons"].append("sympy et le signe par norme du corps divergent")
    res["valide"] = not res["raisons"]
    return res


def fmt(x):
    return f"{x[0]} + {x[1]}*sqrt(2)"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier")
    ap.add_argument("--n", type=int, default=604)
    ap.add_argument("--norme2", type=int, default=36)
    ap.add_argument("--sans-sympy", action="store_true")
    a = ap.parse_args(argv)
    try:
        data = charger(a.fichier)
    except (ValueError, OSError) as e:
        print(f"MOTEUR B : FICHIER MAL FORMÉ : {e}")
        return 2
    r = verifier(data, a.n, a.norme2, not a.sans_sympy)
    print(f"MOTEUR B : n = {r.get('n')}, dim = {DIM}, norme^2 attendue = {a.norme2}")
    if "normes2_distinctes" in r:
        print("  diagonale de Gram (normes^2 distinctes) :", [fmt(x) for x in r["normes2_distinctes"]])
    if "distance2_min" in r:
        print(f"  paires : {r['paires_totales']} ; valeurs distinctes de <x,y> : {r['valeurs_distinctes_gram']} ;"
              f" <x,y> max = {fmt(r['gram_max'])} ; distance^2 minimale exacte = {fmt(r['distance2_min'])} ;"
              f" paires à égalité : {r['paires_a_egalite']} ; violations : {r['violations']}")
    if "sympy_valeurs_testees" in r:
        print(f"  sympy : {r['sympy_valeurs_testees']} valeurs testées, {r['sympy_valeurs_violees']} violée(s)")
    for m in r["raisons"]:
        print("  REJET :", m)
    print("  VERDICT :", "VALIDE" if r["valide"] else "REJETÉ")
    return 0 if r["valide"] else (2 if r["raisons"] and r["raisons"][0].startswith("forme") else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
