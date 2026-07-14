# VCA — `GDVP_NODE_VCA` ✅

[← Node Reference](README.md) · [Manual index](../README.md)

The voltage-controlled amplifier: the level/gate stage of a voice. Q16.16 gain scaling with EMA
convergence (so gain changes are click-free) and optional tanh saturation for soft drive.
Source: `gdvp_dsp_vca.c`, payload `gdvp_node_vca_t` in `gdvp_nodes.h`.

## Signal & ports

- **Audio in (port 0):** signal to amplify.
- **Control in (port 1):** gain/gate modulation — the amplitude [envelope](envelope.md) wires
  here in every stock voice; this is what makes notes start and stop.
- **Output (port 0):** amplified audio.

## Parameters

| Parameter | Param ID / patch key | Range | Meaning |
|---|---|---|---|
| **Gain** | `GDVP_PARAM_VCA_GAIN_CV` / patch `gain` | 0–16383 | Output gain (14-bit), EMA-smoothed to the target |
| **Saturation enable** | `GDVP_PARAM_VCA_SATURATION` | 0/1 | Enable tanh soft-clip on the output |
| **Mute** | `GDVP_PARAM_VCA_MUTE` | 0/1 | Output silence (executes but emits zero) |

## Behaviour notes

### Smoothed gain
Gain is tracked in Q16.16 and converges toward `target_gain` via an EMA, so automation and
envelope control produce smooth amplitude changes rather than zipper noise. The convergence
behaviour is verified by the engine's VCA convergence tests (`test_gdvp_vca_convergence.c`).

### Saturation
With saturation enabled, the output passes through a LUT-based tanh curve
(`gdvp_lut_apply_tanh_saturation`) for analog-style soft clipping without any runtime math. Use
it to add warmth/limiting at the amp stage; for more aggressive or varied nonlinear shaping the
[GFX Gain](gfx.md#gain) node offers fold/µ-law/rectify curves.

### Mute vs. bypass
`Mute` keeps the node in the execution plan but forces zero output. This differs from the
node-level `BYPASSED` flag (DSP skipped for A/B) — mute is an audible silence you can automate.

## Related
- Driven by the amplitude [Envelope](envelope.md) (port 1) and optionally an [LFO](lfo.md) for tremolo.
- Feeds the [Panner](panner.md) in a stereo voice.

---

[← Node Reference](README.md) · [Manual index](../README.md)
