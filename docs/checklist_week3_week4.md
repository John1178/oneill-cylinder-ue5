# O'Neill Cylinder — Checklist, Week 3 & 4

*rev 12 · 2026-09-09 · ordered by execution: **1 = do first**. Detail in `week_3_checklist.md` / `week_4_checklist.md`*

**46 done · 19 open · 71% complete.** Today **Wed 9 Sep**; Week 4 ends **Fri 11 Sep**.

| # | job | items | when |
|---|---|---|---|
| **1** | **Swappable surface** ⭐ *the thesis* | 2 | ✅ **CHECKPOINT PASSED Wed 9** |
| **2** | Failure shot | 1 | **Wed 9** *(free byproduct of 1)* |
| **3** | Replace `M_Temp` | 1 | **Wed 9 PM → Thu 10** |
| **4** | Reference board — fill the gaps | 1 | **Thu 10** |
| **5** | Lit windows | 1 | **Fri 11 AM** |
| **6** | `Weight` case fix | 1 | **Fri 11 PM** *(buffer)* |
| | — end of Week 4 — | **9** | |
| 7 | ~~City-gen design block~~ ✅ → [`layer_contract.md`](layer_contract.md) | 3 open | Week 5 |
| 8 | Zoning | 4 | Week 5 |
| 9 | Real space cubemap | 1 | Week 5 |
| 10 | Shadows at distance | 1 | Week 5 |
| 11 | Detail meshes / kitbash | 1 | Week 5-6 |
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

## 1. Swappable surface — *the thesis* `[Wed 9 AM]`

> One surface = a cylinder project. Two surfaces = a tool.

- [ ] ⬜ Filter out the outer shell face (by radius, or normal direction)
- [x] ✅ **`SG_SurfaceSource` built 2026-09-09.** Contains `Mesh Sampler` + `Get Actor Data` +
      `Copy Points`. `Transform Points` deliberately stayed OUTSIDE — the x50 is a
      placeholder-cube hack, not surface logic, and L0 emits only points.
      Collapsed via the graph editor's **Collapse into Subgraph**.

      **Three exposed parameters** — wired to override pins revealed by each node's ⌄ chevron:
      ```
      SurfaceMesh     -> Mesh Sampler . StaticMesh
      SamplingRadius  -> Mesh Sampler . SamplingRadius     5000 belt / 5 plane
      SurfaceTag      -> Get Actor Data . ActorSelectionTag
      ```
      **Swapping surfaces is now three values on the Subgraph node.** The subgraph is never
      opened and nothing downstream is touched.

      > Graph parameters live in a separate **"Graph Parameters"** tab (Window menu, or the
      > "Open Graph Parameters" button in the graph Details panel) — NOT in Details itself.
      > Drag a parameter onto the canvas to make a `Get Graph Parameter` node.
- [x] ✅ Build a flat-ground version — `SM_Plane2`, 520 x 500 m, tagged `SurfaceSource`
- [x] ✅ **CHECKPOINT PASSED 2026-09-09** — same downstream graph on both surfaces, unchanged.
      7 cubes on the plane, scale 50 uniform, inside the plane bounds. `Load Data Table` →
      `Match And Set` → `MeshSelectorByAttribute` untouched between the two runs.

      **How the surface became an input:**
      ```
      before   Transform Points offset = (-221760.55, 49112.33, 175805.30)
               = the belt actor's address, typed in by hand
      after    Get Actor Data (tag "SurfaceSource", Get Single Point)
               -> Copy Points [Source] <- Mesh Sampler
               swapping surface = move the tag + point the sampler at another mesh
      ```

      **Three baked assumptions the flat twin exposed** — all invisible while only one
      surface existed:
      | assumption | why it hid | how it surfaced |
      |---|---|---|
      | typed world offset | it *was* the belt's address | points flew to the belt |
      | `Copy Points` = `Relative` scale | belt actor scale is **1**, so ×1 is invisible | plane scale 519.8 → **26 km cubes** |
      | sampling radius 5000 | tuned for a 7,900 m belt | 100 uu plane asset → **1 point** |

      > **This is the argument for building the twin even though the cylinder already worked.**
      > A second surface does not just prove the claim — it *finds* the assumptions. Each of
      > these read as correct until something had a different scale.

## 2. Failure shot `[Wed 9]`

- [ ] ⬜ Screenshot the stock Surface Sampler **failing** on the cylinder — points into space,
      cubes on their sides. You get this free while job 1 breaks. Save it when it happens.

## 3. Replace `M_Temp` — 33 meshes `[Wed 9 PM → Thu 10]`

- [ ] ⬜ 3 hull shells, 24 greenhouse modules, 6 supports. **Hull shells first** — they are the
      largest surfaces in the level and still running a placeholder. Biggest visual win available.

## 4. Reference board — fill the gaps `[Thu 10]`

- [ ] ⬜ Board exists but is all wide vistas. **Missing: close-up hull material · structural /
      kitbash detail · window-to-land junction · night + lit windows · scale anchors.**
      Group by *task*, not by subject. NASA Ames (Guidice / Don Davis, 1970s) is public domain
      and is literally O'Neill interiors — the only reference you could legally show in a breakdown.

## 5. Lit windows `[Fri 11 AM]`

- [ ] ⬜ Warm interior light through `Hull_Glass_A/B/C`. Meshes already exist; `M_Emissive` sits
      unused in `/Game/Materials/Masters`. Fixes scale, contrast and story in one change — it is
      both the art job and the top lighting job, not two.

## 6. `Weight` case fix `[Fri 11 PM]`

- [ ] ⬜ `Match Weight Attribute` auto-lowercases to `weight`; the column is `Weight`; PCG is
      case-sensitive. Try the dropdown rather than typing.

---

## 7. City generation — design block ✅ DONE 2026-09-09

**Output: [`layer_contract.md`](layer_contract.md).** Read it before building 8 onward.

- [x] ✅ **1. Layer stack defined** — `L0 surface → L1 density → L2 streets → L3 lots →
      L4 selection → L5 spawn`. L4/L5 already work; L0 partly; L1-L3 not started.
- [x] ✅ **2. Contract between layers written** — every layer consumes points-with-attributes
      and emits points-with-attributes, and never knows what produced its input. Full
      attribute vocabulary table in the contract.
- [x] ✅ **3. Authoring vs generation decided** — three artist controls: **Excel** (what exists),
      **hand-drawn road splines** (where the city goes — doubles as the street skeleton), and
      **density** (village vs downtown). Painted masks deferred, probably permanently — too
      expensive on a curved surface.
- [x] ✅ **4. Determinism decided** — one global seed now; per-region seeds documented as
      future work. Named explicitly because artists won't adopt a system where fixing one
      street re-rolls the city.
- [x] ✅ **5. Data vs graph split** — if a non-technical person should be able to change it,
      it goes in the spreadsheet. That is the argument for the validator tool.

**Reframe this produced:** it is not a city generator, it is a **settlement generator** — the
artist decides whether a stretch is a village or a downtown. Same graph, different input.
The surface is an input; so is the density; so is the road layout.

**Roads are hand-drawn, deliberately.** CityEngine's own most common production use imports real
road data and generates everything else. The procedural value is in blocks → lots → buildings,
all of which sit *downstream* of the streets.

### Decisions this left open

- [ ] ⬜ **7a. L3 — frontage-only or full block subdivision?** Frontage-only lines buildings
      along the roads and leaves interiors empty; block subdivision is the real "city" and is
      the biggest single item in the system. **Recommend frontage-only first** — it produces
      a working city immediately and subdivision slots in above L3 later without touching any
      other layer.  `[Week 5]`
- [ ] ⬜ **7b. Fix the Belt/Zone schema.** `Belt = A/B/All` and `Zone = Residential/Industrial/
      Service/-`, but there are **three** belt meshes named Residential/Industrial/Agriculture.
      `BLD_002` says Belt `A` — matches no mesh. `BLD_006` says Zone `Service` — does not exist,
      so it can never place. **Proposed: `Belt` becomes Residential/Industrial/Agriculture/All,
      `Zone` deleted.** ~30 min: validator, Excel, `CSV_COLUMNS`, `S_ModuleRow`, re-export,
      reimport. **Blocks job 8.**  `[Week 5, before 8]`
- [ ] ⬜ **7c. Clearance enforcement.** The column exists and nothing reads it. Does L3 enforce
      spacing, or does L1 density handle it alone?  `[Week 5]`

## 8. Zoning (Layer 1) `[Week 5]`

- [ ] ⬜ Split the belt into zones along Y, hand-authored
- [ ] ⬜ Write `Zone` onto each surface point
- [ ] ⬜ `Match And Set Attributes` → match `Zone` → `Zone`
- [ ] ⬜ **CHECKPOINT** — residential modules only in the residential stretch

## 9. Real space cubemap `[Week 5]`

- [ ] ⬜ UDS `FlatCubemap` is a dark placeholder, so `Sky Light Intensity` multiplies nothing.
      Fixes ambient across the whole level in one change.

## 10. Shadows vanishing at distance `[Week 5]`

- [ ] ⬜ `Show > Visualize > Virtual Shadow Map`. Measured: `cast_far_shadow = 0` on all 60
      actors, `MaxPhysicalPages = 4096` — two untested candidates.

## 11. Detail meshes / kitbash `[Week 5-6]`

- [ ] ⬜ Ribs, seams, vents, struts, window framing. **The only item that cannot be shortcut** —
      protect time for it. Build as *separate objects*, never edited into the shells. One rib
      modelled once, placed 400×. They become PCG modules, i.e. rows in the sheet.

## 12. Volumetric fog `[Week 6]`

- [ ] ⬜ Physically justified — the habitat has air. Atmospheric perspective sells the 13 km.

## 13. Rect lights at windows `[Week 6]`

- [ ] ⬜ Placed but switched off; an A/B showed them swamped by sun already entering the
      non-shadow-casting glass. Job 5 may remove the need entirely.

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

## Art — 15 done, all 2026-09-08

| | before | after |
|---|---|---|
| Belts ×3 | 104 polys, 391 m edge | 116,736, **11.6 m** |
| Glass ×3 | 104 polys | 116,736, 11.2 m |
| Endcaps B/C | 3,744 | 239,616, **7.2 m** |
| `Ring_Structure` | 2,850, 8 n-gons, 2 objects | 161,610, **9.68 m**, 100% quads, merged |

- [x] ✅ **Endcaps subdivided** — both to 7.2 m edge, no shrinkage (boundary edges pinned)
- [x] ✅ **Belts subdivided** — 391 m → 11.6 m edge. No chord-shrink: axial 7900.20 → 7900.11
- [x] ✅ **Glass subdivided** — 11.2 m edge
- [x] ✅ **`Ring_Structure` subdivided + both collars merged** — 100% quads, zero n-gons
- [x] ✅ **Barrel/endcap junction verified** — the 133 m gap is a structural collar, not a seam
- [x] ✅ **Reimported into UE** — 2,490,268 tris, scale verified exact at 100.00×
- [x] ✅ **Reimport pipeline fixed** — the 53 MB monolith made UE re-translate the whole file
      once per asset (40 min, RAM past 16 GB). Now per-object FBX: 57 files, **2.6 s** to
      export, `asset_import_data` repointed per asset. **Keep exporting per-object.**
- [x] ✅ **Nanite on 55 meshes** — off on the 3 translucent glass
- [x] ✅ **All 57 asset materials bound** — map in `Tools/ue_scripts/material_slot_map.json`
- [x] ✅ **`Hull_Shell_A` confirmed correct** — the station is deliberately asymmetric (greenhouse
      cluster 2.3 km past the top endcap). Do not centre it.
- [x] ✅ **`Ring_Structure.001` resolved by merging** — it was the missing second collar, not a
      duplicate. That end of the station had no UE asset at all.
- [x] ✅ **`REF_Human_1m8` origin** set to bounds centre, world position unchanged
- [x] ✅ **Human scale ref found already in UE** — `SKM_Quinn_LOD0`, 180.0 uu tall
- [x] ✅ **Blender cleaned** — 62 → 59 objects, 4 orphan mesh datablocks purged
- [x] ✅ **UE cleaned** — 58 → 57 assets, 61 MB of stale FBX deleted, **zero on `WorldGridMaterial`**

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
