"""Extrait les 128 offsets d'une solution de la réponse JSON de l'API EinsteinArena et les écrit en forme canonique.

Forme canonique : les chaînes décimales dans l'ordre, une par ligne, séparées par LF, avec un LF final, en ASCII.
Cette forme est ce que le sha256 épinglé désigne (la réponse brute de l'API bouge avec le classement).

Usage : python -I -X utf8 extraire.py <reponse-api.json> <id-solution> <sortie-offsets.txt>
Écrit aussi sur la sortie standard : id, agent, date, score de l'API, sha256 de la forme canonique.
Code de sortie : 0 = écrit ; 1 = solution absente ou malformée ; 2 = usage.
"""

import hashlib
import json
import sys


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    brut = open(argv[0], "rb").read()
    entrees = json.loads(brut.decode("utf-8"))
    trouvees = [e for e in entrees if isinstance(e, dict) and e.get("id") == int(argv[1])]
    if len(trouvees) != 1:
        print(f"ÉCHEC : {len(trouvees)} entrée(s) d'id {argv[1]} dans {argv[0]}")
        return 1
    e = trouvees[0]
    offsets = e.get("data", {}).get("offsets")
    if not isinstance(offsets, list) or not all(isinstance(s, str) and s.isascii() and "\n" not in s for s in offsets):
        print("ÉCHEC : data.offsets n'est pas une liste de chaînes ASCII")
        return 1
    canon = ("\n".join(offsets) + "\n").encode("ascii")
    open(argv[2], "wb").write(canon)
    print(f"id : {e['id']}")
    print(f"agent : {e.get('agentName')}")
    print(f"createdAt : {e.get('createdAt')}")
    print(f"score de l'API : {e.get('score')!r}")
    print(f"nombre d'offsets : {len(offsets)}")
    print(f"sha256 de la forme canonique : {hashlib.sha256(canon).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
