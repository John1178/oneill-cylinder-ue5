# Week 3 — Module Data Pipeline (System 3)

**Rewritten 2026-09-02.** The original version of this file described a manifest *editor*
with a UI, zone-ratio validation, and a JSON schema. That design was superseded — see
"What changed and why" below. Working against the old list would mean feeling behind on
work that was correctly abandoned.

**Friday checkpoint:** UE5 imports the exported CSV as a DataTable, and the validator
catches a deliberately broken spreadsheet.

---

## What changed and why

Research into Epic's PCG framework moved the layout data out of the manifest entirely:

| Data | Old plan | Now |
|---|---|---|
| Module catalogue (37 rows, paths, weights) | JSON manifest | **CSV → UE DataTable** |
| Belt config — road spacing, density, seed, zone ratios | JSON manifest | **PCG component parameters, native** |
| Layout algorithm | manifest-driven | **PCG graph** |

PCG exposes scalars well and they need live iteration, so putting them in a file the artist
edits offline was the wrong shape. That left the tool with one job: **be the gate between the
spreadsheet and the engine.**

Consequences:
- No UI. A CLI validator with **exit codes** is the better artefact — it wires into a
  pre-commit hook or a Perforce change-submit trigger, which a Tkinter window cannot.
- No zone-ratio or missing-reference checks — that data no longer lives here.
- CSV over JSON: the data is flat (9 columns, one value each), diffs cleanly one line per
  module, and opens in Excel. JSON only wins once a field holds a list.

---

## Done

### The tool — `Tools/manifest_tool/export_modules.py`
- [x] `module_list.xlsx` locked — 37 modules, restructured for DataTable import
- [x] Reads the spreadsheet (`read_rows`, carries `_row` for error messages)
- [x] Writes `output/module_list.csv` — `Name` first, 9 columns, human-only columns dropped
- [x] Runs standalone
- [x] Refuses to write on any error; `sys.exit(1)` so a build step can block on it
- [x] Warnings do not block the write (an unbuilt mesh is not an error)

### Validators — five, all tested both directions
- [x] `check_names` — format `PREFIX_NNN`, uniqueness, empty, non-text
- [x] `check_enums` — Category / Zone / Belt / RotationMode / Source against the VALID_ lists
- [x] `check_zone_rules` — Building must have a real zone; non-Building must not
- [x] `check_numbers` — Weight 0.0–1.0, Clearance ≥ 0, both type-guarded
- [x] `check_mesh_paths` — `/Game/` prefix, blank = **warning** not error
- [x] `validate` — runs all five, reports everything at once, never stops at the first error

### Proof
- [x] Broken spreadsheets built and run — every planted fault caught
- [x] Clean spreadsheet returns zero errors (the control test that matters most)
- [x] Every message names row number, offending value, and expected format

### Housekeeping
- [x] `Tools/manifest_tool/` at project root, separable for a public tools repo
- [x] Branch `feature/python-manifest-tool` in use
- [x] `__pycache__/` ignored
- [x] `module_list_README.md` — column meanings, who fills what, what the tool reads

---

## Still open

### UE5 integration — the real remaining gap
- [ ] Blueprint Struct `S_ModuleRow` — **8 fields**, not 9. `Name` becomes the DataTable row
      key and is NOT a struct member. Blueprint structs do not need `FTableRowBase`; only
      C++ ones do.
- [ ] Field types: `Weight` / `Clearance` = Float. Everything except `Mesh` can be **String** —
      the Python validator already guarantees legal values, so enums here would duplicate work.
- [ ] `Mesh` field type — **String vs Soft Object Reference (Static Mesh)**. Soft ref is
      correct for PCG and does not require the asset to exist. Untested — verify on import.
- [ ] Import `module_list.csv` as a DataTable against that struct
- [ ] `import_datatable.py` (~30 min) — points UE at the CSV and reimports, so weight tweaks
      don't mean clicking through the import dialog every time
- [ ] **CHECKPOINT:** run the validator from inside UE5's Python console against a broken sheet

### Test fixtures
- [ ] Commit the deliberately-broken spreadsheets and the runner into
      `Tools/manifest_tool/tests/`. They currently exist only in scratch. A tool shipped with
      fixtures proving it fails correctly reads very differently to a tool alone.

### Prove the data path before the art exists
- [ ] Point 3–4 rows at placeholder cubes and get PCG to spawn them.
      CSV → DataTable → PCG → something visible. Finding a broken link now, on 4 rows, beats
      finding it after 37 meshes are built.

---

## Carried over — Week 2, still unfinished

- [ ] Day/night presets still on test values (magenta emissive, arbitrary opacity)
- [ ] `M_Temp` still on all three `Hull_Shell` meshes and every greenhouse module/support
      — **confirmed live 2026-09-02.** These are the largest surfaces in the level.
- [ ] Delete the orphaned `SC_Refined_SM_Hull_Shell` asset if nothing references it

---

## Art track — untouched since Week 1, now blocking

Still ❌, and Weeks 4–6 are the tight ones. Today's lighting session added a hard dependency:

- [ ] **Mesh subdivision** — `Hull_Shell_A` is **2,190 triangles across 13.4 km**; belts are
      208 triangles each. Facets are visible now that the lighting is correct, and Epic's docs
      name low-poly-plus-smooth-normals as the cause of the shadow terminator artifacts.
      Splitting the giant meshes into segments also fixes Lumen surface cache coverage, World
      Partition streaming and culling — and it is what the modular/PCG plan needs anyway.
- [ ] Reference board (PureRef) — NASA Ames archive is public domain and exact-subject
- [ ] Rough silhouettes for the 6 module categories
- [ ] Material library plan — which categories map to which master, what each parameter does
- [ ] Station shell reference — hull ribbing, endcap structure, panel breakup

---

## Lighting — resolved 2026-09-02, not originally scheduled

Recorded because it consumed a session and produced reusable rules. See `ue_working_rules.md`.

- [x] Exposure pinned via `PPV_Global`; UDS `Apply Exposure Settings` off so nothing fights
- [x] Glass hull panels no longer cast shadows — a translucent material still casts a fully
      opaque shadow in UE, which was blocking all sunlight into the interior
- [x] Root cause found: `Sun Light Intensity` was **5 lux** against a ~100,000 lux reference
- [x] Rebalanced: sun 1000 / EV 8.64 / Stars 16000 / Space Layer 40000
- [x] Sky Light switched from Capture-Based (capturing black space) to `CUSTOM_CUBEMAP`

Open:
- [ ] Real space cubemap — UDS's `FlatCubemap` is a dark placeholder, so intensity has
      nothing to multiply. NASA imagery or a free HDRI.
- [ ] Rect Lights sized to the window strips — the documented way to light an interior from
      an opening, rather than hoping GI carries the sun through
- [ ] Volumetric fog — light shafts and depth. **Physically justified here**, unlike most
      sci-fi: the habitat genuinely has an atmosphere inside it, and atmospheric perspective
      is what will sell the 13 km scale.
- [ ] Practical lights (`INF_004` street lamp, `INF_005` overhead strip)
- [ ] Shadows disappearing at distance — unresolved. Needs
      `Show > Visualize > Virtual Shadow Map`. Note VSM uses **clipmaps**, not the old
      cascaded Dynamic Shadow Distance, so that setting is not the mechanism.

---

## Explicitly NOT this week

- PCG graph work — Week 4
- UE asset validator (naming, tri counts, LODs) — Week 8, when assets exist to validate
- Toon/NPR variant — parked, post-project
- Proper UVs, texel density, normal maps, real textures — Week 6
- Convolution bloom kernel — nice-to-have, needs an authored HDR texture

---

## Risk

Original note said Week 4 (PCG curved-surface alignment) is the likely overrun and Week 3
should be comfortable, making it the right week to close the art gap.

**Week 3 was comfortable and the art gap did not close.** It is now the largest open item, it
blocks the lighting from looking like anything, and Weeks 4–6 have no slack in them.
