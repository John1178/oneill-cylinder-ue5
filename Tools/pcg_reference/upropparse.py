import re


def _match_paren(text, k):
    """text[k] == '('. Return index of the matching ')', skipping quoted strings."""
    depth, quoted, p = 0, False, k
    n = len(text)
    while p < n:
        c = text[p]
        if c == '"' and (p == 0 or text[p - 1] != "\\"):
            quoted = not quoted
        elif not quoted:
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    return p
        p += 1
    return n - 1


def _clean_comment(c):
    c = c.strip()
    if c.startswith("/*"):
        c = re.sub(r"^/\*\*?|\*/$", "", c)
        lines = [re.sub(r"^\s*\*\s?", "", l).strip() for l in c.split("\n")]
    else:
        lines = [l.strip().lstrip("/").strip() for l in c.split("\n")]
    return " ".join(l for l in lines if l).strip() or None


DOC_TAIL = re.compile(r"(/\*\*(?:(?!\*/).)*\*/\s*|(?:[ \t]*//[^\n]*\n\s*)+)$", re.S)


def iter_uproperties(body):
    """Yield dicts for every UPROPERTY in a class/struct body."""
    i = 0
    while True:
        j = body.find("UPROPERTY", i)
        if j < 0:
            return
        k = body.find("(", j)
        if k < 0:
            return
        e = _match_paren(body, k)
        spec = " ".join(body[k + 1:e].split())
        semi = body.find(";", e)
        if semi < 0:
            return
        decl = " ".join(body[e + 1:semi].split())
        i = semi + 1
        pre = body[max(0, j - 2000):j]
        dm = DOC_TAIL.search(pre)
        doc = _clean_comment(dm.group(1)) if dm else None
        # decl: "Type Name = default" | "Type Name{...}" | "Type Name"
        dd = re.match(r"^(.+?)\s+(\w+)\s*(?:=\s*(.+)|(\{.*\}))?$", decl)
        if not dd:
            continue
        typ, name = dd.group(1), dd.group(2)
        default = dd.group(3) or dd.group(4)
        yield dict(spec=spec, type=typ, name=name, default=default, doc=doc)


def editable_props(body):
    out = []
    for u in iter_uproperties(body):
        spec = u["spec"]
        if not re.search(r"Edit(Anywhere|DefaultsOnly|InstanceOnly)", spec):
            continue
        tt = re.search(r'ToolTip\s*=\s*"([^"]*)"', spec)
        dn = re.search(r'DisplayName\s*=\s*"([^"]*)"', spec)
        ec = re.search(r'EditCondition\s*=\s*"([^"]*)"', spec)
        cat = re.search(r'Category\s*=\s*"([^"]*)"', spec) or re.search(r"Category\s*=\s*([\w|]+)", spec)
        out.append(dict(
            name=u["name"],
            display=dn.group(1) if dn else None,
            type=u["type"],
            default=u["default"],
            tooltip=tt.group(1) if tt else u["doc"],
            edit_condition=ec.group(1) if ec else None,
            overridable="PCG_Overridable" in spec,
            category=cat.group(1).strip() if cat else None,
            advanced="AdvancedDisplay" in spec,
        ))
    return out
