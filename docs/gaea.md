# Gaea — reference for this project

*Created 2026-09-15. Gaea 2.3.0.1 **Community** (free). Every line is sourced: **[measured]** = read from
our own files/screens, **[official]** = QuadSpinner docs or site, **[example]** = QuadSpinner's example
projects installed with Gaea, **[community]** = third-party, **[unverified]** = not yet checked.*

---

## 1. What Gaea does here

Gaea produces **images, not the terrain mesh**. Unreal builds the curved mesh (see
`ue_working_rules.md` → Terrain).

```
Gaea (flat, square)                    Unreal
heightmap EXR  ──────────────────────► Modeling Mode: flat sheet → Bend 60° → Displace
city mask      ──────────────────────► PCG: city allowed + L1 density
(optional) slope / erosion masks ────► PCG rules, materials
```

## 2. Our belt project

| | value | source |
|---|---|---|
| File | `Documents\Gaea\Builds\Belt_Residential.terrain` (move to `SourceArt\Gaea\` to version it) | [measured] |
| Terrain Width / Height | **7,900 m / 250 m** | [measured] |
| Build + Preview resolution | **1024** | [measured] |
| Real scale | 7,900 / 1,024 ≈ **7.7 m/px** | maths |
| Belt position | a **horizontal band across the middle**, 1,000 / 7,900 = **12.66%** of image height (rows ~447–577) | maths |

Why a centred band: the Rect's own UVs cover V 0 → 0.127 on a 7.9 × 1 km sheet
(`RectangleMeshGenerator.cpp:43`), matching the band; a centred band lands in the same place even if
Unreal reads the image upside down.

## 3. Community edition limits

From QuadSpinner's edition comparison table [official]:

| | Community | Indie $99 | Pro $199 | Enterprise $299 |
|---|---|---|---|---|
| Single build resolution | **1024²** | 8192² | 16,384² | 16,384² |
| Tiled builds / Regions | ❌ | tiles ✅ | ✅ | ✅ |
| Automation + batch, Variables | ❌ | ❌ | ✅ | ✅ |
| Unreal Engine integration | ❌ | ✅ | ✅ | ✅ |
| Commercial use | ❌ | ✅ | ✅ | ✅ |

- Gaea 3 is a free upgrade for Gaea 2 purchases [official, Order page].
- **Licence:** Community is non-commercial. What that means for a public portfolio is not checked — the
  EULA link returned 404. **Check before publishing.**
- No Gaea MCP server: every one found needs automation/variables, which Community locks. [official table]

## 4. UI map

| where | what | source |
|---|---|---|
| Right-click node → **Mark for Export**, or **F3** | adds it to Nodes to Export | [official] |
| **Build** tab | Resolution, Build Destination, Nodes to Export (format per node) | [measured] |
| **More settings…** → Build Settings and Regions | pages: Resolution · Build · Tiles · Nodes · Script · **Terrain** · Regions · Profiles | [measured] |
| Terrain page | **Width** (terrains are square) + vertical **Height**; shows Real scale | [measured] |
| Build page | destination tokens, ColorSpace "applies to 16-bit and 8-bit RGB outputs only" | [measured] |
| Execute Build / Copy Command Line | bottom of the window | [measured] |
| Terrain tab (side panel) | node list, not terrain size | [measured] |
| Badge next to the project name | preview resolution (1K / 2K) | [measured] |
| Viewport toolbar → **2D Viewport Toggle** | "Shows/Hides 2D viewport" — flat view of the selected node | [official] |
| Viewport toolbar → **Viewport Elements** | **Grid**, **Bounds**, **Navigation Compass** ("directional guidance") | [official] |
| Viewport toolbar → **Render Style** | Realistic · Clay · **Visualize Data** ("view the raw data with render off") | [official] |
| Viewport Tools → **Height Picker** (2D viewport) | under the cursor: Metric Height, Percentage, **Raw Value (0–1)** | [official] |
| Viewport Tools → **Measurement Tool** (2D viewport) | click two points → XYZ coordinates, Distance 2D / 3D | [official] |

## 5. Export

**Measured** from a real build (`Canyon` node, File → New project):

- EXR, one channel `Y`, **32-bit float**, no compression, **1024 × 1024**, `INCREASING_Y`.
- Height port `Out` = 0.000–0.249 with Terrain Height 2,500 m; mask port `Depth` = 0–1.
- Heights are a **0–1 fraction**. *metres = value × Terrain Height* is the working assumption
  [unverified — confirm: change Height, rebuild, values should not change].
- Unreal's Displace reads float/16-bit textures at full precision (`Texture2DUtil.cpp:184-232`).

**Export node formats** [official]: Gaea Raw · Half Raw (16-bit) · Ushort Raw (16-bit) · Float Raw
(32-bit) · JPEG · PNG 8/16/64 · TIFF 8/16/32 · EXR. Location: Build Folder / Custom / Explicit.

## 6. Nodes we use

Descriptions quoted or summarised from docs.gaea.app/reference [official]; wiring from QuadSpinner's
example projects in `C:\Program Files\QuadSpinner\Gaea 2\Examples\` [example].

| node | what it does [official] | how QuadSpinner wires it [example] |
|---|---|---|
| **MountainRange** | "sets up an entire mountain terrain with shapes highly optimized for eroding large-scale landscapes". Scale, Height (max elevation), Style (Basic/Eroded/Stratified/Alpine), Bulk, Seed | — |
| **LinearGradient** | "Generates a straight linear gradient across the terrain." Scale, Direction, Edge Behavior (Clip/Repeat/Mirror) | → `Combine.Input2` (3D Mountain Map); → `Stratify` with `Direction 270` (Mineral Map); `Direction 129, Edge Clip` → `Snow.SnowMap` (Glacier Complex) |
| **RadialGradient** | radial counterpart | → `Curve` → `Sandstone` (Devils Tower) |
| **Curve** | "remap or adjust values… custom response profiles or non-linear adjustments". Mode Absolute / Relative; **Fit Curve** fits the curve to the input range | takes a gradient in and reshapes it (Devils Tower) |
| **Combine** | two inputs + Mask port. Modes incl. **Blend**, **Multiply** ("multiplying source and base"), **Max** ("keeps the brighter value"), Add, Screen, Subtract. Clamps to 0..1 by default. **Mask port: brighter parts → first input, darker → second input** | Multiply, Max, Add, Screen, Subtract all used; `Combine → Erosion2` is the standard chain (Side Carved Mountains, 3D Mountain Map) |
| **Mask** | "Mask draws a mask." Input = drawing guide only. Masking as a post-process is "extremely fast" vs masking a node directly | `Draw.Out → Mask.Mask`, `Craggy.Out → Mask.In` (Crater - Rocky Crust) |
| **Draw** | "draws entire mountain ranges in the shape you choose" (Open Painter); Soften, Height | used as the mask source above |
| **Constant** | "a blank terrain of the height specified, or a flat color output"; used as a mask or secondary input | `Constant → Transform → Combine Multiply` (3D Mountain Map) |
| **Erosion2** | advanced hydraulic erosion; Duration, Downcutting, Erosion Scale, sediment discharge, Shape | often chained 2–3× (Side Carved Mountains) |
| **Export** | exports terrain, masks or textures to files | — |
| **Shape** | Geometry Circle/Rectangle, Uniform, Scale, **Thickness**, Height, X, Y — makes a **hollow frame**, not a filled band | [measured] — not useful as a band guide |

## 7. Recipes

### Band profile — mountains at the belt edges, calm centre (planned)

Design target (`layer_contract.md`): amplitude ~100% at both belt edges, ~25–30% in the centre.

```
LinearGradient (runs across the band)
  → Curve   [high at band edges ≈0.437 and ≈0.563, ~0.27 at 0.5]
  → Combine.Input2 ── Mode Multiply ── Combine.Input1 ← MountainRange
  → Erosion2
```

- Every node and the Multiply mode are official; `Gradient → Curve` and `Combine → Erosion2` are wirings
  QuadSpinner's own examples use.
- **[unverified]** which `Direction` value makes the gradient run top-to-bottom, and whether the Curve
  spline accepts a high–low–high shape. Check both in the 2D preview before tuning.
- Symmetric around 0.5, so gradient orientation (top→bottom or bottom→top) does not matter.

**LinearGradient measured 2026-09-15** (export `LinearGradient_Out.exr`, Scale 0.25684685, Direction 90,
Edge Mirror, 1024²) [measured]:
- **Direction 90 → values change left→right (columns)**, constant top→bottom (row std 0.00000).
- **Ramp length (0→1) = Scale × image width**: 0.2568 × 1024 = 263.0 px; measured half-period 263–264 px.
- **Centred:** value **0.500 at the image centre** (px 512) — the centre is mid-ramp, not a peak or trough.
- **Mirror = triangle wave:** peaks px 117 / 644, troughs px 380 / 907; linear between.
- So for the belt: **Scale = band fraction = 1,000 / 7,900 = 0.1266** gives one 0→1 ramp exactly across the
  band (centre ± 64.8 px). A **Curve** remap 0 → 1, 0.5 → ~0.27, 1 → 1 then gives high edges / calm centre.

**Gradient → Curve measured 2026-09-15** (`002/Curve_Out.exr`; LinearGradient Scale 0.12144831, Direction
default, Edge default; Curve spline (0,1) (0.5052,0) (1,1)) [measured]:
- **Default Direction (not stored in the file = 0) → values change top→bottom (rows).** Use this for the band.
- **Default Edge Behavior is Mirror** (the UI showed Mirror while the file stored no `Edge` key).
- **Curve accepts a high–low–high spline.** Lowest at row **511 (0.0000)**, highest at rows **450 (0.9956)**
  and **574 (0.9957)** — i.e. centre ± 62 px = 0.1214 × 1024 / 2, confirming ramp = Scale × width.
- The spline is **smooth, not linear**: row 480 = 0.32, row 545 = 0.35.
- Outside the band the pattern repeats (Mirror) — ignored by the belt UVs.
- To land the highs on the band edges (rows ~447 / ~577) use **Scale 0.1266**; for a calm-not-flat centre
  set the middle point **Y ≈ 0.27** (design: 25–30% amplitude).
- **Curve axes (measured):** **X = input value** (the gradient: 0 = one band edge, 0.5 = centre, 1 = other
  edge), **Y = output** (1 = full strength, 0 = none). The point at X 0.5 / Y 0 produced 0.000 at the centre row.

**MountainRange × profile measured 2026-09-15** (`003/Combine_Out.exr`; Combine Mode Multiply, **Ratio not
stored = default**; MountainRange defaults, Seed 11596) [measured]:
- Edge rows (447–459, 565–577) mean 0.0551; centre rows (500–523) mean 0.0279 → **centre/edge = 0.506**,
  even though the curve centre is 0.000. So the default Combine is **not** a full multiply.
- *Inference, unverified:* default **Ratio = 0.5** blending input and result (predicts exactly 0.5). QuadSpinner's
  examples store `Ratio: 1.0` explicitly on their Combines. **Set Ratio 1.0** and re-measure.
- **Overall height is low:** max 0.1185 × 250 m ≈ **30 m** at the band edges vs the ~200 m design. MountainRange
  output needs raising (its `Height` property sets maximum elevation [official]) — measure MountainRange alone.

**Ratio 1.0 re-measured 2026-09-15** (`004/`; Combine Multiply Ratio 1.0, Curve middle point (0.5151, 0.1304))
[measured]:
- **Combine = MountainRange × profile exactly** with Ratio 1: effective profile at the centre row 511 = **0.1307**,
  matching the curve point Y 0.1304; edges 0.996. The earlier 0.506 was the default Ratio.
- **MountainRange (defaults, Seed 11596) is only ~30 m tall:** max 0.1219 × 250 m, mean 13 m — about 1/7 of the
  ~200 m edge design.

**Autolevel added, measured 2026-09-15** (`005/`; MountainRange → Autolevel → Combine Multiply Ratio 1; Curve
middle (0.5085, 0.2754); Edge default Mirror; Height 250 m) [measured]:
- **Heights now right:** max **241 m** at the band edge (row 450), centre row 511 max 60 m / mean 21 m;
  **centre/edge = 0.256** (design 25–30%).
- **Sharp crease at each ridge:** row-mean slope flips from +1.58 to −1.79 m/row within ~2 rows (7.7 m/row) —
  the V corner of the profile. This is the visible "extruded line".
- **7 ridges across the square** (rows 78, 203, 325, 450, 574, 698, 821) because Mirror repeats the profile —
  only 450 and 574 are the belt. This is the "multiple belts" look.
- Fix candidates [official node docs]: Edge Behavior **Clip** ("terminates the gradient at edges"; QuadSpinner's
  Glacier example uses Clip); **Blur** ("diffuses sharp shapes… gentler transitions before… blending") on the
  profile; **Warp** ("more organic shapes"); **Erosion2** after Combine (QuadSpinner's standard chain).

**Clip + Blur + Erosion2, measured 2026-09-15** (`006/Erosion2_*.exr`; Edge Clip, Blur defaults between Curve
and Combine, Erosion2 defaults after Combine) [measured]:
- ✅ **One belt:** the mirrored repeats are gone; outside the band the row means vary smoothly (std ~23 m).
- ✅ **Crease gone:** the slope no longer flips at rows 450 / 574 (−0.47 → −0.57 and +0.37 → +0.41 m/row).
- ⚠️ **Height difference shrank:** centre/edge **0.691** (was 0.256). Centre row 511 mean 46 m / max 122 m;
  band-edge rows mean ~66 m / max ~180 m. Tallest row means now sit **outside** the band (row 380: 97 m,
  row 640: 84 m) — with Clip the full-height mountains continue past the band edges, and the blurred profile no
  longer reaches 1.0 at the edge rows.
- Blur vs Erosion2 contribution **not separated yet** — needs Blur, Combine and Erosion2 exported in one build.
- Erosion masks exported by Erosion2: `Flow` 0–0.742, `Wear` 0–0.266, `Deposits` 0–0.034 (candidates for PCG).

**Stage-by-stage, measured 2026-09-15** (`007/`: Blur_Out, Combine_Out, Erosion2_Out; same settings) [measured]:
- **Blur (default Radius) is the cause.** Profile centre 0.275 → **0.561**; band edges 1.0 → **0.78–0.80**; the
  valley widened from rows 450–574 to rows **406–618** (reaches 0.95). Profile centre/edge **0.714**.
- **Erosion2 (defaults) barely changes it:** centre/edge Combine 0.642 → Erosion2 0.691; centre +2.8 m
  (43.0 → 45.8 m), edges −0.9 m, image max 242 → 235 m.

**Blur Radius 0.03, measured 2026-09-15** (`008/`; Blur default Radius was **0.10**) [measured]:
- Profile centre **0.321**, band edges **0.91–0.93**, reaches 0.95 at rows **444 / 580** (unblurred 450 / 574).
- Centre/edge: profile **0.352**, eroded terrain **0.453** (Radius 0.10 gave 0.714 / 0.691).
- **Seam stays soft:** no slope flip at rows 450 / 574 in the profile or the terrain.
- Terrain: centre rows mean 34 m, edge rows mean 76 m, image max 235 m.
- Blur is linear, so lowering the Curve middle point lowers the blurred centre by roughly the same amount
  *(inference)* — Y ≈ 0.20 should bring the profile centre/edge to ~0.27.

**Curve centre 0.213 + Height 400 m, measured 2026-09-15** (`009/`; user also changed Terrain Height 250 → **400 m**
and MountainRange Seed 11596 → **44175**) [measured]:
- **Profile centre/edge 0.290** (centre 0.262, edges 0.925 / 0.928) — inside the 25–30% design. ✅
- **Seam still soft:** no slope flip at rows 450 / 574.
- Terrain (× 400 m): centre rows mean **34 m**, band-edge rows mean **76 m**, tallest **384 m**; terrain
  centre/edge 0.445 (mountain variation + erosion on top of the 0.29 profile).
- 7d.5 relief shape is done; plateaus (5b) next.

**Direction 90, measured 2026-09-15** (`010/Erosion2_Out.exr`) [measured]:
- ✅ **The belt band now runs top→bottom:** valley across columns — lowest **column 509**, column-profile
  centre/edge **0.424**; rows show no valley (1.07). Matches the bend-then-stretch mesh plan (belt along V).
- Heights (× 400 m): centre column ~39 m; band-edge columns 78 m (447) and 110 m (577) — the right edge is taller
  (mountain variation); image max 385 m.
- **Band in pixels now:** columns ~447–577 (belt width) × all rows (belt length). A district at *a–b* km along
  the belt spans rows a/7.9 × 1024 to b/7.9 × 1024 (which end is 0 km is checked at the Unreal import).

**Slope of the natural valley, measured 2026-09-15** (`010/Erosion2_Out.exr`, heights × 400 m — assumption; pixel
7.715 m) [measured]:

| area | median | under 5° | under 10° | height range |
|---|---|---|---|---|
| calm centre strip (cols 480–545) | 3.7° | 63% | 85% | — |
| city zone 1.2–3.4 km (rows 156–441) | 3.4° | 69% | 94% | 21–106 m |
| town zone 4.2–5.4 km (rows 544–700) | 5.3° | 48% | 76% | 45–111 m |
| village zone 6.8–7.4 km (rows 881–959) | 2.6° | 95% | 100% | 16–38 m |
| mountain edges | 9.9° | 26% | 51% | — |

→ **Decision 2026-09-15: nodes only — no hand painting anywhere in the Gaea graph** (user). **No painted plateaus.** PCG follows the terrain; slope rules keep streets and
buildings off steep ground; district positions come from zoning along the belt (checklist job 8). Painting in
Gaea was also blind: the Draw painter shows only a white square (the Mask node shows the terrain as a guide
when its Input is connected [official]).

**Warp + Rivers, measured 2026-09-15** [measured]:
- **Warp default Strength 0.5 is too strong** (`011/`): valley centre wandered cols 400–581 (±48 px ≈ ±370 m);
  343 / 1024 rows left the calm strip, some left the belt.
- **Warp Strength 0.125** (`012/Warp_Out.exr`): centre cols **497–534**, ±7.8 px (**±60 m**), worst 22 px (170 m);
  **0 rows** outside the calm strip. Profile centre 0.259, edges 0.90 / 0.86. ✅ Gentle meander.
- **Rivers at defaults does not carve along the belt** (`012/Rivers_Out − Combine_Out`, × 400 m): image min −28.5 m,
  1st pct −7.0 m, but on river pixels the change is **+3.9 m mean** (inside the band **+8.2 m**) — the channel
  ends up higher, not cut. `Rivers_Depth` max 0.0010 (≈ 0.4 m).
- River path inside the band: present in 964 / 1024 rows, cols 447–531, median width **3 px (~23 m)**; longest
  continuous run rows 42–714 (**5.2 km**).
- Next: raise **Depth** and **Downcutting** [official: Downcutting "controls how deeply rivers erode"] and re-measure.

**Rivers depth tuning, measured 2026-09-15** (`013/`–`015/`; river bed minus the mean of its banks 4–10 px either
side, inside the belt band) [measured]:
- **Depth** only raises the `Rivers_Depth` output (0.97 → 1.36 m); the bed stayed −1.8 m. **Downcutting** is what
  cuts: default → 0.70 took the bed −0.8 → −1.8 m.
- Not a height-floor problem: under the river the ground was 7.1 m minimum / 19.9 m median before Rivers.
  Rivers **raised** river ground +4.4 m median and lifted the image minimum 0 → 4.9 m *(looks like sink-filling —
  inference)*.
- **Downcutting 1.0 + River Valley Width +2** (`015/`): bed **−4.3 m median** (25th pct −11.6 m) after Rivers, but
  only **−1.1 m** after **Erosion2** — erosion refills the channel. Official Rivers doc: apply early for erosion to
  shape channels, **or later for direct waterway addition** → try Rivers **after** Erosion2.
- `015/` Warp was Strength 0.498 / Size 0.606 (not 0.125): valley wander estimate ±71 px, 704 rows outside the
  calm strip — reset to Strength 0.125.
- River path in the band: 911 / 1024 rows, cols 447–573, median width 4 px (~31 m).
- Final heightmap `015/Erosion2_Out`: 10.8–384.8 m, belt band median 66 m.

**Rivers after Erosion2 + Warp Size tests, measured 2026-09-15** [measured]:
- ✅ **Order fix works:** `Combine → Erosion2 → Rivers` (`017/`): final river bed **−5.1 m median** below its banks
  (25th pct −8.6 m) — passes the ≥ 4 m rule. River present in 825 / 1024 rows of the band.
- **Warp Size shrinks bend amplitude too**, not just spacing: Strength 0.125 + Size 0.125 (`016/`) → ±15 m wander
  (vs ±60 m at default Size); Strength 0.18 + Size 0.125 (`017/`) → ±21 m, max 69 m, 0 rows outside the calm strip.
  Straighter, not wavier.
- Warp Strength → wander at default Size: 0.125 → ±60 m; 0.5 → ±370 m (4× strength ≈ 6× wander).
- Final heightmap candidate `017/Rivers_Out.exr`: 10.9–384.7 m.

**Typing exact values** [official, Gaea 2 guide: `gaea2docs-guide` → property-editor]: **right-click a numeric
property → type a number** (metres like `500m` are converted to the property's units). The Nudge panel also
has Halve / Double / Increase-Decrease Small / Min / Max / Reset.
**Curve points:** no documented numeric entry for spline points — drag by eye, then measure the export.
- Hand-painted alternative: a **Mask** node painted by hand into the Combine Mask port — less precise.

### City plateaus (7d.5b)

**Constant** (Height mode, plateau height) → **Combine** Input 1 = Constant, Input 2 = terrain,
**Mask** = painted city mask (bright = Input 1) [official Combine mask rule]. Soft (grey) mask edges give
ramps [official]. Avoid `Max` for this: it keeps the higher value, so hills above the plateau survive
[official: "keeps the brighter value"]. Export the city mask as its own image.

## 7b. Final graph — belt relief (build 018, 2026-09-15)

```
MountainRange (Seed 44175) → Autolevel ─────────────────────┐
                                                             Combine (Multiply, Ratio 1.0) → Erosion2 (defaults) → Rivers → EXPORT
LinearGradient (Scale 0.1214, Direction 90, Edge Clip)       │
  → Curve (0,1) (0.509,0.213) (1,1) → Blur (Radius 0.03) → Warp (Strength 0.18, Size default) ┘
Rivers: Downcutting 1.0 · Depth 0.704 · River Valley Width +2 · Seed 24858 · Headwaters empty
Terrain: Width 7,900 m · Height 400 m · 1K
```

| check | measured (018) | target |
|---|---|---|
| valley profile centre/edge | 0.29 (build 009 settings, unchanged since) | 25–30% |
| seam at band edges | no slope flip | soft |
| valley wander | ±91 m, max 247 m, **0 rows** outside the calm strip | ~±100 m, inside the belt |
| river bed below banks | **−5.3 m** median (25th pct −12.2 m), in 945 / 1024 rows | ≥ 4 m |
| heights | 10.8–384.7 m | edges ≫ centre |

Deliverables: `Rivers_Out.exr` = heightmap · `Rivers_Rivers.exr` = river mask (copied to `SourceArt/Gaea/`).

## 7c. Mask set (7d.11) - first build at defaults (build `belt/001` = `Belt_Residential/019`, 2026-09-16)

`Rivers → Out` feeding **Slope**, **Soil**, **Height** in parallel, all default properties. Measured against
`Rivers_Out.exr` (heights x 400 m, pixel 7.715 m) [measured].

**Terrain reference:** slope median **6.6 deg**, p90 **21.4**, p99 44.0, max 78.4. Belt band (cols 447-577):
median 6.9, p90 17.7.

**Slope at defaults = 98% white** (mean 0.980, median 1.000) — unusable here. Transfer function:

| terrain slope | 0-25 | 25-30 | 30-35 | 35-40 | 40-50 | 50+ |
|---|---|---|---|---|---|---|
| mean `Slope_Out` | 1.000 | 0.997 | 0.873 | 0.560 | 0.153 | 0.001 |

White to ~28 deg, **half at ~38.5**, black past 50. The whole belt sits inside the white plateau, so the
range has to come down into 0-25 deg. UI units for `Range` / `Falloff` still unread (examples store
`Range.Y 1.42`, `Falloff 40.6`, which cannot both be degrees).

**Height at defaults is redundant — a pure function of elevation** (white <=180 m, 0.709 at 200-240,
0.172 at 240-280, black above 280). It holds nothing the heightmap does not. Do the band with a
`smoothstep` in `M_Terrain` and drop the node. *(checklist 7d.11 updated 2026-09-16 to drop height.)*

**Soil at defaults is real but nearly flat:** mean 0.678, std 0.053; 90% of pixels inside 0.591-0.746
(belt band 0.284-0.867). Correlates -0.32 with slope, -0.46 with height — dirt settles low and gentle,
which is right. Needs a contrast stretch: **Soil → Autolevel** (the fix already proven on MountainRange).

**Flow needs no new node:** `Erosion2_Flow.exr` = 0-0.504, mean 0.0016, 0.7% of pixels above 0.05 — a
sparse, sharp stream network.

## 7d. Orientation — the band must run across ROWS, not columns (2026-09-16)

**`LinearGradient Direction 90` was the wrong call.** It puts the valley across image **columns**
(build 010). Unreal's Displace samples the sheet so that the arc direction selects image **rows**, so the
band has to be across rows — i.e. `LinearGradient` **Direction 0** (the default).

Interim fix used for the first mesh: the EXR was **transposed offline** into
`SourceArt/Gaea/Belt_Residential_Height_T.exr` (single `Y` channel, 32-bit float, uncompressed, 1024^2 —
byte-identical header to Gaea's own output apart from `screenWindowWidth`). **Set Direction 0 and rebuild
when the mask set is built**, then no transpose is needed.

**Builds are reproducible.** `belt/001` and `Belt_Residential/019` are byte-identical (same MD5 on
`Rivers_Out` and `Rivers_Rivers`) from the same saved graph. Build **018 differs** (0.89% of pixels equal,
max 20.3 m) because the graph changed between that build and the save two minutes later — not
non-determinism. So a forgotten mask **can** be re-exported later and will still match.

## 8. Traps

| trap | source |
|---|---|
| Example projects can carry **2K** Build/Preview resolution → *"Validation failed: build resolution is higher than allowed by your edition"*. Start from File → New. | [measured] |
| Two docs sites: **docs.quadspinner.com = Gaea 1** (`.tor`, `Gaea.Build.exe`), **docs.gaea.app = Gaea 2**. Don't mix. | [official] |
| docs.gaea.app renders client-side; some URLs 404 to scripts — open in a browser. The GitHub `Gaea2Docs-Reference` pages are mostly empty placeholders. | [measured] |
| "Terrain" tab in the side panel is the node list; terrain size lives in More settings… → Terrain. | [measured] |
| **Save As under a new name restarts the build counter and changes the output folder** (`Belt_Residential/018` then `belt/001`). | [measured] |
| Saving over a test file in `Builds` (e.g. `Canyon River with Sea.terrain`) — the originals live safely in the install `Examples` folder. | [measured] |

## 9. Resources

**Official**
- Docs (Gaea 2): https://docs.gaea.app/ — Node Reference: https://docs.gaea.app/reference · Videos: https://docs.gaea.app/videos/index.html
- YouTube: https://www.youtube.com/quadspinner (node explainers, deep dives, short tips — the docs page says it can lag behind the channel)
- Editions / order: https://quadspinner.com/Order/#Editions
- GitHub: [Gaea2-Docs](https://github.com/QuadSpinner/Gaea2-Docs) · [gaea2docs-guide](https://github.com/QuadSpinner/gaea2docs-guide) · [Gaea2Docs-Reference](https://github.com/QuadSpinner/Gaea2Docs-Reference) · [Gaea.Automation](https://github.com/QuadSpinner/Gaea.Automation) (Gaea 1 `.tor`) · [Gaea2Unreal](https://github.com/QuadSpinner/Gaea2Unreal) (needs Indie+)
- **Local examples** (real node settings, readable as JSON): `C:\Program Files\QuadSpinner\Gaea 2\Examples\`

**Community**
- Motion Forge CG — *Gaea 2 - Mask by Height and with the Draw Node* (June 2025): https://www.youtube.com/watch?v=iuHNm2peAzg
- Motion Forge Pictures — *Gaea 2 to Unreal Engine: 2 ways to import heightmaps* (Chris J Mitchell, 25 Sep 2025; Landscape-based, so only the export half applies here): https://www.motionforgepictures.com/gaea-2-to-unreal-engine-2-ways-to-import-heightmaps-into-unreal-engine/
- *Not read yet:* FAForever wiki Gaea masks (403), Yusri Ghouse ArtStation beginner blog.
