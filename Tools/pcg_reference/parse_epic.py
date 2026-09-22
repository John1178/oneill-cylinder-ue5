"""Refresh the cached Epic node reference.

1. Open https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine
   in a browser and save the page text (the page renders client-side, so a plain HTTP fetch returns nothing).
   The capture is a JSON list [{"type": "text", "text": ...}] or a plain string.
2. python parse_epic.py <capture.json> epic_nodes.json
"""
import json, re, sys

src = sys.argv[1]
raw = json.load(open(src, encoding="utf-8"))
text = raw[0]["text"] if isinstance(raw, list) else raw
text = text.split("---", 1)[1] if "---" in text else text

SEP = "\n\n\t\n\n"
chunks = text.split(SEP)

entries = []
category = None


def split_tail(chunk):
    """Return (body_before_last_para, last_para, category_or_None)."""
    paras = chunk.split("\n\n")
    last = paras[-1].strip()
    cat = None
    # a category header looks like "Category Name\nNode\tDescription\n\nNodeName" -> handled across paras
    if len(paras) >= 2 and paras[-2].strip().endswith("Node\tDescription"):
        head = paras[-2].strip().split("\n")
        cat = head[0].strip() if len(head) >= 2 else None
        body = paras[:-2]
    else:
        body = paras[:-1]
    return "\n\n".join(p.strip() for p in body if p.strip()), last, cat


# first chunk: intro + first category + first node name
body0, name0, cat0 = split_tail(chunks[0])
category = cat0
pending = name0

for ch in chunks[1:]:
    desc, nxt, cat = split_tail(ch)
    entries.append(dict(category=category, node=pending, description=desc))
    if cat:
        category = cat
    pending = nxt

# last chunk: its tail is just trailing page text, the whole thing is the last description
last_desc = chunks[-1].strip()
entries[-1]["description"] = entries[-1]["description"] or last_desc

# trim page footer noise from the final description
for e in entries:
    e["description"] = re.split(r"\n(?:Tags|Ask questions and help your peers|提问并帮助你的同行)", e["description"])[0].strip()

json.dump(entries, open(sys.argv[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
from collections import Counter
print("entries", len(entries))
print(Counter(e["category"] for e in entries).most_common())
for e in entries[:4]:
    print("-", e["category"], "|", e["node"], "|", e["description"][:80])
print("...")
for e in entries[-3:]:
    print("-", e["category"], "|", e["node"], "|", e["description"][:80])
