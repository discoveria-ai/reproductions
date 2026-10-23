"""Moteur B : second vérificateur exact du chargement d'anneau à 15 paires, de code distinct du moteur A.

Différences avec A (aucun import de A) :
  - analyse des chaînes à la main (int, math.gcd), pas de fractions.Fraction ;
  - toutes les valeurs mises au même dénominateur D (ppcm), puis entiers Python seuls ;
  - énumération des 2^15 choix par parcours en profondeur d'un arbre binaire (les préfixes sont partagés) ;
  - critère |2 P_k - T| (T = total), forme algébriquement équivalente à |P_k - (T - P_k)| utilisée par A ;
  - recontrôle complet par sympy.Rational : les 32 768 choix sont recalculés avec une autre énumération
    (itertools.product) et le même minimum, le même nombre de choix minimaux et la même liste de masques sont exigés.
Convention des masques : le bit i vaut 1 si z_i = -u_i (la même que A, pour comparer les listes).

Usage : python -I -X utf8 verif_b.py <best.json> --id 2576 [--attendu 9/8] [--sans-sympy]
Code de sortie : 0 si valide (et égal à --attendu s'il est donné), 1 sinon, 2 si mal formé.
"""

import argparse
import hashlib
import itertools
import json
import math
import re
import sys

N = 15
MOTIF = re.compile(r"(0|[1-9][0-9]*)(\.[0-9]+|/[1-9][0-9]*)?")
ANCIEN = (40317937698944779, 36028797018963968)


class Refus(ValueError):
    pass


def analyser(texte):
    """Chaîne -> (numérateur, dénominateur) réduits, entiers Python."""
    if not isinstance(texte, str):
        raise Refus("valeur non chaîne : les valeurs doivent être des chaînes")
    if not (1 <= len(texte) <= 80):
        raise Refus("longueur de chaîne hors de 1..80")
    m = MOTIF.fullmatch(texte)
    if m is None:
        raise Refus("format : décimal ou fraction positifs attendus")
    entier, suite = m.group(1), m.group(2)
    if suite is None:
        num, den = int(entier), 1
    elif suite[0] == "/":
        num, den = int(entier), int(suite[1:])
    else:
        chiffres = suite[1:]
        num, den = int(entier + chiffres), 10 ** len(chiffres)
    g = math.gcd(num, den)
    num, den = num // g, den // g
    if num.bit_length() > 64 or den.bit_length() > 64:
        raise Refus("numérateur ou dénominateur réduit dépassant 64 bits")
    return num, den


def mise_en_forme(paires):
    """Valide, puis renvoie (D, [U_i], [V_i]) avec u_i = U_i / D, v_i = V_i / D."""
    if not isinstance(paires, list) or len(paires) != N:
        raise Refus(f"{N} paires exactement attendues")
    brutes = []
    for p in paires:
        if not isinstance(p, list) or len(p) != 2:
            raise Refus("chaque entrée doit être une paire [u, v]")
        brutes.append((analyser(p[0]), analyser(p[1])))
    D = 1
    for (nu, du), (nv, dv) in brutes:
        D = math.lcm(D, du, dv)
    U = [nu * (D // du) for (nu, du), _ in brutes]
    V = [nv * (D // dv) for _, (nv, dv) in brutes]
    for i in range(N):
        if U[i] + V[i] > D:
            raise Refus("u + v <= 1 violé")
    return D, U, V


def minimum_entier(U, V):
    """Parcours en profondeur : renvoie (minimum de max_k |2 P_k - T| en unités 1/D, liste triée des masques)."""
    meilleur = [None]
    masques = []

    def descendre(i, masque, prefixes, somme):
        if i == N:
            T = somme
            m = max(abs(2 * p - T) for p in prefixes)
            if meilleur[0] is None or m < meilleur[0]:
                meilleur[0] = m
                masques.clear()
                masques.append(masque)
            elif m == meilleur[0]:
                masques.append(masque)
            return
        for bit in (0, 1):
            z = -U[i] if bit else V[i]
            descendre(i + 1, masque | (bit << i), prefixes + [somme + z], somme + z)

    descendre(0, 0, [], 0)
    return meilleur[0], sorted(masques)


def minimum_sympy(paires_brutes):
    """Recalcul complet avec sympy.Rational et itertools.product (aucun entier mis au même dénominateur)."""
    import sympy
    from sympy import Rational

    vals = [(Rational(p[0]), Rational(p[1])) for p in paires_brutes]
    meilleur, masques = None, []
    for choix in itertools.product((0, 1), repeat=N):
        z = [-vals[i][0] if choix[i] else vals[i][1] for i in range(N)]
        total = sum(z, Rational(0))
        courant, pire = Rational(0), Rational(0)
        for x in z:
            courant += x
            d = abs(2 * courant - total)
            if d > pire:
                pire = d
        masque = sum(1 << i for i in range(N) if choix[i])
        if meilleur is None or pire < meilleur:
            meilleur, masques = pire, [masque]
        elif pire == meilleur:
            masques.append(masque)
    return meilleur, sorted(masques), sympy.__version__


def evaluer(paires_brutes, avec_sympy=False):
    try:
        D, U, V = mise_en_forme(paires_brutes)
    except Refus as e:
        return {"valide": False, "raison": str(e), "valeur": None, "nb_masques": 0, "empreinte_masques": None}
    m, masques = minimum_entier(U, V)
    num, den = m, D
    g = math.gcd(num, den)
    num, den = num // g, den // g  # valeur = (min / D) en unités de 1 : le critère |2 P_k - T| est déjà la valeur
    r = {"valide": True, "raison": "", "valeur": (num, den), "nb_masques": len(masques),
         "empreinte_masques": hashlib.sha256(",".join(map(str, masques)).encode()).hexdigest(),
         "masques": masques, "denominateur_commun": D}
    if avec_sympy:
        ms, mm, ver = minimum_sympy(paires_brutes)
        r["sympy"] = {"version": ver, "valeur": (int(ms.p), int(ms.q)), "nb_masques": len(mm), "meme_liste": mm == masques}
    return r


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier")
    ap.add_argument("--id", type=int, required=True)
    ap.add_argument("--attendu", default=None)
    ap.add_argument("--sans-sympy", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.fichier, "rb") as f:
            liste = json.loads(f.read().decode("utf-8"))
        s = next(x for x in liste if x["id"] == a.id)
        brut = s["data"]["pairs"]
    except (StopIteration, KeyError, ValueError, TypeError) as e:
        print(f"MAL FORMÉ : {e!r}")
        return 2
    r = evaluer(brut, avec_sympy=not a.sans_sympy)
    if not r["valide"]:
        print(f"REJETÉ : {r['raison']}")
        return 1
    num, den = r["valeur"]
    print("MOTEUR B (entiers au même dénominateur, parcours en profondeur ; recontrôle sympy.Rational)")
    print(f"soumission {a.id} ({s.get('agentName')}, score stocké {s.get('score')})")
    print(f"dénominateur commun D = {r['denominateur_commun']}")
    print(f"VALEUR EXACTE = {num}/{den}  (= {num / den!r} en décimal, affichage seulement)")
    print(f"masques atteignant le minimum : {r['nb_masques']} ; sha256 de la liste triée : {r['empreinte_masques']}")
    print(f"premier masque minimal : {r['masques'][0]} ; dernier : {r['masques'][-1]}")
    ao_num, ao_den = ANCIEN
    diff_num = num * ao_den - ao_num * den  # signe de valeur - ancien record, dénominateurs > 0
    print(f"ancien record cité par la plateforme : {ao_num}/{ao_den} ; valeur > ancien : {diff_num > 0} ; "
          f"valeur - ancien = {diff_num}/{den * ao_den}")
    if "sympy" in r:
        s2 = r["sympy"]
        ok = s2["valeur"] == (num, den) and s2["nb_masques"] == r["nb_masques"] and s2["meme_liste"]
        print(f"sympy {s2['version']} (itertools.product, 32768 choix) : {s2['valeur'][0]}/{s2['valeur'][1]} ; "
              f"{s2['nb_masques']} masques ; même liste : {s2['meme_liste']} ; concordance : {ok}")
        if not ok:
            print("DISCORDANCE entre l'énumération en entiers et sympy")
            return 1
    if a.attendu is not None:
        en, ed = (a.attendu.split("/") + ["1"])[:2]
        egal = num * int(ed) == int(en) * den
        print(f"valeur revendiquée {a.attendu} : égalité exacte = {egal}")
        if not egal:
            print("ÉCART avec la valeur revendiquée")
            return 1
    print("VALIDE")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
