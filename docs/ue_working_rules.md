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
