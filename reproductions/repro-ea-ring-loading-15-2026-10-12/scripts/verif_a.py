"""Moteur A : vérificateur exact du problème de chargement d'anneau à 15 paires (EinsteinArena, problème 30).

Définition (énoncé de la plateforme, api/problems/ring-loading-15) : 15 paires (u_i, v_i) de rationnels >= 0 avec
u_i + v_i <= 1. Pour chaque choix z_i dans {v_i, -u_i} (2^15 = 32 768 choix), on calcule
    M(z) = max_{k=1..15} | sum_{i<=k} z_i - sum_{i>k} z_i |
et le score est A(u, v) = min_z M(z). On cherche à le maximiser.

Arithmétique : fractions.Fraction seule, aucun flottant (float() n'est appelé que pour l'affichage décimal).
Formulation de A : somme du préfixe et somme du suffixe calculées séparément pour chaque k (le vérificateur de la
plateforme, lui, utilise 2*préfixe - total). Convention des masques : le bit i du masque vaut 1 si z_i = -u_i.
Les règles de format reproduisent celles du vérificateur de la plateforme (chaîne de 1 à 80 caractères, motif
décimal ou fraction, numérateur et dénominateur réduits tenant sur 64 bits, u + v <= 1, exactement 15 paires).

Usage : python -I -X utf8 verif_a.py <best.json> --id 2576 [--attendu 9/8]
Code de sortie : 0 si la configuration est valide (et égale à --attendu s'il est donné), 1 sinon, 2 si mal formé.
"""

import argparse
import hashlib
import itertools
import json
import re
import sys
from fractions import Fraction

N = 15
MOTIF = re.compile(r"^(?:0|[1-9]\d*)(?:(?:\.\d+)|(?:/[1-9]\d*))?$")
ANCIEN_RECORD = Fraction(40317937698944779, 36028797018963968)  # valeur citée dans l'énoncé de la plateforme


class Refus(ValueError):
    pass


def rationnel(texte):
    if not isinstance(texte, str):
        raise Refus("valeur non chaîne : les valeurs doivent être des chaînes")
    if not 1 <= len(texte) <= 80:
        raise Refus("longueur de chaîne hors de 1..80")
    if MOTIF.fullmatch(texte) is None:
        raise Refus("format : décimal ou fraction positifs attendus")
    x = Fraction(texte)
    if x.numerator.bit_length() > 64 or x.denominator.bit_length() > 64:
        raise Refus("numérateur ou dénominateur réduit dépassant 64 bits")
    return x


def paires_valides(paires):
    if not isinstance(paires, list) or len(paires) != N:
        raise Refus(f"{N} paires exactement attendues")
    sortie = []
    for p in paires:
        if not isinstance(p, list) or len(p) != 2:
            raise Refus("chaque entrée doit être une paire [u, v]")
        u, v = rationnel(p[0]), rationnel(p[1])
        if u + v > 1:
            raise Refus("u + v <= 1 violé")
        sortie.append((u, v))
    return sortie


def pire_cas(z):
    """M(z) : maximum sur k de |somme des k premiers - somme des suivants|, exact."""
    pire = Fraction(0)
    for k in range(1, N + 1):
        prefixe = sum(z[:k], Fraction(0))
        suffixe = sum(z[k:], Fraction(0))
        pire = max(pire, abs(prefixe - suffixe))
    return pire


def valeur(paires):
    """Retourne (minimum exact, liste triée des masques qui l'atteignent)."""
    meilleur, masques = None, []
    for masque in range(1 << N):
        z = [-u if (masque >> i) & 1 else v for i, (u, v) in enumerate(paires)]
        m = pire_cas(z)
        if meilleur is None or m < meilleur:
            meilleur, masques = m, [masque]
        elif m == meilleur:
            masques.append(masque)
    return meilleur, masques


def evaluer(paires_brutes):
    """Contrat commun aux moteurs : dict(valide, raison, valeur, nb_masques, empreinte_masques)."""
    try:
        paires = paires_valides(paires_brutes)
    except Refus as e:
        return {"valide": False, "raison": str(e), "valeur": None, "nb_masques": 0, "empreinte_masques": None}
    v, masques = valeur(paires)
    emp = hashlib.sha256(",".join(map(str, masques)).encode()).hexdigest()
    return {"valide": True, "raison": "", "valeur": v, "nb_masques": len(masques), "empreinte_masques": emp,
            "masques": masques}


def charger(chemin):
    with open(chemin, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def soumission(liste, ident):
    for s in liste:
        if s["id"] == ident:
            return s
    raise KeyError(f"soumission {ident} absente")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier")
    ap.add_argument("--id", type=int, required=True)
    ap.add_argument("--attendu", default=None)
    a = ap.parse_args(argv)
    try:
        s = soumission(charger(a.fichier), a.id)
        brut = s["data"]["pairs"]
    except (KeyError, ValueError, TypeError) as e:
        print(f"MAL FORMÉ : {e}")
        return 2
    r = evaluer(brut)
    if not r["valide"]:
        print(f"REJETÉ : {r['raison']}")
        return 1
    v = r["valeur"]
    print("MOTEUR A (fractions.Fraction, préfixe et suffixe séparés)")
    print(f"soumission {a.id} ({s.get('agentName')}, score stocké {s.get('score')})")
    print(f"15 paires valides, 32768 choix énumérés")
    print(f"VALEUR EXACTE = {v}  (= {float(v)!r} en décimal, affichage seulement)")
    print(f"masques atteignant le minimum : {r['nb_masques']} ; sha256 de la liste triée : {r['empreinte_masques']}")
    print(f"premier masque minimal : {r['masques'][0]} ; dernier : {r['masques'][-1]}")
    print(f"ancien record cité par la plateforme : {ANCIEN_RECORD}")
    diff = v - ANCIEN_RECORD
    print(f"valeur - ancien record = {diff} (> 0 : {diff > 0}) ; rapport valeur/ancien = {float(v / ANCIEN_RECORD):.12f}")
    if a.attendu is not None:
        egal = v == Fraction(a.attendu)
        print(f"valeur revendiquée {a.attendu} : égalité exacte = {egal}")
        if not egal:
            print("ÉCART avec la valeur revendiquée")
            return 1
    print("VALIDE")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
