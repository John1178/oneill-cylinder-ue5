# Layer Contract — the city generation system

*2026-09-09 · the output of the Week 5 design block. Everything from zoning onward gets built
against this. If a layer needs something not listed as its input, the contract is wrong — fix
the contract first, not the graph.*

---

## Glossary — read this before arguing about a layer

*Added 2026-09-25 after "zone" was used for two different things in the same conversation.*

**The ground**

| term | meaning |
|---|---|
| **Belt** | one of the three landmasses inside the cylinder. Everything is built on the **Residential belt**, 7,900 × 998 m (`project_log.md` → One belt first). |
| **Surface (L0)** | whatever mesh PCG samples — the terrain sheet here. Swappable: plane or cylinder, same graph. |
| **Mask** | a greyscale image from Gaea describing the terrain: mountain, slope, river, bank, rock, soil. |
| **Point** | one candidate position carrying attributes. The unit that flows through every layer. |
| **Attribute** | a named value on a point: `UV`, `MaskUV`, `Mountain`, `Slope`, `Zone`, `Density`. |
| **Spacing / sampling radius** | distance between candidate points; sets the *maximum* packing (city 60 m, trees 6.4 m). |

**The city**

| term | meaning |
|---|---|
| **Zone** | the *type* of place — Residential / Service / Industrial. Decides **which modules** may spawn. A label, not a space. |
| **Density** | 0–1 survival chance per candidate point. Decides **how many** buildings. Not a count. |
| **Scatter / Rows** | the one logic switch in the system: organic Poisson, or a regular grid for farm and orchard. |
| **Road** | an artist-drawn spline (L2). Gives points `DistToRoad` and `RoadDir`. |
| **Block** | the area enclosed by roads (L3 stage 2). **A space, not a type** — this is the word for "between the roads". |
| **Frontage** | the band along a road where buildings line up; block interiors stay empty. L3 stage 1. |
| **Lot** | one building's parcel inside a block (`LotSize`). Stage 2. |
| **Zone stretch** | a run of belt carrying one Zone. (Say this rather than "district", which appears nowhere else.) |

**The content**

| term | meaning |
|---|---|
| **Module** | a row in `module_list.xlsx` → `DT_Modules`: mesh path, weight, zone. 37 rows, 13 meshes exist. |
| **Weight** | relative chance of a module being picked among those matching the zone. |
| **`Belt` column** | *in the spreadsheet only*: quality tier A hero / B support / All, read by the **validator**, never by PCG. Not the landmass. |
| **Instance** | the spawned mesh in the level (ISM). |
| **Preset** | a named set of numbers — zone split + density + Scatter/Rows. Data, not logic. |

**The plumbing**

| term | meaning |
|---|---|
| **Graph** | a PCG asset: `PCG_SurfaceTest` (city), `PCG_Vegetation` (trees). |
| **Subgraph** | reusable graph inside others: `SG_SurfaceSource` (sampling), `SG_TerrainMasks` (masks). |
| **Volume** | the actor running a graph: `PCGVolume_Test` (city), `PCGVolume` (trees). |

The two that get confused: **Zone is a type, Block is a space** · **Belt is the landmass everywhere
except the spreadsheet column, where it is a quality tier.**

---

## Who this is for

**One pipeline, three stages.** Not three audiences — the same tool at three moments in a
production.

| stage | who | what they need |
|---|---|---|
| **1. Blockout** ⭐ | **Art director** | Compare options fast, before concept art exists. "Show me this valley as a farm, a town, an industrial zone." |
| 2. Layout | Level artist | Refine spatial flow — draw roads, set density, control where things go |
| 3. Dressing | Environment artist | Control content and variety at close range; hand-override individual placements |

### Stage 1 is primary, and that decides a lot

> **A blockout tool for deciding what a place should be, before anyone commits to what it
> looks like.**

That is a different product from Epic's City Sample, not a worse version of it. Plenty of tools
*dress* an environment; very few help you decide **what to build** before anyone has drawn
concept art. That gap is real in production, and it is the pitch.

**What follows from naming the AD as the primary user:**

- **Greybox is correct, not a limitation.** Only 13 of 37 modules exist. For a pre-concept
  blockout that is not a weakness — a blockout is *supposed* to be grey and repetitive.
  Thin content stops gating the tool story. *(It still matters for the cinematic deliverable.)*
- **Presets are the headline feature**, not a nice-to-have. Fast option comparison is the
  entire job at this stage.
- **Hand-drawn roads are correct.** The AD is exactly the person who wants to draw the layout.
  Generating roads would take away the decision they came here to make.
- **L3 is settled: frontage-only.** A blockout needs massing and fast iteration, not lot
  subdivision. Block subdivision becomes a stage-2 upgrade for the level artist.
- **Regeneration speed is a feature.** If comparing options is the job, slow regeneration kills
  the tool regardless of output quality.

### The gap this exposes — known and deferred, not overlooked

Stage 3 is **not served yet.** All three controls (spreadsheet, splines, density) are *global*.
There is no way to say:

> *"that one building — move it two metres and lock it, and don't lose it when I regenerate."*

Every production placement tool has per-instance override that survives regeneration. Without
it an environment artist must bake to static meshes and edit by hand, which severs the
procedural link and makes the tool one-shot.

This is the same problem as per-region seeding: **locking and not-re-rolling are one feature.**
Deliberately out of scope for this project; named here because knowing what a production
version needs next is worth more than pretending it is finished.

---

## The one rule

> **Every layer consumes points carrying attributes, and emits points carrying attributes.**

That is the whole design. A layer never knows what produced its input or what consumes its
output — only the attributes. This is what makes layers swappable, and it is the surface thesis
applied all the way up:

- the **surface** is an input, not an assumption → flat ground or cylinder, downstream doesn't care
- the **density** is an input, not a rule → a village or a downtown, same graph
- the **road layout** is an input, not an algorithm → the artist draws, the system fills

The pitch that follows: **this is not a city generator. It is a settlement generator — and a
blockout tool for deciding what a place should be, before anyone commits to what it looks like.**

---

## The stack

```
L0  SURFACE      any mesh            ->  points {position, rotation}
L1  DENSITY      artist authoring    ->  + {Density}
L2  STREETS      artist splines      ->  + {DistToRoad, RoadDir}
L3  LOTS         subdivision         ->  + {LotSize}          <- OPEN, see below
L4  SELECTION    DT_Modules          ->  + {Mesh}
L5  SPAWN        instances
```

Status: **L0 partially built · L4 and L5 working and proven · L1, L2, L3 not started.**

---

## L0 — Surface  ⭐ *the thesis layer*

| | |
|---|---|
| **consumes** | one static mesh (any shape) |
| **emits** | points `{ position, rotation }` — rotation aligned to surface normal |
| **authored by** | choosing which mesh to feed it |
| **implemented as** | `SG_SurfaceSource` subgraph |
| **status** | sampling works; **not yet wrapped as a subgraph, no flat-ground twin** |

Rules:
- Must work on a plane and on the cylinder with **no downstream change**. That is the checkpoint.
- Outer shell face must be filtered out (inner r≈95,600 vs outer r≈99,600).
- `Mesh Sampler` emits **mesh-local** coordinates → always followed by `Transform Points`.
- Sampler radius **5000**, never the 10 uu default.

## L1 — Density

| | |
|---|---|
| **consumes** | L0 points |
| **emits** | L0 points + `{ Density: float 0-1 }` |
| **authored by** | **the artist** — this is the primary creative control |
| **status** | not started |

This is what makes the tool general. A low-density stretch is a village; a high-density stretch
is a downtown. Same graph, same modules, different input.

Density is an **artist input, not a derived rule.** Points below a threshold are culled here, so
everything downstream only ever sees points that survived.

**L1 also carries the one genuine logic switch in the system:**

| mode | used by | behaviour |
|---|---|---|
| `Scatter` | city, countryside | Poisson sampling, organic spacing |
| `Rows` | farm, orchard, solar field | regular grid, aligned to a direction |

Everything else that distinguishes a farm from a downtown is a **preset** (see below) — data,
not logic. This switch is the exception, and it is one boolean, not a second system.

## L2 — Streets

| | |
|---|---|
| **consumes** | artist-drawn spline actors |
| **emits** | spline data + `{ DistToRoad, RoadDir }` written onto L1 points |
| **authored by** | **the artist** — drawn by hand |
| **status** | not started |

**Roads are hand-drawn, deliberately.** The canonical pipeline (CityEngine, worldBLD) is
`streets → blocks → lots → buildings`, and the procedural value lives in the three stages
*after* the streets. CityEngine's most common production use imports real road data and
generates everything else; nobody calls it less procedural for that.

The spline does double duty: it is the **structural skeleton** and the **artist's spatial
control** at the same time. Drag it, the district rebuilds. That is the demo shot.

`RoadDir` exists because the schema already has `RotationMode = AlignToRoad`.

*Possible later:* artist draws arterials, system subdivides minor roads inside blocks.

## L3 — Lots  *frontage-only first; subdivision is a stage-2 upgrade*

| | |
|---|---|
| **consumes** | L2 output + street splines |
| **emits** | points + `{ LotSize, Frontage }` |
| **status** | **frontage-only** for the first build (see *Who this is for*); block subdivision deferred to stage 2 |

Both designs are documented below. Everything else in this contract holds either way, which is the point — swapping L3 touches no other layer.

**UE 5.7 core PCG already has the primitives for full block subdivision** — verified against the
engine source, no plugin required (`PCGPrimitives`, which the City Sample uses, is 5.8-only and
is NOT in this install):

```
Create Polygon 2D      closed polygon from points or splines
Polygon2D Operation    Union / Difference / Intersection / ExclusiveOr / CutWithPaths
Offset Polygon         expand-contract (= setback), morphological open/close
Polygon2DInteriorData  points inside a polygon
Create Surface From Spline · Convex Hull 2D · Create Points Grid
```

`CutWithPaths` is the block primitive — its own tooltip: *"Cuts polygons with paths by completing
them using the polygon bounds."* The whole chain is ~5 nodes:

```
boundary spline -> Create Polygon 2D                  the district
road splines    -> Polygon2D Operation CutWithPaths   -> BLOCKS
                -> Offset Polygon (negative)          setback -> LOT AREA
                -> Points Grid + interior cull        -> building points
                -> L4
```

**These nodes are 2D, and the surface is curved. That constraint is also the answer:**

> Do the city layout in **unrolled 2D** — belt length × circumference — then let L0 map the
> result onto whatever surface it was given.

Flat ground needs no mapping; the cylinder needs one wrap; the layout math never changes. This is
the surface thesis applied at the *city* level rather than the scatter level, and it means block
subdivision and the flat-ground twin are **the same work, not competing work**.

*Unverified — needs a 30-minute spike: one boundary polygon, two crossing splines, `CutWithPaths`,
check the blocks come out clean.*

## L4 — Module selection

| | |
|---|---|
| **consumes** | L3 points + `DT_Modules` |
| **emits** | points + `{ Mesh }` (soft object path) |
| **authored by** | **the artist, in Excel** — via the validator pipeline |
| **implemented as** | `Load Data Table` → `Match And Set Attributes` → `MeshSelectorByAttribute` |
| **status** | ✅ **working** — 90 instances proven 2026-09-07 |

- `Mesh` must be the `Asset.Asset` soft-path form. Short form spawns nothing, silently.
  Enforced by `check_mesh_paths`.
- Attribute names are **not** case-sensitive — PCG keys them on `FName`, whose comparison and
  hashing are case-insensitive (`PCGMetadataCommon.h:151,156`), and nothing in PCG lowercases
  what you type (`PCGAttributePropertySelector.cpp:424`). *The opposite claim stood here until
  2026-09-10; it was never checked against source.*
  This is why weighting is currently broken.

## L5 — Spawn

| | |
|---|---|
| **consumes** | L4 points |
| **emits** | static mesh instances |
| **implemented as** | Static Mesh Spawner |
| **status** | ✅ working |

PCG instances the **asset**, so every mesh asset must carry its correct material. An asset on
`WorldGridMaterial` spawns grey checkerboard however good the level looks. All 57 are bound.

---

## Presets — "which toolset am I generating?"

A space colony is not only a city. It has farms, factories, small towns and countryside, and
those are not style variations — a farm is rows and huge parcels with no street frontage, a
factory is a few enormous footprints with access roads.

**The layer stack never changes.** What changes is a preset: which modules are eligible, and what
the parameters are.

| preset | L1 mode | density | roads | clearance | Belt filter | rotation |
|---|---|---|---|---|---|---|
| **City** | Scatter | high | grid | small | Residential | `AlignToRoad` |
| **Town** | Scatter | medium | few | medium | Residential | `AlignToRoad` |
| **Farm** | **Rows** | low | dirt tracks | huge | Agriculture | `Fixed` |
| **Factory** | Scatter | medium | access only | large | Industrial | `AlignToRoad` |
| **Countryside** | Scatter | very low | none | huge | Greenery & Terrain | `Free` |

**A preset is DATA, not code.** It is a Belt filter plus a set of parameter values — so it lives
in the spreadsheet and in graph-instance overrides, both of which already exist and are already
validated. **Adding a sixth preset costs a row set, not an engineering task.**

That is the difference between a sample and a tool, and it is the same argument that justifies
the manifest pipeline: someone who cannot open a PCG graph can still change what comes out, and
the validator stops them shipping something broken.

> **What this is NOT:** four separate generators behind a menu. That would be four half-built
> systems competing for the same weeks. One stack, many presets.

---

## Attribute vocabulary

The complete list. If it isn't here, no layer may read it.

| attribute | type | written by | read by |
|---|---|---|---|
| `position` | vector | L0 | all |
| `rotation` | rotator | L0 | L5 |
| `Density` | float 0-1 | L1 | L1 (cull), L3 |
| `DistToRoad` | float | L2 | L1, L3 |
| `RoadDir` | vector | L2 | L5 (via `AlignToRoad`) |
| `LotSize` | float | L3 | L4 |
| `Belt` | name | Excel | L4 |
| `Mesh` | soft path | L4 | L5 |
| `Weight` | float 0-1 | Excel | L4 |
| `Clearance` | float | Excel | L3 |
| `RotationMode` | enum | Excel | L5 |
| `Seed` | int | graph | L1, L3, L4 |

---

## Data vs graph

| lives in Excel | lives in the graph |
|---|---|
| what modules exist | how points are generated |
| which belt each belongs to | how density culls |
| weight, clearance, rotation mode | how lots are subdivided |
| mesh path | how modules are matched |

**Rule of thumb:** if a non-technical person should be able to change it, it goes in the
spreadsheet. That is the argument for the validator tool — it lets someone who cannot open a
PCG graph still change the output, safely, with a build gate that refuses bad data.

---

## Seeding

**One global seed for now.** Per-region seeds are the production-grade answer — each block keeps
its own, so editing one district leaves the rest untouched — but they are noted as future work
rather than built.

The reason to mention it at all: artists will not adopt a system where fixing one street
re-rolls the whole city. Worth saying out loud in a breakdown even if it isn't implemented.

---

## Open decisions

**1. L3 — RESOLVED: frontage-only first.** Settled by naming the art director as the primary
user — a blockout needs massing and fast options, not lot subdivision. Block subdivision is a
stage-2 upgrade, and because every layer speaks points-with-attributes it inserts above L3 later
without touching L0, L1, L2, L4 or L5. Retained below for the reasoning:

| | frontage-only | full block subdivision |
|---|---|---|
| what it does | buildings line the roads, interior stays empty/green | roads bound blocks, blocks split into lots, lots get buildings |
| work | small | the biggest single item in the system |
| reads as | a street, a strip, a village | a city |
| risk | interiors look empty in a wide shot | classic place solo projects stall |

*Frontage-only first is the safe build — it produces a working city on day one and block
subdivision slots in above L3 later without touching any other layer. That is the contract
earning its keep.*

**2. Belt/Zone schema — RESOLVED 2026-09-10, text corrected 2026-09-24.** The two columns mean
different things and both are right as authored (`module_list.xlsx` ▸ Column Guide; counts measured
over the 37 rows):

| column | meaning | values in the sheet | who reads it |
|---|---|---|---|
| `Zone` | which zone a **building** belongs to; `-` for anything that isn't a building | Residential 3 · Industrial 2 · Service 2 · `-` 30 | **PCG** (job 8 zoning, via `Match And Set Attributes`) |
| `Belt` | quality tier — A hero, B support, All | All 29 · A 7 · B 1 | the **validator** only, to catch a hero module used on a support belt |

An earlier proposal here (`Belt` → Residential/Industrial/Agriculture/All, `Zone` deleted) misread
both columns — `A` is a tier, not a mesh name, and `Service` is a deliberate zone — and was
**withdrawn** (checklist 7b). Job 8 was never blocked by it.

**Still open (checklist 7b-new):** the agriculture belt has no `Zone` value. Either add `Agriculture`
as a fourth zone, or drive farm placement from `Category` (*Greenery & Terrain*, 8 modules).
Needed for the Farm preset in job 19; does not block job 8.

**3. Per-instance override / lock — deferred.** See *Who this is for*. Stage 3 (environment
artist) needs generate-then-hand-edit with overrides surviving regeneration. Same underlying
problem as per-region seeding. Out of scope; named deliberately.

**4. Clearance enforcement.** The column exists but nothing reads it. Does L3 enforce spacing,
or does L1 handle it by density alone?

---

## Demo shot list

What the tool demo has to prove, in order. This decides which controls must be solid.

Ordered for the **art director** — the primary user. Lead with option comparison, because that
is the job.

```
0:00  switch preset     same stretch: town -> farm -> industrial      <- the AD story
0:10  drag density      village becomes downtown
0:18  draw a road       district reorganises around it
0:26  surface swap      flat -> cylinder, same downstream graph       <- the thesis
0:34  edit the sheet    validator runs, reimport, regenerate
0:42  final frame
```

Shots 1 and 4 are the thesis, and they are **two independent axes of the same claim**: the
*content* is an input, and the *shape* is an input. Neither is an assumption baked into the graph.

Shot 5 is the one almost nobody shows — the data layer, and the build gate that refuses to
export broken data.

Everything in this contract exists to make those five shots true.

---

## L0's surface: the terrain sheet (design settled 2026-09-11)

Terrain is a **separate single-sided mesh laid on the belt**, not a displacement of the belt.
The belt remains structure; the terrain is what L0 samples. This is the layer contract working
as intended - L0 says "any mesh", so swapping which mesh it samples is a parameter change.

Building it as a separate sheet also removes four problems the belt mesh carries: uneven polygon
density (measured 2.4 - 315 m^2 per face), a packed material UV with 4.3x texel-density spread,
the double-sided shell that made PCG spawn on the outer face, and the need for a second UV map.

### Shape

```
radius      ~954 m from the axis, plus a base offset so it does not z-fight the belt
footprint   7.9 km long x ~1 km across   (the residential belt)
grid        uniform, 5 m spacing  (~630k tris - nothing to Nanite)
UV          clean 0-1, the ground taking the whole image
```

### Relief: calm centre, mountains at the edges

Relief amplitude varies across the belt's **width**, not its length:

```
 1.0 |        /\                              /\
     |       /  \                            /  \
 0.5 |      /    \__________________________/    \
 0.25|_____/                                      \_____
      glass   mountains     centre 25-30%    mountains   glass
```

- **Edges ~200 m, centre ~50-60 m.** The mask scales amplitude. The centre keeps real
  lowland/highland variation, Earth-like rather than a flat plate - **except the city plateaus**.
- **City plateaus (revised 2026-09-14).** Scaling amplitude alone left no level ground for L2
  streets. Painted districts are flattened in Gaea to one constant height (Mask -> Constant ->
  Combine, mask bright = Constant), with blurred mask edges as ramps into the hills. On the belt
  "level" means **constant radius** - one height value - not a flat plane.
- **Mountains at the edges hide the join** between terrain and structure. Flattening there -
  the first instinct - would expose the seam where ground meets window frame.
- **Cap the gradient before the glass line** or peaks intersect the window geometry.

### Water is not authored

A water sheet sits at a **constant radius** (~950 m) - in a rotating habitat "down" is radially
outward, so a water surface is a *curved sheet*, never a flat plane. A flat plane would look
right in the centre and sink into the ground toward the edges.

Rivers, lakes and coastlines then **emerge** wherever terrain falls below that radius. Gaea's
erosion carves the drainage; the water radius floods it. One value controls how wet the habitat
reads.

### The mask does double duty

The same relief mask, sampled per point via `Sample Texture`, drives **L1 density** - sparse on
the mountains, dense on the city plateaus. One authored image, two consumers. This is the concrete
form "artist authoring" takes in L1: the artist paints or generates a mask, the system reads it.

### PCG reads the terrain, never writes it (settled 2026-09-14)

Terrain is shaped only with **native tools**: Gaea for relief, plateaus and masks; Unreal
Modeling Mode for in-editor sculpting. PCG samples the result, checks slope, and adapts - it has
no path back into the terrain.

- **Why not a PCG terrain writer:** PCG 5.7 has no node that writes terrain. Building one means a
  custom Geometry Script Blueprint on the Beta `PCGGeometryScriptInterop` plugin - development
  cost spent re-creating what native tools already do. The product is the city tool.
- **Artist edits flow through automatically:** `Mesh Sampler` tracks its mesh and PCG refreshes
  when a static mesh is saved (engine source; to be confirmed live in the terrain spike).
- **Slope must be measured against the radial "up"**, never a fixed vector - see checklist 7d.10.
- **Upgrade path:** UE 5.8 Mesh Terrain (Experimental) adds non-destructive layers and PCG
  Query/Write nodes; its `Convert Mesh` tool accepts this static mesh, so nothing is thrown away.
