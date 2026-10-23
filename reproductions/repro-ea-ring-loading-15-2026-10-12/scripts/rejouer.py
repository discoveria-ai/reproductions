"""Rejeu complet : moteur A, moteur B, contrôles négatifs/positifs. Écrit les sorties dans artefacts/.

Usage : python -I -X utf8 -B scripts/rejouer.py <best.json> <problem.json> [<dossier-de-sortie>]
  best.json    : réponse de GET https://einsteinarena.com/api/solutions/best?problem_id=30&limit=10
  problem.json : réponse de GET https://einsteinarena.com/api/problems/ring-loading-15

Refuse de rejouer (code 3) si une des 7 soumissions listées ci-dessous n'a pas le sha256 canonique épinglé
(forme canonique : voir empreintes.py ; elle ne dépend pas des soumissions plus récentes qui apparaîtraient dans la
liste), ou si problem.json n'a pas le sha256 épinglé. Code de sortie 0 seulement si les moteurs A et B valident la
soumission 2576 à 9/8 ET si tous les contrôles sont conformes.
Sans dossier de sortie, artefacts/*.out serait réécrit alors que leurs empreintes sont gravées dans rapport.json.
"""

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ICI = Path(__file__).resolve().parent
PROBLEME_SHA256 = "49f4427e30688fa67b37a10e50f1b33d6656d32cb00a67d9f1b50fed73bf5a9a"
SOUMISSIONS = {
    2566: "7966364ba27eab8177b1ce769f495e3c439468d88d4bc20a502ccc75f16db4bb",
    2569: "6aa4d43d5e987afe4c2f2adf6059035bbc5714b4908a1a550fdcba5a123a2211",
    2573: "551a21a8ae65c888d4e9205b1f0f12aabac11df660a79d39e8844c9e7e42d1bc",
    2574: "5c28d1d7a0697cd85efc5ac06b8c59880de29d5446aa35e8c180e4c7d207a2e8",
    2576: "3b9d1e3a1278889d29d6120e13db84a6cd45e20c4d2601f98c77a3c412425e80",
    2592: "507eae79a16aa753c3fa41881745ee8d61f4af9f2813c753117e207a1ea188f0",
    2593: "cd2e833d4dd8ad8619cfb68c183f57b5f270324d5c50c69b8769a948e97c58b6",
}


def charger_empreintes():
    spec = importlib.util.spec_from_file_location("empreintes", ICI / "empreintes.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def lancer(args):
    p = subprocess.run([sys.executable, "-B", "-I", "-X", "utf8", *map(str, args)], capture_output=True)
    return p.returncode, p.stdout.decode("utf-8") + p.stderr.decode("utf-8")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    best, probleme = Path(argv[0]).resolve(), Path(argv[1]).resolve()
    sortie = Path(argv[2]).resolve() if len(argv) > 2 else ICI.parent / "artefacts"
    sortie.mkdir(parents=True, exist_ok=True)
    emp = charger_empreintes()
    liste = {s["id"]: s for s in json.loads(best.read_bytes().decode("utf-8"))}
    for ident, attendu in SOUMISSIONS.items():
        if ident not in liste or emp.sha_soumission(liste[ident]) != attendu:
            print(f"REFUS : soumission {ident} absente ou différente de l'empreinte canonique épinglée {attendu}")
            return 3
    hp = hashlib.sha256(probleme.read_bytes()).hexdigest()
    if hp != PROBLEME_SHA256:
        print(f"REFUS : sha256 de problem.json {hp} différent de l'empreinte épinglée {PROBLEME_SHA256}")
        return 3
    t0 = time.monotonic()
    etapes = [
        ("sortie_moteur_a.out", [ICI / "verif_a.py", best, "--id", 2576, "--attendu", "9/8"]),
        ("sortie_moteur_b.out", [ICI / "verif_b.py", best, "--id", 2576, "--attendu", "9/8"]),
        ("sortie_controles.out", [ICI / "controles.py", best, ICI]),
    ]
    codes = []
    for nom, args in etapes:
        code, texte = lancer(args)
        (sortie / nom).write_text(texte + f"[code de sortie {code}]\n", encoding="utf-8", newline="\n")
        print(f"{nom} : code de sortie {code}")
        codes.append(code)
    print(f"sha256 canoniques des 7 soumissions : conformes ; sha256 de problem.json : {hp} (conforme)")
    print(f"sha256 du fichier best.json lu : {hashlib.sha256(best.read_bytes()).hexdigest()} (information)")
    print(f"durée murale : {time.monotonic() - t0:.2f} s")
    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
