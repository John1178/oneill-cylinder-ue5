# O'Neill Cylinder — Project Checklist

*rev 18 · 2026-09-16 · one line per task.* Details live in **`ue_working_rules.md`** (how-to, traps,
measurements) · **`project_log.md`** (decisions, history) · **`layer_contract.md`** (system design).

> The one rolling checklist for the whole project. Corrections land here, nowhere else.

**Open: 66 — Publish 1: 37 · Later: 29.** Updated Wed 16 Sep 2026.

**Two releases:** Publish 1 = the PCG tool (greybox), then apply. Later = colony polish; nothing in
Later blocks Publish 1. Why: `project_log.md` → Split into two releases.

### Publish 1 — PCG tool

| # | job | open | when |
|---|---|---|---|
| 1 | ~~Swappable surface~~ | ✅ | closed Wed 9 |
| **7d** | **Terrain on the belt** | 8 | **Week 5 — checkpoint Fri 18 Sep** |
| 7 | Design leftovers — 7b-new · 7c · 7e | 3 | Week 6-7 |
| 6 | DataTable test edits -> xlsx | 1 | Week 5 |
| 8 | Zoning | 4 | Week 6 *(Week 5 if terrain finishes early)* |
| 16 | L1 Density | 4 | Week 6 |
| 17 | L2 Streets | 4 | Week 6-7 |
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
| P | Night / day-night | 3 |

---

# Publish 1 — PCG tool

## 1. Swappable surface ✅

- [x] ✅ `SG_SurfaceSource` + flat twin; checkpoint 2026-09-09 → `ue_working_rules.md` → Surface swapping

## 7d. Terrain on the belt `[Week 5 — checkpoint Fri 18 Sep]`

Design: `layer_contract.md` → L0's surface · How + numbers: `ue_working_rules.md` → Terrain · Decision: `project_log.md` → Terrain

- [x] ✅ Method settled — Gaea → Modeling Mode → PCG reads; spike passed 2026-09-14
- [x] ✅ 4. Full sheet built 2026-09-16 — 567k tris, on the belt → `ue_working_rules.md` → Terrain
- [x] ✅ 4b. Nanite on, fallback 100% (567k), collision Complex As Simple — 2026-09-16
- [x] ✅ 5. Gaea relief — valley + edge mountains + river, done 2026-09-15 (build 018) → `gaea.md` → Final graph
- [ ] ⬜ 5b. ~~City plateaus~~ **deferred 2026-09-15** — PCG follows the natural valley (city zone 94% under 10°); revisit after the L2 tile-seam test
- [ ] ⬜ 7. Point L0 `SurfaceMesh` at the terrain
- [ ] ⬜ 8. Retune `SamplingRadius`
- [ ] ⬜ **CHECKPOINT Fri 18 Sep** — terrain on the belt, PCG samples it
- [ ] ⬜ 9. Gaea masks into PCG
- [ ] ⬜ 10. Slope rules — per-point up, not `Normal To Density` (replaces plateaus: streets/buildings only on gentle ground)
- [ ] ⬜ 11. Gaea mask set — slope, soil, flow, river → EXR (one set feeds material + PCG; city zones come from zoning, job 8)
- [ ] ⬜ 12. `M_Terrain` — blend by the mask set `[after the terrain mesh]`
- [ ] ⬜ 6. Water sheet at constant radius `[Later]`

## 7. Design leftovers

- [x] ✅ Design block → `layer_contract.md`; 7a L3 frontage-only; 7b withdrawn → `project_log.md` → Schema meanings
- [ ] ⬜ 7b-new. Agriculture belt: add an `Agriculture` zone, or drive it by `Category` `[Week 6 — before Zoning]`
- [ ] ⬜ 7c. Clearance column — nothing reads it yet `[Week 7 — with L3 Lots]`
- [ ] ⬜ 7e. Fix `layer_contract.md` Open decision 2 (still lists the withdrawn Belt/Zone rewrite) `[Week 6 — before Zoning]`

## 6. Weighted module selection

- [x] ✅ Working 2026-09-10 → `ue_working_rules.md` → InlineEditConditionToggle
- [ ] ⬜ Move the `BLD_006` / `BLD_004` test edits into the xlsx, or drop them (backups in scratchpad)

## 8. Zoning (L1) `[Week 6 — or Week 5 if terrain finishes early]`

- [ ] ⬜ Split the belt into zones along Y (hand-authored)
- [ ] ⬜ Write `Zone` onto each surface point
- [ ] ⬜ `Match And Set Attributes`: `Zone` → `Zone`
- [ ] ⬜ **CHECKPOINT** — residential modules only in the residential stretch

## 16. L1 Density `[Week 6]`

- [ ] ⬜ Write `Density` (0-1) from the Gaea mask (7d.9)
- [ ] ⬜ Threshold cull
- [ ] ⬜ `Scatter` / `Rows` switch (Rows = farm, orchard)
- [ ] ⬜ Vegetation scatter (trees, grass) from the soil + slope masks — no hand painting

## 17. L2 Streets `[Week 6-7]`

- [ ] ⬜ Artist-drawn splines → `PCG Spline Sampler`
- [ ] ⬜ Align points to the surface normal; spawn street tiles
- [ ] ⬜ Write `DistToRoad` + `RoadDir`
- [ ] ⬜ Test the tile seam at project scale (fallback: shorter tiles or `DeckPlate_Corner`)

## 18. L3 Lots — frontage-only `[Week 7]`

- [ ] ⬜ Buildings line roads via `DistToRoad`; emit `LotSize`, `Frontage`

## 19. Presets `[Week 7]`

- [ ] ⬜ City / Town / Farm / Factory / Countryside as data — filter + parameter set, no new logic
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

## P. Night / day-night *(parked)*

- [ ] ⬜ Wing shutter driven by `MPC_DayNight.DayNightBlend` → `design_day_night.md`
- [ ] ⬜ `M_Emissive` starfield LED
- [ ] ⬜ Day/night presets + hero shots

---

**Done history:** `project_log.md` → What was built. **Traps:** `ue_working_rules.md` → Quick traps.
