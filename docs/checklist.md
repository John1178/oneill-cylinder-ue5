# O'Neill Cylinder — Project Checklist

*rev 13 · 2026-09-10 · ordered by execution: **1 = do first**.*

> **This is the one rolling checklist for the whole project.** It is never replaced by a new
> weekly file. Corrections land here and nowhere else — splitting per week is exactly how job 9
> kept a claim that had already been disproven. Archived detail: `week_1_2_checklist.md`,
> `week_3_checklist.md`, `week_4_checklist.md`.

**42 done · 25 open · 63% complete.** Updated **Thu 10 Sep 2026**.

| # | job | items | when |
|---|---|---|---|
| **1** | ~~Swappable surface~~ ⭐ *the thesis* | ✅ | **CLOSED Wed 9** |
| **2** | Failure shot | 1 | *optional — no scheduled time* |
| **3** | ~~Replace `M_Temp`~~ | ✅ | **done Wed 9** |
| **4** | Reference board — fill the gaps | 1 | **Thu 10** |
| **5** | Lit windows | 1 | **Fri 11 AM** |
| **6** | `Weight` case fix | 1 | **Fri 11 PM** *(buffer)* |
| | — end of Week 4 — | **9** | |
| 7 | ~~City-gen design block~~ ✅ → [`layer_contract.md`](layer_contract.md) | 3 open | Week 5 |
| 7d | **Terrain on the belt** — the sandbox | 5 | Week 5-6 |
| 8 | Zoning | 4 | Week 5 |
| 9 | Real space cubemap | 1 | Week 5 |
| 10 | Shadows at distance | 1 | Week 5 |
| 11 | Detail meshes / kitbash | 4 | Week 5-6 |
| 12 | Volumetric fog | 1 | Week 6 |
| 13 | Rect lights at windows | 1 | Week 6 |
| 14 | Source the 24 modules | 1 | ongoing, in gaps |

**The Week 4 checkpoint already passed** (2026-09-07, 90 instances driven by the DataTable).
Everything below is upside.

**Job 1 goes first only because it is half a day.** If it overruns, stop and move to job 3 —
it needs to exist and be demonstrable, not elegant. That still leaves ~2 of 3 days on art,
which is where the real risk is. Art is not closed by this week either way: job 11 is
multi-week Week 5-6 work regardless.

---

# Open work

## 1. Swappable surface — *the thesis* ✅ CLOSED

> ~~Filter out the outer shell face~~ — **removed 2026-09-09, not done.** The belt is a shell,
> so sampling hit both faces (measured: **36 of 64 cubes on the OUTER surface**, radius ~99,500
> vs ~95,500). But a heightmap terrain will become the sample surface, and terrain is a single
> sheet — there is no second face. The problem disappears rather than needing a filter.
> *(The Blender split into `_Ground` / `_Hull` was done anyway and kept; not imported to UE.)*


- [x] ✅ `SG_SurfaceSource` subgraph — params `SurfaceMesh` / `SurfaceTag` / `SamplingRadius`.
      `Transform Points` stays outside; L0 emits points only.
- [x] ✅ Flat-ground twin — `SM_Plane2`, tagged `SurfaceSource`
- [x] ✅ **CHECKPOINT PASSED 2026-09-09** — same downstream graph on cylinder and plane,
      unchanged. Swapping a surface = 3 parameter values.
      *Three baked assumptions the twin exposed: see `ue_working_rules.md` → Surface swapping.*

## 2. Failure shot — *optional*

- [ ] ⬜ ONE image: the **stock** Surface Sampler failing on the cylinder. It is a statement
      about PCG's default, not about a bug of yours. Lead image is always the working result;
      this goes second or later. Do not schedule time for it.  `[optional]`

## 3. Replace `M_Temp` ✅ DONE 2026-09-09

- [x] ✅ 33 meshes reassigned, **zero left on `M_Temp`**, verified by read-back.
      `MI_Structural_HullShell` x3 · `MI_Greenhouse` x30. Both parent to `M_Structural`,
      which already has triplanar + LWC — no UVs needed at 13 km.
      ⚠️ `M_Temp` was two-sided, `M_Structural` is not — watch for holes.

## 4. Reference board — fill the gaps `[Thu 10]`

- [ ] ⬜ Board exists but is all wide vistas. **Missing: close-up hull material · structural /
      kitbash detail · window-to-land junction · night + lit windows · scale anchors.**
      Group by *task*, not by subject. NASA Ames (Guidice / Don Davis, 1970s) is public domain
      and is literally O'Neill interiors — the only reference you could legally show in a breakdown.

## 5. Lit windows `[Fri 11 AM]`

- [x] ✅ **Interior ambient solved 2026-09-10.** Cause was `Sky Light Intensity` being ~30x too
      low, not the cubemap. **Artist-set values as of 2026-09-10: Sky 50 / Sun 2000** (= 24:1
      key-to-fill; see `ue_working_rules.md` for the lux/cd-m2 conversion).
- [x] ✅ **Sun lens flare ON** — `Enable Sun Lens Flare`, Zoom Chromatic, strength 0.3. Was
      already configured and simply switched off. Light shaft bloom left OFF (needs a medium).
- [ ] ⬜ Tune the rect lights warm and wire to `MPC_DayNight` (`WindowEmissiveIntensity`,
      `WindowEmissiveColor`, `AmbientTint`). Currently 6500 K, `use_temperature=False`.
- [ ] ⬜ Judge whether contact shadows are missed — all 3 rect lights are `cast_shadows=False`.

## 6. `Weight` case fix `[Fri 11 PM]`

- [ ] ⬜ **Case was never the cause** — disproven in engine source 2026-09-10 (chain in
      `ue_working_rules.md`). Re-test in editor and find the real cause. First two suspects:
      `bUseWeightAttribute` ("Use Weight Attribute") unticked — it is an `EditCondition`, so the
      field is inert without it; and `Match Weight Attribute` carries
      `PCG_DiscardPropertySelection`, so a `$Property` entry is rejected — attributes only.

---

## 7. City generation — design block ✅ DONE 2026-09-09

**Output: [`layer_contract.md`](layer_contract.md).** Read it before building 8 onward.

- [x] ✅ Layer stack · inter-layer contract · authoring vs generation · determinism · data vs graph

### Left open

- [x] ✅ **7a. L3 = frontage-only first.** Settled by naming the art director as primary user.
- [x] ✅ **7b. WITHDRAWN 2026-09-10 — there was no schema bug.** The proposal misread two
      columns whose meanings are defined in `module_list.xlsx` ▸ **Column Guide**:
      `Zone` = which zone a **BUILDING** belongs to (Residential/Industrial/Service, `-` for
      everything else); `Belt` = **A hero / B support / All**, a *quality tier* read only by the
      **validator** to catch "Belt A module used in Belt B". PCG does not read `Belt`.
      `Service` is a deliberate building zone, not an orphan. **Job 8 was never blocked.**
- [ ] ⬜ **7b-new. Decide the agriculture belt's vocabulary.** The zone list is building-only,
      so the agriculture belt has no zone. Either add `Agriculture` as a 4th `Zone` value, or
      leave `Zone` building-only as designed and drive agriculture off `Category`
      (`Greenery & Terrain`). Design call, not a bug.  `[Week 5]`
- [ ] ⬜ **7c. Clearance enforcement** — column exists, nothing reads it.  `[Week 5]`

## 7d. Terrain on the belt `[Week 5-6]` — *new scope, 2026-09-09*

Heightmap-generated terrain laid onto the belt's inner surface. **This becomes what L0 samples**,
replacing the belt shell.

- [ ] ⬜ **1. Decide the source.** Gaea (has a CLI + Extensibility API, and a third-party MCP
      exists — but automation needs the **Professional/Enterprise** tier) · UE landscape ·
      sculpt in Blender · or a noise-driven displacement.  `[Week 5]`
- [ ] ⬜ **2. Solve the wrap.** Terrain is authored flat; the belt is curved. Generate in
      **unrolled 2D** (belt length x circumference) and map onto the cylinder — the *same*
      approach already chosen for city layout in `layer_contract.md` L3. One solution, two uses.  `[Week 5]`
- [ ] ⬜ **3. Repoint L0** — `SurfaceMesh` becomes the terrain, not the belt.  `[Week 6]`
- [ ] ⬜ **4. Retune `SamplingRadius`** for the new surface. Already a subgraph parameter, so
      this is a value change, not a rebuild.  `[Week 6]`
- [ ] ⬜ **5. Add slope + aspect rules** now that there is slope to read — max-slope cull,
      align-to-slope, density by flatness. **This is the feature terrain exists to unlock**,
      and it is a strong demo beat.  `[Week 6]`

**Why this is core, not decoration** *(revised 2026-09-09 — an earlier note filed it as
"cinematic only", which was wrong):*

- **The tool needs a sandbox.** Placement on a perfectly smooth cylinder wall looks trivial —
  it is what any scatter node does. On varied terrain the problem becomes *visible*: things
  conforming to slopes, following valleys, avoiding steep ground. The system does not improve;
  it becomes **legible**, which is the whole job of a demo.
- **It unlocks slope and aspect rules** — "nothing above 30 degrees", "orient to the slope",
  "denser in the flats". Standard in every serious placement system, currently **impossible**
  here because a smooth surface has no slope to read. A real capability gap, not garnish.
- **It is a third surface, and the hardest one:**
  ```
  flat plane             trivial
  smooth cylinder        curved
  heightmap on cylinder  curved AND varied
  ```
  Three surfaces of increasing difficulty is a far stronger argument than two.
- **The pipeline is already known** (Gaea -> UE -> terrain master material), so the usual
  "new tool, new export path" cost does not apply here.

**It also fixes for free:** the outer-shell double-spawn (job 1's dropped item), and the belt
reading as a smooth wall rather than as ground.

> **Sequencing:** it changes what PCG samples, so do it **before** zoning and density work,
> not after.

## 8. Zoning (Layer 1) `[Week 5]`

- [ ] ⬜ Split the belt into zones along Y, hand-authored
- [ ] ⬜ Write `Zone` onto each surface point
- [ ] ⬜ `Match And Set Attributes` → match `Zone` → `Zone`
- [ ] ⬜ **CHECKPOINT** — residential modules only in the residential stretch

## 9. Real space cubemap `[optional, cosmetic]`

- [ ] ⬜ ~~`FlatCubemap` is a dark placeholder~~ — **false, disproven 2026-09-10.** It is flat
      **grey** and out-performed a real daylight HDRI at equal intensity. Ambient was fixed by
      `Sky Light Intensity` 20 → 100. A real cubemap now only changes hull **reflections**, not
      ambient — pure look, no longer a fix. Deprioritised.

## 10. Shadows vanishing at distance `[Week 5]`

- [ ] ⬜ `Show > Visualize > Virtual Shadow Map`. Measured: `cast_far_shadow = 0` on all 60
      actors, `MaxPhysicalPages = 4096` — two untested candidates.

## 11. Detail meshes / kitbash `[Week 5-6]`

Separate objects, never edited into the shells. One rib modelled once, placed 400x.
They become PCG modules — rows in the sheet.

**Scoping rule — what is geometry, what is material:**

| detail | representation |
|---|---|
| changes silhouette · casts major shadow · needs collision | **real geometry** |
| edge / frame / seam / panel **reused across assets** | **trim sheet** |
| repeats across a broad surface | tileable + normal |
| shallow, fine, seen front-on | normal map |
| localised storytelling | decal |
| dirt / wear / weathering | vertex paint |

> ⚠️ **Nanite shifts this toward geometry.** 55 meshes on Nanite; 454 k → 2.49 M tris at no
> measurable cost. Do not fake depth you could model.

- [ ] ⬜ **1. Sort the kit list by the table before modelling.** This is what makes the job
      finishable.  `[Week 5]`
- [ ] ⬜ **2. Author ONE trim sheet** — edges, panel bands, pipe strips, frames. Triplanar
      covers the big surfaces; trim covers edges and reused pieces.  `[Week 5-6]`
- [ ] ⬜ **3. Model only what the table calls geometry**  `[Week 5-6]`
- [ ] ⬜ **4. Add to `module_list.xlsx`** so PCG places them  `[Week 6]`

**Not adopted:** POM · vertex painting · decal atlases · Substance authoring — none serve the
blockout user.

## 12. Volumetric fog `[Week 6]`

- [ ] ⬜ Physically justified — the habitat has air. Atmospheric perspective sells the 13 km.

## 13. Rect lights at windows `[Week 6]`

- [x] ✅ **Not optional — they are the interior lighting mechanism.** Folded into job 5.

## 14. Source the 24 modules `[ongoing, in gaps]`

- [ ] ⬜ Megascans / Marketplace. Downloading, not authoring — never schedule it as a block.
      Every one collected is a real mesh path the validator checks and PCG places.

**Cut deliberately:** segmenting into 8-10 pieces (only served World Partition streaming;
Nanite made it moot) · rough silhouettes · material library plan.

---

# Done — 38 items

## Week 3 ✅ fully closed

- [x] ✅ Validator — 5 checks, exit 1 on error, refuses to write bad data
- [x] ✅ Test fixture — 16 planted faults → 15 errors + 1 warning
- [x] ✅ Clean sheet returns zero errors *(the control test)*
- [x] ✅ README for the tool and the fixture
- [x] ✅ `S_ModuleRow` struct — 8 fields (`Name` is the row key, not a field)
- [x] ✅ `DT_Modules` — 37 rows imported, no warnings
- [x] ✅ 500 cubes on the cylinder inner surface, correctly oriented
- [x] ✅ **Stock PCG nodes only** — no custom C++/HLSL/Blueprint needed
- [x] ✅ Found: Mesh Sampler outputs **mesh-local** coords → needs `Transform Points`
- [x] ✅ Found: samples **both** shell faces → inner r≈95,600, outer r≈99,600
- [x] ✅ `feature/python-manifest-tool` merged into `main`
- [x] ✅ Content reorganised — `Station/`, `Materials/Masters+Instances+Functions`
- [x] ✅ Lighting fixed — sun was 5 lux against a 100,000 lux reference
- [x] ✅ `WorldGridMaterial` closed — reimport did **not** fix it; bound each slot explicitly

## The join — 9 done, CHECKPOINT PASSED

- [x] ✅ `Load Data Table` node, Data Table = `DT_Modules`
- [x] ✅ `Output Type` = **Attribute Set** (the UI name for Param)
- [x] ✅ Node output inspected — 37 entries, all 8 columns present
- [x] ✅ `Match And Set Attributes` between surface points and spawner
- [x] ✅ Static Mesh Spawner → **`MeshSelectorByAttribute`**, Attribute = `Mesh`
- [x] ✅ **CHECKPOINT PASSED 2026-09-07 — 90 instances on the belt inner surface**, driven
      entirely by the DataTable. Sheet → export → reimport → regenerate works end to end.
- [x] ✅ `check_mesh_paths` enforces `.AssetName` — caught 33 more rows
- [x] ✅ All 37 spreadsheet paths corrected
- [x] ✅ Test fixture regenerated for the two new soft-path cases

## Art — 15 done, 2026-09-08

| | before | after |
|---|---|---|
| Belts x3 | 104 polys, 391 m edge | 116,736, **11.6 m** |
| Glass x3 | 104 polys | 116,736, 11.2 m |
| Endcaps B/C | 3,744 | 239,616, **7.2 m** |
| `Ring_Structure` | 2,850, 8 n-gons, 2 objects | 161,610, **9.68 m**, merged |

- [x] ✅ Endcaps · belts · glass · `Ring_Structure` subdivided; no chord-shrink
- [x] ✅ Barrel/endcap junction verified — the 133 m gap is a structural collar
- [x] ✅ Reimported — 2,490,268 tris, scale exact at 100.00x
- [x] ✅ **Per-object FBX pipeline** — the 53 MB monolith made UE re-translate the whole file
      per asset (40 min). Now 57 files, 2.6 s export, seconds to reimport. **Keep per-object.**
- [x] ✅ Nanite on 55 (off on translucent glass)
- [x] ✅ All 57 asset materials bound — map in `Tools/ue_scripts/material_slot_map.json`
- [x] ✅ `Hull_Shell_A` confirmed correct — the station is deliberately asymmetric
- [x] ✅ `Ring_Structure.001` was the missing second collar, resolved by merging
- [x] ✅ `REF_Human_1m8` origin fixed; the UE scale ref is `SKM_Quinn_LOD0` (180 uu)
- [x] ✅ Cleaned — Blender 62→59 objects, UE 58→57 assets, 61 MB stale FBX deleted

**Still open from art:** one 5-valence pole per corner on `Ring_Structure` — not blocking.

---

# Things that will bite you

| | |
|---|---|
| **PCG graphs** | Edit in the **editor**, not Python. A Python write with the editor open corrupted the graph — `Invalid PCGGraph`. |
| **World Partition** | Actors are separate packages. `save_current_level()` does **not** save them. Needs `actor.modify(True)` then `save_packages()`. Broke the level twice. |
| **Renaming assets** | **Save the level, then** delete redirectors. The other order nulled 58 mesh references. |
| **Mesh Sampler radius** | Default 10 uu = 10 cm. At 13 km that hangs the editor. Use **5000**. |
| **Cube scale** | A default cube is 100 uu — invisible at station scale. Scale points ~50×. |
| **Load Data Table** | No input pin — right-click **empty space**. |
| **Soft object paths** | Must be `Asset.Asset`. Short form spawns **nothing, silently**. Now caught by `check_mesh_paths`. |
| **Attribute names** | **Case-sensitive.** `weight` ≠ `Weight`. The UI field auto-lowercases what you type. |
| **Silent failures** | PCG often fails with no error. Turn **Debug** on each node and find the last one still holding data. |
| **Nanite hides tri counts** | `get_num_triangles(0)` on a Nanite mesh returns the **fallback**. `Hull_Shell_B` reports 46,132, is really 479,232. Verified against `Hull_Glass_A` (non-Nanite, reports its true 233,472). Check reimports by **bounding box**, not tri count. |
| **Reimport keeps materials** | It **preserves** a binding when the slot name matches. `WorldGridMaterial` only happens on **first** import. |
| **Blender Edit Mode** | Reading `object.data` with Edit Mode open returns a **stale** datablock — counts and UV arrays come back wrong or empty. Use `bmesh.from_edit_mesh()`. |
| **Names aren't evidence** | `SKM_Quinn_LOD0` is a StaticMesh, not skeletal, not Quinn — it's the 1.8 m human ref. Check the measurement, not the label. |
| **"Off-centre" needs a reference** | A value is only off-centre relative to a stated reference. Compare against the whole scene, not the part you're looking at. |

---

**The one thing:** the technical risk Week 4 was budgeted for is retired. All remaining slack
goes to art, which has none. A recruiter scrolls past grey boxes regardless of what's underneath.
