# Day/Night Design — Interior Lighting

Decided Week 2 (System 2), while working out `MPC_DayNight` and the material system.
Supersedes any earlier assumption of a mirror-bounce or fully-simulated light path.

## The mechanism

The two large wing panels (`SolarPanel2` / `SolarPanel3` in the level — leftover blockout
names, not functionally solar power panels) act as a **physical shutter**, not a mirror.

- **Day** — wings rotate open, out of the way. The window band is just glass; with nothing
  blocking it, sunlight shines straight through, no reflection or redirection involved.
- **Night** — wings rotate closed, physically covering the window from outside. Since the sun
  in open space never actually sets, blocking it is the only way to produce "night." The
  wing's inward-facing surface (visible once closed) shows a fake starfield, like a large LED
  display, so the view from inside still reads as a night sky rather than a blank shutter.

This intentionally departs from the real O'Neill cylinder proposal, where hinged mirrors
reflect sunlight into the windows and day/night is produced by opening/closing that
reflection. That mechanism was dropped because:

1. The project's own scope doc explicitly does not require a physically simulated mirror
   mechanism, or scientifically accurate light simulation.
2. Even the "accurate" version would be faked at build time anyway — Lumen does not reliably
   transport light through translucent glass for GI purposes, so a placed light standing in
   for the sun is the practical technique either way.
3. The shutter version is more buildable and demonstrable for a TA portfolio: it requires a
   genuine working animated mechanism (panel rotation) rather than a static reflection concept,
   and gives `M_Emissive` a concrete, well-defined job (the night-sky LED display).

## What this means for the three materials

- **`M_Window`** — plain transparent/translucent glass. No day/night emissive logic of its own;
  brightness comes from whether real light is currently reaching it (wing open) or not (wing
  closed), not from anything the glass material does.
- **`M_Emissive`** — drives the fake starfield LED display on the wing's inward face when closed.
- **`M_Structural`** — unaffected; the wing panel's own body/structure.

## Practical lighting technique

Even with the wing open and the window physically unblocked, we still place an authored light
at/near the window opening to represent "the sun is now visible here," rather than relying on
Lumen to correctly compute transport through the glass mesh. This isn't a narrative fake — it's
the same practical technique real-time productions use for sunlight-through-windows generally,
independent of whether the light path is "really" direct sun or mirror-redirected.

## `MPC_DayNight` parameters (already created)

| Parameter | Type | Purpose |
|---|---|---|
| `DayNightBlend` | Scalar | Master 0–1 day/night state |
| `WindowEmissiveIntensity` | Scalar | Strength of the placed stand-in light / starfield display |
| `WindowEmissiveColor` | Vector | Color of the above |
| `AmbientTint` | Vector | Subtle scene-wide color shift between states |

**Not yet built, optional enhancement:** wire the wing panels' own rotation to
`DayNightBlend` as well, so one parameter drives both the physical mechanism and the
resulting light — matches the System 2 checkpoint ("toggling one MPC value shifts
everything") but with an added visible mechanical payoff. Not required for the Week 2
checklist itself.

## Exterior (separate system, not connected to the above)

Ultra Dynamic Sky, with **Space Mode enabled** (starfield, no atmospheric scatter/clouds) —
appropriate for vacuum, and reinforces why the wing/window mechanism is needed at all (no
atmosphere means no ambient fill; without it, the interior would be harsh black-and-white
contrast with nothing in between if left unlit). UDS's own day/night cycle only affects the
exterior sky and sun — it is not wired to `MPC_DayNight` and does not reach the interior,
since the hull (and closed wings) block it.
