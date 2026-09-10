---
name: space-colony
description: Working rules for the O'Neill Cylinder UE 5.7 PCG portfolio project — the precision protocol (measure live state, never assert from memory), the hard-won engine traps, the L0-L5 layer contract, and the division of labour. Use this whenever the task touches this project in any way: Unreal Engine, PCG graphs, Blender meshes, the module_list.xlsx pipeline, the manifest validator, materials, Nanite, World Partition, FBX import/export, the checklist, or the layer contract. Also use it before answering any question about what the project contains or what state something is in — those answers must come from a measurement, not from recall.
---

# O'Neill Cylinder — project working rules

A solo UE 5.7.4 portfolio project targeting **PCG-focused technical art roles**, on a fixed
10-week runway. The pitch: *a blockout tool for deciding what a place should be, before anyone
commits to what it looks like.* The cylinder is the proof, not the product.

## Division of labour — this matters more than anything else here

**The user builds and judges. You measure, research, and wrangle data.**

| the user does | you do |
|---|---|
| edits PCG graphs in the editor | probes live state, reports numbers |
| models in Blender | one-off scripts, batch operations, file conversion |
| all art and taste calls | research with sources, engine-source lookups |
| writes their own Python | boilerplate, data transforms, verification queries |

They have said, repeatedly: *"if you did all of it then i can't learn anything here"* and
*"did you change my code? i want to type it myself."* Offer to write the boilerplate; never
take over the parts they are learning. When they ask a question, they want the reasoning and
the evidence, not just the answer.

## The precision protocol

The single most common failure in this project is asserting something plausible instead of
checking. It has cost hours. **Probe → act → verify.**

- **Read live state before answering.** "What material is on X", "how many polys", "is Y
  enabled" — all of these have a measurable answer. Go and get it.
- **Verify after writing.** An operation that raised no exception has not been confirmed.
  Several UE APIs fail silently — `get_editor_property('static_materials')` returns *copies*,
  so mutating them and reassigning does nothing and raises nothing. Always read back.
- **Prefer engine source over web search** for how a node behaves:
  ```
  C:\Program Files\Epic Games\UE_5.7\Engine\Plugins\PCG\Source
  ```
  Grepping the headers for enums, tooltips and property names has been decisively better than
  searching. Do this before guessing at a node's options.
- **Say which kind of claim you are making.** MEASURED (I read it just now) · DOCUMENTED
  (a source says so) · INFERRED (I reasoned it). Do not let the third masquerade as the first.
- **A measured value means nothing until compared to a reference.** A number is only "wrong",
  "off-centre" or "too dark" relative to something stated.

## Traps that have already broken this project

| | |
|---|---|
| **PCG graphs** | Edit in the **editor**, never via Python. A Python write with the editor open corrupted the graph (`Invalid PCGGraph`). |
| **World Partition** | Actors are separate packages. `save_current_level()` does **not** save them — needs `actor.modify(True)` then `save_packages()`. This broke the level twice. |
| **Renaming assets** | **Save the level, then** delete redirectors. The other order nulled 58 mesh references. |
| **Soft object paths** | Must be `Asset.Asset`. The short form spawns **nothing, silently**. Enforced by `check_mesh_paths`. |
| **Attribute names are NOT case-sensitive** | Verified in engine source 2026-09-10. `FPCGAttributeIdentifier` keys on `FName`, and `operator==` / `GetTypeHash` use FName's case-insensitive comparison index (`PCGMetadataCommon.h:151,156`). Nothing in PCG lowercases what you type (`PCGAttributePropertySelector.cpp:424`). The old rule here claimed the opposite — it was wrong. |
| **Nanite hides tri counts** | `get_num_triangles(0)` returns the **fallback** mesh. Verify reimports by **bounding box**, not tri count. Nanite also silently reduced PCG sampling (90 → 64 points). |
| **Blender Edit Mode** | Reading `object.data` while Edit Mode is open returns a **stale** datablock. Use `bmesh.from_edit_mesh()` or leave Edit Mode first. |
| **Mesh Sampler** | Emits **mesh-local** coordinates and reads the mesh *asset*, ignoring actor scale. Radius 5000 for the belt; the default 10 uu will hang the editor at 13 km. |
| **Silent PCG failures** | Often no error at all. Turn **Debug** on each node in turn and find the last one still holding data. |
| **Names aren't evidence** | `SKM_Quinn_LOD0` is a StaticMesh, not skeletal, not Quinn — it is the 1.8 m human scale ref. Check the measurement, not the label. |

Fuller detail lives in `docs/ue_working_rules.md`.

## The layer contract

**One rule: every layer consumes points carrying attributes, and emits points carrying
attributes.** A layer never knows what produced its input. That is what makes layers swappable.

```
L0  SURFACE      any mesh          ->  points {position, rotation}     PROVEN on 2 surfaces
L1  DENSITY      artist authoring  ->  + {Density}                     not started
L2  STREETS      artist splines    ->  + {DistToRoad, RoadDir}         not started
L3  LOTS         frontage-only     ->  + {LotSize}                     not started
L4  SELECTION    DT_Modules        ->  + {Mesh}                        working
L5  SPAWN        instances                                             working
```

Anything **surface-scale-dependent belongs in a subgraph parameter**, not a typed value —
learned by finding three baked assumptions that were invisible until a second surface existed.

Full design, presets, attribute vocabulary and open decisions: `docs/layer_contract.md`.

## Where things are

```
docs/checklist.md               THE rolling checklist for the whole project, ordered by
                                execution (1 = do first). Never superseded by a new weekly file -
                                corrections only ever land in the newest doc, which is how job 9
                                went stale.
docs/layer_contract.md          the system design
docs/ue_working_rules.md        traps and rules, longer form
docs/module_list.xlsx           ▸ **Column Guide** sheet = the AUTHORITATIVE meaning of every
                                DT_Modules column. Read it before proposing any schema change -
                                a 7b "fix" was proposed and withdrawn for skipping it.
Tools/manifest_tool/            the validator - the user's own Python
Tools/ue_scripts/               material_slot_map.json
SourceArt/FBX/                  57 per-object FBXs - keep exporting per-object
SourceArt/Refined/SC_Refined.blend
```

**Keep the checklist lean.** It is a tick-list: task, deadline, key number. Rationale goes in
`ue_working_rules.md` or `layer_contract.md`. It has twice been bloated with explanation and had
to be trimmed back — if you are writing paragraphs into it, it is drifting.
