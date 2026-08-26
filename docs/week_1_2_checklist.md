# Weeks 1–2 — Full Checklist (System + Art + Pipeline)

Compiled from the execution guide (Rev 2), art asset guide, and scope doc (Rev 2).
Status as of end of Week 2, day 2.

**Legend:** `[x]` done · `[~]` partially done · `[ ]` not started

---

## SYSTEM 1 — Blockout & World Partition (Week 1)

- [x] Cylinder shell locked at final scale, human-reference checked
      → 444.17 m dia × 1787.77 m long. Verified 3 ways: Blender human ref,
        Nanite stats, in-engine actor bounds. Camera sits 1.4 m off inner surface.
- [x] World Partition enabled
      → Converted via `WorldPartitionConvertCommandlet`. Actors in `__ExternalActors__`.
- [x] Corrupt `Cube` asset removed (actor first, then asset, then committed)
- [x] All level actors scale-verified (`Ring`, wings, spine all at scale 1.0)
- [ ] **Refined version of the exterior shell** ← scope doc requires "greybox AND refined"
      → Still pure blockout: smooth cylinder, flat wings, plain torus ring.
        No hull ribbing, panel breakup, endcap structure, or spoke detail.
        Scheduled: Week 3–4 art track ("Structural shells").

**Friday checkpoint:** "Cylinder shell locked at final scale, in a WP level" — **MET**

---

## SYSTEM 2 — Master Materials & MPC (Week 2)

### Checklist items (mechanism level — all met)

- [x] Three master materials built
      → `M_Structural`, `M_Emissive`, `M_Window` all exist and compile.
- [x] `MPC_DayNight` created and wired into all three
      → 4 params: `DayNightBlend`, `WindowEmissiveIntensity`,
        `WindowEmissiveColor`, `AmbientTint`.
- [x] Single-value day/night toggle confirmed working scene-wide
      → Verified: flipping `DayNightBlend` changes all three materials.
- [x] At least one custom HLSL node
      → `MF_Triplanar` — normal-based blend weights driving a procedural grime mask.
        Repurposed after discovering UE 5.7 ships a native triplanar node.

**Friday checkpoint:** "Toggling one MPC value shifts all material families" — **MET**

### What "complete" actually requires (NOT met)

The checklist above measures whether the *mechanism* works. It does not measure
whether the material system is usable. These are from the scope doc's material goals:

- [ ] **Material instances created** ← biggest gap
      → Scope doc: "multiple material instances instead of many unrelated materials."
        Currently: 3 masters, **0 instances**. The master/instance pattern is half built.
        Needed: `MI_Structural_Hull`, `MI_Structural_Truss`, `MI_Emissive_CityLights`,
        `MI_Emissive_Starfield`, `MI_Window_Belt`, etc.
- [ ] **Applied to real geometry**
      → Materials only tested on placeholder cubes. `MainCylinder`, wings, and Ring
        still carry the original FBX-imported Phong materials.
- [ ] **Real textures**
      → `M_Structural` uses a brick placeholder. No metal panelling, no normal maps,
        no roughness/ORM maps, no starfield texture for `M_Emissive`.
- [ ] **Day/night presets actually tuned**
      → Current values are arbitrary test numbers (magenta emissive, 0.4/0.05 opacity).
        Neither state has been art-directed to look like day or night.
- [ ] **Legacy materials cleaned up**
      → `M_Agriculture`, `M_Industrial`, `M_Residential`, `M_Space_colony`, GreyBox/*
        are leftover FBX Phong imports. Should become instances of the new masters,
        or be deleted.
- [ ] **Grime mask finished**
      → Currently lerps to a flat colour. Production version: lerp to a grime *texture*
        + noise breakup so flat faces get variation. Deferred to Week 11 polish.
- [ ] `M_Window` two-sided flag (glass is viewed from inside AND outside)
- [ ] `M_Emissive` base colour set to black (currently grey 0.406)

---

## ART TRACK — Concept & Kit Planning (Weeks 1–2)

Per the art asset guide, this runs *parallel* to Systems 1–2, not after them.
**Almost entirely not started.**

- [ ] **Reference board** — silhouettes and mood per module category
      → PureRef is installed. Five boards (or one split five ways): structural shells,
        habitat surfaces, greenery, infrastructure, debris/wear.
- [ ] **Rough silhouettes** for each of the five categories
- [~] **Module list locked**
      → Draft exists at `docs/module_list.xlsx` (62 modules, all categories in range).
        Names/counts/belt assignments are placeholders — not reviewed or locked.
- [ ] **Material library plan**
      → Was supposed to precede building the masters. Built them without it.
        Retroactively worth writing: which module categories map to which master,
        what each parameter controls, trim-sheet strategy.
- [ ] **Station shell reference** — hull ribbing, endcap structure, panel breakup
      → Feeds Week 3–4 structural detail work.

---

## PIPELINE — Version Control (ongoing, per scope doc)

- [x] Git repository with incremental commit history
      → Local + public remote at github.com/John1178/oneill-cylinder-ue5
- [x] Git LFS configured for binary assets (`.uasset`, `.umap`, `.fbx`, textures)
- [x] Large-binary handling decision made and documented
      → Third-party marketplace content excluded (`StarterContent`, `UltraDynamicSky`)
        — 1234 MB → 8.24 MB, licence-safe for a public repo.
- [~] **Git workflow documented**
      → Decisions exist in `docs/design_day_night.md` and commit history, but there's
        no written workflow section (branching strategy, LFS rationale, what's
        excluded and why). Scope doc wants a paragraph on this in the final write-up.

---

## Honest summary

**Checklist items: 6 of 6 met** across Systems 1 and 2.

**Production completeness: roughly half.** The material system's architecture works
but has no instances, no real textures, and isn't applied to the actual station.
The art track for Weeks 1–2 is essentially untouched.

**Highest-value remaining work this week, in order:**

1. Material instances (completes the architecture, unblocks module assignment later)
2. Apply materials to real station geometry, replace the Phong imports
3. Tune actual day/night presets
4. Art-track catch-up: reference board, silhouettes, lock the module list
