# CLAUDE.md — O'Neill Cylinder project handoff

*Written 2026-09-15 (end of Week 5, day 2) as the summary to survive a context compaction.*

---

## 1. The project

Solo **UE 5.7.4** O'Neill cylinder portfolio piece aimed at **Technical Artist (PCG) roles**. The product is a
**PCG city-generation tool**; the colony is the stage it runs on. User works full time, >1 year runway,
"don't waste every day".

**Docs (read these before acting):**

| file | holds |
|---|---|
| `docs/checklist.md` | the one rolling checklist — **one-line tasks only** |
| `docs/project_log.md` | decisions + history + working rules |
| `docs/ue_working_rules.md` | engine how-to, traps, measurements (incl. **Terrain** section) |
| `docs/gaea.md` | everything Gaea: limits, UI, nodes, recipes, measurements, final graph |
| `docs/layer_contract.md` | the city-generation system design (L0–L5, demo shot list) |
| `docs/schedule_revised_10week.md` | the 10-week plan (superseded in parts by the checklist) |

## 2. How to work with this user

- **Search before answering.** Anything about tool/node behaviour, settings, limits, workflows: check official
  docs, engine source, or the app's own example files first, cite it, and label anything unverified.
- **Propose before applying.** Show what will change (docs, structure, judgment calls) and wait for OK. Small
  factual logging of measured results can go straight in, but say so.
- **Keep `checklist.md` terse.** Evidence and numbers live in the other docs.
- **The user builds in-editor and makes art calls. I measure, research, wrangle data, write boilerplate.**
  The user types their own tool code.
- **Gaea graphs: nodes only, no hand painting** (user decision 2026-09-15).
- **Hard rules:** PCG graphs are edited in the editor, never via Python · no asset imports through the MCP
  bridge · save the level before deleting redirectors · World Partition actors need `actor.modify(True)` ·
  don't max the PC.

## 3. Where the project stands (2026-09-15)

**Two releases** (decided 2026-09-14): **Publish 1 = the PCG tool** (greybox, then apply for jobs);
**Later = colony polish**. Checklist: **68 open — Publish 1: 39 · Later: 29**.

**Week 5 checkpoint (Fri 18 Sep): terrain on the belt, PCG sampling it.**

### Terrain decisions
- Terrain is a **separate curved static mesh** laid on the belt. **PCG reads it, never writes it.** Shaped only
  with native tools: Gaea + Unreal Modeling Mode. Rejected: Landscape, WPO curved-world shader, Blender,
  Houdini, Voxel Plugin. Upgrade path: UE 5.8 Mesh Terrain.
- **No painted city plateaus.** PCG follows the natural valley; slope rules keep streets/buildings off steep
  ground; district positions come from zoning (job 8) as numbers.
- Gaea is **Community (free)**: 1K builds, square terrains, no automation → no Gaea MCP server.

### Done
- **Modeling Mode spike passed** (Testing_Map): bend 60° = 954.93 m wide / 127.94 m rise; displacement goes
  **inward**; sculpt smooth at 640k tris; **PCG regenerates after a sculpt is saved**.
- **Belt measured** (`Space_Colony`, MCP line traces): axis along **Y** through
  **(−221,760.55, 49,112.33, 175,805.30)**, inner radius **954.66 m**, span **±30°**, length 7,900 m; the other
  two belts are the same belt rotated **±120°**.
- **Gaea relief finished** (build 018, checklist 7d.5 ✅): valley with mountains at the belt edges, soft seam,
  gentle meander (±91 m, never leaves the calm centre), river bed **−5.3 m** below its banks, heights
  10.8–384.7 m. Full node settings in `docs/gaea.md` → *Final graph*.
- **Deliverables copied** to `SourceArt/Gaea/`: `Belt_Residential_Height.exr` (heightmap) and
  `Belt_Residential_RiverMask.exr` (river mask). Both LFS-tracked.

### Next (Wed 16 Sep): the terrain mesh in Unreal — checklist 7d.4
Steps and every measured number are in `ue_working_rules.md` → **Terrain** → *Full-sheet recipe*:
1. Rect **Depth 99,800 (X) / 63 subdiv · Width 99,000 (Y) / 500 subdiv** (X longest so Warp bends the right way)
2. Warp **Bend 60°**, bounds ±49,900 → arc radius **953.0 m**
3. Actor **Scale Y 7.98** → 7,900 m, then **Bake Transform** (distance fields can't take non-uniform scale)
4. Displace **Flat ×2** → ~5.3 m grid, ~567k tris
5. Displace **Texture2D Map** with the Gaea EXR — UV Scale **(0.1266, 1.008)**, UV Offset **(0.4367, 0)**,
   Base value 0, Intensity = Terrain Height × 100 (400 m → 40,000)
6. Place at **X −221,760.55, Y 49,112.33, Z 80,505.3**
7. Then 7d.4b Nanite fallback check → 7d.7 point L0 at the terrain → 7d.8 SamplingRadius → **checkpoint**

**Unverified, check at first import:** which UV direction matches the image rows, whether Unreal imports the
float EXR as R32F or RGBA16F, and whether metres = value × Terrain Height.

## 4. Open questions
- Gaea **Community licence is non-commercial** — check what that means for a public portfolio **before publishing**.
- Does the demo video get a terrain/slope shot? (`checklist.md` → D1)
- Third belt: cut or keep? (job 15)
- Optional prep: add Gaea **Slope / Soil / Height** mask nodes off Rivers Out (checklist 7d.11) — tune later with
  `M_Terrain`. Tree/grass placement stays in PCG, driven by those masks (job 16).

## 5. Uncommitted work
Docs updated today (`checklist.md`, `gaea.md`, `ue_working_rules.md`, plus the two EXRs in `SourceArt/Gaea/`)
and the user still has to **Save As** the Gaea project into `SourceArt/Gaea/Belt_Residential.terrain`, then commit.
