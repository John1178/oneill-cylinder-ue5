# O'Neill Cylinder — Working Checklist, Week 3 & 4

*Last updated 2026-09-07. Detail lives in `week_3_checklist.md` / `week_4_checklist.md`.
This file is the tick-list.*

---

# Week 3 — DONE

### Python tool
- [x] Validator — 5 checks, exit code 1 on error, refuses to write bad data
- [x] Test fixture — 14 planted faults, catches 13 errors + 1 warning
- [x] Clean sheet returns zero errors *(the control test)*
- [x] README for the tool and the fixture

### Into Unreal
- [x] `S_ModuleRow` struct — 8 fields (`Name` is the row key, **not** a field)
- [x] `DT_Modules` — 37 rows imported, no warnings

### PCG proof of concept
- [x] 500 cubes placed on the cylinder inner surface, correctly oriented
- [x] **Confirmed: stock PCG nodes only** — no custom C++/HLSL/Blueprint needed
- [x] Found: Mesh Sampler outputs **mesh-local** coords → needs `Transform Points`
- [x] Found: samples **both shell faces** → inner r≈95,600, outer r≈99,600

### Housekeeping
- [x] `feature/python-manifest-tool` merged into `main`
- [x] Content reorganised — `Station/`, `Materials/Masters+Instances+Functions`
- [x] Lighting fixed — sun was 5 lux against a 100,000 lux reference

### Still open from Week 3
- [ ] Mesh assets default to `WorldGridMaterial`
  *(level looks right only because actors carry component overrides)*
  → fixed by reimporting the FBXs, which is happening anyway for subdivision

---

# Week 4 — TO DO

## 1. Finish the join
*Do this first — it's short.*

- [x] Add node **`Load Data Table`**, set Data Table = `DT_Modules`
  > ⚠️ It has **no input pin**. Right-click empty space — dragging from a pin filters it out of the list.
- [x] `Output Type` = **Attribute Set** (the UI name for Param). Param is probably what `Match And Set Attributes` wants.
- [x] Inspect the node output — confirm 37 entries carrying
  `Category` / `Zone` / `Belt` / `Mesh` / `Weight` / `RotationMode` / `Clearance` / `Source`
- [x] Add **`Match And Set Attributes`** between surface points and spawner:
  ```
  match_attributes      = false      (no zone matching yet)
  use_weight_attribute  = true
  weight_attribute      = Weight
  ```
- [x] Static Mesh Spawner → Mesh Selector Type = **`MeshSelectorByAttribute`**, Attribute Name = `Mesh`
- [x] ✅ **CHECKPOINT PASSED 2026-09-07** — **90 instances spawned on the belt inner surface**, driven entirely by the DataTable. Edit spreadsheet → re-export → reimport → regenerate works.

### The bug that ate an hour, and the rule it produced
```
/Game/Meshes/Placeholders/SM_Cube            silently spawns NOTHING
/Game/Meshes/Placeholders/SM_Cube.SM_Cube    works
```
Soft object paths need the `Asset.Asset` form. **No error, no warning** — PCG resolves it to
nothing and skips the point. Every other check passed, which is what made it expensive.

- [x] `check_mesh_paths` now enforces the `.AssetName` suffix — caught 33 more rows that
      would each have failed the same silent way
- [x] All 37 spreadsheet paths corrected

### Still open on this section
- [ ] **Weighting does not work.** `Match Weight Attribute` auto-lowercases to `weight`,
      but the column is `Weight` and PCG attribute names are case-sensitive. Currently
      unticked, so selection is unweighted and the `Weight` column is doing nothing.
      Try the field's dropdown rather than typing.
- [ ] Update `tests/module_list_BROKEN.xlsx` — it holds old short-form paths, so its
      results no longer match the count in its README.

## 2. Make the surface swappable
*This is the portfolio thesis.*

- [ ] Filter out the outer shell face (by radius, or by normal direction)
- [ ] Wrap surface sampling in its own subgraph
  ```
  input  = which mesh
  output = points carrying position + rotation
  ```
- [ ] Build a **flat-ground version** of the same subgraph, same output contract
- [ ] ✅ **CHECKPOINT** — the same downstream graph runs on both, unchanged

> **Why this matters:** the claim is *"the surface is an input, not an assumption."*
> One surface = a cylinder project with ambitious framing. Two surfaces = a tool.

## 3. Zoning (Layer 1)

- [ ] Split the belt into zones along its length (ranges by Y, hand-authored)
- [ ] Write a `Zone` attribute onto each surface point
- [ ] Set `Match And Set Attributes` to match `Zone` → `Zone`
- [ ] ✅ **CHECKPOINT** — residential modules only appear in the residential stretch

## 4. Save the failure shot

- [ ] Screenshot the standard Surface Sampler **failing** on the cylinder — points firing into space, cubes on their sides

> You'll produce this for free while things don't work. **Save it when it happens.** A two-panel before/after sells the whole project in two seconds, and almost nobody does it.

## 5. Art track
### 🔴 The actual risk — nothing done since Week 1

- [ ] **Subdivide the meshes** ← highest priority
  `Hull_Shell_A` = 2,190 tris across 13.4 km. Belts = 208 tris each.
  **Split into segments**, don't just subdivide in place. Fixes four things at once:
  - shadow terminator artifacts (visible facets on the dome)
  - Lumen surface cache coverage
  - World Partition streaming + culling
  - gives PCG denser, smoother surfaces to sample
- [ ] Reimport the FBXs *(also restores default material slots)*
- [ ] Replace `M_Temp` — it's on 34 meshes including all 3 hull shells + greenhouses
- [ ] Reference board (PureRef) — NASA Ames archive, public domain, exact subject
- [ ] Rough silhouettes, 6 categories
- [ ] Material library plan
- [ ] Start downloading the 24 sourced modules (Megascans / Marketplace)

## 6. Lighting
*Carried, not blocking.*

- [ ] **Real space cubemap** ← biggest single visual win available
  UDS `FlatCubemap` is a dark placeholder, so `Sky Light Intensity` is multiplying nothing
- [ ] Volumetric fog — physically justified here, **the habitat has air**. Atmospheric perspective is what will sell the 13 km scale.
- [ ] Rect lights at the windows — placed but switched **off**. An A/B showed them swamped by sun already entering the glass. Revisit after ambient exists.
- [ ] Shadows vanishing at distance — unresolved. Use `Show > Visualize > Virtual Shadow Map`.
  > VSM uses **clipmaps**, not the old Dynamic Shadow Distance — that setting is not the mechanism.

---

# Things that will bite you
*Learned the hard way.*

| | |
|---|---|
| **PCG graphs** | Edit in the **editor**, not through Python. Python writes while the editor was open corrupted the graph — `Invalid PCGGraph`, nodes silently refused to place. |
| **World Partition** | Actors are **separate packages**. `save_current_level()` does **not** save them. Needs `actor.modify(True)` then `save_packages()`. This broke the level twice. |
| **Renaming assets** | **Save the level, then** delete redirectors. The other way round nulled 58 mesh references. |
| **Mesh Sampler radius** | Default is 10 uu = 10 cm. At 13 km scale that will hang the editor. Use **5000**. |
| **Cube scale** | A default cube is 100 uu — invisible at station scale. Scale points up ~50× or you'll think nothing spawned. |
| **Load Data Table** | No input pin — right-click **empty space** to add it. |
| **Soft object paths** | Must be `Asset.Asset`. The short form spawns **nothing, silently**. Now caught by `check_mesh_paths`. |
| **Attribute names** | **Case-sensitive.** `weight` ≠ `Weight`. The UI field auto-lowercases what you type. |
| **Silent failures** | PCG often fails with no error at all. Turn **Debug** on each node in turn and find the last one that still has data — that halves the search space instantly. |

---

# The one thing to remember

**The technical risk Week 4 was budgeted for is already retired** — curved-surface sampling works with stock nodes.

**All the remaining slack should go to art, which has none.**
A recruiter scrolls past grey boxes no matter what is underneath them.
