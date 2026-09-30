# PCG Nodes — UE 5.7.4 reference

*Built 2026-09-16 from the engine source of the installed UE 5.7.4 (`Engine/Plugins/PCG`, `PCGInterops`, `Experimental/PCGInterops`, `Experimental/PCGBiomeCore`) plus Epic's online node reference (5.8 edition). Every node below is in this project's palette — all PCG plugins are enabled in `Space_Colony.uproject`.*

**Search this file by the name you see in the graph editor** — titles and palette aliases are both listed.

| tag | meaning |
|---|---|
| **[src]** | text taken from the engine source — authoritative for 5.7.4 |
| **[epic]** | text from Epic's node reference page (5.8 edition — may describe newer behaviour) |
| **[class]** | no node tooltip in source; this is the C++ class comment |
| ⚠ | deprecated — do not use in new graphs |
| β / 🧪 | node lives in a **Beta** / **Experimental** plugin |
| ◆ | setting is overridable — it gets a pin and can be driven by a graph parameter |
| ★ | used or planned in this project (details in section 8) |
| ↳ | a field inside the struct setting on the row above |
| *Only when* | the setting is greyed out / hidden unless this condition holds (`EditCondition` [src]) |

**Counts:** 214 placeable node classes · 1157 settings · 4 deprecated · ~158 extra palette entries from aliases · 114 PCGBiomeCore assets.

## Contents

1. [Plugins and maturity](#1-plugins-and-maturity)
2. [Index — every node on one line](#2-index--every-node-on-one-line)
3. [Nodes by category](#3-nodes-by-category)
4. [Palette aliases — one class, many search names](#4-palette-aliases--one-class-many-search-names)
5. [Deprecated and replaced](#5-deprecated-and-replaced)
6. [Name mismatches with Epic's docs](#6-name-mismatches-with-epics-docs)
7. [PCGBiomeCore — graph assets, not nodes](#7-pcgbiomecore--graph-assets-not-nodes)
8. [Project notes — nodes this project uses](#8-project-notes--nodes-this-project-uses)
9. [Coverage and gaps](#9-coverage-and-gaps)
10. [Sources and how this was built](#10-sources-and-how-this-was-built)

---

## 1. Plugins and maturity

From each plugin's `.uplugin` [src]. All are **enabled** in this project.

| plugin | maturity | nodes | what it adds |
|---|---|---|---|
| `PCG` | production | 196 | the framework and all core nodes |
| `PCGGeometryScriptInterop` | β Beta | 12 | Mesh Sampler, Get Dynamic Mesh Data, Primitive Cross-Section and the 9 Dynamic Mesh nodes |
| `PCGPythonInterop` | β Beta | 1 | Execute Python Script |
| `PCGExternalDataInterop` | β Beta | 1 | Load Alembic |
| `PCGFastGeoInterop` | 🧪 Experimental | 0 | no nodes — a backend: *"enables runtime spawning of primitives using FastGeo components"* [src .uplugin] |
| `PCGInstancedActorsInterop` | 🧪 Experimental | 1 | Spawn Instanced Actors |
| `PCGNaniteAssembliesInterop` | 🧪 Experimental | 1 | Nanite Assembly Static Mesh Builder |
| `PCGNiagaraInterop` | 🧪 Experimental | 1 | Write To Niagara Data Channel |
| `PCGWaterInterop` | 🧪 Experimental | 1 | Get Water Spline Data |
| `PCGBiomeCore` | 🧪 Experimental | 0 | graph assets + Blueprints, no C++ nodes — see section 7 |

Epic's rule for Beta/Experimental: use with caution when shipping. **Mesh Sampler is Beta** — this project's whole L0 layer sits on it.

---

## 2. Index — every node on one line

Sorted by category, then name. The description is the first sentence of the best available text.

### Sampler — 8

| node | what it does | flags |
|---|---|---|
| [Copy Points](#copy-points) | For each point pair from the source and the target, create a copy, inheriting properties & attributes depending on the node settings. | ★ |
| [Mesh Sampler](#mesh-sampler) | Sample points on a static mesh. | ★ β |
| [Sample Texture](#sample-texture) | Samples color of texture at each point. | ★ |
| [Scene Capture](#scene-capture) | Perform a 2D orthographic scene capture and write the result to a render target data. |  |
| [Select Points](#select-points) | Selects a stable random subset of the input points. |  |
| [Spline Sampler](#spline-sampler) | Generates points along the given Spline, and within the Bounding Shape if provided. | ★ |
| [Surface Sampler](#surface-sampler) | Generates points in two dimensional domain that sample the Surface input and lie within the Bounding Shape input. |  |
| [Volume Sampler](#volume-sampler) | Generates points in the three dimensional bounds of the Volume input and within the Bounding Shape input if provided. |  |

### Spatial — 56

| node | what it does | flags |
|---|---|---|
| [Attribute Set To Point](#attribute-set-to-point) | Converts attribute sets to point data |  |
| [Bad Outputs](#bad-outputs) | Test node to write bad outputs | hidden |
| [Bounds From Mesh](#bounds-from-mesh) | Sets the bounds according to the static or skeletal mesh(es) provided in the mesh pin. |  |
| [Clean Spline](#clean-spline) | Remove superfluous control points along the spline, such as those that are co-located or collinear. |  |
| [Clip Paths](#clip-paths) | Clips paths against the polygons, to have the paths either inscribed in the polygons (intersection) or outside the polygons (difference). |  |
| [Create Collision Data](#create-collision-data) | Creates a volumetric representation of the points as if they had their selected mesh collision. |  |
| [Create Points](#create-points) | Creates point data from a provided list of points. |  |
| [Create Points Grid](#create-points-grid) | Creates a 2D or 3D grid of points. |  |
| [Create Points Sphere](#create-points-sphere) | Generate points on the surface of a sphere. |  |
| [Create Polygon 2D](#create-polygon-2d) | Creates a (closed) 2d polygon per input. | ★ |
| [Create Spline](#create-spline) | Creates PCG spline data from the input PCG point data, in a sequential order. |  |
| [Create Surface From Polygon2D](#create-surface-from-polygon2d) | Creates a surface data from a Polygon 2D data. |  |
| [Create Surface From Spline](#create-surface-from-spline) | Create an implicit surface for each given spline. |  |
| [Cull Points Outside Actor Bounds](#cull-points-outside-actor-bounds) | Culls points that lie outside the current actor bounds. |  |
| [Difference](#difference) | Spatially subtracts the target difference data from the source data, outputing the difference of the two. |  |
| [Distance](#distance) | Calculates and appends a signed 'Distance' attribute to the source data. |  |
| [Duplicate Cross-Sections](#duplicate-cross-sections) |  |  |
| [Elevation Isolines](#elevation-isolines) | Compute the elevation isolines of a surface, can output either points or splines. |  |
| [Find Convex Hull 2D](#find-convex-hull-2d) | Return the 2D convex hull of a set of points on the XY plane. |  |
| [Get Actor Data](#get-actor-data) | Builds a collection of PCG-compatible data from the selected actors. | ★ |
| [Get Bounds](#get-bounds) | Computes the bounds of the inputs as attributes. |  |
| [Get Dynamic Mesh Data](#get-dynamic-mesh-data) | Builds a collection of PCG-compatible data from the selected actors. | β |
| [Get Landscape Data](#get-landscape-data) | Builds a collection of landscapes from the selected actors. |  |
| [Get PCG Component Data](#get-pcg-component-data) | Builds a collection of data from other PCG components on the selected actors. |  |
| [Get Primitive Data](#get-primitive-data) | Builds a collection of primitive data from primitive components on the selected actors. |  |
| [Get Segment](#get-segment) | Gets a specific segment from the input. |  |
| [Get Spline Control Points](#get-spline-control-points) | Extracts the control points from the spline(s) as point data. |  |
| [Get Spline Data](#get-spline-data) | Builds a collection of splines from the selected actors. |  |
| [Get Texture Data](#get-texture-data) | Generates points by sampling the given texture. |  |
| [Get Virtual Texture Data](#get-virtual-texture-data) | Builds a collection of virtual texture data from the selected actors. |  |
| [Get Volume Data](#get-volume-data) | Builds a collection of volumes from the selected actors. |  |
| [Get Water Spline Data](#get-water-spline-data) | Builds a collection of data from WaterSplineComponents on the selected actors. | 🧪 |
| [Inner Intersection](#inner-intersection) | Spatial data will be generated as the result of intersecting with the other source inputs sequentially or no output if such an intersection does not exist. |  |
| [Intersection](#intersection) | For each given source input on the primary pin, spatial data will be generated as the result of sequentially intersecting with the other source inputs (implicitly unioned |  |
| [Make Concrete](#make-concrete) | Concrete data is passed through (e.g. |  |
| [Merge Points](#merge-points) | Merges multiple data sources into a single data output. |  |
| [Mutate Seed](#mutate-seed) | Applies a new random seed from point input. |  |
| [Normal To Density](#normal-to-density) | Finds the angle against the specified direction and applies that to the density | ★ |
| [Offset Polygon](#offset-polygon) | Offsets polygon to either make it larger or smaller, or open/close holes based on the offset quantity. |  |
| [Point From Mesh](#point-from-mesh) | Creates a single point at the origin with an attribute named MeshPathAttributeName containing a SoftObjectPath to the StaticMesh/SkeletalMesh. |  |
| [Point Neighborhood](#point-neighborhood) | Computes quantities from nearby neighbor points, such as average density, color, and position. |  |
| [Polygon Operation](#polygon-operation) | Performs polygon operations between the inputs. | ★ |
| [Primitive Cross-Section](#primitive-cross-section) | Creates spline cross-sections of one more primitives based on vertex features. | β |
| [Projection](#projection) | Projects each of the inputs connected to In onto the Projection Target and concatenates all of the results to Out. |  |
| [Spatial Noise](#spatial-noise) | Various fractal noises that can be used to filter points |  |
| [Spline Direction](#spline-direction) | Direct the order of a spline's control points. |  |
| [Spline Intersection](#spline-intersection) | Intersects splines against other splines (or themselves) and returns varied results based on user need. |  |
| [Spline to Segment](#spline-to-segment) | Take a spline as input and create a point data, with each point being a segment defined by 2 connected control points. |  |
| [Split Spline](#split-spline) | Splits spline at a specific distance(s), key(s) or at certain values. |  |
| [Subdivide Segment](#subdivide-segment) |  |  |
| [Subdivide Spline](#subdivide-spline) |  |  |
| [To Point](#to-point) | Convert input to point data, performing sampling with default settings if necessary |  |
| [Union](#union) | Combine spatial data into a union of all inputs. |  |
| [World Ray Hit Query](#world-ray-hit-query) | Allows generic access (based on raycasts) to collisions in the world that behaves like a surface. |  |
| [World Raycast](#world-raycast) | Casts a line trace or collision shape sweep from provided points along a given direction returning the location of the impact. |  |
| [World Volumetric Query](#world-volumetric-query) | Allows generic access (based on overlaps) to collisions in the world that behaves like a volume. |  |

### Point Ops — 13

| node | what it does | flags |
|---|---|---|
| [Apply Hierarchy](#apply-hierarchy) | Applies hierarchy transformations based on a hierarchy depth, point index & parent index scheme. |  |
| [Apply Scale To Bounds](#apply-scale-to-bounds) | Applies the scale of each point to its bounds and resets the scale. |  |
| [Attract](#attract) | Attracts source points to target points based on a max distance and a criteria. |  |
| [Blur](#blur) | Select an attribute on a point data and blur it using the values from neighbors within some distance, center to center, and can be done over multiple iterations. |  |
| [Bounds Modifier](#bounds-modifier) | Applies a transformation on the point bounds & optionally its steepness. |  |
| [Cluster](#cluster) | Given a desired number of clusters (categories), find the best fit cluster for each point by distance, using one of various clustering algorithms. |  |
| [Collapse Points](#collapse-points) | Collapses points with their closest neighbors until all points are farther than the search distance. |  |
| [Combine Points](#combine-points) | Combines each point to share a singular bound extent. |  |
| [Duplicate Point](#duplicate-point) | Creates duplicates of each point with optional transform offsets. |  |
| [Extents Modifier](#extents-modifier) | Modifies the extent of each point in the point data by manipulating the bounds. |  |
| [Reset Point Center](#reset-point-center) | Modify the position of a point within its bounds, while keeping its bounds the same. |  |
| [Split Points](#split-points) | Splits each input point into two separate points and sets bounds based on the position and axis of the cut. |  |
| [Transform Points](#transform-points) | Changes the points transforms (either in place or to an attribute with Apply to Attribute) using basic random rules. | ★ |

### Filter — 11

| node | what it does | flags |
|---|---|---|
| [Density Filter](#density-filter) | Filters points based on density and the provided filter ranges. |  |
| [Filter Attribute Elements](#filter-attribute-elements) *(also: Point Filter, Attribute Filter)* | Filter elements by attribute that allows to do "A op B" type filtering, where A is the input spatial data or Attribute set, and B is either a constant, another spatial da |  |
| [Filter Attribute Elements by Range](#filter-attribute-elements-by-range) *(also: Point Filter Range, Attribute Filter Range)* | Attribute filter on range that allows to do "A op B" type filtering, where A is the input spatial data or Attribute set, and B is either a constant, another spatial data | ★ |
| [Filter Data By Attribute](#filter-data-by-attribute) | Separates input data by whether they have the specified attribute or not, or on the data attribute value. |  |
| [Filter Data By Index](#filter-data-by-index) | Filters data in the collection according to user selected indices |  |
| [Filter Data By Tag](#filter-data-by-tag) | Filters data in the collection according to whether they have, or don't have, some tags |  |
| [Filter Data By Type](#filter-data-by-type) | Filters data in the collection according to data type |  |
| [Filter Elements By Index](#filter-elements-by-index) | Filters points or the elements of an attribute set based on a second input of points, attribute sets, or a user-defined index range expression. |  |
| [Random Choice](#random-choice) | Chooses entries randomly through ratio or a fixed number of entries. |  |
| [Remove Empty Data](#remove-empty-data) | Remove all data in the input pin that is empty. |  |
| [Self Pruning](#self-pruning) | Removes intersections between points in the same point data, prioritizing data based on the settings (Large to Small, etc.). |  |

### Metadata (attributes) — 35

| node | what it does | flags |
|---|---|---|
| [Attribute Bitwise Op](#attribute-bitwise-op) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Attribute Boolean Op](#attribute-boolean-op) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Attribute Cast](#attribute-cast) | Cast an attribute to another type. |  |
| [Attribute Compare Op](#attribute-compare-op) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Attribute Maths Op](#attribute-maths-op) | Metadata operation between Points/Spatial/AttributeSet data. | ★ |
| [Attribute Noise](#attribute-noise) *(also: Density Noise)* | Apply some noise to an attribute/property. |  |
| [Attribute Partition](#attribute-partition) | Splites the input data (Point Data or Attribute Set, or other spatial data to be converted to Point Data if required) in a partition according to the attributes selected. |  |
| [Attribute Reduce](#attribute-reduce) | Take all the entries/points from the input and perform a reduce operation on the given attribute/property and output the result into a ParamData. |  |
| [Attribute Remap](#attribute-remap) *(also: Density Remap, Attribute Curve Remap)* | Remap an attribute using either a range or a curve. |  |
| [Attribute Remove Duplicates](#attribute-remove-duplicates) | Remove duplicates for given attributes |  |
| [Attribute Rename](#attribute-rename) | Renames an existing attribute. |  |
| [Attribute Rotator Op](#attribute-rotator-op) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Attribute Select](#attribute-select) | Take all the entries/points from the input and perform a select operation on the given attribute/property on the given axis (if the attribute/property is a vector) and ou |  |
| [Attribute String Op](#attribute-string-op) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Attribute Transform Op](#attribute-transform-op) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Attribute Trig Op](#attribute-trig-op) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Attribute Vector Op](#attribute-vector-op) | Metadata operation between Points/Spatial/AttributeSet data. | ★ |
| [Break Transform Attribute](#break-transform-attribute) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Break Vector Attribute](#break-vector-attribute) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Copy Attributes](#copy-attributes) | Copy from the Input Source to Output Target attribute. | ⚠ |
| [Copy Attributes](#copy-attributes) | Copy from the Input Source to Output Target attribute. |  |
| [Copy Attributes](#copy-attributes) | Copy from the Input Source to Output Target attribute. | ⚠ |
| [Delete Attributes](#delete-attributes) | Removes attributes from a given input metadata. |  |
| [Extract Attribute](#extract-attribute) | Extract an attribute at a given index into a new attribute set. |  |
| [Generate Seed](#generate-seed) | Generate a seed attribute |  |
| [Get Attribute From Point Index](#get-attribute-from-point-index) | Get the attribute/property of a point given its index. |  |
| [Get Element Count](#get-element-count) | Return the number of elements in the input data. |  |
| [Hash Attribute](#hash-attribute) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Make Rotator Attribute](#make-rotator-attribute) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Make Transform Attribute](#make-transform-attribute) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Make Vector Attribute](#make-vector-attribute) | Metadata operation between Points/Spatial/AttributeSet data. |  |
| [Match And Set Attributes](#match-and-set-attributes) | Matches or randomly assigns values from the Attribute Set to the input data. | ★ |
| [Merge Attributes](#merge-attributes) | Merges multiple attribute sets in a single attribute set with multiple entries and all the provided attributes |  |
| [Parse String](#parse-string) | Parse string passed as attribute into a compatible PCG type. |  |
| [Point Match And Set](#point-match-and-set) | For all points, if a match is found (e.g. |  |

### Param (attribute sets) — 9

| node | what it does | flags |
|---|---|---|
| [Add Attribute](#add-attribute) | Add a new attribute to a spatial data or an attribute set. |  |
| [Create Constant](#create-constant) |  |  |
| [Data Tags To Attribute Set](#data-tags-to-attribute-set) | Extracts the tags on the data to an attribute set. |  |
| [Get Actor Property](#get-actor-property) | Extract a property value from an actor/component into a ParamData. |  |
| [Get Attribute List](#get-attribute-list) | Creates an attribute set with one entry per attribute on the input data. |  |
| [Get Attribute Set from Index](#get-attribute-set-from-index) | Retrieves a single entry from an Attribute Set. |  |
| [Get Property From Object Path](#get-property-from-object-path) | Extract property from a list of soft object paths. |  |
| [Get Tags](#get-tags) | Creates an attribute set with one entry per tag |  |
| [Point To Attribute Set](#point-to-attribute-set) | Converts point data to an attribute set with one entry per point and the same attributes. |  |

### Spawner — 6

| node | what it does | flags |
|---|---|---|
| [Create Target Actor](#create-target-actor) | Creates an empty actor from a template that can be used as a target for writing PCG artifacts to, such as the Static Mesh Spawner. |  |
| [Instanced Skinned Mesh Spawner](#instanced-skinned-mesh-spawner) |  |  |
| [Spawn Instanced Actors](#spawn-instanced-actors) | Spawns instanced actors from the input data. | 🧪 |
| [Spawn Spline Component](#spawn-spline-component) | Spawn a spline component from a spline data. |  |
| [Spawn Spline Mesh](#spawn-spline-mesh) | Create a USplineMeshComponent for each segment along a given spline. |  |
| [Static Mesh Spawner](#static-mesh-spawner) | Spawn one static mesh per point in the provided point data. | ★ |

### Control Flow — 6

| node | what it does | flags |
|---|---|---|
| [Branch](#branch) | Control flow node that will route the input to either Output A or Output B, based on the 'Output To B' property - which can also be overridden. |  |
| [Runtime Quality Branch](#runtime-quality-branch) | Control flow node that dynamically routes input data based on 'pcg.Quality' setting. |  |
| [Runtime Quality Select](#runtime-quality-select) | Selects from input pins based on 'pcg.Quality' setting. |  |
| [Select](#select) | Control flow node that will select all input data on either Pin A or Pin B only, based on the 'Use Input B' property - which can also be overridden. |  |
| [Select (Multi)](#select-multi) | Control flow node that will select all input data on a single input pin that matches a given selection mode and corresponding 'selection' property - which can also be ove |  |
| [Switch](#switch) | Control flow node that passes through input data to a specific output pin that matches a given selection mode and corresponding 'selection' property - which can also be o |  |

### Subgraph — 3

| node | what it does | flags |
|---|---|---|
| [Loop](#loop) | Executes the specified Subgraph for each data on the loop pins (or on the first pin if no specific loop pins are provided), keeping the rest constant. |  |
| [Spawn Actor](#spawn-actor) | Spawns either the contents of an actor or an actor per point in the provided input data. |  |
| [Subgraph](#subgraph) | Executes another graph as a subgraph. | ★ |

### Graph Parameters — 2

| node | what it does | flags |
|---|---|---|
| [Get Graph Parameter](#get-graph-parameter) | Getter for user parameters defined in PCGGraph, by the user. | ★ |
| [Get Graph Parameter](#get-graph-parameter) | Generic getter for user parameter defined in the PCG Graph, by the user. |  |

### Input / Output — 10

| node | what it does | flags |
|---|---|---|
| [Data Table Row To Attribute Set](#data-table-row-to-attribute-set) | Extracts a single row from a data table to an Attribute Set. |  |
| [Export Selected Attributes](#export-selected-attributes) | Exports selected attributes directly to a file in a specified format. |  |
| [Get Asset List](#get-asset-list) | Returns the list of asset, with options (class, bp generated class, etc.) from a source - collection or folder. |  |
| [Input Node](#input-node) |  | hidden |
| [Load Alembic](#load-alembic) | Loads data from an Alembic file | β |
| [Load Data Table](#load-data-table) | Loads data from DataTable asset | ★ |
| [Load PCG Data Asset](#load-pcg-data-asset) | Loader/Executor of PCG data assets |  |
| [Nanite Assembly Static Mesh Builder](#nanite-assembly-static-mesh-builder) | [EXPERIMENTAL] Create a Static Mesh using Nanite assemblies from the input point data. | 🧪 |
| [Save PCG Data Asset](#save-pcg-data-asset) | Exports the input data to a PCG Data Asset. |  |
| [Save Texture to Asset](#save-texture-to-asset) | Save the input texture to a UTexture2D asset (format is always BGRA8). |  |

### Generic — 27

| node | what it does | flags |
|---|---|---|
| [Add Component](#add-component) | Adds component(s) to specified target actor(s). |  |
| [Add Tags](#add-tags) | Applies the specified tags on the output data. |  |
| [Apply On Object](#apply-on-object) | Applies property overrides and executes functions on a target object. |  |
| [Compute Graph](#compute-graph) |  |  |
| [Data Attributes To Tags](#data-attributes-to-tags) | Copy data attributes and their values to tags. |  |
| [Data Count](#data-count) | Returns the count of data in the input data collection. |  |
| [Delete Tags](#delete-tags) | Filters the tags on the input data. |  |
| [Execute Python Script](#execute-python-script) | Execute a Python script from an inline or connected input, or directly from a .py file. | β |
| [Gather](#gather) | Gathers multiple data in a single collection. |  |
| [Get Console Variable](#get-console-variable) | Reads the given console variable and writes the value to an attribute set. |  |
| [Get Execution Context Info](#get-execution-context-info) | Returns some context-specific common information. |  |
| [Get Loop Index](#get-loop-index) | Returns the index of the loop this subgraph is executing, if any. |  |
| [Get Subgraph Depth](#get-subgraph-depth) | Returns the call depth of this graph. |  |
| [Get Tool Data](#get-tool-data) | Builds a collection of PCG-compatible data from the selected tools. |  |
| [Graph Authoring Test Helper](#graph-authoring-test-helper) | Testing helper - generates a node with a single input and output pin of the stipulated type. |  |
| [Grid Linkage](#grid-linkage) |  |  |
| [Pathfinding](#pathfinding) | Finds the optimal path across the points of a given point cloud--should one exist--when provided a start and goal location, and a maximum jump distance between points. |  |
| [Proxy](#proxy) | Executes another settings object, which can be overridden. |  |
| [Replace Tags](#replace-tags) | Replaces the tags on the input data. |  |
| [Select Grammar](#select-grammar) | Select a grammar by comparing an input attribute against a provided criteria. |  |
| [Sort Attributes](#sort-attributes) | Sorts data based on an attribute. |  |
| [Sort Data By Tag Value](#sort-data-by-tag-value) | Sorts data by tag value (i.e. |  |
| [Tags to Data Attributes](#tags-to-data-attributes) | Parse tags and create data attributes from it. |  |
| [Trivial](#trivial) | Trivial / Pass-through settings used for input/output nodes |  |
| [Wait](#wait) | Waits some time and/or frames. |  |
| [Wait Until Landscape Is Ready](#wait-until-landscape-is-ready) | Waits until landscape is ready, then passes data downstream. |  |
| [Write To Niagara Data Channel](#write-to-niagara-data-channel) | Allow writing attributes to a Niagara Data Channel. | 🧪 |

### Dynamic Mesh — 9

| node | what it does | flags |
|---|---|---|
| [Append Meshes From Points](#append-meshes-from-points) | Append meshes at the points transforms. | β |
| [Boolean Operation](#boolean-operation) | Boolean operation between dynamic meshes. | β |
| [Create Empty Dynamic Mesh](#create-empty-dynamic-mesh) | Create an empty dynamic mesh data. | β |
| [Dynamic Mesh Transform](#dynamic-mesh-transform) | Apply a transform to all dynamic meshes. | β |
| [Merge Dynamic Meshes](#merge-dynamic-meshes) | Appends all incoming dynamic meshes to the first dynamic mesh in order. | β |
| [Save Dynamic Mesh To Asset](#save-dynamic-mesh-to-asset) | Saves dynamic mesh data into a static mesh asset. | β |
| [Spawn Dynamic Mesh](#spawn-dynamic-mesh) | Spawn a dynamic mesh component for each dynamic mesh data in input. | β |
| [Spline To Mesh](#spline-to-mesh) | Converts a closed spline into a mesh. | β |
| [Static Mesh To Dynamic Mesh Element](#static-mesh-to-dynamic-mesh-element) | Convert a static mesh into a dynamic mesh data. | β |

### GPU — 3

| node | what it does | flags |
|---|---|---|
| [Custom HLSL](#custom-hlsl) | Produces a HLSL compute shader which will be executed on the GPU. |  |
| [Generate Landscape Textures](#generate-landscape-textures) | Generates landscape height texture and grass maps on the GPU. | ⚠ |
| [Generate Landscape Textures](#generate-landscape-textures) *(also: Generate Grass Maps)* | Generates landscape height texture and grass maps on the GPU. |  |

### Debug — 5

| node | what it does | flags |
|---|---|---|
| [Debug](#debug) | Debugs the previous node in the graph but is not transient. |  |
| [Print Grammar](#print-grammar) | Prints the result of an interpreted grammar. |  |
| [Print String](#print-string) | Issues a specified message to the log, and optionally to the graph and/or screen. |  |
| [Sanity Check Point Data](#sanity-check-point-data) | Validates that the input data point(s) have a value in the given range; outside of the range this node logs an error and cancels the generation. |  |
| [Visualize Attribute](#visualize-attribute) | Visualizes a selected attribute on screen at each point's transform. |  |

### Reroute — 4

| node | what it does | flags |
|---|---|---|
| [Named Reroute Base](#named-reroute-base) | Base class for both reroute declaration and usage to share implementation, but also because they use the same visual node representation in the editor. |  |
| [Named Reroute Declaration](#named-reroute-declaration) |  |  |
| [Named Reroute Usage](#named-reroute-usage) |  |  |
| [Reroute](#reroute) |  |  |

### Resource — 2

| node | what it does | flags |
|---|---|---|
| [Get Resource Path](#get-resource-path) | Converts a resource data to an attribute set containing the resource path. |  |
| [Get Static Mesh Resource Data](#get-static-mesh-resource-data) | Creates static mesh resource data from the given soft object paths. |  |

### Data Layers — 2

| node | what it does | flags |
|---|---|---|
| [Get Actor Data Layers](#get-actor-data-layers) |  |  |
| [Partition by Actor Data Layers](#partition-by-actor-data-layers) |  |  |

### Blueprint — 1

| node | what it does | flags |
|---|---|---|
| [Execute Blueprint](#execute-blueprint) | Executes a specified custom Blueprint Class with the Execute or Execute With Context method on a clean instance of a Blueprint Class deriving from UPCGBlueprintElement. |  |

### Density — 1

| node | what it does | flags |
|---|---|---|
| [Density Remap](#density-remap) | Applies a linear transform to the point densities. | ⚠ |

### Hierarchical Generation — 1

| node | what it does | flags |
|---|---|---|
| [Hi Gen Grid Size](#hi-gen-grid-size) | Set the execution grid size for downstream nodes. |  |

---

## 3. Nodes by category

Each entry: title, class, plugin, description, detected pins, and **every editable setting** the node declares (its own plus inherited ones below `UPCGSettings`). Enum settings list their options.

### ▸ Sampler

#### Copy Points  ★

`UPCGCopyPointsSettings` · plugin `PCG`

[src] For each point pair from the source and the target, create a copy, inheriting properties & attributes depending on the node settings.

[epic] Copies an instance of all points in the Source per point in the Target input. There are multiple options for inheriting spatial properties, but Attribute Inheritance has the most impact on the performance of this node. You can use this node to perform nested loop copies so you can have one source with two targets with two outputs, or two sources with two target with four outputs. This node is often used to instantiate Point Data generated in local space (namely in PCG assemblies/assets). Prior to post processing at their world position.

**Pin data types detected:** in `Point` → out `default`

★ **This project:** L0 — places mesh-local points on the actor

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `RotationInheritance` | `EPCGCopyPointsInheritanceMode` | `EPCGCopyPointsInheritanceMode::Relative` | ◆ | The method used to determine output point rotation *Options: Relative · Source · Target* |
| `bApplyTargetRotationToPositions` | `bool` | `true` | ◆ | If this option is set, points will have their source position transformed using the target transform with rotation *Only when* `RotationInheritance==EPCGCopyPointsInheritanceMode::Source` |
| `ScaleInheritance` | `EPCGCopyPointsInheritanceMode` | `EPCGCopyPointsInheritanceMode::Relative` | ◆ | The method used to determine output point scale *Options: Relative · Source · Target* |
| `bApplyTargetScaleToPositions` | `bool` | `true` | ◆ | If this option is set, points will have their source position transformed using the target transform with scale *Only when* `ScaleInheritance==EPCGCopyPointsInheritanceMode::Source` |
| `ColorInheritance` | `EPCGCopyPointsInheritanceMode` | `EPCGCopyPointsInheritanceMode::Relative` | ◆ | The method used to determine output point color *Options: Relative · Source · Target* |
| `SeedInheritance` | `EPCGCopyPointsInheritanceMode` | `EPCGCopyPointsInheritanceMode::Relative` | ◆ | The method used to determine output seed values. Relative recomputes the seed from the new location. *Options: Relative · Source · Target* |
| `AttributeInheritance` | `EPCGCopyPointsMetadataInheritanceMode` | `EPCGCopyPointsMetadataInheritanceMode::SourceFirst` | ◆ | The method used to determine output data attributes *Options: SourceFirst · TargetFirst · SourceOnly · TargetOnly · None* |
| `TagInheritance` | `EPCGCopyPointsTagInheritanceMode` | `EPCGCopyPointsTagInheritanceMode::Both` | ◆ | The method used to determine the output data tags *Options: Both · Source · Target* |
| `bCopyEachSourceOnEveryTarget` | `bool` | `true` | ◆ | If this option is set, each source point data will be copied to every target point data (cartesian product), producing N * M point data. Otherwise, will do a N:N (or N:1 or 1:N) operation, producing N point data. |
| `bMatchBasedOnAttribute` | `bool` | `false` |  | Perform a conditional copy point where data pairs must have a matching attribute in order to participate in the copy operation. EXPERIMENTAL: This feature is work in progress and is currently GPU-only. It may not be stable, and may be removed in the future. *Only when* `bExecuteOnGPU` |
| `MatchAttribute` | `FName` | `NAME_None` |  | Attribute that must be present on both the source data and the target point, and have the same value. EXPERIMENTAL: This feature is work in progress and is currently GPU-only. It may not be stable, and may be removed in the future. *Only when* `bExecuteOnGPU && bMatchBasedOnAttribute` |

#### Mesh Sampler  ★ · β Beta

`UPCGMeshSamplerSettings` · plugin `PCGGeometryScriptInterop`

[src] Sample points on a static mesh.

[epic] Samples points on a specified static mesh. Note that this operation is costly. Requires the PCG Geometry Script Interop plugin and the Geometry Script plugin.

**Pin data types detected:** in `Any` → out `Point`

★ **This project:** L0 sampler in `SG_SurfaceSource`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bExtractMeshFromInput` | `bool` | `false` |  | Can provide a list of inputs to sample the meshes from. It can be a list of StaticMeshes, a list of Actors that have a Scene Component (like a Static Mesh Component), or a list of Scene Components directly. Geometry Script needs to be able to extract a dynamic mesh from this scene component (so won't work for ISMCs for example) and for now will work only with a single scene component. Each entry (either in the same d … |
| `StaticMesh` | `soft UStaticMesh` |  | ◆ | Soft Object Path to the mesh to sample from. Will be loaded. *Only when* `!bExtractMeshFromInput` |
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | Selector to read data from. *Only when* `bExtractMeshFromInput` |
| `SamplingMethod` | `EPCGMeshSamplingMethod` | `EPCGMeshSamplingMethod::OnePointPerTriangle` |  | *Options: OnePointPerTriangle · OnePointPerVertex · PoissonSampling* |
| `bUseColorChannelAsDensity` | `bool` | `false` | ◆ | Will extract the color channel into the density. |
| `ColorChannelAsDensity` | `EPCGColorChannel` | `EPCGColorChannel::Red` | ◆ | *Options: Red · Green · Blue · Alpha* *Only when* `bUseColorChannelAsDensity` |
| `bVoxelize` | `bool` | `false` | ◆ | Enable voxelisation as a preparation pass. Can be more expensive given the VoxelSize. |
| `VoxelSize` | `float` | `100.0f` | ◆ | Size of a voxel for the voxelization. *Only when* `bVoxelize` |
| `bRemoveHiddenTriangles` | `bool` | `true` | ◆ | Post-processing pass after voxelization to remove hidden triangles. *Only when* `bVoxelize` |
| `RequestedLODType` | `EGeometryScriptLODType` | `EGeometryScriptLODType::RenderData` | ◆ | LOD type to use when creating DynamicMesh from specified StaticMesh. |
| `RequestedLODIndex` | `int32` | `0` | ◆ |  |
| `SamplingOptions` | `FGeometryScriptMeshPointSamplingOptions` |  | ◆ | Poisson Sampling parameters *Only when* `SamplingMethod == EPCGMeshSamplingMethod::PoissonSampling` |
| ↳ `SamplingRadius` | `float` | `10.0` |  | Desired "radius" of sample points. Spacing between samples is at least 2x this value. |
| ↳ `MaxNumSamples` | `int` | `0` |  | Maximum number of samples requested. If 0 or default value, mesh will be maximally sampled |
| ↳ `RandomSeed` | `int` | `0` |  | Random Seed used to initialize sampling strategies |
| ↳ `SubSampleDensity` | `double` | `10` |  | Density of subsampling used in Poisson strategy. Larger numbers mean "more accurate" (but slower) results. |
| ↳ `SamplingMethodVersion` | `int` | `INDEX_NONE` |  | If < 0, the latest, recommended sampling methods will be used. Otherwise, requests a specific sampling method version. Set this for more consistent results across UE versions, at the risk of worse performance or quality. Valid versions are: Method 0: UE 5.5 and earlier sampling method. Slower initial (dense) point sampling, less robust to degenerate triangles. Method 1: Currently the default method. |
| `NonUniformSamplingOptions` | `FGeometryScriptNonUniformPointSamplingOptions` |  | ◆ | *Only when* `SamplingMethod == EPCGMeshSamplingMethod::PoissonSampling` |
| ↳ `MaxSamplingRadius` | `float` | `0.0` |  | If MaxSampleRadius > SampleRadius, then output sample radius will be in range [SampleRadius, MaxSampleRadius] |
| ↳ `SizeDistribution` | `EGeometryScriptSamplingDistributionMode` | `EGeometryScriptSamplingDistributionMode::Uniform` |  | SizeDistribution setting controls the distribution of sample radii |
| ↳ `SizeDistributionPower` | `double` | `2.0` |  | SizeDistributionPower is used to control how extreme the Size Distribution shift is. Valid range is [1,10] *Only when* `(SizeDistribution != EGeometryScriptSamplingDistributionMode::Uniform)` |
| ↳ `WeightMode` | `EGeometryScriptSamplingWeightMode` | `EGeometryScriptSamplingWeightMode::WeightedRandom` |  | WeightMode controls how any active Weight scheme is used to affect sample radius |
| ↳ `bInvertWeights` | `bool` | `false` |  | If true, weight values are inverted |
| `bExtractUVAsAttribute` | `bool` | `false` | ◆ | *Only when* `SamplingMethod != EPCGMeshSamplingMethod::OnePointPerVertex` |
| `UVAttributeName` | `FName` | `TEXT("UV")` | ◆ | *Only when* `SamplingMethod != EPCGMeshSamplingMethod::OnePointPerVertex && bExtractUVAsAttribute` |
| `UVChannel` | `int32` | `0` | ◆ | *Only when* `SamplingMethod != EPCGMeshSamplingMethod::OnePointPerVertex && bExtractUVAsAttribute` |
| `bOutputTriangleIds` | `bool` | `false` | ◆ | *Only when* `SamplingMethod != EPCGMeshSamplingMethod::OnePointPerVertex` |
| `TriangleIdAttributeName` | `FName` | `TEXT("TriangleId")` | ◆ | *Only when* `SamplingMethod != EPCGMeshSamplingMethod::OnePointPerVertex && bOutputTriangleIds` |
| `bOutputMaterialInfo` | `bool` | `false` | ◆ | *Only when* `SamplingMethod != EPCGMeshSamplingMethod::OnePointPerVertex` |
| `MaterialIdAttributeName` | `FName` | `TEXT("MaterialId")` | ◆ | *Only when* `SamplingMethod != EPCGMeshSamplingMethod::OnePointPerVertex && bOutputMaterialInfo` |
| `MaterialAttributeName` | `FName` | `TEXT("Material")` | ◆ | *Only when* `SamplingMethod != EPCGMeshSamplingMethod::OnePointPerVertex && bOutputMaterialInfo` |
| `PointSteepness` | `float` | `0.5f` | ◆ | Each PCG point represents a discretized, volumetric region of world space. The points' Steepness value [0.0 to 1.0] establishes how "hard" or "soft" that volume will be represented. From 0, it will ramp up linearly increasing its influence over the density from the point's center to up to two times the bounds. At 1, it will represent a binary box function with the size of the point's bounds. |
| `bSynchronousLoad` | `bool` | `false` |  |  |

#### Sample Texture  ★

`UPCGSampleTextureSettings` · plugin `PCG`

[src] Samples color of texture at each point.

**Pin data types detected:** in `BaseTexture, Point` → out `default`

★ **This project:** 7d.9 Gaea masks into PCG

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `TextureMappingMethod` | `EPCGTextureMappingMethod` | `EPCGTextureMappingMethod::Planar` | ◆ | Whether to treat the sample positions as being in 0-1 UV space. If method is Planar then the coordinates will be transformed according to the texture settings. *Options: Planar · UVCoordinates* |
| `UV Coordinates Attribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | The attribute that provides sample positions for sampling the texture. *Only when* `TextureMappingMethod == EPCGTextureMappingMethod::UVCoordinates` |
| `TilingMode` | `EPCGTextureAddressMode` | `EPCGTextureAddressMode::Wrap` | ◆ | Overrides the texture's tiling to wrap or clamp its UVs. *Options: Clamp · Wrap* *Only when* `TextureMappingMethod == EPCGTextureMappingMethod::UVCoordinates` |
| `DensityMergeFunction` | `EPCGDensityMergeOperation` | `EPCGDensityMergeOperation::Set` | ◆ | Controls the behavior of density computation with respect to initial data. *Options: Set · Ignore · Minimum · Maximum · Add · Subtract · Multiply · Divide* |
| `bClampOutputDensity` | `bool` | `true` | ◆ | Controls whether the output density should be clamped or not. |

#### Scene Capture

`UPCGSceneCaptureSettings` · plugin `PCG`

[src] Perform a 2D orthographic scene capture and write the result to a render target data. Can be costly, use with caution with runtime generation.

**Pin data types detected:** in `Spatial` → out `RenderTarget`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PixelFormat` | `TEnumAsByte<enum ETextureRenderTargetFormat>` | `ETextureRenderTargetFormat::RTF_RGBA16f` | ◆ | Subset of EPixelFormat exposed to UTextureRenderTarget2D. |
| `CaptureSource` | `TEnumAsByte<enum ESceneCaptureSource>` | `ESceneCaptureSource::SCS_SceneColorHDR` | ◆ | Specifies which component of the scene rendering should be output to the render target. |
| `TexelSize` | `float` | `50.0f` | ◆ | Size of a texel in the render target in world units (cm). |
| `bSkipReadbackToCPU` | `bool` | `false` |  | Skip CPU readback during initialization of the render target data. |

#### Select Points

`UPCGSelectPointsSettings` · plugin `PCG`

[src] Selects a stable random subset of the input points.

[epic] Selects a subset of points from the input Point Data using a probability that a given point will be selected or not. In practice, this means that if you take a ratio of 0.5, you will have approximately half the input points, but have no guarantee on whether it is going to be exactly half or not. Since the decision to select a point or not is done independently, this follows a normal distribution.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Ratio` | `float` | `0.1f` | ◆ |  |
| `bKeepZeroDensityPoints` | `bool` | `false` | ◆ |  |

#### Spline Sampler  ★

`UPCGSplineSamplerSettings` · plugin `PCG`

[src] Generates points along the given Spline, and within the Bounding Shape if provided.

[epic] Samples points using the spline as the source material. Sampling on the spline means directly on the spline curve, while the Horizontal, Vertical and Volume options sample on the spline volume (driven by the radius of the control points in the Y/Z axes). Sampling inside the spline requires the spline to be closed.

**Pin data types detected:** in `PolyLine, Spatial` → out `default`

★ **This project:** job 17 L2 Streets

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SamplerParams` | `FPCGSplineSamplerParams` |  | ◆ |  |

#### Surface Sampler

`UPCGSurfaceSamplerSettings` · plugin `PCG`

[src] Generates points in two dimensional domain that sample the Surface input and lie within the Bounding Shape input.

[epic] Samples points on a Surface data, in a regular grid pattern. This node contains the following options: Point Extents: Defines the basic grid cell size on the surface. Looseness: Defines cell size to allow for variation. In practice, the cell size is point extents * (1 + Looseness). Points Per Square Meter: Computes the ratio of kept cells. This property limits overcrowding when your grid is large.

**Pin data types detected:** in `Spatial, Surface` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PointsPerSquaredMeter` | `float` | `0.1f` | ◆ | Controls the grid cell size, down to a minimum size defined by the Point Extents. |
| `PointExtents` | `FVector` | `FVector(50.0f)` | ◆ | Extents of the points to create (e.g. half their total size) |
| `Looseness` | `float` | `1.0f` | ◆ | Controls how points are placed in their cell with 0 being in the center and 1 being anywhere inside the full cell size. |
| `bUnbounded` | `bool` | `false` | ◆ | If no Bounding Shape input is provided, the actor bounds are used to limit the sample generation domain. This option allows ignoring the actor bounds and generating over the entire surface. Use with caution as this may generate a lot of points. |
| `bApplyDensityToPoints` | `bool` | `true` | ◆ |  |
| `PointSteepness` | `float` | `0.5f` | ◆ | Each PCG point represents a discretized, volumetric region of world space. The points' Steepness value [0.0 to 1.0] establishes how "hard" or "soft" that volume will be represented. From 0, it will ramp up linearly increasing its influence over the density from the point's center to up to two times the bounds. At 1, it will represent a binary box function with the size of the point's bounds. |
| `bKeepZeroDensityPoints` | `bool` | `false` | ◆ |  |
| `bUseLegacyGridCreationMethod` | `bool` | `false` |  | Controls whether the prior grid creation mechanism (with cells being extents * (1 + steepness), then filtered by points by squared meters) is used. |

#### Volume Sampler

`UPCGVolumeSamplerSettings` · plugin `PCG`

[src] Generates points in the three dimensional bounds of the Volume input and within the Bounding Shape input if provided.

[epic] Samples the provided spatial data on a regular 3D grid. This exhibits 'voxel-like' behavior and could potentially be costly for large data or high densities.

**Pin data types detected:** in `Spatial` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `VoxelSize` | `FVector` | `PCGVolumeSampler::DefaultVoxelSize` | ◆ |  |
| `bUnbounded` | `bool` | `false` | ◆ | If no Bounding Shape input is provided, the actor bounds are used to limit the sample generation domain. This option allows ignoring the actor bounds and generating over the entire volume. Use with caution as this may generate a lot of points. |
| `PointSteepness` | `float` | `0.5f` | ◆ | Each PCG point represents a discretized, volumetric region of world space. The points' Steepness value [0.0 to 1.0] establishes how "hard" or "soft" that volume will be represented. From 0, it will ramp up linearly increasing its influence over the density from the point's center to up to two times the bounds. At 1, it will represent a binary box function with the size of the point's bounds. |

### ▸ Spatial

#### Attribute Set To Point

`UPCGConvertToPointDataSettings` · plugin `PCG`

[class] Converts attribute sets to point data

[epic] Converts an Attribute Set to Data Point by creating one default point per entry in the Attribute Set. The resulting Point Data has the same attributes as the original Attribute Set.

**Pin data types detected:** in `Param` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bMatchAttributeNamesWithPropertyNames` | `bool` | `false` | ◆ | Try to match attribute names that matches point property names to automatically set them. |
| `AttributeToConvert` | `TMap<FPCGAttributePropertyInputSelector, FPCGAttributePropertyOutputSe …` |  | ◆ | Can remap attribute to point properties at the same time. |
| `bDeleteOriginalRemappedAttribute` | `bool` | `true` | ◆ | When an attribute is remapped, delete the original. |

#### Bad Outputs  hidden in palette

`UPCGBadOutputsNodeSettings` · plugin `PCG`

[class] Test node to write bad outputs

*No editable settings declared.*

#### Bounds From Mesh

`UPCGBoundsFromMeshSettings` · plugin `PCG`

[src] Sets the bounds according to the static or skeletal mesh(es) provided in the mesh pin.

**Pin data types detected:** in `Param, Point` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `MeshAttribute` | `FPCGAttributePropertyInputSelector` |  |  | Attribute from which to source the meshes to use. |
| `bSilenceAttributeNotFoundErrors` | `bool` | `false` |  | Will not produce warnings when the input data does not have the required attribute. |
| `bSynchronousLoad` | `bool` | `false` |  | By default, will use async loading for the meshes. |

#### Clean Spline

`UPCGCleanSplineSettings` · plugin `PCG`

[src] Remove superfluous control points along the spline, such as those that are co-located or collinear.

**Pin data types detected:** in `Spline` → out `Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bFuseColocatedControlPoints` | `bool` | `true` | ◆ | Fuse control points that share the same location in world space, within a distance threshold. Colocated points are inherently collinear, so this will automatically be applied when removing collinear points. |
| `ColocationDistanceThreshold` | `double` | `UE_KINDA_SMALL_NUMBER` | ◆ | Control points will be considered co-located if they are within this distance from one another. *Only when* `bFuseColocatedControlPoints` |
| `bUseSplineLocalSpace` | `bool` | `false` | ◆ | Use spline local space for the distance calculation, rather than world space. *Only when* `bFuseColocatedControlPoints` |
| `FuseMode` | `EPCGControlPointFuseMode` | `EPCGControlPointFuseMode::Auto` | ◆ | Controls how two co-located points will be fused together. *Options: KeepFirst · KeepSecond · Merge · Auto* *Only when* `bFuseColocatedControlPoints` |
| `bRemoveCollinearControlPoints` | `bool` | `true` | ◆ | Remove control points on linear sections of the spline that would otherwise have no effect on the final spline calculation. |
| `CollinearAngleThreshold` | `double` | `5` | ◆ | A control point will be considered collinear if it is within this angle from the segment between its previous and next control points. *Only when* `bRemoveCollinearControlPoints` |
| `bUseRadians` | `bool` | `false` |  | Use radians directly, instead of degrees. The current 'CollinearAngleThreshold' value will be automatically converted when toggled. *Only when* `bRemoveCollinearControlPoints` |

#### Clip Paths

`UPCGClipPathsSettings` · plugin `PCG`

[src] Clips paths against the polygons, to have the paths either inscribed in the polygons (intersection) or outside the polygons (difference).

[epic] Used to intersect or difference splines with Polygon 2D shapes.

**Pin data types detected:** in `Point, Polygon2D, Spline` → out `Point, Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGClipPathOperation` | `EPCGClipPathOperation::Intersection` |  | Controls whether the paths will be clipped to be inside or outside the clip polygons. *Options: Intersection · Difference* |
| `SplineMaxDiscretizationError` | `double` | `1.0` | ◆ | Maximum squared distance before we need to subdivide a segment again as part of the spline discretization to a polygon. |

#### Create Collision Data

`UPCGCreateCollisionDataSettings` · plugin `PCG`

[src] Creates a volumetric representation of the points as if they had their selected mesh collision.

**Pin data types detected:** in `default` → out `Primitive`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `CollisionAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `CollisionQueryFlag` | `EPCGCollisionQueryFlag` | `EPCGCollisionQueryFlag::Simple` | ◆ | Controls how shapes are selected from collision. Performance warning on using complex shapes. *Options: Simple · Complex · SimpleFirst · ComplexFirst* |
| `bWarnIfAttributeCouldNotBeUsed` | `bool` | `true` |  |  |
| `bSynchronousLoad` | `bool` | `false` |  |  |

#### Create Points

`UPCGCreatePointsSettings` · plugin `PCG`

[src] Creates point data from a provided list of points.

[epic] Creates a point data containing points from a static description of points. This node is normally used to create a single point to seed another process that would require some world position or similar.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PointsToCreate` | `TArray<FPCGPoint>` |  | ◆ |  |
| `CoordinateSpace` | `EPCGCoordinateSpace` | `EPCGCoordinateSpace::World` | ◆ | Sets the generation referential of the points *Options: World · OriginalComponent · LocalComponent* |
| `bCullPointsOutsideVolume` | `bool` | `false` | ◆ | If true, points are removed if they are outside of the volume |

#### Create Points Grid

`UPCGCreatePointsGridSettings` · plugin `PCG`

[src] Creates a 2D or 3D grid of points.

[epic] Creates a point data containing a simple grid of points defined by the settings. This node is used in local space mode couples with the Copy Points node to create grids around multiple sources.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `GridExtents` | `FVector` | `FVector(500.0, 500.0, 50.0)` | ◆ |  |
| `CellSize` | `FVector` | `FVector(100.0, 100.0, 100.0)` | ◆ |  |
| `PointSteepness` | `float` | `0.5f` | ◆ | Each PCG point represents a discretized, volumetric region of world space. The points' Steepness value [0.0 to 1.0] establishes how "hard" or "soft" that volume will be represented. From 0, it will ramp up linearly increasing its influence over the density from the point's center to up to two times the bounds. At 1, it will represent a binary box function with the size of the point's bounds. |
| `CoordinateSpace` | `EPCGCoordinateSpace` | `EPCGCoordinateSpace::World` | ◆ | Sets the generation referential of the points *Options: World · OriginalComponent · LocalComponent* |
| `bSetPointsBounds` | `bool` | `true` | ◆ | If true, the bounds of the points are set to 50.0, if false, 1.0 |
| `bCullPointsOutsideVolume` | `bool` | `false` | ◆ | If true, points are removed if they are outside of the volume |
| `PointPosition` | `EPCGPointPosition` | `EPCGPointPosition::CellCenter` | ◆ | *Options: CellCenter · CellCorners* |

#### Create Points Sphere

`UPCGCreatePointsSphereSettings` · plugin `PCG`

[src] Generate points on the surface of a sphere.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SphereGeneration` | `EPCGSphereGeneration` | `EPCGSphereGeneration::Geodesic` | ◆ | Determines the type of sphere generated. *Options: Geodesic · Angle · Segments · Random · Poisson* |
| `CoordinateSpace` | `EPCGCoordinateSpace` | `EPCGCoordinateSpace::World` | ◆ | Sets the generation referential of the points. *Options: World · OriginalComponent · LocalComponent* |
| `PointOrientation` | `EPCGSpherePointOrientation` | `EPCGSpherePointOrientation::Radial` | ◆ | Will determine the points' orientation, once generated. *Options: Radial · Centric · None* |
| `Origin` | `FVector` | `FVector::ZeroVector` | ◆ | The sphere's origin, around which the points will be generated. |
| `Radius` | `double` | `100.0` | ◆ | The sphere's radius. |
| `GeodesicSubdivisions` | `int32` | `2` | ◆ | Determines the number of subdivisions of the geodesic sphere. Becomes exponentially more expensive as it gets higher. *Only when* `SphereGeneration == EPCGSphereGeneration::Geodesic` |
| `Latitudinal Segment (Degrees)` | `double` | `12` | ◆ | The latitudinal angle (in degrees) between generated segments on the standard sphere grid. *Only when* `SphereGeneration == EPCGSphereGeneration::Angle` |
| `Longitudinal Segment (Degrees)` | `double` | `12` | ◆ | The longitudinal angle (in degrees) between generated segments on the standard sphere grid. *Only when* `SphereGeneration == EPCGSphereGeneration::Angle` |
| `LatitudinalSegments` | `int32` | `15` | ◆ | Will determine the latitudinal angle between segments needed to generate this number of latitudinal segments. *Only when* `SphereGeneration == EPCGSphereGeneration::Segments` |
| `LongitudinalSegments` | `int32` | `30` | ◆ | Will determine the longitudinal angle between segments needed to generate this number of longitudinal segments. *Only when* `SphereGeneration == EPCGSphereGeneration::Segments` |
| `SampleCount` | `int32` | `100` | ◆ | Determines the number of samples generated for the random generation and the poisson sampling. *Only when* `SphereGeneration == EPCGSphereGeneration::Random \|\| SphereGeneration == EPCGSphereGeneration::Poisson` |
| `PoissonDistance` | `double` | `100.0` | ◆ | The maximum world distance between points sampled on the sphere's surface during a Poisson sampling, in cm. *Only when* `SphereGeneration == EPCGSphereGeneration::Poisson` |
| `PoissonMaxAttempts` | `int32` | `32` | ◆ | Poisson sampling will continue to search for open positions until this limit is reached. *Only when* `SphereGeneration == EPCGSphereGeneration::Poisson` |
| `LatitudinalStartAngle` | `double` | `-90.0` | ◆ | Points will be generated on the sphere's surface beginning at this equatorial angle. |
| `LatitudinalEndAngle` | `double` | `90.0` | ◆ | Points will cease to be generated on the sphere's surface after this equatorial angle. |
| `LongitudinalStartAngle` | `double` | `-180.0` | ◆ | Points will be generated on the sphere's surface beginning at this meridional angle. |
| `LongitudinalEndAngle` | `double` | `180.0` | ◆ | Points will cease to be generated on the sphere's surface after this meridional angle. |
| `Jitter` | `double` | `0.0` | ◆ | Adds randomization (in the range of [-Jitter, Jitter]) of the angles of a generated point. *Only when* `SphereGeneration == EPCGSphereGeneration::Angle \|\| SphereGeneration == EPCGSphereGeneration::Segments` |
| `PointSteepness` | `float` | `0.5f` | ◆ | Directly set as the output points' steepness value. |
| `bCullPointsOutsideVolume` | `bool` | `false` | ◆ | Points are removed if they are outside the volume. |
| `PointLimit` | `int32` | `1000000` |  | Adds a graph error and prevents generation if the generated point count would exceed this amount. |

#### Create Polygon 2D  ★

`UPCGCreatePolygon2DSettings` · plugin `PCG`

[src] Creates a (closed) 2d polygon per input.

[epic] Creates a Polygon 2D data from the input point data or spline data.

**Pin data types detected:** in `Point, Spline` → out `default`

★ **This project:** job 18b

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputType` | `EPCGCreatePolygonInputType` | `EPCGCreatePolygonInputType::Automatic` | ◆ | Controls the way input data will be considered - either as closed or open paths. *Options: Automatic · ForceOpen · ForceClosed* |
| `bUseHoleAttribute` | `bool` | `false` | ◆ | Controls whether we will use the hole attribute to separate outer from hole segments. Note that the attribute will be used only when the input is a point data. |
| `HoleIndexAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute that describes the hole index of the points, where -1 is the outer polygon, and other values are for holes. Expects values on inputs to be sequential and increasing only. Note that this will be used only on point data. *Only when* `bUseHoleAttribute` |
| `bUsePolygonWidthAttribute` | `bool` | `false` | ◆ | Controls whether target polygon width (when open/forced open) will be driven by an attribute. |
| `PolygonWidthAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute from which to get the width value *Only when* `bUsePolygonWidthAttribute` |
| `OpenPolygonWidth` | `double` | `100.0` | ◆ | Target width of the polygon generated from an open path. *Only when* `!bUsePolygonWidthAttribute && InputType != EPCGCreatePolygonInputType::ForceClosed` |
| `SplineMaxDiscretizationError` | `double` | `1.0` | ◆ | Maximum squared distance before we need to subdivide a segment again as part of the spline discretization to a polygon. |

#### Create Spline

`UPCGCreateSplineSettings` · plugin `PCG`

[src] Creates PCG spline data from the input PCG point data, in a sequential order.

[epic] Creates a Spline from the input point data. Contains options to create the following: Create Component or Create Data Only Closed or Linear Splines Apply custom in and out tangents from Attribute names.

**Pin data types detected:** in `default` → out `Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `EPCGCreateSplineMode` | `EPCGCreateSplineMode::CreateDataOnly` | ◆ | *Options: CreateDataOnly · CreateComponent* |
| `bClosedLoop` | `bool` | `false` | ◆ |  |
| `bLinear` | `bool` | `false` | ◆ | Controls whether the segment between control points is a curve (when false) or a straight line (when true). |
| `bApplyCustomTangents` | `bool` | `false` | ◆ | Allow to specify custom tangents for each point, as an attribute. Can't be set if the spline is linear. *Only when* `!bLinear` |
| `ArriveTangentAttribute` | `FName` |  | ◆ | *Only when* `!bLinear && bApplyCustomTangents` |
| `LeaveTangentAttribute` | `FName` |  | ◆ | *Only when* `!bLinear && bApplyCustomTangents` |
| `PostProcessFunctionNames` | `TArray<FName>` |  |  | Specify a list of functions to be called on the target actor after spline creation. Functions need to be parameter-less and with "CallInEditor" flag enabled. |

#### Create Surface From Polygon2D

`UPCGCreateSurfaceFromPolygon2DSettings` · plugin `PCG`

[src] Creates a surface data from a Polygon 2D data.

[epic] Creates an implicit surface from a Polygon 2D. This surface can then be used like other surfaces in the Surface Sampler, Difference, Intersection, and other operations.

**Pin data types detected:** in `default` → out `Surface`

*No editable settings declared.*

#### Create Surface From Spline

`UPCGCreateSurfaceFromSplineSettings` · plugin `PCG`

[src] Create an implicit surface for each given spline. The surface is given by the top-down 2D projection of the spline. Each spline must be closed.

[epic] Creates an implicit surface from a closed spline. This surface can then be used like other surfaces in the Surface Sampler, Difference, Intersection, and other operations. At this point in time, this relies on a discretization of the spline and as such, might not work for very large splines. If that is the case, consider sampling your spline first, then creating a new spline (using the Create Spline node) before using this node.

**Pin data types detected:** in `Spline` → out `Surface`

*No editable settings declared.*

#### Cull Points Outside Actor Bounds

`UPCGCullPointsOutsideActorBoundsSettings` · plugin `PCG`

[src] Culls points that lie outside the current actor bounds.

[epic] Culls point from the input Point Data based on the current component (partition actor or original) bounds with additional control for bounds expansion. This can be used to make sure input data is relevant to the current processing while allowing some overlap if required.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `BoundsExpansion` | `float` | `0.0` | ◆ |  |
| `Mode` | `EPCGCullPointsMode` | `EPCGCullPointsMode::Ordered` | ◆ | *Options: Ordered · Unordered* |

#### Difference

`UPCGDifferenceSettings` · plugin `PCG`

[src] Spatially subtracts the target difference data from the source data, outputing the difference of the two.

[epic] Outputs the result of the difference of each source against the union of the differences. This node has the following options: Density Function: Controls which density function is used after the operation is complete. Contains the following options: Minimum: Final density is equal to the density of the source minus the max density of all the differences. Clamped Subtraction: Final density is equal to the density of the source minus the sum density of all the differences. This value is clamped between 0 and 1. Binary: Final density is equal to 0 if the density of the difference is greater than zero. Otherwise the final density is equal to the density of the source. Mode: Controls behavior of difference in the presence of concrete spatial data vs continuous data (other types, more akin to distribution functions). Note that in some cases where we want to select a concrete element, this shou …

**Pin data types detected:** in `Spatial` → out `Spatial`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `DensityFunction` | `EPCGDifferenceDensityFunction` | `EPCGDifferenceDensityFunction::Minimum` | ◆ | The density function to use when recalculating the density after the operation. *Options: Minimum · ClampedSubstraction · Binary* |
| `Mode` | `EPCGDifferenceMode` | `EPCGDifferenceMode::Inferred` |  | Describes how the difference operation will treat the output data: Continuous - Non-destructive data output will be maintained. Discrete - Output data will be discrete points, or explicitly converted to points. Inferred - Output data will choose from Continuous or Discrete, based on the source and operation. *Options: Inferred · Continuous · Discrete* |
| `bDiffMetadata` | `bool` | `true` |  |  |
| `bKeepZeroDensityPoints` | `bool` | `false` | ◆ | If enabled, the output will not automatically filter out points with zero density. |

#### Distance

`UPCGDistanceSettings` · plugin `PCG`

[src] Calculates and appends a signed 'Distance' attribute to the source data. For each of the source points, a distance attribute will be calculated between it and the nearest target point.

[epic] For each point in the first input, calculates the distance to the nearest point in the second input and automatically ignores self when computing the distance from one point data set to the same point data set. Optionally, can output the distance vector as an attribute. This node is used to simulate distance fields or create distance-based gradients in a Point Data. This can be used to tweak the scale of trees on the edges of forests or ones that are too close to a stream.

**Pin data types detected:** in `Point` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bOutputToAttribute` | `bool` | `true` | ◆ | Output the distance or distance vector to an attribute. |
| `OutputAttribute` | `FPCGAttributePropertySelector` | `FPCGAttributePropertySelector::CreateAttributeSelector(PCGDi …` | ◆ | The attribute output for the resulting distance value. *Only when* `bOutputToAttribute` |
| `bOutputDistanceVector` | `bool` | `false` | ◆ | Controls whether the attribute will be a scalar or a vector *Only when* `bOutputToAttribute` |
| `bSetDensity` | `bool` | `false` | ◆ | If true, will also set the density to be 0 - 1 based on MaximumDistance |
| `MaximumDistance` | `double` | `20000.0` | ◆ | A maximum distance to search, which is used as an optimization |
| `SourceShape` | `PCGDistanceShape` | `PCGDistanceShape::SphereBounds` | ◆ | What shape is used on the 'source' points |
| `TargetShape` | `PCGDistanceShape` | `PCGDistanceShape::SphereBounds` | ◆ | What shape is used on the 'target' points |
| `bCheckSourceAgainstRespectiveTarget` | `bool` | `false` | ◆ | If this option is on, each source will be tested against its respective target (for a N:N operation). Source and Target num must be the same (or 1). |

#### Duplicate Cross-Sections

`UPCGDuplicateCrossSectionsSettings` · plugin `PCG`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

**Pin data types detected:** in `Param, Spline` → out `Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bExtrudeVectorAsAttribute` | `bool` | `false` |  | Set it to true if you want the extrude vector to be taken from the input spline as attribute, or fixed in the settings. |
| `ExtrudeVector` | `FVector` | `FVector(0.0, 0.0, 1000.0)` | ◆ | *Only when* `!bExtrudeVectorAsAttribute` |
| `ExtrudeVectorAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to be taken from the input spline containing the extrude vector for the slicing. *Only when* `bExtrudeVectorAsAttribute` |
| `bExtraOutputAttributesOnDataDomain` | `bool` | `true` | ◆ | Choose if the Extra Output Attributes are added to the Data domain or the Elements domain. If ForwardAttributesFromModulesInfo is true, module info attributes will also be pushed to the data domain. |
| `bOutputSplineIndexAttribute` | `bool` | `true` | ◆ |  |
| `SplineIndexAttributeName` | `FName` | `TEXT("SplineIndex")` | ◆ | Name of the spline index output attribute name. *Only when* `bOutputSplineIndexAttribute` |
| `bModuleInfoAsInput` | `bool` | `false` |  | Set it to true to pass the info as attribute set. *(from `UPCGSubdivisionBaseSettings`)* |
| `ModulesInfo` | `TArray<FPCGSubdivisionSubmodule>` |  |  | Fixed array of modules used for the subdivision. *Only when* `!bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| `Attribute Names for Module Info` | `FPCGSubdivisionModuleAttributeNames` |  |  | Fixed array of modules used for the subdivision. *Only when* `bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| ↳ `SymbolAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SymbolAttributeName` |  | Mandatory. Expected type: FName. |
| ↳ `SizeAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SizeAttributeName` |  | Mandatory. Expected type: double. |
| ↳ `bProvideScalable` | `bool` | `false` |  |  |
| ↳ `ScalableAttributeName` | `FName` | `PCGSubdivisionBase::Constants::ScalableAttributeName` |  | Optional. Expected type: bool. If disabled, default value will be false. *Only when* `bProvideScalable` |
| ↳ `bProvideDebugColor` | `bool` | `false` |  |  |
| ↳ `DebugColorAttributeName` | `FName` | `PCGSubdivisionBase::Constants::DebugColorAttributeName` |  | Optional. Expected type: Vector4. If disabled, default value will be (1.0, 1.0, 1.0, 1.0). *Only when* `bProvideDebugColor` |
| `GrammarSelection` | `FPCGGrammarSelection` |  | ◆ | An encoded string that represents how to apply a set of rules to a series of defined modules. *(from `UPCGSubdivisionBaseSettings`)* |
| ↳ `bGrammarAsAttribute` | `bool` | `false` | ◆ | Read the grammar as an attribute rather than directly from the settings. Grammar syntax: - Each symbol can have multiple characters - Modules are defined in '[]', multiple symbols in a module are separated with ',' - Modules can be repeated a fixed number of times, by adding a number after it (like [A,B]3 will produce ABABAB) - Modules can be marked repeated an indefinite number of times, with '*'. (like [A,B]* will … |
| ↳ `GrammarString` | `FString` |  | ◆ | An encoded string that represents how to apply a set of rules to a series of defined modules. *Only when* `!bGrammarAsAttribute` |
| ↳ `GrammarAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to be taken from the input spline containing the grammar to use. *Only when* `bGrammarAsAttribute` |
| `bUseSeedAttribute` | `bool` | `false` | ◆ | Controls whether we'll use an attribute to drive random seeding for stochastic processes in the subdivision. *(from `UPCGSubdivisionBaseSettings`)* |
| `SeedAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to use to drive seed selection. It should be convertible to an integer. *Only when* `bUseSeedAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bForwardAttributesFromModulesInfo` | `bool` | `false` | ◆ | Do a match and set with the incoming modules info, only if the modules info is passed as input. *Only when* `bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| `SymbolAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SymbolAttributeName` | ◆ | Name of the Symbol output attribute name. *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputSizeAttribute` | `bool` | `true` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `SizeAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SizeAttributeName` | ◆ | Name of the Size output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputSizeAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputScalableAttribute` | `bool` | `true` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `ScalableAttributeName` | `FName` | `PCGSubdivisionBase::Constants::ScalableAttributeName` | ◆ | Name of the Scalable output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputScalableAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputDebugColorAttribute` | `bool` | `false` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `DebugColorAttributeName` | `FName` | `PCGSubdivisionBase::Constants::DebugColorAttributeName` | ◆ | Name of the Debug Color output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputDebugColorAttribute` *(from `UPCGSubdivisionBaseSettings`)* |

#### Elevation Isolines

`UPCGElevationIsolinesSettings` · plugin `PCG`

[class] Compute the elevation isolines of a surface, can output either points or splines. Currently only work for Z-up surfaces.

**Pin data types detected:** in `Spatial, Surface` → out `Point, Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ElevationStart` | `double` | `0.0` | ◆ | Minimum elevation of the isolines. |
| `ElevationEnd` | `double` | `1000.0` | ◆ | Maximum elevation of the isolines. |
| `ElevationIncrement` | `double` | `100.0` | ◆ | Increment elevation between each isolines. |
| `Resolution` | `double` | `100.0` | ◆ | Resolution of the grid for the discretization of the surface. This is the size of one cell, in cm. |
| `bAddTagOnOutputForSameElevation` | `bool` | `false` | ◆ | Can add a tag (integer) to group output data that are at the same elevation. |
| `bProjectSurfaceNormal` | `bool` | `false` | ◆ | Option to either have Z up or project the surface normal at this position (similar to project rotations on the projection node). |
| `bOutputAsSpline` | `bool` | `false` |  | Will output splines rather than points. |
| `bLinearSpline` | `bool` | `false` | ◆ | Spline can either be curved or linear. *Only when* `bOutputAsSpline` |

#### Find Convex Hull 2D

`UPCGConvexHull2DSettings` · plugin `PCG`

[src] Return the 2D convex hull of a set of points on the XY plane.

[epic] Computes a 2D convex from the input Point Data using the location only (not bounds) of each point. This node can be used in conjunction with the Create Spline node to create a spline that encompasses all the points and that in turn can also be passed into the Create Surface From Spline node.

*No editable settings declared.*

#### Get Actor Data  ★

`UPCGDataFromActorSettings` · plugin `PCG`

[src] Builds a collection of PCG-compatible data from the selected actors.

[epic] General version of the Get … Data nodes. Reads data from an Actor using the Actor Filter and the Mode. It contains the following options: Actor Filter: Determines which Actors to consider when fetching Actor data. Include Children: Determines whether to consider any child Actors of the input. Mode: Contains the following options: Parse Actor Components: Builds PCG data from the components on the Actor. Get Single Point: Return one point data containing one point per actor with its transform and local bounds. Use MergeSinglePointData option if you need to. Get Data from PCG Component: Returns the result of another actor's PCG execution. Note that only data passed to the Output node is stored on the PCG component and only some types are supported (Point Data & Attribute Set), and will be queried accordingly. PCG will make sure that the execution of the remote actor will be done before cont …

**Pin data types detected:** in `Any` → out `Point`

★ **This project:** L0 — finds the surface actor by tag

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. |

#### Get Bounds

`UPCGGetBoundsSettings` · plugin `PCG`

[src] Computes the bounds of the inputs as attributes.

[epic] Creates an attribute set containing the world space bounds (min & max) of any given Spatial data. Note that this is more general than the Combine Points node as it will return bounds for more types. This node can be used as a higher-level construct to do larger scale processing in a graph.

**Pin data types detected:** in `Spatial` → out `Param`

*No editable settings declared.*

#### Get Dynamic Mesh Data  β Beta

`UPCGGetDynamicMeshDataSettings` · plugin `PCGGeometryScriptInterop`

[src] Builds a collection of PCG-compatible data from the selected actors.

**Pin data types detected:** in `default` → out `DynamicMesh`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Options` | `FGeometryScriptCopyMeshFromComponentOptions` |  | ◆ | If data is coming from a component, you can impact the options there. |
| ↳ `bWantNormals` | `bool` | `true` |  |  |
| ↳ `bWantTangents` | `bool` | `true` |  |  |
| ↳ `bWantInstanceColors` | `bool` | `false` |  | Whether to request per-instance vertex colors (where applicable; applies to RenderData LODs of Static Mesh components) |
| ↳ `RequestedLOD` | `FGeometryScriptMeshReadLOD` | `FGeometryScriptMeshReadLOD()` |  |  |
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` *(from `UPCGDataFromActorSettings`)* |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` *(from `UPCGDataFromActorSettings`)* |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` *(from `UPCGDataFromActorSettings`)* |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` *(from `UPCGDataFromActorSettings`)* |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` *(from `UPCGDataFromActorSettings`)* |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. *(from `UPCGDataFromActorSettings`)* |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. *(from `UPCGDataFromActorSettings`)* |

#### Get Landscape Data

`UPCGGetLandscapeSettings` · plugin `PCG`

[src] Builds a collection of landscapes from the selected actors.

[epic] Specialization of the Get Actor Data node that returns appropriately typed and constructed Landscape data.

**Pin data types detected:** in `default` → out `Landscape`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SamplingProperties` | `FPCGLandscapeDataProps` |  | ◆ |  |
| ↳ `bGetHeightOnly` | `bool` | `false` | ◆ | Controls whether the points projected on the landscape will return the normal/tangent (if false) or only the position (if true) |
| ↳ `bGetLayerWeights` | `bool` | `true` | ◆ | Controls whether data from landscape layers will be retrieved (turning it off is an optimization if that data is not needed) |
| ↳ `bGetActorReference` | `bool` | `false` | ◆ | Controls whether the points from this landscape will return the actor from which they originate (e.g. which Landscape Proxy) |
| ↳ `bGetPhysicalMaterial` | `bool` | `false` | ◆ | Controls whether the points from the landscape will have their physical material added as the "PhysicalMaterial" attribute |
| ↳ `bGetComponentCoordinates` | `bool` | `false` | ◆ | Controls whether the component coordinates will be added the point as attributes ('CoordinateX', 'CoordinateY') |
| ↳ `bSampleVirtualTextures` | `bool` | `true` | ◆ | Controls whether the landscape will try to sample from the landscape virtual textures (if they exist). Only relevant to GPU sampling. |
| ↳ `bSampleVirtualTextureNormals` | `bool` | `false` | ◆ | Controls whether the landscape will try to sample normals from a normals virtual texture (if it exists), otherwise computes normals from multiple height samples. Only relevant to GPU sampling. Note that normal virtual textures may be detail normals and not match the actual landscape surface normals, so enable this with caution. Requires bSampleVirtualTextures to be true. *Only when* `bSampleVirtualTextures` |
| `bUnbounded` | `bool` | `true` | ◆ | Editor only: If true, the intersected landscape bounds are going to be used to prepare the landscape cache, otherwise the PCG Component's grid bounds will be used. |
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` *(from `UPCGDataFromActorSettings`)* |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` *(from `UPCGDataFromActorSettings`)* |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` *(from `UPCGDataFromActorSettings`)* |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` *(from `UPCGDataFromActorSettings`)* |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` *(from `UPCGDataFromActorSettings`)* |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. *(from `UPCGDataFromActorSettings`)* |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. *(from `UPCGDataFromActorSettings`)* |

#### Get PCG Component Data

`UPCGGetPCGComponentSettings` · plugin `PCG`

[src] Builds a collection of data from other PCG components on the selected actors. Automatically tags each output with the grid size it was collected from, prefixed by "PCG_GridSize_" (e.g.PCG_GridSize_12800). Note: a component cannot get component data from itself or other components in its execution context, as it could create a circular dependency.

[epic] Specialization of the Get Actor Data node that returns only the generated output from selected actor PCG components.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` *(from `UPCGDataFromActorSettings`)* |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` *(from `UPCGDataFromActorSettings`)* |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` *(from `UPCGDataFromActorSettings`)* |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` *(from `UPCGDataFromActorSettings`)* |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` *(from `UPCGDataFromActorSettings`)* |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. *(from `UPCGDataFromActorSettings`)* |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. *(from `UPCGDataFromActorSettings`)* |

#### Get Primitive Data

`UPCGGetPrimitiveSettings` · plugin `PCG`

[src] Builds a collection of primitive data from primitive components on the selected actors.

[epic] Specialization of the Get Actor Data node that returns appropriately typed and filtered Primitive data.

**Pin data types detected:** in `default` → out `Primitive`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` *(from `UPCGDataFromActorSettings`)* |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` *(from `UPCGDataFromActorSettings`)* |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` *(from `UPCGDataFromActorSettings`)* |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` *(from `UPCGDataFromActorSettings`)* |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` *(from `UPCGDataFromActorSettings`)* |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. *(from `UPCGDataFromActorSettings`)* |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. *(from `UPCGDataFromActorSettings`)* |

#### Get Segment

`UPCGGetSegmentSettings` · plugin `PCG`

[src] Gets a specific segment from the input.

[epic] Returns a segment index point or spline from a point, spline, or Polygon 2D.

**Pin data types detected:** in `Param, Point, Polygon2D, Spline` → out `Point, Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bUseInputSegmentData` | `bool` | `false` |  | Controls whether the segment index will be provided from a matching data source or use a constant. |
| `bUseInputHoleData` | `bool` | `false` |  | Controls whether the hole index will be provided from a matching data source or use a constant. |
| `bOutputSplineData` | `bool` | `false` |  | Controls whether the output is a spline or points. |
| `SegmentIndexAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Specifies the attribute from which to extract the segment index value. *Only when* `bUseInputSegmentData` |
| `SegmentIndex` | `int32` | `0` | ◆ | Specifies the segment index to extract from the input data. Supports negative indices (-1 being the last, etc.). *Only when* `!bUseInputSegmentData` |
| `HoleIndexAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Specifies the attribute from which to extract the hole index value. *Only when* `bUseInputHoleData` |
| `HoleIndex` | `int32` | `-1` | ◆ | Specifies the hole index to use for polygons in the input data. Note that -1 denotes the outer polygon. *Only when* `!bUseInputHoleData` |

#### Get Spline Control Points

`UPCGGetSplineControlPointsSettings` · plugin `PCG`

[src] Extracts the control points from the spline(s) as point data.

**Pin data types detected:** in `PolyLine` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ArriveTangentAttributeName` | `FName` | `PCGSplineSamplerConstants::ArriveTangentAttributeName` |  |  |
| `LeaveTangentAttributeName` | `FName` | `PCGSplineSamplerConstants::LeaveTangentAttributeName` |  |  |

#### Get Spline Data

`UPCGGetSplineSettings` · plugin `PCG`

[src] Builds a collection of splines from the selected actors.

[epic] Specialization of the Get Actor Data node that returns appropriately typed and filtered Spline data.

**Pin data types detected:** in `default` → out `PolyLine`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` *(from `UPCGDataFromActorSettings`)* |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` *(from `UPCGDataFromActorSettings`)* |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` *(from `UPCGDataFromActorSettings`)* |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` *(from `UPCGDataFromActorSettings`)* |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` *(from `UPCGDataFromActorSettings`)* |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. *(from `UPCGDataFromActorSettings`)* |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. *(from `UPCGDataFromActorSettings`)* |

#### Get Texture Data

`UPCGTextureSamplerSettings` · plugin `PCG`

[src] Generates points by sampling the given texture. If the texture is CPU-accessible, the sampler will prefer the CPU version of the texture. Otherwise, the texture will be read back from the GPU if one is present.

[epic] Loads a texture to a surface data. Note that this requires a GPU to execute for most compressed texture types. This supprots sampling of compressed textures, UTexture2DArrays with an index to select the desired UTexture2d, sampling CPU-avaialble Textures which can be created using the Availability property on any UTextures, and Point Fitlering instead of of only Bilinear filtering. This node also allows editor-only option to force CPU sampling. This creates a duplicate of the target texture that is CPU-visible and uncompressed and samples that instead. It avoids compression artifacts from GPU sampling.

**Pin data types detected:** in `default` → out `BaseTexture`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Transform` | `FTransform` | `FTransform::Identity` | ◆ | Surface transform |
| `bUseAbsoluteTransform` | `bool` | `false` | ◆ |  |
| `TextureArrayIndex` | `int` | `0` | ◆ | Index of texture array slice. Only used when built with editor and if the type of Texture is UTexture2DArray. |
| `bUseDensitySourceChannel` | `bool` | `true` | ◆ |  |
| `Density Source Channel` | `EPCGTextureColorChannel` | `EPCGTextureColorChannel::Alpha` | ◆ | *Options: Red · Green · Blue · Alpha* *Only when* `bUseDensitySourceChannel` |
| `Filter` | `EPCGTextureFilter` | `EPCGTextureFilter::Bilinear` | ◆ | Method used to determine the value for a sample based on the value of nearby texels. *Options: Point · Bilinear* |
| `TexelSize` | `float` | `50.0f` | ◆ | The size of one texel in cm, used when calling ToPointData. |
| `bUseAdvancedTiling` | `bool` | `false` | ◆ | Whether to tile the source or to stretch it to fit target area. |
| `Tiling` | `FVector2D` | `FVector2D(1.0, 1.0)` | ◆ | *Only when* `bUseAdvancedTiling` |
| `CenterOffset` | `FVector2D` | `FVector2D::ZeroVector` | ◆ | *Only when* `bUseAdvancedTiling` |
| `Rotation` | `float` | `0` | ◆ | Rotation to apply when sampling texture. *Only when* `bUseAdvancedTiling` |
| `bUseTileBounds` | `bool` | `false` | ◆ |  |
| `TileBoundsMin` | `FVector2D` | `FVector2D(-0.5, -0.5)` | ◆ | *Only when* `bUseAdvancedTiling && bUseTileBounds` |
| `TileBoundsMax` | `FVector2D` | `FVector2D(0.5, 0.5)` | ◆ | *Only when* `bUseAdvancedTiling && bUseTileBounds` |
| `Force Editor Only CPU Sampling` | `bool` | `false` |  | Even if the texture is not set to CPU-available, it can still be accessed from CPU memory under certain conditions (sRGB disabled, no mipmaps, and non-compressed format). Reading from CPU memory will be faster and more accurate than reading from GPU memory, since the texture will not be subject to compression or resolution clamping. Enable this flag to force a duplicate of the texture with the correct settings for CP … |
| `bSynchronousLoad` | `bool` | `false` |  | By default, texture loading is asynchronous, can force it synchronous if needed. |
| `bSkipReadbackToCPU` | `bool` | `false` |  | Skip CPU readback during initialization of the texture data. |
| `Texture` | `soft UTexture` | `nullptr` | ◆ | Texture specific parameters |

#### Get Virtual Texture Data

`UPCGGetVirtualTextureSettings` · plugin `PCG`

[src] Builds a collection of virtual texture data from the selected actors.

**Pin data types detected:** in `default` → out `VirtualTexture`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` *(from `UPCGDataFromActorSettings`)* |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` *(from `UPCGDataFromActorSettings`)* |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` *(from `UPCGDataFromActorSettings`)* |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` *(from `UPCGDataFromActorSettings`)* |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` *(from `UPCGDataFromActorSettings`)* |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. *(from `UPCGDataFromActorSettings`)* |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. *(from `UPCGDataFromActorSettings`)* |

#### Get Volume Data

`UPCGGetVolumeSettings` · plugin `PCG`

[src] Builds a collection of volumes from the selected actors. AVolume or APCGPartitionActor produce volume data. Use GetPrimitiveData for primitive components (i.e like Box, Sphere or Static Mesh collisions).

[epic] Specialization of the Get Actor Data node that returns appropriately typed and filtered Volume data.

**Pin data types detected:** in `default` → out `Volume`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` *(from `UPCGDataFromActorSettings`)* |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` *(from `UPCGDataFromActorSettings`)* |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` *(from `UPCGDataFromActorSettings`)* |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` *(from `UPCGDataFromActorSettings`)* |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` *(from `UPCGDataFromActorSettings`)* |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. *(from `UPCGDataFromActorSettings`)* |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. *(from `UPCGDataFromActorSettings`)* |

#### Get Water Spline Data  🧪 Experimental

`UPCGGetWaterSplineSettings` · plugin `PCGWaterInterop`

[src] Builds a collection of data from WaterSplineComponents on the selected actors.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ | Describes which actors to select for data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `ComponentSelector` | `FPCGComponentSelectorSettings` |  | ◆ | Describes which components to select for the data collection. *(from `UPCGDataFromActorSettings`)* |
| ↳ `ComponentSelection` | `EPCGComponentSelection` | `EPCGComponentSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowComponentSelection` |
| ↳ `ComponentSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowComponentSelection && ComponentSelection==EPCGComponentSelection::ByTag` |
| ↳ `ComponentSelectionClass` | `class UActorComponent` |  |  | Actor class to match against when filtering actors. *Only when* `bShowComponentSelection && bShowComponentSelectionClass && ComponentSelection==EPCGComponentSelection::ByClass` |
| `Mode` | `EPCGGetDataFromActorMode` | `EPCGGetDataFromActorMode::ParseActorComponents` |  | Describes what kind of data we will collect from the found actor(s). *Options: ParseActorComponents · GetSinglePoint · GetDataFromProperty · GetDataFromPCGComponent · GetDataFromPCGComponentOrParseComponents · GetActorReference · GetComponentsReference* *Only when* `DisplayModeSettings()` *(from `UPCGDataFromActorSettings`)* |
| `bIgnorePCGGeneratedComponents` | `bool` | `true` |  | Ignores any component that was spawned by PCG. *Only when* `Mode == EPCGGetDataFromActorMode::ParseActorComponents \|\| Mode == EPCGGetDataFromActorMode::GetComponentsReference` *(from `UPCGDataFromActorSettings`)* |
| `bAlsoOutputSinglePointData` | `bool` | `false` |  | Also produces a single point data at the actor location. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bComponentsMustOverlapSelf` | `bool` | `true` |  | Only get data from components which overlap with the bounds of your source component. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `bGetDataOnAllGrids` | `bool` | `true` |  | Get data from all grid sizes if there is a partitioned PCG component on the actor, instead of a specific set of grid sizes. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `AllowedGrids` | `int32` | `int32(EPCGHiGenGrid::Uninitialized)` |  | Select which grid sizes to consider when collecting data from partitioned PCG components. *Only when* `!bGetDataOnAllGrids && Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGCompon …` *(from `UPCGDataFromActorSettings`)* |
| `Merge Simple Data` | `bool` | `false` |  | Merges all the single point data outputs into a single point data. *Only when* `Mode == EPCGGetDataFromActorMode::GetSinglePoint \|\| Mode == EPCGGetDataFromActorMode::GetActorReference \|\| Mode == EPCGGetDataFromActorM …` *(from `UPCGDataFromActorSettings`)* |
| `ExpectedPins` | `TArray<FName>` |  |  | Provide pin names to match against the found component output pins. Data will automatically be wired to the expected pin if the name comparison succeeds. All unmatched pins will go into the standard out pin. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponent \|\| Mode == EPCGGetDataFromActorMode::GetDataFromPCGComponentOrParseComponents` *(from `UPCGDataFromActorSettings`)* |
| `PropertyName` | `FName` | `NAME_None` |  | The property name on the found actor to create a data collection from. *Only when* `Mode == EPCGGetDataFromActorMode::GetDataFromProperty` *(from `UPCGDataFromActorSettings`)* |
| `bAlwaysRequeryActors` | `bool` | `false` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest data from them. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceSanitizedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were sanitized to replace invalid characters. *(from `UPCGDataFromActorSettings`)* |
| `bSilenceReservedAttributeNameWarnings` | `bool` | `false` |  | Silence warnings that attribute names were rejected because they clash with reserved names. *(from `UPCGDataFromActorSettings`)* |
| `bTrackActorsOnlyWithinBounds` | `bool` | `true` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. *(from `UPCGDataFromActorSettings`)* |

#### Inner Intersection

`UPCGInnerIntersectionSettings` · plugin `PCG`

[src] Spatial data will be generated as the result of intersecting with the other source inputs sequentially or no output if such an intersection does not exist. See also: Intersection Node

[epic] Computes the inner intersection between all data provided to the node, regardless of their pins. Example: Input contains [A, B, C] Result: A ∩ B ∩ C

**Pin data types detected:** in `Spatial` → out `Spatial`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `DensityFunction` | `EPCGIntersectionDensityFunction` | `EPCGIntersectionDensityFunction::Multiply` | ◆ | *Options: Multiply · Minimum* |
| `bKeepZeroDensityPoints` | `bool` | `false` | ◆ | If enabled, output points with a density value of 0 will NOT be automatically filtered out. |

#### Intersection

`UPCGOuterIntersectionSettings` · plugin `PCG`

[src] For each given source input on the primary pin, spatial data will be generated as the result of sequentially intersecting with the other source inputs (implicitly unioned), should an intersection exist. Additional pins maybe dynamically added and for each of these, all of the inputs into the same pin will be 'unioned' together automatically. Source pins receiving no or empty data will logically return an empty output, unless the 'Ignore Empty Secondary Input' flag has been set to 'true'. See also: Inner Intersection Node, Union Node

[epic] Computes an outer intersection for each data provided in the Primary Source pin, where the result is one intersection per data on the primary source pin against the union of data on each other Source pins. Example: Primary Source contains [A, B] Source 1 contains [C, D] Source 2 contains [E]. Result: A ∩ (C ∪ D) ∩ E, B ∩ (C ∪ D) ∩ E

**Pin data types detected:** in `default` → out `Spatial`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `DensityFunction` | `EPCGIntersectionDensityFunction` | `EPCGIntersectionDensityFunction::Multiply` | ◆ | *Options: Multiply · Minimum* |
| `bIgnorePinsWithNoInput` | `bool` | `false` | ◆ | If enabled, dynamic input pins that have no incoming data will be bypassed during the intersection operation calculation, which would otherwise result in an empty result. |
| `bKeepZeroDensityPoints` | `bool` | `false` | ◆ | If enabled, output points with a density value of 0 will NOT be automatically filtered out. |

#### Make Concrete

`UPCGMakeConcreteSettings` · plugin `PCG`

[src] Concrete data is passed through (e.g. Point, Curve, Landscape). Spatial data (e.g. Intersection, Difference, Union) is collapsed to Point. Non-Spatial data (e.g. Attribute Set) is discarded.

[epic] Collapses composite data types (intersection, difference, union)into point data. For already concrete data, has no effect. This node isn’t normally used directly but is a conversion step into specific nodes.

**Pin data types detected:** in `default` → out `Concrete`

*No editable settings declared.*

#### Merge Points

`UPCGMergeSettings` · plugin `PCG`

[src] Merges multiple data sources into a single data output.

[epic] Combines multiple input point data into a single point data. Attributes are merged and non-common attributes are defaulted as needed.

**Pin data types detected:** in `default` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bMergeMetadata` | `bool` | `true` | ◆ | Controls whether the resulting merge data will have any metadata |

#### Mutate Seed

`UPCGMutateSeedSettings` · plugin `PCG`

[src] Applies a new random seed from point input.

[epic] Mutates the seed of every point in the input point data according to its position, previous seed, this node’s seed, and the component’s seed. This node is useful to separate random behavior after doing some operations that are duplicating points but might not otherwise affect the seed.

*No editable settings declared.*

#### Normal To Density  ★

`UPCGNormalToDensitySettings` · plugin `PCG`

[class] Finds the angle against the specified direction and applies that to the density

[epic] Computes point data density based on the point normal and the provided settings (Normal, Offset, Strength, Density Mode) which is similar to a dot product, with additional flexibility. This node is often used to affect in some way some of the points that are most closely aligned with a specific axis (making some trees taller) or least aligned (removing trees on steep inclines).

★ **This project:** cylinder trap — see section 8

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Normal` | `FVector` | `FVector::UpVector` | ◆ | The normal to compare against |
| `Offset` | `double` | `0.0` | ◆ | This is biases the value towards or against the normal (positive or negative) |
| `Strength` | `double` | `1.0` | ◆ | This applies a curve to scale the result density with Result = Result^(1/Strength) |
| `DensityMode` | `PCGNormalToDensityMode` | `PCGNormalToDensityMode::Set` |  | The operator to apply to the output density |

#### Offset Polygon

`UPCGOffsetPolygon2DSettings` · plugin `PCG` · internal name `OffsetPolygon2D`

[src] Offsets polygon to either make it larger or smaller, or open/close holes based on the offset quantity.

[epic] Applies an offset to a Polygon 2D shape to make it larger or smaller. Handles overlap.

**Pin data types detected:** in `Param, Polygon2D` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGPolygonOffsetOperation` | `EPCGPolygonOffsetOperation::Offset` |  | *Options: Offset · Open · Close* |
| `bInheritMetadata` | `bool` | `true` |  |  |
| `bUseOffsetFromInput` | `bool` | `false` |  |  |
| `OffsetAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `bUseOffsetFromInput` |
| `Offset` | `double` | `100.0` | ◆ | *Only when* `!bUseOffsetFromInput` |

#### Point From Mesh

`UPCGPointFromMeshSettings` · plugin `PCG`

[src] Creates a single point at the origin with an attribute named MeshPathAttributeName containing a SoftObjectPath to the StaticMesh/SkeletalMesh.

[epic] Builds a point data containing one point with the bounds of the provided static mesh and a reference to that mesh. This is useful when selection of the potential mesh is done upfront and then moving these bounds to the points (often through a partition node + Loop node + Point From Mesh combination) prior to doing intersection tests or self pruning.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mesh` | `soft UObject` |  | ◆ |  |
| `MeshPathAttributeName` | `FName` | `NAME_None` |  | Name of the string attribute to be created and hold a SoftObjectPath to the Mesh |
| `bSynchronousLoad` | `bool` | `false` |  | By default, mesh loading is asynchronous, can force it synchronous if needed. |

#### Point Neighborhood

`UPCGPointNeighborhoodSettings` · plugin `PCG`

[src] Computes quantities from nearby neighbor points, such as average density, color, and position.

[epic] Computes neighborhood-based values and sets them on the input point data, according to a search distance (in engine units). The values include distance to center, average neighborhood center, average density and average color. This node can be used to smoothen out density or values across points, which is often useful for natural procedural processes.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SearchDistance` | `double` | `500.0` | ◆ |  |
| `bSetDistanceToAttribute` | `bool` | `false` | ◆ | Allows the non-normalized distance to be output into a user-generated attribute. |
| `DistanceAttribute` | `FName` | `TEXT("Distance")` | ◆ | The output attribute name to write the non-normalized distance, if not "None". *Only when* `bSetDistanceToAttribute` |
| `bSetAveragePositionToAttribute` | `bool` | `false` | ◆ | Allows the average position to be output into a user-generated attribute. |
| `AveragePositionAttribute` | `FName` | `TEXT("AvgPosition")` | ◆ | The output attribute name to write the average positions, if not "None". *Only when* `bSetAveragePositionToAttribute` |
| `SetDensity` | `EPCGPointNeighborhoodDensityMode` | `EPCGPointNeighborhoodDensityMode::None` | ◆ | Writes either the normalized distance or the average density to the point density. *Options: None · SetNormalizedDistanceToDensity · SetAverageDensity* |
| `bSetAveragePosition` | `bool` | `false` | ◆ | Writes the average position to the point transform. |
| `bSetAverageColor` | `bool` | `false` | ◆ | Writes the target color to the point color if true, otherwise keeps the source color. |
| `bWeightedAverage` | `bool` | `false` | ◆ | Takes the bounds into account when projecting points. |

#### Polygon Operation  ★

`UPCGPolygon2DOperationSettings` · plugin `PCG` · internal name `Polygon2DOperation`

[src] Performs polygon operations between the inputs.

[epic] Polygon-to-polygon operations, including intersection, union, and difference. Additionally, a Polygon 2D can be cut using splines to subdivide or isolate a shape. For example, you could slice a larger area using spline data into a grid pattern, then use that pattern to create individual city blocks in a city generator graph.

**Pin data types detected:** in `Point, Polygon2D, Spline` → out `default`

★ **This project:** job 18b — `CutWithPaths`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGPolygonOperation` | `EPCGPolygonOperation::Intersection` |  | Controls operation to be performed on the input polygons (vs. the clip polygons). *Options: Union · Difference · Intersection · PairwiseIntersection · InnerIntersection · ExclusiveOr · CutWithPaths* |
| `MetadataMode` | `EPCGPolygonOperationMetadataMode` | `EPCGPolygonOperationMetadataMode::Full` |  | Controls whether metadata on the resulting output will be either not computed & defaulted ('None'), based on the input polygons only ('SourceOnly') or using both the source and the clip polygons. *Options: None · SourceOnly · Full* |
| `SplineMaxDiscretizationError` | `double` | `1.0` | ◆ | Maximum squared distance before we need to subdivide a segment again as part of the spline discretization to a path. * *Only when* `Operation==EPCGPolygonOperation::CutWithPaths` |
| `bQuiet` | `bool` | `false` |  | Controls whether the operation can log warnings/errors if it fails. |

#### Primitive Cross-Section  β Beta

`UPCGPrimitiveCrossSectionSettings` · plugin `PCGGeometryScriptInterop`

[src] Creates spline cross-sections of one more primitives based on vertex features.

**Pin data types detected:** in `DynamicMesh, Primitive, Volume` → out `Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SliceDirection` | `FVector` | `FVector::UpVector` | ◆ | Slicing will happen from the minimum vertex along this direction vector (normalized). |
| `ExtrusionVectorAttribute` | `FPCGAttributePropertyOutputSelector` |  | ◆ | The attribute that will be populated with each cross-section's extrusion vector. |
| `MinimumCoplanarVertices` | `int32` | `3` | ◆ | The minimum required number of vertices that must be co-planar in order to be considered a tier "feature". |
| `MaxMeshVertexCount` | `int32` | `2048` | ◆ | A safeguard to prevent finding features on an overly complex mesh. *Only when* `GenerateCrossSectionMode != EPCGGenerateCrossSectionMode::TierSlicing` |
| `bEnableTierMerging` | `bool` | `false` | ◆ | Cull tiers that are within a specified threshold. |
| `TierMergingThreshold` | `double` | `1.0` | ◆ | If a tier is within this distance (in cm) of the previous tier, it will be culled. *Only when* `bEnableTierMerging` |
| `bEnableMinAreaCulling` | `bool` | `false` | ◆ | Cull tiers that have a surface area smaller than a specified threshold. |
| `MinAreaCullingThreshold` | `double` | `100.0` | ◆ | If a tier is smaller in area than this threshold, it will be culled. *Only when* `bEnableMinAreaCulling` |
| `bEnableMinHeightCulling` | `bool` | `true` | ◆ | Culls tiers that don't meed a minimum height requirement. |
| `MinHeightCullingThreshold` | `double` | `1.0` | ◆ | If a tier is smaller in height than this threshold, it will be culled. *Only when* `bEnableMinHeightCulling` |
| `bRemoveRedundantSections` | `bool` | `true` | ◆ | If multiple tiers can be combined into a single tier without affecting the contour, remove the redundant one. Note: This will currently cull even if there are other unique tiers in between. |

#### Projection

`UPCGProjectionSettings` · plugin `PCG`

[src] Projects each of the inputs connected to In onto the Projection Target and concatenates all of the results to Out.

[epic] Creates a projection data from a source data to project onto a target. Note that if there are no special projection representations for that source data to that target data, then it converts the data to points. This node is very often used to re-project points on surfaces after some manipulation in the graph. For example, it will often follow a Copy Points node to replace the points in a proper position in their environment.

**Pin data types detected:** in `Concrete` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ProjectionParams` | `FPCGProjectionParams` |  | ◆ |  |
| ↳ `bProjectPositions` | `bool` | `true` |  | Project positions. |
| ↳ `bProjectRotations` | `bool` | `true` |  | Project rotations. |
| ↳ `bProjectScales` | `bool` | `false` |  | Project scales. |
| ↳ `ColorBlendMode` | `EPCGProjectionColorBlendMode` | `EPCGProjectionColorBlendMode::SourceValue` |  | The blend mode for colors during the projection *Options: SourceValue · TargetValue · Add · Subtract · Multiply* |
| ↳ `AttributeList` | `FString` | `TEXT("")` |  | Attributes to either explicitly exclude or include in the projection operation, depending on the Attribute Mode setting. Leave empty to gather all attributes and their values. Format is comma separated list like: Attribute1,Attribute2 . |
| ↳ `AttributeMode` | `EPCGMetadataFilterMode` | `EPCGMetadataFilterMode::ExcludeAttributes` |  | How the attribute list is used. Exclude Attributes will ignore these attributes and their values on the projection target. *Options: ExcludeAttributes · IncludeAttributes* |
| ↳ `AttributeMergeOperation` | `EPCGMetadataOp` | `EPCGMetadataOp::TargetValue` |  | Operation to use to combine attributes that reside on both source and target data. *Options: Min · Max · Sub · Add · Mul · Div · SourceValue · TargetValue* |
| ↳ `TagMergeOperation` | `EPCGProjectionTagMergeMode` | `EPCGProjectionTagMergeMode::Source` |  | Controls whether the data tags are taken from the source, the target or both. *Options: Source · Target · Both* |
| `bForceCollapseToPoint` | `bool` | `false` | ◆ | Force the result to be sampled to points, equivalent to having a To Point node after the projection node. |
| `bKeepZeroDensityPoints` | `bool` | `false` | ◆ |  |

#### Spatial Noise

`UPCGSpatialNoiseSettings` · plugin `PCG`

[class] Various fractal noises that can be used to filter points

[epic] Constructs a spatially-consistent noise pattern (such as Perlin noise) and writes it to a specified attribute. This node can be used in conjunction with the Match and Set Attributes with the input-driven weights to have spatial-noise applied to selection. In general, this node is useful to obtain more natural looking distributions.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `PCGSpatialNoiseMode` | `PCGSpatialNoiseMode::Perlin2D` | ◆ | The noise method used |
| `EdgeMask2DMode` | `PCGSpatialNoiseMask2DMode` | `PCGSpatialNoiseMask2DMode::Perlin` | ◆ | *Only when* `Mode == PCGSpatialNoiseMode::EdgeMask2D` |
| `Iterations` | `int32` | `4` | ◆ | this is how many times the fractal method recurses. A higher number will mean more detail *Only when* `Mode != PCGSpatialNoiseMode::Voronoi2D` |
| `bTiling` | `bool` | `false` | ◆ | if true, will generate results that tile along the bounding box size of the |
| `Brightness` | `float` | `0.0` | ◆ |  |
| `Contrast` | `float` | `1.0` | ◆ |  |
| `ValueTarget` | `FPCGAttributePropertyOutputNoSourceSelector` |  | ◆ | The output attribute name to write, if not 'None' |
| `RandomOffset` | `FVector` | `FVector(100000.0)` | ◆ | Adds a random amount of offset up to this amount |
| `Transform` | `FTransform` | `FTransform::Identity` | ◆ | this will apply a transform to the points before calculating noise *Only when* `Mode != PCGSpatialNoiseMode::Voronoi2D \|\| !bTiling` |
| `VoronoiCellRandomness` | `double` | `1.0` | ◆ | the less random this is, the more it returns to being a grid *Only when* `Mode == PCGSpatialNoiseMode::Voronoi2D` |
| `VoronoiCellIDTarget` | `FPCGAttributePropertyOutputNoSourceSelector` |  | ◆ | The output attribute name to write the voronoi cell id, if not 'None' *Only when* `Mode == PCGSpatialNoiseMode::Voronoi2D` |
| `bVoronoiOrientSamplesToCellEdge` | `bool` | `false` | ◆ | If true it will orient the output points to point towards the cell edges, which can be used for effects *Only when* `Mode == PCGSpatialNoiseMode::Voronoi2D` |
| `TiledVoronoiResolution` | `int32` | `8` | ◆ | The cell resolution of the tiled voronoi (across the bounds) *Only when* `Mode == PCGSpatialNoiseMode::Voronoi2D && bTiling` |
| `TiledVoronoiEdgeBlendCellCount` | `int32` | `2` | ◆ | how many cells around the edge will tile *Only when* `Mode == PCGSpatialNoiseMode::Voronoi2D && bTiling` |
| `EdgeBlendDistance` | `float` | `1.0` | ◆ | if > 0, we blend to a tiling edge value *Only when* `Mode == PCGSpatialNoiseMode::EdgeMask2D` |
| `EdgeBlendCurveOffset` | `float` | `1.0` | ◆ | Adjust the center point of the curve (where x = curve(x) crosses over) *Only when* `Mode == PCGSpatialNoiseMode::EdgeMask2D` |
| `EdgeBlendCurveIntensity` | `float` | `1.0` | ◆ | will makes the falloff harsher or softer *Only when* `Mode == PCGSpatialNoiseMode::EdgeMask2D` |

#### Spline Direction

`UPCGReverseSplineSettings` · plugin `PCG`

[class] Direct the order of a spline's control points. This can be conditional to force a given orientation (clockwise or counter clockwise).

**Pin data types detected:** in `Spline` → out `Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGReverseSplineOperation` | `EPCGReverseSplineOperation::Reverse` |  | *Options: Reverse · ForceClockwise · ForceCounterClockwise* |

#### Spline Intersection

`UPCGSplineIntersectionSettings` · plugin `PCG`

[class] Intersects splines against other splines (or themselves) and returns varied results based on user need.

[epic] Finds intersecting splines in 3D and adds control points at each intersection, or returns the intersections points.

**Pin data types detected:** in `Spline` → out `Point, Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Type` | `EPCGSplineIntersectionType` | `EPCGSplineIntersectionType::AgainstOtherSplines` |  | Controls type of intersection test that will be done. *Options: AgainstOtherSplines* |
| `Output` | `EPCGSplineIntersectionOutput` | `EPCGSplineIntersectionOutput::OriginalSplinesWithIntersectio …` |  | Controls type of output result. *Options: IntersectionPointsOnly · OriginalSplinesWithIntersections* |
| `bOutputSplineIndices` | `bool` | `false` |  | Controls whether the output will contain the index of the intersecting splines *Only when* `Type!=EPCGSplineIntersectionType::Self` |
| `OriginatingSplineIndexAttribute` | `FPCGAttributePropertyOutputSelector` |  | ◆ | Attribute that will contain the first spline index (only in the output case of intersection points.) *Only when* `bOutputSplineIndices && Type!=EPCGSplineIntersectionType::Self && Output==EPCGSplineIntersectionOutput::IntersectionPointsOnly` |
| `IntersectingSplineIndexAttribute` | `FPCGAttributePropertyOutputSelector` |  | ◆ | Attribute that will contain the first intersecting spline index, or -1 if not an intersection control point. *Only when* `bOutputSplineIndices` |
| `DistanceThreshold` | `double` | `10.0` | ◆ | Maximum distance at which we report an intersection on the splines. |

#### Spline to Segment

`UPCGSplineToSegmentSettings` · plugin `PCG`

[src] Take a spline as input and create a point data, with each point being a segment defined by 2 connected control points. The point position will be in the middle of those 2 control points, and the extents of the point will be half the difference between those 2 control points.

**Pin data types detected:** in `Spline` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bExtractTangents` | `bool` | `false` |  | Can extract the tangents with previous segment and next segment. |
| `bExtractAngles` | `bool` | `true` |  | Can extract the angle with previous tangent and next tangent. Will be 0 at the extremity for non-closed splines. |
| `bExtractConnectivityInfo` | `bool` | `true` |  | Can set the index of the previous and next segment (to keep information on connectivity). |
| `bExtractClockwiseInfo` | `bool` | `true` |  | Can output a global attribute to know if the spline points order is clockwise or counterclockwise. (Only for closed loops). |

#### Split Spline

`UPCGSplitSplinesSettings` · plugin `PCG`

[class] Splits spline at a specific distance(s), key(s) or at certain values.

**Pin data types detected:** in `Param, Spline` → out `Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `EPCGSplitSplineMode` | `EPCGSplitSplineMode::ByAlpha` |  | Split criteria. *Options: ByKey · ByDistance · ByAlpha · ByPredicateOnControlPoints* |
| `bUseConstant` | `bool` | `true` |  | Controls whether the input splines will be cut using a single constant or values driven either by an additional input or based on a predicate on the spline control points. *Only when* `Mode != EPCGSplitSplineMode::ByPredicateOnControlPoints` |
| `Constant` | `double` | `0.5` | ◆ | Constant (either Key, Distance or Alpha) that will be used to split the splines. *Only when* `bUseConstant && Mode != EPCGSplitSplineMode::ByPredicateOnControlPoints` |
| `Attribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute identifying either the provenance of the split constants (key, distance or alpha) or the predicate on the control points. *Only when* `!bUseConstant \|\| Mode == EPCGSplitSplineMode::ByPredicateOnControlPoints` |
| `bShouldOutputOriginatingSplineIndex` | `bool` | `true` | ◆ | Controls whether the output spline will have an attribute containing the index of the originating spline. |
| `OutputOriginatingSplineIndex` | `FPCGAttributePropertyOutputSelector` |  | ◆ | Attribute to write the originating spline index to. *Only when* `bShouldOutputOriginatingSplineIndex` |

#### Subdivide Segment

`UPCGSubdivideSegmentSettings` · plugin `PCG`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

**Pin data types detected:** in `Param, Point` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SubdivisionAxis` | `EPCGSplitAxis` | `EPCGSplitAxis::X` |  | Subdivision direction in point local space. *Options: X · Y · Z* |
| `bFlipAxisAsAttribute` | `bool` | `false` |  | Use an attribute to determine whether we should flip axis. |
| `bShouldFlipAxis` | `bool` | `false` | ◆ | If we need to flip axis. *Only when* `!bFlipAxisAsAttribute` |
| `FlipAxisAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Name of the attribute to know if we need to flip axis. *Only when* `bFlipAxisAsAttribute` |
| `bAcceptIncompleteSubdivision` | `bool` | `false` | ◆ | If the subdivision with a given grammar doesn't fill the entire segment, setting it to true makes it a valid case. |
| `bOutputModuleIndexAttribute` | `bool` | `false` | ◆ |  |
| `ModuleIndexAttributeName` | `FName` | `TEXT("ModuleIndex")` | ◆ | Name of the module index output attribute name. *Only when* `bOutputModuleIndexAttribute` |
| `bOutputExtremityAttributes` | `bool` | `false` | ◆ | Output attributes labeling the first and final points after subdivision. |
| `IsFirstAttributeName` | `FName` | `TEXT("IsFirst")` | ◆ | Name of the attribute labeling the first output point from the first module. *Only when* `bOutputExtremityAttributes` |
| `IsFinalAttributeName` | `FName` | `TEXT("IsFinal")` | ◆ | Name of the attribute labeling the final output point from the final module. *Only when* `bOutputExtremityAttributes` |
| `bOutputExtremityNeighborIndexAttribute` | `bool` | `false` | ◆ |  |
| `ExtremityNeighborIndexAttributeName` | `FName` | `TEXT("ExtremityNeighborIndex")` | ◆ | Name of the extremity neighbor index output attribute name. *Only when* `bOutputExtremityNeighborIndexAttribute` |
| `bModuleInfoAsInput` | `bool` | `false` |  | Set it to true to pass the info as attribute set. *(from `UPCGSubdivisionBaseSettings`)* |
| `ModulesInfo` | `TArray<FPCGSubdivisionSubmodule>` |  |  | Fixed array of modules used for the subdivision. *Only when* `!bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| `Attribute Names for Module Info` | `FPCGSubdivisionModuleAttributeNames` |  |  | Fixed array of modules used for the subdivision. *Only when* `bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| ↳ `SymbolAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SymbolAttributeName` |  | Mandatory. Expected type: FName. |
| ↳ `SizeAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SizeAttributeName` |  | Mandatory. Expected type: double. |
| ↳ `bProvideScalable` | `bool` | `false` |  |  |
| ↳ `ScalableAttributeName` | `FName` | `PCGSubdivisionBase::Constants::ScalableAttributeName` |  | Optional. Expected type: bool. If disabled, default value will be false. *Only when* `bProvideScalable` |
| ↳ `bProvideDebugColor` | `bool` | `false` |  |  |
| ↳ `DebugColorAttributeName` | `FName` | `PCGSubdivisionBase::Constants::DebugColorAttributeName` |  | Optional. Expected type: Vector4. If disabled, default value will be (1.0, 1.0, 1.0, 1.0). *Only when* `bProvideDebugColor` |
| `GrammarSelection` | `FPCGGrammarSelection` |  | ◆ | An encoded string that represents how to apply a set of rules to a series of defined modules. *(from `UPCGSubdivisionBaseSettings`)* |
| ↳ `bGrammarAsAttribute` | `bool` | `false` | ◆ | Read the grammar as an attribute rather than directly from the settings. Grammar syntax: - Each symbol can have multiple characters - Modules are defined in '[]', multiple symbols in a module are separated with ',' - Modules can be repeated a fixed number of times, by adding a number after it (like [A,B]3 will produce ABABAB) - Modules can be marked repeated an indefinite number of times, with '*'. (like [A,B]* will … |
| ↳ `GrammarString` | `FString` |  | ◆ | An encoded string that represents how to apply a set of rules to a series of defined modules. *Only when* `!bGrammarAsAttribute` |
| ↳ `GrammarAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to be taken from the input spline containing the grammar to use. *Only when* `bGrammarAsAttribute` |
| `bUseSeedAttribute` | `bool` | `false` | ◆ | Controls whether we'll use an attribute to drive random seeding for stochastic processes in the subdivision. *(from `UPCGSubdivisionBaseSettings`)* |
| `SeedAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to use to drive seed selection. It should be convertible to an integer. *Only when* `bUseSeedAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bForwardAttributesFromModulesInfo` | `bool` | `false` | ◆ | Do a match and set with the incoming modules info, only if the modules info is passed as input. *Only when* `bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| `SymbolAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SymbolAttributeName` | ◆ | Name of the Symbol output attribute name. *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputSizeAttribute` | `bool` | `true` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `SizeAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SizeAttributeName` | ◆ | Name of the Size output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputSizeAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputScalableAttribute` | `bool` | `true` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `ScalableAttributeName` | `FName` | `PCGSubdivisionBase::Constants::ScalableAttributeName` | ◆ | Name of the Scalable output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputScalableAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputDebugColorAttribute` | `bool` | `false` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `DebugColorAttributeName` | `FName` | `PCGSubdivisionBase::Constants::DebugColorAttributeName` | ◆ | Name of the Debug Color output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputDebugColorAttribute` *(from `UPCGSubdivisionBaseSettings`)* |

#### Subdivide Spline

`UPCGSubdivideSplineSettings` · plugin `PCG`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

**Pin data types detected:** in `Param, PolyLine` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bAcceptIncompleteSubdivision` | `bool` | `false` | ◆ | If the subdivision with a given grammar doesn't fill the entire spline, setting it to true makes it a valid case. |
| `bModuleHeightAsAttribute` | `bool` | `false` |  | Select the module height from an attribute. |
| `ModuleHeight` | `double` | `100.0` |  | The height of each placed module. *Only when* `!bModuleHeightAsAttribute` |
| `ModuleHeightAttribute` | `FPCGAttributePropertyInputSelector` |  |  | Selection will be used as the module height for placed modules. *Only when* `bModuleHeightAsAttribute` |
| `bOutputModuleIndexAttribute` | `bool` | `false` | ◆ |  |
| `ModuleIndexAttributeName` | `FName` | `TEXT("ModuleIndex")` | ◆ | Name of the module index output attribute name. *Only when* `bOutputModuleIndexAttribute` |
| `bOutputExtremityAttributes` | `bool` | `false` | ◆ | Output attributes labeling the first and final points after subdivision. |
| `IsFirstAttributeName` | `FName` | `TEXT("IsFirst")` | ◆ | Name of the attribute labeling the first output point from the first module. *Only when* `bOutputExtremityAttributes` |
| `IsFinalAttributeName` | `FName` | `TEXT("IsFinal")` | ◆ | Name of the attribute labeling the final output point from the final module. *Only when* `bOutputExtremityAttributes` |
| `ModulePlacementTolerance` | `double` | `0.01` | ◆ | Maximum acceptable distance tolerance between placed modules (overlap or gap) - a smaller number is more precise. Affects performance if the number is very small. |
| `bModuleInfoAsInput` | `bool` | `false` |  | Set it to true to pass the info as attribute set. *(from `UPCGSubdivisionBaseSettings`)* |
| `ModulesInfo` | `TArray<FPCGSubdivisionSubmodule>` |  |  | Fixed array of modules used for the subdivision. *Only when* `!bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| `Attribute Names for Module Info` | `FPCGSubdivisionModuleAttributeNames` |  |  | Fixed array of modules used for the subdivision. *Only when* `bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| ↳ `SymbolAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SymbolAttributeName` |  | Mandatory. Expected type: FName. |
| ↳ `SizeAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SizeAttributeName` |  | Mandatory. Expected type: double. |
| ↳ `bProvideScalable` | `bool` | `false` |  |  |
| ↳ `ScalableAttributeName` | `FName` | `PCGSubdivisionBase::Constants::ScalableAttributeName` |  | Optional. Expected type: bool. If disabled, default value will be false. *Only when* `bProvideScalable` |
| ↳ `bProvideDebugColor` | `bool` | `false` |  |  |
| ↳ `DebugColorAttributeName` | `FName` | `PCGSubdivisionBase::Constants::DebugColorAttributeName` |  | Optional. Expected type: Vector4. If disabled, default value will be (1.0, 1.0, 1.0, 1.0). *Only when* `bProvideDebugColor` |
| `GrammarSelection` | `FPCGGrammarSelection` |  | ◆ | An encoded string that represents how to apply a set of rules to a series of defined modules. *(from `UPCGSubdivisionBaseSettings`)* |
| ↳ `bGrammarAsAttribute` | `bool` | `false` | ◆ | Read the grammar as an attribute rather than directly from the settings. Grammar syntax: - Each symbol can have multiple characters - Modules are defined in '[]', multiple symbols in a module are separated with ',' - Modules can be repeated a fixed number of times, by adding a number after it (like [A,B]3 will produce ABABAB) - Modules can be marked repeated an indefinite number of times, with '*'. (like [A,B]* will … |
| ↳ `GrammarString` | `FString` |  | ◆ | An encoded string that represents how to apply a set of rules to a series of defined modules. *Only when* `!bGrammarAsAttribute` |
| ↳ `GrammarAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to be taken from the input spline containing the grammar to use. *Only when* `bGrammarAsAttribute` |
| `bUseSeedAttribute` | `bool` | `false` | ◆ | Controls whether we'll use an attribute to drive random seeding for stochastic processes in the subdivision. *(from `UPCGSubdivisionBaseSettings`)* |
| `SeedAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to use to drive seed selection. It should be convertible to an integer. *Only when* `bUseSeedAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bForwardAttributesFromModulesInfo` | `bool` | `false` | ◆ | Do a match and set with the incoming modules info, only if the modules info is passed as input. *Only when* `bModuleInfoAsInput` *(from `UPCGSubdivisionBaseSettings`)* |
| `SymbolAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SymbolAttributeName` | ◆ | Name of the Symbol output attribute name. *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputSizeAttribute` | `bool` | `true` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `SizeAttributeName` | `FName` | `PCGSubdivisionBase::Constants::SizeAttributeName` | ◆ | Name of the Size output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputSizeAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputScalableAttribute` | `bool` | `true` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `ScalableAttributeName` | `FName` | `PCGSubdivisionBase::Constants::ScalableAttributeName` | ◆ | Name of the Scalable output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputScalableAttribute` *(from `UPCGSubdivisionBaseSettings`)* |
| `bOutputDebugColorAttribute` | `bool` | `false` | ◆ | *(from `UPCGSubdivisionBaseSettings`)* |
| `DebugColorAttributeName` | `FName` | `PCGSubdivisionBase::Constants::DebugColorAttributeName` | ◆ | Name of the Debug Color output attribute name, ignored if Forward Attributes From Modules Info is true. *Only when* `bOutputDebugColorAttribute` *(from `UPCGSubdivisionBaseSettings`)* |

#### To Point

`UPCGCollapseSettings` · plugin `PCG`

[class] Convert input to point data, performing sampling with default settings if necessary

[epic] Casts the data to a point data if it is already one or discretizes the spatial data to point data.

**Pin data types detected:** in `Spatial` → out `default`

*No editable settings declared.*

#### Union

`UPCGUnionSettings` · plugin `PCG`

[src] Combine spatial data into a union of all inputs. Order of inputs is respected, beginning with the dynamic pin inputs.

[epic] Creates a logical union between data, from a distribution function perspective. Result depends on the density function option chosen. Density Function: Controls which density function is used after the operation is complete. Contains the following options: Maximum: Final density is equal to the max density of the source. Clamped Addition: Final density is equal to the sum of the densities in all the differences. This value is clamped between 0 and 1. Binary: Final density is equal to 1 if any density of the source is greater than zero. Note that this is rarely useful except in the context of a binary difference.

**Pin data types detected:** in `default` → out `Spatial`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Type` | `EPCGUnionType` | `EPCGUnionType::LeftToRightPriority` | ◆ | WITH_EDITOR ~End UPCGSettingsWithDynamicInputs interface *Options: LeftToRightPriority · RightToLeftPriority · KeepAll* |
| `DensityFunction` | `EPCGUnionDensityFunction` | `EPCGUnionDensityFunction::Maximum` | ◆ | *Options: Maximum · ClampedAddition · Binary* |

#### World Ray Hit Query

`UPCGWorldRayHitSettings` · plugin `PCG`

[src] Allows generic access (based on raycasts) to collisions in the world that behaves like a surface.

[epic] Creates a surface-like data that performs ray casts in the physics world. It can pass data to any node that expects a surface data. By default, the size and orientation of the rays is driven by the source component's actor properties (most likely a volume), but the ray properties can be overridden. It contains the following options: Apply Metadata From Landscape: Gets the landscape layer values if the raycast hits the landscape. Note that there is a small performance cost involved with this. Ignore PCG Hits: Ignores all PCG generated assets. Is useful when there is no ordering enforced vs other nodes creating data in the world (or other graphs). Optionally, can return the physical material and the actor hit. The Filtering elements are used for finer-grained control to ignore or keep only some of the hits.

**Pin data types detected:** in `default` → out `Surface`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `CollisionShape` | `FPCGCollisionShape` |  | ◆ | Parameters for either using a line trace or specifying a collision shape for a sweep. |
| ↳ `ShapeType` | `EPCGCollisionShapeType` | `EPCGCollisionShapeType::Line` | ◆ | Shape that will be used in the collision detection. *Options: Line · Box · Sphere · Capsule* |
| ↳ `Half Extent (Box)` | `FVector` | `FVector::OneVector` | ◆ | Half the size of the sweep box's X, Y, Z components in world space. *Only when* `ShapeType == EPCGCollisionShapeType::Box` |
| ↳ `Radius (Sphere)` | `float` | `100.f` | ◆ | Radius of the sweep's sphere in world space. *Only when* `ShapeType == EPCGCollisionShapeType::Sphere` |
| ↳ `Radius (Capsule)` | `float` | `100.f` | ◆ | Radius of the spherical shape of the sweep's capsule in world space. *Only when* `ShapeType == EPCGCollisionShapeType::Capsule` |
| ↳ `Half Height (Capsule)` | `float` | `100.f` | ◆ | Half the length of the sweep's capsule in world space. *Only when* `ShapeType == EPCGCollisionShapeType::Capsule` |
| ↳ `ShapeRotation` | `FRotator` | `FRotator::ZeroRotator` | ◆ | World space rotation applied to the collision shape prior to the sweep. *Only when* `ShapeType != EPCGCollisionShapeType::Line` |
| `QueryParams` | `FPCGWorldRayHitQueryParams` |  | ◆ |  |

#### World Raycast

`UPCGWorldRaycastElementSettings` · plugin `PCG`

[src] Casts a line trace or collision shape sweep from provided points along a given direction returning the location of the impact.

**Pin data types detected:** in `PointOrParam, Spatial` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `CollisionShape` | `FPCGCollisionShape` |  | ◆ | Parameters for either using a line trace or specifying a collision shape. |
| ↳ `ShapeType` | `EPCGCollisionShapeType` | `EPCGCollisionShapeType::Line` | ◆ | Shape that will be used in the collision detection. *Options: Line · Box · Sphere · Capsule* |
| ↳ `Half Extent (Box)` | `FVector` | `FVector::OneVector` | ◆ | Half the size of the sweep box's X, Y, Z components in world space. *Only when* `ShapeType == EPCGCollisionShapeType::Box` |
| ↳ `Radius (Sphere)` | `float` | `100.f` | ◆ | Radius of the sweep's sphere in world space. *Only when* `ShapeType == EPCGCollisionShapeType::Sphere` |
| ↳ `Radius (Capsule)` | `float` | `100.f` | ◆ | Radius of the spherical shape of the sweep's capsule in world space. *Only when* `ShapeType == EPCGCollisionShapeType::Capsule` |
| ↳ `Half Height (Capsule)` | `float` | `100.f` | ◆ | Half the length of the sweep's capsule in world space. *Only when* `ShapeType == EPCGCollisionShapeType::Capsule` |
| ↳ `ShapeRotation` | `FRotator` | `FRotator::ZeroRotator` | ◆ | World space rotation applied to the collision shape prior to the sweep. *Only when* `ShapeType != EPCGCollisionShapeType::Line` |
| `RaycastMode` | `EPCGWorldRaycastMode` | `EPCGWorldRaycastMode::Infinite` |  | Determines how the ray's direction and distance will be calculated. *Options: Infinite · ScaledVector · NormalizedWithLength · Segments* |
| `OriginInputAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | The selected attribute determines the ray origin. |
| `bOverrideRayDirections` | `bool` | `false` | ◆ | Use a selected attribute as the ray direction. *Only when* `RaycastMode != EPCGWorldRaycastMode::Segments` |
| `RayDirection` | `FVector` | `-FVector::UnitZ()` | ◆ | A ray direction that will be used for all raycasts. *Only when* `RaycastMode != EPCGWorldRaycastMode::Segments && !bOverrideRayDirections` |
| `RayDirectionAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | The selected attribute determines the ray direction. *Only when* `RaycastMode != EPCGWorldRaycastMode::Segments && bOverrideRayDirections` |
| `EndPointAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | The selected attribute determines the ray terminal point. *Only when* `RaycastMode == EPCGWorldRaycastMode::Segments` |
| `bOverrideRayLengths` | `bool` | `false` | ◆ | Use a selected attribute as the ray length. *Only when* `RaycastMode == EPCGWorldRaycastMode::NormalizedWithLength` |
| `RayLength` | `double` | `100000.0` | ◆ | A ray length that will be used for all raycasts. *Only when* `RaycastMode == EPCGWorldRaycastMode::NormalizedWithLength && !bOverrideRayLengths` |
| `RayLengthAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | The selected attribute determines the ray length. *Only when* `RaycastMode == EPCGWorldRaycastMode::NormalizedWithLength && bOverrideRayLengths` |
| `WorldQueryParams` | `FPCGWorldRaycastQueryParams` |  | ◆ | World ray trace parameters. |
| `bKeepOriginalPointOnMiss` | `bool` | `false` | ◆ | Will keep the original points at their location if the raycast misses or if the hit result is out of bounds. |
| `bUnbounded` | `bool` | `false` | ◆ | If no Bounding Shape input is provided, the actor bounds are used to limit the sample generation domain. |

#### World Volumetric Query

`UPCGWorldQuerySettings` · plugin `PCG`

[src] Allows generic access (based on overlaps) to collisions in the world that behaves like a volume.

[epic] Creates a volume-like data that gathers points from the physics world. It can pass data to any node that expects a surface data. The Search for overlap check controls whether overlaps are returned as points or only queries overlapping nothing (subject to filtering) are returned. Can also optionally return the actor "found" in that volume.

**Pin data types detected:** in `default` → out `Volume`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `QueryParams` | `FPCGWorldVolumetricQueryParams` |  | ◆ |  |
| ↳ `bIgnorePCGHits` | `bool` | `false` | ◆ | If true, will ignore hits/overlaps on content created from PCG. |
| ↳ `bIgnoreSelfHits` | `bool` | `true` | ◆ |  |
| ↳ `CollisionChannel` | `TEnumAsByte<ECollisionChannel>` | `ECC_WorldStatic` | ◆ |  |
| ↳ `bTraceComplex` | `bool` | `false` | ◆ | Queries against complex collision if enabled, performance warning |
| ↳ `ActorTagFilter` | `EPCGWorldQueryFilter` | `EPCGWorldQueryFilter::None` | ◆ | *Options: None · Include · Exclude · Require* |
| ↳ `ActorTagsList` | `FString` |  | ◆ | *Only when* `ActorTagFilter != EPCGWorldQueryFilter::None` |
| ↳ `ActorClassFilter` | `EPCGWorldQueryFilter` | `EPCGWorldQueryFilter::None` | ◆ | *Options: None · Include · Exclude · Require* |
| ↳ `ActorClass` | `class AActor` |  | ◆ | *Only when* `ActorClassFilter != EPCGWorldQueryFilter::None` |
| ↳ `ActorFilterFromInput` | `EPCGWorldQueryFilter` | `EPCGWorldQueryFilter::None` | ◆ | Will add an input pin to pass a list of actor references for filtering if this value is not set to None. *Options: None · Include · Exclude · Require* |
| ↳ `ActorFilterInputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | Input source for the attribute to read from the Filter Actor pin. *Only when* `ActorFilterFromInput != EPCGWorldQueryFilter::None` |
| ↳ `SelectLandscapeHits` | `EPCGWorldQuerySelectLandscapeHits` | `EPCGWorldQuerySelectLandscapeHits::Include` | ◆ | *Options: Exclude · Include · Require* |
| ↳ `bGetReferenceToActorHit` | `bool` | `false` | ◆ |  |
| ↳ `bGetReferenceToPhysicalMaterial` | `bool` | `false` | ◆ |  |
| ↳ `bSearchForOverlap` | `bool` | `true` | ◆ | Controls whether we are trying to find an overlap with physical objects (true) or to find empty spaces that do not contain anything (false) |

### ▸ Point Ops

#### Apply Hierarchy

`UPCGApplyHierarchySettings` · plugin `PCG`

[class] Applies hierarchy transformations based on a hierarchy depth, point index & parent index scheme. This is used in the context of PCG Data Assets that have these fields by default.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PointKeyAttributes` | `TArray<FPCGAttributePropertyInputSelector>` |  | ◆ | Attributes that constitute a unique key representing the point. All attributes must be int32 at this time. |
| `ParentKeyAttributes` | `TArray<FPCGAttributePropertyInputSelector>` |  | ◆ | Attributes that constitute a unique key representing the point's parent in the hierarchy. All attributes must be int32 at this time. |
| `HierarchyDepthAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `RelativeTransformAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `ApplyParentRotation` | `EPCGApplyHierarchyOption` |  | ◆ | *Options: Always · Never · OptInByAttribute · OptOutByAttribute* |
| `ApplyParentRotationAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `ApplyParentRotation==EPCGApplyHierarchyOption::OptInByAttribute\|\|ApplyParentRotation==EPCGApplyHierarchyOption::OptOutByAttribute` |
| `ApplyParentScale` | `EPCGApplyHierarchyOption` |  | ◆ | *Options: Always · Never · OptInByAttribute · OptOutByAttribute* |
| `ApplyParentScaleAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `ApplyParentScale==EPCGApplyHierarchyOption::OptInByAttribute\|\|ApplyParentScale==EPCGApplyHierarchyOption::OptOutByAttribute` |
| `ApplyHierarchy` | `EPCGApplyHierarchyOption` |  | ◆ | *Options: Always · Never · OptInByAttribute · OptOutByAttribute* |
| `ApplyHierarchyAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `ApplyHierarchy==EPCGApplyHierarchyOption::OptInByAttribute\|\|ApplyHierarchy==EPCGApplyHierarchyOption::OptOutByAttribute` |
| `bWarnOnPointsWithInvalidParent` | `bool` | `true` | ◆ |  |

#### Apply Scale To Bounds

`UPCGApplyScaleToBoundsSettings` · plugin `PCG`

[src] Applies the scale of each point to its bounds and resets the scale.

[epic] For each point in the input Point Data(s), the bounds min and max is multiplied by their scale and the scale will be reset to 1, but preserving negative values.

*No editable settings declared.*

#### Attract

`UPCGAttractSettings` · plugin `PCG` · internal name `AttractElement`

[src] Attracts source points to target points based on a max distance and a criteria.

**Pin data types detected:** in `Point` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `EPCGAttractMode` | `EPCGAttractMode::Closest` | ◆ | Controls the criteria used for the attract operation. *Options: Closest · MinAttribute · MaxAttribute · FromIndex* |
| `AttractorIndexAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Index attribute on the source that maps a point to a point from the target. *Only when* `Mode == EPCGAttractMode::FromIndex` |
| `Distance` | `double` | `100.0` | ◆ | Will be used to determine which points to attract. *Only when* `Mode != EPCGAttractMode::FromIndex` |
| `bRemoveUnattractedPoints` | `bool` | `false` | ◆ | Can optionally remove points that weren't attracted to points on the target. Will have no effect when the source is the target. |
| `TargetAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | The target attribute used when attracted by attribute value. *Only when* `Mode == EPCGAttractMode::MinAttribute \|\| Mode == EPCGAttractMode::MaxAttribute` |
| `bUseSourceWeight` | `bool` | `false` | ◆ |  |
| `SourceWeightAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | This attribute will determine the weight of the fusion result for the source point. It will be normalized to the range of [0..1]. *Only when* `bUseSourceWeight` |
| `bUseTargetWeight` | `bool` | `false` | ◆ |  |
| `TargetWeightAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | This attribute will determine the weight of the fusion result for the target point. It will be normalized to the range of [0..1]. *Only when* `bUseTargetWeight` |
| `Weight` | `double` | `1.0` | ◆ | *Only when* `!bUseSourceWeight && !bUseTargetWeight` |
| `SourceAndTargetAttributeMapping` | `TMap<FPCGAttributePropertyInputSelector, FPCGAttributePropertyInputSel …` |  |  |  |
| `bOutputAttractIndex` | `bool` | `false` | ◆ |  |
| `OutputAttractIndexAttribute` | `FPCGAttributePropertyOutputNoSourceSelector` |  | ◆ | *Only when* `bOutputAttractIndex` |

#### Blur

`UPCGBlurSettings` · plugin `PCG` · internal name `BlurElement`

[class] Select an attribute on a point data and blur it using the values from neighbors within some distance, center to center, and can be done over multiple iterations.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to use as a base value. Needs to be numerical. |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | Attribute where the result will be written. |
| `NumIterations` | `int` | `1` | ◆ | Number of iterations to apply the blur. |
| `SearchDistance` | `double` | `1000.0` | ◆ | Radius for search. |
| `BlurMode` | `EPCGBlurElementMode` | `EPCGBlurElementMode::Constant` | ◆ | *Options: which · N · Linear · Gaussian* |
| `bUseCustomStandardDeviation` | `bool` | `false` | ◆ | By default, the standard deviation will be SearchDistance / 3, so that at search distance from the point it corresponds to 3 std deviation. *Only when* `BlurMode == EPCGBlurElementMode::Gaussian` |
| `CustomStandardDeviation` | `double` | `1.0` | ◆ | *Only when* `BlurMode == EPCGBlurElementMode::Gaussian && bUseCustomStandardDeviation` |

#### Bounds Modifier

`UPCGBoundsModifierSettings` · plugin `PCG`

[src] Applies a transformation on the point bounds & optionally its steepness.

[epic] Modifies the bounds property on points in the provided point data. This node is used to affect the bounds in the input Point Data in a simple way, which might be useful prior to a Self Pruning node or Intersections or Differences for example to tweak the final result.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `EPCGBoundsModifierMode` | `EPCGBoundsModifierMode::Scale` | ◆ | *Options: Set · Intersect · Include · Translate · Scale* |
| `BoundsMin` | `FVector` | `FVector::One()` | ◆ |  |
| `BoundsMax` | `FVector` | `FVector::One()` | ◆ |  |
| `bAffectSteepness` | `bool` | `false` | ◆ |  |
| `Steepness` | `float` | `1.0f` | ◆ | *Only when* `bAffectSteepness` |

#### Cluster

`UPCGClusterSettings` · plugin `PCG` · internal name `ClusterElement`

[src] Given a desired number of clusters (categories), find the best fit cluster for each point by distance, using one of various clustering algorithms.

**Pin data types detected:** in `Point` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Algorithm` | `EPCGClusterAlgorithm` | `EPCGClusterAlgorithm::KMeans` | ◆ | Mathematical algorithm for selecting clusters. *Options: KMeans · EM* |
| `Clusters` | `int32` | `3` | ◆ | Number of clusters (segments) to group the points into. Each point will be assigned a cluster at the end. |
| `ClusterAttribute` | `FPCGAttributePropertyOutputNoSourceSelector` |  | ◆ | Cluster IDs will be written to this attribute on the main output. |
| `MaxIterations` | `int32` | `100` | ◆ | A limit on the number of iterations to run on each algorithm, if it doesn't otherwise converge. A higher number can offer more accuracy at the cost of processing time. |
| `Tolerance` | `double` | `UE_DOUBLE_KINDA_SMALL_NUMBER` | ◆ | For EM, the maximum allowed difference between the last two iterations' "Log Likelihood"--which converges from positive infinity to 0 in relation to point-to-cluster probabilities. It is exponential, so raising this number can offer faster iteration if exact precision isn't needed. *Only when* `Algorithm == EPCGClusterAlgorithm::EM` |
| `bOutputFinalCentroids` | `bool` | `false` |  | Output the final location of the centroids or gaussians. |
| `bOutputFinalCentroidElementCount` | `bool` | `false` | ◆ | Output the element count for each of the final centroids. *Only when* `bOutputFinalCentroids` |
| `FinalCentroidElementCountAttribute` | `FPCGAttributePropertyOutputNoSourceSelector` |  | ◆ | Final centroid element count will be written to this attribute on the Final Centroid output. *Only when* `bOutputFinalCentroidElementCount` |

#### Collapse Points

`UPCGCollapsePointsSettings` · plugin `PCG`

[src] Collapses points with their closest neighbors until all points are farther than the search distance.

**Pin data types detected:** in `Point` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `DistanceThreshold` | `double` | `100.0` | ◆ | Distance at which we will stop collapsing points. E.g. Points will continue collapsing until every point is at least this distance from each other. |
| `Mode` | `EPCGCollapseMode` | `EPCGCollapseMode::PairwiseClosest` | ◆ | *Options: PairwiseClosest* |
| `ComparisonMode` | `EPCGCollapseComparisonMode` | `EPCGCollapseComparisonMode::Position` | ◆ | *Options: Position · Center* |
| `VisitOrder` | `EPCGCollapseVisitOrder` | `EPCGCollapseVisitOrder::Ordered` | ◆ | Determines order in which we will collapse points pair-wise. *Options: Ordered · Random · MinAttribute · MaxAttribute* *Only when* `Mode == EPCGCollapseMode::PairwiseClosest` |
| `VisitOrderAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to drive visit order. *Only when* `Mode == EPCGCollapseMode::PairwiseClosest && (VisitOrder == EPCGCollapseVisitOrder::MinAttribute \|\| VisitOrder == EPCGCollapseVisitOrder:: …` |
| `bUseMergeWeightAttribute` | `bool` | `false` | ◆ | Controls whether input points will use a weight driven by an attribute |
| `MergeWeightAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute that will drive relative weight when merging points (only in the Weighted mode). *Only when* `bUseMergeWeightAttribute` |
| `AttributesToMerge` | `TArray<FPCGAttributePropertyOutputNoSourceSelector>` |  |  | List of attributes to merge on the final points, based on the weights. |

#### Combine Points

`UPCGCombinePointsSettings` · plugin `PCG`

[src] Combines each point to share a singular bound extent.

[epic] For each input Point Data, outputs a new Point Data containing a single point that encompasses all points in its respective Point Data. This allows recomputing Point Data and setting a specific transform. This node is used as an optimization or higherlevel view on some data in some instances.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bCenterPivot` | `bool` | `true` | ◆ | Places the point at the center of the combined bounds. |
| `bUseFirstPointTransform` | `bool` | `true` | ◆ | Use the transform of the initial point. |
| `PointTransform` | `FTransform` | `FTransform()` | ◆ | Transform the point and adjust the bounds. *Only when* `!bUseFirstPointTransform` |

#### Duplicate Point

`UPCGDuplicatePointSettings` · plugin `PCG`

[src] Creates duplicates of each point with optional transform offsets.

[epic] For each point, duplicate the point and move it along an axis defined by the Direction, and apply a transform on the new point. Repeat the process the number of times Iterations indicates. If "Direction applied in relative space" is selected, the axis of displacement is picked from the new point iteratively. This node is used to lay down a lot of points quickly, and to build fractal-like patterns.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Iterations` | `int` | `1` | ◆ | Number of duplicates to produce. |
| `Direction` | `FVector` | `FVector(0.0, 0.0, 1.0)` | ◆ | Direction to stack point duplicates. |
| `bDirectionAppliedInRelativeSpace` | `bool` | `false` | ◆ | Controls whether the axis displacement will be made in relative space or not |
| `bOutputSourcePoint` | `bool` | `true` | ◆ | Include the source point. |
| `PointTransform` | `FTransform` |  | ◆ | Transform offset for each point duplicate |

#### Extents Modifier

`UPCGPointExtentsModifierSettings` · plugin `PCG`

[epic] Modifies the extent of each point in the point data by manipulating the bounds.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Extents` | `FVector` | `FVector::One()` | ◆ |  |
| `Mode` | `EPCGPointExtentsModifierMode` | `EPCGPointExtentsModifierMode::Set` | ◆ | *Options: Set · Minimum · Maximum · Add · Multiply* |

#### Reset Point Center

`UPCGResetPointCenterSettings` · plugin `PCG`

[src] Modify the position of a point within its bounds, while keeping its bounds the same.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PointCenterLocation` | `FVector` | `FVector(0.5, 0.5, 0.5)` | ◆ | Set the normalized center of the point |

#### Split Points

`UPCGSplitPointsSettings` · plugin `PCG`

[src] Splits each input point into two separate points and sets bounds based on the position and axis of the cut.

[epic] For each point, create two points split in "Before Split" and "After Split" where the bounds are split along the specified "Split Axis" and "Split Position". For example, if the Split Position is 0.5, each point is cut in its middle and each half is a different output. This can be used to do more complex point assemblies by supporting subdivision.

**Pin data types detected:** in `default` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SplitPosition` | `float` | `0.5f` | ◆ |  |
| `SplitAxis` | `EPCGSplitAxis` | `EPCGSplitAxis::Z` | ◆ | *Options: X · Y · Z* |

#### Transform Points  ★

`UPCGTransformPointsSettings` · plugin `PCG`

[epic] Changes the points transforms (either in place or to an attribute with Apply to Attribute) using basic random rules. Each component of the transform (translation, rotation, scale) can be set to Absolute instead of relative to allow for more control. It contains the following options: Uniform Scale: Scales point data to the same X, Y, Z ratio. Recompute Seed: Forces the points seed to be updated according to their new world position. Example: use a Transform Points node with Absolute Rotation and rotation Z being 0 will make certain that the points are pointing in Z up.This makes sure the points are upwards after sampling from the landscape. This node is useful in generating spatial variation with control on the input Point Data. It is a staple of graphs generating natural looking data.

★ **This project:** `PCG_SurfaceTest`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bApplyToAttribute` | `bool` | `false` | ◆ | If the operation should be applied to a Transform attribute instead of the point transform. |
| `AttributeName` | `FName` |  | ◆ | *Only when* `bApplyToAttribute` |
| `OffsetMin` | `FVector` | `FVector::Zero()` | ◆ |  |
| `OffsetMax` | `FVector` | `FVector::Zero()` | ◆ |  |
| `bAbsoluteOffset` | `bool` | `false` | ◆ | Set offset in world space |
| `RotationMin` | `FRotator` | `FRotator::ZeroRotator` | ◆ |  |
| `RotationMax` | `FRotator` | `FRotator::ZeroRotator` | ◆ |  |
| `bAbsoluteRotation` | `bool` | `false` | ◆ | Set rotation directly instead of additively |
| `ScaleMin` | `FVector` | `FVector::One()` | ◆ |  |
| `ScaleMax` | `FVector` | `FVector::One()` | ◆ |  |
| `bAbsoluteScale` | `bool` | `false` | ◆ | Set scale directly instead of multiplicatively |
| `bUniformScale` | `bool` | `true` | ◆ | Scale uniformly on each axis. Uses the X component of ScaleMin and ScaleMax. |
| `bRecomputeSeed` | `bool` | `false` | ◆ | Recompute the seed for each new point using its new location *Only when* `!bApplyToAttribute` |

### ▸ Filter

#### Density Filter

`UPCGDensityFilterSettings` · plugin `PCG`

[epic] Filters points based on density and the provided filter ranges. This node is fully superceded by the Attribute Filter node, but is more specialized and more efficient than it is. This node should be used when performance is a major concern or when it makes it easier to convey intent in the graph this way.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `LowerBound` | `float` | `0.5f` | ◆ |  |
| `UpperBound` | `float` | `1.0f` | ◆ |  |
| `bInvertFilter` | `bool` | `false` | ◆ |  |
| `bKeepZeroDensityPoints` | `bool` | `false` | ◆ |  |

#### Filter Attribute Elements

`UPCGAttributeFilteringSettings` · plugin `PCG` · internal name `AttributeFilter`

**Also in the palette as:** *Point Filter*, *Attribute Filter*

[class] Filter elements by attribute that allows to do "A op B" type filtering, where A is the input spatial data or Attribute set, and B is either a constant, another spatial data (if input is a spatial data), an Attribute set (in filter) or the input itself. The filtering can be done either on properties or attributes. Some examples: - Threshold on property by constant (A.Density > 0.5) - Threshold on attribute by constant (A.aaa != "bob") - Threshold on property by metadata attribute(A.density >= B.bbb) - Threshold on property by property(A.density <= B.steepness) - Threshold on attribute by metadata attribute(A.aaa < B.bbb) - Threshold on attribute by property(A.aaa == B.color)

**Pin data types detected:** in `Any, PointOrParam` → out `PointOrParam`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operator` | `EPCGAttributeFilterOperator` | `EPCGAttributeFilterOperator::Greater` | ◆ | *Options: Greater · GreaterOrEqual · Lesser · LesserOrEqual · Equal · NotEqual · Substring · Matches* |
| `TargetAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Target property/attribute related properties |
| `bUseConstantThreshold` | `bool` | `false` | ◆ | Threshold property/attribute/constant related properties |
| `ThresholdAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bUseConstantThreshold` |
| `bUseSpatialQuery` | `bool` | `true` | ◆ | If the threshold data is Point data, it will sample input points in threshold data. Always true with Spatial data. *Only when* `!bUseConstantThreshold` |
| `AttributeTypes` | `FPCGMetadataTypesConstantStruct` |  |  | *Only when* `bUseConstantThreshold` |
| ↳ `Type` | `EPCGMetadataTypes` | `EPCGMetadataTypes::Double` |  | *Options: 15 options* *Only when* `bAllowsTypeChange` |
| ↳ `FloatValue` | `float` | `0.0f` |  | All different types *Only when* `Type == EPCGMetadataTypes::Float` |
| ↳ `Int32Value` | `int32` | `0` |  | *Only when* `Type == EPCGMetadataTypes::Integer32` |
| ↳ `DoubleValue` | `double` | `0.0` |  | *Only when* `Type == EPCGMetadataTypes::Double` |
| ↳ `IntValue` | `int64` | `0` |  | *Only when* `Type == EPCGMetadataTypes::Integer64` |
| ↳ `Vector2Value` | `FVector2D` | `FVector2D::ZeroVector` |  | *Only when* `Type == EPCGMetadataTypes::Vector2` |
| ↳ `VectorValue` | `FVector` | `FVector::ZeroVector` |  | *Only when* `Type == EPCGMetadataTypes::Vector` |
| ↳ `Vector4Value` | `FVector4` | `FVector4::Zero()` |  | *Only when* `Type == EPCGMetadataTypes::Vector4` |
| ↳ `QuatValue` | `FQuat` | `FQuat::Identity` |  | *Only when* `Type == EPCGMetadataTypes::Quaternion` |
| ↳ `TransformValue` | `FTransform` | `FTransform::Identity` |  | *Only when* `Type == EPCGMetadataTypes::Transform` |
| ↳ `StringValue` | `FString` | `""` |  | *Only when* `Type == EPCGMetadataTypes::String` |
| ↳ `BoolValue` | `bool` | `false` |  | *Only when* `Type == EPCGMetadataTypes::Boolean` |
| ↳ `RotatorValue` | `FRotator` | `FRotator::ZeroRotator` |  | *Only when* `Type == EPCGMetadataTypes::Rotator` |
| ↳ `NameValue` | `FName` | `NAME_None` |  | *Only when* `Type == EPCGMetadataTypes::Name` |
| ↳ `SoftClassPathValue` | `FSoftClassPath` |  |  | *Only when* `Type == EPCGMetadataTypes::SoftClassPath` |
| ↳ `SoftObjectPathValue` | `FSoftObjectPath` |  |  | *Only when* `Type == EPCGMetadataTypes::SoftObjectPath` |
| `bWarnOnDataMissingAttribute` | `bool` | `true` |  | Controls whether the node will emit a warning when the input data or the filter data doesn't have the attribute to filter on. |
| `bGenerateOutputDataEvenIfEmpty` | `bool` | `true` |  | Always generate output data (possibly empty) for both the in and out filters, even if all/none of the elements were filtered. |

#### Filter Attribute Elements by Range  ★

`UPCGAttributeFilteringRangeSettings` · plugin `PCG` · internal name `AttributeFilterRange`

**Also in the palette as:** *Point Filter Range*, *Attribute Filter Range*

[class] Attribute filter on range that allows to do "A op B" type filtering, where A is the input spatial data or Attribute set, and B is either a constant, another spatial data (if input is a spatial data), an Attribute set (in filter) or the input itself. The filtering can be done either on properties or attributes. Some examples (that might not make sense, but are valid): - Threshold on property by constant (A.Density in [0.2, 0.5]) - Threshold on attribute by constant (A.aaa in [0.4, 0.6]) - Threshold on property by metadata attribute(A.density in [B.bbmin, B.bbmax]) - Threshold on property by property(A.density in [B.position.x, B.steepness]) - Threshold on attribute by metadata attribute(A.aaa in [B.bbmin, B.bbmax]) - Threshold on attribute by property(A.aaa in [B.position, B.scale])

**Pin data types detected:** in `Any, PointOrParam` → out `PointOrParam`

★ **This project:** 7d.10 — palette alias *Point Filter Range*

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `TargetAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Target property/attribute related properties |
| `MinThreshold` | `FPCGAttributeFilterThresholdSettings` |  | ◆ | Threshold property/attribute/constant related properties |
| ↳ `bInclusive` | `bool` | `true` | ◆ | If the threshold in included or excluded from the range. |
| ↳ `bUseConstantThreshold` | `bool` | `false` | ◆ |  |
| ↳ `ThresholdAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bUseConstantThreshold` |
| ↳ `bUseSpatialQuery` | `bool` | `true` | ◆ | For Point Data, enabling this option will use sampling rather than comparing points 1 to 1 directly. For other spatial data, this is always true, and for attribute sets, always false. *Only when* `!bUseConstantThreshold` |
| ↳ `AttributeTypes` | `FPCGMetadataTypesConstantStruct` |  |  | *Only when* `bUseConstantThreshold` |
| `MaxThreshold` | `FPCGAttributeFilterThresholdSettings` |  | ◆ |  |
| ↳ `bInclusive` | `bool` | `true` | ◆ | If the threshold in included or excluded from the range. |
| ↳ `bUseConstantThreshold` | `bool` | `false` | ◆ |  |
| ↳ `ThresholdAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bUseConstantThreshold` |
| ↳ `bUseSpatialQuery` | `bool` | `true` | ◆ | For Point Data, enabling this option will use sampling rather than comparing points 1 to 1 directly. For other spatial data, this is always true, and for attribute sets, always false. *Only when* `!bUseConstantThreshold` |
| ↳ `AttributeTypes` | `FPCGMetadataTypesConstantStruct` |  |  | *Only when* `bUseConstantThreshold` |
| `bWarnOnDataMissingAttribute` | `bool` | `true` |  | Controls whether the node will emit a warning when the input data or the filter data doesn't have the attribute to filter on. |
| `bGenerateOutputDataEvenIfEmpty` | `bool` | `true` |  | Always generate output data (possibly empty) for both the in and out filters, even if all/none of the elements were filtered. |

#### Filter Data By Attribute

`UPCGFilterByAttributeSettings` · plugin `PCG`

[src] Separates input data by whether they have the specified attribute or not, or on the data attribute value.

[epic] Separates data (not contents) based on whether they have a specified metadata attribute, with the data having the attribute in the Inside Filter output and the rest in the Outside Filter output. This is used to prevent errors and warning on subgraph sections that rely on the existence of certain attributes that might not be guaranteed to exists in some circumstances, such as when getting data from actors in a world.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `FilterMode` | `EPCGFilterByAttributeMode` | `EPCGFilterByAttributeMode::FilterByExistence` | ◆ | *Options: FilterByExistence · FilterByValue · FilterByValueRange* |
| `Attributes` | `FName` |  | ◆ | Comma-separated list of attributes to look for *Only when* `FilterMode == EPCGFilterByAttributeMode::FilterByExistence` |
| `MetadataDomain` | `FName` | `PCGDataConstants::DefaultDomainName` | ◆ | Domain to target for filtering existence *Only when* `FilterMode == EPCGFilterByAttributeMode::FilterByExistence` |
| `Operator` | `EPCGStringMatchingOperator` | `EPCGStringMatchingOperator::Equal` | ◆ | *Options: Equal · Substring · Matches* *Only when* `FilterMode == EPCGFilterByAttributeMode::FilterByExistence` |
| `bIgnoreProperties` | `bool` | `false` | ◆ | Controls whether properties (denoted by $) will be considered in the filter or not. *Only when* `FilterMode == EPCGFilterByAttributeMode::FilterByExistence` |
| `FilterByValueMode` | `EPCGFilterByAttributeValueMode` | `EPCGFilterByAttributeValueMode::AnyOf` | ◆ | *Options: AnyOf · AllOf* *Only when* `FilterMode != EPCGFilterByAttributeMode::FilterByExistence` |
| `TargetAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `FilterMode != EPCGFilterByAttributeMode::FilterByExistence` |
| `FilterOperator` | `EPCGAttributeFilterOperator` | `EPCGAttributeFilterOperator::Greater` | ◆ | *Options: Greater · GreaterOrEqual · Lesser · LesserOrEqual · Equal · NotEqual · Substring · Matches* *Only when* `FilterMode == EPCGFilterByAttributeMode::FilterByValue` |
| `Threshold` | `FPCGFilterByAttributeThresholdSettings` |  | ◆ | *Only when* `FilterMode == EPCGFilterByAttributeMode::FilterByValue` |
| ↳ `bUseConstantThreshold` | `bool` | `true` | ◆ |  |
| ↳ `ThresholdAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bUseConstantThreshold` |
| ↳ `AttributeTypes` | `FPCGMetadataTypesConstantStruct` |  |  | *Only when* `bUseConstantThreshold` |
| `MinThreshold` | `FPCGFilterByAttributeThresholdSettingsRange` |  | ◆ | Threshold property/attribute/constant related properties *Only when* `FilterMode == EPCGFilterByAttributeMode::FilterByValueRange` |
| ↳ `bUseConstantThreshold` | `bool` | `true` | ◆ |  |
| ↳ `ThresholdAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bUseConstantThreshold` |
| ↳ `AttributeTypes` | `FPCGMetadataTypesConstantStruct` |  |  | *Only when* `bUseConstantThreshold` |
| ↳ `bInclusive` | `bool` | `false` | ◆ | *Only when* `ShowInclusive()` |
| `MaxThreshold` | `FPCGFilterByAttributeThresholdSettingsRange` |  | ◆ | *Only when* `FilterMode == EPCGFilterByAttributeMode::FilterByValueRange` |
| ↳ `bUseConstantThreshold` | `bool` | `true` | ◆ |  |
| ↳ `ThresholdAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bUseConstantThreshold` |
| ↳ `AttributeTypes` | `FPCGMetadataTypesConstantStruct` |  |  | *Only when* `bUseConstantThreshold` |
| ↳ `bInclusive` | `bool` | `false` | ◆ | *Only when* `ShowInclusive()` |

#### Filter Data By Index

`UPCGFilterByIndexSettings` · plugin `PCG`

[src] Filters data in the collection according to user selected indices

[epic] Separates data (not contents) based on their index and the filter provided in the settings. This filter is built from a string that contains individual indices or ranges separated by commas. Negative numbers are supported similar to how Python ranges work. For example, on an array of size 10 (values between 0 and 9), the selected indices 0, 2, 4:5, 7:-1 will include the indices 0, 2, 4, 7, and 8. This is used when there are very well known parameters in your graph that precisely allows some data, but it is likely that the first or last indices will generally be the most commonly selected indices.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bInvertFilter` | `bool` | `false` | ◆ | Will invert which indices will be included and excluded. |
| `SelectedIndices` | `FString` |  | ◆ | Selected individual indices or index ranges to include or exclude. Negative end indices allowed. For example, on an array of size 10: '0,2,4:5,7:-1' will include indices: 0,2,4,7,8 |

#### Filter Data By Tag

`UPCGFilterByTagSettings` · plugin `PCG`

[src] Filters data in the collection according to whether they have, or don't have, some tags

[epic] Separates data (not contents) according to their tags. You can specify a comma-separated list of Tags to filter by. This is useful when getting data from the world and building relationships between data in PCG. For example, the Get Actor Data node could return all actors with a given tag and then some of these would be inclusions and exclusions. Using the Fitler Data By Tag node then separates the data and passes it to where it woul dbe useful in the graph.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGFilterByTagOperation` | `EPCGFilterByTagOperation::KeepTagged` | ◆ | *Options: KeepTagged · RemoveTagged* |
| `Operator` | `EPCGStringMatchingOperator` | `EPCGStringMatchingOperator::Equal` | ◆ | *Options: Equal · Substring · Matches* |
| `SelectedTags` | `FString` |  | ◆ | Comma-separated list of tags |
| `bTokenizeOnWhiteSpace` | `bool` | `false` |  | *Only when* `bTokenizeOnWhiteSpace` |

#### Filter Data By Type

`UPCGFilterByTypeSettings` · plugin `PCG`

[src] Filters data in the collection according to data type

[epic] Separates data (not contents) based on their type, as dictated by the Target Type. Note that it is possible to have the Outside Filter pin show up in the settings. This node is used in the graph as a way of automatically filtering but there are other instances where it might be useful to determine behavior in the graph based on the data types provided. This would be allowed here in conjunction with the Count Data node.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `TargetType` | `FPCGDataTypeIdentifier` | `EPCGDataType::Any` |  |  |
| ↳ `CustomSubtype` | `int32` | `-1` |  |  |
| `bShowOutsideFilter` | `bool` | `false` |  |  |

#### Filter Elements By Index

`UPCGFilterElementsByIndexSettings` · plugin `PCG`

[src] Filters points or the elements of an attribute set based on a second input of points, attribute sets, or a user-defined index range expression.

**Pin data types detected:** in `PointOrParam` → out `PointOrParam`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bSelectIndicesByInput` | `bool` | `true` |  | A second input will define the indices to filter. |
| `IndexSelectionAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | The attribute which will define the indices to filter. *Only when* `bSelectIndicesByInput` |
| `SelectedIndices` | `FString` | `TEXT(":")` | ◆ | Selected individual indices or index ranges to include or exclude. Negative end indices allowed. For example, on an array of size 10: '0,2,4:5,7:-1' will include indices: 0,2,4,7,8. *Only when* `!bSelectIndicesByInput` |
| `bOutputDiscardedElements` | `bool` | `false` |  | An additional output for discarded elements. |
| `bInvertFilter` | `bool` | `false` | ◆ | Will invert which indices will be included and excluded. |

#### Random Choice

`UPCGRandomChoiceSettings` · plugin `PCG`

[src] Chooses entries randomly through ratio or a fixed number of entries. Chosen/Discarded entries will be in the same order than they appear in the input data.

**Pin data types detected:** in `PointOrParam` → out `PointOrParam`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bFixedMode` | `bool` | `true` | ◆ | Either choose a fixed number of entries, or a ratio of entries. |
| `FixedNumber` | `int` | `1` | ◆ | Defines the number of entries to keep. *Only when* `bFixedMode` |
| `Ratio` | `float` | `0.5` | ◆ | Defines the ratio of entries to keep. *Only when* `!bFixedMode` |
| `bOutputDiscardedEntries` | `bool` | `true` |  | By default, we output discarded entries. If you don't need them, disable this option. |
| `bHasCustomSeedSource` | `bool` | `false` | ◆ | Use an attribute as a source for generating the seed, i.e. similar to or replacing the $Seed property on points. Mostly useful for attribute sets as points have this unique seed by default. |
| `CustomSeedSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to generate the selection seed from. *Only when* `bHasCustomSeedSource` |
| `bUseFirstAttributeOnly` | `bool` | `true` | ◆ | Controls whether only the first element's attribute will be used to generate the selection seed. Otherwise, all values will be used to compute it. *Only when* `bHasCustomSeedSource` |

#### Remove Empty Data

`UPCGRemoveEmptyDataSettings` · plugin `PCG`

[src] Remove all data in the input pin that is empty.

**Pin data types detected:** in `Any` → out `Any`

*No editable settings declared.*

#### Self Pruning

`UPCGSelfPruningSettings` · plugin `PCG`

[epic] Removes intersections between points in the same point data, prioritizing data based on the settings (Large to Small, etc.). Points with a similar radius can be randomly selected using randomized pruning to prevent patterns from emerging.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Parameters` | `FPCGSelfPruningParameters` |  | ◆ |  |
| ↳ `PruningType` | `EPCGSelfPruningType` | `EPCGSelfPruningType::LargeToSmall` | ◆ | *Options: LargeToSmall · SmallToLarge · AllEqual · None · RemoveDuplicates* |
| ↳ `ComparisonSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | By default, it will prune according to the extents of each point, but you can provide another comparison like Density, or a dynamic attribute. Only support numeric values or vector (vector will be reduced to its squared length). *Only when* `PruningType == EPCGSelfPruningType::LargeToSmall \|\| PruningType == EPCGSelfPruningType::SmallToLarge` |
| ↳ `RadiusSimilarityFactor` | `float` | `0.25f` | ◆ | Similarity factor to consider 2 points "equal". (For example, if a point extents squared length is 10 and factor is 0.25, all points between 7.5 and 12.5 will be considered "the same"). *Only when* `PruningType == EPCGSelfPruningType::LargeToSmall \|\| PruningType == EPCGSelfPruningType::SmallToLarge` |
| ↳ `bRandomizedPruning` | `bool` | `true` | ◆ |  |
| ↳ `bUseCollisionAttribute` | `bool` | `false` | ◆ | *Only when* `PruningType != EPCGSelfPruningType::RemoveDuplicates` |
| ↳ `CollisionAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Specifies to use the collision from a given mesh instead of the point; note that this will be ignored in the Remove Duplicates mode. *Only when* `bUseCollisionAttribute && PruningType != EPCGSelfPruningType::RemoveDuplicates` |
| ↳ `CollisionQueryFlag` | `EPCGCollisionQueryFlag` | `EPCGCollisionQueryFlag::Simple` | ◆ | Controls whether queries will be done against complex collisions or not. If enabled, performance warning. *Options: Simple · Complex · SimpleFirst · ComplexFirst* *Only when* `bUseCollisionAttribute && PruningType != EPCGSelfPruningType::RemoveDuplicates` |

### ▸ Metadata (attributes)

#### Attribute Bitwise Op

`UPCGMetadataBitwiseSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataBitwiseOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataBitwiseOperation` | `EPCGMetadataBitwiseOperation::And` |  | *Options: And · Not · Or · Xor · ShiftLeft · ShiftRight* |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation != EPCGMetadataBitwiseOperation::Not` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Boolean Op

`UPCGMetadataBooleanSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataBooleanOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataBooleanOperation` | `EPCGMetadataBooleanOperation::And` |  | *Options: And · Not · Or · Xor · Nand · Nor · Xnor · Imply · Nimply* |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation != EPCGMetadataBooleanOperation::Not` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Cast

`UPCGAttributeCastSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataTypes` value** — see section 4.

[class] Cast an attribute to another type. Support broadcastable cast (like double -> FVector) and constructible cast (like double -> float)

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `OutputType` | `EPCGMetadataTypes` | `EPCGMetadataTypes::Float` | ◆ | *Options: 15 options* |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ |  |

#### Attribute Compare Op

`UPCGMetadataCompareSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataCompareOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataCompareOperation` | `EPCGMetadataCompareOperation::Equal` |  | *Options: Equal · NotEqual · Greater · GreaterOrEqual · Less · LessOrEqual* |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `Tolerance` | `double` | `UE_DOUBLE_SMALL_NUMBER` |  | *Only when* `Operation == EPCGMetadataCompareOperation::Equal \|\| Operation == EPCGMetadataCompareOperation::NotEqual` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Maths Op  ★

`UPCGMetadataMathsSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataMathsOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

★ **This project:** 7d.10 slope rules

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataMathsOperation` | `EPCGMetadataMathsOperation::Add` |  | *Options: 25 options* |
| `bForceRoundingOpToInt` | `bool` | `false` |  | For rounding operation, if the input type is float or double, use this option to force the output attribute to be int64. *Only when* `Operation == EPCGMetadataMathsOperation::Round \|\| Operation == EPCGMetadataMathsOperation::Truncate \|\| Operation == EPCGMetadataMathsOpe …` |
| `bForceOpToDouble` | `bool` | `false` |  | For operations that can yield floating point values, if the input type are ints, use this option to force the output attribute to be double. *Only when* `Operation == EPCGMetadataMathsOperation::Divide \|\| Operation == EPCGMetadataMathsOperation::Sqrt \|\| Operation == EPCGMetadataMathsOperat …` |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `(Operation & '/Script/PCG.EPCGMetadataMathsOperation::BinaryOp') \|\| (Operation & '/Script/PCG.EPCGMetadataMathsOperation::TernaryOp')` |
| `InputSource3` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation & '/Script/PCG.EPCGMetadataMathsOperation::TernaryOp'` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Noise

`UPCGAttributeNoiseSettings` · plugin `PCG`

**Also in the palette as:** *Density Noise*

[class] Apply some noise to an attribute/property. You can select the mode you want and a noise range. Support all numerical types and vectors/rotators.

[epic] Computes new values for a target attribute for each point in a set of point data. This works with Point Data and Attribute Sets. The value will depend on the selected input attribute, Mode, Noise Min, and Noise Max. This is useful to add variation on contiuous parameters.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ |  |
| `Mode` | `EPCGAttributeNoiseMode` | `EPCGAttributeNoiseMode::Set` | ◆ | Attribute = (Original op Noise), Noise in [NoiseMin, NoiseMax] *Options: Set · Minimum · Maximum · Add · Multiply* |
| `NoiseMin` | `float` | `0.f` | ◆ |  |
| `NoiseMax` | `float` | `1.f` | ◆ |  |
| `bInvertSource` | `bool` | `false` | ◆ | Attribute = 1 - Attribute before applying the operation |
| `bClampResult` | `bool` | `false` | ◆ | Clamp the result between 0 and 1. Always applied if we apply noise to the density. |
| `bHasCustomSeedSource` | `bool` | `false` | ◆ |  |
| `CustomSeedSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `bHasCustomSeedSource` |

#### Attribute Partition

`UPCGMetadataPartitionSettings` · plugin `PCG`

[epic] Splites the input data (Point Data or Attribute Set, or other spatial data to be converted to Point Data if required) in a partition according to the attributes selected. All elements with the same values for each of the selected attributes ends up in the same output data. This is helpful to separate data going into a Loop node if there is processing to be done in a certain situation for the same attribute value, such as sampling points on a mesh using the Mesh Sampler and propagating these points through a Copy Points on the "right" points.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PartitionAttributeSelectors` | `TArray<FPCGAttributePropertyInputSelector>` | `{FPCGAttributePropertyInputSelector()}` |  | The data will be partitioned on these selected attributes. |
| `bTokenizeOnWhiteSpace` | `bool` | `false` |  | *Only when* `bTokenizeOnWhiteSpace` |
| `Output Partition Index` | `bool` | `false` | ◆ | Assign an index partition as an extra attribute. |
| `bDoNotPartition` | `bool` | `true` | ◆ | If we assign an index, we can also not partition (and only assign the partition index to the original data). *Only when* `bAssignIndexPartition` |
| `PartitionIndexAttributeName` | `FName` | `TEXT("PartitionIndex")` | ◆ | *Only when* `bAssignIndexPartition` |

#### Attribute Reduce

`UPCGAttributeReduceSettings` · plugin `PCG`

**One palette entry per `EPCGAttributeReduceOperation` value** — see section 4.

[class] Take all the entries/points from the input and perform a reduce operation on the given attribute/property and output the result into a ParamData. Note: Special case for average on Quaternion since they are not trivially averageable. We have a simplistic approximation that would be accurate only if the quaternions are close to each other. The accurate version of the average is using eigenvectors/eigenvalues which is way more complicated and computationally expensive. Quaternion will also be normatilzed at the end. Beware if you are using this average.

**Pin data types detected:** in `Any` → out `Any, Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `bWriteToDataDomain` | `bool` | `false` |  | By default the reduce output the result into an new attribute set, but it can also be written into the data domain of the input. |
| `OutputAttributeName` | `FName` | `NAME_None` | ◆ |  |
| `Operation` | `EPCGAttributeReduceOperation` | `EPCGAttributeReduceOperation::Average` | ◆ | *Options: Average · Max · Min · Sum · Join* |
| `JoinDelimiter` | `FString` | `FString(", ")` | ◆ | *Only when* `Operation==EPCGAttributeReduceOperation::Join` |
| `bMergeOutputAttributes` | `bool` | `false` | ◆ | Option to merge all results into a single attribute set with multiple entries, instead of multiple attribute sets with a single value in them. *Only when* `!bWriteToDataDomain` |

#### Attribute Remap

`UPCGAttributeRemapSettings` · plugin `PCG`

**Also in the palette as:** *Density Remap*, *Attribute Curve Remap*

[src] Remap an attribute using either a range or a curve.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `EPCGAttributeRemapMode` | `EPCGAttributeRemapMode::Ranges` | ◆ | *Options: Ranges · Curve* |
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InRangeMin` | `double` | `0.f` | ◆ | If InRangeMin = InRangeMax, then that attribute value is mapped to the average of OutRangeMin and OutRangeMax *Only when* `Mode == EPCGAttributeRemapMode::Ranges` |
| `InRangeMax` | `double` | `1.f` | ◆ | If InRangeMin = InRangeMax, then that attribute value is mapped to the average of OutRangeMin and OutRangeMax *Only when* `Mode == EPCGAttributeRemapMode::Ranges` |
| `OutRangeMin` | `double` | `0.f` | ◆ | *Only when* `Mode == EPCGAttributeRemapMode::Ranges` |
| `OutRangeMax` | `double` | `1.f` | ◆ | *Only when* `Mode == EPCGAttributeRemapMode::Ranges` |
| `bClampToUnitRange` | `bool` | `false` | ◆ | If checked, outside values will be clamped between 0 and 1. *Only when* `Mode == EPCGAttributeRemapMode::Ranges` |
| `bIgnoreValuesOutsideInputRange` | `bool` | `false` | ◆ | Attribute values outside of the input range will be unaffected by the remapping *Only when* `Mode == EPCGAttributeRemapMode::Ranges` |
| `bAllowInverseRange` | `bool` | `false` | ◆ | Allow remapping when Min is larger than Max, e.g. from [0.0, 1.0] -> [1.0, 0.0]. *Only when* `Mode == EPCGAttributeRemapMode::Ranges` |
| `Curve` | `FRuntimeFloatCurve` |  | ◆ | Note that this is no longer the default value for new nodes, it is now 'true' *Only when* `Mode == EPCGAttributeRemapMode::Curve` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Remove Duplicates

`UPCGAttributeRemoveDuplicatesSettings` · plugin `PCG`

[class] Remove duplicates for given attributes

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `AttributeSelectors` | `TArray<FPCGAttributePropertyInputSelector>` | `{ FPCGAttributePropertyInputSelector() }` |  | The data will be partitioned on these selected attributes, and we will only keep the first entry for each partition. |

#### Attribute Rename

`UPCGMetadataRenameSettings` · plugin `PCG`

[epic] Renames an existing attribute. This node is used when downstream processing needs specific attributes to exist. This is useful to pass data down to subgraphs.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `AttributeToRename` | `FPCGAttributePropertyInputSelector` |  | ◆ | Selector to the attribute to rename. Can also specify a metadata domain. Can't be a property or contains extractors. |
| `NewAttributeName` | `FName` | `NAME_None` | ◆ | Name of the new attribute, rename is in place. It will be on the same domain specified by the AttributeToRename selector. |

#### Attribute Rotator Op

`UPCGMetadataRotatorSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataRotatorOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataRotatorOperation` | `EPCGMetadataRotatorOperation::Combine` |  | *Options: Combine · Invert · Lerp · Normalize · TransformRotation · InverseTransformRotation* |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation != EPCGMetadataRotatorOperation::Invert` |
| `InputSource3` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation == EPCGMetadataRotatorOperation::Lerp` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Select

`UPCGAttributeSelectSettings` · plugin `PCG`

[class] Take all the entries/points from the input and perform a select operation on the given attribute/property on the given axis (if the attribute/property is a vector) and output the result into a ParamData. It will also output the selected point if the input is a PointData. Only support vector attributes and scalar attributes. CustomAxis is overridable. In case of the median operation, and the number of elements is even, we arbitrarily chose a point (Index = Num / 2) If the OutputAttributeName is None, we will use InputSource.GetName().

[epic] Computes the Min, Max, or Median on a selected Axis. Note that this is analogous to computing a dot product with an axis.

**Pin data types detected:** in `Spatial` → out `Param, Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `OutputAttributeName` | `FName` | `NAME_None` |  |  |
| `Operation` | `EPCGAttributeSelectOperation` | `EPCGAttributeSelectOperation::Min` | ◆ | *Options: Min · Max · Median* |
| `Axis` | `EPCGAttributeSelectAxis` | `EPCGAttributeSelectAxis::X` | ◆ | *Options: X · Y · Z · W · CustomAxis* |
| `CustomAxis` | `FVector4` | `FVector4::Zero()` | ◆ | *Only when* `Axis == EPCGAttributeSelectAxis::CustomAxis` |

#### Attribute String Op

`UPCGMetadataStringOpSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataStringOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

[epic] Performs String-related attribute operations, such as appending strings. This node is used in conjunction with the Print String node and the Create Target Actor nodes.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataStringOperation` | `EPCGMetadataStringOperation::Append` |  | *Options: Append · Replace · Substring · Matches · ToUpper · ToLower · TrimStart · TrimEnd · TrimStartAndEnd* |
| `SearchCase` | `TEnumAsByte<ESearchCase::Type>` | `ESearchCase::CaseSensitive` | ◆ | *Only when* `Operation == EPCGMetadataStringOperation::Substring \|\| Operation == EPCGMetadataStringOperation::Matches` |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource3` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation==EPCGMetadataStringOperation::Replace` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Transform Op

`UPCGMetadataTransformSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataTransformOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataTransformOperation` | `EPCGMetadataTransformOperation::Compose` |  | *Options: Compose · Invert · Lerp* |
| `TransformLerpMode` | `EPCGTransformLerpMode` | `EPCGTransformLerpMode::QuatInterp` |  | *Options: QuatInterp · EulerInterp · follows* *Only when* `Operation == EPCGMetadataTransformOperation::Lerp` |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation != EPCGMetadataTransformOperation::Invert` |
| `InputSource3` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation == EPCGMetadataTransformOperation::Lerp` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Trig Op

`UPCGMetadataTrigSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataTrigOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataTrigOperation` | `EPCGMetadataTrigOperation::Acos` |  | *Options: Acos · Asin · Atan · Atan2 · Cos · Sin · Tan · DegToRad · RadToDeg* |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation == EPCGMetadataTrigOperation::Atan2` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Attribute Vector Op  ★

`UPCGMetadataVectorSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataVectorOperation` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

★ **This project:** 7d.10 slope rules (Dot, Normalize)

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGMetadataVectorOperation` | `EPCGMetadataVectorOperation::Cross` |  | *Options: Cross · Dot · Distance · Normalize · Length · RotateAroundAxis · TransformDirection · TransformLocation · InverseTransformDirection · InverseTransformLocation* |
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation != EPCGMetadataVectorOperation::Normalize && Operation != EPCGMetadataVectorOperation::Length` |
| `InputSource3` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation == EPCGMetadataVectorOperation::RotateAroundAxis` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Break Transform Attribute

`UPCGMetadataBreakTransformSettings` · plugin `PCG`

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

[epic] Breaks down a Transform attribute into its components: Translation, Rotation, and Scale.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Break Vector Attribute

`UPCGMetadataBreakVectorSettings` · plugin `PCG`

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

[epic] Breaks down a Vector attribute into its components: X, Y, Z, and W.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Copy Attributes  ⚠ deprecated

`UPCGAttributeTransferSettings` · plugin `PCG`

> ⚠ Deprecated in 5.5: *Use UPCGCopyAttributeSettings* [src]

[src] Copy from the Input Source to Output Target attribute.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGCopyAttributesOperation` | `EPCGCopyAttributesOperation::CopyEachSourceToEachTargetRespe …` | ◆ | *Options: 15 options* *(from `UPCGCopyAttributesSettings`)* |
| `bCopyAllAttributes` | `bool` | `false` | ◆ | *(from `UPCGCopyAttributesSettings`)* |
| `bCopyAllDomains` | `bool` | `false` | ◆ | If checked, it is copying all attributes from all domains, as long as the source domain is supported on the target data. *Only when* `bCopyAllAttributes` *(from `UPCGCopyAttributesSettings`)* |
| `MetadataDomainsMapping` | `TMap<FName, FName>` |  |  | When copying all attributes, a mapping can be specified. If it is empty, it's going to be Default -> Default. *Only when* `bCopyAllAttributes && !bCopyAllDomains` *(from `UPCGCopyAttributesSettings`)* |
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bCopyAllAttributes` *(from `UPCGCopyAttributesSettings`)* |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *Only when* `!bCopyAllAttributes` *(from `UPCGCopyAttributesSettings`)* |

#### Copy Attributes

`UPCGCopyAttributesSettings` · plugin `PCG`

[src] Copy from the Input Source to Output Target attribute.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGCopyAttributesOperation` | `EPCGCopyAttributesOperation::CopyEachSourceToEachTargetRespe …` | ◆ | *Options: 15 options* |
| `bCopyAllAttributes` | `bool` | `false` | ◆ |  |
| `bCopyAllDomains` | `bool` | `false` | ◆ | If checked, it is copying all attributes from all domains, as long as the source domain is supported on the target data. *Only when* `bCopyAllAttributes` |
| `MetadataDomainsMapping` | `TMap<FName, FName>` |  |  | When copying all attributes, a mapping can be specified. If it is empty, it's going to be Default -> Default. *Only when* `bCopyAllAttributes && !bCopyAllDomains` |
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bCopyAllAttributes` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *Only when* `!bCopyAllAttributes` |

#### Copy Attributes  ⚠ deprecated

`UPCGMetadataOperationSettings` · plugin `PCG`

> ⚠ Deprecated in 5.5: *Use UPCGCopyAttributeSettings* [src]

[src] Copy from the Input Source to Output Target attribute.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGCopyAttributesOperation` | `EPCGCopyAttributesOperation::CopyEachSourceToEachTargetRespe …` | ◆ | *Options: 15 options* *(from `UPCGCopyAttributesSettings`)* |
| `bCopyAllAttributes` | `bool` | `false` | ◆ | *(from `UPCGCopyAttributesSettings`)* |
| `bCopyAllDomains` | `bool` | `false` | ◆ | If checked, it is copying all attributes from all domains, as long as the source domain is supported on the target data. *Only when* `bCopyAllAttributes` *(from `UPCGCopyAttributesSettings`)* |
| `MetadataDomainsMapping` | `TMap<FName, FName>` |  |  | When copying all attributes, a mapping can be specified. If it is empty, it's going to be Default -> Default. *Only when* `bCopyAllAttributes && !bCopyAllDomains` *(from `UPCGCopyAttributesSettings`)* |
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bCopyAllAttributes` *(from `UPCGCopyAttributesSettings`)* |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *Only when* `!bCopyAllAttributes` *(from `UPCGCopyAttributesSettings`)* |

#### Delete Attributes

`UPCGDeleteAttributesSettings` · plugin `PCG`

[class] Removes attributes from a given input metadata. Either removes specifically named attributes or remove all attributes not in a given list. The output will be the original data with the updated metadata.

[epic] Filters (keep or remove) comma-separated attributes from an Attribute Set or Spatial Data. This node is used to remove attributes that aren't useful downstream. In some caeses, it might worthwhile to do so to not pollute output data with temporary attributes, but also because some operations are more costly on a per-attribute basis, such as Copy Points, and depends on the settings being used.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGAttributeFilterOperation` | `EPCGAttributeFilterOperation::KeepSelectedAttributes` | ◆ | Implementation note: the default has been changed to DeleteSelected for new objects *Options: KeepSelectedAttributes · DeleteSelectedAttributes* |
| `Operator` | `EPCGStringMatchingOperator` | `EPCGStringMatchingOperator::Equal` | ◆ | *Options: Equal · Substring · Matches* |
| `SelectedAttributes` | `FString` |  | ◆ | Comma-separated list of attributes to keep or remove from the input data. |
| `bTokenizeOnWhiteSpace` | `bool` | `false` |  | *Only when* `bTokenizeOnWhiteSpace` |
| `MetadataDomain` | `FName` | `PCGDataConstants::DefaultDomainName` | ◆ | When deleting attributes, it only target a single domain that can be specified here. |

#### Extract Attribute

`UPCGExtractAttributeSettings` · plugin `PCG`

[src] Extract an attribute at a given index into a new attribute set. Support any domain. Index needs to be in range of valid indexes for the given domain.

**Pin data types detected:** in `Any` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `Index` | `int32` | `0` | ◆ |  |
| `OutputAttributeName` | `FPCGAttributePropertyOutputSelector` |  | ◆ |  |

#### Generate Seed

`UPCGGenerateSeedSettings` · plugin `PCG`

[src] Generate a seed attribute

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `GenerationSource` | `EPCGGenerateSeedSource` | `EPCGGenerateSeedSource::RandomStream` |  | The source method seed attribute. *Options: RandomStream · HashEachSourceAttribute · HashStringConstant* |
| `String` | `FString` |  |  | This value will be hashed and applied to generate each new seed. *Only when* `GenerationSource == EPCGGenerateSeedSource::HashStringConstant` |
| `SeedSource` | `FPCGAttributePropertyInputSelector` |  |  | The source attribute to hash to generate each new seed. *Only when* `GenerationSource == EPCGGenerateSeedSource::HashEachSourceAttribute` |
| `bResetSeedPerInput` | `bool` | `true` | ◆ | Reset the seed at the beginning of each input's generation to stay order agnostic. *Only when* `GenerationSource != EPCGGenerateSeedSource::HashEachSourceAttribute` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | The target attribute output of the generated seed. |

#### Get Attribute From Point Index

`UPCGAttributeGetFromPointIndexSettings` · plugin `PCG`

[class] Get the attribute/property of a point given its index. The result will be in a ParamData. There is also a second output that will output the selected point. This point will be output even if the property/attribute doesn't exist. The Index can be overridden by a second Params input.

[epic] Retrieves a single point from point data and its attributes in a separate Attribute Set. This node is often used inside of loops on partitioned data to retrieve the common attribute value easily.

**Pin data types detected:** in `Point` → out `Param, Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `Index` | `int32` | `0` | ◆ |  |
| `OutputAttributeName` | `FPCGAttributePropertyOutputSelector` |  | ◆ |  |

#### Get Element Count

`UPCGNumberOfElementsSettings` · plugin `PCG` · internal name `GetElementsCount`

[src] Return the number of elements in the input data.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `OutputAttributeName` | `FName` | `"NumEntries"` | ◆ |  |

#### Hash Attribute

`UPCGHashAttributeSettings` · plugin `PCG`

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Input Source` | `FPCGAttributePropertyInputSelector` |  | ◆ | ~End IPCGSettingsDefaultValueProvider interface |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Make Rotator Attribute

`UPCGMetadataMakeRotatorSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataMakeRotatorOp` value** — see section 4.

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation != EPCGMetadataMakeRotatorOp::MakeRotFromX && Operation != EPCGMetadataMakeRotatorOp::MakeRotFromY && Operation != EPCGMetadataMak …` |
| `InputSource3` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Operation == EPCGMetadataMakeRotatorOp::MakeRotFromAxes \|\| Operation == EPCGMetadataMakeRotatorOp::MakeRotFromAngles` |
| `Operation` | `EPCGMetadataMakeRotatorOp` | `EPCGMetadataMakeRotatorOp::MakeRotFromAxes` |  | *Options: MakeRotFromX · MakeRotFromY · MakeRotFromZ · MakeRotFromXY · MakeRotFromYX · MakeRotFromXZ · MakeRotFromZX · MakeRotFromYZ · MakeRotFromZY · MakeRotFromAxes · MakeRotFromAngles* |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Make Transform Attribute

`UPCGMetadataMakeTransformSettings` · plugin `PCG`

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

[epic] Creates a Transform attribute from three provided attributes: Translation, Rotation, and Scale.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource3` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Make Vector Attribute

`UPCGMetadataMakeVectorSettings` · plugin `PCG`

[src] Metadata operation between Points/Spatial/AttributeSet data. Output data will be taken from the first spatial data by default, or first pin if all are attribute sets. It can be overridden in the settings.

[epic] Creates a Vector attribute from two to four attributes based on Output Type.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource1` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource2` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource3` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `InputSource4` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `OutputType` | `EPCGMetadataTypes` | `EPCGMetadataTypes::Vector2` |  | *Options: 15 options* |
| `MakeVector3Op` | `EPCGMetadataMakeVector3` | `EPCGMetadataMakeVector3::ThreeValues` |  | *Options: ThreeValues · Vector2AndValue* *Only when* `OutputType == EPCGMetadataTypes::Vector` |
| `MakeVector4Op` | `EPCGMetadataMakeVector4` | `EPCGMetadataMakeVector4::FourValues` |  | *Options: FourValues · Vector2AndTwoValues · TwoVector2 · Vector3AndValue* *Only when* `OutputType == EPCGMetadataTypes::Vector4` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Match And Set Attributes  ★

`UPCGMatchAndSetAttributesSettings` · plugin `PCG`

[src] Matches or randomly assigns values from the Attribute Set to the input data. Supports N (input):1 (match data), or N:N configurations.

[epic] Selects an entry in the provided Attribute Set table (Match Data) and copies its values to the input data (Point Data or Attribute Set). This supercedes the Point Match and Set node. Selection is driven by matching an attribute (Match Attributes) on the input data (Input Attribute) with an attribute on the Match Data (Match Attribute) so that values are copied only from an entry in the Match Data if their values coincide. When data is not matching an attribute, all entries in the Match Data are considered valid matches. Additionally, there is an option to keep or discard entries that do not match anything from the Match Data. In cases where there are multiple potential matches in the Match Data, it is possible to weight them (Match Weight Attribute) or one will be selected randomly. It is possible to correlate a [0 - 1] value from the input data to the normalized weight from the Match Da …

**Pin data types detected:** in `Param, PointOrParam` → out `PointOrParam`

★ **This project:** `PCG_SurfaceTest`; job 8 Zoning

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bMatchAttributes` | `bool` | `false` | ◆ | Controls whether selection of the attribute set values to copy will be done by matching point-to-attribute set (true) or done randomly (false). |
| `InputAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute from the point data to select & match. *Only when* `bMatchAttributes` |
| `MatchAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute from the attribute set to match against. *Only when* `bMatchAttributes` |
| `bKeepUnmatched` | `bool` | `true` | ◆ | Controls whether points that have no valid match in the attribute set are kept as is (default values) or removed from the output. *Only when* `bMatchAttributes` |
| `bFindNearest` | `bool` | `false` | ◆ | Controls whether the match operation will return the nearest match and not only match on equality. *Only when* `bMatchAttributes` |
| `MaxDistanceMode` | `EPCGMatchMaxDistanceMode` | `EPCGMatchMaxDistanceMode::NoMaxDistance` | ◆ | Controls whether the match operation has a maximum distance on which to reject points that would be too far from the nearest value. *Options: NoMaxDistance · UseConstantMaxDistance · AttributeMaxDistance* *Only when* `bFindNearest` |
| `MaxDistanceForNearestMatch` | `FPCGMetadataTypesConstantStruct` |  |  | Constant value that establishes the maximum distance an entry can be from its nearest match to be selected *Only when* `bFindNearest && MaxDistanceMode==EPCGMatchMaxDistanceMode::UseConstantMaxDistance` |
| ↳ `Type` | `EPCGMetadataTypes` | `EPCGMetadataTypes::Double` |  | *Options: 15 options* *Only when* `bAllowsTypeChange` |
| ↳ `FloatValue` | `float` | `0.0f` |  | All different types *Only when* `Type == EPCGMetadataTypes::Float` |
| ↳ `Int32Value` | `int32` | `0` |  | *Only when* `Type == EPCGMetadataTypes::Integer32` |
| ↳ `DoubleValue` | `double` | `0.0` |  | *Only when* `Type == EPCGMetadataTypes::Double` |
| ↳ `IntValue` | `int64` | `0` |  | *Only when* `Type == EPCGMetadataTypes::Integer64` |
| ↳ `Vector2Value` | `FVector2D` | `FVector2D::ZeroVector` |  | *Only when* `Type == EPCGMetadataTypes::Vector2` |
| ↳ `VectorValue` | `FVector` | `FVector::ZeroVector` |  | *Only when* `Type == EPCGMetadataTypes::Vector` |
| ↳ `Vector4Value` | `FVector4` | `FVector4::Zero()` |  | *Only when* `Type == EPCGMetadataTypes::Vector4` |
| ↳ `QuatValue` | `FQuat` | `FQuat::Identity` |  | *Only when* `Type == EPCGMetadataTypes::Quaternion` |
| ↳ `TransformValue` | `FTransform` | `FTransform::Identity` |  | *Only when* `Type == EPCGMetadataTypes::Transform` |
| ↳ `StringValue` | `FString` | `""` |  | *Only when* `Type == EPCGMetadataTypes::String` |
| ↳ `BoolValue` | `bool` | `false` |  | *Only when* `Type == EPCGMetadataTypes::Boolean` |
| ↳ `RotatorValue` | `FRotator` | `FRotator::ZeroRotator` |  | *Only when* `Type == EPCGMetadataTypes::Rotator` |
| ↳ `NameValue` | `FName` | `NAME_None` |  | *Only when* `Type == EPCGMetadataTypes::Name` |
| ↳ `SoftClassPathValue` | `FSoftClassPath` |  |  | *Only when* `Type == EPCGMetadataTypes::SoftClassPath` |
| ↳ `SoftObjectPathValue` | `FSoftObjectPath` |  |  | *Only when* `Type == EPCGMetadataTypes::SoftObjectPath` |
| `MaxDistanceInputAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `bFindNearest && MaxDistanceMode==EPCGMatchMaxDistanceMode::AttributeMaxDistance` |
| `bUseInputWeightAttribute` | `bool` | `false` | ◆ | Controls whether we will use the attribute provided in the Input Weight Attribute to perform entry selection. |
| `InputWeightAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Input weight from the points, assumed to be in the [0, 1] range. *Only when* `bUseInputWeightAttribute` |
| `Use Match Weight` | `bool` | `false` | ◆ | Controls whether we will consider the weights, as determined by the Weight Attribute values on the attribute set. |
| `Match Weight Attribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to weight more or less some entries from the attribute set. *Only when* `bUseWeightAttribute` |
| `bWarnIfNoMatchData` | `bool` | `true` |  | Controls whether we will emit a warning and return nothing if there is no provided attribute set. |
| `bWarnOnAttributeCast` | `bool` | `true` |  |  |

#### Merge Attributes

`UPCGMergeAttributesSettings` · plugin `PCG`

[src] Merges multiple attribute sets in a single attribute set with multiple entries and all the provided attributes

[epic] Merges multiple attribute sets (in order of connection) together. Attributes that are not common are set to their respective default value (as of attribute creation) in the entries that did not have these attributes.

**Pin data types detected:** in `default` → out `Param`

*No editable settings declared.*

#### Parse String

`UPCGParseStringSettings` · plugin `PCG`

[src] Parse string passed as attribute into a compatible PCG type. Failed to parse will result to the value be set to Identity(for quat and transform) or 0 (for the rest). Int/Int64: Support base 10 or base 16 number (ie. 0xff). If int overflows, result is platform dependant. Float/Double: Support normal representation or exposant representation (ie. 13.5e-2f) Bool: [True/Yes/On] [False/No/Off], or 0 -> false and the rest -> trueVectors/Quat: X=<value> Y=<value> Z=<value> W=<value> OR <value>,<value>,<value>,<value> Rotator: P=<value> Y=<value> R=<value> or Pitch=<value> Yaw=<value> Roll=<value> or <value,<value>,<value> Transform: <value>,<value>,<value>\|<value>,<value>,<value>\|<value>,<value>,<value> (Translation\|Rotation\|Scale)

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `TargetType` | `EPCGMetadataTypes` | `EPCGMetadataTypes::Integer32` | ◆ | *Options: 15 options* |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *(from `UPCGMetadataSettingsBase`)* |
| `OutputDataFromPin` | `FName` | `PCGMetadataSettingsBaseConstants::DefaultOutputDataFromPinNa …` |  | *(from `UPCGMetadataSettingsBase`)* |

#### Point Match And Set

`UPCGPointMatchAndSetSettings` · plugin `PCG`

[src] For all points, if a match is found (e.g. some attribute is equal to some value), sets a value on the point (e.g. another attribute).

[epic] Using the Match And Set Type option, finds a match for each point based on the selection criteria, then applies the value to an attribute. A common use case is to select meshes to be used downstream in a Static Mesh Spawner node with the By Attribute selector.

**Pin data types detected:** in `default` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `MatchAndSetType` | `class UPCGMatchAndSetBase` |  |  | Defines the type of Match & Set object to use. |
| `SetTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | "Set" part of the Match & Set - defines what will be changed in the operation |
| `SetTargetType` | `EPCGMetadataTypes` | `EPCGMetadataTypes::Double` |  | If the "Set" part is an attribute, then the type must be provided *Options: 15 options* *Only when* `bSetTargetIsAttribute` |

### ▸ Param (attribute sets)

#### Add Attribute

`UPCGAddAttributeSettings` · plugin `PCG`

[class] Add a new attribute to a spatial data or an attribute set. New attribute can be a constant, hardcoded in the node, or can come from another Attribute Set. Can also add all the attributes coming from the other Attribute Set.

[epic] Adds an attribute to point data or an attribute set.

**Pin data types detected:** in `Any, Param` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `!bCopyAllAttributes` |
| `OutputTarget` | `FPCGAttributePropertyOutputSelector` |  | ◆ | *Only when* `!bCopyAllAttributes` |
| `AttributeTypes` | `FPCGMetadataTypesConstantStruct` |  |  |  |
| ↳ `Type` | `EPCGMetadataTypes` | `EPCGMetadataTypes::Double` |  | *Options: 15 options* *Only when* `bAllowsTypeChange` |
| ↳ `FloatValue` | `float` | `0.0f` |  | All different types *Only when* `Type == EPCGMetadataTypes::Float` |
| ↳ `Int32Value` | `int32` | `0` |  | *Only when* `Type == EPCGMetadataTypes::Integer32` |
| ↳ `DoubleValue` | `double` | `0.0` |  | *Only when* `Type == EPCGMetadataTypes::Double` |
| ↳ `IntValue` | `int64` | `0` |  | *Only when* `Type == EPCGMetadataTypes::Integer64` |
| ↳ `Vector2Value` | `FVector2D` | `FVector2D::ZeroVector` |  | *Only when* `Type == EPCGMetadataTypes::Vector2` |
| ↳ `VectorValue` | `FVector` | `FVector::ZeroVector` |  | *Only when* `Type == EPCGMetadataTypes::Vector` |
| ↳ `Vector4Value` | `FVector4` | `FVector4::Zero()` |  | *Only when* `Type == EPCGMetadataTypes::Vector4` |
| ↳ `QuatValue` | `FQuat` | `FQuat::Identity` |  | *Only when* `Type == EPCGMetadataTypes::Quaternion` |
| ↳ `TransformValue` | `FTransform` | `FTransform::Identity` |  | *Only when* `Type == EPCGMetadataTypes::Transform` |
| ↳ `StringValue` | `FString` | `""` |  | *Only when* `Type == EPCGMetadataTypes::String` |
| ↳ `BoolValue` | `bool` | `false` |  | *Only when* `Type == EPCGMetadataTypes::Boolean` |
| ↳ `RotatorValue` | `FRotator` | `FRotator::ZeroRotator` |  | *Only when* `Type == EPCGMetadataTypes::Rotator` |
| ↳ `NameValue` | `FName` | `NAME_None` |  | *Only when* `Type == EPCGMetadataTypes::Name` |
| ↳ `SoftClassPathValue` | `FSoftClassPath` |  |  | *Only when* `Type == EPCGMetadataTypes::SoftClassPath` |
| ↳ `SoftObjectPathValue` | `FSoftObjectPath` |  |  | *Only when* `Type == EPCGMetadataTypes::SoftObjectPath` |
| `bCopyAllAttributes` | `bool` | `false` | ◆ |  |
| `bCopyAllDomains` | `bool` | `false` | ◆ | If checked, it is copying all attributes from all domains, as long as the source domain is supported on the target data. *Only when* `bCopyAllAttributes` |
| `MetadataDomainsMapping` | `TMap<FName, FName>` |  |  | When copying all attributes, a mapping can be specified. If it is empty, it's going to be Default -> Default. *Only when* `bCopyAllAttributes && !bCopyAllDomains` |

#### Create Constant

`UPCGCreateAttributeSetSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataTypes` value** — see section 4.

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `AttributeTypes` | `FPCGMetadataTypesConstantStruct` |  |  |  |
| ↳ `Type` | `EPCGMetadataTypes` | `EPCGMetadataTypes::Double` |  | *Options: 15 options* *Only when* `bAllowsTypeChange` |
| ↳ `FloatValue` | `float` | `0.0f` |  | All different types *Only when* `Type == EPCGMetadataTypes::Float` |
| ↳ `Int32Value` | `int32` | `0` |  | *Only when* `Type == EPCGMetadataTypes::Integer32` |
| ↳ `DoubleValue` | `double` | `0.0` |  | *Only when* `Type == EPCGMetadataTypes::Double` |
| ↳ `IntValue` | `int64` | `0` |  | *Only when* `Type == EPCGMetadataTypes::Integer64` |
| ↳ `Vector2Value` | `FVector2D` | `FVector2D::ZeroVector` |  | *Only when* `Type == EPCGMetadataTypes::Vector2` |
| ↳ `VectorValue` | `FVector` | `FVector::ZeroVector` |  | *Only when* `Type == EPCGMetadataTypes::Vector` |
| ↳ `Vector4Value` | `FVector4` | `FVector4::Zero()` |  | *Only when* `Type == EPCGMetadataTypes::Vector4` |
| ↳ `QuatValue` | `FQuat` | `FQuat::Identity` |  | *Only when* `Type == EPCGMetadataTypes::Quaternion` |
| ↳ `TransformValue` | `FTransform` | `FTransform::Identity` |  | *Only when* `Type == EPCGMetadataTypes::Transform` |
| ↳ `StringValue` | `FString` | `""` |  | *Only when* `Type == EPCGMetadataTypes::String` |
| ↳ `BoolValue` | `bool` | `false` |  | *Only when* `Type == EPCGMetadataTypes::Boolean` |
| ↳ `RotatorValue` | `FRotator` | `FRotator::ZeroRotator` |  | *Only when* `Type == EPCGMetadataTypes::Rotator` |
| ↳ `NameValue` | `FName` | `NAME_None` |  | *Only when* `Type == EPCGMetadataTypes::Name` |
| ↳ `SoftClassPathValue` | `FSoftClassPath` |  |  | *Only when* `Type == EPCGMetadataTypes::SoftClassPath` |
| ↳ `SoftObjectPathValue` | `FSoftObjectPath` |  |  | *Only when* `Type == EPCGMetadataTypes::SoftObjectPath` |
| `OutputTarget` | `FPCGAttributePropertyOutputNoSourceSelector` |  | ◆ |  |

#### Data Tags To Attribute Set

`UPCGTagsToAttributeSetSettings` · plugin `PCG` · internal name `TagsToAttributeSet`

[src] Extracts the tags on the data to an attribute set.

**Pin data types detected:** in `default` → out `Param`

*No editable settings declared.*

#### Get Actor Property

`UPCGGetActorPropertySettings` · plugin `PCG`

[class] Extract a property value from an actor/component into a ParamData.

[epic] Retrieves the contents of a property from the actor holding the PCG component (or higher in the object hierarchy). By default, it looks at actor-level properties (useful for Blueprint variables), but it can look at component properties as well using the Select Component option. This property can hold a "flat" struct (such as one with no arrays) or be an array of a valid supported type. In the case of an array, then the output will be an Attribute Set with multiple entries. This node is useful to retrieve data from actors in the world (self or otherwise) to allow for per-instance control in the graph, using the same interface as the Get Actor Data. This could, for example, hold a list of static meshes to spawn material sand more.

**Pin data types detected:** in `Any` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorSelector` | `FPCGActorSelectorSettings` |  | ◆ |  |
| ↳ `ActorFilter` | `EPCGActorFilter` | `EPCGActorFilter::Self` |  | Which actors to consider. *Options: Self · Parent · Root · AllWorldActors · Original · FromInput* *Only when* `bShowActorFilter` |
| ↳ `bMustOverlapSelf` | `bool` | `false` |  | Filters out actors that do not overlap the source component bounds. *Only when* `ActorFilter==EPCGActorFilter::AllWorldActors` |
| ↳ `bIncludeChildren` | `bool` | `false` |  | Whether to consider child actors. *Only when* `bShowIncludeChildren && ActorFilter!=EPCGActorFilter::AllWorldActors` |
| ↳ `bDisableFilter` | `bool` | `false` |  | Enables/disables fine-grained actor filtering options. *Only when* `ActorFilter!=EPCGActorFilter::AllWorldActors && bIncludeChildren` |
| ↳ `ActorSelection` | `EPCGActorSelection` | `EPCGActorSelection::ByTag` |  | How to select when filtering actors. *Options: ByTag · ByClass* *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter))` |
| ↳ `ActorSelectionTag` | `FName` |  |  | Tag to match against when filtering actors. *Only when* `bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) && ActorSelection==EPCGActo …` |
| ↳ `ActorSelectionClass` | `class AActor` |  |  | Actor class to match against when filtering actors. *Only when* `bShowActorSelectionClass && bShowActorSelection && (ActorFilter==EPCGActorFilter::AllWorldActors \|\| (bIncludeChildren && !bDisableFilter)) …` |
| ↳ `ActorReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | Controls what attribute to read from when the actor selector uses the "FromInput" actor filter. *Only when* `ActorFilter==EPCGActorFilter::FromInput` |
| ↳ `bSelectMultiple` | `bool` | `false` |  | If true processes all matching actors, otherwise returns data from first match. *Only when* `bShowSelectMultiple && ActorFilter==EPCGActorFilter::AllWorldActors && ActorSelection!=EPCGActorSelection::ByName` |
| ↳ `bIgnoreSelfAndChildren` | `bool` | `false` |  | If true, ignores results found from within this actor's hierarchy. *Only when* `bShowIgnoreSelfAndChildren && ActorFilter==EPCGActorFilter::AllWorldActors` |
| `bSelectComponent` | `bool` | `false` | ◆ | Allow to look for an actor component instead of an actor. It will need to be attached to the found actor. |
| `ComponentClass` | `class UActorComponent` |  | ◆ | If we are looking for an actor component, the class can be specified here. *Only when* `bSelectComponent` |
| `bProcessAllComponents` | `bool` | `false` | ◆ | Process all Actor components. If not set, only the first component found will be processed. *Only when* `bSelectComponent` |
| `bOutputComponentReference` | `bool` | `false` | ◆ | Controls whether a component reference attribute will be added to the result *Only when* `bSelectComponent` |
| `PropertyName` | `FName` | `NAME_None` | ◆ | Property name to extract. Can only extract properties that are compatible with metadata types. If None, extract the actor/component directly. Can be a comma-separated list, assuming they have the same cardinality. |
| `bForceObjectAndStructExtraction` | `bool` | `false` | ◆ | If the property is a struct/object supported by metadata, this option can be toggled to force extracting all (compatible) properties contained in this property. Automatically true if unsupported by metadata. For now, only supports direct child properties (and not deeper). |
| `OutputAttributeName` | `FPCGAttributePropertyOutputSelector` |  | ◆ | In the case of multiple properties being extracted, will be ignored. *Only when* `!bForceObjectAndStructExtraction` |
| `bSanitizeOutputAttributeName` | `bool` | `true` |  | If the output attribute name has special characters, remove them. |
| `bOutputActorReference` | `bool` | `false` | ◆ | Controls whether an actor reference attribute will be added to the result |
| `bAlwaysRequeryActors` | `bool` | `true` |  | If this is true, we will never put this element in cache, and will always try to re-query the actors and read the latest properties from them. |
| `bTrackActorsOnlyWithinBounds` | `bool` | `false` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. |

#### Get Attribute List

`UPCGGetAttributesSettings` · plugin `PCG`

[src] Creates an attribute set with one entry per attribute on the input data.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bGetType` | `bool` | `false` |  | Controls whether the attribute types will be extracted into the 'Type' attribute (as a name). |
| `bGetDefaultValue` | `bool` | `false` |  | Controls whether the default value for the attribute will be extracted into the 'DefaultValue' attribute (as a string). |

#### Get Attribute Set from Index

`UPCGAttributeGetFromIndexSettings` · plugin `PCG` · internal name `GetAttributeFromIndex`

[src] Retrieves a single entry from an Attribute Set.

**Pin data types detected:** in `Param` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Index` | `int32` | `0` | ◆ |  |

#### Get Property From Object Path

`UPCGGetPropertyFromObjectPathSettings` · plugin `PCG`

[class] Extract property from a list of soft object paths.

[epic] Retrieves the contents of a property from the actor holding the PCG component (or higher in the object hierarchy). This is similar to the Get Actor Property node except that it can take actor references (soft object paths) through an Attribute Set. This node is useful in data-driven use cases where a data table could hold references to actors and could easily retrieve properties from these as needed without having to rely on actor selection.

**Pin data types detected:** in `Param` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ObjectPathsToExtract` | `TArray<FSoftObjectPath>` |  |  | If nothing is connected in the In pin, will use those static paths to load. |
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | If something is connected in the In pin, will look for this attribute values to load. |
| `PropertyName` | `FName` | `NAME_None` | ◆ | Property name to extract. Can only extract properties that are compatible with metadata types. If None, extract the object. |
| `bForceObjectAndStructExtraction` | `bool` | `false` |  | If the property is a struct/object supported by metadata, this option can be toggled to force extracting all (compatible) properties contained in this property. Automatically true if unsupported by metadata. For now, only supports direct child properties (and not deeper). |
| `OutputAttributeName` | `FPCGAttributePropertyOutputSelector` |  | ◆ | In the case of multiple properties being extracted, will be ignored. *Only when* `!bForceObjectAndStructExtraction` |
| `bSanitizeOutputAttributeName` | `bool` | `true` |  | If the output attribute name has special characters, remove them. |
| `bSynchronousLoad` | `bool` | `false` |  | By default, object loading is asynchronous, can force it synchronous if needed. |
| `bPersistAllData` | `bool` | `false` |  | Opt-in option to create empty data when there is nothing to extract or property is not found, to have the same number of inputs than outputs. |
| `bSilenceErrorOnEmptyObjectPath` | `bool` | `false` |  | Opt-in option to silence errors when the path is Empty or nothing to extract. |

#### Get Tags

`UPCGGetTagsSettings` · plugin `PCG`

[src] Creates an attribute set with one entry per tag

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bExtractTagValues` | `bool` | `false` |  | Creates a 'Values' attribute and stores the values of the valued tags (e.g. 'Tag:Value' tags) as a string. |

#### Point To Attribute Set

`UPCGConvertToAttributeSetSettings` · plugin `PCG`

[src] Converts point data to an attribute set with one entry per point and the same attributes.

[epic] Converts a Point Data to Attribute Set by dropping all of the point properties and keeping only the point attributes. If the input Point Data has no attribute, then no Attribute Set will be output. This node can be useful as an optimization in either processing or memory in certain cases, or to homogenize data types across the graph.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PropertiesToConvert` | `TMap<FPCGAttributePropertyInputSelector, FPCGAttributePropertyOutputSe …` |  | ◆ | Can add properties to convert at the same time, with a potential remap. |
| `bOverrideExistingAttributes` | `bool` | `false` | ◆ | If properties are converted and there is already an attribute with the same name, it can be overridden by the property. |

### ▸ Spawner

#### Create Target Actor

`UPCGCreateTargetActor` · plugin `PCG`

[epic] Creates an empty actor from a template that can be used as a target for writing PCG artifacts to, such as the Static Mesh Spawner.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `TemplateActor` | `AActor` |  |  | *Only when* `bAllowTemplateActorEditing` |
| `AttachOptions` | `EPCGAttachOptions` | `EPCGAttachOptions::Attached` |  | *Options: NotAttached · Attached · InFolder · InGraphFolder · InGeneratedFolder* |
| `CommaSeparatedActorTags` | `FString` |  | ◆ | Comma-separated list of tags to add to the newly created target actor. |
| `PropertyOverrideDescriptions` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | Override the default property values on the created target actor. Applied before post-process functions. |
| `PostProcessFunctionNames` | `TArray<FName>` |  |  | Specify a list of functions to be called on the target actor after creation. Functions need to be parameter-less and with "CallInEditor" flag enabled. |
| `DataLayerSettings` | `FPCGDataLayerSettings` |  | ◆ |  |
| ↳ `DataLayerSourceType` | `EPCGDataLayerSource` | `EPCGDataLayerSource::Self` |  | What source should be used to assign Data Layers to the spawned actor *Options: Self · DataLayerReferences* |
| ↳ `DataLayerReferenceAttribute` | `FPCGAttributePropertyInputSelector` |  |  | *Only when* `DataLayerSourceType==EPCGDataLayerSource::DataLayerReferences` |
| ↳ `IncludedDataLayers` | `FPCGDataLayerReferenceSelector` |  |  | When left empty, all Data Layers from the Data Layer Source are included, if any Data Layers are specified, only those will be included |
| ↳ `ExcludedDataLayers` | `FPCGDataLayerReferenceSelector` |  |  | Specified Data Layers will get excluded from the Data Layer Source |
| ↳ `AddDataLayers` | `FPCGDataLayerReferenceSelector` |  |  | Specified Data Layers will get added |
| `HLOD Settings` | `FPCGHLODSettings` |  | ◆ |  |
| ↳ `HLODSourceType` | `EPCGHLODSource` | `EPCGHLODSource::Self` |  | What source should be used to assign HLOD Layer to the spawned actor *Options: Self · Reference · Template* |
| ↳ `HLODLayer` | `UHLODLayer` |  |  | *Only when* `HLODSourceType==EPCGHLODSource::Reference` |
| `bDeleteActorsBeforeGeneration` | `bool` | `false` |  |  |
| `TemplateActorClass` | `class AActor` |  |  |  |
| `bAllowTemplateActorEditing` | `bool` | `false` |  | TODO: make this InlineEditConditionToggle, not done because property changed event does not propagate correctly so we can't track accurately the need to create the target actor |

#### Instanced Skinned Mesh Spawner

`UPCGSkinnedMeshSpawnerSettings` · plugin `PCG` · internal name `SkinnedMeshSpawner`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

**Pin data types detected:** in `Point` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InstanceDataPackerType` | `class UPCGSkinnedMeshInstanceDataPackerBase` |  |  | Defines the method of custom data packing for spawned anim bank meshes. Note, Rotators are treated as 3 floats, while Quaternions are treated as 4 floats. You can see an attribute's type in the 'Attribute List View' window, and use an 'Attribute Cast' node to cast to the desired type. |
| `SkinnedMeshComponentPropertyOverrides` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | Map an attribute directly to an anim bank descriptor property, the value of which will be overriden when generated. Note: Currently only enabled using SelectByAttribute mesh selection. |
| `bApplyMeshBoundsToPoints` | `bool` | `true` |  | Sets the BoundsMin and BoundsMax attributes of each point to reflect the AnimBank mesh spawned at its location |
| `PostProcessFunctionNames` | `TArray<FName>` |  |  | Specify a list of functions to be called on the target actor after instances are spawned. Functions need to be parameter-less and with "CallInEditor" flag enabled. |
| `bSynchronousLoad` | `bool` | `false` |  | Meshes/Materials will be synchronously loaded before spawning instead of asynchronously. |
| `bSilenceOverrideAttributeNotFoundErrors` | `bool` | `false` |  | Opt-in option to silence errors when the property override attributes are not found. |
| `bWarnOnIdenticalSpawn` | `bool` | `true` |  | Adds a warning to the node on repeated spawning with identical conditions (ie. same mesh descriptor at same spawn location, etc). |

#### Spawn Instanced Actors  🧪 Experimental

`UPCGSpawnInstancedActorsSettings` · plugin `PCGInstancedActorsInterop`

[src] Spawns instanced actors from the input data. Note that the actor classes should be previously registered and that this node does not work at runtime.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bSpawnByAttribute` | `bool` | `false` | ◆ | Controls whether the actor class to use will be driven by an attribute on the input data. |
| `SpawnAttributeSelector` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute specifier for the attribute class to spawn. *Only when* `bSpawnByAttribute` |
| `ActorClass` | `class AActor` |  | ◆ | Actor class to spawn when not using the 'Spawn by Attribute' mode. *Only when* `!bSpawnByAttribute` |
| `bMuteOnEmptyClass` | `bool` | `false` | ◆ | Mutes warnings on empty class, which can be useful when some points might not have a valid class. |

#### Spawn Spline Component

`UPCGSpawnSplineSettings` · plugin `PCG`

[class] Spawn a spline component from a spline data.

**Pin data types detected:** in `Spline` → out `Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SplineComponent` | `class USplineComponent` | `USplineComponent::StaticClass()` | ◆ | Class of the component to spawn, must be a subclass of Spline Component. |
| `bSpawnComponentFromAttribute` | `bool` | `false` | ◆ |  |
| `SpawnComponentFromAttributeName` | `FPCGAttributePropertyInputSelector` |  | ◆ | If the class of the component to spawn is coming from an attribute. |
| `PostProcessFunctionNames` | `TArray<FName>` |  |  | Specify a list of functions to be called on the target actor after spline creation. Functions need to be parameter-less and with "CallInEditor" flag enabled. |
| `PropertyOverrideDescriptions` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | Overrides to apply on the spawned component. |
| `bOutputSplineComponentReference` | `bool` | `true` | ◆ |  |
| `ComponentReferenceAttributeName` | `FName` | `PCGAddComponentConstants::ComponentReferenceAttribute` | ◆ | Can output the spawned component reference in an attribute. |

#### Spawn Spline Mesh

`UPCGSpawnSplineMeshSettings` · plugin `PCG`

[src] Create a USplineMeshComponent for each segment along a given spline.

**Pin data types detected:** in `PolyLine` → out `PolyLine`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SplineMeshDescriptor` | `FSoftSplineMeshComponentDescriptor` |  |  |  |
| `SplineMeshParams` | `FPCGSplineMeshParams` |  | ◆ |  |
| ↳ `ForwardAxis` | `EPCGSplineMeshForwardAxis` | `EPCGSplineMeshForwardAxis::X` | ◆ | Chooses the forward axis for the spline mesh orientation. *Options: X · Y · Z* |
| ↳ `bScaleMeshToBounds` | `bool` | `false` | ◆ | Scale mesh to the spline control point bounds. Especially useful on Landscape Splines, where the bounds come from the width. |
| ↳ `bScaleMeshToLandscapeSplineFullWidth` | `bool` | `false` | ◆ | Scale the mesh to the full width of the Landscape Spline (including Falloff). Only applies to Landscape Splines. *Only when* `bScaleMeshToBounds` |
| ↳ `SplineUpDir` | `FVector` | `FVector(0.0, 0.0, 1.0)` | ◆ | Axis (in component space) that is used to determine X axis for coordinates along spline. |
| ↳ `NaniteClusterBoundsScale` | `float` | `1.0f` | ◆ | How much to scale the calculated culling bounds of Nanite clusters after deformation. NOTE: This should only be set greater than 1.0 if it fixes visible issues with clusters being incorrectly culled. |
| ↳ `SplineBoundaryMin` | `float` | `0.0f` | ◆ | Minimum coordinate along the spline forward axis which corresponds to start of spline. If set to 0.0, will use bounding box to determine bounds. |
| ↳ `SplineBoundaryMax` | `float` | `0.0f` | ◆ | Maximum coordinate along the spline forward axis which corresponds to end of spline. If set to 0.0, will use bounding box to determine bounds. |
| ↳ `bSmoothInterpRollScale` | `bool` | `true` | ◆ | If true, will use smooth interpolation (ease in/out) for Scale, Roll, and Offset along this section of spline. If false, uses linear. |
| ↳ `StartOffset` | `FVector2D` | `FVector2D::ZeroVector` | ◆ | Starting offset of the mesh from the spline, in component space. |
| ↳ `EndOffset` | `FVector2D` | `FVector2D::ZeroVector` | ◆ | Ending offset of the mesh from the spline, in component space. |
| `PostProcessFunctionNames` | `TArray<FName>` |  |  | Specify a list of functions to be called on the target actor after spline mesh creation. Functions need to be parameter-less and with "CallInEditor" flag enabled. |
| `bSynchronousLoad` | `bool` | `false` |  | Force meshes/materials to load synchronously. |
| `SplineMeshOverrideDescriptions` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | Overrides for spline mesh descriptor. |
| `SplineMeshParamsOverride` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | Overrides for spline mesh params. |
| `SplineMeshComponentOverride` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | Overrides for the spline mesh component. |

#### Static Mesh Spawner  ★

`UPCGStaticMeshSpawnerSettings` · plugin `PCG`

[epic] Spawn one static mesh per point in the provided point data. Static Mesh options are added to the Mesh Entries array and selected using each entry's Weight. This is done by taking the sum of all the weight values and converting them to a percentage for each entry. For example, if there are four entries in the array that each have a value of 1, the value of the sum is 4. Each entry's weight is then divided by the sum and converted to a percentage. This means each entry has a 25% chance of spawning. Selection of the static mesh is done using variations based on the selected Mesh Selector Type option. It contains the following options: PCG Mesh Selector Weighted: Selects an entry based on the total weight of entries. PCG Mesh Selector By Attribute: Selects an entry based on an attribute present on the mesh. PCG Mesh Selector Weighted By Category: Selects a category by looking up an Attribute …

**Pin data types detected:** in `Point` → out `default`

★ **This project:** `PCG_SurfaceTest` (L5)

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `MeshSelectorType` | `class UPCGMeshSelectorBase` |  |  | Defines the method of mesh selection per input data |
| `bAllowDescriptorChanges` | `bool` | `true` |  | Allows PCG to make some changes on the descriptors as situation arises (using ISM instead of HISM for nanite meshes, etc.) |
| `InstanceDataPackerType` | `class UPCGInstanceDataPackerBase` |  |  | Defines the method of custom data packing for spawned (H)ISMCs. Note, Rotators are treated as 3 floats, while Quaternions are treated as 4 floats. You can see an attribute's type in the 'Attribute List View' window, and use an 'Attribute Cast' node to cast to the desired type. |
| `StaticMeshComponentPropertyOverrides` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | Map an attribute directly to an ISM Descriptor property, the value of which will be overriden when generated. Note: Currently only enabled using SelectByAttribute mesh selection. |
| `OutAttributeName` | `FName` | `NAME_None` |  | Attribute name to store mesh SoftObjectPaths inside if the output pin is connected. Note: Will overwrite existing data if the attribute name already exists. |
| `bApplyMeshBoundsToPoints` | `bool` | `true` |  | Sets the BoundsMin and BoundsMax attributes of each point to reflect the StaticMesh spawned at its location |
| `PostProcessFunctionNames` | `TArray<FName>` |  |  | Specify a list of functions to be called on the target actor after instances are spawned. Functions need to be parameter-less and with "CallInEditor" flag enabled. |
| `bSynchronousLoad` | `bool` | `false` |  | Meshes/Materials will be synchronously loaded before spawning instead of asynchronously. |
| `bAllowMergeDifferentDataInSameInstancedComponents` | `bool` | `true` | ◆ | Controls whether instances stemming from different data can end up in the same ISM. Performance warning if set to false. |
| `bSilenceOverrideAttributeNotFoundErrors` | `bool` | `false` |  | Opt-in option to silence errors when the property override attributes are not found. |
| `bWarnOnIdenticalSpawn` | `bool` | `true` |  | Adds a warning to the node on repeated spawning with identical conditions (ie. same mesh descriptor at same spawn location, etc). |

### ▸ Control Flow

#### Branch

`UPCGBranchSettings` · plugin `PCG`

[src] Control flow node that will route the input to either Output A or Output B, based on the 'Output To B' property - which can also be overridden.

[epic] Selects one of two outputs based on a Boolean attribute. This allows the provided data to pass to either the "Output A" or "Output B" based on a boolean value that can be overridden in the graph. Controls execution flow tthrough the graph so that depending on specific circumstances (presence or absence of something, platform running, and so on) some different parts of a graph are executed. The branch that does not have any data is culled from execution in order to perform more efficiently.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bOutputToB` | `bool` | `false` | ◆ |  |

#### Runtime Quality Branch

`UPCGQualityBranchSettings` · plugin `PCG`

[src] Control flow node that dynamically routes input data based on 'pcg.Quality' setting.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bUseLowPin` | `bool` | `false` | ◆ |  |
| `bUseMediumPin` | `bool` | `false` | ◆ |  |
| `bUseHighPin` | `bool` | `false` | ◆ |  |
| `bUseEpicPin` | `bool` | `false` | ◆ |  |
| `bUseCinematicPin` | `bool` | `false` | ◆ |  |

#### Runtime Quality Select

`UPCGQualitySelectSettings` · plugin `PCG`

[src] Selects from input pins based on 'pcg.Quality' setting.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bUseLowPin` | `bool` | `false` | ◆ |  |
| `bUseMediumPin` | `bool` | `false` | ◆ |  |
| `bUseHighPin` | `bool` | `false` | ◆ |  |
| `bUseEpicPin` | `bool` | `false` | ◆ |  |
| `bUseCinematicPin` | `bool` | `false` | ◆ |  |

#### Select

`UPCGBooleanSelectSettings` · plugin `PCG`

[src] Control flow node that will select all input data on either Pin A or Pin B only, based on the 'Use Input B' property - which can also be overridden.

[epic] Selects one of two inputs to be forwarded to a single output based on a Boolean attribute. This is used to control execution flow in the graph so that depending on specific circumstances (presence or absence of something, platform running, and so on) some different parts of a graph are executed. Select branches (inputs) are not culled from execution at this point but may be in a future release.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bUseInputB` | `bool` | `false` | ◆ |  |

#### Select (Multi)

`UPCGMultiSelectSettings` · plugin `PCG`

[src] Control flow node that will select all input data on a single input pin that matches a given selection mode and corresponding 'selection' property - which can also be overridden.

[epic] Multi-input version of the Select node, which can be made to be an integer, enum, or string-based. This node is especially useful to make it more obvious in the graph when picking different data. It removes some of the "magic number" impression, or in cases where there are more than two inputs to select from.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SelectionMode` | `EPCGControlFlowSelectionMode` | `EPCGControlFlowSelectionMode::Integer` |  | Determines the type of value to be used to select an input. *Options: Integer · Enum · String* |
| `IntegerSelection` | `int32` | `0` | ◆ | Determines which input will be selected if the selection mode is Integer. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::Integer` |
| `IntOptions` | `TArray<int32>` | `{0}` |  | Determines the available input pin selection options. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::Integer` |
| `StringSelection` | `FString` |  | ◆ | Determines which input will be selected if the selection mode is String. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::String` |
| `StringOptions` | `TArray<FString>` |  |  | Determines the available input pin selection options. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::String` |
| `EnumSelection` | `FEnumSelector` |  | ◆ | Determines which input pin will be selected if the selection mode is Enum. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::Enum` |

#### Switch

`UPCGSwitchSettings` · plugin `PCG`

[src] Control flow node that passes through input data to a specific output pin that matches a given selection mode and corresponding 'selection' property - which can also be overridden.

[epic] Multi-output version of the Branch node, which can be made to pick an integer, string, or enum. This node is especially useful to make it more obvious in the graph when picking different data. It removes some of the "magic number" impression, or in cases where there are more than two inputs to select from.

**Pin data types detected:** in `Any` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SelectionMode` | `EPCGControlFlowSelectionMode` | `EPCGControlFlowSelectionMode::Integer` |  | Determines the type of value to be used to select an output. *Options: Integer · Enum · String* |
| `IntegerSelection` | `int32` | `0` | ◆ | Determines which output will be selected if the selection mode is Integer. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::Integer` |
| `IntOptions` | `TArray<int32>` | `{0}` |  | Determines the available output pin selection options. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::Integer` |
| `StringSelection` | `FString` |  | ◆ | Determines which output will be selected if the selection mode is String. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::String` |
| `StringOptions` | `TArray<FString>` |  |  | Determines the available output pin selection options. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::String` |
| `EnumSelection` | `FEnumSelector` |  | ◆ | Determines which output pin will be selected if the selection mode is Enum. *Only when* `SelectionMode == EPCGControlFlowSelectionMode::Enum` |

### ▸ Subgraph

#### Loop

`UPCGLoopSettings` · plugin `PCG`

[src] Executes the specified Subgraph for each data on the loop pins (or on the first pin if no specific loop pins are provided), keeping the rest constant.

[epic] Executes another graph as a subgraph, once per data in the loop pins. Non-loop pins are passed as-is. Pin properties are set up on the input & output nodes in each graph. The usage of the pins will drive their behavior when executed in a Loop. Feedback pins have a special behavior such that they should be paired with another of the same name in the output. During execution, the first iteration will receive the data on the feedback pin from the calling graph, but subsequent iterations will get the data from the previous iteration. This node is extremely important to simplify local processing on the same kind of data, for example by allowing sampling on a single mesh (with the Mesh Sampler node) then copying that data only on the relevant data. It is also used to build data sets that have interdependencies on them (sequences of selection & exclusions) and the like.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bUseGraphDefaultPinUsage` | `bool` | `true` |  | Controls whether the pin usage (normal, loop, feedback) will be taken from the subgraph to execute or from the manually provided list. |
| `LoopPins` | `FString` |  |  | Comma-separated list of pin names on which we will loop by-element in a step-wise fashion; if more than one is provided, it is expected that they all have the same number of data. If none are provided, the first connected pin will taken as the pin to loop on. *Only when* `!bUseGraphDefaultPinUsage` |
| `FeedbackPins` | `FString` |  |  | Comma-separated list of pin names that will act as feedback pins, namely that in a given iteration it will receive the data from the output pin of the same name of the previous loop iteration. These pins can have initial data, in which case only the first iteration will get this data. *Only when* `!bUseGraphDefaultPinUsage` |
| `bTokenizeOnWhiteSpace` | `bool` | `false` |  | *Only when* `bTokenizeOnWhiteSpace` |

#### Spawn Actor

`UPCGSpawnActorSettings` · plugin `PCG`

[epic] Spawns either the contents of an actor or an actor per point in the provided input data. The actor is driven by the template actor class or the instanced templated actor or by attribute depending on the settings. It contains the following options: Template Actor Class: List of available Actors in your project. Option: Collapse Actors: Gathers some of the actor components (Static Mesh Components and PCG Components) and acts collapsed inside of the target actor. Merge PCG only: Spawns one actor per point If the spawned actor has a PCG component, its inputs are bundled into a single graph execution. No Merging: Spawns one actor per point. In the No Merging case, it is possible to set properties to the actors from attributes on the points through the ‘Spawned Actor Property Override Descriptions’. Attach mode: Not attached: No engine-aware relationship will exist between the original actor ( …

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PostSpawnFunctionNames` | `TArray<FName>` |  |  | Can specify a list of functions from the template class to be called on each actor spawned, in order. Need to have "CallInEditor" flag enabled and have either no parameters or exactly the parameters PCGPoint and PCGMetadata *Only when* `Option!=EPCGSpawnActorOption::CollapseActors` |
| `Option` | `EPCGSpawnActorOption` | `EPCGSpawnActorOption::CollapseActors` |  | Controls how actors are spawned; collapsed in more efficient components or as-is with generation or not. Note that new nodes now have the 'No Merging' option by default. *Options: CollapseActors · MergePCGOnly · NoMerging* |
| `bForceDisableActorParsing` | `bool` | `true` |  | *Only when* `Option==EPCGSpawnActorOption::NoMerging` |
| `GenerationTrigger` | `EPCGSpawnActorGenerationTrigger` | `EPCGSpawnActorGenerationTrigger::Default` |  | *Options: Default · ForceGenerate · DoNotGenerateInEditor · DoNotGenerate* *Only when* `Option==EPCGSpawnActorOption::NoMerging` |
| `bInheritActorTags` | `bool` | `false` |  | Warning: inheriting parent actor tags work only in non-collapsed actor hierarchies *Only when* `Option!=EPCGSpawnActorOption::CollapseActors` |
| `TagsToAddOnActors` | `TArray<FName>` |  |  | *Only when* `Option!=EPCGSpawnActorOption::CollapseActors` |
| `TemplateActor` | `AActor` |  |  | *Only when* `bAllowTemplateActorEditing && Option != EPCGSpawnActorOption::CollapseActors` |
| `SpawnedActorPropertyOverrideDescriptions` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | *Only when* `Option != EPCGSpawnActorOption::CollapseActors` |
| `AttachOptions` | `EPCGAttachOptions` | `EPCGAttachOptions::Attached` |  | Controls where spawned actors will appear in the Outliner. Note that attaching actors to an actor couples their streaming. Note that new nodes now have the 'In Folder' option by default. *Options: NotAttached · Attached · InFolder · InGraphFolder · InGeneratedFolder* *Only when* `Option != EPCGSpawnActorOption::CollapseActors` |
| `bSpawnByAttribute` | `bool` | `false` |  |  |
| `SpawnAttribute` | `FName` | `NAME_None` |  | *Only when* `bSpawnByAttribute` |
| `bWarnOnIdenticalSpawn` | `bool` | `true` |  | Adds a warning to the node on repeated spawning with identical conditions (ie. same actor at same spawn location, etc). |
| `bDeleteActorsBeforeGeneration` | `bool` | `false` |  |  |
| `DataLayerSettings` | `FPCGDataLayerSettings` |  | ◆ |  |
| ↳ `DataLayerSourceType` | `EPCGDataLayerSource` | `EPCGDataLayerSource::Self` |  | What source should be used to assign Data Layers to the spawned actor *Options: Self · DataLayerReferences* |
| ↳ `DataLayerReferenceAttribute` | `FPCGAttributePropertyInputSelector` |  |  | *Only when* `DataLayerSourceType==EPCGDataLayerSource::DataLayerReferences` |
| ↳ `IncludedDataLayers` | `FPCGDataLayerReferenceSelector` |  |  | When left empty, all Data Layers from the Data Layer Source are included, if any Data Layers are specified, only those will be included |
| ↳ `ExcludedDataLayers` | `FPCGDataLayerReferenceSelector` |  |  | Specified Data Layers will get excluded from the Data Layer Source |
| ↳ `AddDataLayers` | `FPCGDataLayerReferenceSelector` |  |  | Specified Data Layers will get added |
| `HLOD Settings` | `FPCGHLODSettings` |  | ◆ |  |
| ↳ `HLODSourceType` | `EPCGHLODSource` | `EPCGHLODSource::Self` |  | What source should be used to assign HLOD Layer to the spawned actor *Options: Self · Reference · Template* |
| ↳ `HLODLayer` | `UHLODLayer` |  |  | *Only when* `HLODSourceType==EPCGHLODSource::Reference` |
| `TemplateActorClass` | `class AActor` |  |  |  |
| `bAllowTemplateActorEditing` | `bool` | `false` |  | *Only when* `Option != EPCGSpawnActorOption::CollapseActors` |

#### Subgraph  ★

`UPCGSubgraphSettings` · plugin `PCG`

[epic] Executes another graph as a subgraph. Note that a graph can call itself recursively; the graph will execute until this Subgraph node is culled from execution (because of Control Flow nodes) or when it has no input data. Subgraph nodes are a major element in reducing graph complexity and maximizing reuse. They also enable recursivity which can be useful in some circumstances.

★ **This project:** `PCG_SurfaceTest` -> `SG_SurfaceSource`

*No editable settings declared.*

### ▸ Graph Parameters

#### Get Graph Parameter  ★

`UPCGUserParameterGetSettings` · plugin `PCG`

**One palette entry per `EPCGMetadataTypes` value** — see section 4.

[class] Getter for user parameters defined in PCGGraph, by the user. Will pick up the value from the graph instance.

**Pin data types detected:** in `default` → out `Param`

★ **This project:** L0 — reads the 8 subgraph parameters

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bForceObjectAndStructExtraction` | `bool` | `false` |  | If the property is a struct/object supported by metadata, this option can be toggled to force extracting all (compatible) properties contained in this property. Automatically true if unsupported by metadata. For now, only supports direct child properties (and not deeper). |
| `bSanitizeOutputAttributeName` | `bool` | `true` |  | If the output attribute name has special characters, remove them. |

#### Get Graph Parameter

`UPCGGenericUserParameterGetSettings` · plugin `PCG`

[class] Generic getter for user parameter defined in the PCG Graph, by the user. Will pick up the value from the graph instance. This getter allows to set manually the user parameter they want to get, and add extractor, the same way than GetActorProperty or GetPropertyFromObjectPath

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PropertyPath` | `FString` |  | ◆ |  |
| `bForceObjectAndStructExtraction` | `bool` | `false` | ◆ | If the property is a struct/object supported by metadata, this option can be toggled to force extracting all (compatible) properties contained in this property. Automatically true if unsupported by metadata. For now, only supports direct child properties (and not deeper). |
| `bSanitizeOutputAttributeName` | `bool` | `true` |  | If the output attribute name has special characters, remove them. |
| `OutputAttributeName` | `FName` | `NAME_None` | ◆ |  |
| `Source` | `EPCGUserParameterSource` | `EPCGUserParameterSource::Current` |  | *Options: Current · Upstream · Root* |
| `bQuiet` | `bool` | `false` |  |  |

### ▸ Input / Output

#### Data Table Row To Attribute Set

`UPCGDataTableRowToParamDataSettings` · plugin `PCG`

[epic] Extracts a single row from a data table to an Attribute Set. This is a single-row access to a data table in a less flexible manner than what the Load Data Table enable, but can still be useful.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `RowName` | `FName` | `NAME_None` | ◆ | The name of the row to copy from |
| `DataTable` | `soft UDataTable` |  | ◆ | the data table to copy from |
| `bSynchronousLoad` | `bool` | `false` |  | By default, data table loading is asynchronous, can force it synchronous if needed. |

#### Export Selected Attributes

`UPCGExportSelectedAttributesSettings` · plugin `PCG` · internal name `PCGExportSelectedAttributes`

[src] Exports selected attributes directly to a file in a specified format.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Format` | `EPCGExportAttributesFormat` | `EPCGExportAttributesFormat::Binary` | ◆ | Data will be exported to a local file in this format. *Options: Binary · Json* |
| `Layout` | `EPCGExportAttributesLayout` | `EPCGExportAttributesLayout::ByElement` | ◆ | Determines how the data will be laid out in the export. *Options: ByElement · ByAttribute* *Only when* `Format != EPCGExportAttributesFormat::Binary` |
| `Path` | `FDirectoryPath` |  | ◆ | The directory to save the data within. If none is selected a dialog will open by default. |
| `FileName` | `FString` |  | ◆ | The file name (without extension) to export the data. |
| `bExportAllAttributes` | `bool` | `true` | ◆ |  |
| `AttributeSelectors` | `TArray<FPCGAttributePropertyInputSelector>` |  | ◆ | The attributes to use as sources for the data export. Only those selected will be exported from the input data. *Only when* `!bExportAllAttributes` |
| `bAddCustomDataVersion` | `bool` | `false` |  |  |
| `CustomVersion` | `int32` | `0` |  | Extra user version for any special requirements. Must be >= 0. *Only when* `bAddCustomDataVersion` |

#### Get Asset List

`UPCGGetAssetListSettings` · plugin `PCG`

[src] Returns the list of asset, with options (class, bp generated class, etc.) from a source - collection or folder.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `AssetListSource` | `EPCGAssetListSource` | `EPCGAssetListSource::Folder` | ◆ | Controls whether we will retrieve the files from a specified directory or from a collection. *Options: Folder · Collection* |
| `Directory` | `FDirectoryPath` |  | ◆ | Directory path to parse for assets. In 'long package name' format, e.g. '/Game/' and so on. *Only when* `AssetListSource == EPCGAssetListSource::Folder` |
| `Collection` | `FName` |  | ◆ | Name of the collection to parse for assets. *Only when* `AssetListSource == EPCGAssetListSource::Collection` |
| `bGetClassPath` | `bool` | `false` | ◆ | Controls whether the class path will also be exported as part of this node in the 'ClassPath' attribute. |
| `bQuiet` | `bool` | `false` | ◆ | Controls whether inexistant or empty collections will log a warning. |

#### Input Node  hidden in palette

`UPCGGraphInputOutputSettings` · plugin `PCG`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Pins` | `TArray<FPCGPinProperties>` |  |  | WITH_EDITOR ~End UPCGSettings interface |

#### Load Alembic  β Beta

`UPCGLoadAlembicSettings` · plugin `PCGExternalDataInterop`

[src] Loads data from an Alembic file

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `AlembicFilePath` | `FFilePath` |  | ◆ |  |
| `ConversionScale` | `FVector` | `FVector(1.0f, -1.0f, 1.0f)` | ◆ | Scale to apply during import. Note that for both Max/Maya presets the value flips the Y axis. |
| `ConversionRotation` | `FVector` | `FVector::ZeroVector` | ◆ | Rotation in Euler angles applied during import. For Max, use (90, 0, 0). |
| `bConversionFlipHandedness` | `bool` | `false` | ◆ | When changing handedness, it is sometimes needed to flip the rotation direction |
| `Setup from standard` | `EPCGLoadAlembicStandardSetup` | `EPCGLoadAlembicStandardSetup::None` |  | *Options: None · CitySample* |
| `AttributeMapping` | `TMap<FString, FPCGAttributePropertyInputSelector>` |  |  | *(from `UPCGExternalDataSettings`)* |

#### Load Data Table  ★

`UPCGLoadDataTableSettings` · plugin `PCG`

[src] Loads data from DataTable asset

[epic] Loads a UDataTable into PCG point data. This node can either import the table as Point Data or as an Attribute Set. This is extremely useful to make PCG data-driven without having to look at the PCG graph. Changes in the Data Table are propagated to PCG when the file is saved.

**Pin data types detected:** in `default` → out `Any`

★ **This project:** `PCG_SurfaceTest` — `DT_Modules`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `DataTable` | `soft UDataTable` |  | ◆ |  |
| `OutputType` | `EPCGExclusiveDataType` | `EPCGExclusiveDataType::Point` |  | *Options: 20 options* |
| `bSynchronousLoad` | `bool` | `false` |  | By default, data table loading is asynchronous, can force it synchronous if needed. |
| `AttributeMapping` | `TMap<FString, FPCGAttributePropertyInputSelector>` |  |  | *(from `UPCGExternalDataSettings`)* |

#### Load PCG Data Asset

`UPCGLoadDataAssetSettings` · plugin `PCG` · internal name `PCGLoadDataAsset`

[class] Loader/Executor of PCG data assets

[epic] Loads, either synchronously or asynchronously, a PCG Data Asset object and passes its data downstream in the graph.

**Pin data types detected:** in `Param` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Asset` | `soft UPCGDataAsset` |  | ◆ |  |
| `bLoadFromInput` | `bool` | `false` |  | WITH_EDITORONLY_DATA |
| `AssetReferenceSelector` | `FPCGAttributePropertyInputSelector` |  |  | *Only when* `bLoadFromInput` |
| `InputIndexTag` | `FName` | `NAME_None` |  | *Only when* `bLoadFromInput` |
| `DataIndexTag` | `FName` | `NAME_None` |  | *Only when* `bLoadFromInput` |
| `bSetDefaultAttributeOverridesFromInput` | `bool` | `false` |  | Exposes an attribute set pin to override defaults of the loaded data assets. |
| `DefaultAttributeOverrides` | `TArray<FString>` |  |  | List of Tag:Value default value overrides to apply on the loaded data assets. *Only when* `!bSetDefaultAttributeOverridesFromInput` |
| `bWarnIfNoAsset` | `bool` | `true` |  |  |
| `bSynchronousLoad` | `bool` | `false` |  | By default, data table loading is asynchronous, can force it synchronous if needed. |

#### Nanite Assembly Static Mesh Builder  🧪 Experimental

`UPCGNaniteAssemblyStaticMeshBuilderSettings` · plugin `PCGNaniteAssembliesInterop`

[src] [EXPERIMENTAL] Create a Static Mesh using Nanite assemblies from the input point data. Points are expected to be in local coordinates.

**Pin data types detected:** in `Point` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ExportParams` | `FPCGAssetExporterParameters` |  | ◆ |  |
| ↳ `bOpenSaveDialog` | `bool` | `true` |  | Controls whether we will open a Save... dialog, works only when a single level is exported. Overrides update anywhere. |
| ↳ `AssetName` | `FString` |  |  | Target asset path name |
| ↳ `AssetPath` | `FString` |  |  | Target asset path to write the PCG assets to. |
| ↳ `bSaveOnExportEnded` | `bool` | `true` |  | Controls whether the assets will be saved at the end of the process or not. |
| `MeshAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute for the mesh to spawn for a given point. |
| `MaterialOverrides` | `TArray<FPCGAttributePropertyInputSelector>` |  |  | Array of attributes for material overrides. 1 Attribute per slot. |
| `bSynchronousLoad` | `bool` | `false` |  | Meshes/Materials will be synchronously loaded before spawning instead of asynchronously. |

#### Save PCG Data Asset

`UPCGSaveDataAssetSettings` · plugin `PCG` · internal name `PCGSaveDataAsset`

[src] Exports the input data to a PCG Data Asset.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Pins` | `TArray<FPCGPinProperties>` |  |  |  |
| `CustomDataCollectionExporterClass` | `class UPCGDataCollectionExporter` |  |  |  |
| `Params` | `FPCGAssetExporterParameters` |  | ◆ |  |
| ↳ `bOpenSaveDialog` | `bool` | `true` |  | Controls whether we will open a Save... dialog, works only when a single level is exported. Overrides update anywhere. |
| ↳ `AssetName` | `FString` |  |  | Target asset path name |
| ↳ `AssetPath` | `FString` |  |  | Target asset path to write the PCG assets to. |
| ↳ `bSaveOnExportEnded` | `bool` | `true` |  | Controls whether the assets will be saved at the end of the process or not. |
| `AssetDescription` | `FString` |  | ◆ |  |
| `AssetColor` | `FLinearColor` | `FLinearColor::White` | ◆ |  |

#### Save Texture to Asset

`UPCGSaveTextureToAssetSettings` · plugin `PCG`

[src] Save the input texture to a UTexture2D asset (format is always BGRA8). Outputs a soft object path attribute for the saved texture. Note: This node is editor only.

**Pin data types detected:** in `BaseTexture` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ExporterParams` | `FPCGAssetExporterParameters` |  | ◆ |  |
| ↳ `bOpenSaveDialog` | `bool` | `true` |  | Controls whether we will open a Save... dialog, works only when a single level is exported. Overrides update anywhere. |
| ↳ `AssetName` | `FString` |  |  | Target asset path name |
| ↳ `AssetPath` | `FString` |  |  | Target asset path to write the PCG assets to. |
| ↳ `bSaveOnExportEnded` | `bool` | `true` |  | Controls whether the assets will be saved at the end of the process or not. |

### ▸ Generic

#### Add Component

`UPCGAddComponentSettings` · plugin `PCG`

[src] Adds component(s) to specified target actor(s).

**Pin data types detected:** in `Any, Point` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bUseClassAttribute` | `bool` | `false` |  | Controls whether component class selection will be done by attribute or from a constant defined in this node. |
| `ClassAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Specifies component class selection *Only when* `bUseClassAttribute` |
| `TemplateComponentClass` | `class UActorComponent` |  |  | *Only when* `!bUseClassAttribute` |
| `bAllowTemplateComponentEditing` | `bool` | `false` |  | *Only when* `!bUseClassAttribute` |
| `TemplateComponent` | `UActorComponent` |  |  | *Only when* `!bUseClassAttribute && bAllowTemplateComponentEditing` |
| `ActorReferenceAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Specifies what attribute is used to derive actor reference *Only when* `CanEditActorReference()` |
| `ComponentReferenceAttribute` | `FPCGAttributePropertyOutputNoSourceSelector` |  | ◆ | Specifies what attribute to write the component reference to. |

#### Add Tags

`UPCGAddTagSettings` · plugin `PCG`

[src] Applies the specified tags on the output data.

[epic] Adds tags on the provided data based on comma-separated lists of tags. This is used to improve data tracking in more complex graphs in conjunction with the Filter Data By Tag node.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `TagsToAdd` | `FString` |  | ◆ | Comma-separated list of tags to apply to the node. |
| `Prefix` | `FString` |  | ◆ | Common prefix to add to all tags, can be left empty. |
| `Suffix` | `FString` |  | ◆ | Common suffix to add to all tags, can be left empty. |
| `bIgnoreTagValueParsing` | `bool` | `false` | ◆ | Controls whether tags are not considered to be key-value pairs, e.g. that the prefix/suffix will be added before the ':' (if any) or not. |
| `bTokenizeOnWhiteSpace` | `bool` | `false` |  | *Only when* `bTokenizeOnWhiteSpace` |

#### Apply On Object

`UPCGApplyOnActorSettings` · plugin `PCG` · internal name `ApplyOnActor`

[src] Applies property overrides and executes functions on a target object.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ObjectReferenceAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | If something is connected in the In pin, will look for this attribute values to load, representing the object reference. |
| `PropertyOverrideDescriptions` | `TArray<FPCGObjectPropertyOverrideDescription>` |  |  | Override the default property values on the target actor. Applied before post-process functions. |
| `PostProcessFunctionNames` | `TArray<FName>` |  |  | Specify a list of functions to be called on the target actor. Functions need to be parameter-less and with "CallInEditor" flag enabled. |
| `bSilenceErrorOnEmptyObjectPath` | `bool` | `false` |  | Opt-in option to silence errors when the path is Empty or nothing to extract. |
| `bPropagateObjectChangeEvent` | `bool` | `false` |  | Overrides can propagate the change to the object if it is necessary. May trigger expensive downstream computation or infinite refresh loop if PCG listens to changes to this object. Only works in Editor. |
| `bSynchronousLoad` | `bool` | `false` |  | By default, object loading is asynchronous, can force it synchronous if needed. |

#### Compute Graph

`UPCGComputeGraphSettings` · plugin `PCG`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

*No editable settings declared.*

#### Data Attributes To Tags

`UPCGDataAttributesToTagsSettings` · plugin `PCG`

[src] Copy data attributes and their values to tags.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bDiscardNonParseableAttributeTypes` | `bool` | `true` | ◆ | If the type is not parseable (like a Quaternion for example), it can be discarded or just added as name. |
| `bDiscardAttributeValue` | `bool` | `false` | ◆ | Do not output the value of the attribute in the tag (e.g. MyAttr:1), but only the attribute name (e.g. MyAttr) |
| `AttributesTagsMapping` | `TMap<FString, FPCGAttributePropertyOutputSelector>` |  |  | Map between input attribute/tags to output attribute/tags. Can use @Source to keep the name. If empty, copies everything. *(from `UPCGDataAttributesAndTagsSettingsBase`)* |
| `bDeleteInputsAfterOperation` | `bool` | `false` | ◆ | After the operation, can delete the input attributes/tags *(from `UPCGDataAttributesAndTagsSettingsBase`)* |

#### Data Count

`UPCGDataNumSettings` · plugin `PCG` · internal name `DataNum`

[src] Returns the count of data in the input data collection.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `OutputAttributeName` | `FName` | `NAME_None` | ◆ |  |

#### Delete Tags

`UPCGDeleteTagsSettings` · plugin `PCG`

[class] Filters the tags on the input data.

[epic] Removes tags from the input data, either for all mathces against a comma-separated list or if a tag is not in the provided list. This node can be used to normalize tags on data to process downstream and is more of an organizational node. However, it could be used as a way to mark data as being processed in a workflow where the same processing could be done multiple times.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Operation` | `EPCGTagFilterOperation` | `EPCGTagFilterOperation::DeleteSelectedTags` | ◆ | *Options: KeepOnlySelectedTags · DeleteSelectedTags* |
| `Operator` | `EPCGStringMatchingOperator` | `EPCGStringMatchingOperator::Equal` | ◆ | *Options: Equal · Substring · Matches* |
| `SelectedTags` | `FString` |  | ◆ | Comma-separated list of tags to add or remove from the input data. |
| `bTokenizeOnWhiteSpace` | `bool` | `false` |  | *Only when* `bTokenizeOnWhiteSpace` |

#### Execute Python Script  β Beta

`UPCGExecutePythonScriptSettings` · plugin `PCGPythonInterop`

[src] Execute a Python script from an inline or connected input, or directly from a .py file.

**Pin data types detected:** in `Param` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ScriptInputMethod` | `EPCGPythonScriptInputMethod` | `EPCGPythonScriptInputMethod::Input` |  | The method for receiving the intended Python source. *Options: Input · File* |
| `ScriptSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | Which attribute to use as a script source. *Only when* `ScriptInputMethod == EPCGPythonScriptInputMethod::Input` |
| `ScriptPath` | `FFilePath` |  | ◆ | The path to the .py file that will be executed. *Only when* `ScriptInputMethod == EPCGPythonScriptInputMethod::File` |
| `bMuteEditorToast` | `bool` | `false` | ◆ |  |

#### Gather

`UPCGGatherSettings` · plugin `PCG`

[src] Gathers multiple data in a single collection. Can also be used to order execution through the dependency-only pin.

[epic] Takes all inputs and generates a single collection holding all the input data. Used mainly for organization. Contains a Dependency Only pin to sequence execution in cases where it is important (such as World Ray Hit Query vs. content spawned in a given graph). Note that all data provided to this pin will not be passed to the output.

**Pin data types detected:** in `default` → out `Any`

*No editable settings declared.*

#### Get Console Variable

`UPCGGetConsoleVariableSettings` · plugin `PCG`

[src] Reads the given console variable and writes the value to an attribute set. Note: Setting the console variable will not trigger a regeneration.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ConsoleVariableName` | `FName` | `NAME_None` | ◆ |  |
| `OutputAttributeName` | `FName` | `NAME_None` | ◆ |  |

#### Get Execution Context Info

`UPCGGetExecutionContextSettings` · plugin `PCG` · internal name `GetExecutionContext`

[src] Returns some context-specific common information.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `EPCGGetExecutionContextMode` | `EPCGGetExecutionContextMode::IsRuntime` |  | *Options: IsEditor* |

#### Get Loop Index

`UPCGGetLoopIndexSettings` · plugin `PCG`

[src] Returns the index of the loop this subgraph is executing, if any.

[epic] Returns an attribute set containing the current loop index if this is executed inside of a loop subgraph. This returns only the index of the direct subgraph and does not go up the graph hierarchy to find the nearest loop. This can be used to compute per-iteration data for recursive patterns or for logging purposes.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bWarnIfCalledOutsideOfLoop` | `bool` | `true` |  | Controls whether this node will create a warning when not called from within a loop. |

#### Get Subgraph Depth

`UPCGGetSubgraphDepthSettings` · plugin `PCG`

[src] Returns the call depth of this graph.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `EPCGSubgraphDepthMode` | `EPCGSubgraphDepthMode::Depth` |  | *Options: Depth · RecursiveDepth* |
| `DistanceRelativeToUpstreamGraph` | `int` | `0` | ◆ | In the case of recursive depth, it is possible to target the current graph (0), the parent graph (1) or other graphs upstream (2+). *Only when* `Mode == EPCGSubgraphDepthMode::RecursiveDepth` |
| `bQuietInvalidDepthQueries` | `bool` | `false` |  | *Only when* `Mode == EPCGSubgraphDepthMode::RecursiveDepth` |

#### Get Tool Data

`UPCGDataFromTool` · plugin `PCG`

[src] Builds a collection of PCG-compatible data from the selected tools.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ToolTag` | `FName` | `NAME_None` | ◆ | The tool tag on the pcg component to create a data collection from. Example given: "PaintTool" will allow you to retrieve points created by the PaintTool in the level viewport in PCG mode. |
| `DataInstance` | `FName` | `NAME_None` | ◆ | The optional name of the data this node should retrieve. If you want to support multiple tool outputs of the same type, differentiate using this name. Example given: "Trees" or "Bushes" will allow you to paint onto two different layers so you can process them differently in the graph. |

#### Graph Authoring Test Helper

`UPCGGraphAuthoringTestHelperSettings` · plugin `PCG`

[class] Testing helper - generates a node with a single input and output pin of the stipulated type.

*No editable settings declared.*

#### Grid Linkage

`UPCGGridLinkageSettings` · plugin `PCG`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

*No editable settings declared.*

#### Pathfinding

`UPCGPathfindingSettings` · plugin `PCG` · internal name `PathfindingElement`

[src] Finds the optimal path across the points of a given point cloud--should one exist--when provided a start and goal location, and a maximum jump distance between points. Can return a partial path.

**Pin data types detected:** in `Point, PointOrParam` → out `Point, Spline`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SearchDistance` | `double` | `1000` | ◆ | The max distance from each point to search for the next viable point in the path. |
| `bStartLocationsAsInput` | `bool` | `false` |  |  |
| `StartLocationAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `bStartLocationsAsInput` |
| `Start` | `FVector` | `FVector::ZeroVector` | ◆ | The location the pathfinding should attempt to reach. Not used when using start locations from an input. *Only when* `!bStartLocationsAsInput` |
| `bGoalLocationsAsInput` | `bool` | `false` |  |  |
| `GoalLocationAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `bGoalLocationsAsInput` |
| `Goal` | `FVector` | `FVector::ZeroVector` | ◆ | The location the pathfinding should attempt to reach. Not used when using goal locations from an input. *Only when* `!bGoalLocationsAsInput` |
| `GoalMappingMode` | `EPCGPathfindingGoalMappingMode` | `EPCGPathfindingGoalMappingMode::EachStartToNearestGoal` | ◆ | How each goal location correlates to each start location. Only relevant when using multiple start and goal locations as input. *Options: EachStartToNearestGoal · EachStartToEachGoal · EachStartToPairwiseGoal* |
| `HeuristicWeight` | `double` | `1.0` | ◆ | The heuristic estimates a faster path to speed up processing. A higher than 1 heuristic weight can be faster, but it may cease being the optimal path. A weight of 0 is essentially flood fill. |
| `CostFunctionMode` | `EPCGPathfindingCostFunctionMode` | `EPCGPathfindingCostFunctionMode::Distance` | ◆ | Controls whether the cost function will use a given attribute as a scalar wrt to the distance. *Options: Distance · FitnessScore · CostMultiplier* |
| `CostAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Attribute to use as part of the cost function - it's meaning will depend on the cost function mode (fitness value, scalar multiplier, or else). *Only when* `CostFunctionMode != EPCGPathfindingCostFunctionMode::Distance` |
| `MaximumFitnessPenaltyFactor` | `double` | `10.0` | ◆ | Fitness penalty scalar (maximum penalty applied when fitness is zero.) *Only when* `CostFunctionMode == EPCGPathfindingCostFunctionMode::FitnessScore` |
| `bUsePathTraces` | `bool` | `false` | ◆ | Controls whether raycasts will be used to test for collisions along the path (hit results will be considered obstacles for the pathfinding). |
| `PathTraceParams` | `FPCGWorldRaycastQueryParams` |  | ◆ | *Only when* `bUsePathTraces` |
| `bAcceptPartialPath` | `bool` | `true` | ◆ | Even if the path is not complete, return a viable partial path to the point closest to the goal. Output data will be tagged with "CompletePath" or "PartialPath", depending on the result, if enabled. |
| `bOutputAsSpline` | `bool` | `true` |  | The final path will be a spline. If false, the final path will be an ordered point data. |
| `SplineMode` | `EPCGPathfindingSplineMode` | `EPCGPathfindingSplineMode::Curve` | ◆ | Determines how the output spline's curves will be calculated. *Options: Curve · Linear* *Only when* `bOutputAsSpline` |
| `bCopyOriginatingPoints` | `bool` | `false` | ◆ | Copy the properties and attributes from the originating point input to the output points. *Only when* `!bOutputAsSpline` |

#### Proxy

`UPCGIndirectionSettings` · plugin `PCG`

[src] Executes another settings object, which can be overridden.

[epic] Placeholder node replacement that allows dynamic override during execution of the graph. A Prototype (default value) can be set to show the proper node pines, but the node being run can be driven through parameter overrides. This is especially usefull to allow some per-instance controls from pre-built nodes, such as exposing specific noise types.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ProxyInterfaceMode` | `EPCGProxyInterfaceMode` | `EPCGProxyInterfaceMode::BySettings` |  | Defines which interface to use for populating pins *Options: ByNativeElement · ByBlueprintElement · BySettings* |
| `SettingsClass` | `class UPCGSettings` |  |  | The element settings class used to define the pin interface for this node instance *Only when* `ProxyInterfaceMode == EPCGProxyInterfaceMode::ByNativeElement` |
| `BlueprintElementClass` | `class UPCGBlueprintBaseElement` |  |  | The blueprint element class used to define the pin interface for this node instance *Only when* `ProxyInterfaceMode == EPCGProxyInterfaceMode::ByBlueprintElement` |
| `Settings` | `UPCGSettings` |  | ◆ | The element settings, which can be overriden, that will be used during the proxy execution |
| `bTagOutputsBasedOnOutputPins` | `bool` | `true` | ◆ |  |

#### Replace Tags

`UPCGReplaceTagsSettings` · plugin `PCG`

[class] Replaces the tags on the input data.

[epic] Replaces tags on the input data by their matching counterpart. This node supports replacing tags in either 1:1, N:1, or N:N relationships using comma-separated lists.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SelectedTags` | `FString` |  | ◆ | Comma-separated list of tags to be replaced from the input data. If no tags are replaced, then these tags will be removed. |
| `ReplacedTags` | `FString` |  | ◆ | Comma-separated list of new tags to replace the selected tags. |
| `bTokenizeOnWhiteSpace` | `bool` | `false` |  | *Only when* `bTokenizeOnWhiteSpace` |

#### Select Grammar

`UPCGSelectGrammarSettings` · plugin `PCG`

[src] Select a grammar by comparing an input attribute against a provided criteria.

**Pin data types detected:** in `Param, Point` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `bKeyAsAttribute` | `bool` | `true` | ◆ | Select the key with an attribute. |
| `Key` | `FName` |  | ◆ | An attribute key that represents the desired set of grammars. *Only when* `!bKeyAsAttribute` |
| `KeyAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | An attribute selector for a key that represents the desired set of grammars. *Only when* `bKeyAsAttribute` |
| `ComparedValueAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | The attribute on the input data to be compared against. Will be numerically evaluated. |
| `bCriteriaAsInput` | `bool` | `false` |  | Toggle for an additional input "Selection Criteria Data" which accepts criteria info as an attribute set matching the structure type 'FPCGSelectGrammarCriteria'. |
| `Criteria` | `TArray<FPCGSelectGrammarCriterion>` |  | ◆ | Selection criteria that will be evaluated in order. *Only when* `!bCriteriaAsInput` |
| `bCopyKeyForUnselectedGrammar` | `bool` | `false` | ◆ | If no grammar is selected for a given point, pass through the key value. |
| `bRemapCriteriaAttributeNames` | `bool` | `false` | ◆ | Remap expected attribute names for the comparison criteria. *Only when* `bCriteriaAsInput` |
| `Remap Criteria Attribute Names` | `FPCGSelectGrammarCriteriaAttributeNames` |  | ◆ | The attribute names expected for the comparison criteria. *Only when* `bRemapCriteriaAttributeNames` |
| ↳ `KeyAttributeName` | `FName` | `TEXT("Key")` |  |  |
| ↳ `ComparatorAttributeName` | `FName` | `TEXT("Comparator")` |  |  |
| ↳ `FirstValueAttributeName` | `FName` | `TEXT("FirstValue")` |  |  |
| ↳ `SecondValueAttributeName` | `FName` | `TEXT("SecondValue")` |  |  |
| ↳ `GrammarAttributeName` | `FName` | `TEXT("Grammar")` |  |  |
| `OutputGrammarAttribute` | `FPCGAttributePropertyOutputSelector` |  | ◆ | The attribute to output the selected grammar. |

#### Sort Attributes

`UPCGSortAttributesSettings` · plugin `PCG`

[src] Sorts data based on an attribute.

[epic] Sorts the input data (Point Data and Attribute Set) by a specified attribute in ascending or descending order. This node can be used to order data in such a way to make it predictable for downstream nodes. For example, you could order some values by priority then act on this downstream.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InputSource` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `SortMethod` | `EPCGSortMethod` | `EPCGSortMethod::Ascending` | ◆ | *Options: Ascending · Descending* |

#### Sort Data By Tag Value

`UPCGSortTagsSettings` · plugin `PCG` · internal name `SortTags`

[src] Sorts data by tag value (i.e. with tags of the form Tag:Value)

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Tag` | `FName` |  | ◆ |  |
| `SortMethod` | `EPCGSortMethod` | `EPCGSortMethod::Ascending` | ◆ | *Options: Ascending · Descending* |

#### Tags to Data Attributes

`UPCGTagsToDataAttributesSettings` · plugin `PCG`

[src] Parse tags and create data attributes from it.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `AttributesTagsMapping` | `TMap<FString, FPCGAttributePropertyOutputSelector>` |  |  | Map between input attribute/tags to output attribute/tags. Can use @Source to keep the name. If empty, copies everything. *(from `UPCGDataAttributesAndTagsSettingsBase`)* |
| `bDeleteInputsAfterOperation` | `bool` | `false` | ◆ | After the operation, can delete the input attributes/tags *(from `UPCGDataAttributesAndTagsSettingsBase`)* |

#### Trivial

`UPCGTrivialSettings` · plugin `PCG`

[class] Trivial / Pass-through settings used for input/output nodes

*No editable settings declared.*

#### Wait

`UPCGWaitSettings` · plugin `PCG`

[src] Waits some time and/or frames. Not a node that should be used in production except in very special cases.

**Pin data types detected:** in `default` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `WaitTimeInSeconds` | `double` | `1.0` | ◆ |  |
| `WaitTimeInEngineFrames` | `int64` | `0` | ◆ |  |
| `WaitTimeInRenderFrames` | `int64` | `0` | ◆ |  |
| `bEndWaitWhenAllConditionsAreMet` | `bool` | `true` | ◆ | Controls whether all conditions are needed or any condition is sufficient to end the wait. |

#### Wait Until Landscape Is Ready

`UPCGWaitLandscapeReadySettings` · plugin `PCG` · internal name `WaitUntilLandscapeReady`

[src] Waits until landscape is ready, then passes data downstream.

**Pin data types detected:** in `Any` → out `Any`

*No editable settings declared.*

#### Write To Niagara Data Channel  🧪 Experimental

`UPCGWriteToNiagaraDataChannelSettings` · plugin `PCGNiagaraInterop`

[class] Allow writing attributes to a Niagara Data Channel.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `DataChannel` | `soft UNiagaraDataChannelAsset` |  | ◆ |  |
| `NiagaraVariablesPCGAttributeMapping` | `TMap<FName, FPCGAttributePropertyInputSelector>` |  |  |  |
| `bVisibleToGame` | `bool` | `true` | ◆ | Data written to this data channel is visible to Blueprint and C++ logic reading from it |
| `bVisibleToCPU` | `bool` | `true` | ◆ | Data written to this data channel is visible to Niagara CPU emitters |
| `bVisibleToGPU` | `bool` | `false` | ◆ | Data written to this data channel is visible to Niagara GPU emitters |
| `bSynchronousLoad` | `bool` | `false` |  |  |

### ▸ Dynamic Mesh

#### Append Meshes From Points  β Beta

`UPCGAppendMeshesFromPointsSettings` · plugin `PCGGeometryScriptInterop`

[src] Append meshes at the points transforms. Mesh can be a single static mesh, multiple meshes coming from the points or another dynamic mesh.

**Pin data types detected:** in `DynamicMesh, Point` → out `DynamicMesh`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Mode` | `EPCGAppendMeshesFromPointsMode` |  |  | *Options: SingleStaticMesh · StaticMeshFromAttribute · DynamicMesh* |
| `StaticMesh` | `soft UStaticMesh` |  | ◆ | *Only when* `Mode==EPCGAppendMeshesFromPointsMode::SingleStaticMesh` |
| `MeshAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | *Only when* `Mode==EPCGAppendMeshesFromPointsMode::StaticMeshFromAttribute` |
| `bExtractMaterials` | `bool` | `true` | ◆ | Allows to extract materials from the static mesh and set them in the resulting append. *Only when* `Mode!=EPCGAppendMeshesFromPointsMode::DynamicMesh` |
| `RequestedLODType` | `EGeometryScriptLODType` | `EGeometryScriptLODType::RenderData` | ◆ | LOD type to use when creating DynamicMesh from specified StaticMesh. *Only when* `Mode!=EPCGAppendMeshesFromPointsMode::DynamicMesh` |
| `RequestedLODIndex` | `int32` | `0` | ◆ | *Only when* `Mode!=EPCGAppendMeshesFromPointsMode::DynamicMesh` |
| `bSynchronousLoad` | `bool` | `false` |  | *Only when* `Mode!=EPCGAppendMeshesFromPointsMode::DynamicMesh` |

#### Boolean Operation  β Beta

`UPCGBooleanOperationSettings` · plugin `PCGGeometryScriptInterop`

[src] Boolean operation between dynamic meshes.

**Pin data types detected:** in `DynamicMesh` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `BooleanOperation` | `EGeometryScriptBooleanOperation` | `EGeometryScriptBooleanOperation::Intersection` | ◆ |  |
| `BooleanOperationOptions` | `FGeometryScriptMeshBooleanOptions` |  | ◆ |  |
| ↳ `bFillHoles` | `bool` | `true` |  |  |
| ↳ `bSimplifyOutput` | `bool` | `true` |  |  |
| ↳ `SimplifyPlanarTolerance` | `float` | `0.01f` |  |  |
| ↳ `bAllowEmptyResult` | `bool` | `false` |  | Whether to allow the Mesh Boolean operation to generate an empty mesh as its result |
| ↳ `OutputTransformSpace` | `EGeometryScriptBooleanOutputSpace` | `EGeometryScriptBooleanOutputSpace::TargetTransformSpace` |  | The coordinate space to use for the result mesh |
| `TagInheritanceMode` | `EPCGBooleanOperationTagInheritanceMode` |  | ◆ | *Options: Both · A · B* |
| `Mode` | `EPCGBooleanOperationMode` | `EPCGBooleanOperationMode::EachAWithEachB` | ◆ | *Options: EachAWithEachB · EachAWithEachBSequentially · EachAWithEveryB* |

#### Create Empty Dynamic Mesh  β Beta

`UPCGCreateEmptyDynamicMeshSettings` · plugin `PCGGeometryScriptInterop`

[src] Create an empty dynamic mesh data.

**Pin data types detected:** in `default` → out `DynamicMesh`

*No editable settings declared.*

#### Dynamic Mesh Transform  β Beta

`UPCGDynamicMeshTransformSettings` · plugin `PCGGeometryScriptInterop`

[src] Apply a transform to all dynamic meshes.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Transform` | `FTransform` |  | ◆ |  |

#### Merge Dynamic Meshes  β Beta

`UPCGMergeDynamicMeshesSettings` · plugin `PCGGeometryScriptInterop`

[src] Appends all incoming dynamic meshes to the first dynamic mesh in order.

**Pin data types detected:** in `default` → out `DynamicMesh`

*No editable settings declared.*

#### Save Dynamic Mesh To Asset  β Beta

`UPCGSaveDynamicMeshToAssetSettings` · plugin `PCGGeometryScriptInterop`

[src] Saves dynamic mesh data into a static mesh asset.

**Pin data types detected:** in `DynamicMesh` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ExportParams` | `FPCGAssetExporterParameters` |  | ◆ |  |
| ↳ `bOpenSaveDialog` | `bool` | `true` |  | Controls whether we will open a Save... dialog, works only when a single level is exported. Overrides update anywhere. |
| ↳ `AssetName` | `FString` |  |  | Target asset path name |
| ↳ `AssetPath` | `FString` |  |  | Target asset path to write the PCG assets to. |
| ↳ `bSaveOnExportEnded` | `bool` | `true` |  | Controls whether the assets will be saved at the end of the process or not. |
| `bExportMaterialsFromDynamicMesh` | `bool` | `true` | ◆ | This option has higher priority than CopyMeshToAssetOptions.ReplaceMaterials. If true, we will replace the materials from the materials stored on the PCG Dynamic Mesh data. Otherwise, we will follow what is set in CopyMeshToAssetOptions. |
| `CopyMeshToAssetOptions` | `FGeometryScriptCopyMeshToAssetOptions` |  | ◆ |  |
| ↳ `bEnableRecomputeNormals` | `bool` | `false` |  |  |
| ↳ `bEnableRecomputeTangents` | `bool` | `false` |  |  |
| ↳ `bEnableRemoveDegenerates` | `bool` | `false` |  |  |
| ↳ `BoneHierarchyMismatchHandling` | `EGeometryScriptBoneHierarchyMismatchHandling` | `EGeometryScriptBoneHierarchyMismatchHandling::DoNothing` |  | An option that specifies, for skeletal mesh assets, how mismatches between the existing reference skeleton on the asset, and the bone hierarchy stored on the geometry are handled. By default, no attempt is made to resolve this mismatch. |
| ↳ `bRemapBoneIndicesToMatchAsset` | `bool` | `false` |  | UE_DEPRECATED(5.6, "Deprecated. Use BoneHierarchyMismatchHandling instead.") |
| ↳ `bUseOriginalVertexOrder` | `bool` | `false` |  | Use the original vertex order found in the source data. This is useful if the inbound mesh was originally non-manifold, and needs to keep the non-manifold structure when re-created. |
| ↳ `bUseBuildScale` | `bool` | `true` |  | Whether to use the build scale on the target asset. If enabled, the inverse scale will be applied when saving to the asset, and the BuildScale will be preserved. Otherwise, BuildScale will be set to 1.0 on the asset BuildSettings. |
| ↳ `bReplaceMaterials` | `bool` | `false` |  | Whether to replace the materials on the asset with those in the New Materials array |
| ↳ `GenerateLightmapUVs` | `EGeometryScriptGenerateLightmapUVOptions` | `EGeometryScriptGenerateLightmapUVOptions::MatchTargetLODSett …` |  | Whether to generate lightmap UVs |
| ↳ `NewMaterials` | `TArray<UMaterialInterface` |  |  | New materials to set if Replace Materials is enabled. Ignored otherwise. |
| ↳ `NewMaterialSlotNames` | `TArray<FName>` |  |  | Optional slot names for the New Materials. Ignored if not the same length as the New Materials array. |
| ↳ `bApplyNaniteSettings` | `bool` | `false` |  | If enabled, NaniteSettings will be applied to the target Asset if possible |
| ↳ `DEPRECATED NANITE SETTING` | `FGeometryScriptNaniteOptions` | `FGeometryScriptNaniteOptions()` |  | Replaced FGeometryScriptNaniteOptions with usage of Engine FMeshNaniteSettings |
| ↳ `Nanite Settings` | `FMeshNaniteSettings` |  |  | Nanite Settings applied to the target Asset, if bApplyNaniteSettings = true |
| ↳ `bEmitTransaction` | `bool` | `true` |  |  |
| ↳ `bDeferMeshPostEditChange` | `bool` | `false` |  |  |
| `MeshWriteLOD` | `FGeometryScriptMeshWriteLOD` |  | ◆ |  |
| ↳ `bWriteHiResSource` | `bool` | `false` |  |  |
| ↳ `LODIndex` | `int32` | `0` |  |  |

#### Spawn Dynamic Mesh  β Beta

`UPCGSpawnDynamicMeshSettings` · plugin `PCGGeometryScriptInterop`

[src] Spawn a dynamic mesh component for each dynamic mesh data in input.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PostProcessFunctionNames` | `TArray<FName>` |  |  | Specify a list of functions to be called on the target actor after instances are spawned. Functions need to be parameter-less and with "CallInEditor" flag enabled. |

#### Spline To Mesh  β Beta

`UPCGSplineToMeshSettings` · plugin `PCGGeometryScriptInterop`

[src] Converts a closed spline into a mesh.

**Pin data types detected:** in `Spline` → out `default`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ErrorTolerance` | `double` | `1.0` |  | How far to allow the triangulation boundary can deviate from the spline curve before we add more vertices |
| `FlattenMethod` | `EFlattenCurveMethod` | `EFlattenCurveMethod::DoNotFlatten` |  | Whether and how to flatten the curves. If curves are flattened, they can also be offset. |
| `Thickness` | `double` | `0.0` |  | If > 0, Extrude the triangulation by this amount. |
| `bFlipResult` | `bool` | `false` |  | Whether to flip the facing direction of the generated mesh. |
| `OpenCurves` | `EOffsetOpenCurvesMethod` | `EOffsetOpenCurvesMethod::TreatAsClosed` |  | How to handle open curves: Either offset them, or treat them as closed curves. *Only when* `FlattenMethod != EFlattenCurveMethod::DoNotFlatten` |
| `CurveOffset` | `double` | `0.0` |  | How much offset to apply to curves. *Only when* `FlattenMethod != EFlattenCurveMethod::DoNotFlatten` |
| `OffsetClosedCurves` | `EOffsetClosedCurvesMethod` | `EOffsetClosedCurvesMethod::OffsetOuterSide` |  | Whether and how to apply offset to closed curves. *Only when* `FlattenMethod != EFlattenCurveMethod::DoNotFlatten && CurveOffset != 0` |
| `EndShapes` | `EOpenCurveEndShapes` | `EOpenCurveEndShapes::Square` |  | The shape of the ends of offset curves. *Only when* `FlattenMethod != EFlattenCurveMethod::DoNotFlatten && OpenCurves != EOffsetOpenCurvesMethod::TreatAsClosed && CurveOffset != 0` |
| `JoinMethod` | `EOffsetJoinMethod` | `EOffsetJoinMethod::Square` |  | The shape of joins between segments of an offset curve. *Only when* `FlattenMethod != EFlattenCurveMethod::DoNotFlatten && CurveOffset != 0` |
| `MiterLimit` | `double` | `1.0` |  | How far a miter join can extend before it is replaced by a square join. *Only when* `FlattenMethod != EFlattenCurveMethod::DoNotFlatten && CurveOffset != 0 && JoinMethod == EOffsetJoinMethod::Miter` |

#### Static Mesh To Dynamic Mesh Element  β Beta

`UPCGStaticMeshToDynamicMeshSettings` · plugin `PCGGeometryScriptInterop`

[src] Convert a static mesh into a dynamic mesh data.

**Pin data types detected:** in `default` → out `DynamicMesh`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `StaticMesh` | `soft UStaticMesh` |  | ◆ |  |
| `bExtractMaterials` | `bool` | `true` | ◆ | Allows to extract materials from the static mesh and store them in the PCG Dynamic Mesh Data. |
| `OverrideMaterials` | `TArray<soft UMaterialInterface` |  |  | If it extracts materials, we can specify override materials. It needs to have the same number of material overrides than there are materials on the static mesh. *Only when* `bExtractMaterials` |
| `RequestedLODType` | `EGeometryScriptLODType` | `EGeometryScriptLODType::MaxAvailable` | ◆ | LOD type to use when creating DynamicMesh from specified StaticMesh. |
| `RequestedLODIndex` | `int32` | `0` | ◆ |  |
| `bSynchronousLoad` | `bool` | `false` |  |  |

### ▸ GPU

#### Custom HLSL

`UPCGCustomHLSLSettings` · plugin `PCG`

**One palette entry per `EPCGKernelType` value** — see section 4.

[src] Produces a HLSL compute shader which will be executed on the GPU.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `KernelType` | `EPCGKernelType` | `EPCGKernelType::PointProcessor` |  | *Options: PointProcessor · PointGenerator · TextureProcessor · TextureGenerator · Custom · AttributeSetProcessor* |
| `NumElements` | `int` | `256` | ◆ | *Only when* `KernelType == EPCGKernelType::PointGenerator` |
| `Num Elements` | `FIntPoint` | `FIntPoint(64, 64)` |  | *Only when* `KernelType == EPCGKernelType::TextureGenerator` |
| `DispatchThreadCount` | `EPCGDispatchThreadCount` | `EPCGDispatchThreadCount::FromFirstOutputPin` |  | *Options: FromFirstOutputPin · Fixed · FromProductOfInputPins* *Only when* `KernelType == EPCGKernelType::Custom` |
| `ThreadCountMultiplier` | `int` | `1` | ◆ | *Only when* `KernelType == EPCGKernelType::Custom && DispatchThreadCount != EPCGDispatchThreadCount::Fixed` |
| `FixedThreadCount` | `int` | `1` | ◆ | *Only when* `KernelType == EPCGKernelType::Custom && DispatchThreadCount == EPCGDispatchThreadCount::Fixed` |
| `Input Pins` | `TArray<FName>` |  |  | *Only when* `KernelType == EPCGKernelType::Custom && DispatchThreadCount == EPCGDispatchThreadCount::FromProductOfInputPins` |
| `InputPins` | `TArray<FPCGPinProperties>` | `Super::DefaultPointInputPinProperties()` |  |  |
| `OutputPins` | `TArray<FPCGPinPropertiesGPU>` | `{ FPCGPinPropertiesGPU(PCGPinConstants::DefaultOutputLabel, …` |  |  |
| `KernelSourceOverride` | `UComputeSource` |  |  | Override your kernel with a PCG compute source asset. |
| `AdditionalSources` | `TArray<UComputeSource` |  |  | Additional source files to use in your kernel. |
| `bMuteUnwrittenPinDataErrors` | `bool` | `false` |  | Mute uninitialized data errors. |

#### Generate Landscape Textures  ⚠ deprecated

`UDEPRECATED_PCGGenerateGrassMapsSettings` · plugin `PCG`

[src] Generates landscape height texture and grass maps on the GPU.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SelectedGrassTypes` | `TArray<FString>` |  |  | Select which grass types to generate. *Only when* `!bOverrideFromInput` *(from `UPCGGenerateLandscapeTexturesSettings`)* |
| `bOverrideFromInput` | `bool` | `false` |  | Override grass types from input. *(from `UPCGGenerateLandscapeTexturesSettings`)* |
| `GrassTypesAttribute` | `FPCGAttributePropertyInputSelector` |  |  | Input attribute to pull grass type strings from. *Only when* `bOverrideFromInput` *(from `UPCGGenerateLandscapeTexturesSettings`)* |
| `bExcludeSelectedGrassTypes` | `bool` | `true` | ◆ | If toggled, will only generate grass types which are not selected. *(from `UPCGGenerateLandscapeTexturesSettings`)* |
| `bSkipReadbackToCPU` | `bool` | `false` |  | Skip CPU readback of emitted textures during initialization of the texture datas. *(from `UPCGGenerateLandscapeTexturesSettings`)* |
| `bGenerateHeightMap` | `bool` | `false` |  | Generate a landscape height texture. *(from `UPCGGenerateLandscapeTexturesSettings`)* |

#### Generate Landscape Textures

`UPCGGenerateLandscapeTexturesSettings` · plugin `PCG`

**Also in the palette as:** *Generate Grass Maps*

[src] Generates landscape height texture and grass maps on the GPU.

**Pin data types detected:** in `Landscape, Param` → out `Texture`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `SelectedGrassTypes` | `TArray<FString>` |  |  | Select which grass types to generate. *Only when* `!bOverrideFromInput` |
| `bOverrideFromInput` | `bool` | `false` |  | Override grass types from input. |
| `GrassTypesAttribute` | `FPCGAttributePropertyInputSelector` |  |  | Input attribute to pull grass type strings from. *Only when* `bOverrideFromInput` |
| `bExcludeSelectedGrassTypes` | `bool` | `true` | ◆ | If toggled, will only generate grass types which are not selected. |
| `bSkipReadbackToCPU` | `bool` | `false` |  | Skip CPU readback of emitted textures during initialization of the texture datas. |
| `bGenerateHeightMap` | `bool` | `false` |  | Generate a landscape height texture. |

### ▸ Debug

#### Debug

`UPCGDebugSettings` · plugin `PCG`

[epic] Debugs the previous node in the graph but is not transient. This works the same as enabling debug on the nodes that provide their data to this node. This is useful to have a permanent debug point in a grpah since it is not transient even though the debug parameters are. It does not execute in non-editor builds.

**Pin data types detected:** in `Any` → out `default`

*No editable settings declared.*

#### Print Grammar

`UPCGPrintGrammarSettings` · plugin `PCG`

[src] Prints the result of an interpreted grammar.

**Pin data types detected:** in `default` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `Grammar` | `FString` |  | ◆ | The grammar to interpret. |

#### Print String

`UPCGPrintElementSettings` · plugin `PCG`

[src] Issues a specified message to the log, and optionally to the graph and/or screen.

[epic] Prints a message that outputs a prefixed message optionally to the log, node, and screen. This acts as a passthrough node in the shipping build, meaning that it will not output the prefixed message at this point. This node is useful for debugging and validating assumptions in a graph, such as on dead branches following control flow nodes.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `PrintString` | `FString` |  | ◆ | The core message to print to the logger, graph, and/or screen. |
| `Verbosity` | `EPCGPrintVerbosity` | `EPCGPrintVerbosity::Log` | ◆ | The verbosity level of the printed message. *Options: NoLogging · Log · Warning · Error · Display* |
| `CustomPrefix` | `FString` |  | ◆ | A prefix to which the core message will be appended. |
| `bDisplayOnNode` | `bool` | `false` | ◆ | Display warnings or errors on this node. |
| `bPrintPerComponent` | `bool` | `true` | ◆ | Use the component as part of the key hash and print a message for each component with this node. |
| `bPrintToScreen` | `bool` | `false` | ◆ | Print the message to the editor viewport. |
| `PrintToScreenDuration` | `double` | `15.0` | ◆ | The duration (in seconds) of the on screen message. *Only when* `bPrintToScreen` |
| `PrintToScreenColor` | `FColor` | `FColor::Cyan` | ◆ | The color of the on screen message. *Only when* `bPrintToScreen` |
| `bPrefixWithOwner` | `bool` | `false` |  | Prefix the message with the name of the component's owner. *Only when* `bPrintPerComponent` |
| `bPrefixWithComponent` | `bool` | `false` |  | Prefix the message with the name of the component. *Only when* `bPrintPerComponent` |
| `bPrefixWithGraph` | `bool` | `true` |  | Prefix the message with the name of the graph. *Only when* `bPrintPerComponent` |
| `bPrefixWithNode` | `bool` | `true` |  | Prefix the message with the name of the node. |
| `bEnablePrint` | `bool` | `true` | ◆ | Enable the functionality of this node. Disable to bypass printing. |

#### Sanity Check Point Data

`UPCGSanityCheckPointDataSettings` · plugin `PCG`

[epic] Validates that the input data point(s) have a value in the given range; outside of the range this node logs an error and cancels the generation. This is useful when trying to validate assumptions in a graph but shouldn't be considered a good building block in graphs.

**Pin data types detected:** in `Point` → out `Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `MinPointCount` | `int32` | `0` | ◆ |  |
| `MaxPointCount` | `int32` | `100` | ◆ |  |

#### Visualize Attribute

`UPCGVisualizeAttributeSettings` · plugin `PCG`

[src] Visualizes a selected attribute on screen at each point's transform.

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `AttributeSource` | `FPCGAttributePropertyInputSelector` |  | ◆ | This attribute will be have it's value printed in proximity to each input point's transform. |
| `CustomPrefixString` | `FString` |  | ◆ | A custom added prefix to which the attribute value will be appended. |
| `bPrefixWithIndex` | `bool` | `true` | ◆ | Prefix the printed value with the point's index. |
| `bPrefixWithAttributeName` | `bool` | `false` | ◆ | Prefix the printed value with the attribute's name. |
| `LocalOffset` | `FVector` | `FVector(0, 0, 0)` | ◆ | A local offset from the point's location to draw the text. |
| `Color` | `FColor` | `FColor::Cyan` | ◆ | The color of the on displayed value. |
| `Duration` | `double` | `30.0` | ◆ | The duration (in seconds) of the displayed value. |
| `PointLimit` | `int32` | `4096` | ◆ | The limit of points to draw debug messages. |
| `bVisualizeEnabled` | `bool` | `true` | ◆ | The visualizer is enabled. Useful for dynamically overriding. |

### ▸ Reroute

#### Named Reroute Base

`UPCGNamedRerouteBaseSettings` · plugin `PCG`

[class] Base class for both reroute declaration and usage to share implementation, but also because they use the same visual node representation in the editor.

*No editable settings declared.*

#### Named Reroute Declaration

`UPCGNamedRerouteDeclarationSettings` · plugin `PCG`

[epic] Named reroute nodes are akin to reroute nodes but they do not have visual edges. They are used to remove otherwise very long edges or spaghetti edges across large graphs. They can be renamed and be consumed (usage) at multiple places but they can be defined only at a single place in a graph (definition). reate Surface From Polygon 2D landscape building virtual worlds procedural generation

**Pin data types detected:** in `default` → out `Any`

*No editable settings declared.*

#### Named Reroute Usage

`UPCGNamedRerouteUsageSettings` · plugin `PCG`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

*No editable settings declared.*

#### Reroute

`UPCGRerouteSettings` · plugin `PCG`

[epic] Graph organizational tool to add control points on edges, making them look nicer in the graph.

**Pin data types detected:** in `Any` → out `Any`

*No editable settings declared.*

### ▸ Resource

#### Get Resource Path

`UPCGGetResourcePath` · plugin `PCG`

[class] Converts a resource data to an attribute set containing the resource path.

**Pin data types detected:** in `Resource` → out `Param`

*No editable settings declared.*

#### Get Static Mesh Resource Data

`UPCGGetStaticMeshResourceDataSettings` · plugin `PCG`

[class] Creates static mesh resource data from the given soft object paths.

**Pin data types detected:** in `Param` → out `StaticMeshResource`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `StaticMeshes` | `TArray<soft UStaticMesh` |  |  | Produces one resource data per entry. *Only when* `!bOverrideFromInput` |
| `bOverrideFromInput` | `bool` | `false` |  | Override static meshes from input. |
| `MeshAttribute` | `FPCGAttributePropertyInputSelector` |  |  | Input attribute to pull meshes from. *Only when* `bOverrideFromInput` |

### ▸ Data Layers

#### Get Actor Data Layers

`UPCGGetActorDataLayersSettings` · plugin `PCG` · internal name `PCGGetActorDataLayers`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

**Pin data types detected:** in `PointOrParam` → out `Param`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorReferenceAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ | Actor reference Attribute to use from input to resolve actors |
| `DataLayerReferenceAttribute` | `FPCGAttributePropertyOutputSelector` |  | ◆ | Data Layer reference Attribute to use as output |

#### Partition by Actor Data Layers

`UPCGPartitionByActorDataLayersSettings` · plugin `PCG`

*No official description in the engine source or Epic's reference. Settings below are the only documentation.*

**Pin data types detected:** in `Param, Point, PointOrParam` → out `Param, Point`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `ActorReferenceAttribute` | `FPCGAttributePropertyInputSelector` |  | ◆ |  |
| `DataLayerReferenceAttribute` | `FPCGAttributePropertyOutputSelector` |  | ◆ | Data Layer reference Attribute to use as output for Data Layer Partitions |
| `IncludedDataLayers` | `FPCGDataLayerReferenceSelector` |  |  | When left empty, all Data Layers are included, if any Data Layers are specified, only those will be included |
| ↳ `bAsInput` | `bool` | `false` |  | Set it to true to get Data Layers through input attribute set. |
| ↳ `Attribute` | `FPCGAttributePropertyInputSelector` |  |  | *Only when* `bAsInput` |
| ↳ `DataLayers` | `TArray<soft UDataLayerAsset` |  |  | *Only when* `!bAsInput` |
| `ExcludedDataLayers` | `FPCGDataLayerReferenceSelector` |  |  | Specified Data Layers will get excluded |
| ↳ `bAsInput` | `bool` | `false` |  | Set it to true to get Data Layers through input attribute set. |
| ↳ `Attribute` | `FPCGAttributePropertyInputSelector` |  |  | *Only when* `bAsInput` |
| ↳ `DataLayers` | `TArray<soft UDataLayerAsset` |  |  | *Only when* `!bAsInput` |

### ▸ Blueprint

#### Execute Blueprint

`UPCGBlueprintSettings` · plugin `PCG`

[epic] Executes a specified custom Blueprint Class with the Execute or Execute With Context method on a clean instance of a Blueprint Class deriving from UPCGBlueprintElement.

**Pin data types detected:** in `Any` → out `Any`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `BlueprintElementType` | `class UPCGBlueprintBaseElement` |  |  |  |
| `TrackedActorTags` | `TArray<FName>` |  |  |  |
| `bTrackActorsOnlyWithinBounds` | `bool` | `false` |  | If this is checked, found actors that are outside component bounds will not trigger a refresh. Only works for tags for now in editor. |

### ▸ Density

#### Density Remap  ⚠ deprecated

`UPCGDensityRemapSettings` · plugin `PCG`

> ⚠ Deprecated in 5.5: *Superseded by UPCGAttributeRemapSettings* [src]

[epic] Applies a linear transform to the point densities. Optionally, this can be set to not affect values outside the input range. D' = (Out_Max - Out_Min) * (D - In_min) / (In_max - In_min) + Out_Min

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `InRangeMin` | `float` | `0.f` | ◆ | If InRangeMin = InRangeMax, then that density value is mapped to the average of OutRangeMin and OutRangeMax |
| `InRangeMax` | `float` | `1.f` | ◆ | If InRangeMin = InRangeMax, then that density value is mapped to the average of OutRangeMin and OutRangeMax |
| `OutRangeMin` | `float` | `0.f` | ◆ |  |
| `OutRangeMax` | `float` | `1.f` | ◆ |  |
| `bExcludeValuesOutsideInputRange` | `bool` | `false` | ◆ | Density values outside of the input range will be unaffected by the remapping |

### ▸ Hierarchical Generation

#### Hi Gen Grid Size

`UPCGHiGenGridSizeSettings` · plugin `PCG`

[src] Set the execution grid size for downstream nodes. Enables executing a single graph across a hierarchy of grids. Has no effect if any of the following are true: \t* Generating PCG component is not set to Partitioned. \t* Hierarchical Generation is disabled in the graph settings. \t* Executed in a subgraph, as subgraphs are always invoked on parent grid level.

**Pin data types detected:** in `Any` → out `Any, Spatial`

| setting | type | default | ◆ | what it does |
|---|---|---|---|---|
| `HiGen Grid Size` | `EPCGHiGenGrid` | `EPCGHiGenGrid::Grid256` |  | *Options: increment · Grid8 · Grid16 · Grid32 · Grid64 · Grid128 · Grid256 · Grid512 · Grid1024 · Grid2048 · Unbounded* |

---

## 4. Palette aliases — one class, many search names

PCG lets one settings class publish several palette entries with different defaults (`GetPreconfiguredInfo()` [src]). Typing any of these names in the graph editor gives you the class on the left with that option preselected. **23 classes do this.**

### Named aliases

| palette name | is really | class |
|---|---|---|
| *Point Filter* | Filter Attribute Elements | `UPCGAttributeFilteringSettings` |
| *Attribute Filter* | Filter Attribute Elements | `UPCGAttributeFilteringSettings` |
| *Point Filter Range* | Filter Attribute Elements by Range | `UPCGAttributeFilteringRangeSettings` |
| *Attribute Filter Range* | Filter Attribute Elements by Range | `UPCGAttributeFilteringRangeSettings` |
| *Density Noise* | Attribute Noise | `UPCGAttributeNoiseSettings` |
| *Density Remap* | Attribute Remap | `UPCGAttributeRemapSettings` |
| *Attribute Curve Remap* | Attribute Remap | `UPCGAttributeRemapSettings` |
| *Generate Grass Maps* | Generate Landscape Textures | `UPCGGenerateLandscapeTexturesSettings` |

### Per-type aliases

- **Create Constant** — *New <Type> Constant* for each of: Float, Double, Integer32, Integer64, Vector2, Vector, Vector4, Quaternion, Transform, String, Boolean, Rotator, Name, Soft Object Path, Soft Class Path
- **Get Graph Parameter** — *New <Type> Parameter* for each of: Float, Double, Integer32, Integer64, Vector2, Vector, Vector4, Quaternion, Transform, String, Boolean, Rotator, Name, Soft Object Path, Soft Class Path
- **Attribute Cast** — *Cast to <Type>* for each of: Float, Double, Integer32, Integer64, Vector2, Vector, Vector4, Quaternion, Transform, String, Boolean, Rotator, Name, Soft Object Path, Soft Class Path

### Per-operation aliases

Each operation below is its own palette entry. Descriptions: [src] enum tooltip where the source has one, otherwise [epic].

#### Custom HLSL — 6 operations (`EPCGKernelType`)

| operation | description |
|---|---|
| **Point Processor** | [src] Kernel executes on each point in first input pin. |
| **Point Generator** | [src] Kernel executes for fixed number of points, configurable on node. |
| **Texture Processor** | [src] Kernel executes on each texel in the first input pin. |
| **Texture Generator** | [src] Kernel executes for each texel in a fixed size texture, configurable on node. |
| **Custom** | [src] Execution thread counts and output buffer sizes configurable on node. All data read/write indices must be manually bounds checked. |
| **Attribute Set Processor** | [src] Kernel executes on each element of the attribute sets in the first input pin. |

#### Attribute Reduce — 5 operations (`EPCGAttributeReduceOperation`)

| operation | description |
|---|---|
| **Average** | [epic] Gathers ensemble information on which the graph could operate on. For example, you could find the average position to use as a good pivot to scale against for all points in a Point Data. |
| **Max** | [epic] Gathers ensemble information on which the graph could operate on. For example, you could find the average position to use as a good pivot to scale against for all points in a Point Data. |
| **Min** | [epic] Gathers ensemble information on which the graph could operate on. For example, you could find the average position to use as a good pivot to scale against for all points in a Point Data. |
| **Sum** |  |
| **Join** |  |

#### Attribute Bitwise Op — 6 operations (`EPCGMetadataBitwiseOperation`)

| operation | description |
|---|---|
| **And** | [epic] Computes the result of the bitwise AND between two attributes. |
| **Not** | [epic] Computes the result of the bitwise NOT between two attributes. |
| **Or** | [epic] Computes the result of the bitwise OR between two attributes. |
| **Xor** | [epic] Computes the result of the bitwise XOR (Exclusive OR) between two attributes. |
| **Shift Left** | [src] << operation |
| **Shift Right** | [src] >> operation |

#### Attribute Boolean Op — 9 operations (`EPCGMetadataBooleanOperation`)

| operation | description |
|---|---|
| **And** | [epic] Computes the result of the boolean AND between two attributes. |
| **Not** | [epic] Computes the result of the boolean NOT between two attributes. |
| **Or** | [epic] Computes the result of the boolean OR between two attributes. |
| **Xor** | [epic] Computes the result of the boolean XOR (Exclusive OR) between two attributes. |
| **Nand** | [epic] Computes the result of the boolean NAND between two attributes. |
| **Nor** | [epic] Computes the result of the boolean NOR between two attributes. |
| **Xnor** | [epic] Computes the result of the boolean XNOR (Exclusive NOR) between two attributes. |
| **Imply** | [src] A -> B False only when (A=1, B=0) |
| **Nimply** | [src] A -/-> B True only when (A=1, B=0) |

#### Attribute Compare Op — 6 operations (`EPCGMetadataCompareOperation`)

| operation | description |
|---|---|
| **Equal** | [epic] Writes the comparison Equal To result between two attributes to a boolean attribute. |
| **Not Equal** | [epic] Writes the comparison Not Equal result between two attributes to a boolean attribute. |
| **Greater** | [epic] Writes the comparison Greater Than result between two attributes to a boolean attribute. |
| **Greater Or Equal** | [epic] Writes the comparison Greater Than Or Equal To result between two attributes to a boolean attribute. |
| **Less** | [epic] Writes the comparison Less Than result between two attributes to a boolean attribute. |
| **Less Or Equal** | [epic] Writes the comparison Less Than or Equal To result between two attributes to a boolean attribute. |

#### Make Rotator Attribute — 11 operations (`EPCGMetadataMakeRotatorOp`)

| operation | description |
|---|---|
| **Make Rot From X** |  |
| **Make Rot From Y** |  |
| **Make Rot From Z** |  |
| **Make Rot From XY** |  |
| **Make Rot From YX** |  |
| **Make Rot From XZ** |  |
| **Make Rot From ZX** |  |
| **Make Rot From YZ** |  |
| **Make Rot From ZY** |  |
| **Make Rot From Axes** |  |
| **Make Rot From Euler Angles** |  |

#### Attribute Maths Op — 25 operations (`EPCGMetadataMathsOperation`)

| operation | description |
|---|---|
| **Sign** | [epic] Computes the value of the Sign mathematical operation and writes the result to an attribute. Evaluates an input value and indicates whether it is positive, negative, or exactly zero. If the input is negative, this node outputs -1. If the input is exactly 0, this node outputs 0. If the input is posit … |
| **Frac** | [epic] Computes the value of the Frac mathematical operation. Takes in an input value and returns the fractional portion of that value. For example, for an input value X, the result is X minus the Floor of X. The output value ranges from zero to one, inclusive on the low end, exclusive on the high end. |
| **Truncate** | [epic] Computes the value of the Truncate mathematical operation and writes the result to an attribute. This expression truncates a value by discarding the fractional part while leaving the whole number. For example, a value of 1.4 is truncated to 1. |
| **Round** | [epic] Computes the value of the Round mathematical operation and writes the result to an attribute. This expression takes in an input value and rounds it to the nearest whole number. |
| **Sqrt** | [epic] Computes the value of the Square Root mathematical operation on an input and writes the result to an attribute. |
| **Abs** | [epic] Computes the value of the Absolute Value mathematical operation. Converts an input attribute value into a positive value and writes the result to an attribute. |
| **Floor** | [epic] Computes the value of the Floor mathematical operation. Takes in an input value, rounds it down to the nearest integer, and writes the result to an attribute. |
| **Ceil** | [epic] Computes the value of the Ceiling mathematical operation. Takes an input value and rounds it up to the next integer. |
| **One Minus** | [src] 1 - X operation |
| **Inc** | [src] X + 1 operation |
| **Dec** | [src] X - 1 operation |
| **Negate** | [src] -X operation |
| **Add** | [epic] Computes the value of the Add mathematical operation. Takes two input values, adds them together, and writes the result to an attribute. |
| **Subtract** | [epic] Computes the value of the Subtract mathematical operation. This expression takes in two inputs and subtracts the second input from the first. |
| **Multiply** | [epic] Computes the value of the Multiply mathematical operation. Takes in two input values, multiplies them, and writes the result to an attribute. |
| **Divide** | [epic] Computes the value of the Divide mathematical operation. Takes in two inputs, divides the first input by the second, and writes the result to an attribute. |
| **Max** | [epic] Computes the value of the Max mathematical operation on attribute(s) and writes the result to an attribute. This operation takes in two input values and outputs the higher of the two. |
| **Min** | [epic] Computes the value of the Min mathematical operation on attribute(s) and writes the result to an attribute. This operation takes in two input values and outputs the lower of the two. |
| **Pow** | [epic] Computes the value of the Power mathematical operation. This expression takes in two values: a base and an exponent. It raises the base value to the exponent power and outputs the result as an attribute. |
| **Modulo** | [epic] Computes the value of the Modulo mathematical operation. Takes in two input values and divides the first by the second. It then returns the remainder and writes that as an attribute. |
| **Set** | [epic] Sets the output attribute to the value of the provided attributes. |
| **Clamp** | [epic] Computes the value of the Clamp mathematical operation. Takes in input values and constrains them to a specific range. |
| **Lerp** | [epic] Computes the value of the Linear Interpolate mathematical operation. This expression draws a line between two points and uses a third Ratio value to determine the value of a point along that line. It then writes this value to an attribute. |
| **Mul Add** | [src] Multiply Add (A + B * C) |
| **Add Modulo** | [src] Add Modulo (A + B) % C. If B is negative: (A + C + B) % C |

#### Attribute Rotator Op — 6 operations (`EPCGMetadataRotatorOperation`)

| operation | description |
|---|---|
| **Combine** | [epic] Combines two rotation values and writes the result as an attribute, combining first A, then B. |
| **Invert** | [epic] Finds the inverse of a provided Rotator and writes the result as an attribute. |
| **Lerp** | [epic] Linearly interpolates between two Rotator inputs A and B based on the Ratio. This applies 100 percent of A when Ratio is 0 and 100 percent of B when Ratio is 1. |
| **Normalize** | [epic] Clamps an angle to a range of -180 to 180 and writes the result as an attribute. |
| **Transform Rotation** | [epic] Transforms a rotation by a given Transform. This node takes a rotation as input and applies the given transform. |
| **Inverse Transform Rotation** | [epic] Transforms a Rotator by the inverse of the supplied transform. |

#### Attribute String Op — 9 operations (`EPCGMetadataStringOperation`)

| operation | description |
|---|---|
| **Append String** |  |
| **Replace String** |  |
| **Substring** | [src] True if string A contains substring B. |
| **Matches** | [src] True if string A matches substring B exactly. |
| **To Upper** | [src] Convert all characters to upper case. |
| **To Lower** | [src] Convert all characters to lower case. |
| **Trim Start** | [src] Trim whitespace from the beginning of the string. |
| **Trim End** | [src] Trim whitespace from the end of the string. |
| **Trim Start and End** | [src] Trim whitespace from the beginning and end of the string. |

#### Attribute Transform Op — 3 operations (`EPCGMetadataTransformOperation`)

| operation | description |
|---|---|
| **Compose** | [epic] Composes two Transforms in order: A B. Order is important when composing Transforms. A B yields a Transform that first applies A, then B to any subsequent transformation.The result is written to an attribute. |
| **Invert** | [epic] Inverts the input Transform and writes the new Transform as an attribute. |
| **Lerp** | [epic] Linearly interpolates between two Transform inputs A and B based on the Ratio. This applies 100 percent of A when Ratio is 0 and 100 percent of B when Ratio is 1. |

#### Attribute Trig Op — 9 operations (`EPCGMetadataTrigOperation`)

| operation | description |
|---|---|
| **Acos** | [epic] Returns the inverse cosine (arccos) of an input and writes the result to an attribute. |
| **Asin** | [epic] Returns the inverse sine (arcsin) of an input and writes the result to an attribute. |
| **Atan** | [epic] Returns the inverse tangent (arctan) of an input and writes the result to an attribute. |
| **Atan2** | [epic] Returns the inverse tangent (arctan2) of 2 inputs (B/A) and writes the result to an attribute. |
| **Cos** | [epic] Returns the cosine (cos) of an input and writes the result to an attribute. |
| **Sin** | [epic] Returns the sine (sin) of an input and writes the result to an attribute. |
| **Tan** | [epic] Returns the tangent (tan) of an input and writes the result to an attribute. |
| **Deg To Rad** | [epic] Returns a radians value based on the input in degrees and writes the result to an attribute. |
| **Rad To Deg** | [epic] Returns a degrees value based on the input in radians and writes the result to an attribute. |

#### Attribute Vector Op — 10 operations (`EPCGMetadataVectorOperation`)

| operation | description |
|---|---|
| **Cross** | [epic] Outputs the Cross Product of two input vectors. |
| **Dot** | [epic] Returns the Dot Product of two input Vectors. |
| **Distance** | [epic] Calculates the distance between two Vector inputs. |
| **Normalize** | [epic] Outputs a normalized copy of the Vector, ensuring it is safe to do so based on the length. Returns a zero vector if vector length is too small to safely normalize. |
| **Length** | [epic] Returns the length of a Vector stored in an input vector. |
| **Rotate Around Axis** | [epic] Calculates and returns the result of Vector A rotated by Angle (Deg) around Axis. |
| **Transform Direction** | [epic] Transforms an input direction Vector by the supplied transform. Does not change its length.The result is written to an attribute. |
| **Transform Location** |  |
| **Inverse Transform Direction** | [epic] Transforms a direction Vector by the inverse of the input Transform, but does not change its length. The result is written to an attribute. |
| **Inverse Transform Location** | [epic] Transforms a location by the inverse of the input Transform. The result is written to an attribute. |

---

## 5. Deprecated and replaced

| node | class | since | replacement [src] |
|---|---|---|---|
| Density Remap | `UPCGDensityRemapSettings` | 5.5 | Superseded by UPCGAttributeRemapSettings |
| Generate Landscape Textures | `UDEPRECATED_PCGGenerateGrassMapsSettings` | — | class is prefixed `UDEPRECATED_` |
| Copy Attributes | `UPCGAttributeTransferSettings` | 5.5 | Use UPCGCopyAttributeSettings |
| Copy Attributes | `UPCGMetadataOperationSettings` | 5.5 | Use UPCGCopyAttributeSettings |

The palette name **Density Remap** still exists, but it now creates **Attribute Remap** (section 4) — the old `UPCGDensityRemapSettings` class is the deprecated one. Same for **Generate Grass Maps** → Generate Landscape Textures.

---

## 6. Name mismatches with Epic's docs

Epic's reference is the 5.8 edition and lags the engine: it names 123 nodes; **99 of the 214 placeable 5.7.4 classes** match one of those by title. The rest are documented here from source only.

**In Epic's page but not a 5.7.4 node title or alias:**

- *Curve Remap Density* (Density)
- *Distance to Density* (Density)
- *Discard Points on Irregular Surface* (Filter)
- *Apply On Actor* (Generic)
- *Get Data Count* (Generic)
- *Get Entries Count* (Generic)
- *Sort Points* (Generic)
- *Spatial Data Bounds To Point* (Helpers)
- *Grid Size* (Hierarchical Generation)
- *Load Alembic File* (Input Output)
- *Copy Attribute* (Metadata)
- *Create Attribute* (Metadata)
- *Filter Attributes by Name* (Metadata)
- *Transfer Attribute* (Metadata)
- *Build Rotation From Up Vector* (Point Ops)
- *Texture Sampler* (Sampler)
- *Get Points Count* (Spatial)
- *Split Splines* (Spatial)
- *Point from Player Pawn* (Spawner)

**Names this project's docs use that differ from the 5.7.4 node title:**

| written in our docs | 5.7.4 palette | note |
|---|---|---|
| Point Filter Range (`ue_working_rules.md`, 7d.10) | *Point Filter Range* | valid — alias of **Filter Attribute Elements by Range** |
| Polygon2D Operation (checklist 18b) | **Polygon Operation** | internal name is `Polygon2DOperation`; `CutWithPaths` exists |
| Data From Actor (`ue_working_rules.md`) | **Get Actor Data** | class is still `UPCGDataFromActorSettings` |
| Density Remap | *Density Remap* | now an alias of **Attribute Remap**; the old class is deprecated |

---

## 7. PCGBiomeCore — graph assets, not nodes

`Experimental/PCGBiomeCore` (enabled) ships **no C++ node classes** — only PCG graph assets, Blueprints and data assets (114 files). Its graphs appear in the palette as subgraphs. Listed by folder [src: plugin Content]:

- **AssemblyBehavior** (2): `BiomeCore_AssemblyBehavior_Template`, `BiomeCore_DefaultAssemblyBehavior`
- **BiomeAssets** (10): `DefaultAsset`, `BiomeAsset`, `BiomeAssetBaseTemplate`, `BiomeAssetTemplate`, `BiomeAsset_AssemblyOptions`, `BiomeAsset_AssetOptions`, `BiomeAsset_DebugOptions`, `BiomeAsset_FilterOptions`, `BiomeAsset_MeshOptions`, `BiomeAsset_RunTimeOptions`
- **(root)** (2): `BiomeCore`, `LocalBiomeCore`
- **BiomeDefinitions** (3): `DefaultBiome`, `BiomeDefinition`, `BiomeDefinitionTemplate`
- **BiomeGenerators** (6): `DefaultGenerator`, `BiomeGenerator_ElevationLines`, `BiomeGenerator_SubGeneratorSetup`, `BiomeGenerator`, `BiomeGeneratorTemplate`, `BiomeGenerator_SpatialNoiseSettings`
- **Blueprints** (11): `BP_PCGBiomeBaseActor`, `BP_PCGBiomeCore`, `BP_PCGBiomeCore_Runtime`, `BP_PCGBiomeCore_RuntimeGroundScatter`, `BP_PCGBiomeExclusionSpline`, `BP_PCGBiomeExclusionVolume`, `BP_PCGBiomeSpline`, `BP_PCGBiomeTexture`, `BP_PCGBiomeVolume`, `BP_PCGCustomBiomeData`, `BP_PCGSpecificCropField`
- **Core** (45): `BiomeCore_ApplyScaleAndBounds`, `BiomeCore_AssemblyInstancer`, `BiomeCore_AssignAssetsToPoints`, `BiomeCore_AssignDefinitionsToAssets`, `BiomeCore_BoundsFromAssembly`, `BiomeCore_BoundsFromMeshLoop`, `BiomeCore_BuildRootAssetTable`, `BiomeCore_ChildTransformLoop`, `BiomeCore_CullPointsOutsidePartitionActors`, `BiomeCore_CullUnusedSubTypes`, `BiomeCore_CullUnusedSubTypesInnerLoop`, `BiomeCore_DifferenceByPriority`, `BiomeCore_DifferenceByRecursionLevel`, `BiomeCore_Filters`, `BiomeCore_Filters_Inst`, `BiomeCore_HashRuntimeAssetPath`, `BiomeCore_IsolateAssets`, `BiomeCore_MergeStringAttributeEntriesInnerLoop`, `BiomeCore_MergeStringAttributeEntriesLoop`, `BiomeCore_OverlapWithChildrenGraph`, `BiomeCore_PerGeneratorLoop`, `BiomeCore_PostDifference_FilterAssemblies`, `BiomeCore_PrepareChildRecursion`, `BiomeCore_PrepareChildWeights`, `BiomeCore_PrepareGroundScatterAssetsAndDefinitions`, `BiomeCore_PrepareTagsData`, `BiomeCore_ProjectTexture`, `BiomeCore_ProjectionLoop`, `BiomeCore_ResolveAssetProperties`, `BiomeCore_ResolveGeneratorsFromAssets`, `BiomeCore_RestoreDataByGenerators`, `BiomeCore_RestoreTags`, `BiomeCore_RootTransformLoop`, `BiomeCore_RunFiltersLoop`, `BiomeCore_RunGenerators`, `BiomeCore_RunTransformGraph`, `BiomeCore_SelfPruningGraph`, `BiomeCore_SetChildFilterBoundsFromWeights`, `BiomeCore_TagAssetsWithGenerators`, `BiomeCore_TilePartitioner`, `BiomeCore_ValidateAssetPaths`, `BiomeLocalCache`, `BiomeLocalCache_Spline`, `BiomeLocalCache_Texture`, `BiomeLocalCache_Volume`
- **EdMode** (2): `BiomeSplineTool`, `BiomeVolumeTool`
- **Filters** (4): `BiomeFilter_Density_Noise`, `BiomeFilter_Density_Noise_Multiply`, `BiomeFilter_WaterDistance_Level`, `BiomeFilter`
- **GraphTemplates** (1): `TPL_BiomeCore_Generator`
- **Runtime** (14): `BiomeCoreRuntime_GenerationMethod`, `BiomeCoreRuntime_Graph`, `BiomeCoreRuntime_InfluenceType`, `BiomeRuntimeAsset`, `BiomeRuntimeAssetBaseTemplate`, `BiomeRuntimeAssetTemplate`, `BiomeCore_ResolveAssetPropertiesAndGeneratorGraphLoop`, `GroundScatterAccumulateWeights`, `GroundScatterGeneratorGraphGPU`, `GroundScatterGeneratorGraphGPUTemplate`, `GroundScatterRunGenerators`, `GroundScatterWeightsDistributionLoop`, `PointGeneratorLS`, `PointGeneratorRVT`
- **Setup** (5): `BiomeCore_DefaultBiomeTextureProj_Inst`, `DefaultBiomeSpline`, `DefaultBiomeVolume`, `LandscapeDataSetting`, `WorldRayHitSetting`
- **Specific** (3): `SpecificBiomeData_Template`, `SpecificCropField`, `SpecificCropField_Generator`
- **Transforms** (5): `BasicSecondaries`, `DuplicatePattern`, `DuplicatePoints`, `DuplicateUp`, `MoveUp`
- **Utils** (1): `BiomeCore_PrepareAssetTags`

---

## 8. Project notes — nodes this project uses

Facts measured in `Space_Colony` or read from source this session. Full context: `ue_working_rules.md`.

### Where they sit

```
PCG_SurfaceTest
  Subgraph (SG_SurfaceSource) -> Transform Points -> Match And Set Attributes <- Load Data Table
                                                     -> Static Mesh Spawner
PCG_Vegetation  (7d.9, on PCGVolume2)
  Subgraph (SG_SurfaceSource) .Out 1 -> Multiply (UV -> MaskUV) -> Output
SG_SurfaceSource  (L0)
  Mesh Sampler (Extract UV -> `UV`, channel 0) --> Copy Points <-- Get Actor Data (By Tag)
  Copy Points -> Output pin `Out 1`   (the `Out` pin carries nothing)
  8 x Get Graph Parameter: SurfaceMesh, SurfaceTag, SamplingRadius, Max Num Samples,
                           Sub Sample Density, Requested LOD Type, Remove Hidden Triangles, Seed
```

### Traps, with evidence

| node | trap | evidence |
|---|---|---|
| **Mesh Sampler** | `Requested LOD Type = Render Data` samples LOD 0 of the render data — on a **Nanite** mesh that is the **fallback**, not the Nanite geometry | [src] `PCGMeshSampler.h` default `RenderData`; measured: Fallback Target `Auto` cut LOD 0 from 567,000 to **1,837** tris |
| **Mesh Sampler** | point spacing is **at least 2 × Sampling Radius** | [src] tooltip; measured radius 1000 → min spacing **20.0 m** |
| **Mesh Sampler** | `Max Num Samples = 0` means **no limit**, not zero points — it fills the whole surface | [src] *"If 0 or default value, mesh will be maximally sampled"*, loop `MeshSurfacePointSampling.cpp:377-427`; measured 2026-09-22: **17,066** points at radius 1000, nearest neighbour 20.0–26.2 m (an earlier 2,336 was not a full fill) |
| **Mesh Sampler** | the node's stock `Max Num Samples` (500) caps a large surface | measured: 7.9 km belt starved at 500 |
| **Mesh Sampler** | `Remove Hidden Triangles` only runs when `Voxelize` is on | [src] `EditCondition = bVoxelize` — with Voxelize off it does nothing |
| **Mesh Sampler** | two seeds exist: `Sampling Options → Random Seed` and the node `Seed` (needs `Use Seed`) | [src] class properties — check which one a Seed parameter drives |
| **Get Actor Data** | `Get Single Point` + `By Tag` + `select_multiple = false` silently takes the **first** matching actor | measured: ring structure shared `SurfaceSource`; every instance spawned **76,444 cm** too high |
| **Copy Points** | defaults apply the target's rotation **and scale to positions** | [src] `bApplyTargetRotationToPositions`, `bApplyTargetScaleToPositions` default `true`; a scaled surface actor scales the point layout |
| **Transform Points** | `Absolute Scale` off = scale multiplies | [src]; `PCG_SurfaceTest` uses relative 50 |
| **any input pin** | dragging a new wire onto a connected input pin **adds** a second connection, it does not replace the first — both datasets flow through and the node runs on each | measured 2026-09-30: rewiring the zone split to the lot line left all three filters at `In edges = 2`, so 36 old scatter points spawned alongside 55 lot points. Check with `len(pin.edges)` |
| **Spline Sampler** | `Compute Distance` names its attribute `Distance` by default — the same name the **Distance** node writes | [src] `PCGSplineSampler.h:28`; rename to `RoadDist` or the two silently fight |
| **Transform Points** | `Absolute Offset` **off** rotates the offset into the point's own frame; on, it is world space | [src] `PCGTransformPoints.cpp:207-215`; this is what makes one number mean "12 m left of the road" on a curving spline |
| **Distance** | an unconnected **`Target`** pin makes the node a silent **pass-through** — no attribute, no warning; the failure surfaces downstream as *"Attribute … does not exist"* | [src] `PCGDistance.cpp:148-153` `PCGGather::GatherDataForPin(Source)`; cost one generate 2026-09-28 |
| **Distance** | `Output Distance Vector` writes `TargetPos − SourcePos`, i.e. **from** the source point **toward** the nearest target — use it directly as a facing direction | [src] `PCGDistance.cpp:356-365`; measured: buildings face the road to **0.92° median** |
| **Spline Sampler** | a freshly added node defaults to Mode **Subdivision**, 1 per segment — a 2,287 m / 5-point road yields **9 samples 208-392 m apart**, not a dense line | measured 2026-09-28: `RoadDir` from that sampler put facings **75° median** off; Mode `Distance`, increment 100 → 0.92°. Duplicate an existing sampler (Ctrl+W) to carry settings |
| **Normal To Density** | compares every point against **one fixed vector** (`UpVector`) — wrong on a cylinder | [src] `Normal` default `FVector::UpVector`; use per-point up with Attribute Vector Op instead (7d.10) |
| **Get Graph Parameter** | a newly added graph parameter starts at **0** and is immediately marked overridden, silently replacing the node's working value | measured 2026-09-16 on `SG_SurfaceSource` |
| **Subgraph** `SG_SurfaceSource` | the points leave on **`Out 1`**; `Out` is empty — wiring `Out` gives no points and **no error** | measured 2026-09-22: output node pins `Out` 0 edges, `Out1` 1 edge; `PCG_Vegetation` wired to `Out` → Multiply got nothing (a maths op with no data on its main input returns nothing, `PCGMetadataOpElementBase.cpp:639-643`) |
| **Attribute Maths Op** *(all metadata ops)* | an unconnected input takes a **typed-in constant** — right-click the pin → *Activate Inline Constant* · *Convert to Vector2*; connecting one input switches the others on | [src] `PCGEditorGraphNodeBase.cpp:251-285, 1405-1414`; allowed types `PCGMetadataHelpers.h:107` (no Float / Quat / Transform); marked experimental |
| **Get Texture Data** | the default **GPU read returns a low mip** — a 1024 mask came back at **64 px** (one texel ≈ 123 m), so mask edges bleed and points with a true value of 0 survive. Fix: tick **Force Editor Only CPU Sampling** | measured 2026-09-22 on the mountain mask: PCG densities matched a 64-px downsample to a median of 0.0005; with CPU sampling on they match the 1024 file (median 0.0005, max 0.002 = the 8-bit step) and the 2,196 false survivors vanished. PCG duplicates the texture with NoMipmaps + uncompressed to do it (`PCGTextureData.cpp:562-587`) |
| **Sample Texture** | drops every point whose sampled density is **0** — black mask = no points, not density-0 points | [src] `PCGTextureData.cpp:434` returns `OutDensity > 0 \|\| bKeepZeroDensityPoints`; `PCGSampleTexture.cpp` writes a point only when that is true |

### Planned nodes (checked to exist in 5.7.4)

| plan | node | confirmed |
|---|---|---|
| 7d.9 Gaea masks | **Sample Texture** | exists; Sampler category |
| 7d.10 slope rules | **Attribute Vector Op** → *Dot*, *Normalize*; **Point Filter Range** | Vector Op has 10 operations incl. Dot and Normalize; Point Filter Range is an alias |
| 17 L2 Streets | **Spline Sampler** | exists |
| 18b block subdivision | **Polygon Operation** → `CutWithPaths` | [src] *"Cuts polygons with paths by completing them using the polygon bounds. If both ends of the path are not outside the input polygons, the results might be incorrect."* |

---

## 9. Coverage and gaps

- **11 nodes have no description** in either source or Epic's page: Get Actor Data Layers, Partition by Actor Data Layers, Compute Graph, Grid Linkage, Input Node, Create Constant, Named Reroute Usage, Duplicate Cross-Sections, Subdivide Segment, Subdivide Spline, Instanced Skinned Mesh Spawner. Their settings tables are the only documentation.
- **Pins are partial.** Detected from `InputPinProperties()` / `OutputPinProperties()` where they name a data type directly; many nodes inherit the default pins and show none. Check the node in the editor for exact pins.
- **Settings come from headers.** Properties added through metadata, instanced structs or dynamic pins (e.g. Select (Multi), Switch) are not listed. Struct settings are expanded one level (↳) when the struct has 16 fields or fewer; selector structs such as `FPCGAttributePropertyInputSelector` have custom UI and no fields to list.
- **Base classes are omitted** from sections 2–3: `UPCGDynamicMeshBaseSettings`, `UPCGFilterDataBaseSettings`, `UPCGBaseSubgraphSettings`, `UPCGControlFlowSettings`, `UPCGDataAttributesAndTagsSettingsBase`, `UPCGSettingsWithDynamicInputs`, `UPCGExternalDataSettings`, `UPCGMetadataSettingsBase`, `UPCGSubdivisionBaseSettings`.
- **Epic's page is 5.8.** Where an [epic] description disagrees with [src], trust [src] for this 5.7.4 project.

---

## 10. Sources and how this was built

- Engine source, UE 5.7.4 install: every `UCLASS` deriving from `UPCGSettings` under `Engine/Plugins/PCG/Source`, `PCGInterops`, `Experimental/PCGInterops`, `Experimental/PCGBiomeCore`. Title / tooltip / category from `GetDefaultNodeTitle()`, `GetNodeTooltipText()`, `GetType()` (inherited where not overridden, named constants resolved inside their namespace). Settings from `UPROPERTY(EditAnywhere …)` with their comments. Aliases from `GetPreconfiguredInfo()`; enum options from `UENUM`s with `UMETA`.
- Epic node reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine (read 2026-09-16, page marked 5.8).
- Plugin maturity: each plugin's `.uplugin` (`IsBetaVersion` / `IsExperimentalVersion`). Enabled state: `Space_Colony.uproject`.
- **Regenerate, don't hand-edit sections 1–7 and 9.** `python Tools/pcg_reference/build.py` rescans the engine and rewrites this file (edit `ENGINE` in `build.py` after an upgrade, e.g. to 5.8 for Mesh Terrain). Epic's page is cached in `Tools/pcg_reference/epic_nodes.json` (it renders client-side, so refreshing it needs a browser capture — see `parse_epic.py`). Section 8 lives in `gen_doc.py` and is written by hand from project evidence.

