"""Description exacte de la configuration : ce que le fichier contient réellement (entiers seuls).

Usage : python -I -X utf8 statistiques.py <solution.json>
"""
import collections
import itertools
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
V = d["vectors"]
print("clés du fichier :", sorted(d.keys()))
print("n =", d["n"], "dim =", d["dim"], "; description du fichier :", d["description"])
print("vecteurs :", len(V), "; entrées par vecteur :", sorted({len(v) for v in V}))
P = [v[0::2] for v in V]
Q = [v[1::2] for v in V]
avec_q = sum(1 for q in Q if any(q))
print("vecteurs avec au moins une partie en sqrt(2) non nulle :", avec_q)
print("valeurs distinctes des parties p :", sorted({x for p in P for x in p}))
print("valeurs distinctes des parties q :", sorted({x for q in Q for x in q}))
print("plus grande entrée en valeur absolue :", max(abs(x) for v in V for x in v))
H = collections.Counter()
for i, j in itertools.combinations(range(len(V)), 2):
    a = b = 0
    for k in range(11):
        pa, qa = P[i][k] - P[j][k], Q[i][k] - Q[j][k]
        a += pa * pa + 2 * qa * qa
        b += 2 * pa * qa
    H[(a, b)] += 1
print("valeurs distinctes de distance^2 (a + b sqrt2) et nombre de paires :")
for (a, b), c in sorted(H.items(), key=lambda t: t[0][0] + t[0][1] * 2 ** 0.5):  # tri d'affichage seulement
    print(f"  {a} + {b}*sqrt(2) : {c}")
voisins = collections.Counter()
for (i, j) in itertools.combinations(range(len(V)), 2):
    a = b = 0
    for k in range(11):
        pa, qa = P[i][k] - P[j][k], Q[i][k] - Q[j][k]
        a += pa * pa + 2 * qa * qa
        b += 2 * pa * qa
    if (a, b) == (36, 0):
        voisins[i] += 1
        voisins[j] += 1
print("degré dans le graphe des contacts (paires à distance^2 = 36 exactement) :", sorted(collections.Counter(voisins.values()).items()))
