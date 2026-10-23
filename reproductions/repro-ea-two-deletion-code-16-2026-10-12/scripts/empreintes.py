"""Empreintes d'un fichier : sha256 et sha1 d'objet git (blob). Usage : python -I -X utf8 empreintes.py <fichier> [...]"""
import hashlib
import sys

for chemin in sys.argv[1:]:
    brut = open(chemin, "rb").read()
    blob = hashlib.sha1(b"blob %d\0" % len(brut) + brut).hexdigest()
    print(f"{chemin}\n  octets : {len(brut)}\n  sha256 : {hashlib.sha256(brut).hexdigest()}\n  sha1 d'objet git (blob) : {blob}")
