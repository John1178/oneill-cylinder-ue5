# Working rules — Unreal Engine

**Check the source before acting or before stating a fix.**

Written 2026-09-02 after a lighting session where reasoning-instead-of-reading cost
about an hour and produced two wrong diagnoses.

---

## The rule

Every statement about UE behaviour must be labelled as one of:

| label | means |
|---|---|
| **MEASURED** | read out of the live project this session — a cvar, a property, a bound |
| **DOCUMENTED** | found in official docs or the asset vendor's docs, with a link |
| **INFERRED** | reasoning from general knowledge. **Not a finding. Say so.** |

An INFERRED claim is a hypothesis to test, never a fix to apply.
If a fix is about to be applied, it must be MEASURED or DOCUMENTED first.

---

## Order of operations

```
1. MEASURE the live project     (what is actually set right now?)
2. READ the documentation        (what does this system actually do?)
3. Form the hypothesis
4. Change ONE thing
5. Verify by reading the state back
```

Skipping step 2 is what goes wrong. Step 1 feels like enough because it produces
real numbers — but numbers without the system's rules attached lead straight to a
confident wrong answer.

---

## For third-party assets, read THEIR docs, not general UE logic

Ultra Dynamic Sky, MagicaCloth, any marketplace system: these have their own
rules that override normal engine assumptions.

**Case from 2026-09-02:** UDS's documentation says plainly:

> When enabled, UDS will override any Post Process volumes in your level and take
> care of exposure settings.

Instead of reading that, I created a PostProcessVolume and raised its priority to
out-rank UDS. It worked mechanically and was the wrong approach — the documented
fix is a toggle in UDS's own Exposure category. Generic UE knowledge actively
misled here, because the asset is built to break the normal rule.

**Rule:** if a marketplace asset is involved in the system being debugged, find its
documentation before touching anything.

---

## Use the engine's own visualisers instead of inferring

Reading a symptom off a screenshot and reasoning backwards is guessing. UE ships
tools that answer these questions directly:

| question | tool |
|---|---|
| What is auto-exposure actually doing? | `Show > Visualize > HDR (Eye Adaptation)` |
| Is Lumen seeing this surface? | `Show > Visualize > Lumen Surface Cache` (pink = not covered) |
| Shader cost | Shader Complexity view mode |
| What is a shadow doing | `r.Shadow.Virtual.Visualize` |

If a visualiser exists for the question, use it before forming an opinion.

---

## Don't guess numeric values

**Case from 2026-09-02:** pinned exposure to EV100 = 10 with no basis. Result: a
completely black viewport, and 20 minutes spent debugging the wrong thing.

Real reference values existed and took one search to find:

| scene | EV100 |
|---|---|
| Bright sun, midday (100,000 lux) | ≈ 15 |
| Night, starlight (0.001 lux) | ≈ -8.3 |
| Emissive: candle | 5-10 nits |
| Emissive: fluorescent tube | 50-200 nits |

**Rule:** if a number is being typed into the engine and its source can't be named,
look it up first. "Try 10 and see" wastes more time than the search would have.

---

## Fix the cause before the compensation

**Case from 2026-09-02:** pinned exposure on an interior that had no light in it.
Exposure was the compensation; the missing light was the cause. Pinning first just
produced black, and made it impossible to tell which problem was which.

**Order:** get the underlying thing physically right, *then* lock down the layer
that was papering over it.

---

## Change one thing, and be able to revert

Every change should be listed so it can be undone. In one session the following
were changed, some right and some wrong:

- created a PostProcessVolume (wrong approach — deleted)
- raised its priority over UDS (wrong approach — deleted with it)
- nulled UDS's exposure bias curve (wrong — went with the volume)
- turned OFF `cast_shadow` on the glass hull panels (**correct, kept** — a
  translucent material still casts a fully opaque shadow in UE, so the glass was
  blocking all sunlight into the interior)

Being able to say exactly which of those was still applied is what made it possible
to test cleanly.

---

## Scale changes which system is even in play

**Case from 2026-09-02:** diagnosed "shadows vanish at distance" as the sun's
`Dynamic Shadow Distance` being 20,000 uu (200 m) against a 13.4 km station.
Plausible, measured, and probably wrong — because with Virtual Shadow Maps enabled,
directional lights use a **clipmap** structure, not the old cascaded shadow
distance. The measured number was real; the system it belonged to was not the one
in use.

**Rule:** confirm which rendering path is active before attributing a symptom to a
setting from a different one.

---

## Documented findings worth keeping (with sources)

- **Translucent materials still cast fully opaque shadows** unless shadow casting is
  disabled. Blend mode alone does not let light through.
- **UDS Space mode disables all clouds, atmosphere and sky colouring**, leaving only
  sun, moon and stars — so there is *no atmospheric ambient light*. Interiors must be
  lit with practical lights.
  <https://www.ultradynamicsky.com/Documentation/V9/9-7>
- **UDS overrides post process volumes for exposure by design.** Use its own Exposure
  category rather than fighting it with volume priority.
- **A window gets a Rect Light sized to the opening** — the standard way to light an
  interior from an opening, rather than hoping GI carries the sun through.
  <https://80.lv/articles/setting-up-lighting-for-a-sci-fi-space-environment-in-unreal-engine-5>
- **Rect and Spot lights with physical intensities are traced more aggressively by
  Lumen than emissive surfaces** — prefer them for light that must bounce.
- **Shadow terminator problem:** low-poly geometry with high curvature and smooth
  normals produces shadow artifacts. Fix by increasing polygon count.
  <https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine>
- **Lumen surface cache fails on meshes that are too complex or too large** — commonly
  when an entire room or structure is one mesh. Fix by splitting the mesh, or raising
  Max Lumen Mesh Cards in the Static Mesh build settings. Pink in the Surface Cache
  view means Lumen cannot see that surface.
- **Auto-exposure meters average scene luminance.** A mostly-black frame (space) makes
  it open up and blow out the one lit object. Lock exposure for these shots.

---

## A measured value means nothing until it is compared to a reference

This is the rule the whole 2026-09-02 session existed to teach.

`Sun Light Intensity = 5.0` was measured **early** and noted as "worth checking".
It was not compared to anything, so it sat there while three separate symptoms were
chased for over an hour. Real daylight is ~100,000 lux. The sun was **20,000× too
dim**, and every symptom was downstream of it:

- interior black (nothing to bounce)
- exterior blown out (auto-exposure metering a near-black scene, then amplifying)
- planet black (too dim to survive any sane exposure)
- pinning exposure gave black (pinned for light that did not exist)

**Rule:** when a number is read out of the engine, immediately ask *what should this
be?* If that question can't be answered, look up the reference before moving on. An
unanchored number is not evidence.

Useful anchors:

| quantity | reference |
|---|---|
| Sunlight | ~100,000 lux → EV100 ≈ 15 |
| Overcast day | ~1,000-2,000 lux → EV100 ≈ 8.6-9.6 |
| Starlight | ~0.001 lux → EV100 ≈ -8 |
| Emissive: candle | 5-10 nits |
| Emissive: fluorescent tube | 50-200 nits |
| EV100 from lux | `EV100 = log2(lux / 2.5)` |

---

## A probe reading is only valid where the probe is

The HDR (Eye Adaptation) illuminance meter reads **one point**, chosen by the current
view. A reading of 994.993 LUX was taken in one camera framing and applied as if it
described the scene. Moving the camera dropped it to 4.742 LUX — a 200× difference,
same scene, same instant.

**Rule:** take the reading in the shot being lit for. If the camera moves, the number
is void.

---

## Third-party Blueprint properties: try the DISPLAY name

UDS's variables appeared unreachable from Python — `list_class_properties` returned
only inherited `AActor` properties, and every snake_case guess failed. They are in
fact fully readable and writable using the **display name with spaces**:

```python
uds.get_editor_property('time_of_day')   # fails
uds.get_editor_property('Time of Day')   # 1593.599939
```

Confirmed working: `Time of Day`, `Sky Mode`, `Sun Light Intensity`,
`Moon Light Intensity`, `Sky Light Intensity`, `Overall Intensity`,
`Night Brightness`, `Space Glow Brightness`, `Cloud Coverage`,
`Apply Exposure Settings`, `Simulate Real Stars`, `Latitude`, `Longitude`,
`Planets/Moons` (note: no spaces around the slash).

**Still unreachable:** members *inside* a Blueprint struct (e.g. an entry of
`Planets/Moons`). Those are opaque - the Details panel is the only way in.

**Rule:** before concluding a marketplace asset can't be driven from Python, try the
display name.

---

## Physical correctness and readability are different goals - choose deliberately

With the sun at a realistic 100,000 lux and exposure pinned to match (EV 15.3), the
scene became physically correct **and** lost every star, because starlight sits ~20
stops below daylight. Real photographs of sunlit spacecraft have black skies for this
exact reason.

Sun brightness, exposure pin, and background visibility are **one linked system**:
raise the sun → raise the pin → the background falls out the bottom.

**Rule:** decide which of the two you're serving before changing any of the three, and
say which it is. "Physically accurate" and "reads well" are both legitimate; drifting
between them by accident is not.

---

## UDS Space Layer — which control does what

Resolved 2026-09-02 after raising the wrong value three times. The names are
misleading, so this is worth keeping.

| control | what it actually affects | where |
|---|---|---|
| `Space Layer Brightness (Day)` / `(Night)` | **the planet BODY** — this is the one | Space Layer category, actor level |
| `Space Glow Brightness` | only the diffuse **halo around** the planet | Space Layer category, actor level |
| `Light Vector` | which light defines the lit/dark side (Sun / Moon / Custom) | inside `Planets/Moons` entry |
| `Dark Side Tint` | colour of the unlit side — near-black by default | inside `Planets/Moons` entry |
| `Emissive Texture` (+ tints) | night-side city lights, for a readable dark side | inside `Planets/Moons` entry |
| `Parent` | what the planet moves with; **No Parent = fixed, does not follow the sun** | inside `Planets/Moons` entry |

A planet rendering as a pure black disc that still occludes stars is almost always
one of:

1. **Body brightness too low for the current exposure** — the usual cause. Fix with
   `Space Layer Brightness (Day)/(Night)`. Values scale with how bright the pinned
   exposure is: with exposure at EV ~1, a value of 5 was invisible and 200 read well.
2. **Facing its dark side** — `Light Vector` is pointed at a light with no intensity,
   or `Parent` is No Parent so the planet's fixed orientation and the sun's moving
   direction produce an unlit phase. No brightness value fixes this; use the
   `Emissive Texture` city-lights layer instead.

Note `Space Glow Brightness` is a trap: it sounds like the planet's brightness, sits
right next to it, and does nothing to the planet body.

**Python access:** the Space Layer *actor-level* values are settable by display name
(`'Space Layer Brightness (Day)'`, brackets included). Everything inside a
`Planets/Moons` entry is an opaque struct — Details panel only.

---

## Sky background and subject brightness are one system

Three values must be tuned together, never alone:

```
Sun Light Intensity  ->  what the subject receives
Pinned EV100         ->  what the camera exposes for
Star / Space Layer brightness -> whether the background survives that exposure
```

Change one and the other two need revisiting. Observed on 2026-09-02:

| sun | pinned EV | result |
|---|---|---|
| 5 lux | auto (−7.13) | station blown out, stars fine, Earth lit |
| 5 lux | 0.92 | station correct, stars gone until raised, Earth black until raised |
| 100,000 lux | 15.29 | physically correct, everything in the sky gone (~20 stops down) |

There is no setting that gives a sunlit subject *and* a visible star field. Real
photographs of sunlit spacecraft have black skies. Games cheat by pushing the
background far past physical values — which is a legitimate art decision, but make it
knowingly.

---

## Save the level BEFORE deleting redirectors

**Case from 2026-09-04.** Renamed `Meshes/Refined/` to `Meshes/Station/`, verified all 57 level
actors now pointed at the new paths, then deleted the leftover redirectors. The level had **not
been saved** since the rename, so the `.umap` and external actor files on disk still held the old
paths. Deleting the redirectors removed the only bridge between them.

Result on the next editor restart:
- **58 of 60 StaticMeshActors had `mesh = None`**
- every mesh asset's material slot fell back to `WorldGridMaterial`

Recovered by name-matching actors to assets, but the mesh assets' *default* materials could not
be restored — there is no Python API for it (`EditorStaticMeshLibrary.set_material` and
`StaticMeshEditorSubsystem.set_material` do not exist). Only component overrides could be set.

**Rule:**
```
1. rename / move assets
2. SAVE THE LEVEL          <- the step that was skipped
3. save all dirty assets
4. only then Fix Up Redirectors / delete them
```

**The deeper error:** in-memory references updating is not evidence that on-disk references
updated. Redirectors exist precisely for the things that are *not* currently loaded. This is the
same failure as the exposure guess earlier — verify one thing, assume it covers another.

---

## Don't edit a PCG graph through Python while its editor is open

**Case from 2026-09-04.** Added, removed and rewired PCG nodes via Python while the graph asset
was open in the editor. `remove_node` returned `None` rather than a success value, and the graph
ended up in a state the editor rejected:

```
LogPCGEditor: Error: Invalid PCGGraph
```

Symptoms: nodes added from Python never rendered in the open editor, and clicking any node in the
palette silently did nothing. The asset then could not be deleted — 5 native references held by
`GCObjectReferencer` — until the editor was restarted.

**Rule:** PCG graphs are edited in the editor. Python is for *reading* them — node lists, settings
values, generated instance transforms. If a graph must be written to, close its editor first, and
expect to verify the result by reopening it.

---

## Nanite — what it does, what it does NOT do

Measured on UE **5.7.4**, 2026-09-07.

### Blend mode support — the hard constraint

| blend mode | Nanite |
|---|---|
| Opaque | supported, optimal |
| Masked | supported since 5.1, **substantially more expensive** than opaque |
| **Translucent** | **NOT supported.** The mesh renders with the *default material* and logs warnings. |

Measured in this project: `r.Nanite.AllowMaskedMaterials = 1`. The only translucent
materials are `M_Window` / `MI_Window_Belt`, used by `SC_Refined_SM_Hull_Glass_A/B/C`.
**Those three must stay non-Nanite.** Everything else in the project is opaque.

### What Nanite does NOT fix

**It does not fix the shadow terminator problem.** Nanite *manages* geometry — clusters it,
culls it, LODs it. It does not *create* it. A 1,083-poly mesh stays 1,083 polys. Epic's fix
for the terminator artifact is still "increase the polygon count".

```
Nanite        makes dense geometry CHEAP   (you can afford it)
Subdivision   makes geometry DENSE         (you still have to do it)
```

**Nanite Tessellation is not a substitute either.** It exists in 5.7 but is gated:

```
r.Nanite.AllowTessellation = 0     <- OFF by default in this project
r.Nanite.Tessellation      = 1     <- runtime flag, gated by the above
```

It is runtime displacement from a map — *surface detail*, not silhouette. It will not round
out a cylinder that is one polygon per 12 metres.

### What Nanite does NOT replace

| system | relationship |
|---|---|
| **World Partition** | Not interchangeable. WP streams **by actor** — a single 13.4 km actor is all-or-nothing no matter how Nanite handles its interior. **Segmentation is still required for streaming.** |
| **LODs** | Nanite **supersedes** them. A Nanite mesh ignores its LOD chain. Do not author LODs for Nanite meshes — the work is discarded. |
| **HLOD** | Cooperates. Nanite near, HLOD for distant region-level representation. |

### Does splitting a mesh cost more draw calls?

Yes for the pieces actually drawn — and that is the point. One 13.4 km mesh is submitted
**in full** whenever any part of it is on screen; you cannot cull half a mesh. Twenty
segments cull independently, so in practice fewer are drawn. The draw-call cost only starts
to bite in the hundreds-to-thousands of pieces, nowhere near 8-20.

### New in 5.7, unverified against Epic's own release notes

`NaniteSettings` gained `voxel_level`, `voxel_ndf`, `voxel_opacity` — the Nanite Foliage /
Voxels system, aimed at dense vegetation without LOD popping. Possibly relevant to the
`VEG_*` modules. **MegaLights** is in beta with improved translucency and particle shadowing.
Both worth confirming in Epic's docs before planning around them.


## Surface swapping — three assumptions a second surface exposed

*2026-09-09. Every one of these read as correct while only one surface existed.*

| assumption | why it stayed hidden | how it surfaced |
|---|---|---|
| world offset typed into `Transform Points` | it *was* the belt actor's address | points flew to the belt while the camera looked at the plane |
| `Copy Points` on `Relative` scale | the belt actor's scale is exactly **1**, so x1 is invisible | plane scale 519.8 → **26 km cubes** |
| `Mesh Sampler` radius 5000 | tuned for a 7,900 m belt | a 100 uu plane asset → **1 point** |

**Rule:** a setting that is wrong can look right when the value happens to be identity.
Building the second surface is not just proof of portability — it is how the assumptions get
found. Anything surface-scale-dependent belongs in a subgraph **parameter**, not a typed value.

**Also:** `Mesh Sampler` reads `RENDER_DATA` LOD 0, which on a **Nanite** mesh is the coarse
fallback. Enabling Nanite silently dropped belt sampling from 90 points to 64.


## Asset imports must NOT go through the MCP Python bridge

**Crashed the editor 2026-09-10.** Calling `AssetTools.import_asset_tasks()` from the MCP
Python bridge asserts and takes the editor down:

```
Assertion failed: ++Queue(QueueIndex).RecursionGuard == 1
Engine/Source/Runtime/Core/Private/Async/TaskGraph.cpp  Line: 689

callstack: PythonScriptPlugin -> UnrealMCPython.dll
           -> FMCPythonTcpServer::ProcessDataOnGameThread()
```

**Why:** the import internally waits on the task graph for texture compilation, and the bridge
is already executing inside a game-thread task. Pumping the task graph from inside a task that
is pumping it is what the recursion guard exists to catch.

**Rule:** import assets through the **Content Browser** (drag and drop, or Import button).
Afterwards, Python can safely *read* and *set properties* on the imported asset — those are
plain property access with no task-graph involvement.

**Same family as:** editing PCG graphs via Python (corrupts the graph). Some editor operations
are not safe to drive remotely; the bridge is for measuring and property-setting, not for
operations that internally block on engine subsystems.

**Also of note:** the file was a 93 MB, 10000 x 5000 Radiance HDR. Size was not the stated
cause, but a sky-light cubemap never needs 10K — downsize to 2K before importing anyway.

---

## Ultra_Dynamic_Sky owns the Sky Light — set the actor's variables, not the component

**Symptom:** setting `SkyLightComponent.cubemap` via Python appeared to succeed (read-back
confirmed `HDR_multi_nebulae_1`, resolution 1024). A second read moments later showed
`FlatCubemap` at resolution 128. UDS had stamped its own values back.

**Cause:** UDS drives the sky light from its own Blueprint variables every tick / construction
run. Writing the component is always overwritten.

**The controls (measured, exact internal names, spaces included):**

```
Sky Light Mode                              UDS_SkyLightMode enum
Sky Light Cubemap                           TextureCube  <- the real control
Sky Light Intensity
Sky Light Cubemap Angle
Sky Light Lower Hemisphere Tint (Cubemap)
Sky Light Intensity Multiplier In Interiors
Skylight Leaking / Full Skylight Leaking Distance     (post process, Lumen)
```

`UDS_SkyLightMode` = Capture Based · Custom Cubemap · Cubemap with Dynamic Color Tinting.
There are **two** SkyLightComponents on the actor: `SkyLight` (capture based) and
`Cubemap Sky Light`; the mode decides which is visible.

**How the names were found:** Python reflection on a Blueprint actor returns only the base
`Actor` class — `dir()` shows no Blueprint variables. FNames are stored as plain strings in the
`.uasset` name table, so:

```bash
grep -aoE "[ -~]{4,}" Ultra_Dynamic_Sky.uasset | grep -Ei "cubemap|skylight" | sort -u
```

This also returns Epic's and UDS's own tooltips. It is faster and more reliable than searching
the web for how a Blueprint behaves — same principle as reading the PCG engine headers.

**The measurement that mattered (identical framing via `capture_actors`, one variable):**

```
Courtyard Daylight HDRI @ 20    near-black, only the sun-lit wing edge reads
Courtyard Daylight HDRI @ 600   hull, rings, glass, belt all read
FlatCubemap             @ 600   brighter still - the agriculture belt's green reads
nebula HDRI             @ 20    indistinguishable from black
```

**Conclusion:** the interior was black because `Sky Light Intensity` was **20, ~30x too low** —
not because the cubemap was dark. The flat grey cubemap beats a real daylight HDRI here, because
it is uniform and UDS tints it by time of day. The 93 MB HDRI import was unnecessary.

**Rule:** before hunting for a better asset, test whether the *scale* is wrong. And when
comparing two looks, capture from a fixed pose — `capture_actors` frames by actor bounds and is
repeatable, whereas `capture_viewport` moves the moment the user flies the camera, which
invalidated the first three comparisons made here.

---

## Light intensity does not survive a change of scale — inverse square is brutal at 1 km

`RectLight_Window_A/B/C` were set to **100,000 candelas** with a 7 km x 900 m source and a 4 km
attenuation radius. They appeared to be working; hiding all three and re-capturing the same
frame was **indistinguishable**. They were contributing nothing, inside or out.

```
illuminance = intensity / distance^2
100,000 cd / (1,000 m)^2  =  0.1 lux          direct sunlight is ~100,000 lux
```

Six orders of magnitude short. 100,000 cd is a sane number for a window in a room; the cylinder
interior is 993 m from axis to hull, so the same number is worthless. Same family as the Mesh
Sampler radius tuned for 7,900 m: **a value calibrated at one scale is not wrong-looking at
another, it is just dead.**

**Rule:** whenever a light, radius, or distance moves between scales, recompute it rather than
nudging it. For lights, `I / d^2` gives the answer in one line.

## The interior/exterior lighting contradiction, and why it is not one

The interior wanted high ambient; the exterior wanted near-zero (space). Driving both from
`Sky Light Intensity` is a genuine conflict — 600 lit the interior and washed the exterior, 15
fixed the exterior and killed the interior.

**Attempted fix that FAILED:** hand the interior to the rect lights (1e9 cd) and drop Sky Light
to 15. Measured: the rect lights do light the ground and the PCG cubes — hiding them turned the
frame black, so they work. But all three sit at the glass panels emitting *radially inward*, and
the endcaps' surface normals point *along* the axis, so the endcaps receive them at grazing
incidence and went pure black. Three window lights are not a complete interior rig.

**What actually works — the difference is one float:**

```
2026-09-10 artist-set:   Sky Light 50   Sun 2000     -> 24:1 key-to-fill
earlier approved:        Sky Light 100  Sun 1000     -> 6.4:1
```

**The two lights are in different units — you cannot ratio them directly.** Per Epic's docs,
Directional Light is *illuminance* in **lux**; Sky Light is *luminance* in **cd/m2**, multiplied
by the cubemap's pixel values. Convert with the Lambertian relation `E = pi * L`:

```
fill_lux  =  pi * SkyLightIntensity * P          P = average cubemap pixel (FlatCubemap ~0.53)
key_lux   =  SunLightIntensity
SkyLightIntensity for a target ratio  =  SunLightIntensity / (ratio * pi * P)
```

P was calibrated from the observation that Sky 600 read "brighter than the sun" at Sun 1000:
`pi * 600 * P = 1000` -> P ~ 0.53, i.e. mid-grey, as expected for a flat grey cubemap.

Sourced reference points: direct sun at 1 AU = **128,000 lux**; Earth albedo mean **0.3**
(orbital average 24-42%). Cinematography convention: 2:1 flat, 4:1 medium, 8:1 dramatic.

The Sky Light is omnidirectional, so no value satisfies both at once and no local light rig has
so far replaced it. Changing one value per shot type costs nothing, duplicates nothing, and
cannot drift. Rect lights stay at 100,000 (they contribute little at that value, but they are
the placed rig for later tuning).

**Process failure worth more than the lighting finding:** the interior was already approved as
"almost perfect" at Sky Light 100, with only the exterior outstanding. The next change altered
the *interior* to chase a single-setup theory, breaking the approved half to fix the unapproved
half. **When one half of something is signed off, work only on the other half.**

**Rejected alternatives, with reasons:**

- **Duplicate the map** — two copies of geometry that must both receive every Blender reimport,
  and they will drift. Also duplicates 70 World Partition external actor packages.
- **UDS "Apply Interior Adjustments"** — driven by *player camera position* and it modulates the
  single global sky light. Through the glass panels the interior and space are visible in the
  same frame, so a camera-based switch pops, and while inside, the space seen through the glass
  gets the interior's ambient.
- **A level split** — same reason: you cannot be in two levels in one shot, and this station is
  built to be seen through.
- **Lighting Scenarios** — a baked-lightmap feature; this project is fully dynamic, and the
  engine's World Partition source contains no references to them.
- **Data Layers** — *not* rejected. The correct tool if per-shot lighting variants are ever
  needed: toggleable sets of lighting actors, geometry stays single-source. Zero exist so far.

---

## PCG attribute names are NOT case-sensitive — the old rule was wrong

This project carried the rule *"Attribute names are case-sensitive; `weight` != `Weight`, and the
UI field auto-lowercases what you type."* **Both halves are false.** Verified against UE 5.7
engine source 2026-09-10, file and line for each step:

| claim | evidence |
|---|---|
| PCG reads the *authored* field name from a Blueprint struct, not the GUID-suffixed internal name | `PCGDataTableElement.cpp:150` — `RowStruct->GetAuthoredNameForField()` |
| the attribute selector does not transform what you type | `PCGAttributePropertySelector.cpp:424` — passes the string straight to `SetAttributeName` |
| `SetAttributeName` stores the FName verbatim | `PCGAttributePropertySelector.cpp:141` |
| attribute lookup is case-**insensitive** | `PCGMetadataCommon.h:151,156` — `FPCGAttributeIdentifier` keys on `FName`; `operator==` and `GetTypeHash` both go through FName, which compares on the case-insensitive comparison index |
| nothing in PCG lowercases attribute names | no `ToLower` in `PCG/Private/Elements` or `PCG/Private/MeshSelectors` except the explicit String Operation node |

`DT_Modules` is a `UserDefinedStruct` row (`S_ModuleRow`, 37 rows), columns:
`Category, Zone, Belt, Mesh, Weight, RotationMode, Clearance, Source`. PCG sees `Weight`.

**So whatever failure produced this rule had another cause.** Two candidates found while reading
`PCGMatchAndSetAttributes.h:109-121`:

- `bUseWeightAttribute` ("Use Weight Attribute") is an `EditCondition` on `Match Weight
  Attribute`. Untick it and the field is inert while still *displaying* your typed value.
- `Match Weight Attribute` is declared `PCG_DiscardPropertySelection`, so a `$Property` entry is
  rejected there — attributes only.

Note there are **two** weight fields on that node and they are not interchangeable:
`InputWeightAttribute` (weight carried on the incoming points) and `WeightAttribute`
(DisplayName **"Match Weight Attribute"** — the weight column on the match data, i.e. the table).

**The general lesson:** this rule survived for weeks because it was plausible and was never
checked against source. A rule recorded from a single failed attempt is a hypothesis, not a
fact — mark it as such until the mechanism is verified.

---

## `InlineEditConditionToggle` — the checkbox with no row

`Match And Set Attributes` ignored the `Weight` column for weeks. The recorded cause was
"PCG lowercases the name and PCG is case-sensitive." Both halves were false. The real cause:

```cpp
// PCGMatchAndSetAttributes.h:116
meta = (DisplayName = "Use Match Weight", InlineEditConditionToggle, PCG_Overridable)
bool bUseWeightAttribute = false;
```

`InlineEditConditionToggle` tells the Details panel **not to give the bool its own row**. It
renders as a small unlabelled checkbox *to the left of* the field it gates. So the
`Match Weight Attribute` field accepts your typed name, displays it back, and does nothing.
There is no error and no warning. It reads exactly like the name being rejected.

**Rule:** when a PCG field accepts a value and has no effect, grep its header for
`EditCondition` before doubting the value. Any property whose `EditCondition` bool is marked
`InlineEditConditionToggle` has a hidden checkbox next to it.

Also on that node: `bMatchAttributes` defaults to **false**, which means *random* selection
rather than point-to-table matching (`PCGMatchAndSetAttributes.h:77`). Random + Use Match Weight
is exactly the setup for weighted variety with no zoning, which is what the weight test used.

**Verified working 2026-09-10:** SM_Cube (total weight 3.0) and SM_Cone (0.8) spawning at
roughly 79/21.

---

## Substrate glass — `M_Window`, solved 2026-09-11

**This project has Substrate ON** (`r.Substrate=True` in `DefaultEngine.ini`). Every "UE5 glass
material" tutorial online describes the **legacy** path (Shading Model = Thin Translucent). That
advice does not apply here and will waste a day. Check `r.Substrate` before taking any material
advice from the internet.

**The symptom:** window looked like flat grey film. `Metallic`/`Specular`/`Roughness` greyed out
on the output node. Then, after rebuilding as Substrate, completely opaque.

**Two causes, both invisible from the graph:**

**1. Translucency Lighting Mode was `Volumetric NonDirectional`** — Epic's tooltip
(`EngineTypes.h:317`) says *"Use this on particle effects like smoke and dust... the material
normal is not taken into account."* No specular at all. That is the smoke-and-dust mode, on a
window. Correct value is `Surface ForwardShading` (`TLM_SurfacePerPixelLighting`), whose tooltip
says *"Use this on translucent surfaces like glass and water."*

**2. The Slab's `SubSurfaceType` was stuck on `Diffusion`.** This is the one that cost the most
time. It is a **dropdown in the Slab node's Details panel**, not a pin, so it is invisible in
every screenshot of the graph. `MaterialExpressionSubstrate.h:21-23`:

```cpp
MSS_Diffusion     ToolTip="Diffusion based sub-surface scattering"
MSS_SimpleVolume  ToolTip="Approximation of optically thin slab (e.g.: glass)
                           where light is visible through the material"
```

Diffusion is opaque by definition - light scatters in and never leaves. **Set it to
`Simple Volume`.**

**Why changing the blend mode did not fix it:** the code that derives `SubSurfaceType` from the
blend mode (`Material.cpp:4271`, `ConvertSlabExpressionMaterialSubSurfaceType`) runs **only
during asset conversion**, never on a settings change. The value was stamped `Diffusion` when
`M_Window` was auto-converted to Substrate and stayed there permanently.

**Blend mode naming trap** (`EngineTypes.h:253-256`):

```cpp
BLEND_TranslucentGreyTransmittance = BLEND_Translucent   // SAME VALUE - plain "Translucent"
BLEND_TranslucentColoredTransmittance                    // separate entry, value 7
   DisplayName = "SUBSTRATE_ONLY - Translucent - Colored Transmittance"
```

Picking "Translucent" silently gives **grey** transmittance and discards the tint's colour.

**The working recipe:**

```
root:   Blend Mode    Translucent - Colored Transmittance   (the SUBSTRATE_ONLY entry)
        Lighting Mode Surface ForwardShading
        Screen Space Reflections  ON
        Is Thin Surface           ON
        Two Sided                 ON
        Refraction                None      (a flat pane barely refracts; warps at 7 km)

graph:  Substrate Slab BSDF -> Substrate Coverage Weight -> Front Material
        Diffuse Albedo   0,0,0     glass has no diffuse; grey here reads as frosted plastic
        F0               0.04      glass IOR 1.5; Epic's dielectric range is 0-0.08
        Roughness        0.02      near-mirror
        Coverage Weight  1.0       coverage scales the REFLECTION too - low coverage = no glass
        SSS MFP      <- GlassTint -> Substrate Transmittance-To-MeanFreePath -> MFP

node:   Slab Details -> Sub Surface Type = Simple Volume     <- NOT a pin. Easy to miss.
```

**The diagnostic that mattered:** the orange banner at the bottom of the Slab node states its
classification. It read `SSS Diffusion (Opaque)` the entire time. **Read that banner** - it says
what Substrate thinks the slab is, and no amount of wiring will override it.

**Also found:** `r.Substrate.ProjectGBufferFormat=0`, written by the **project template**, not
chosen. `RenderUtils.cpp:1960` describes 0 as *"Substrate materials are fit into a blendable
GBuffer... **lots of visual effects and fidelity are lost.** ... enforce ClosuresPerPixel=1."*
Engine default is 1. Changing it needs an editor restart.

**Also set (2026-09-11):**
- `r.Lumen.TranslucencyReflections.FrontLayer.EnableForProject=1` in `DefaultEngine.ini`. Ships
  **OFF**; without it translucent surfaces only get the low-quality Radiance Cache (glossy, no mirror).
- `GlassTint` 0.97 / 1.0 / 0.98 is an **instance override** on `MI_Window_Belt`, not in the master.

**Leftovers (checklist job 5):**
- The `NightOpacity` / `DayOpacity` / `DayNightBlend` Lerp still feeds `Opacity Override`, which
  Substrate greys out and ignores. Move it onto the tint, or delete it.
- Window rect lights: 6500 K with `use_temperature=False`, `cast_shadows=False` on all 3. To wire to
  `MPC_DayNight`: `WindowEmissiveIntensity`, `WindowEmissiveColor`, `AmbientTint`.

---

## A `False` return does not mean the write failed

`unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value()` returned **False**
while setting `GlassTint` on `MI_Window_Belt` on 2026-09-11. The read-back showed the value
applied correctly and the override registered.

Companion to the `static_materials` trap, which fails *silently while returning nothing*. Between
them: **a UE Python write can succeed while reporting failure, and fail while reporting nothing.**
The return value carries no information either way. Only a read-back does.

## Material assets open in the Material Editor will overwrite external writes

`M_Window`'s Blend Mode was set to `TranslucentColoredTransmittance` via Python and verified.
Some time later it read `BLEND_TRANSLUCENT` again - the Material Editor had the asset open, and
applying node changes there wrote its stale in-memory copy over the Python change.

**Rule:** before setting a property on a material from Python, close it in the Material Editor -
or set it in the Details panel instead. Prefer putting values on a **material instance**: no
shader recompile, and the master's open editor cannot clobber it.

---

## Gitignoring a content folder does not ignore its level's actors

The Vehicle feature pack was ignored with `Content/VehicleTemplate/` and `Content/Vehicles/` on
2026-09-11, verified "0 tracked". Three days later **41 of its files were still staged**:

```
Content/__ExternalActors__/VehicleTemplate/    38 files
Content/__ExternalObjects__/VehicleTemplate/    3 files
```

**Why:** World Partition stores each level's actors as separate packages under
`Content/__ExternalActors__/<map path>/`, **outside** the folder the level itself lives in. The
pack ships a demo map, so its actors landed in a path the content-folder rule never covered.
The verification checked the paths the rule named, not the paths the pack actually wrote.

**Rule:** when ignoring any marketplace/Fab/feature pack that contains a map, also ignore
`Content/__ExternalActors__/<PackName>/` and `Content/__ExternalObjects__/<PackName>/`. Then
verify with a sweep rather than by path: `git status --porcelain | grep -i <packname>`.

Also check what the pack edited outside Content: this one enabled `ChaosVehiclesPlugin` in the
`.uproject` and added input mappings to `DefaultInput.ini`, and dropped template input assets in
`Content/Input/` (confirmed unreferenced by project content before ignoring).

---

## Terrain — Modeling Mode + Gaea (spike 2026-09-14)

Decision + rejected options: `project_log.md` → Terrain. Design: `layer_contract.md` → L0's surface.

### The belt (measured 2026-09-11)

116,744 verts / 233,472 tris, 11.6 m avg edge, 994.73 × 7,900.11 × 162.61 m, 15.7 km² (both shell
faces). Its `UVMap` is a packed material unwrap with 4.3× texel-density spread — unusable for terrain.
**Never feed the belt into Gaea** — Gaea rasterises meshes to heightfields and destroys the curve.
Terrain is generated unrolled in 2D and mapped by UV. **One mesh, no chunking:** Nanite already splits
into 128-tri clusters; 630k tris ≈ 9 MB; World Partition streams actors, not geometry.

### Spike results (`Testing_Map`, asset `/Game/Maps/_GENERATED/johnnykong/Rectangle_270F106C`)

| step | settings | measured |
|---|---|---|
| Rect | Depth 100,000 (X) / 200 subdiv · Width 50,000 (Y) / 100 subdiv · Ground Plane | 40,000 tris, 1,000 × 500 m |
| Warp Bend | Upper +50,000 · Lower −50,000 · Bend 60° · Lock Bottom off | 954.93 m wide, 127.94 m rise = R 954.9 m exactly |
| Displace | Texture2D Map `T_Perlin_Noise_M` · Base 0 · Intensity 5,000 · Subdiv 0 · UV Scale (1,2) | lowest Z +0.24 m, width 939.78 m → displacement is **inward** |
| Displace | Constant 0 · `Flat` · Subdiv 3 | 640,000 tris / 321,201 verts |
| Vertex Sculpt | default brush | smooth; Accept a few seconds; lowest Z → −14.4 m |
| PCG | Rectangle tagged `SurfaceSource`, `PCGVolume` + `PCG_SurfaceTest`, SamplingRadius 2000 | spawned modules followed the sculpt |

### Modeling Mode facts (UE 5.7 source)

- **Rect subdivisions ClampMax 500** (`AddPrimitiveTool.h:176`). Tool `Depth` runs along X, `Width`
  along Y (`AddPrimitiveTool.cpp:551`).
- **Rect UVs are aspect-scaled** (`RectangleMeshGenerator.cpp:43`) — the short side gets 0 → short/long.
- **Warp aligns gizmo Z to the longest bounds axis** (`MeshSpaceDeformerTool.cpp:162-187`). X-longest →
  gizmo Y = world up → bends upward. A square ties into the Y branch and bends sideways. On the 7.9 km
  sheet it picks the length — **rotate the gizmo by hand**. Bend keeps arc length.
- **Displace `Flat` subdivision** = `FUniformTessellate`: each triangle → (N+1)² (`UniformTessellate.h:21`).
  `PN Triangles` rounds the shape.
- **Displace base value** defaults to 128/255 — set 0 so black = no displacement. Intensity clamp
  −10,000 to 100,000; the slider only goes ±100, type the value.
- **Displace reads 16-bit and float textures at full precision:** `G16`, `RGBA16`, `RGBA16F`, `R32F`,
  `RGBA32F` (`Texture2DUtil.cpp:184-232`).
- **New assets are not saved** (`AutoGenerateButDoNotAutosave`, stored in `_GENERATED` next to the map).
  The map can save pointing at a mesh that is not on disk — Save All after every Accept.
- **Sculpting is destructive** (no layers). Re-displacing from a new heightmap should wipe hand
  sculpts — expected, untested. Order: Gaea → Displace first, sculpt last.
- **PCG follows edits:** Mesh Sampler tracks the sampled mesh (`PCGMeshSampler.cpp:545`); PCG
  refreshes on static mesh save (`PCGActorAndComponentMapping.cpp`, `OnObjectSaved`).
- **Nanite fallback:** complex-as-simple collision uses the fallback, not the Nanite geometry. Check
  Fallback Relative Error / Triangle Percent on the sheet, or you walk on a coarser shape than you see.

### Belt inner surface — measured in `Space_Colony` 2026-09-15 (MCP line traces from the axis)

- Actor `SC_Refined_SM_Belt_Residential`: pivot on the axis **(−221,760.55, 49,112.33, 175,805.30)**, rotation 0,
  scale 1. Bounds Y ±395,005 (7,900 m), X ±49,737, Z 76,380 → 92,641. **Axis runs along world Y.**
- **Radius 954.66 m** straight down at Y −300,000 and Y +400,000 (identical → axis parallel to Y) and at ±20°.
- **Near the edges the belt flattens outward:** 24° → 955.01 m · 26° → 955.79 m · 28° → 957.27 m (both sides) ·
  29° → 958.46 m · 29.5° → 959.23 m. Surface normals stop following the circle past ~23° (tilt ~24°).
- **±30.5° hits `Hull_Glass_A/B`** at ~974–976 m → the belt spans **±30°** (60°).
- Traces at the belt's middle (Y 49,112) hit **`SC_Refined_SM_Ring_Structure`** at ~955.5 m instead — a ring
  crosses the belt there. Measure belt surfaces away from rings.
- **The other two belts are the same belt rotated ±120° about the axis** (measured bounds, all three actors share the
  axis pivot, rotation 0, same 7,900 m length): `Belt_Industrial` bounds centre offset from the axis (+73,820, +43,082)
  with extents X 26,068 / Z 43,389; `Belt_Agriculture` (−73,828, +43,071) with X 26,039 / Z 43,362. A 60° arc
  rotated to 0°–60° predicts centre (735.8 m, 430.5 m) and extents (258.5 m, 430.5 m) — matches. The art table
  also lists the three belts as identical (116,736 quads each).
  → **Same terrain sheet fits all three**: duplicate the mesh asset per belt (Displace edits the asset), move its
  pivot onto the axis (Edit Pivot tool), rotate ±120° about Y.

### Full-sheet recipe — bend first, then stretch (BUILT 2026-09-16)

Warp bends along the longest side, so bend a near-square piece, then stretch along the axis:

1. Rect **Depth 99,800 (X) / 63 subdiv · Width 99,000 (Y) / 500 subdiv** — X longest so the gizmo auto-aligns.
   Arc radius = 99,800 / (π/3) = **953.0 m** (1.66 m inside the belt's 954.66 m).
2. Warp Bend **60°**, Upper/Lower **±49,900**, Lock Bottom off → expect ~953 m wide, ~127.7 m rise.
3. Actor **Scale Y = 7.98** (790,011 / 99,000) → 7,900 m long. Stretching along the axis leaves the arc unchanged.
4. **Bake Transform** (Bake Rotation on, Bake Scale = Bake Full Scale, Recenter Pivot off) — Epic's Mesh
   Distance Fields doc: "Non-uniform scaling cannot be handled correctly". Tool options from `BakeTransformTool.h`.
5. Displace `Flat` Subdivisions **2** → ~5.3 m grid, ~567k tris.
6. Displace **Texture2D Map** with the Gaea EXR: UV Scale **(0.1266, 1.008)**, UV Offset **(0.4367, 0)**
   (`UV = UV * UVScale + UVOffset`, `DisplaceMeshTool.cpp:216`). Rect UVs: U 0–1 across the width, V 0–0.992
   along the length → the belt runs along the image's **vertical** axis → Gaea LinearGradient **Direction 90**.
7. Place at **X −221,760.55, Y 49,112.33, Z 80,505.3** (lowest point = axis Z − 95,300). The pivot stays at the
   bottom centre through Warp and Bake (spike: location 0,0,0 with min Z 0 at the centre).

### Measured while building it (2026-09-16)

| step | predicted | measured |
|---|---|---|
| Rect | 63,000 tris · 998 × 990 m | 63,000 tris / 32,064 verts · 99,800 × 99,000 cm ✅ |
| Bend 60° | 953.02 m wide · 127.68 m rise | 953.02 m · 127.65 m ✅ |
| Bake Transform | Y 7,900.2 m · scale 1,1,1 | 7,900.2 m · 1,1,1 · X and Z unchanged ✅ |
| Displace Flat ×2 | 567,000 tris | 567,000 tris / 285,190 verts ✅ |

- **Bent-sheet lowest point sits at Z +3.29 cm, not 0** — the arc is cut into 63 flat segments and the centre
  falls between two vertices; the chord sag there is 3.29 cm exactly. Not an error.
- **Keep a duplicate of the bent+baked sheet** before displacing (`Backup1`). Displace edits the asset and the
  accept is **not undoable** — without a spare it is a four-step rebuild.
- **Verify by tracing from the cylinder axis, not from the bounding box.** Ground measured 897.6 m (centre),
  911.4 / 923.0 m at ±25° — all inside the belt's 954.66 m. Bounding-box reasoning misled repeatedly because the
  actor was not placed at the recipe coordinates.
- **The terrain floats 32–57 m above the belt plate** as placed; nudge ~35 m outward to close the edge gap.

### Displace tool — the parts that cost a day

- **UV orientation:** the arc direction selects image **rows**, the belt length selects **columns**. Gaea's
  `LinearGradient Direction 90` produced the band across *columns*, so the EXR had to be transposed
  (`Belt_Residential_Height_T.exr`). Fix at source next rebuild: **Direction 0** → `gaea.md` → 7d.
- **Transposing the image and swapping UV Scale/Offset are the same flip** — do both and they cancel. Symptom:
  long smeared streaks down the length.
- **Displace reads the texture's SOURCE, not the platform data** (`DisplaceMeshTool.cpp:869` calls
  `ReadTexture(..., bPreferPlatformData=false)` → `ReadTexture_SourceData`). So Compression Settings and sRGB do
  not affect displacement accuracy — only the material later. Source formats read at full precision: `BGRA8`,
  `RGBA16`, `RGBA16F`, `RGBA32F`, `R32F`, `G16` (`Texture2DUtil.cpp:184-240`).
- **Displace Intensity clamps to −10,000 … 100,000** (`DisplaceMeshTool.h`), slider only ±100 — type the value.
  So you **cannot** flip direction with a negative intensity at our scale (we need ±40,000).
- **Displacement Map Base Value defaults to 128/255** — set 0 or everything darker than mid-grey displaces the
  wrong way. It does **not** persist across a rebuild.
- **Rect UVs (source-confirmed):** `RectGen.Width = tool Depth` (X), `RectGen.Height = tool Width` (Y)
  (`AddPrimitiveTool.cpp:551`); the short side gets 0 → short/long (`RectangleMeshGenerator.cpp:43`).
- **Warp Bend is Beta** and its bend/normal direction is not consistent between rebuilds — Epic forum thread on
  bend direction. If displacement runs the wrong way, fix it with **Attribs → Normals → Invert Normals**, not
  with a negative intensity.

### Nanite fallback — 7d.4b, measured 2026-09-16

**Enabling Nanite with the default `Fallback Target = Auto` cut Render Data LOD 0 from 567,000 to 1,837
triangles** — a 99.7% reduction, ~90 m triangles across terrain that varies by tens of metres inside each one.

That matters because **both PCG and collision read the fallback, not the Nanite geometry**:

- `PCGMeshSampler.h`: `RequestedLODType = EGeometryScriptLODType::RenderData`, `RequestedLODIndex = 0` — so the
  Mesh Sampler scatters onto the fallback by default.
- Epic: the fallback is used "when a complex collision is needed, using lightmaps for baked lighting, and for
  hardware ray tracing reflections with Lumen". Our mesh is `CTF_USE_SIMPLE_AND_COMPLEX`, so line traces hit it too.

Engine defaults (`EngineTypes.h` → `FMeshNaniteSettings`): `bEnabled false` · `FallbackTarget Auto` ·
`FallbackPercentTriangles 1.0` · `FallbackRelativeError 1.0` · `KeepPercentTriangles 1.0` · `TrimRelativeError 0.0`.
**The percent/relative-error fields only take effect once `FallbackTarget` is off `Auto`.**

**Setting used (verified 2026-09-16):** Nanite on · **Fallback Target = Percent Triangles** · **Fallback Triangle
Percent = 100** · Collision Complexity = **Use Complex Collision As Simple**. Verified: Render Data LOD 0 back to
**567,000 tris / 285,190 verts**, identical to the source. Cost: a second full-res copy in memory.

- ⚠️ **The UI field is a percentage, the engine property is a 0–1 fraction.** Typing `1.0` in the Static Mesh
  Editor means *one percent* → 5,670 tris (567,000 × 1%, measured). Type **100**.
- The mesh had **0 simple and 0 convex collision shapes**, so under `Simple And Complex` line traces hit it but
  capsules and physics passed straight through. `Use Complex Collision As Simple` is required, not optional.
- **`Show → Nanite Fallback` (Ctrl + N)** in the Static Mesh Editor toggles the viewport between the Nanite mesh
  and the fallback — the direct way to see what collision and PCG actually use.
- Escape hatch if the 567k collision cook is too heavy: lower the fallback and set the Mesh Sampler's
  **`Requested LOD Type` to `Source Model`** so PCG stays exact while collision goes coarse.

### Gaea 2.3.0.1 Community (measured)

- **Build cap 1K.** The `Canyon River with Sea` example failed validation (*"build resolution is higher
  than allowed by your edition"*) — its file had Build **and** Preview Resolution 2048. A File → New
  project built at 1024 (Bake 2048 did not block it).
- **Terrains are square:** one `Width` + vertical `Height`. No tiles, regions, automation or variables
  on Community (official edition table).
- **Belt layout:** a 1 km band inside a 7,900 m square → ~7.7 m/px. The Rect's own UVs (V 0 → 0.127 on a
  7.9 × 1 km sheet) already match the band — no UV re-projection needed.
- **EXR export:** one channel `Y`, 32-bit float, no compression, 1024 × 1024, `INCREASING_Y`. Height
  port `Out` 0–0.249 (Height 2,500 m); mask port `Depth` 0–1. Heights are a **0–1 fraction**.
  *Metres = value × Height is the working assumption, unproven* (confirm: change Height, rebuild,
  values unchanged). Displace Intensity would then be Height (m) × 100.
- **Unknown:** which image edge is UV 0 in Unreal; whether Unreal imports the float EXR as R32F or RGBA16F.
- **Licence:** Community is non-commercial — check what that means for a public portfolio before publishing.

### City plateaus in Gaea

**Mask** (Edit Mask; `Blur` + `Iterations` for ramps) → **Constant** (height mode) → **Combine**:
Input 1 = Constant, Input 2 = terrain, Mask = city mask (bright = Input 1). **Not `Max` mode** — Max
keeps the higher value, so hills above the plateau survive. Level on the belt = one height value =
constant radius. Export the city mask as its own image.

### Slope on a cylinder — the `Normal To Density` trap

`Normal To Density` compares every point against ONE fixed vector (`FVector Normal = UpVector`,
`PCGNormalToDensity.h:51`); up turns 60° across the belt. Per-point up instead: `Attribute Maths Op`
Subtract (axis X −221,760, Z 175,805 minus `$Position`) → drop Y *(unverified: does Maths Op work
per component on vectors?)* → `Attribute Vector Op` Normalize → Dot with `$Rotation.Up` (Mesh Sampler
sets point Z = surface normal, `PCGMeshSampler.cpp:82`) → `Point Filter Range` (1.0 = flat;
cos 5° = 0.996). Baked alternative: Gaea **Slope** mask — cheaper, stale after an Unreal sculpt.

---

## Distance shadows — two candidates, untested

Measured: `cast_far_shadow = 0` on all 60 actors; `MaxPhysicalPages = 4096`. Check with
`Show > Visualize > Virtual Shadow Map` before changing either.

## Detail meshes — what is geometry, what is material

| detail | representation |
|---|---|
| changes silhouette · casts major shadow · needs collision | real geometry |
| edge / frame / seam / panel reused across assets | trim sheet |
| repeats across a broad surface | tileable + normal |
| shallow, fine, seen front-on | normal map |
| localised storytelling | decal |
| dirt / wear / weathering | vertex paint |

Nanite shifts this toward geometry: 55 meshes on Nanite, 454 k → 2.49 M tris at no measurable cost.
Separate objects, never edited into the shells — one rib modelled once, placed 400×, each a row in
the sheet. `M_Structural` measured 2026-09-14: one placeholder texture (`Textures/images`, also on
`MI_Belt_Agriculture`), no normal map, no grime parameter.
**Not adopted:** POM · vertex painting · decal atlases · Substance authoring — none serve the blockout user.

---

## Quick traps (moved from the checklist 2026-09-14)

| | |
|---|---|
| **PCG graphs** | Edit in the **editor**, not Python. A Python write with the editor open corrupted the graph — `Invalid PCGGraph`. |
| **World Partition** | Actors are separate packages. `save_current_level()` does **not** save them. Needs `actor.modify(True)` then `save_packages()`. Broke the level twice. |
| **Renaming assets** | **Save the level, then** delete redirectors. The other order nulled 58 mesh references. |
| **Mesh Sampler radius** | Default 10 uu = 10 cm. At 13 km that hangs the editor. Use **5000**. |
| **Cube scale** | A default cube is 100 uu — invisible at station scale. Scale points ~50×. |
| **Load Data Table** | No input pin — right-click **empty space**. |
| **Soft object paths** | Must be `Asset.Asset`. Short form spawns **nothing, silently**. Now caught by `check_mesh_paths`. |
| **Attribute names** | **NOT case-sensitive** — PCG keys attributes on `FName` (case-insensitive). |
| **Silent failures** | PCG often fails with no error. Turn **Debug** on each node and find the last one still holding data. |
| **Nanite hides tri counts** | `get_num_triangles(0)` on a Nanite mesh returns the **fallback**. `Hull_Shell_B` reports 46,132, is really 479,232. Check reimports by **bounding box**. |
| **Reimport keeps materials** | It **preserves** a binding when the slot name matches. `WorldGridMaterial` only happens on **first** import. |
| **Read back what renders** | A component `override_materials` entry beats the asset's default. Job 3 was ticked done while 33 actors still rendered `M_Temp`. Read `component.get_materials()`. |
| **`M_Temp` was two-sided** | `M_Structural`, which replaced it on 33 assets, is not. |
| **DataTable-only edits** | Re-exporting `module_list.xlsx` reverts edits made only in `DT_Modules`. StarterContent meshes break on clone (gitignored). |
| **Blender Edit Mode** | `object.data` with Edit Mode open is **stale**. Use `bmesh.from_edit_mesh()`. |
| **Names aren't evidence** | `SKM_Quinn_LOD0` is a StaticMesh, not skeletal, not Quinn — it's the 1.8 m human ref. |
| **"Off-centre" needs a reference** | Compare against the whole scene, not the part you're looking at. |
| **Modeling Mode assets** | Created but **not saved**. Save All after every Accept. |
