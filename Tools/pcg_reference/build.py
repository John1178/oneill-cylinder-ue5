"""Rebuild docs/pcg_nodes.md from the installed engine source.

    python Tools/pcg_reference/build.py

Steps: scan node classes -> aliases + enums -> structs -> list PCGBiomeCore assets -> write the doc.
Epic's descriptions come from the cached epic_nodes.json (see parse_epic.py to refresh it).
"""
import os, subprocess, sys

ENGINE = r"C:\Program Files\Epic Games\UE_5.7"   # change after an engine upgrade

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(PROJECT, "docs", "pcg_nodes.md")
env = dict(os.environ, PCG_REF_ENGINE=ENGINE)


def run(*args):
    print(">", " ".join(args))
    subprocess.run([sys.executable, *args], cwd=HERE, env=env, check=True)


run("pcg_scan.py", "pcg_nodes2.json")
run("pcg_aliases.py", "pcg_aliases.json")      # also writes pcg_enums.json
run("pcg_structs.py", "pcg_structs.json")

content = os.path.join(ENGINE, "Engine", "Plugins", "Experimental", "PCGBiomeCore", "Content")
assets = []
for dp, dn, fn in os.walk(content):
    for f in fn:
        if f.endswith(".uasset"):
            assets.append(os.path.relpath(os.path.join(dp, f), content).replace(os.sep, "/"))
with open(os.path.join(HERE, "biome_assets.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(sorted(assets)) + "\n")
print("biome assets:", len(assets))

run("gen_doc.py", DOC)
print("done ->", DOC)
