"""Contrôles négatifs et positifs pour les moteurs A et B (kissing number d=11, solution n=604).

Chaque contrôle négatif modifie la solution EN MÉMOIRE (rien n'est écrit) et doit être rejeté par les DEUX moteurs,
pour la raison attendue (un contrôle isole une seule vérification). Les contrôles positifs doivent être acceptés.

Usage : python -I -X utf8 controles.py <solution.json> <dossier-des-moteurs>
Code de sortie : 0 si tous les contrôles se comportent comme attendu, 1 sinon.
"""

import copy
import importlib.util
import json
import sys
from pathlib import Path


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def vecteur(coords):
    """coords : liste de 11 éléments (a, b) = a + b sqrt 2 ; retourne la liste plate de 22 entiers."""
    assert len(coords) == 11
    return [x for ab in coords for x in ab]


Z = (0, 0)


def main(argv):
    fichier, dossier = argv
    A = charger_module("verif_a", Path(dossier) / "verif_a.py")
    B = charger_module("verif_b", Path(dossier) / "verif_b.py")
    base = A.charger(fichier)
    n0 = len(base["vectors"])
    assert n0 == 604 and base["vectors"][0] == [6] + [0] * 21

    def moteurs(data, n):
        ra = A.verifier(data, n, (36, 0))
        rb = B.verifier(data, n, 36, avec_sympy=True)
        return ra, rb

    def aff(r):
        return "VALIDE" if r["valide"] else "REJETÉ"

    cas = []  # (nom, data, n_attendu, attendu_valide, mot_cle_raison_A, mot_cle_raison_B)

    # N1 : un vecteur perturbé (+1 sur une coordonnée rationnelle) : norme modifiée
    d = copy.deepcopy(base); d["vectors"][5][0] += 1
    cas.append(("N1 vecteur 5 perturbé (+1 sur p_0)", d, 604, False, "norme", "diagonale"))

    # N2 : 605e vecteur = copie exacte du vecteur 7
    d = copy.deepcopy(base); d["n"] = 605; d["vectors"].append(list(d["vectors"][7]))
    cas.append(("N2 605e vecteur dupliqué (copie du vecteur 7)", d, 605, False, "non distincts", "non distincts"))

    # N3 : 605e vecteur de mauvaise norme (7 e_1 : norme^2 49)
    d = copy.deepcopy(base); d["n"] = 605; d["vectors"].append(vecteur([(7, 0)] + [Z] * 10))
    cas.append(("N3 605e vecteur de mauvaise norme (7 e_1, norme^2 = 49)", d, 605, False, "norme", "diagonale"))

    # N4 : 605e vecteur de norme 36 mais trop proche de 6 e_1 : (4 sqrt2, 2, 0..) ; <x,y> = 24 sqrt2 > 18
    # dist^2 a (6,0..0) = 72 - 48 sqrt2 ; dist^2 - 36 = 36 - 48 sqrt2 : a > 0, b < 0, a^2 < 2 b^2 (signe non trivial)
    d = copy.deepcopy(base); d["n"] = 605; d["vectors"].append(vecteur([(0, 4), (2, 0)] + [Z] * 9))
    cas.append(("N4 605e vecteur de norme 36 trop proche de 6 e_1 (4 sqrt2, 2, 0..)", d, 605, False, "paire", "paire"))

    # N5 : le dernier vecteur remplacé par (3 sqrt2, 3 sqrt2, 0..) : norme 36, distinct, mais dist^2 a 6 e_1 = 72 - 36 sqrt2
    d = copy.deepcopy(base); d["vectors"][603] = vecteur([(0, 3), (0, 3)] + [Z] * 9)
    cas.append(("N5 dernier vecteur remplacé par (3 sqrt2, 3 sqrt2, 0..) : norme 36, distance violée", d, 604, False, "paire", "paire"))

    # N6 : un vecteur de moins, alors que 604 sont revendiqués
    d = copy.deepcopy(base); d["n"] = 603; d["vectors"] = d["vectors"][:603]
    cas.append(("N6 603 vecteurs pour une revendication de 604", d, 604, False, "forme", "forme"))

    # N7 : entrée flottante (6.0 au lieu de 6) ; N8 : booléen à la place d'un entier
    d = copy.deepcopy(base); d["vectors"][0][0] = 6.0
    cas.append(("N7 entrée flottante 6.0", d, 604, False, "forme", "forme"))
    d = copy.deepcopy(base); d["vectors"][1][1] = False
    cas.append(("N8 entrée booléenne false à la place de 0", d, 604, False, "forme", "forme"))

    # N9 : même norme apparente mais partie en sqrt2 non nulle : (0,3) x 4 + ... = 3 sqrt2 coordonnées : 4 * 18 = 72 pas 36 ;
    # ici (a, b) = (0, 1) répété 18 fois impossible en 11 coordonnées : on prend (6,1)^... : norme^2 = 36 + 2 + 12 sqrt2
    d = copy.deepcopy(base); d["vectors"][2] = vecteur([(0, 0), (0, 0), (6, 1)] + [Z] * 8)
    cas.append(("N9 vecteur 2 : coordonnée 6 + sqrt2 (norme^2 = 38 + 12 sqrt2)", d, 604, False, "norme", "diagonale"))

    # Positifs : 603 premiers vecteurs revendiqués 603 ; 22 premiers (+-6 e_i) revendiqués 22 ; fichier intact
    d = copy.deepcopy(base); d["n"] = 603; d["vectors"] = d["vectors"][:603]
    cas.append(("P1 sous-ensemble de 603 vecteurs revendiqué 603 (doit passer)", d, 603, True, None, None))
    d = copy.deepcopy(base); d["n"] = 16; d["vectors"] = d["vectors"][:16]
    cas.append(("P2 16 premiers vecteurs (+-6 e_i, i < 8) revendiqués 16 (doit passer ; distance^2 min = 72)", d, 16, True, None, None))
    cas.append(("P3 fichier intact, 604 (doit passer)", base, 604, True, None, None))

    ok_global = True
    print(f"{'contrôle':<92} {'attendu':<8} {'A':<8} {'B':<8} verdict")
    for nom, data, n, attendu, mca, mcb in cas:
        ra, rb = moteurs(data, n)
        bon = (ra["valide"] == attendu) and (rb["valide"] == attendu)
        if not attendu:
            # le motif de rejet doit être celui attendu (un seul contrôle isolé)
            bon = bon and any(mca in x for x in ra["raisons"]) and any(mcb in x for x in rb["raisons"])
            if nom.startswith(("N4", "N5")):  # distance seule : ni norme, ni doublon
                bon = bon and len(ra["raisons"]) == 1 and len(rb["raisons"]) == 1
            if nom.startswith("N2"):  # doublon : ses distances nulles violent aussi le seuil, mais pas la norme
                bon = bon and not any("norme" in x for x in ra["raisons"])
        if nom.startswith("P2"):
            bon = bon and ra["distance2_min"] == (72, 0) and rb["distance2_min"] == (72, 0)
        if nom.startswith("P3"):
            bon = bon and ra["distance2_min"] == (36, 0) and ra["distance2_min"] == rb["distance2_min"] \
                and ra["paires_a_egalite"] == rb["paires_a_egalite"]
        ok_global &= bon
        print(f"{nom:<92} {'valide' if attendu else 'rejet':<8} {aff(ra):<8} {aff(rb):<8} {'OK' if bon else 'ÉCHEC'}")
        if not attendu:
            print(f"    A : {ra['raisons']}")
            print(f"    B : {rb['raisons']}")
            if "premiere_violation" in ra:
                i, j, dd = ra["premiere_violation"]
                print(f"    A : première violation : paire ({i}, {j}), distance^2 exacte = {dd[0]} + {dd[1]}*sqrt(2)")
    # N4 / N5 : valeur exacte attendue de la violation
    d4 = [c for c in cas if c[0].startswith("N4")][0][1]
    ra = A.verifier(d4, 605, (36, 0))
    mini4 = ra["distance2_min"]
    print(f"N4 : distance^2 minimale exacte observée = {mini4[0]} + {mini4[1]}*sqrt(2) (attendu pour (0, 604) : 72 - 48*sqrt(2))")
    d5 = [c for c in cas if c[0].startswith("N5")][0][1]
    mini5 = A.verifier(d5, 604, (36, 0))["distance2_min"]
    print(f"N5 : distance^2 minimale exacte observée = {mini5[0]} + {mini5[1]}*sqrt(2) (<= 72 - 36*sqrt(2) attendu pour (0, 603))")
    print("TOUS LES CONTRÔLES CONFORMES" if ok_global else "AU MOINS UN CONTRÔLE NON CONFORME")
    return 0 if ok_global else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
