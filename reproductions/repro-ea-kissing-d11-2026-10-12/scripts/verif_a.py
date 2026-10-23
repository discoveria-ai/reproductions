"""Moteur A : vérificateur exact du kissing number en dimension 11 (solution EinsteinArena n=604).

Arithmétique : entiers Python seuls, éléments de Z[sqrt 2] représentés par des couples (a, b) = a + b*sqrt 2.
Aucun flottant, aucune tolérance. Le signe de a + b*sqrt 2 est décidé par disjonction de cas sur les signes
de a et b, puis, si ceux-ci diffèrent, par comparaison des entiers a^2 et 2*b^2 (sqrt 2 irrationnel : égalité
impossible hors (0, 0)).

Usage : python -I -X utf8 verif_a.py <solution.json> [--n 604] [--norme2 36]
Code de sortie : 0 si la configuration est valide, 1 sinon, 2 si le fichier est mal formé.
"""

import argparse
import itertools
import json
import sys

DIM = 11


def _refuse(x):
    raise ValueError(f"constante JSON non entière refusée : {x}")


def charger(chemin):
    """Lit le JSON en refusant tout flottant (parse_float) et NaN/Infinity (parse_constant)."""
    with open(chemin, "rb") as f:
        brut = f.read()
    return json.loads(brut.decode("utf-8"), parse_float=_refuse, parse_constant=_refuse)


# ---- arithmétique de Z[sqrt 2] : (a, b) = a + b*sqrt 2 -------------------------------------------------

def mul(x, y):
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def signe(x):
    """-1, 0 ou +1 : signe exact de a + b*sqrt 2."""
    a, b = x
    if a == 0 and b == 0:
        return 0
    if a >= 0 and b >= 0:
        return 1
    if a <= 0 and b <= 0:
        return -1
    # signes strictement opposés : a et b*sqrt 2 se compensent ou non
    d = a * a - 2 * b * b  # jamais nul ici (sqrt 2 irrationnel)
    assert d != 0
    if a > 0:  # b < 0 : a + b sqrt2 > 0  <=>  a^2 > 2 b^2
        return 1 if d > 0 else -1
    return -1 if d > 0 else 1  # a < 0, b > 0 : a + b sqrt2 > 0  <=>  2 b^2 > a^2


def cmp(x, y):
    return signe(sub(x, y))


# ---- forme du fichier ---------------------------------------------------------------------------------

def forme(data, n_attendu):
    """Liste des vecteurs sous forme de n-uplets de 11 couples, ou lève ValueError."""
    if not isinstance(data, dict):
        raise ValueError("racine JSON non objet")
    if data.get("n") != n_attendu or data.get("dim") != DIM:
        raise ValueError(f"en-tête n/dim inattendu : {data.get('n')!r}/{data.get('dim')!r}")
    vecs = data.get("vectors")
    if not isinstance(vecs, list) or len(vecs) != n_attendu:
        raise ValueError(f"nombre de vecteurs {len(vecs) if isinstance(vecs, list) else '?'} != {n_attendu}")
    out = []
    for i, v in enumerate(vecs):
        if not isinstance(v, list) or len(v) != 2 * DIM:
            raise ValueError(f"vecteur {i} : longueur {len(v) if isinstance(v, list) else '?'} != {2 * DIM}")
        for x in v:
            if type(x) is not int:  # exclut bool, float, str
                raise ValueError(f"vecteur {i} : entrée non entière {x!r}")
        out.append(tuple((v[2 * k], v[2 * k + 1]) for k in range(DIM)))
    return out


def norme2(v):
    s = (0, 0)
    for c in v:
        s = add(s, mul(c, c))
    return s


def verifier(data, n_attendu=604, norme2_attendue=(36, 0)):
    """Retourne un dict de résultats. valide = True seulement si tous les contrôles passent."""
    res = {"moteur": "A", "valide": False, "raisons": []}
    try:
        vecs = forme(data, n_attendu)
    except ValueError as e:
        res["raisons"].append(f"forme : {e}")
        return res
    res["n"] = len(vecs)
    if len(set(vecs)) != len(vecs):
        res["raisons"].append(f"vecteurs non distincts : {len(vecs) - len(set(vecs))} doublon(s)")
    normes = [norme2(v) for v in vecs]
    distinctes = sorted(set(normes))
    res["normes2_distinctes"] = distinctes
    if len(distinctes) != 1:
        res["raisons"].append(f"normes différentes : {len(distinctes)} valeurs")
    if any(nm != norme2_attendue for nm in normes):
        res["raisons"].append(f"norme^2 différente de {norme2_attendue}")
    N = norme2_attendue
    mini = None
    egalites = 0
    violations = []
    for i, j in itertools.combinations(range(len(vecs)), 2):
        d = (0, 0)
        for p, q in zip(vecs[i], vecs[j]):
            e = sub(p, q)
            d = add(d, mul(e, e))
        s = cmp(d, N)
        if s < 0:
            violations.append((i, j, d))
        elif s == 0:
            egalites += 1
        if mini is None or cmp(d, mini) < 0:
            mini = d
    res["distance2_min"] = mini
    res["paires_totales"] = len(vecs) * (len(vecs) - 1) // 2
    res["paires_a_egalite"] = egalites
    res["violations"] = len(violations)
    if violations:
        i, j, d = violations[0]
        res["premiere_violation"] = (i, j, d)
        res["raisons"].append(f"{len(violations)} paire(s) à distance^2 < {N}")
    res["valide"] = not res["raisons"]
    return res


def fmt(x):
    a, b = x
    return f"{a} + {b}*sqrt(2)"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier")
    ap.add_argument("--n", type=int, default=604)
    ap.add_argument("--norme2", type=int, default=36)
    a = ap.parse_args(argv)
    try:
        data = charger(a.fichier)
    except (ValueError, OSError) as e:
        print(f"MOTEUR A : FICHIER MAL FORMÉ : {e}")
        return 2
    r = verifier(data, a.n, (a.norme2, 0))
    print(f"MOTEUR A : n = {r.get('n')}, dim = {DIM}, norme^2 attendue = {a.norme2}")
    if "normes2_distinctes" in r:
        print("  normes^2 distinctes :", [fmt(x) for x in r["normes2_distinctes"]])
        print(f"  paires : {r['paires_totales']} ; distance^2 minimale exacte = {fmt(r['distance2_min'])} ;"
              f" paires à égalité avec la norme^2 : {r['paires_a_egalite']} ; violations : {r['violations']}")
    for m in r["raisons"]:
        print("  REJET :", m)
    print("  VERDICT :", "VALIDE" if r["valide"] else "REJETÉ")
    return 0 if r["valide"] else (2 if r["raisons"] and r["raisons"][0].startswith("forme") else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
