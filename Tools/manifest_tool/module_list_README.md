# Module List — What It Is and How To Use It

`module_list.xlsx` is the catalogue of every asset the PCG system is allowed to place.
It is the single source of truth for *what exists*. The manifest (a separate file) decides
*what goes where*.

If a module is not in this list, PCG cannot place it.

---

## Where it sits in the pipeline

```
module_list.xlsx          <-- you edit this
      |
      v  export
   CSV / JSON             <-- generated, never hand-edited
      |
      v  import
  UE DataTable asset
      |
      v
   PCG graph  ->  Attribute Set  ->  Mesh Selector by Attribute  ->  spawn
```

The spreadsheet is the human surface. Everything downstream is generated from it.
Editing the generated files directly means your changes are lost on the next export.

---

## The sheets

| Sheet | Purpose |
|---|---|
| **Module List** | The data. One row per module. |
| **Column Guide** | What each column means, who fills it, and whether the tool reads it. **Read this before editing.** |
| **Workload** | How many modules come from each source, and what that implies. |
| **Notes** | Revision history and design decisions. |

---

## Before you edit

**Read the Column Guide sheet.** It colour-codes every column:

- **Red — REQUIRED**: the tool reads it. Wrong or missing means the export fails.
- **Amber — optional**: read, but blanks are tolerated.
- **Grey — ignored**: for humans. Change freely, nothing breaks.

The two most common mistakes:

**Renaming `Name` on an existing module.** PCG and every saved manifest refer to modules by
this ID. Renaming it orphans them. Add a new row instead and retire the old one.

**Assuming `Weight` is a percentage.** It is not. Weights are *relative* within a zone and do
not need to sum to anything. Three modules at 1.0 / 0.6 / 0.4 means roughly 5 / 3 / 2 out of
every ten placements.

---

## What Weight actually controls

Weight is the difference between a belt that looks *designed* and one that looks *shuffled*.

With every module at 1.0, each is equally likely, and the result reads as noise. Setting a
common filler high (1.0) and a distinctive piece low (0.3) produces the rhythm of a real
environment — mostly ordinary buildings, occasional landmarks.

It is the single knob that most affects whether generated output looks intentional.

---

## Adding a module

1. Add a row. Give it the next ID in its category prefix (`BLD_008`, `STR_007`, …).
2. Fill every REQUIRED column. `Mesh` may be blank if the asset does not exist yet —
   the validator reports it as not-yet-ready rather than an error.
3. Set `Weight` relative to the other modules in the same zone, not in isolation.
4. Set `Source` so the workload stays honest.
5. Re-run the export. Do not hand-edit the generated CSV/JSON.

## Retiring a module

Do **not** delete the row — anything referencing that ID silently breaks.
Set `Weight` to `0` so it is never placed, and note why in `Notes`. Delete it only once
you have confirmed no manifest references it.

---

## Column reference (summary)

| Column | Required | Notes |
|---|---|---|
| `Name` | ✅ | Unique ID. Must be first column — UE DataTable requirement. Never rename. |
| `DisplayName` | — | Human label only. |
| `Category` | ✅ | One of the six kit categories. |
| `Zone` | ✅ buildings | Residential / Industrial / Service, or `-`. Manifest zone ratios reference this. |
| `Belt` | ✅ | A (hero), B (support), or All. Belt C is out of scope. |
| `Mesh` | ✅ | Content Browser path. This is what PCG actually spawns. |
| `Weight` | ✅ | 0.0–1.0, relative within a zone. |
| `Source` | optional | Model / Megascans / Marketplace / Scan. Marketplace cannot go in the public repo. |
| `Status` | optional | Production tracking. |
| `Notes` | — | Free text. |

Full explanations, with failure modes, are on the **Column Guide** sheet.

---

## Constraints worth knowing

**The columns are not freely extensible.** A UE DataTable requires a UStruct whose fields map
1:1 to the column names. Adding a column means updating that struct. Extra columns can exist in
the spreadsheet for human use, but the export must drop them.

**`Name` must stay the first column.** UE's CSV DataTable import requires it.

**Marketplace assets cannot be committed to the public repository.** Licensing. The repo holds
tools and code; the visual showcase is video and screenshots.

---

## Known gaps

**Interiors (室内).** Not covered. Interior spaces are a separate problem — layouts, occlusion,
streaming — and are out of scope for this project. Recorded here deliberately rather than left
to be discovered.
