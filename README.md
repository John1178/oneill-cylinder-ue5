# O'Neill Cylinder — Space Colony

A procedurally-assisted O'Neill cylinder space habitat, built in **Unreal Engine 5.7** as a
solo Technical Artist portfolio project. Open-type cylinder, ~3 months, six core systems:
blockout, master materials, a Python asset-manifest tool, curved-surface PCG building
placement, an Editor Utility Widget for scene control, and World Partition / HLOD
optimization.

![exterior view](docs/images/exterior.png)

## Status: Week 1 — blockout

- Station shell blocked out in Blender, imported as FBX
- Rescaled from an accidental ~4.5x oversize to **444.17 m diameter × 1787.77 m long**,
  verified against a human reference mesh and independently confirmed in-engine
- World Partition converted and working
- A live Unreal ⇄ Python tool connection is set up for scripted editor work (see
  `Plugins/UnrealMCPython/`)

## Setup

This repo excludes third-party marketplace content (**UltraDynamicSky**, **StarterContent**)
to stay small and licence-clean. After cloning:

1. Open `Space_Colony.uproject` in UE 5.7
2. Re-add UltraDynamicSky (Fab/Marketplace) and StarterContent (Content Browser → Add →
   Starter Content) if you want the level to open without missing-asset warnings
3. Git LFS is required — `git lfs install` before cloning

## Interesting problems

**Curved-surface PCG.** Standard placement (`Transform Points` etc.) randomizes rotation but
doesn't align to the surface normal of a curved interior — buildings placed this way tilt off
the hull instead of standing "up" relative to the local surface. Solving this needs a custom
alignment approach rather than a drag-and-drop node. Not started yet — this is the Week 5
milestone.

**Lighting a sealed interior.** Ultra Dynamic Sky assumes an outdoor scene with a sun overhead;
inside a closed cylinder there's no sky to catch it. Real O'Neill cylinder designs solve this
with mirror panels bouncing sunlight in through window strips — the blockout already has both,
but nothing currently uses them for lighting. Diagnosed, not yet solved.

## Tech

Unreal Engine 5.7 · World Partition · PCG · Python (Editor scripting)

## License

All rights reserved for now. Ask if you want to reuse anything.
