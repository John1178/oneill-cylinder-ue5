# Week 3 — Python Manifest Tool & Data Pipeline (System 3)

Merged week: the original plan split this across Weeks 3 and 4 ("build standalone, then port
into UE5"). Writing it UE-aware from the start skips the port. See `schedule_revised_10week.md`.

**Friday checkpoint:** UE5 loads + validates a manifest via the Python console.

---

## BLOCKER — must be done first

- [ ] **Lock `module_list.xlsx`**
      Currently a draft generated from the art guide's category descriptions, not your decisions.
      The validator checks against real module IDs, so wrong names here become wrong data everywhere
      downstream (PCG, the EUW, the manifest schema).
      → Open it, rename/delete/add until the 30 modules are what you actually intend to build.
      → ~1 hour. Nothing else in Week 3 is safe to start before this.

---

## Decisions to make before writing code

- [ ] **UI framework** — Tkinter (ships with Python, plainer) vs PySide6 (better looking,
      needs installing; UE5 bundles PySide internally so it's available in-editor)
- [ ] **Data format** — JSON (nested, natural for zone ratios + module sets) vs
      CSV (flatter, closer to the existing xlsx)
- [ ] **Where the tool lives in the repo** — suggest `Tools/manifest_tool/` at project root,
      so it's separable for the public tools repo later

---

## Core deliverables (from the scope doc)

### Schema
- [ ] Define the manifest schema — what a belt actually contains
      - Belt index / name
      - Segment count or segment length
      - Zone type ratios (residential / industrial / agriculture)
      - Module set per zone (references module IDs from the module list)
      - Seed
      - Density
- [ ] Write one real example manifest by hand, so the schema is proven before the tool exists

### The tool
- [ ] Reads a manifest file
- [ ] Writes a manifest file
- [ ] Basic UI — load, edit, save, validate
- [ ] Runs standalone (outside Unreal)

### Validation — the three the scope doc names explicitly
- [ ] Flags **missing module references** (manifest names a module ID that doesn't exist)
- [ ] Flags **zone ratios that don't sum correctly**
- [ ] Flags **duplicate module IDs**

### UE5 integration
- [ ] Script runs inside UE5's Python environment
- [ ] UE5 can load a manifest
- [ ] UE5 can run validation and report results to the console
- [ ] **CHECKPOINT:** validator catches a deliberately broken manifest, from inside UE5

---

## NOT on the checklist, but needed anyway

These aren't in the execution guide's checklist. They're either implied, carried over, or
things the guide assumes without stating.

### Carried over from Week 2 (unfinished)
- [ ] Tune day/night presets — current values are test numbers (magenta emissive, arbitrary opacity)
- [ ] Place `SM_Hull_Shell_A/B/C` in the level and delete the stale `SC_Refined_SM_Hull_Shell` actor
- [ ] Delete the orphaned `SC_Refined_SM_Hull_Shell` asset once nothing references it
- [ ] Decide whether `SM_Greenhouse_Support_01..06` keep `M_Temp` or revert to `MI_Structural_Hull`

### Art track (Weeks 1–2, still untouched — runs parallel, needed by Week 3–4 modelling)
- [ ] Reference board (PureRef) — NASA Ames archive is public domain and exact-subject
- [ ] Rough silhouettes for the 5 module categories
- [ ] Material library plan (which categories map to which master, what each parameter does)
- [ ] Station shell reference — hull ribbing, endcap structure, panel breakup

### Implied by the guide but never stated
- [ ] **Test data** — at least one deliberately broken manifest to prove the validator works.
      A validator that has never caught anything is not demonstrated.
- [ ] **README for the tool** — how to run it, what the schema means. This is the artifact a
      recruiter actually reads; the scope doc wants tool UI screenshots as a deliverable.
- [ ] **Screenshots of the tool UI** — named in the scope doc's deliverables list, easy to
      forget until Week 10 when the tool has changed.
- [ ] **Commit granularly** — the scope doc wants "real, incremental commit history."
      One commit at the end of the week undercuts that deliverable.
- [ ] Decide the tool's failure behaviour — does it refuse to save an invalid manifest,
      or save with warnings? (Affects how the PCG side can trust its input.)

### Pipeline hygiene
- [ ] Branch for this work: `feature/python-manifest-tool` (already created, unused)
- [ ] `.gitignore` entry for Python artifacts in the tools folder if not already covered
      (`__pycache__/` is already ignored)

---

## Explicitly NOT this week

- Toon/NPR shading variant — parked, post-project decision
- Dim sum game rebuild — parked until after the O'Neill project ships
- PCG work — that's Week 4
- Proper UV unwrapping / texel density — Week 6 texture pass
- Normal maps, real textures — Week 6

---

## Risk

The execution guide flags Week 4 (PCG curved-surface alignment) as the likely overrun, not this
week. Week 3 should be comfortable — which makes it the right week to also close the art-track
gap, since Weeks 4–6 will be tighter.
