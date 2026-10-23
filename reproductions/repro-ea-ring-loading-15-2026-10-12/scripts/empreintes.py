"""Empreintes d'un fichier : sha256 (et sha1 d'objet git, blob), puis, pour une liste de soumissions de
l'API EinsteinArena, le sha256 canonique de chaque soumission.

Usage : python -I -X utf8 empreintes.py <fichier> [...]
        python -I -X utf8 empreintes.py --soumissions <best.json>
Forme canonique d'une soumission : json.dumps({"id", "score", "pairs"}, sort_keys=True, separators=(",", ":"),
ensure_ascii=False) encodé en UTF-8. Elle ne dépend ni de l'ordre ni du contenu des autres soumissions de la liste.
"""
import hashlib
import json
import sys


def canonique(s):
    obj = {"id": s["id"], "score": s["score"], "pairs": s["data"]["pairs"]}
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha_soumission(s):
    return hashlib.sha256(canonique(s)).hexdigest()


def main(argv):
    if argv and argv[0] == "--soumissions":
        brut = open(argv[1], "rb").read()
        for s in sorted(json.loads(brut.decode("utf-8")), key=lambda x: x["id"]):
            print(f"{s['id']} {s['agentName']} {s['score']} {sha_soumission(s)}")
        return 0
    for chemin in argv:
        brut = open(chemin, "rb").read()
        blob = hashlib.sha1(b"blob %d\0" % len(brut) + brut).hexdigest()
        print(f"{chemin}\n  octets : {len(brut)}\n  sha256 : {hashlib.sha256(brut).hexdigest()}\n  sha1 d'objet git (blob) : {blob}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
