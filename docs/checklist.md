# O'Neill Cylinder — Project Checklist

*rev 14 · 2026-09-14 · ordered by execution: **1 = do first**.*

> **This is the one rolling checklist for the whole project.** It is never replaced by a new
> weekly file. Corrections land here and nowhere else — splitting per week is exactly how job 9
> kept a claim that had already been disproven. Archived detail: `week_1_2_checklist.md`,
> `week_3_checklist.md`, `week_4_checklist.md`.

**52 done · 60 open · 46% complete.** Updated **Mon 14 Sep 2026**.

| # | job | items | when |
|---|---|---|---|
| **1** | ~~Swappable surface~~ ⭐ *the thesis* | ✅ | **CLOSED Wed 9** |
| **3** | ~~Replace `M_Temp`~~ | ✅ | **done Mon 14** |
| **4** | Reference board — fill the gaps | 1 | **Thu 10** |
| **5** | Lit windows | 1 | **Fri 11 AM** |
| **6** | Weighted module selection | 1 | **Fri 11 PM** *(buffer)* |
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
| 15 | Second belt | 1 | Week 6-7 |
| 16 | L1 Density | 3 | Week 6 |
| 17 | L2 Streets | 4 | Week 6-7 |
| 18 | L3 Lots — frontage-only | 2 | Week 7 |
| 19 | Presets | 2 | Week 7 |
| 20 | Editor panel + reimport script | 3 | Week 7 |
| 21 | Optimisation pass | 3 | Week 8 |
| 22 | Polish — shots and captures | 3 | Week 9 |
| 23 | Delivery | 4 | Week 10 |
| P | Night / day-night mechanism | 3 | *parked* |

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

## 3. Replace `M_Temp` ✅ DONE 2026-09-14 *(reopened and fixed same day)*

- [x] ✅ 33 mesh **assets** reassigned: `MI_Structural_HullShell` x3 · `MI_Greenhouse` x30, both
      parent to `M_Structural` (triplanar + LWC). ⚠️ `M_Temp` was two-sided, `M_Structural` is not.
- [x] ✅ **Fixed in the level 2026-09-14.** 33 component overrides cleared; actors fall back to the correct
      asset defaults. Verified three ways: renders 30x `MI_Greenhouse` + 3x `MI_Structural_HullShell`,
      **0** saved actor files contain `M_Temp`, registry referencers **0** after rescan.
      `M_Temp` itself is now unreferenced and deletable.

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
- [x] ✅ **`M_Window` glass rebuilt on Substrate 2026-09-11.** Was `Volumetric NonDirectional`
      (the smoke/dust lighting mode) + opacity-as-transparency = grey film. Now Slab -> Coverage
      Weight -> Front Material, Colored Transmittance, Surface ForwardShading. **The killer was
      `Sub Surface Type: Diffusion -> Simple Volume`** — a Details dropdown, not a pin, stamped
      at Substrate auto-conversion and never re-derived. Full recipe in `ue_working_rules.md`.
- [ ] ⬜ **Re-point the orphaned day/night rig.** `NightOpacity`/`DayOpacity`/`DayNightBlend`
      Lerp still runs into `Opacity Override`, which Substrate greys out and ignores. Move it
      onto the tint, or delete it.
- [x] ✅ **`r.Substrate.ProjectGBufferFormat` = 1** (verified 2026-09-11).
- [x] ✅ **Glass reflections fixed** — `r.Lumen.TranslucencyReflections.FrontLayer.EnableForProject=1`
      added to `DefaultEngine.ini`. Ships **OFF**; without it translucent surfaces only get the
      low-quality Radiance Cache (glossy, no mirror). `GlassTint` -> 0.97/1.0/0.98 as an
      **instance override** on `MI_Window_Belt` (first override on that instance).
- [ ] ⬜ Tune the rect lights warm and wire to `MPC_DayNight` (`WindowEmissiveIntensity`,
      `WindowEmissiveColor`, `AmbientTint`). Currently 6500 K, `use_temperature=False`.
- [ ] ⬜ Judge whether contact shadows are missed — all 3 rect lights are `cast_shadows=False`.

## 6. Weighted module selection `[Fri 11 PM]`

- [x] ✅ **WORKING 2026-09-10.** Cube and cone spawning in weighted proportion.
      **Real cause: `bUseWeightAttribute` is `InlineEditConditionToggle`** — it has no row of its
      own in Details, it is the small unlabelled checkbox *left of* the `Match Weight Attribute`
      field. The field accepts and displays a typed name while doing nothing until it is ticked.
      Case was never involved. `Match Attributes` stays **off** = random weighted selection.
- [ ] ⬜ **Two test edits live only in the DataTable** — `BLD_006` -> `SM_Cone` (job 6) and
      `BLD_004` -> `Shape_Cylinder` (job 8 prep). Re-exporting `module_list.xlsx` reverts both, and
      `Shape_Cylinder` is StarterContent (gitignored) so it also breaks on clone. Move both into
      the xlsx with repo-safe meshes, or drop them. Backups in `scratchpad/`.

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
- [ ] ⬜ **7e. Correct `layer_contract.md`** — Open decision 2 still proposes the withdrawn Belt/Zone
      rewrite as pending, and the Presets table + Attribute vocabulary read `Belt` as a belt name.
      Left as-is it re-triggers the same wrong fix (the job 9 failure mode).

## 7d. Terrain on the belt `[Week 5-6]`

**A separate single-sided mesh laid on the belt, not a displacement of it.** The belt stays as
structure; the terrain becomes what L0 samples. Full design in `layer_contract.md`.

- [x] ✅ **1. Source:** real-world DEM -> **Gaea 2.0** -> heightmap + masks (the known
      "Real to Unreal" workflow). Gaea stays — it is the **mask generator** that drives PCG.
- [x] ✅ **2. Wrap dissolved.** Terrain is generated in **unrolled 2D** (7.9 km x 1 km) and
      mapped by UV. **Never feed the belt into Gaea** — it rasterises meshes to heightfields and
      destroys the curve. UE Landscape also ruled out: flat grid, and WPO curving is visual only.
- [x] ✅ **3. Belt measured 2026-09-11:** 116,744 verts / 233,472 tris, **11.6 m** avg edge,
      994.73 x 7900.11 x 162.61 m, area 15.7 km² (both shell faces). Existing `UVMap` is a packed
      material unwrap with **4.3x texel-density spread** — unusable for terrain, and now moot.
- [x] ✅ **Scope settled 2026-09-11: Residential belt only** (prove it, then repeat on the
      others). Terrain **sits on** the belt; the belt stays underneath. **ONE mesh, no chunking**
      — Nanite already splits into 128-tri clusters and page-streams them; 630k tris ≈ **9 MB**.
      World Partition streams *actors* not geometry, so one big actor is always-loaded but costs
      only that 9 MB. Chunking would add UV, export and seam work to solve nothing.
- [ ] ⬜ **4. Generate the terrain sheet** — single-sided, radius ~954 m + base offset,
      7.9 km x ~1 km, uniform grid at **5 m** spacing (~630k tris). Clean 0-1 UV.
- [ ] ⬜ **4b. On import, check Nanite fallback settings** (Fallback Relative Error / Triangle
      Percent). Complex-as-simple collision uses the **fallback**, not the Nanite geometry — too
      aggressive and you walk on a coarser shape than you see. This is what made the sports car
      misbehave on the belt.
- [ ] ⬜ **5. Author the relief mask** — amplitude across the **width**: ~25-30% centre,
      ~100% toward both edges, capped before the glass line. Edge relief ~200 m, centre ~50-60 m.
- [ ] ⬜ **6. Water sheet** — curved, constant radius (~950 m), under the terrain base.
      Rivers and lakes **emerge** from terrain below that radius; they are not authored.
- [ ] ⬜ **7. Repoint L0** — `SurfaceMesh` becomes the terrain.  `[Week 6]`
- [ ] ⬜ **8. Retune `SamplingRadius`** — already a subgraph parameter, so a value change.
- [ ] ⬜ **9. Wire the Gaea masks into PCG:** `Mesh Sampler` -> tick **`bExtractUVAsAttribute`**
      (ships OFF), then `Get Texture Data` + `Sample Texture` with
      **TextureMappingMethod = UVCoordinates**. Gives L1 an image-authored density source.
- [ ] ⬜ **10. Slope + aspect rules** — max-slope cull, align-to-slope, density by flatness.
      **The feature terrain exists to unlock.**  `[Week 6]`

**Why it is core, not decoration:** a smooth cylinder has no slope to read, so placement looks
like any scatter node. Terrain makes the system *legible* and unlocks slope rules. It is also a
third surface — flat plane / smooth cylinder / varied cylinder — which is a stronger argument
than two.

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
- [ ] ⬜ **5. Texture pass on `M_Structural`** — measured 2026-09-14: one generic placeholder texture
      (`Textures/images`, also on `MI_Belt_Agriculture`), no normal map, no grime parameter.  `[Week 6]`

**Not adopted:** POM · vertex painting · decal atlases · Substance authoring — none serve the
blockout user.

## 12. Volumetric fog `[Week 6]`

- [ ] ⬜ Physically justified — the habitat has air. Atmospheric perspective sells the 13 km.

## 13. Rect lights at windows `[Week 6]`

- [x] ✅ **Not optional — they are the interior lighting mechanism.** Folded into job 5.

## 14. Source the 24 modules `[ongoing, in gaps]`

- [ ] ⬜ Downloading, not authoring — never schedule it as a block. Every one collected is a
      real mesh path the validator checks and PCG places.
- [ ] ⬜ **Audit packs already owned before buying anything.** `Industrial Infrastructure`
      (Sierra Division) and `Ruined Modern Buildings Pack` (Madyan Studios) are already in the
      Fab library and sit squarely on the kitbash rows.
- [ ] ⬜ **Back up the 4 local Bridge downloads** (`Documents/Megascans Library`, 636 MB) before
      Bridge is retired — Bridge-era downloads cannot be re-fetched once the app goes offline.
      Library access is via **Fab** now; Bridge is Deprecated.

**Scope note:** Megascans covers **17 of 37 rows** (VEG 8 + HAB 5 + WEAR 4 — scanned nature,
ground, grime) and those are now free and owned. The other **20** (BLD 7 + STR 6 + INF 7) are
sci-fi kitbash, which Megascans never had — that is where sourcing effort actually goes.
- [ ] ⬜ **Prefer CC0 over Fab for this project** — Poly Haven / ambientCG / Textures.com free
      tier. Fab + Marketplace assets **cannot ship in the public repo**; CC0 can, so the repo
      stays runnable on clone. That is worth more in a portfolio than better scans.

**Cut deliberately:** segmenting into 8-10 pieces (only served World Partition streaming;
Nanite made it moot) · rough silhouettes · material library plan.


## 15. Second belt `[Week 6-7]`

- [ ] ⬜ Repeat terrain + PCG on a second belt once Residential is proven. The schedule cut Belt C and
      planned two; the level has three belt meshes — pick the second, decide if the third is cut.

## 16. L1 Density `[Week 6]`  *layer_contract: not started*

- [ ] ⬜ Write `Density` (0-1) onto points — source is the Gaea mask (7d.9).
- [ ] ⬜ Threshold cull — points below it are removed here; nothing downstream sees them.
- [ ] ⬜ `Scatter` / `Rows` switch — the one logic branch in the system (Rows = farm, orchard).

## 17. L2 Streets `[Week 6-7]`  *layer_contract: not started*

- [ ] ⬜ Artist-drawn spline actors -> `PCG Spline Sampler` (oriented points every N m).
- [ ] ⬜ Align points to the cylinder surface normal; spawn street tiles (`Ground_Paved_Street`, `Pathway_Straight`).
- [ ] ⬜ Write `DistToRoad` + `RoadDir`; L5 reads `RotationMode = AlignToRoad` from them.
- [ ] ⬜ **Test the tile seam at project scale** — never verified. Fallback: shorter tiles or `DeckPlate_Corner`.

## 18. L3 Lots — frontage-only `[Week 7]`

- [ ] ⬜ Buildings line the roads via `DistToRoad`; block interiors stay green. Emits `LotSize`, `Frontage`.
- [ ] ⬜ *(stage 2, optional)* 30-min spike: boundary polygon + two splines -> `Polygon2D Operation`
      `CutWithPaths` -> check the blocks come out clean. Unverified.

## 19. Presets `[Week 7]`  *demo shot 1*

- [ ] ⬜ City / Town / Farm / Factory / Countryside as **data** — an eligibility filter + parameter set, no new logic.
- [ ] ⬜ Needs 7b-new first: the Presets table filters on `Belt`, which is a quality tier, not a belt name.

## 20. Editor panel + reimport script `[Week 7]`  *yours to write*

- [ ] ⬜ **`import_datatable.py`** — reimports `DT_Modules` from the exported CSV in one command, no import dialog.
- [ ] ⬜ **Editor Utility Widget** — seed, density, zone split, preset; runs export -> validate -> reimport ->
      regenerate. The validator stays a CLI with exit codes (Week 3 decision); the panel calls it.
- [ ] ⬜ **CHECKPOINT** — the panel regenerates a belt without opening the PCG graph.

## 21. Optimisation pass `[Week 8]`

- [ ] ⬜ Baseline **before** any change: draw calls, frame time, and PCG regeneration time.
- [ ] ⬜ HLOD, instancing, LOD pass — then capture **after**. One clear round, not two.
- [ ] ⬜ *(deferred)* Drive `CastShadow` / `CullDistance` from the sheet via `static_mesh_component_property_overrides`.

## 22. Polish — shots and captures `[Week 9]`

- [ ] ⬜ Hero shots on the residential belt.
- [ ] ⬜ Capture the tool UI and PCG debug views.
- [ ] ⬜ Practical lights on spawned lamp modules (`INF_004` street lamp, `INF_005` overhead strip) — needs job 14.

## 23. Delivery `[Week 10]`

- [ ] ⬜ **Demo video** cut to the shot list in `layer_contract.md` (preset -> density -> road -> surface swap -> sheet edit).
- [ ] ⬜ **Breakdown page** — lead with what broke on the cylinder and how it was fixed.
- [ ] ⬜ Resume bullets.
- [ ] ⬜ Document the Git workflow — branching, LFS, what is gitignored and why. *(partial since Week 1-2)*

## P. Night / day-night mechanism *(parked 2026-09-10 — PCG + terrain first)*

- [ ] ⬜ Wing shutter rotation driven by `MPC_DayNight.DayNightBlend` — never built (`design_day_night.md`).
- [ ] ⬜ `M_Emissive` starfield LED on the wing's inner face — measured 2026-09-14: **no texture parameters**.
- [ ] ⬜ Day/night presets off test values, then day/night hero shots. Job 5's rect-light wiring belongs here too.

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
| **Attribute names** | **NOT case-sensitive** — old rule disproven in engine source 2026-09-10. PCG keys attributes on `FName` (case-insensitive) and never lowercases what you type. |
| **Silent failures** | PCG often fails with no error. Turn **Debug** on each node and find the last one still holding data. |
| **Nanite hides tri counts** | `get_num_triangles(0)` on a Nanite mesh returns the **fallback**. `Hull_Shell_B` reports 46,132, is really 479,232. Verified against `Hull_Glass_A` (non-Nanite, reports its true 233,472). Check reimports by **bounding box**, not tri count. |
| **Reimport keeps materials** | It **preserves** a binding when the slot name matches. `WorldGridMaterial` only happens on **first** import. |
| **Read back what renders** | A mesh asset's default material is not what a placed actor shows — a component `override_materials` entry wins. Job 3 was ticked done after checking assets while 33 actors still rendered `M_Temp`. Read `component.get_materials()`. |
| **Blender Edit Mode** | Reading `object.data` with Edit Mode open returns a **stale** datablock — counts and UV arrays come back wrong or empty. Use `bmesh.from_edit_mesh()`. |
| **Names aren't evidence** | `SKM_Quinn_LOD0` is a StaticMesh, not skeletal, not Quinn — it's the 1.8 m human ref. Check the measurement, not the label. |
| **"Off-centre" needs a reference** | A value is only off-centre relative to a stated reference. Compare against the whole scene, not the part you're looking at. |

---

**The one thing:** the technical risk Week 4 was budgeted for is retired. All remaining slack
goes to art, which has none. A recruiter scrolls past grey boxes regardless of what's underneath.
