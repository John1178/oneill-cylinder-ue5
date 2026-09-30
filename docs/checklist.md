# O'Neill Cylinder — Project Checklist

*rev 27 · 2026-09-30 · one line per task.* Details live in **`ue_working_rules.md`** (how-to, traps,
measurements) · **`project_log.md`** (decisions, history) · **`layer_contract.md`** (system design).

> The one rolling checklist for the whole project. Corrections land here, nowhere else.

**Open: 58 — Publish 1: 20 · Later: 38.** Updated Wed 30 Sep 2026.

**Two releases:** Publish 1 = the PCG tool (greybox), then apply. Later = colony polish; nothing in
Later blocks Publish 1. Why: `project_log.md` → Split into two releases.

**One belt first.** Build and prove everything on the **Residential** belt; the other two only after the
system runs end to end (job 15). Why: `project_log.md` → One belt first.

### Publish 1 — PCG tool

| # | job | open | when |
|---|---|---|---|
| 1 | ~~Swappable surface~~ | ✅ | closed Wed 9 |
| **7d** | **Terrain on the belt** | 3 | **Week 5 — checkpoint Fri 18 Sep** |
| 7 | Design leftovers — 7c | 1 | Week 7 |
| 6 | ~~DataTable test edits -> xlsx~~ | ✅ | closed Thu 24 |
| 8 | ~~Zoning~~ | ✅ | closed Thu 24 |
| 16 | L1 Density | 1 | Week 6-7 |
| 17 | L2 Streets | 3 | Week 6-7 |
| 18 | L3 Lots — frontage-only | 1 | Week 7 |
| 19 | Presets | 2 | Week 7 |
| 20 | Editor panel + reimport script | 3 | Week 7 |
| **D1** | **Publish 1 — video, breakdown, apply** | 7 | **Week 8** |

### Later — colony polish

| # | job | open |
|---|---|---|
| 3 | ~~Replace `M_Temp`~~ | ✅ |
| 4 | Reference board | 1 |
| 5 | Lit windows — leftovers | 3 |
| 7d.6 | Water sheet | 1 |
| 9 | Real space cubemap *(cosmetic)* | 1 |
| 10 | Shadows at distance | 1 |
| 11 | Detail meshes / kitbash | 5 |
| 12 | Volumetric fog | 1 |
| 13 | ~~Rect lights~~ — folded into 5 | ✅ |
| 14 | Source the 24 modules *(⏰ Bridge backup)* | 4 |
| 15 | Second belt | 1 |
| 18b | L3 block subdivision *(stage 2)* | 1 |
| 21 | Optimisation pass | 3 |
| 22 | Polish — hero shots | 2 |
| 23 | Colony delivery | 2 |
| T | Terrain look — leftovers | 6 |
| V | Vegetation polish *(moved out of 16, Week 6)* | 4 |
| P | Night / day-night | 3 |

---

# Publish 1 — PCG tool

## 1. Swappable surface ✅

- [x] ✅ `SG_SurfaceSource` + flat twin; checkpoint 2026-09-09 → `ue_working_rules.md` → Surface swapping

## 7d. Terrain on the belt `[Week 5 — checkpoint Fri 18 Sep]`

Design: `layer_contract.md` → L0's surface · How + numbers: `ue_working_rules.md` → Terrain · Decision: `project_log.md` → Terrain

- [x] ✅ Method settled — Gaea → Modeling Mode → PCG reads; spike passed 2026-09-14
- [x] ✅ 4. Full sheet built 2026-09-16 — 567k tris, on the belt, 565-935 m from the axis
- [x] ✅ 4b. Nanite on, fallback 100% (567k), collision Complex As Simple — 2026-09-16
- [x] ✅ 5. Gaea relief — valley + edge mountains + river, done 2026-09-15 (build 018) → `gaea.md` → Final graph
- [ ] ⬜ 5b. ~~City plateaus~~ **deferred 2026-09-15** — PCG follows the natural valley (city zone 94% under 10°); revisit after the L2 tile-seam test
- [x] ✅ 7. L0 points at the terrain — 64 instances land 731.8-944.2 m from the axis, 2026-09-16
- [x] ✅ 8. Retuned — radius 1000, density 10.0; 2,336 points, 20 m min spacing, 2026-09-16
- [x] ✅ **CHECKPOINT met 2026-09-16 (2 days early)** — terrain on the belt, PCG samples it
- [x] ✅ 9. Gaea masks into PCG — mountain mask on the points, values match the file, 2026-09-22
- [x] ✅ 10. Slope rules — per-point up (Mul Add → MakeRotFromZ) + slope gate; in **both** graphs 2026-09-25, city capped at 10° → `ue_working_rules.md` → SG_TerrainMasks
- [x] ✅ 11. Gaea mask set — mountain, rock, soil (build 021) + river/flow/slope from 018; imported to `/Game/Terrain/Mask/` 2026-09-18
- [x] ✅ 12. Terrain material — `M_Terrain_Master` + `MI_Terrain_Residential`, signed off 2026-09-22
- [ ] ⬜ 13. Delete the `M_Terrain` v1 backup once the master is proven
- [ ] ⬜ 6. Water sheet at constant radius `[Later]`

## 7. Design leftovers

- [x] ✅ Design block → `layer_contract.md`; 7a L3 frontage-only; 7b withdrawn → `project_log.md` → Schema meanings
- [x] ✅ 7b-new. `Agriculture` added as a fourth `Zone` value (`VEG_007` crop rows); validator rule widened, 2026-09-28
- [ ] ⬜ 7c. Clearance column — nothing reads it yet `[Week 7 — with L3 Lots]`
- [x] ✅ 7e. `layer_contract.md` Open decision 2 corrected — Zone = building zoning (PCG reads it), Belt = quality tier (validator only), 2026-09-24

## 6. Weighted module selection

- [x] ✅ Working 2026-09-10 → `ue_working_rules.md` → InlineEditConditionToggle
- [x] ✅ `BLD_004` cylinder / `BLD_006` cone mesh paths written into the xlsx + CSV re-exported 2026-09-24 — reimport `DT_Modules` in the editor

## 8. Zoning (L1) `[Week 6 — or Week 5 if terrain finishes early]`

- [x] ✅ Split the belt into zones along Y — thirds at −80,000 / 180,000, 2026-09-24
- [x] ✅ Write `Zone` onto each surface point — 3 × Add Attribute (String) → Merge Points
- [x] ✅ `Match And Set Attributes`: `Zone` → `Zone`, Keep Unmatched off
- [x] ✅ **CHECKPOINT met 2026-09-24** — 2,432 points, 806/796/830 per zone, no crossover → `ue_working_rules.md` → Zoning

## 16. L1 Density `[Week 6]`

- [x] ✅ Write `Density` (0-1) — artist input, one value per zone (0.8 / 0.5 / 0.3), 2026-09-28
- [x] ✅ Threshold cull — `Attribute Noise` → `Roll`, keep where `Roll` < `Density`; 143 → 83 points, within 2 of predicted
- [x] ✅ Trees from the masks — treeline band + slope rule, 30,866 trees, 2026-09-22
- *(the rest of the planting moved to Later → job V, 2026-09-24 — not needed for the tool demo)*

## 17. L2 Streets `[Week 6-7]`

- [x] ✅ Artist-drawn spline → `Get Spline Data` (tag `Road`) → `Spline Sampler`, 2026-09-25
- [x] ✅ `DistToRoad` via the `Distance` node + 40 m frontage filter — 302 points line the road
- [x] ✅ `RoadDir` — 2nd `Distance` node (Output Distance Vector) → `Make Rot From ZX`; facing error median 0.92°, lean 0.00°, 2026-09-28
- [ ] ⬜ Road mesh is a 1 m cube bar — author a road tile **with kerb + pavement** (~100 × 1200 × 20 cm, outer thirds raised) `[polish]`
- [ ] ⬜ Road floats/sinks between control points — fix: Spline Sampler → `Projection` (target `World Ray Hit Query`) → `Create Spline` → Spawn Spline Mesh `[polish]`
- [x] ✅ ~~Tile seam test~~ — withdrawn: `Spawn Spline Mesh` bends one mesh along the spline, no tiles, no seams

## 18. L3 Lots — frontage-only `[Week 7]`

- [x] ✅ Lot line from the road spline — sample 5 m, keep 1 per `Frontage` (modulo), ±12 m setback; 50 buildings, 25/side, 12.00 m out, facing error 0.00°, 2026-09-30
- [x] ✅ Emits `Frontage` (2500) + `LotSize` (2000); spacing is an attribute, so job 19 sets it per zone
- [ ] ⬜ Lot points skip the `Mountain`/`Slope` gates — `SG_TerrainMasks` needs `TexCoord[0]`, which spline points lack. Decide: compute mask UV from position, or rely on the artist-drawn road

## 19. Presets `[Week 7]`

- [ ] ⬜ City / Town / Farm / Factory / Countryside as data — filter + parameter set, no new logic
- [ ] ⬜ `Scatter` / `Rows` switch (Rows = farm, orchard) — moved from job 16 2026-09-28: needs an `Agriculture` stretch to switch on
- [ ] ⬜ Needs 7b-new first

## 20. Editor panel + reimport script `[Week 7]` *yours to write*

- [ ] ⬜ `import_datatable.py` — one-command DataTable reimport
- [ ] ⬜ Editor Utility Widget — seed, density, zone split, preset → export → validate → reimport → regenerate
- [ ] ⬜ **CHECKPOINT** — the panel regenerates a belt without opening the graph

## D1. Publish 1 `[Week 8]`

- [ ] ⬜ Capture tool UI + PCG debug views
- [ ] ⬜ Measure regeneration time + instance count
- [ ] ⬜ Demo video — shot list in `layer_contract.md`
- [ ] ⬜ Breakdown page — lead with what broke on the cylinder
- [ ] ⬜ Resume bullets
- [ ] ⬜ Document the Git workflow
- [ ] ⬜ **CHECKPOINT** — publish and start applying

*Open question: does the demo get a terrain / slope shot?*

---

# Later — colony polish

## 3. Replace `M_Temp` ✅

- [x] ✅ Done 2026-09-14 → `project_log.md` → What was built

## 4. Reference board

- [ ] ⬜ Fill gaps: hull close-up · kitbash detail · window-to-land junction · night windows · scale anchors (NASA Ames art is public domain)

## 5. Lit windows

- [x] ✅ Ambient, lens flare, Substrate glass, GBuffer, reflections → `ue_working_rules.md`
- [ ] ⬜ Re-point the orphaned day/night Lerp → `ue_working_rules.md` → Substrate glass
- [ ] ⬜ Rect lights warm + wire to `MPC_DayNight`
- [ ] ⬜ Judge whether contact shadows are missed

## 9. Real space cubemap *(cosmetic)*

- [ ] ⬜ Reflections only — ambient was never the cubemap

## 10. Shadows at distance

- [ ] ⬜ Visualize VSM, then test the two candidates → `ue_working_rules.md` → Distance shadows

## 11. Detail meshes / kitbash

Scoping table: `ue_working_rules.md` → Detail meshes

- [ ] ⬜ 1. Sort the kit list by the scoping table
- [ ] ⬜ 2. Author one trim sheet
- [ ] ⬜ 3. Model only what the table calls geometry
- [ ] ⬜ 4. Add them to `module_list.xlsx`
- [ ] ⬜ 5. Texture pass on `M_Structural`

## 12. Volumetric fog

- [ ] ⬜ Add fog — the habitat has air

## 13. Rect lights ✅

- [x] ✅ Folded into job 5

## 14. Source the 24 modules *(in gaps)* → `project_log.md` → Content sourcing

- [ ] ⬜ Collect modules in gaps
- [ ] ⬜ Audit owned Fab packs before buying
- [ ] ⬜ ⏰ Back up the 4 Bridge downloads
- [ ] ⬜ Prefer CC0 over Fab

## 15. Second belt

- [ ] ⬜ Repeat terrain + PCG on a second belt; decide if the third is cut

## 18b. L3 block subdivision *(stage 2)*

- [ ] ⬜ 30-min spike: `Polygon2D Operation` `CutWithPaths` on a boundary + two splines

## 21. Optimisation pass

- [ ] ⬜ Baseline: draw calls, frame time, PCG regen time
- [ ] ⬜ HLOD, instancing, LOD pass → capture after
- [ ] ⬜ *(deferred)* Drive `CastShadow` / `CullDistance` from the sheet

## 22. Polish — hero shots

- [ ] ⬜ Hero shots on the residential belt
- [ ] ⬜ Practical lights on lamp modules (needs 14)

## 23. Colony delivery

- [ ] ⬜ Colony video (hero shots, day/night if P is built)
- [ ] ⬜ Update the breakdown with art + optimisation numbers

## T. Terrain look — leftovers → `ue_working_rules.md` → Terrain material

- [ ] ⬜ Height-blend the layers with the displacement maps
- [ ] ⬜ RVT so scatter picks up the ground colour
- [ ] ⬜ Collapse the surface block into `MF_TerrainSurface`
- [ ] ⬜ Gaea detail normal (Anastomosis → Roughing)
- [ ] ⬜ Grass diffuse still below Epic's 0.21 — revisit under final lighting
- [ ] ⬜ Sky light fill for the shaded / backlit side (now 75)

## V. Vegetation polish → `ue_working_rules.md` → Vegetation

Trees are built and upright (job 16); everything below is dressing, not tool features.

- [ ] ⬜ Rocks, bushes, reeds from the masks (no hand painting)
- [ ] ⬜ Second tree rule for the flat stretches — scattered valley trees / hedgerows from noise, not the mountain mask
- [ ] ⬜ Grass on runtime generation near the camera (millions of instances otherwise)
- [ ] ⬜ Swap the engine sample trees for real meshes (Megascans 3D plants, two-sided foliage — gitignored)

## P. Night / day-night *(parked)*

- [ ] ⬜ Wing shutter driven by `MPC_DayNight.DayNightBlend` → `design_day_night.md`
- [ ] ⬜ `M_Emissive` starfield LED
- [ ] ⬜ Day/night presets + hero shots

---

**Done history:** `project_log.md` → What was built. **Traps:** `ue_working_rules.md` → Quick traps.
