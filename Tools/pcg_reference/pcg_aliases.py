import os, re, json, sys

ENGINE = os.environ.get("PCG_REF_ENGINE", r"C:\Program Files\Epic Games\UE_5.7")
ROOTS = [
    os.path.join(ENGINE, r"Engine\Plugins\PCG\Source"),
    os.path.join(ENGINE, r"Engine\Plugins\PCGInterops"),
    os.path.join(ENGINE, r"Engine\Plugins\Experimental\PCGInterops"),
]


def read(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except Exception:
        return ""


hs, cs = [], []
for r in ROOTS:
    for dp, dn, fn in os.walk(r):
        if "Intermediate" in dp:
            continue
        for f in fn:
            (hs if f.endswith(".h") else cs if f.endswith(".cpp") else []).append(os.path.join(dp, f))

H = "\n".join(read(p) for p in hs)
C = "\n".join(read(p) for p in cs)

STR = r'"((?:[^"\\]|\\.)*)"'


def body_after(text, start):
    i = text.find("{", start)
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i:j + 1]
    return text[i:]


# enums: name -> [(value, display, tooltip, hidden)]
def split_top(s):
    parts, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        parts.append("".join(cur))
    return parts


enums = {}
for m in re.finditer(r"enum\s+class\s+(\w+)\s*(?::\s*\w+)?\s*\{", H):
    name = m.group(1)
    if name in enums:
        continue
    body = body_after(H, m.start())[1:-1]
    vals = []
    for piece in split_top(body):
        # leading comments on this entry become its tooltip
        doc_lines = []
        code_lines = []
        for line in piece.split("\n"):
            s = line.strip()
            if s.startswith("//"):
                doc_lines.append(s.lstrip("/").strip())
            elif s:
                code_lines.append(s)
        code = " ".join(code_lines)
        code = re.sub(r"/\*\*?(.*?)\*/", lambda mm: (doc_lines.append(mm.group(1).strip()) or ""), code, flags=re.S)
        mm = re.match(r"\s*(\w+)", code)
        if not mm:
            continue
        val = mm.group(1)
        meta_m = re.search(r"UMETA\s*\(((?:[^()]|\([^()]*\))*)\)", code)
        meta = meta_m.group(1) if meta_m else ""
        dn = re.search(r'DisplayName\s*=\s*"([^"]*)"', meta)
        tt = re.search(r'ToolTip\s*=\s*"([^"]*)"', meta, re.I)
        tip = tt.group(1) if tt else (" ".join(d for d in doc_lines if d) or None)
        vals.append(dict(value=val,
                         display=dn.group(1) if dn else re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", val),
                         tooltip=tip, hidden=bool(re.search(r"\bHidden\b", meta))))
    enums[name] = vals

out = {}
for m in re.finditer(r"(U\w+)::GetPreconfiguredInfo\s*\(\s*\)\s*const\s*\{", C):
    cls = m.group(1)
    body = body_after(C, m.start())
    entry = dict(enum=None, excluded=[], explicit=[])
    pe = re.search(r"PopulateFromEnum<(\w+)>\s*\((.*?)\)\s*;", body, re.S)
    if pe:
        entry["enum"] = pe.group(1)
        entry["excluded"] = re.findall(re.escape(pe.group(1)) + r"::(\w+)", pe.group(2))
    for lm in re.finditer(r"LOCTEXT\s*\(\s*" + STR + r"\s*,\s*" + STR + r"\s*\)", body):
        entry["explicit"].append(lm.group(2))
    if entry["enum"]:
        vals = enums.get(entry["enum"], [])
        entry["values"] = [v for v in vals if v["value"] not in entry["excluded"] and not v["hidden"]
                           and v["value"] not in ("MAX", "Count", "Num") and not v["value"].endswith("_MAX")]
    out[cls] = entry

json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(enums, open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "pcg_enums.json"), "w",
                      encoding="utf-8"), indent=1, ensure_ascii=False)
print("enums saved:", len(enums))
print("classes with aliases:", len(out))
for k, v in out.items():
    n = len(v.get("values", [])) if v["enum"] else 0
    print(f"  {k:44s} enum={v['enum'] or '-':34s} values={n:3d} explicit={v['explicit']}")
