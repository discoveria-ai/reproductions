"""Contrôles négatifs, positifs et différentiel des moteurs A et B (aire de l'union des triangles de Kakeya).

Usage : python -I -X utf8 controles.py <offsets.txt> <reponse-api-best.json> <dossier-des-moteurs>
        (offsets.txt : forme canonique de la solution 2608 ; reponse-api-best.json : GET /api/solutions/best?problem_id=26)
Code de sortie : 0 si tous les contrôles ont l'issue attendue, 1 sinon.

Négatifs : doivent être REJETÉS par les deux moteurs (forme invalide, ou aire exacte arrondie différente de la
valeur revendiquée). Positifs : valeurs analytiques et classement public recalculés ; différentiel A/B sur des
cas aléatoires à petit n (offsets en huitièmes : nombreux croisements triples et triangles confondus).
"""

import importlib.util
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

REVENDIQUE = "0.10675394011230244"
ID_REVENDIQUE = 2608


def charger(dossier, nom):
    spec = importlib.util.spec_from_file_location(nom, Path(dossier) / f"{nom}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dec25(f):
    """Chaîne décimale exacte (<= 25 décimales) d'un Fraction dont le dénominateur divise 10^25."""
    v = f * 10 ** 25
    assert v.denominator == 1
    v = v.numerator
    s = str(abs(v)).rjust(26, "0")
    return ("-" if v < 0 else "") + s[:-25] + "." + s[-25:]


def lignes(chemin):
    t = Path(chemin).read_text(encoding="ascii").split("\n")
    return t[:-1] if t and t[-1] == "" else t


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    base = lignes(argv[0])
    api = json.loads(Path(argv[1]).read_bytes().decode("utf-8"))
    A, B = charger(argv[2], "verif_a"), charger(argv[2], "verif_b")
    cache = {}

    def passer(chaines, revendique, n=128):
        cle = (tuple(map(repr, chaines)), revendique, n)
        if cle not in cache:
            cache[cle] = (A.evaluer(chaines, revendique, n), B.evaluer(chaines, revendique, n))
        return cache[cle]

    echecs = 0
    print(f"{'contrôle':<92} {'attendu':<8} {'A':<8} {'B':<8} verdict")

    def ligne(nom, attendu, ra, rb, ok_extra=True, details=()):
        nonlocal echecs
        ok = ra[0] == attendu and rb[0] == attendu and ok_extra
        echecs += 0 if ok else 1
        print(f"{nom:<92} {('rejet' if attendu == 'REJETÉ' else 'accepté'):<8} {ra[0]:<8} {rb[0]:<8} {'OK' if ok else 'ÉCHEC'}")
        for d in details:
            print("    " + d)

    def aire_flottante(ra):
        return repr(float(ra[1])) if ra[1] is not None else "-"

    # ---- négatifs : même valeur revendiquée, entrée altérée
    def negatif(nom, chaines, revendique=REVENDIQUE, n=128):
        ra, rb = passer(chaines, revendique, n)
        det = [f"A : {m}" for m in ra[2][-1:]] + [f"B : {m}" for m in rb[2][-1:]]
        if ra[1] is not None:
            det.append(f"aire exacte arrondie (A) : {aire_flottante(ra)} ; accord exact A/B : {ra[1] == rb[1]}")
        ligne(nom, "REJETÉ", ra, rb, ok_extra=(ra[1] == rb[1]), details=det)

    p = list(base)
    p[17] = dec25(Fraction(base[17]) + Fraction(1, 10 ** 6))
    negatif("N1 offset 17 décalé de +1e-6", p)
    p = list(base)
    p[0], p[127] = p[127], p[0]
    negatif("N2 offsets 0 et 127 échangés", p)
    negatif("N3 offsets tous nuls (triangles à base commune)", ["0"] * 128)
    negatif("N4 offsets dans l'ordre inverse", base[::-1])
    negatif("N5 solution intacte, valeur revendiquée abaissée à 0.1067", base, "0.1067")
    plus_bas = repr(math.nextafter(float(REVENDIQUE), 0.0))
    negatif(f"N6 solution intacte, valeur revendiquée un double plus bas ({plus_bas})", base, plus_bas)
    negatif("N7 127 offsets au lieu de 128", base[:127])
    p = list(base)
    p[5] = p[5] + "1"
    negatif("N8 offset 5 à 26 décimales (limite : 25)", p)
    p = list(base)
    p[5] = float(base[5])
    negatif("N9 offset 5 donné comme nombre JSON (flottant) et non comme chaîne", p)
    p = list(base)
    p[5] = "1e-3"
    negatif("N10 offset 5 en notation scientifique '1e-3'", p)
    p = list(base)
    p[5] = "12345.0"
    negatif("N11 offset 5 à 5 chiffres entiers (limite : 4)", p)

    # ---- information : une perturbation sous le grain du double n'est pas détectée par la revendication
    p = list(base)
    p[17] = dec25(Fraction(base[17]) + Fraction(1, 10 ** 25))
    ra, rb = passer(p, REVENDIQUE)
    a0 = passer(base, REVENDIQUE)[0][1]
    ok = ra[0] == "VALIDE" and rb[0] == "VALIDE" and ra[1] == rb[1] and ra[1] != a0
    echecs += 0 if ok else 1
    print(f"{'I1 offset 17 décalé de +1e-25 (information : la valeur revendiquée est un double)':<92} {'accepté':<8} {ra[0]:<8} {rb[0]:<8} {'OK' if ok else 'ÉCHEC'}")
    print(f"    aire exacte modifiée : {ra[1] != a0} ; écart exact = {float(ra[1] - a0):.3e} ; double inchangé : {float(ra[1]) == float(a0)}")

    # ---- positifs
    def positif_exact(nom, chaines, attendue, n):
        ra, rb = passer(chaines, None, n)
        ok = ra[1] == attendue and rb[1] == attendue
        echecs_loc = 0 if ok else 1
        nonlocal echecs
        echecs += echecs_loc
        print(f"{nom:<92} {'accepté':<8} {ra[0]:<8} {rb[0]:<8} {'OK' if ok else 'ÉCHEC'}")
        print(f"    aire exacte A = {ra[1]} ; B = {rb[1]} ; attendue = {attendue}")

    positif_exact("P1 n = 1 : un triangle, aire 1/2", ["0"], Fraction(1, 2), 1)
    positif_exact("P2 n = 2, offsets égaux : aire 3/8 (calcul à la main : 1/4 + 1/4 - 1/8)", ["0", "0"], Fraction(3, 8), 2)
    positif_exact("P3 n = 128, triangles disjoints (offsets 10 j) : somme des aires = 1/2",
                  [str(10 * j) for j in range(1, 129)], Fraction(1, 2), 128)

    ra, rb = passer(base, REVENDIQUE)
    ok = ra[0] == "VALIDE" and rb[0] == "VALIDE" and ra[1] == rb[1]
    echecs += 0 if ok else 1
    print(f"{'P4 solution 2608 intacte, valeur revendiquée ' + REVENDIQUE:<92} {'accepté':<8} {ra[0]:<8} {rb[0]:<8} {'OK' if ok else 'ÉCHEC'}")
    print(f"    aire exacte A = B : {ra[1] == rb[1]}")

    # classement public : chaque score de l'API doit être le double de l'aire exacte recalculée
    aires = []
    for e in api:
        offs = e["data"]["offsets"]
        ra, rb = passer(offs, repr(e["score"]))
        aires.append((e["agentName"], e["id"], ra[1]))
        ok = ra[0] == "VALIDE" and rb[0] == "VALIDE" and ra[1] == rb[1]
        echecs += 0 if ok else 1
        titre = "P5 entrée API id " + str(e["id"]) + " (" + e["agentName"] + ") : double de l'aire exacte = score " + repr(e["score"])
        print(f"{titre:<92} {'accepté':<8} {ra[0]:<8} {rb[0]:<8} {'OK' if ok else 'ÉCHEC'}")
    if len(aires) > 1:
        ordre = all(aires[i][2] < aires[i + 1][2] for i in range(len(aires) - 1))
        echecs += 0 if ordre else 1
        titre = "P5b ordre exact croissant des aires dans la réponse de l'API : " + " < ".join(a[0] for a in aires)
        print(f"{titre:<92} {'accepté':<8} {'-':<8} {'-':<8} {'OK' if ordre else 'ÉCHEC'}")

    # différentiel A/B sur petits n
    alea = random.Random(20261012)
    divergences, total = 0, 0
    for _ in range(80):
        n = alea.randint(2, 8)
        offs =[dec25(Fraction(alea.randint(0, 16), 8)).rstrip("0").rstrip(".") or "0" for _ in range(n)]
        ra, rb = A.evaluer(offs, None, n), B.evaluer(offs, None, n)
        total += 1
        if ra[1] != rb[1] or ra[1] is None:
            divergences += 1
            print(f"    divergence A/B : n={n} offsets={offs} A={ra[1]} B={rb[1]}")
    ok = divergences == 0
    echecs += 0 if ok else 1
    print(f"{'P6 différentiel A/B : ' + str(total) + ' cas aléatoires (n de 2 à 8, offsets en huitièmes), graine 20261012':<92} {'accepté':<8} {'-':<8} {'-':<8} {'OK' if ok else 'ÉCHEC'}")
    print(f"    divergences : {divergences}")

    print(f"\nrésumé : {'tous les contrôles ont l’issue attendue' if echecs == 0 else str(echecs) + ' contrôle(s) en échec'}")
    return 0 if echecs == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
