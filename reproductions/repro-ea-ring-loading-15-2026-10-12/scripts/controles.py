"""Contrôles négatifs et positifs pour les moteurs A et B (chargement d'anneau à 15 paires, EinsteinArena).

Chaque contrôle modifie les données EN MÉMOIRE (rien n'est écrit) et passe aux DEUX moteurs ; les deux doivent
donner le même résultat, pour la raison attendue. Les contrôles négatifs rejettent soit l'entrée (format, contrainte),
soit la valeur revendiquée 9/8 (la configuration est valide mais sa valeur exacte est différente de 9/8).
Les contrôles positifs ont une valeur connue indépendamment du code : valeur citée par la plateforme pour la
construction d'AlphaEvolve, score stocké de chaque soumission, invariances exactes du problème (échange u/v,
renversement de l'ordre, homogénéité).

Usage : python -I -X utf8 controles.py <best.json> <dossier-des-moteurs>
Code de sortie : 0 si tous les contrôles se comportent comme attendu, 1 sinon.
"""

import copy
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

REVENDIQUE = Fraction(9, 8)
ANCIEN = Fraction(40317937698944779, 36028797018963968)


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def texte(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def main(argv):
    fichier, dossier = argv
    A = charger_module("verif_a", Path(dossier) / "verif_a.py")
    B = charger_module("verif_b", Path(dossier) / "verif_b.py")
    liste = json.loads(Path(fichier).read_bytes().decode("utf-8"))
    sol = {s["id"]: s for s in liste}
    base = sol[2576]["data"]["pairs"]
    cache = {}

    def moteurs(paires):
        cle = json.dumps(paires, sort_keys=True)
        if cle not in cache:
            ra = A.evaluer(paires)
            rb = B.evaluer(paires)
            va = ra["valeur"]
            vb = Fraction(*rb["valeur"]) if rb["valeur"] else None
            cache[cle] = (ra, rb, va, vb)
        return cache[cle]

    lignes, anomalies = [], []

    def noter(code, nom, ok, detail):
        lignes.append(f"{code} | {'CONFORME' if ok else 'NON CONFORME'} | {nom} | {detail}")
        if not ok:
            anomalies.append(code)

    # ---- contrôles négatifs : entrée rejetée par les deux moteurs, pour le motif attendu -------------------
    def neg_entree(code, nom, paires, mot_a, mot_b):
        ra, rb, _, _ = moteurs(paires)
        ok = (not ra["valide"]) and (not rb["valide"]) and mot_a in ra["raison"] and mot_b in rb["raison"]
        noter(code, nom, ok, f"A : {ra['raison'] or 'ACCEPTÉ'} ; B : {rb['raison'] or 'ACCEPTÉ'}")

    d = copy.deepcopy(base)[:14]
    neg_entree("N1", "14 paires au lieu de 15", d, "15 paires", "15 paires")

    d = copy.deepcopy(base); d[0] = ["1/2", "3/4"]
    neg_entree("N2", "paire 0 = (1/2, 3/4) : u + v = 5/4 > 1", d, "u + v", "u + v")

    d = copy.deepcopy(base); d[3] = ["-7/16", "9/16"]
    neg_entree("N3", "valeur négative -7/16", d, "format", "format")

    d = copy.deepcopy(base); d[4] = [0.25, "1/4"]
    neg_entree("N4", "nombre JSON 0.25 au lieu d'une chaîne", d, "non chaîne", "non chaîne")

    d = copy.deepcopy(base); d[5] = ["1/36893488147419103232", "0"]
    neg_entree("N5", "dénominateur 2^65 (dépasse 64 bits)", d, "64 bits", "64 bits")

    d = copy.deepcopy(base); d[6] = ["3/4", "1/4.5"]
    neg_entree("N6", "texte non rationnel '1/4.5'", d, "format", "format")

    # ---- contrôles négatifs : configuration valide mais valeur exacte != 9/8 ---------------------------------
    def neg_valeur(code, nom, paires):
        ra, rb, va, vb = moteurs(paires)
        ok = ra["valide"] and rb["valide"] and va == vb and va != REVENDIQUE
        alerte = ""
        if ok and va > REVENDIQUE:
            ok, alerte = False, " ; ALERTE : valeur > 9/8, à examiner (record plus haut ?)"
        det = (f"A : {va} ; B : {vb} ; {'< 9/8' if ok else 'pas < 9/8'}" + alerte
               if ra["valide"] and rb["valide"] else f"A : {ra['raison']} ; B : {rb['raison']}")
        noter(code, nom, ok, det)

    d = copy.deepcopy(base); d[4] = ["1/4", "1/8"]
    neg_valeur("N7", "paire 4 (1/4, 1/4) remplacée par (1/4, 1/8)", d)

    d = copy.deepcopy(base); d[1] = ["999999/1000000", "0"]
    neg_valeur("N8", "paire 1 (1, 0) remplacée par (999999/1000000, 0)", d)

    d = copy.deepcopy(base); d[7] = ["499999999/1000000000", "1/2"]
    neg_valeur("N9", "paire 7 (1/2, 1/2) : u réduit de 1e-9", d)

    neg_valeur("N10", "soumission 2593 (Wilhelmina, score stocké 1.1249999999999991)", sol[2593]["data"]["pairs"])
    neg_valeur("N11", "soumission 2574 (GPT-Explorer, score stocké 1.119047619047619)", sol[2574]["data"]["pairs"])
    neg_valeur("N12", "soumission 2566 (AlphaEvolve, ancien record)", sol[2566]["data"]["pairs"])
    neg_valeur("N13", "15 paires (0, 0)", [["0", "0"]] * 15)

    # ---- contrôles positifs -----------------------------------------------------------------------------------
    ra, rb, va, vb = moteurs(base)
    noter("P1", "soumission 2576 : 9/8 exactement (revendication)", va == vb == REVENDIQUE,
          f"A : {va} ; B : {vb} ; {ra['nb_masques']} et {rb['nb_masques']} masques minimaux")

    ra, rb, va, vb = moteurs(sol[2566]["data"]["pairs"])
    noter("P2", "soumission 2566 (AlphaEvolve) = valeur exacte citée par l'énoncé de la plateforme",
          va == vb == ANCIEN, f"A : {va} ; B : {vb} ; attendu : {ANCIEN}")

    tout, details = True, []
    for ident in sorted(sol):
        ra, rb, va, vb = moteurs(sol[ident]["data"]["pairs"])
        stocke = sol[ident]["score"]
        ok = ra["valide"] and rb["valide"] and va == vb and float(va) == stocke
        tout = tout and ok
        details.append(f"{ident}:{va if va is not None else 'rejeté'}")
    noter("P3", "float(valeur exacte) = score stocké pour les 7 soumissions, A et B d'accord", tout, " ; ".join(details))

    d = copy.deepcopy(base); d = [[p[1], p[0]] for p in d]
    _, _, va, vb = moteurs(d)
    noter("P4", "invariance : échange u <-> v dans toutes les paires", va == vb == REVENDIQUE, f"A : {va} ; B : {vb}")

    d = list(reversed(copy.deepcopy(base)))
    _, _, va, vb = moteurs(d)
    noter("P5", "invariance : ordre des 15 paires renversé", va == vb == REVENDIQUE, f"A : {va} ; B : {vb}")

    d = [[texte(Fraction(p[0]) / 2), texte(Fraction(p[1]) / 2)] for p in base]
    _, _, va, vb = moteurs(d)
    noter("P6", "homogénéité : toutes les valeurs divisées par 2 donnent 9/16", va == vb == REVENDIQUE / 2,
          f"A : {va} ; B : {vb}")

    _, _, v2574, _ = moteurs(sol[2574]["data"]["pairs"])
    d = [[texte(Fraction(p[0]) / 3), texte(Fraction(p[1]) / 3)] for p in sol[2574]["data"]["pairs"]]
    _, _, va, vb = moteurs(d)
    noter("P7", "homogénéité : soumission 2574 divisée par 3 donne le tiers de sa valeur", va == vb == v2574 / 3,
          f"A : {va} ; B : {vb} ; valeur de 2574 : {v2574}")

    print("Contrôles du rejeu (chaque ligne : code | conformité | contrôle | détail)")
    for l in lignes:
        print(l)
    nn = sum(1 for l in lignes if l.startswith("N"))
    npos = sum(1 for l in lignes if l.startswith("P"))
    print(f"{nn} contrôles négatifs, {npos} contrôles positifs ; non conformes : {anomalies or 'aucun'}")
    return 0 if not anomalies else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
