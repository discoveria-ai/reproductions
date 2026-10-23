"""Moteur B : second vérificateur, de code et d'algorithme distincts du moteur A (aucun import commun).

Même propriété que A : mots binaires de longueur 16, deux à deux distincts, et aucune paire de mots distincts n'a de
sous-séquence commune de longueur 14 (équivalent à D2(x) inter D2(y) vide, car deux mots de longueur 16 partagent un
descendant de longueur 14 exactement quand ils ont une sous-séquence commune de longueur 14).

Algorithme B : pour chacune des C(n,2) paires, longueur de la plus longue sous-séquence commune (LCS) par programmation
dynamique 16 x 16 sur des chaînes ; la paire est en conflit quand LCS >= 14. Aucune énumération de descendants.
Sont aussi rendus la répartition exacte des LCS sur les paires (le maximum doit être <= 13) et le nombre de paires à LCS = 13.

Usage : python -I -X utf8 verif_b.py <reponse_api.json> [--id 2605] [--n 219]
Code de sortie : 0 valide, 1 rejeté, 2 fichier mal formé.
"""

import argparse
import json
import sys
from collections import Counter

LONGUEUR = 16
SEUIL = LONGUEUR - 2  # deux suppressions : conflit quand LCS >= 14


def lcs(x, y):
    """Longueur de la plus longue sous-séquence commune de deux chaînes (ligne par ligne)."""
    prec = [0] * (len(y) + 1)
    for cx in x:
        cur = [0]
        for j, cy in enumerate(y):
            cur.append(prec[j] + 1 if cx == cy else max(prec[j + 1], cur[j]))
        prec = cur
    return prec[-1]


def lire(chemin, ident):
    """Rend (objet, mots) pour l'id demandé dans la réponse de l'API, sans rien supposer de plus que le JSON."""
    with open(chemin, "rb") as f:
        donnees = json.loads(f.read().decode("utf-8"))
    if not isinstance(donnees, list):
        raise ValueError("la réponse n'est pas une liste")
    candidats = [s for s in donnees if isinstance(s, dict) and s.get("id") == ident]
    if len(candidats) != 1:
        raise ValueError(f"{len(candidats)} solution(s) d'id {ident}")
    return candidats[0], candidats[0]["data"]["words"]


def verifier(mots, n_revendique):
    """mots : liste d'objets Python non fiables. Rend {valide, motifs, conflits, stats}."""
    vide = {"conflits": [], "stats": {}}
    if not isinstance(mots, list):
        return {"valide": False, "motifs": ["forme : pas une liste"], **vide}
    motifs = []
    if len(mots) != n_revendique:
        motifs.append(f"forme : {len(mots)} mots pour {n_revendique} revendiqués")
    for i, w in enumerate(mots):
        if type(w) is not str:
            motifs.append(f"forme : mot {i} de type {type(w).__name__}")
        elif len(w) != LONGUEUR or set(w) - {"0", "1"}:
            motifs.append(f"forme : mot {i} n'est pas un mot binaire de longueur {LONGUEUR}")
    if motifs:
        return {"valide": False, "motifs": motifs, **vide}
    vus = Counter(mots)
    doublons = [w for w, c in vus.items() if c > 1]
    if doublons:
        return {"valide": False, "motifs": [f"mots non distincts : {len(doublons)} mot(s) répété(s)"], **vide}
    repartition = Counter()
    conflits = []
    n = len(mots)
    for i in range(n):
        for j in range(i + 1, n):
            v = lcs(mots[i], mots[j])
            repartition[v] += 1
            if v >= SEUIL:
                conflits.append((i, j))
    stats = {
        "mots": n,
        "paires": n * (n - 1) // 2,
        "lcs_maximal": max(repartition) if repartition else None,
        "paires_a_lcs_13": repartition.get(SEUIL - 1, 0),
        "repartition_lcs": dict(sorted(repartition.items())),
    }
    if conflits:
        motifs.append(f"{len(conflits)} paire(s) avec une sous-séquence commune de longueur >= {SEUIL}")
    return {"valide": not motifs, "motifs": motifs, "conflits": conflits, "stats": stats}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier")
    ap.add_argument("--id", type=int, default=2605)
    ap.add_argument("--n", type=int, default=219)
    a = ap.parse_args(argv)
    try:
        s, mots = lire(a.fichier, a.id)
        if s.get("score") != len(mots):
            raise ValueError(f"score publié {s.get('score')} différent du nombre de mots {len(mots)}")
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"MOTEUR B : fichier mal formé : {e}")
        return 2
    r = verifier(mots, a.n)
    print(f"MOTEUR B : solution {a.id}, {len(mots)} mots, {a.n} revendiqués")
    for k, v in r["stats"].items():
        print(f"  {k} = {v}")
    print(f"  paires en conflit : {len(r['conflits'])}")
    for m in r["motifs"]:
        print(f"  motif : {m}")
    print("  VERDICT : " + ("VALIDE" if r["valide"] else "REJETÉ"))
    return 0 if r["valide"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
