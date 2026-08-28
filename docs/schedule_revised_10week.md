# Revised Schedule — 10 Weeks

Supersedes the 12-week plan in `execution_guide_oneill_cylinder_v2.pdf`.
Two weeks removed by merging compressible stages, not by cutting deliverables.

## Schedule

| Week | System | Focus | Friday checkpoint |
|------|--------|-------|-------------------|
| ~~1~~ | 1 | Blockout, World Partition, scale-check | ✅ **DONE** |
| ~~2~~ | 2 | Master materials + MPC day/night + custom HLSL | ✅ **DONE** |
| 3 | 3 | Python manifest schema, validator, **and** UE5 Python integration | UE5 loads + validates a manifest via Python console |
| 4 | 4 | PCG graph, single belt, placeholder cubes | One belt generates on the curved surface |
| 5 | 4 | Connect Python manifest data to PCG graph | PCG reads belt parameters from validated manifest |
| 6 | 4 | Expand to **two** belts, swap in real modules | Two belts generate with categorised modules |
| 7 | 5 | Editor Utility Widget, wired to PCG + Python | Panel regenerates a belt without touching the graph |
| 8 | 6 | Profiling baseline, HLOD, instancing, LOD pass | Before/after draw call + frame time captured |
| 9 | Polish | Lighting, hero shots on Belt A, screenshots | Day/night hero shots, tool UI, debug views captured |
| 10 | Delivery | Breakdown page, demo video, resume bullets | All deliverables complete |

## What changed from the 12-week plan, and why

**Weeks 3+4 merged into Week 3.** The original split was "build the validator standalone in VS Code,
then port it into UE5's Python environment." Writing it UE-aware from the start skips the port.
Justified by existing Python/scripting experience.

**Three belts reduced to two (Week 6).** The scope doc already states only Belt A needs hero quality,
with B and C existing "to read correctly from a distance." The PCG system demonstrates identically
on two belts. Belt C is cut, not deferred.

**Weeks 9+10 merged into Week 8.** The scope doc asks for "one clear round of optimization changes"
with before/after metrics — that is one week's work unless gold-plated.

## What was deliberately NOT cut

**Polish and delivery (Weeks 9–10).** This is where the portfolio is actually produced — hero shots,
breakdown page, write-ups. Cutting here means doing all the work and failing to present it.

**The custom HLSL, the Python tool, the PCG curved-surface problem, and the optimization metrics.**
These are the four things that make this read as a Technical Artist case study rather than an
environment art piece. All retained.

## Known risk

The execution guide flags the PCG curved-surface alignment (now Week 4) as likely to overrun,
because no single node aligns rotation to a curved surface normal — it needs a custom Blueprint
function or line-trace approach. The compression elsewhere is the buffer for this. If Week 4
runs long, the project lands at 11 weeks, still ahead of the original plan.

## Art track (runs parallel)

| Weeks | Focus |
|-------|-------|
| 1–2 | Concept, silhouettes, material library plan, module list lock |
| 3–4 | Structural shells + habitat surfaces blockout |
| 5 | Kit variation — infrastructure, greenery, debris/wear |
| 6 | Texture pass, belt-wide integration check against PCG |
| 7–8 | Belt A hero detail |
| 9–10 | Lighting, screenshots, delivery — **not modeling time** |

**Module count reduced from 62 to 30** — see `module_list.xlsx`. The art guide's category ranges
(12–16 structural, etc.) describe a full production kit; 30 modules with good variation reads as
well as 62 rushed ones, and the PCG system demonstrates itself equally on either.

If art runs behind, protect Belt A hero detail over kit variation — a slightly repetitive support
belt is a smaller portfolio cost than a hero belt that is not actually hero quality.
