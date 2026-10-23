"""Rejeu complet : moteur A, moteur B, contrôles, vérificateur public de la plateforme. Écrit les sorties dans un dossier.

Usage : python -I -X utf8 scripts/rejouer.py <solutions_best_problem34_limit4.json> <problem_two-deletion-code-16.json> [<dossier-de-sortie>]

Épinglage : la réponse de l'API change à chaque nouvelle soumission, donc ce n'est pas elle qu'on épingle mais la liste
des 219 mots de la solution d'id 2605 (sha256 des mots, un par ligne, ordre du fichier, saut de ligne final) ; le texte du
vérificateur est épinglé par verif_plateforme.py. Tout écart : refus, code 3. La réponse à utiliser peut donc être n'importe
quel téléchargement de /api/solutions/best?problem_id=34&limit=N (N >= 1 tant que la solution 2605 reste première ou dans les N).
Code de sortie 0 seulement si les moteurs A et B valident la solution, si tous les contrôles sont conformes et si le
vérificateur de la plateforme l'accepte.
"""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

IDENT = 2605
SHA256_MOTS = "f8ac54a8b0910350a896e9524e6f74b753124d788b52ac0618ab6de34a13755b"
SHA256_REPONSE_RELEVEE = "8fece05aec4a8ed9f4aac3b7078ad4f82f6b7e66ef9b4adc214077e835bea218"
ICI = Path(__file__).resolve().parent


def lancer(args):
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", *map(str, args)], capture_output=True)
    return p.returncode, p.stdout.decode("utf-8") + p.stderr.decode("utf-8")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    sol, prob = Path(argv[0]).resolve(), Path(argv[1]).resolve()
    sortie = Path(argv[2]).resolve() if len(argv) > 2 else ICI.parent / "artefacts"
    sortie.mkdir(parents=True, exist_ok=True)
    try:
        cible = [s for s in json.loads(sol.read_bytes().decode("utf-8")) if isinstance(s, dict) and s.get("id") == IDENT]
        mots = cible[0]["data"]["words"]
        h = hashlib.sha256(("\n".join(mots) + "\n").encode("utf-8")).hexdigest()
    except (ValueError, IndexError, KeyError, TypeError) as e:
        print(f"REFUS : solution d'id {IDENT} introuvable ou mal formée dans {sol} : {e}")
        return 3
    if h != SHA256_MOTS:
        print(f"REFUS : sha256 de la liste de mots {h} différent de l'empreinte épinglée {SHA256_MOTS}")
        return 3
    print(f"sha256 de la liste des {len(mots)} mots de la solution {IDENT} : {h} (conforme)")
    print(f"(info) sha256 du fichier de réponse : {hashlib.sha256(sol.read_bytes()).hexdigest()} ; relevé le 2026-10-12 : {SHA256_REPONSE_RELEVEE}")
    t0 = time.monotonic()
    etapes = [
        ("sortie_moteur_a.out", [ICI / "verif_a.py", sol]),
        ("sortie_moteur_b.out", [ICI / "verif_b.py", sol]),
        ("sortie_controles.out", [ICI / "controles.py", sol, ICI]),
        ("sortie_plateforme.out", [ICI / "verif_plateforme.py", prob, sol]),
    ]
    codes = []
    for nom, args in etapes:
        code, texte = lancer(args)
        (sortie / nom).write_text(texte + f"[code de sortie {code}]\n", encoding="utf-8", newline="\n")
        print(f"{nom} : code de sortie {code}")
        codes.append(code)
    print(f"durée murale : {time.monotonic() - t0:.2f} s")
    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
