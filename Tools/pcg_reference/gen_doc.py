import json, re, os, sys
from collections import defaultdict, OrderedDict

SP = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]

nodes = json.load(open(os.path.join(SP, "pcg_nodes2.json"), encoding="utf-8"))
aliases = json.load(open(os.path.join(SP, "pcg_aliases.json"), encoding="utf-8"))
enums = json.load(open(os.path.join(SP, "pcg_enums.json"), encoding="utf-8"))
epic = json.load(open(os.path.join(SP, "epic_nodes.json"), encoding="utf-8"))
biome = [l.strip() for l in open(os.path.join(SP, "biome_assets.txt"), encoding="utf-8") if l.strip()]
structs = json.load(open(os.path.join(SP, "pcg_structs.json"), encoding="utf-8"))


def struct_of(t):
    m = re.match(r"^\s*(?:const\s+)?(F\w+)\s*$", t)
    if not m:
        return None
    s = structs.get(m.group(1))
    if not s or not s["fields"] or len(s["fields"]) > 16:
        return None
    return m.group(1), s["fields"]

norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())

OPCATS = {
    "Attribute Maths Op": "UPCGMetadataMathsSettings",
    "Attribute Rotator Op": "UPCGMetadataRotatorSettings",
    "Attribute Vector Op": "UPCGMetadataVectorSettings",
    "Attribute Boolean Op": "UPCGMetadataBooleanSettings",
    "Attribute Trig Op": "UPCGMetadataTrigSettings",
    "Attribute Compare Op": "UPCGMetadataCompareSettings",
    "Attribute Bitwise Op": "UPCGMetadataBitwiseSettings",
    "Attribute Reduce Op": "UPCGAttributeReduceSettings",
    "Attribute Transform Op": "UPCGMetadataTransformSettings",
}
epic_nodes = {}
epic_ops = defaultdict(dict)
epic_uncat = {}
for e in epic:
    if e["category"] in OPCATS:
        epic_ops[OPCATS[e["category"]]][norm(e["node"])] = e["description"]
    elif e["category"] == "Uncategorized":
        epic_uncat[norm(e["node"])] = e
    else:
        epic_nodes[norm(e["node"])] = e
# reroute helpers from Epic's "Uncategorized" block
UNCAT_MAP = {
    "UPCGRerouteSettings": "addreroutenode",
    "UPCGNamedRerouteDeclarationSettings": "addnamedreroutedeclarationnode",
}

CAT_NAME = {
    "Sampler": "Sampler", "Spatial": "Spatial", "PointOps": "Point Ops", "Filter": "Filter",
    "Metadata": "Metadata (attributes)", "Param": "Param (attribute sets)", "Spawner": "Spawner",
    "ControlFlow": "Control Flow", "Subgraph": "Subgraph", "GraphParameters": "Graph Parameters",
    "InputOutput": "Input / Output", "Generic": "Generic", "DynamicMesh": "Dynamic Mesh", "GPU": "GPU",
    "Debug": "Debug", "Reroute": "Reroute", "Resource": "Resource", "DataLayers": "Data Layers",
    "Blueprint": "Blueprint", "Density": "Density", "HierarchicalGeneration": "Hierarchical Generation",
}
CAT_ORDER = ["Sampler", "Spatial", "PointOps", "Filter", "Metadata", "Param", "Spawner", "ControlFlow",
             "Subgraph", "GraphParameters", "InputOutput", "Generic", "DynamicMesh", "GPU", "Debug", "Reroute",
             "Resource", "DataLayers", "Blueprint", "Density", "HierarchicalGeneration"]


def subplugin(n):
    parts = n["header"].split("/")
    if parts[0] == "PCG":
        return "PCG"
    if parts[0] == "PCGInterops":
        return parts[1]
    if parts[0] == "Experimental" and len(parts) > 2:
        return parts[2]
    return n["plugin"]


MATURITY = {
    "PCG": "", "PCGGeometryScriptInterop": "β", "PCGPythonInterop": "β", "PCGExternalDataInterop": "β",
    "PCGFastGeoInterop": "🧪", "PCGInstancedActorsInterop": "🧪", "PCGNaniteAssembliesInterop": "🧪",
    "PCGNiagaraInterop": "🧪", "PCGWaterInterop": "🧪",
}

# nodes this project uses or plans to use -> short note (facts only, see section 8)
PROJECT = {
    "UPCGMeshSamplerSettings": "L0 sampler in `SG_SurfaceSource`",
    "UPCGDataFromActorSettings": "L0 — finds the surface actor by tag",
    "UPCGCopyPointsSettings": "L0 — places mesh-local points on the actor",
    "UPCGUserParameterGetSettings": "L0 — reads the 8 subgraph parameters",
    "UPCGTransformPointsSettings": "`PCG_SurfaceTest`",
    "UPCGLoadDataTableSettings": "`PCG_SurfaceTest` — `DT_Modules`",
    "UPCGMatchAndSetAttributesSettings": "`PCG_SurfaceTest`; job 8 Zoning",
    "UPCGStaticMeshSpawnerSettings": "`PCG_SurfaceTest` (L5)",
    "UPCGSubgraphSettings": "`PCG_SurfaceTest` -> `SG_SurfaceSource`",
    "UPCGNormalToDensitySettings": "cylinder trap — see section 8",
    "UPCGMetadataVectorSettings": "7d.10 slope rules (Dot, Normalize)",
    "UPCGMetadataMathsSettings": "7d.10 slope rules",
    "UPCGAttributeFilteringRangeSettings": "7d.10 — palette alias *Point Filter Range*",
    "UPCGSampleTextureSettings": "7d.9 Gaea masks into PCG",
    "UPCGSplineSamplerSettings": "job 17 L2 Streets",
    "UPCGPolygon2DOperationSettings": "job 18b — `CutWithPaths`",
    "UPCGCreatePolygon2DSettings": "job 18b",
}

live = [n for n in nodes if not n["abstract"]]
by_cls = {n["cls"]: n for n in nodes}


def esc(s, cap=None):
    if s is None:
        return ""
    s = " ".join(str(s).split()).replace("|", "\\|")
    if cap and len(s) > cap:
        s = s[:cap].rstrip() + " …"
    return s


def first_sentence(s):
    s = " ".join((s or "").split())
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    return (m.group(1) if m else s)[:170]


def enum_opts(t):
    t = t.strip()
    m = re.match(r"(?:TEnumAsByte<)?(E\w+)>?$", t)
    if not m:
        return None
    vals = enums.get(m.group(1))
    if not vals:
        return None
    vis = [v["value"] for v in vals if not v["hidden"] and v["value"] not in ("MAX", "Count", "Num")]
    if not vis or len(vis) > 14:
        return f"{len(vis)} options" if vis else None
    return " · ".join(vis)


def clean_type(t):
    t = t.replace("TObjectPtr<", "").replace("TSoftObjectPtr<", "soft ").replace("TSubclassOf<", "class ")
    t = re.sub(r">+$", "", t) if t.count("<") < t.count(">") else t
    return t


def aliases_for(cls):
    a = aliases.get(cls)
    if not a:
        return []
    names = [x for x in a["explicit"] if "{0}" not in x]
    return names


L = []
w = L.append

# ------------------------------------------------------------------ header
w("# PCG Nodes — UE 5.7.4 reference")
w("")
w("*Built 2026-09-16 from the engine source of the installed UE 5.7.4 (`Engine/Plugins/PCG`, `PCGInterops`, "
  "`Experimental/PCGInterops`, `Experimental/PCGBiomeCore`) plus Epic's online node reference (5.8 edition). "
  "Every node below is in this project's palette — all PCG plugins are enabled in `Space_Colony.uproject`.*")
w("")
w("**Search this file by the name you see in the graph editor** — titles and palette aliases are both listed.")
w("")
w("| tag | meaning |")
w("|---|---|")
w("| **[src]** | text taken from the engine source — authoritative for 5.7.4 |")
w("| **[epic]** | text from Epic's node reference page (5.8 edition — may describe newer behaviour) |")
w("| **[class]** | no node tooltip in source; this is the C++ class comment |")
w("| ⚠ | deprecated — do not use in new graphs |")
w("| β / 🧪 | node lives in a **Beta** / **Experimental** plugin |")
w("| ◆ | setting is overridable — it gets a pin and can be driven by a graph parameter |")
w("| ★ | used or planned in this project (details in section 8) |")
w("| ↳ | a field inside the struct setting on the row above |")
w("| *Only when* | the setting is greyed out / hidden unless this condition holds (`EditCondition` [src]) |")
w("")
cnt_live = len(live)
cnt_props = sum(len(n["props"]) for n in live)
cnt_alias = sum(len(v.get("values", [])) + len(aliases_for(k)) for k, v in aliases.items())
w(f"**Counts:** {cnt_live} placeable node classes · {cnt_props} settings · "
  f"{sum(1 for n in live if n['deprecated'])} deprecated · ~{cnt_alias} extra palette entries from aliases · "
  f"{len(biome)} PCGBiomeCore assets.")
w("")
w("## Contents")
w("")
w("1. [Plugins and maturity](#1-plugins-and-maturity)")
w("2. [Index — every node on one line](#2-index--every-node-on-one-line)")
w("3. [Nodes by category](#3-nodes-by-category)")
w("4. [Palette aliases — one class, many search names](#4-palette-aliases--one-class-many-search-names)")
w("5. [Deprecated and replaced](#5-deprecated-and-replaced)")
w("6. [Name mismatches with Epic's docs](#6-name-mismatches-with-epics-docs)")
w("7. [PCGBiomeCore — graph assets, not nodes](#7-pcgbiomecore--graph-assets-not-nodes)")
w("8. [Project notes — nodes this project uses](#8-project-notes--nodes-this-project-uses)")
w("9. [Coverage and gaps](#9-coverage-and-gaps)")
w("10. [Sources and how this was built](#10-sources-and-how-this-was-built)")
w("")

# ------------------------------------------------------------------ 1 plugins
w("---")
w("")
w("## 1. Plugins and maturity")
w("")
w("From each plugin's `.uplugin` [src]. All are **enabled** in this project.")
w("")
w("| plugin | maturity | nodes | what it adds |")
w("|---|---|---|---|")
PL_DESC = {
    "PCG": "the framework and all core nodes",
    "PCGGeometryScriptInterop": "Mesh Sampler, Get Dynamic Mesh Data, Primitive Cross-Section and the 9 Dynamic Mesh nodes",
    "PCGPythonInterop": "Execute Python Script",
    "PCGExternalDataInterop": "Load Alembic",
    "PCGFastGeoInterop": "no nodes — a backend: *\"enables runtime spawning of primitives using FastGeo components\"* [src .uplugin]",
    "PCGInstancedActorsInterop": "Spawn Instanced Actors",
    "PCGNaniteAssembliesInterop": "Nanite Assembly Static Mesh Builder",
    "PCGNiagaraInterop": "Write To Niagara Data Channel",
    "PCGWaterInterop": "Get Water Spline Data",
}
pc = defaultdict(int)
for n in live:
    pc[subplugin(n)] += 1
MAT_TXT = {"": "production", "β": "β Beta", "🧪": "🧪 Experimental"}
for p in ["PCG", "PCGGeometryScriptInterop", "PCGPythonInterop", "PCGExternalDataInterop", "PCGFastGeoInterop",
          "PCGInstancedActorsInterop", "PCGNaniteAssembliesInterop", "PCGNiagaraInterop", "PCGWaterInterop"]:
    w(f"| `{p}` | {MAT_TXT[MATURITY.get(p, '')]} | {pc.get(p, 0)} | {PL_DESC[p]} |")
w("| `PCGBiomeCore` | 🧪 Experimental | 0 | graph assets + Blueprints, no C++ nodes — see section 7 |")
w("")
w("Epic's rule for Beta/Experimental: use with caution when shipping. **Mesh Sampler is Beta** — this project's "
  "whole L0 layer sits on it.")
w("")

# ------------------------------------------------------------------ 2 index
w("---")
w("")
w("## 2. Index — every node on one line")
w("")
w("Sorted by category, then name. The description is the first sentence of the best available text.")
w("")
groups = defaultdict(list)
for n in live:
    groups[n["type"]].append(n)
for cat in CAT_ORDER:
    if cat not in groups:
        continue
    w(f"### {CAT_NAME.get(cat, cat)} — {len(groups[cat])}")
    w("")
    w("| node | what it does | flags |")
    w("|---|---|---|")
    for n in sorted(groups[cat], key=lambda x: x["title"].lower()):
        ep = epic_nodes.get(norm(n["title"]))
        desc = n["tooltip"] or (ep["description"] if ep else "")
        flags = []
        if n["cls"] in PROJECT:
            flags.append("★")
        if n["deprecated"]:
            flags.append("⚠")
        m = MATURITY.get(subplugin(n), "")
        if m:
            flags.append(m)
        if n["hidden"]:
            flags.append("hidden")
        al = aliases_for(n["cls"])
        anchor = re.sub(r"[^a-z0-9 -]", "", n["title"].lower()).replace(" ", "-")
        title = f"[{n['title']}](#{anchor})"
        if al:
            title += " *(also: " + ", ".join(al) + ")*"
        w(f"| {title} | {esc(first_sentence(desc))} | {' '.join(flags)} |")
    w("")

# ------------------------------------------------------------------ 3 details
w("---")
w("")
w("## 3. Nodes by category")
w("")
w("Each entry: title, class, plugin, description, detected pins, and **every editable setting** the node declares "
  "(its own plus inherited ones below `UPCGSettings`). Enum settings list their options.")
w("")
for cat in CAT_ORDER:
    if cat not in groups:
        continue
    w(f"### ▸ {CAT_NAME.get(cat, cat)}")
    w("")
    for n in sorted(groups[cat], key=lambda x: x["title"].lower()):
        flags = []
        if n["cls"] in PROJECT:
            flags.append("★")
        if n["deprecated"]:
            flags.append("⚠ deprecated")
        m = MATURITY.get(subplugin(n), "")
        if m:
            flags.append({"β": "β Beta", "🧪": "🧪 Experimental"}[m])
        if n["hidden"]:
            flags.append("hidden in palette")
        w(f"#### {n['title']}" + ("  " + " · ".join(flags) if flags else ""))
        w("")
        meta = [f"`{n['cls']}`", f"plugin `{subplugin(n)}`"]
        if n["name"] and norm(n["name"]) != norm(n["title"]):
            meta.append(f"internal name `{n['name']}`")
        w(" · ".join(meta))
        w("")
        al = aliases_for(n["cls"])
        if al:
            w("**Also in the palette as:** " + ", ".join(f"*{a}*" for a in al))
            w("")
        a = aliases.get(n["cls"])
        if a and a.get("enum") and a.get("values"):
            w(f"**One palette entry per `{a['enum']}` value** — see section 4.")
            w("")
        if n["deprecated"] and n.get("dep_msg"):
            w(f"> ⚠ Deprecated in {n['dep_version']}: *{n['dep_msg']}* [src]")
            w("")
        if n["tooltip"]:
            tag = "[class]" if n.get("tooltip_note") == "class comment" else "[src]"
            w(f"{tag} {esc(n['tooltip'])}")
            w("")
        ep = epic_nodes.get(norm(n["title"]))
        if not ep and n["cls"] in UNCAT_MAP:
            ep = epic_uncat.get(UNCAT_MAP[n["cls"]])
        if ep and ep["description"] and norm(ep["description"])[:60] != norm(n["tooltip"] or "")[:60]:
            w(f"[epic] {esc(ep['description'], 900)}")
            w("")
        if not n["tooltip"] and not ep:
            w("*No official description in the engine source or Epic's reference. Settings below are the only "
              "documentation.*")
            w("")
        pin_in = ", ".join(n["inputs"]["types"]) if n["inputs"]["types"] else None
        pin_out = ", ".join(n["outputs"]["types"]) if n["outputs"]["types"] else None
        if pin_in or pin_out:
            w(f"**Pin data types detected:** in `{pin_in or 'default'}` → out `{pin_out or 'default'}`")
            w("")
        if n["cls"] in PROJECT:
            w(f"★ **This project:** {PROJECT[n['cls']]}")
            w("")
        if n["props"]:
            w("| setting | type | default | ◆ | what it does |")
            w("|---|---|---|---|---|")
            def row(p, prefix="", inherited_from=None):
                nm = p["display"] or p["name"]
                typ = clean_type(p["type"])
                opts = enum_opts(p["type"])
                tip = esc(p["tooltip"], 420)
                if opts:
                    tip = (tip + " " if tip else "") + f"*Options: {esc(opts)}*"
                if p.get("edit_condition"):
                    tip = (tip + " " if tip else "") + f"*Only when* `{esc(p['edit_condition'], 140)}`"
                if inherited_from:
                    tip = (tip + " " if tip else "") + f"*(from `{inherited_from}`)*"
                dflt = esc(p["default"], 60) if p["default"] else ""
                w(f"| {prefix}`{esc(nm)}` | `{esc(typ, 70)}` | {('`' + dflt + '`') if dflt else ''} | "
                  f"{'◆' if p.get('overridable') else ''} | {tip} |")

            for p in n["props"]:
                row(p, inherited_from=p["from"] if p["from"] != n["cls"] else None)
                st = struct_of(p["type"])
                if st:
                    for f in st[1]:
                        row(f, prefix="↳ ")
            w("")
        else:
            w("*No editable settings declared.*")
            w("")

# ------------------------------------------------------------------ 4 aliases
w("---")
w("")
w("## 4. Palette aliases — one class, many search names")
w("")
w("PCG lets one settings class publish several palette entries with different defaults "
  "(`GetPreconfiguredInfo()` [src]). Typing any of these names in the graph editor gives you the class on the left "
  "with that option preselected. **23 classes do this.**")
w("")
w("### Named aliases")
w("")
w("| palette name | is really | class |")
w("|---|---|---|")
for cls, a in aliases.items():
    for x in a["explicit"]:
        if "{0}" in x:
            continue
        w(f"| *{x}* | {by_cls[cls]['title'] if cls in by_cls else cls} | `{cls}` |")
w("")
w("### Per-type aliases")
w("")
for cls, a in aliases.items():
    tmpl = [x for x in a["explicit"] if "{0}" in x]
    if tmpl and a.get("values"):
        vals = ", ".join(v["display"] for v in a["values"])
        w(f"- **{by_cls[cls]['title']}** — *{tmpl[0].replace('{0}', '<Type>')}* for each of: {vals}")
w("")
w("### Per-operation aliases")
w("")
w("Each operation below is its own palette entry. Descriptions: [src] enum tooltip where the source has one, "
  "otherwise [epic].")
w("")
for cls, a in aliases.items():
    if not a.get("enum") or not a.get("values") or any("{0}" in x for x in a["explicit"]):
        continue
    t = by_cls[cls]["title"] if cls in by_cls else cls
    w(f"#### {t} — {len(a['values'])} operations (`{a['enum']}`)")
    w("")
    w("| operation | description |")
    w("|---|---|")
    ops = epic_ops.get(cls, {})
    for v in a["values"]:
        d = v["tooltip"]
        tag = "[src]"
        if not d:
            d = ops.get(norm(v["display"])) or ops.get(norm(v["value"]))
            tag = "[epic]" if d else ""
        w(f"| **{v['display']}** | {(tag + ' ' + esc(d, 300)) if d else ''} |")
    w("")

# ------------------------------------------------------------------ 5 deprecated
w("---")
w("")
w("## 5. Deprecated and replaced")
w("")
w("| node | class | since | replacement [src] |")
w("|---|---|---|---|")
for n in nodes:
    if n["deprecated"]:
        w(f"| {n['title']} | `{n['cls']}` | {n.get('dep_version') or '—'} | {esc(n.get('dep_msg')) or 'class is prefixed `UDEPRECATED_`'} |")
w("")
w("The palette name **Density Remap** still exists, but it now creates **Attribute Remap** (section 4) — the old "
  "`UPCGDensityRemapSettings` class is the deprecated one. Same for **Generate Grass Maps** → Generate Landscape "
  "Textures.")
w("")

# ------------------------------------------------------------------ 6 mismatches
w("---")
w("")
w("## 6. Name mismatches with Epic's docs")
w("")
w("Epic's reference is the 5.8 edition and lags the engine: it names "
  f"{len(epic_nodes)} nodes; **{sum(1 for n in live if norm(n['title']) in epic_nodes)} of the "
  f"{len(live)} placeable 5.7.4 classes** match one of those by title. The rest are documented here from source only.")
w("")
engt = {norm(n["title"]) for n in nodes}
for n in nodes:
    for x in aliases_for(n["cls"]):
        engt.add(norm(x))
missing = [e for k, e in epic_nodes.items() if k not in engt]
if missing:
    w("**In Epic's page but not a 5.7.4 node title or alias:**")
    w("")
    for e in missing:
        w(f"- *{e['node']}* ({e['category']})")
    w("")
w("**Names this project's docs use that differ from the 5.7.4 node title:**")
w("")
w("| written in our docs | 5.7.4 palette | note |")
w("|---|---|---|")
w("| Point Filter Range (`ue_working_rules.md`, 7d.10) | *Point Filter Range* | valid — alias of **Filter Attribute Elements by Range** |")
w("| Polygon2D Operation (checklist 18b) | **Polygon Operation** | internal name is `Polygon2DOperation`; `CutWithPaths` exists |")
w("| Data From Actor (`ue_working_rules.md`) | **Get Actor Data** | class is still `UPCGDataFromActorSettings` |")
w("| Density Remap | *Density Remap* | now an alias of **Attribute Remap**; the old class is deprecated |")
w("")

# ------------------------------------------------------------------ 7 biome
w("---")
w("")
w("## 7. PCGBiomeCore — graph assets, not nodes")
w("")
w("`Experimental/PCGBiomeCore` (enabled) ships **no C++ node classes** — only PCG graph assets, Blueprints and data "
  f"assets ({len(biome)} files). Its graphs appear in the palette as subgraphs. Listed by folder [src: plugin Content]:")
w("")
bf = OrderedDict()
for p in biome:
    top = p.split("/")[0] if "/" in p else "(root)"
    bf.setdefault(top, []).append(p.split("/")[-1].replace(".uasset", ""))
for k, v in bf.items():
    w(f"- **{k}** ({len(v)}): " + ", ".join(f"`{x}`" for x in v))
w("")

# ------------------------------------------------------------------ 8 project
w("---")
w("")
w("## 8. Project notes — nodes this project uses")
w("")
w("Facts measured in `Space_Colony` or read from source this session. Full context: `ue_working_rules.md`.")
w("")
w("### Where they sit")
w("")
w("```")
w("PCG_SurfaceTest")
w("  Subgraph (SG_SurfaceSource) -> Transform Points -> Match And Set Attributes <- Load Data Table")
w("                                                     -> Static Mesh Spawner")
w("SG_SurfaceSource  (L0)")
w("  Mesh Sampler --> Copy Points <-- Get Actor Data (By Tag)")
w("  8 x Get Graph Parameter: SurfaceMesh, SurfaceTag, SamplingRadius, Max Num Samples,")
w("                           Sub Sample Density, Requested LOD Type, Remove Hidden Triangles, Seed")
w("```")
w("")
w("### Traps, with evidence")
w("")
w("| node | trap | evidence |")
w("|---|---|---|")
w("| **Mesh Sampler** | `Requested LOD Type = Render Data` samples LOD 0 of the render data — on a **Nanite** mesh "
  "that is the **fallback**, not the Nanite geometry | [src] `PCGMeshSampler.h` default `RenderData`; measured: "
  "Fallback Target `Auto` cut LOD 0 from 567,000 to **1,837** tris |")
w("| **Mesh Sampler** | point spacing is **at least 2 × Sampling Radius** | [src] tooltip; measured radius 1000 → "
  "min spacing **20.0 m** |")
w("| **Mesh Sampler** | `Max Num Samples = 0` means **no limit**, not zero points | [src] *\"If 0 or default value, mesh "
  "will be maximally sampled\"*; measured 2,336 points at 0 |")
w("| **Mesh Sampler** | the node's stock `Max Num Samples` (500) caps a large surface | measured: 7.9 km belt "
  "starved at 500 |")
w("| **Mesh Sampler** | `Remove Hidden Triangles` only runs when `Voxelize` is on | [src] `EditCondition = bVoxelize` "
  "— with Voxelize off it does nothing |")
w("| **Mesh Sampler** | two seeds exist: `Sampling Options → Random Seed` and the node `Seed` (needs `Use Seed`) | "
  "[src] class properties — check which one a Seed parameter drives |")
w("| **Get Actor Data** | `Get Single Point` + `By Tag` + `select_multiple = false` silently takes the **first** "
  "matching actor | measured: ring structure shared `SurfaceSource`; every instance spawned **76,444 cm** too high |")
w("| **Copy Points** | defaults apply the target's rotation **and scale to positions** | [src] "
  "`bApplyTargetRotationToPositions`, `bApplyTargetScaleToPositions` default `true`; a scaled surface actor "
  "scales the point layout |")
w("| **Transform Points** | `Absolute Scale` off = scale multiplies | [src]; `PCG_SurfaceTest` uses relative 50 |")
w("| **Normal To Density** | compares every point against **one fixed vector** (`UpVector`) — wrong on a cylinder | "
  "[src] `Normal` default `FVector::UpVector`; use per-point up with Attribute Vector Op instead (7d.10) |")
w("| **Get Graph Parameter** | a newly added graph parameter starts at **0** and is immediately marked overridden, "
  "silently replacing the node's working value | measured 2026-09-16 on `SG_SurfaceSource` |")
w("")
w("### Planned nodes (checked to exist in 5.7.4)")
w("")
w("| plan | node | confirmed |")
w("|---|---|---|")
w("| 7d.9 Gaea masks | **Sample Texture** | exists; Sampler category |")
w("| 7d.10 slope rules | **Attribute Vector Op** → *Dot*, *Normalize*; **Point Filter Range** | Vector Op has 10 "
  "operations incl. Dot and Normalize; Point Filter Range is an alias |")
w("| 17 L2 Streets | **Spline Sampler** | exists |")
w("| 18b block subdivision | **Polygon Operation** → `CutWithPaths` | [src] *\"Cuts polygons with paths by completing "
  "them using the polygon bounds. If both ends of the path are not outside the input polygons, the results might "
  "be incorrect.\"* |")
w("")

# ------------------------------------------------------------------ 9 gaps
w("---")
w("")
w("## 9. Coverage and gaps")
w("")
nodesc = [n["title"] for n in live if not n["tooltip"] and not epic_nodes.get(norm(n["title"]))
          and n["cls"] not in UNCAT_MAP]
w(f"- **{len(nodesc)} nodes have no description** in either source or Epic's page: " + ", ".join(nodesc) +
  ". Their settings tables are the only documentation.")
w("- **Pins are partial.** Detected from `InputPinProperties()` / `OutputPinProperties()` where they name a data "
  "type directly; many nodes inherit the default pins and show none. Check the node in the editor for exact pins.")
w("- **Settings come from headers.** Properties added through metadata, instanced structs or dynamic pins "
  "(e.g. Select (Multi), Switch) are not listed. Struct settings are expanded one level (↳) when the struct has "
  "16 fields or fewer; selector structs such as `FPCGAttributePropertyInputSelector` have custom UI and no fields "
  "to list.")
w("- **Base classes are omitted** from sections 2–3: " +
  ", ".join(f"`{n['cls']}`" for n in nodes if n["abstract"]) + ".")
w("- **Epic's page is 5.8.** Where an [epic] description disagrees with [src], trust [src] for this 5.7.4 project.")
w("")

# ------------------------------------------------------------------ 10 sources
w("---")
w("")
w("## 10. Sources and how this was built")
w("")
w("- Engine source, UE 5.7.4 install: every `UCLASS` deriving from `UPCGSettings` under `Engine/Plugins/PCG/Source`, "
  "`PCGInterops`, `Experimental/PCGInterops`, `Experimental/PCGBiomeCore`. Title / tooltip / category from "
  "`GetDefaultNodeTitle()`, `GetNodeTooltipText()`, `GetType()` (inherited where not overridden, named "
  "constants resolved inside their namespace). Settings from `UPROPERTY(EditAnywhere …)` with their comments. "
  "Aliases from `GetPreconfiguredInfo()`; enum options from `UENUM`s with `UMETA`.")
w("- Epic node reference: "
  "https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine "
  "(read 2026-09-16, page marked 5.8).")
w("- Plugin maturity: each plugin's `.uplugin` (`IsBetaVersion` / `IsExperimentalVersion`). Enabled state: "
  "`Space_Colony.uproject`.")
w("- **Regenerate, don't hand-edit sections 1–7 and 9.** `python Tools/pcg_reference/build.py` rescans the engine "
  "and rewrites this file (edit `ENGINE` in `build.py` after an upgrade, e.g. to 5.8 for Mesh Terrain). Epic's page "
  "is cached in `Tools/pcg_reference/epic_nodes.json` (it renders client-side, so refreshing it needs a browser "
  "capture — see `parse_epic.py`). Section 8 lives in `gen_doc.py` and is written by hand from project evidence.")
w("")

open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote", OUT, "lines", len(L))
