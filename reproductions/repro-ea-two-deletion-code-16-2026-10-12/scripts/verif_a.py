"""Moteur A : code corrigeant deux suppressions, longueur 16 ; énumération des descendants et index inversé.

Propriété vérifiée (énoncé de la plateforme EinsteinArena, problème two-deletion-code-16) : un ensemble C de mots
BINAIRES de LONGUEUR 16, DEUX À DEUX DISTINCTS, tel que pour deux mots distincts x, y de C les ensembles
D2(x) et D2(y) soient disjoints, où D2(x) = mots de longueur 14 obtenus en supprimant deux positions de x.
Équivalent : aucune paire de mots distincts n'a de sous-séquence commune de longueur 14 (le moteur B le calcule ainsi).

Algorithme A (aucun calcul de plus longue sous-séquence commune) :
  - chaque mot est un entier de 16 bits ; les 120 suppressions de deux positions se font par opérations sur les bits
    (pas de chaînes de caractères) ;
  - un index inversé 14 bits -> liste des indices de mots qui l'ont pour descendant ; tout seau à plus d'un mot
    donne les paires en conflit. Rien n'est tiré au hasard, aucun flottant, aucune tolérance.

Usage : python -I -X utf8 verif_a.py <reponse_api.json> [--id 2605] [--n 219]
Code de sortie : 0 valide, 1 rejeté, 2 fichier mal formé.
"""

import argparse
import json
import sys

L = 16
PAIRES_POSITIONS = [(p, q) for q in range(L) for p in range(q)]  # p < q, positions comptées depuis le bit de poids faible


def supprimer(x, p, q):
    """Supprime les bits p < q de l'entier x (16 bits) et rend l'entier de 14 bits. q d'abord : p n'est pas décalé."""
    x = ((x >> (q + 1)) << q) | (x & ((1 << q) - 1))
    return ((x >> (p + 1)) << p) | (x & ((1 << p) - 1))


def descendants(x):
    return {supprimer(x, p, q) for p, q in PAIRES_POSITIONS}


def charger(chemin, ident):
    """Lit la réponse de l'API (liste d'objets {id, agentName, score, createdAt, data:{words}}) et rend l'objet d'id donné."""
    obj = json.load(open(chemin, "rb"))
    if not isinstance(obj, list):
        raise ValueError("la réponse n'est pas une liste")
    trouves = [s for s in obj if isinstance(s, dict) and s.get("id") == ident]
    if len(trouves) != 1:
        raise ValueError(f"{len(trouves)} solution(s) d'id {ident}")
    return trouves[0]


def verifier(mots, n_revendique):
    """mots : liste d'objets Python (non fiables). Rend un dict {valide, motifs, conflits, stats}."""
    motifs, conflits, stats = [], [], {}
    if not isinstance(mots, list):
        return {"valide": False, "motifs": ["forme : les mots ne forment pas une liste"], "conflits": [], "stats": {}}
    if len(mots) != n_revendique:
        motifs.append(f"forme : {len(mots)} mots pour {n_revendique} revendiqués")
    entiers = []
    for i, w in enumerate(mots):
        if not isinstance(w, str):
            motifs.append(f"forme : mot {i} n'est pas une chaîne ({type(w).__name__})")
        elif len(w) != L:
            motifs.append(f"forme : mot {i} de longueur {len(w)} au lieu de {L}")
        elif any(c not in "01" for c in w):
            motifs.append(f"forme : mot {i} contient un caractère hors 0/1")
        else:
            entiers.append((i, int(w, 2)))
    if motifs:
        return {"valide": False, "motifs": motifs, "conflits": [], "stats": {}}
    if len(mots) != len(set(mots)):
        motifs.append(f"mots non distincts : {len(mots) - len(set(mots))} doublon(s)")
        return {"valide": False, "motifs": motifs, "conflits": [], "stats": {}}
    seaux = {}
    taille_boules = []
    for i, x in entiers:
        d = descendants(x)
        taille_boules.append(len(d))
        for v in d:
            seaux.setdefault(v, []).append(i)
    for v, lst in seaux.items():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                conflits.append((lst[a], lst[b]))
    conflits = sorted(set(conflits))
    stats = {
        "mots": len(entiers),
        "descendants_distincts_utilises": len(seaux),
        "somme_tailles_boules": sum(taille_boules),
        "taille_boule_min": min(taille_boules),
        "taille_boule_max": max(taille_boules),
        "occupation_max_d_un_seau": max(len(l) for l in seaux.values()),
        "mots_de_longueur_14_possibles": 1 << 14,
    }
    if conflits:
        motifs.append(f"{len(conflits)} paire(s) de mots partageant un descendant de longueur 14")
    return {"valide": not motifs, "motifs": motifs, "conflits": conflits, "stats": stats}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier")
    ap.add_argument("--id", type=int, default=2605)
    ap.add_argument("--n", type=int, default=219)
    a = ap.parse_args(argv)
    try:
        s = charger(a.fichier, a.id)
        mots = s["data"]["words"]
        if s.get("score") != len(mots):
            raise ValueError(f"score publié {s.get('score')} différent du nombre de mots {len(mots)}")
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"MOTEUR A : fichier mal formé : {e}")
        return 2
    r = verifier(mots, a.n)
    print(f"MOTEUR A : solution {a.id} ({s.get('agentName')}, {s.get('createdAt')}), {len(mots)} mots, {a.n} revendiqués")
    for k, v in r["stats"].items():
        print(f"  {k} = {v}")
    print(f"  paires en conflit : {len(r['conflits'])}")
    for m in r["motifs"]:
        print(f"  motif : {m}")
    print("  VERDICT : " + ("VALIDE" if r["valide"] else "REJETÉ"))
    return 0 if r["valide"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
