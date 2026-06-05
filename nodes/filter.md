# Filter — `GDVP_NODE_FILTER` ✅

[← Node Reference](README.md) · [Manual index](../README.md)

A **TPT-SVF** — Topology-Preserving Transform State-Variable Filter with Zero-Delay Feedback.
It is unconditionally stable across the entire Nyquist range, including self-oscillation, and
offers four response types and a cascaded slope engine from 6 to 24 dB/oct. Source:
`gdvp_dsp_filter.c`, payload `gdvp_node_filter_t` in `gdvp_nodes.h`.

## Signal & ports

- **Audio in (port 0):** the signal to filter.
- **Control in (port 1):** modulation of cutoff — the classic envelope-to-cutoff or LFO-to-cutoff
  routing in stock patches wires here.
- **Output (port 0):** filtered audio.

## Parameters

| Parameter | Param ID / patch key | Range | Meaning |
|---|---|---|---|
| **Mode** | patch `mode` / `GDVP_PARAM_FILTER_TYPE_CV` (NRPN 2/1) | 0–3 | `0`=Low-pass, `1`=Band-pass, `2`=High-pass, `3`=Notch |
| **Cutoff** | `GDVP_PARAM_FILTER_CUTOFF_CV` (CC 74) / patch `cutoff` | 0–16383 | Corner frequency; perceptually mapped (see [cutoff curve](#cutoff)) |
| **Resonance** | `GDVP_PARAM_FILTER_RESONANCE_CV` (CC 71) / patch `resonance` | 0–16383 | Emphasis at cutoff; high values self-oscillate |
| **Slope** | `GDVP_PARAM_FILTER_SLOPE` / patch `slope` | 0–3 | `0`=6, `1`=12, `2`=18, `3`=24 dB/oct (see [slope](#slope)) |
| **Drive** | `GDVP_PARAM_FILTER_DRIVE_CV` (NRPN 2/0) | 0–16383 | Pre-gain into the saturation stage |
| **Saturation type** | (node `saturation_type`) | enum | Saturation curve applied in the filter path |

### Filter envelope parameters (when a dedicated filter envelope is used)
The canonical map also defines a full filter-envelope set routed via CC: **Attack (CC 75),
Decay (CC 76), Sustain (CC 77), Release (CC 78)** — `GDVP_PARAM_FILTER_ATTACK_CV` … `_RELEASE_CV`.
These drive an [Envelope](envelope.md) node wired into the filter's port 1.

## Behaviour notes

### Perceptual cutoff curve {#cutoff}
The linear 14-bit cutoff CV is reshaped through an **x³ polynomial** before indexing the
coefficient LUT (`gdvp_cv_to_filter_index`). Without this, a linear knob spends ~95% of its
travel in the muffled low end and ~5% in a bright sliver; the cube law redistributes resolution
so the sweep *sounds* smooth and musical across the whole range.

### Cascaded slope engine {#slope}
The base SVF is one 12 dB/oct section. To reach steeper slopes the filter cascades a second
section: its first integrators (`s1`,`s2`) live inside the 28-byte node, and the **second
section's** state (`s3`,`s4`) spills into a voice-indexed static bank keyed by
`(voice_id, logical filter node)`. This keeps the node byte-exact and the bank sized to the true
voice bound (128 voices × patch nodes) with **zero dynamic allocation**. On a cold-strike voice
allocation the section-2 state is zeroed alongside `s1`/`s2`. Practically: slopes are clean and
per-voice independent; resonance and modulation are preserved across the cascade.

### Zero-Delay Feedback and stability
The trapezoidal integrators use 64-bit intermediate products and Q16.16 state with explicit
saturation limits (`±32767.99`), so the filter stays stable even at extreme resonance and cutoff,
including self-oscillation. There are two unswitched hot paths: static coefficients, and a
per-sample **FM-modulated** coefficient path when cutoff is being modulated at audio rate.

### OSAC — exact coefficients at both rates
When the filter runs oversampled (128-sample blocks), it does **not** approximate by halving the
coefficient. Instead `gdvp_lut_resolve_g_ptr(frames)` selects the mathematically exact
`g = tan(π·fc/fs)` LUT for the active rate (64 or 128). This is the "Oversampling Accuracy
Correction" (OSAC) referenced throughout the codebase. See [Glossary: OSAC](../glossary.md#osac).

### Bifurcated cutoff/resonance
Patch/UI cutoff and resonance write the **base** fields (`base_cutoff_q16`,
`base_resonance_q16`); MIDI/LFO modulation writes separate **bipolar offset** fields
(`mod_cutoff_q16`, `mod_resonance_q16`, centred at `8192`). The DSP merges both at audio rate, so
live modulation never overwrites the knob position. See [Parameters: bifurcation](../parameters.md#bifurcation).

## Related
- Modulate cutoff from an [Envelope](envelope.md) (port 1) or [LFO](lfo.md) for sweeps.
- The `acid_squelch` / `lfo_filter_sweep` examples are filter-forward patches ([library](../patches.md#library)).

---

[← Node Reference](README.md) · [Manual index](../README.md)
