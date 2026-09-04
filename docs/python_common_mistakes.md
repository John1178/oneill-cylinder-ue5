# Python — mistakes I keep making

Written from real mistakes made while building `Tools/manifest_tool/export_modules.py`.
Every example below is something that actually happened, not a textbook case.

Read this before writing a new script, and again when something doesn't work.

---

## 1. Quotes mean "the text itself", no quotes means "the value in this variable"

**Happened 3 times.** The single most common mistake.

```python
open("out_path", "w")     # creates a file literally NAMED out_path
open(out_path, "w")       # writes to the path stored in the variable
```

Same rule inside f-strings — `{ }` marks a variable, everything else is literal text:

```python
f"Category 'Building' is not valid"     # always prints "Building"
f"Category '{category}' is not valid"   # prints the actual bad value
```

The first version once reported `Category 'Building' is not valid` when the real
value was `Buliding`. The message was wrong in a way that pointed the reader at
the *correct* spelling. Worse than no message.

**How to catch it:** if the output is identical every run, something that should
be a variable is in quotes.

---

## 2. Copy-paste, then change only ONE of the two things

**Happened 3 times.** Copy a block, change the obvious thing, miss the second one.

```python
source = module["Source"]
if source not in VALID_ZONES:        # changed the variable, not the list
```

```python
f"row {n}: Category '{belt}' is not valid"   # changed the variable, not the word
```

```python
write_csv(XLSX_PATH, SHEET_NAME)     # pasted read_rows' arguments
```

None of these crash. They produce *confident wrong output* — the VALID_ZONES one
flagged all 37 rows of a clean spreadsheet as errors.

**How to catch it:** before copying a block a third time, run it once. Then when
you paste, say out loud what changes — usually it's two things, not one.

---

## 3. Test against data you KNOW is clean

The `VALID_ZONES` bug was invisible until the checker ran on the good spreadsheet
and returned 37 errors. A checker that flags everything looks like it's working
hard and is actually broken.

**Rule:** every check needs two runs.
- Known-good data → must return empty
- Deliberately broken data → must catch exactly what you broke

Only passing one of those proves nothing.

---

## 4. Is this line inside the loop or outside it?

**Happened twice.** Indentation isn't cosmetic in Python — it decides what runs
when.

```python
for i in range(len(headers)):
    module[headers[i]] = row[i]
    module["_row"] = row_num       # ran 12 times; nothing in it changes
```

```python
parts = name.split("_")            # sat ABOVE the loop, before `name` existed
for module in rows:
    name = module["Name"]
```

**The question to ask:** *does anything on this line change on each pass?*
- Yes → belongs inside
- No → belongs outside

---

## 5. `range()` counts. It does not describe a span.

```python
if weight not in range(0.0, 1.0):    # TypeError - range needs whole numbers
```

Even with whole numbers, `range(0, 2)` is the list `[0, 1]` — the value `0.6`
is not in it, so every valid weight gets flagged.

For "is it between", compare against each end:

```python
if weight < 0.0 or weight > 1.0:
```

`range` is for counting loops (`range(len(headers))`). Different job.

---

## 6. Loop over the LIST, and give the item a different name

**Three wrong versions in a row:**

```python
for w in validate:      # that's the function, not a list
for w in result:        # that's the spreadsheet rows, not the messages
for warning in warning: # same name for the list and one item
```

The shape is always:

```python
for <one item> in <the list>:
```

Two different names, because they're two different things. Plural list names
help — `for warning in warnings` reads naturally and can't clash.

**Before writing a loop, say what's in the list.** `warnings` holds finished
message strings. `result` holds dicts of spreadsheet data. Different lists,
different purposes.

---

## 7. Parameter names only exist INSIDE the function

```python
def write_csv(rows, out_path):
    ...

# in main():
write_csv(rows, out_path)     # NameError - those names don't exist here
write_csv(result, OUT_PATH)   # correct - main's names for the same things
```

`rows` and `out_path` are labels for whatever gets handed in. The caller uses
its own names. That's the point — the function works no matter what the caller
calls its variables.

---

## 8. `isinstance` — copy the `== False`, not the type

```python
if isinstance(weight, (int, float)) == False:   # weight should be a NUMBER
if isinstance(mesh, str) == False:              # mesh should be TEXT
```

When copying this between functions, the **type changes** and the `== False`
**stays**. Got this backwards twice — changed `str` to `(int, float)` while
leaving off the `== False`.

**Why it matters at all:** a validator must never crash on bad data. That's its
whole job. Comparing `None < 0.0` or calling `.split()` on a number throws an
exception and kills the tool before it checks any other row.

---

## 9. One step at a time

Merging three steps into one guess produced this:

```python
for warning in validate:
    if warning and errors == True:
        print(warning, errors)
    else:
        write_csv
```

Four separate mistakes tangled together, none fixable without unpicking the
others. (`write_csv` with no brackets doesn't call anything either — it just
names the function.)

Write one step, run it, then the next. Slower per line, much faster overall.

---

## 10. Guessing then running IS the method

Nobody types code knowing it works. You type your best guess and let the machine
tell you. An error message is a result, not a failure — `ValueError: dict
contains fields not in fieldnames: 'Status', '_row', 'DisplayName', 'Notes'`
named the exact problem and the exact fix.

Read the error before assuming you don't understand. It usually says what's
wrong in plain words.

---

## Quick checklist before running anything

- [ ] Anything in quotes that should be a variable?
- [ ] If I copied a block — did I change **both** things?
- [ ] Is each line at the right indent level (inside vs outside the loop)?
- [ ] Am I looping over the list, with a different name for the item?
- [ ] Does it return empty on data I know is clean?
- [ ] Does it catch exactly what I deliberately broke?
