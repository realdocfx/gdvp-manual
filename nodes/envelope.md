# Envelope — `GDVP_NODE_ENVELOPE` ✅

[← Node Reference](README.md) · [Manual index](../README.md)

A five-stage ADSR with **independent curve shapes per stage**, velocity scaling, legato and
retrigger behaviour, optional inversion, and a click-free, level-continuous release. Source:
`gdvp_dsp_envelope.c`, payload `gdvp_node_env_t` in `gdvp_nodes.h`.

## Signal & ports

- **Output (port 0):** a control signal, typically wired into a [filter](filter.md) port 1
  (cutoff envelope) or a [VCA](vca.md) port 1 (amplitude envelope / the "gate").
- The envelope is gated by the voice (note-on starts attack, note-off starts release).

## Stages

`Attack(0) → Decay(1) → Sustain(2) → Release(3) → End(4)`. Sustain holds until note-off; release
runs from wherever the level currently is, down to zero.

## Parameters

| Parameter | Param ID / patch key | Range | Meaning |
|---|---|---|---|
| **Attack rate** | `GDVP_PARAM_ENV_ATTACK_RATE` / patch `attack` | 0–16383 | Time CV (see [time curve](#time)); higher = slower |
| **Decay rate** | `GDVP_PARAM_ENV_DECAY_RATE` / patch `decay` | 0–16383 | Time CV |
| **Sustain level** | `GDVP_PARAM_ENV_SUSTAIN_LEVEL` / patch `sustain` | 0–16383 | Held amplitude (expanded to 16-bit internally) |
| **Release rate** | `GDVP_PARAM_ENV_RELEASE_RATE` / patch `release` | 0–16383 | Time CV |
| **Attack curve** | patch `attack_curve` | 0–3 | `0`=Linear, `1`=Log, `2`=Exp, `3`=Sigmoid |
| **Decay curve** | patch `decay_curve` | 0–3 | as above |
| **Release curve** | patch `release_curve` | 0–3 | as above |
| **Velocity scale** | patch `velocity_scale` | 0–65535 | How strongly note velocity scales output |
| **Flags** | (node `flags`) | bitmask | bit0 Legato, bit1 Retrigger, bit2 Invert, bit3 Expressive, bit4 Release-now |

## Behaviour notes

### Time CV → rate, the x⁶ law {#time}
The staging pool stores canonical 14-bit **time** CVs, but the DSP needs a phase **increment**.
The conversion (`gdvp_cv_to_env_rate`) inverts the CV (so `0` = fastest, `16383` = slowest) and
applies an **x⁶ polynomial expansion**. The high exponent gives you fine control over short times
and a very wide overall range, matching how musical envelope times feel. A base increment of 1 is
always added so an envelope can never hang (the code calls this "Zeno's paradox protection").

### Curve shapes
Each of attack, decay and release independently selects Linear / Log / Exp / Sigmoid via a LUT
(`gdvp_lut_get_envelope`). This lets you pair, say, a snappy exponential attack with a gentle
logarithmic release.

### Click-free, C0-continuous release {#release}
Release computes a proportional drop from `release_start_level` — the exact amplitude at the
moment of note-off — down to zero. The first sample of release is therefore *exactly* the level
the envelope was at, guaranteeing no step discontinuity (C0 continuity) and no click, even if you
release mid-attack. This replaced an older inverse-LUT scheme that could jump levels.

### Capacitor-charge retrigger
On a fast retrigger that begins near the peak, the attack rate is scaled up inversely with the
remaining gap so the envelope converges in well under a millisecond instead of crawling — a model
of `V(t) = V_peak − (V_peak − V_start)·e^(−t/RC)`. Low starting levels use the normal rate. This
makes rapid re-triggered envelopes feel tight rather than sluggish.

### Legato, retrigger, invert, expressive
- **Legato (bit0):** don't reset phase on an overlapping note — the envelope continues.
- **Retrigger (bit1):** restart the envelope on each note.
- **Invert (bit2):** output negative-going modulation (e.g. for inverse filter sweeps).
- **Expressive (bit3):** track continuous MPE pressure for per-note dynamics
  ([Performance: MPE](../performance.md#mpe-per-note-expression)).

### Oversampling
When the host voice is oversampled, envelope rates are halved with a guard that prevents a
non-zero rate from rounding to zero (`GDVP_OS_RATE`), so timing is consistent at 1× and 2×.

## Related
- Wire to [Filter](filter.md) port 1 for cutoff envelopes; to [VCA](vca.md) port 1 for amplitude.
- Filter-specific envelope CCs (75–78) are listed on the [Filter page](filter.md).

---

[← Node Reference](README.md) · [Manual index](../README.md)
