# Test fixture — `module_list_BROKEN.xlsx`

A copy of `docs/module_list.xlsx` with **14 deliberate faults**, one for every branch of
every validator in `export_modules.py`.

Its purpose is to prove the validator actually fails when it should. A validator that has
only ever been run on clean data has not been demonstrated — it might be returning an empty
list because everything passes, or because it is broken.

## Run it

```bash
cd Tools/manifest_tool
python -c "import export_modules as em; e,w = em.validate(em.read_rows('tests/module_list_BROKEN.xlsx', em.SHEET_NAME)); [print(x) for x in e]; [print('WARN', x) for x in w]"
```

## What is planted

| row | column | value | should trigger |
|---|---|---|---|
| 3 | Name | *(blank)* | `check_names` — empty |
| 5 | Name | `BLD_001` | `check_names` — duplicate of row 2 |
| 7 | Name | `BLD009` | `check_names` — no underscore |
| 9 | Name | `BLD_00A` | `check_names` — suffix not digits |
| 11 | Category | `Buliding` | `check_enums` — typo |
| 13 | Belt | `C` | `check_enums` — belt C was cut from the project |
| 15 | Source | `Fab` | `check_enums` — not a valid source |
| 6 | Zone | `-` | `check_zone_rules` — a Building with no zone |
| 25 | Zone | `Residential` | `check_zone_rules` — a non-Building with a zone |
| 19 | Weight | `5.0` | `check_numbers` — above 1.0 |
| 21 | Weight | `high` | `check_numbers` — not a number |
| 23 | Clearance | `-3` | `check_numbers` — negative |
| 27 | Mesh | `C:\models\thing.fbx` | `check_mesh_paths` — not a UE content path |
| 29 | Mesh | *(blank)* | `check_mesh_paths` — **warning only**, not an error |

## Expected result

```
13 errors, 1 warning
```

The blank mesh on row 29 is deliberately a **warning**, not an error: an unbuilt asset is
normal during production and must not block the export. If it ever appears in the errors
list, the warning/error split has broken.

## Two controls that matter as much as the faults

1. **The clean spreadsheet must return zero errors.** A check that flags everything looks
   like it is working hard and is actually broken — this happened during development, when
   `check_enums` compared `Source` against `VALID_ZONES` and flagged all 37 rows.
2. **The tool must exit non-zero and write no file** when errors exist. That exit code is
   the interface a pre-commit hook or a Perforce change-submit trigger reads.

## Note on maintaining this file

Row numbers are hard-coded above, so **inserting or deleting rows in
`docs/module_list.xlsx` will not shift this fixture** — it is a frozen copy, not a live
mirror. If the schema changes (a column added or renamed), regenerate the fixture from the
current spreadsheet rather than editing this one.

Also note the faults are placed on rows whose *category* suits them: the
"Building with no zone" fault has to sit on an actual Building row, or it is valid data and
nothing fires.
