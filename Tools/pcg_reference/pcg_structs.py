import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upropparse import editable_props

ENGINE = os.environ.get("PCG_REF_ENGINE", r"C:\Program Files\Epic Games\UE_5.7")
ROOTS = [
    os.path.join(ENGINE, r"Engine\Plugins\PCG\Source"),
    os.path.join(ENGINE, r"Engine\Plugins\PCGInterops"),
    os.path.join(ENGINE, r"Engine\Plugins\Experimental\PCGInterops"),
    os.path.join(ENGINE, r"Engine\Plugins\Runtime\GeometryScripting\Source\GeometryScriptingCore\Public"),
]


def read(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


def body_of(text, start):
    i = text.find("{", start)
    if i < 0:
        return ""
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
    return text[i:]


def clean_comment(c):
    c = re.sub(r"^\s*/\*\*?|\*/\s*$", "", c.strip())
    lines = [re.sub(r"^\s*\*\s?", "", l).strip() for l in c.split("\n")]
    return " ".join(l for l in lines if l).strip()




def props_of(body):
    return editable_props(body)




structs = {}
rx = re.compile(r"USTRUCT\s*\(((?:[^()]|\([^()]*\))*)\)\s*struct\s+(?:\w+_API\s+)?(F\w+)\s*(?::\s*public\s+(\w+))?", re.S)
for r in ROOTS:
    for dp, dn, fn in os.walk(r):
        if "Intermediate" in dp:
            continue
        for f in fn:
            if not f.endswith(".h"):
                continue
            t = read(os.path.join(dp, f))
            for m in rx.finditer(t):
                name = m.group(2)
                if name in structs:
                    continue
                structs[name] = dict(base=m.group(3), fields=props_of(body_of(t, m.end())))

# fold base-struct fields in
for name, s in structs.items():
    b = s["base"]
    seen = set()
    while b and b in structs and b not in seen:
        seen.add(b)
        s["fields"] = structs[b]["fields"] + s["fields"]
        b = structs[b]["base"]

json.dump(structs, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("structs", len(structs), "with fields", sum(1 for s in structs.values() if s["fields"]))
for k in ("FGeometryScriptMeshPointSamplingOptions", "FPCGActorSelectorSettings", "FPCGAttributePropertyInputSelector"):
    s = structs.get(k)
    print(k, "->", [f["name"] for f in s["fields"]] if s else "MISSING")
