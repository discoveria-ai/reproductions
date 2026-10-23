"""Rejeu complet : extraction, moteurs A et B, témoins, quantité exacte, contrôles. Écrit les sorties dans un dossier.

Usage : python -I -X utf8 rejouer.py <reponse-api-best.json> <problem.json> <dossier-de-sortie>
  reponse-api-best.json : GET https://einsteinarena.com/api/solutions/best?problem_id=26&limit=4 (ou limit=1)
  problem.json          : GET https://einsteinarena.com/api/problems/kakeya-needle-128
  dossier-de-sortie     : un dossier à part (sinon artefacts/*.out serait réécrit alors que leurs empreintes
                          sont gravées dans rapport.json)

Refuse de rejouer si la forme canonique des 128 offsets de la solution 2608 n'a pas le sha256 épinglé (code 3).
Code de sortie 0 seulement si toutes les étapes sont conformes. Les offsets canoniques sont écrits dans un
dossier temporaire supprimé à la fin : la solution n'est pas conservée.
"""

import hashlib
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SHA256_CANONIQUE = "8a9e475f2c54b96d21b6bb385b04d55d559029a9ad96b83e92eddb9173609c29"
ID_SOLUTION = "2608"
REVENDIQUE = "0.10675394011230244"
ICI = Path(__file__).resolve().parent


def lancer(args):
    p = subprocess.run([sys.executable, "-B", "-I", "-X", "utf8", *map(str, args)], capture_output=True)
    return p.returncode, p.stdout.decode("utf-8") + p.stderr.decode("utf-8")


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    best, probleme, sortie = (Path(a).resolve() for a in argv)
    sortie.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    with tempfile.TemporaryDirectory() as tmp:
        offsets = Path(tmp) / "offsets.txt"
        code, texte = lancer([ICI / "extraire.py", best, ID_SOLUTION, offsets])
        (sortie / "sortie_extraction.out").write_text(texte + f"[code de sortie {code}]\n", encoding="utf-8", newline="\n")
        print(f"sortie_extraction.out : code de sortie {code}")
        if code != 0:
            return 1
        h = hashlib.sha256(offsets.read_bytes()).hexdigest()
        if h != SHA256_CANONIQUE:
            print(f"REFUS : sha256 canonique {h} différent de l'empreinte épinglée {SHA256_CANONIQUE}")
            return 3
        print(f"sha256 canonique des offsets : {h} (conforme)")
        codes = [code]
        fraction_a = None
        etapes = [
            ("sortie_moteur_a.out", [ICI / "verif_a.py", offsets, REVENDIQUE]),
            ("sortie_moteur_b.out", [ICI / "verif_b.py", offsets, REVENDIQUE]),
        ]
        for nom, args in etapes:
            code, texte = lancer(args)
            (sortie / nom).write_text(texte + f"[code de sortie {code}]\n", encoding="utf-8", newline="\n")
            print(f"{nom} : code de sortie {code}")
            codes.append(code)
            if nom == "sortie_moteur_a.out":
                m = re.search(r"fraction (\d+/\d+)", texte)
                fraction_a = m.group(1) if m else None
        if fraction_a is None:
            print("ÉCHEC : fraction exacte du moteur A introuvable")
            return 1
        suite = [
            ("sortie_temoin_plateforme.out", [ICI / "temoin_plateforme.py", probleme, offsets, fraction_a]),
            ("sortie_temoin_flottant.out", [ICI / "temoin_flottant.py", offsets]),
            ("sortie_quantite.out", [ICI / "quantite.py", offsets, ICI]),
            ("sortie_controles.out", [ICI / "controles.py", offsets, best, ICI]),
        ]
        for nom, args in suite:
            code, texte = lancer(args)
            (sortie / nom).write_text(texte + f"[code de sortie {code}]\n", encoding="utf-8", newline="\n")
            print(f"{nom} : code de sortie {code}")
            codes.append(code)
    print(f"durée murale : {time.monotonic() - t0:.2f} s")
    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
