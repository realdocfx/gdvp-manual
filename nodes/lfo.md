# LFO — `GDVP_NODE_LFO` ✅

[← Node Reference](README.md) · [Manual index](../README.md)

A **multi-timescale** low-frequency oscillator — a "time synthesis engine" that derives three
modulation layers (meso, micro, macro) from a single shared phase, with organic chaos drift and
key-sync. It shares the oscillator's phase machinery but adds depth-layered output. Source:
`gdvp_dsp_lfo.c`, payload `gdvp_node_lfo_t` in `gdvp_nodes.h`.

## Signal & ports

- **Output (port 0):** a modulation signal, wired into any modulatable input — a [filter](filter.md)
  port 1 (filter sweep), an [oscillator](oscillator.md) (vibrato / PWM), a [VCA](vca.md) (tremolo).
- **Mod input:** an external CV can modulate the LFO **rate** linearly (FM of the LFO).

## Parameters

| Parameter | Patch key / field | Range | Meaning |
|---|---|---|---|
| **Shape** | `shape` | 0–5 | `0`=Sine, `1`=Square, `2`=Triangle, `3`=Saw, `4`=Sample&Hold, `5`=Noise |
| **Rate** | `rate` (`target_rate_cv`) | 0–16383 | Base rate, **logarithmically mapped** via `GDVP_LUT_LFO_INC` |
| **Meso depth** | `meso_depth` | 0–16383 | Rhythm/gesture layer (1× the base phase) |
| **Micro depth** | `micro_depth` | 0–16383 | Texture layer (16× rate, toward audio-rate shimmer) |
| **Macro depth** | `macro_depth` | 0–16383 | Evolution/drift layer (filtered chaos) |
| **Inertia** | `inertia` (`rate_inertia`) | 0–15 | Rate-slew EMA shift; `0` = instant, higher = sluggish/organic |
| **Sync mode** | `sync_mode` | 0–2 | `0`=Free, `1`=Transport sync, `2`=Key sync |
| **Polarity** | flag bit0 | uni/bi | Bipolar vs unipolar output |

## Behaviour notes

### Three timescales from one phase
A single 32-bit `global_phase` advances each sample; the kernel reads it three ways at zero extra
cost: the **meso** layer indexes the phase directly (1×), the **micro** layer uses `phase << 4`
(16× faster, for shimmer/texture), and the **macro** layer is a one-pole EMA-filtered xorshift
chaos source that slowly modulates the effective rate (drift/evolution). The three depths are
**perceptually squared** (`depth² >> 14`) before mixing so crossfading between layers sounds
smooth rather than abrupt. Set a single layer for a conventional LFO; combine them for evolving,
non-repeating modulation.

### Logarithmic rate + inertia
Rate CV is mapped logarithmically through a LUT, so the knob feels even across a wide span
(sub-Hz drifts up to fast shimmer). `rate_inertia` slews the rate change itself — turn it up and
rate moves *glide* rather than jump, which is what gives the LFO its "organic" feel.

> ℹ️ **When you'll hear it (and when you won't).** SLEW MASS only acts while the rate is
> *changing* — a knob move, a MIDI CC, or DAW automation. On a static rate it is silent **by
> design**: it is a glide on rate transitions, not a modifier of the steady tone. To hear it,
> hold a note and sweep FREQUENCY with SLEW MASS at zero, then again at maximum — the second
> sweep arrives noticeably late (about ¾ s of lag at full mass). Key-sync note-ons snap the
> rate, so per-note restarts are always immediate regardless of mass.

### Sync {#sync}
- **Key sync (mode 2):** ✅ works. A HARD_RESET (note-triggered) zeros the phase and snaps the
  smoothed rate, so the LFO restarts in phase on each note — essential for consistent per-note
  vibrato onset.
- **Transport sync (mode 1):** ⚠️ **not yet active.** The LFO kernel currently receives the
  transport `tick_mask` but casts it to `(void)` (a comment marks this "Phase 2"). So selecting
  transport-sync does not yet lock the LFO to tempo on this build. See
  [Performance: tempo](../concepts/performance.md#tempo) and [Appendix A](../appendix/engine-status.md).

### Sample & Hold / Noise shapes
Shapes 4 and 5 use the LFO's own xorshift PRNG (`prng_state`) and a `sh_latch`, giving stepped
random (S&H) and noise modulation without an external source.

## Related
- Vibrato → wire to [Oscillator](oscillator.md) pitch; tremolo → wire to [VCA](vca.md);
  filter sweep → wire to [Filter](filter.md) port 1.
- Examples: `lfo_vibrato`, `lfo_tremolo`, `lfo_pwm`, `lfo_filter_sweep` ([library](../sound/patches.md#library)).

---

[← Node Reference](README.md) · [Manual index](../README.md)
