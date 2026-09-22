import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upropparse import editable_props
from collections import Counter

ENGINE = os.environ.get("PCG_REF_ENGINE", r"C:\Program Files\Epic Games\UE_5.7")
ROOTS = [
    os.path.join(ENGINE, r"Engine\Plugins\PCG\Source"),
    os.path.join(ENGINE, r"Engine\Plugins\PCGInterops"),
    os.path.join(ENGINE, r"Engine\Plugins\Experimental\PCGInterops"),
    os.path.join(ENGINE, r"Engine\Plugins\Experimental\PCGBiomeCore"),
]


def read(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


headers, cpps = [], []
for r in ROOTS:
    for dp, dn, fn in os.walk(r):
        if "Intermediate" in dp or "Binaries" in dp:
            continue
        for f in fn:
            if f.endswith(".h"):
                headers.append(os.path.join(dp, f))
            elif f.endswith(".cpp"):
                cpps.append(os.path.join(dp, f))

htext = {h: read(h) for h in headers}
all_cpp = "\n".join(read(p) for p in cpps)
all_src = all_cpp + "\n" + "\n".join(htext.values())

STR = r'"((?:[^"\\]|\\.)*)"'
STRS = r'((?:\s*' + STR + r')+)'


def join_strs(s):
    return "".join(re.findall(STR, s)).replace('\\"', '"').replace("\\n", " ").strip()


def lit(expr):
    m = re.search(r"NSLOCTEXT\s*\(\s*" + STR + r"\s*,\s*" + STR + r"\s*," + STRS + r"\s*\)", expr, re.S)
    if m:
        return join_strs(m.group(3))
    m = re.search(r"LOCTEXT\s*\(\s*" + STR + r"\s*," + STRS + r"\s*\)", expr, re.S)
    if m:
        return join_strs(m.group(2))
    m = re.search(r"INVTEXT\s*\(" + STRS + r"\s*\)", expr, re.S)
    if m:
        return join_strs(m.group(1))
    m = re.search(r"TEXT\s*\(\s*" + STR + r"\s*\)", expr, re.S)
    if m:
        return m.group(1)
    return None


_const_cache = {}


def resolve_const(name):
    if name in _const_cache:
        return _const_cache[name]
    val = None
    m = re.search(r"\b" + re.escape(name) + r"\s*(?:=|\()\s*((?:NS)?LOCTEXT\s*\(.*?\)|INVTEXT\s*\(.*?\)|TEXT\s*\(.*?\)|FName\s*\(.*?\)\s*\)?)", all_src, re.S)
    if m:
        val = lit(m.group(1))
    _const_cache[name] = val
    return val


def ns_block(ns):
    # return the text of every `namespace <ns> { ... }` block
    blocks = []
    for m in re.finditer(r"namespace\s+" + re.escape(ns) + r"\s*\{", all_src):
        blocks.append(body_of(all_src, m.start()))
    return "\n".join(blocks)


def resolve_scoped(ns, name):
    key = (ns, name)
    if key in _const_cache:
        return _const_cache[key]
    val = None
    src = ns_block(ns) if ns else all_src
    m = re.search(r"\b" + re.escape(name) + r"\s*(?:=|\()\s*((?:NS)?LOCTEXT\s*\(.*?\)|INVTEXT\s*\(.*?\)|TEXT\s*\(.*?\)|FName\s*\(.*?\)\s*\)?)", src, re.S)
    if m:
        val = lit(m.group(1))
    _const_cache[key] = val
    return val


def value_from_body(src):
    if src is None:
        return None
    v = lit(src)
    if v is not None:
        return v
    m = re.search(r"return\s+(?:(\w+)::)?(\w+)\s*;", src)
    if m:
        return resolve_scoped(m.group(1), m.group(2))
    return None


def body_of(text, start):
    i = text.find("{", start)
    if i < 0:
        return ""
    depth = 0
    for j in range(i, len(text)):
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
    return text[i:]


def method_src(cls, body, name):
    m = re.search(r"\b" + name + r"\s*\(\s*\)\s*const\s*(?:override)?\s*(?:final)?\s*\{(.*?)\}", body, re.S)
    if m:
        return m.group(1)
    m = re.search(r"\b" + re.escape(cls) + r"::" + name + r"\s*\(\s*\)\s*const\s*\{(.*?)\n\}", all_cpp, re.S)
    if m:
        return m.group(1)
    return None


def clean_comment(c):
    c = re.sub(r"^\s*/\*\*?|\*/\s*$", "", c.strip())
    lines = [re.sub(r"^\s*\*\s?", "", l).strip() for l in c.split("\n")]
    return " ".join(l for l in lines if l).strip()


# class declarations with their preceding doc comment
decl = re.compile(
    r"(/\*\*(?:(?!\*/).)*\*/\s*)?UCLASS\s*\(((?:[^()]|\([^()]*\))*)\)\s*class\s+"
    r"((?:(?:\w+_API|UE_DEPRECATED\s*\([^)]*\))\s+)*)(U\w+)\s*(?:final\s*)?:\s*public\s+(\w+)",
    re.S,
)
classes = {}
for h, t in htext.items():
    for m in decl.finditer(t):
        doc, spec, mods, cls, base = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        dep = re.search(r'UE_DEPRECATED\s*\(\s*([\d.]+)\s*,\s*"([^"]*)"', mods or "")
        classes[cls] = dict(cls=cls, base=base, spec=" ".join(spec.split()), header=h,
                            body=body_of(t, m.end()), doc=clean_comment(doc) if doc else None,
                            dep_version=dep.group(1) if dep else None, dep_msg=dep.group(2) if dep else None)


def ancestry(c):
    chain = []
    while c in classes and c not in chain:
        chain.append(c)
        c = classes[c]["base"]
    chain.append(c)
    return chain


def is_settings(c):
    return "UPCGSettings" in ancestry(c)




def props_of(body):
    return editable_props(body)


def pins_of(cls, body, which):
    src = method_src(cls, body, which) or ""
    types = re.findall(r"EPCGDataType(?:Identifier)?::(\w+)|FPCGDataTypeInfo(\w+)::AsId", src)
    types = [a or b for a, b in types]
    labels = re.findall(r"PCGPinConstants::(\w+)", src)
    return dict(types=sorted(set(types)), labels=sorted(set(labels)))


out = []
for cls, d in classes.items():
    if cls == "UPCGSettings" or not is_settings(cls):
        continue
    chain = ancestry(cls)

    def inherit(fn):
        for c in chain:
            if c not in classes:
                continue
            v = fn(c)
            if v:
                return v, c
        return None, None

    title, title_from = inherit(lambda c: value_from_body(method_src(c, classes[c]["body"], "GetDefaultNodeTitle")))
    name, _ = inherit(lambda c: value_from_body(method_src(c, classes[c]["body"], "GetDefaultNodeName")))
    tip, tip_from = inherit(lambda c: value_from_body(method_src(c, classes[c]["body"], "GetNodeTooltipText")))
    typ, _ = inherit(lambda c: (lambda s: (re.search(r"EPCGSettingsType::(\w+)", s).group(1)
                                            if s and re.search(r"EPCGSettingsType::(\w+)", s) else None))(
        method_src(c, classes[c]["body"], "GetType")))
    if title_from and title_from != cls:
        title = None  # a base title is not this node's title
    if not title and name:
        title = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)
    if not title:
        title = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", re.sub(r"^U(PCG)?|Settings$|ElementSettings$", "", cls))
    if tip_from and tip_from != cls:
        tip_note = "inherited from " + tip_from
    else:
        tip_note = None
    if not tip and d["doc"]:
        tip = d["doc"]
        tip_note = "class comment"

    spec = d["spec"]
    hp = d["header"].replace(os.sep, "/")
    rel = hp.split("Engine/Plugins/")[-1]
    parts = rel.split("/")
    plugin = parts[0] if parts[0] != "Experimental" else parts[0] + "/" + parts[1]
    kw = re.search(r'Keywords\s*=\s*"([^"]*)"', spec)

    # props: own + ancestors below UPCGSettings
    props = []
    for c in chain:
        if c == "UPCGSettings" or c not in classes:
            break
        for p in props_of(classes[c]["body"]):
            p["from"] = c
            props.append(p)

    out.append(dict(
        cls=cls, base=d["base"], name=name, title=title, tooltip=tip, tooltip_note=tip_note, type=typ,
        abstract="Abstract" in spec,
        hidden=bool(re.search(r"\bHidden\b|HideDropdown|NotPlaceable", spec)),
        deprecated=("Deprecated" in spec) or cls.startswith("UDEPRECATED") or bool(d.get("dep_version")),
        dep_version=d.get("dep_version"), dep_msg=d.get("dep_msg"),
        keywords=kw.group(1) if kw else None,
        plugin=plugin, header=rel,
        inputs=pins_of(cls, d["body"], "InputPinProperties"),
        outputs=pins_of(cls, d["body"], "OutputPinProperties"),
        props=props,
    ))

out.sort(key=lambda x: ((x["type"] or "zz"), (x["title"] or x["cls"])))
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("settings nodes", len(out))
print("abstract", sum(o["abstract"] for o in out), "hidden", sum(o["hidden"] for o in out),
      "deprecated", sum(o["deprecated"] for o in out))
print("title", sum(1 for o in out if o["title"]), "tooltip", sum(1 for o in out if o["tooltip"]),
      "type", sum(1 for o in out if o["type"]), "props total", sum(len(o["props"]) for o in out))
print(Counter(o["type"] for o in out).most_common())
print(Counter(o["plugin"] for o in out).most_common())
