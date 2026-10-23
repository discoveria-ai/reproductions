"""Rejeu complet : moteur A, moteur B, contrôles négatifs/positifs. Écrit les sorties dans artefacts/.

Usage : python -I -X utf8 scripts/rejouer.py <solution_n=604_d=11.json> [<dossier-de-sortie>]

Refuse de rejouer si le sha256 du fichier diffère de celui épinglé (code 3). Code de sortie 0 seulement si
les moteurs A et B valident la solution ET si tous les contrôles sont conformes.
"""

import hashlib
import subprocess
import sys
import time
from pathlib import Path

SHA256_ATTENDU = "0bde9ca2c434d7beb5af63a64a291498e8c264d9a5718b738e92dd70b9ba7761"
ICI = Path(__file__).resolve().parent


def lancer(args):
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", *map(str, args)], capture_output=True)
    return p.returncode, p.stdout.decode("utf-8") + p.stderr.decode("utf-8")


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    sol = Path(argv[0]).resolve()
    sortie = Path(argv[1]).resolve() if len(argv) > 1 else ICI.parent / "artefacts"
    sortie.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256(sol.read_bytes()).hexdigest()
    if h != SHA256_ATTENDU:
        print(f"REFUS : sha256 {h} différent de l'empreinte épinglée {SHA256_ATTENDU}")
        return 3
    t0 = time.monotonic()
    etapes = [
        ("sortie_moteur_a.out", [ICI / "verif_a.py", sol]),
        ("sortie_moteur_b.out", [ICI / "verif_b.py", sol]),
        ("sortie_controles.out", [ICI / "controles.py", sol, ICI]),
        ("sortie_statistiques.out", [ICI / "statistiques.py", sol]),
    ]
    codes = []
    for nom, args in etapes:
        code, texte = lancer(args)
        (sortie / nom).write_text(texte + f"[code de sortie {code}]\n", encoding="utf-8", newline="\n")
        print(f"{nom} : code de sortie {code}")
        codes.append(code)
    print(f"sha256 de la solution : {h} (conforme)")
    print(f"durée murale : {time.monotonic() - t0:.2f} s")
    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
