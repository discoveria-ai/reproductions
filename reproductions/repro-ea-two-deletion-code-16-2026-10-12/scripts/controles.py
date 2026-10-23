"""Contrôles pour les moteurs A et B (code corrigeant 2 suppressions, longueur 16, solution à 219 mots).

Chaque contrôle négatif modifie les mots EN MÉMOIRE (rien n'est écrit) et doit être rejeté par les DEUX moteurs, avec
des paires en conflit identiques d'un moteur à l'autre. Les contrôles positifs doivent être acceptés par les deux.
Deux contrôles de cohérence s'y ajoutent : la suppression par bits du moteur A égale la suppression par chaînes sur les
65 536 mots de 16 bits, et A et B donnent exactement les mêmes paires en conflit sur des codes aléatoires.

Usage : python -I -X utf8 controles.py <reponse_api.json> <dossier-des-moteurs> [--id 2605] [--n 219]
Code de sortie : 0 si tous les contrôles se comportent comme attendu, 1 sinon.
"""

import importlib.util
import json
import random
import sys
from pathlib import Path


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def inserer_bits(w, positions_suppr, ajouts):
    """Supprime les positions données de w (liste de 16) puis insère les couples (position, bit) dans le résultat de 14."""
    s = [c for k, c in enumerate(w) if k not in positions_suppr]
    for pos, bit in sorted(ajouts):
        s.insert(pos, bit)
    return "".join(s)


def main(argv):
    fichier, dossier = argv[0], argv[1]
    ident = int(argv[argv.index("--id") + 1]) if "--id" in argv else 2605
    n0 = int(argv[argv.index("--n") + 1]) if "--n" in argv else 219
    A = charger_module("verif_a", Path(dossier) / "verif_a.py")
    B = charger_module("verif_b", Path(dossier) / "verif_b.py")
    base = list(A.charger(fichier, ident)["data"]["words"])
    assert len(base) == n0 and len(set(base)) == n0

    def moteurs(mots, n):
        return A.verifier(mots, n), B.verifier(mots, n)

    def retourner(w, k):
        return w[:k] + ("1" if w[k] == "0" else "0") + w[k + 1:]

    lignes, ok_global = [], True

    def cas_negatif(nom, mots, n, motif_a, motif_b, conflits_attendus=None):
        nonlocal ok_global
        ra, rb = moteurs(mots, n)
        rejet = (not ra["valide"]) and (not rb["valide"])
        raison = any(motif_a in m for m in ra["motifs"]) and any(motif_b in m for m in rb["motifs"])
        memes = sorted(ra["conflits"]) == sorted(rb["conflits"])
        contient = True
        if conflits_attendus is not None:
            contient = all(c in ra["conflits"] for c in conflits_attendus)
        ok = rejet and raison and memes and contient
        ok_global &= ok
        lignes.append(f"{nom:<86} rejet    {'REJETÉ' if not ra['valide'] else 'VALIDE':<8} {'REJETÉ' if not rb['valide'] else 'VALIDE':<8} {'OK' if ok else 'ÉCHEC'}")
        lignes.append(f"    A : {ra['motifs']} ; conflits {ra['conflits'][:6]}{' ...' if len(ra['conflits']) > 6 else ''}")
        lignes.append(f"    B : {rb['motifs']} ; conflits {rb['conflits'][:6]}{' ...' if len(rb['conflits']) > 6 else ''}")
        return ra, rb

    def cas_positif(nom, mots, n):
        nonlocal ok_global
        ra, rb = moteurs(mots, n)
        ok = ra["valide"] and rb["valide"]
        ok_global &= ok
        lignes.append(f"{nom:<86} valide   {'VALIDE' if ra['valide'] else 'REJETÉ':<8} {'VALIDE' if rb['valide'] else 'REJETÉ':<8} {'OK' if ok else 'ÉCHEC'}")
        return ra, rb

    # --- négatifs : un mot ajouté qui viole la propriété ---
    w0 = base[0]
    m = base + [retourner(w0, 7)]
    cas_negatif("N1 220e mot ajouté = mot 0 avec un bit inversé (LCS 15 avec lui)", m, 220, "partageant", "sous-séquence commune", [(0, 219)])

    # N2 : mot ajouté à LCS exactement 14 avec le mot 10 : deux suppressions puis deux insertions, absent du code
    w10 = base[10]
    cand = None
    for p in range(16):
        for q in range(p + 1, 16):
            for ins in ((0, "0"), (14, "1")), ((3, "1"), (9, "0")), ((5, "0"), (5, "0")):
                c = inserer_bits(w10, {p, q}, ins)
                if len(c) == 16 and c not in base:
                    cand = c
                    break
            if cand:
                break
        if cand:
            break
    assert cand and B.lcs(cand, w10) >= 14
    m = base + [cand]
    cas_negatif(f"N2 220e mot à LCS >= 14 avec le mot 10 (deux suppressions, deux insertions) : {cand}", m, 220, "partageant", "sous-séquence commune", [(10, 219)])

    # N3 : doublon exact
    cas_negatif("N3 220e mot = copie exacte du mot 7 (doublon)", base + [base[7]], 220, "non distincts", "non distincts")

    # N4 : un mot remplacé, même effectif 219
    m = list(base)
    m[5] = retourner(base[6], 3)
    cas_negatif("N4 mot 5 remplacé par le mot 6 avec un bit inversé (effectif inchangé 219)", m, 219, "partageant", "sous-séquence commune", [(5, 6)])

    # N5.. : entrées hors format
    cas_negatif("N5 mot de longueur 15 (mot 3 tronqué)", base[:3] + [base[3][:15]] + base[4:], 219, "longueur", "n'est pas un mot binaire")
    cas_negatif("N6 mot avec un caractère '2'", base[:3] + [base[3][:5] + "2" + base[3][6:]] + base[4:], 219, "hors 0/1", "n'est pas un mot binaire")
    cas_negatif("N7 entier 101 à la place d'une chaîne", base[:3] + [101] + base[4:], 219, "pas une chaîne", "de type int")
    cas_negatif("N8 218 mots pour 219 revendiqués", base[:218], 219, "218 mots pour 219", "218 mots pour 219")
    cas_negatif("N9 mot suivi d'une espace (longueur 17)", base[:3] + [base[3] + " "] + base[4:], 219, "longueur 17", "n'est pas un mot binaire")

    # N10 : frontière exacte : LCS 14 rejeté
    zeros = "0" * 16
    cas_negatif("N10 {0^16, 0^14 11} : LCS exactement 14 (frontière côté rejet)", [zeros, "0" * 14 + "11"], 2, "partageant", "sous-séquence commune", [(0, 1)])

    # --- positifs ---
    cas_positif("P1 fichier intact, 219 revendiqués", base, n0)
    cas_positif("P2 les 218 premiers mots, 218 revendiqués", base[:218], 218)
    cas_positif("P3 les 100 premiers mots, 100 revendiqués", base[:100], 100)
    cas_positif("P4 {0^16, 1^16}", [zeros, "1" * 16], 2)
    ra, rb = cas_positif("P5 {0^16, 0^13 111} : LCS exactement 13 (frontière côté acceptation)", [zeros, "0" * 13 + "111"], 2)
    ok = rb["stats"]["lcs_maximal"] == 13
    ok_global &= ok
    lignes.append(f"    P5 : LCS maximal observé par B = {rb['stats']['lcs_maximal']} (attendu 13) {'OK' if ok else 'ÉCHEC'}")

    # --- cohérence : suppression par bits (A) = suppression par chaînes, pour les 65 536 mots ---
    desaccords = 0
    for x in range(1 << 16):
        s = format(x, "016b")
        par_chaines = {int(s[:i] + s[i + 1:j] + s[j + 1:], 2) for i in range(15) for j in range(i + 1, 16)}
        if par_chaines != A.descendants(x):
            desaccords += 1
    ok = desaccords == 0
    ok_global &= ok
    lignes.append(f"C1 suppression par bits (A) = suppression par chaînes sur les 65536 mots : {desaccords} désaccord(s) {'OK' if ok else 'ÉCHEC'}")

    # --- cohérence : A et B ont exactement les mêmes paires en conflit sur des codes aléatoires (graine fixe) ---
    rng = random.Random(20261012)
    nb_codes, taille, total_conflits, desaccords_c = 40, 150, 0, 0
    for _ in range(nb_codes):
        mots = [format(x, "016b") for x in rng.sample(range(1 << 16), taille)]
        ra, rb = A.verifier(mots, taille), B.verifier(mots, taille)
        total_conflits += len(ra["conflits"])
        if sorted(ra["conflits"]) != sorted(rb["conflits"]) or ra["valide"] != rb["valide"]:
            desaccords_c += 1
    ok = desaccords_c == 0 and total_conflits > 0
    ok_global &= ok
    lignes.append(f"C2 {nb_codes} codes aléatoires de {taille} mots (graine 20261012) : {total_conflits} paires en conflit au total, {desaccords_c} désaccord(s) entre A et B {'OK' if ok else 'ÉCHEC'}")

    print("\n".join(lignes))
    print("TOUS LES CONTRÔLES CONFORMES" if ok_global else "AU MOINS UN CONTRÔLE NON CONFORME")
    return 0 if ok_global else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
