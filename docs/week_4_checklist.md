# Week 4 — PCG on the Curved Surface (System 4)

**Schedule says:** "PCG graph, single belt, placeholder cubes."
**Friday checkpoint:** one belt generates on the curved surface, driven by the DataTable.

**Flagged as the likely overrun week.** The original guide expected the curved-surface alignment
to need a custom Blueprint or line-trace approach. **It doesn't — that was proven on 2026-09-04**
with stock nodes. So the risk that was budgeted for is already retired, and Week 4 has more slack
than planned. Spend it on the art track, which does not.

---

## The thesis this week has to serve

Not "I made a procedural city." That's common and reads as a tutorial follow-along.

> **Procedural tools assume flat ground. I built a placement system where the surface is an input
> instead of an assumption, so the artist designs the shape and the tools follow.**

Consequences for how the work is built:
- The surface layer must be a **separate subgraph** that can be swapped, not inlined
- Everything downstream consumes "points carrying position + normal" and never knows what
  produced them
- **The claim is only proven if it runs on two surfaces.** Flat ground AND the cylinder.
  One surface and it's just a cylinder project with ambitious framing.

---

## 1. Finish the join — the first task

The spawner currently uses a hardcoded cube. `DT_Modules` has never been connected.

- [x] Add **`Load Data Table`** node, set `Data Table` = `DT_Modules`
      - node has **no input pin** — right-click empty space, don't drag from a pin
      - `Output Type` = **Attribute Set** (the UI name for Param). Confirmed: the
        `Match Data` pin is typed `Param` and rejects Point.
- [x] Inspect its output — confirm 37 entries carrying `Category`, `Zone`, `Belt`, `Mesh`,
      `Weight`, `RotationMode`, `Clearance`, `Source`
- [x] Add **`Match And Set Attributes`** between the surface points and the spawner

      Pass 1, no matching — just prove the join:
      ```
      match_attributes      false
      use_weight_attribute  true
      weight_attribute      Weight
      ```
      Every point gets a random module weighted by the spreadsheet. Trees next to warehouses.
      That is fine — it proves data is flowing.

- [x] Switch the Static Mesh Spawner to **`MeshSelectorByAttribute`**, Attribute Name = **`Mesh`**
- [x] **CHECKPOINT PASSED 2026-09-07** — 90 instances spawned on the belt inner surface,
      driven entirely by the DataTable. Spreadsheet -> CSV -> DataTable -> PCG -> level.

#### The bug that cost an hour
```
/Game/Meshes/Placeholders/SM_Cube            silently spawns NOTHING
/Game/Meshes/Placeholders/SM_Cube.SM_Cube    works
```
Soft object paths need the `Asset.Asset` form. **No error, no warning** — PCG resolves it to
nothing and skips the point. Epic's docs confirm the canonical form is `/package/path.assetname`.

- [x] `check_mesh_paths` now enforces `.AssetName` — immediately caught 33 more rows
- [x] All 37 spreadsheet paths corrected
- [x] Test fixture regenerated: **16 faults -> 15 errors + 1 warning**, including two new
      soft-object-path cases

#### Still open on this section
- [ ] **Weighting does not work.** The `Match Weight Attribute` field auto-lowercases to
      `weight`; the column is `Weight` and PCG attribute names are case-sensitive. Selection
      is currently unweighted. Try the field's dropdown instead of typing.
- [ ] *(optional)* Prove the soft-path rule on your own setup — revert one row to the short
      form, reimport, regenerate, watch the cube count drop. The DataTable was reimported in
      the same step as the path fix, so strictly the cause is documented-and-inferred, not
      measured.

---

## 2. Clean up the surface layer

- [ ] **Filter out the outer shell.** The belt is a shell and both faces get sampled.
      Inner ≈ radius 95,600, outer ≈ 99,600. Filter by radius or by normal direction.
- [ ] **Wrap the surface sampling in a subgraph** — `SG_SurfaceSource` or similar.
      Input: which mesh. Output: points with position + rotation.
      This is the swappable piece; everything else depends on it being isolated.
- [ ] **Build a flat-ground version of the same subgraph** (Surface Sampler on a landscape or
      a plane). Same output contract.
- [ ] **CHECKPOINT — the thesis:** the same downstream graph runs on both, unchanged.

---

## 3. Zoning — Layer 1

The surface points have no `Zone` attribute, so zone-matching cannot work yet.

- [ ] Split the belt into zones along its length. Simplest version: ranges by Y position,
      hand-authored, not generated.
- [ ] Write `Zone` onto each surface point
- [ ] Then set `Match And Set Attributes` to match `Zone` -> `Zone`
- [ ] **CHECKPOINT:** residential modules only appear in the residential stretch

---

## 4. Save the failure shot

- [ ] **Screenshot the standard Surface Sampler failing on the cylinder** — points firing off
      into space, cubes lying on their sides.

      Portfolios show the polished result and hide the broken version, so every project looks
      equally easy and none of them prove anything. A two-panel before/after communicates the
      entire project in two seconds. **You will produce this image for free while things don't
      work — save it when it happens.**

---

## Deferred, deliberately

- **Streets / road network.** PCG 5.7 does have `CreateSplineMesh` / `SpawnSplineMesh` /
  `SplineToMesh` nodes, so the project log's "PCG can't deform meshes along splines" needs
  revisiting — but roads are Layer 2 and JD2 Tier 2. Not this week.
- **Blocks / lots.** Layer 3, needs streets first.
- `import_datatable.py` — convenience, write it when the reimport clicking annoys you.

---

## Art track — Week 4 (parallel, and now the real risk)

Schedule says "structural shells + habitat surfaces blockout" for Weeks 3-4. Week 3's art track
was **not started**. This is now the project's largest open item.

- [ ] **Mesh subdivision — highest priority.** `Hull_Shell_A` is 2,190 triangles across 13.4 km;
      belts are 208 each. Fixes four things at once:
      - shadow terminator artifacts (Epic's documented cause: low poly + high curvature + smooth normals)
      - Lumen surface cache coverage
      - World Partition streaming and culling
      - gives PCG denser, smoother surfaces to sample
      **Split into segments, don't just subdivide in place** — segmentation is what the modular
      plan needs anyway.
- [ ] **Reimport the FBXs** while you're there — that also restores the mesh assets' default
      material slots, currently `WorldGridMaterial`
- [ ] Replace `M_Temp` — it is on 34 meshes including all three hull shells and every greenhouse.
      The largest surfaces in the level are running a placeholder.
- [ ] Reference board (PureRef) — NASA Ames archive, public domain, exact subject
- [ ] Rough silhouettes, 6 categories
- [ ] Material library plan
- [ ] **Start sourcing** — 24 of 37 modules are Megascans/Marketplace, i.e. downloading, not
      authoring. Every one collected is a real mesh path the validator can check and PCG can place.

---

## Lighting — carried, not urgent

- [ ] Real space cubemap. UDS's `FlatCubemap` is a dark placeholder, so `Sky Light Intensity`
      is multiplying nothing. NASA imagery or a free HDRI. **Biggest single visual win available.**
- [ ] Rect lights at the windows are placed but currently **switched off** — an A/B showed they
      were swamped by sunlight already entering through the (non-shadow-casting) glass.
      Revisit once ambient exists.
- [ ] Volumetric fog. Physically justified here, unlike most sci-fi: the habitat has an
      atmosphere inside it, and atmospheric perspective is what will sell the 13 km scale.
- [ ] Shadows vanishing at distance — still unresolved. Needs
      `Show > Visualize > Virtual Shadow Map`. Note VSM uses **clipmaps**, not the old cascaded
      Dynamic Shadow Distance, so that setting is not the mechanism.

---

## Risk

**The technical risk this week was budgeted for and has already been retired.** Surface sampling
with correct orientation works with stock nodes.

**The remaining risk is entirely art.** The pipeline will be further along than the content it has
to place — a working data-driven system spawning grey cubes because none of the 37 meshes exist.

A recruiter scrolls past grey boxes regardless of what is underneath them. Weeks 5-6 have no
slack, so any art work displaced from Week 4 has nowhere to go.
