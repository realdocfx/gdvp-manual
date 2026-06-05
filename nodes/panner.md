# Panner — `GDVP_NODE_PANNER` ✅

[← Node Reference](README.md) · [Manual index](../README.md)

Constant-power stereo placement with EMA-smoothed, artifact-free sweeps. Source:
`gdvp_dsp_panner.c`, payload `gdvp_node_panner_t` in `gdvp_nodes.h`.

## Signal & ports

- **Audio in (port 0):** mono signal to place.
- **Output:** stereo (the panner writes the left/right pair into contiguous bus routing).

## Parameters

| Parameter | Param ID / patch key | Range | Meaning |
|---|---|---|---|
| **Pan position** | `GDVP_PARAM_PAN_CV` (CC 10) / patch `pan` | 0–16383 | `0` = hard left, `8192` = centre, `16383` = hard right |
| **Pan law** | `GDVP_PARAM_PAN_LAW` / patch `pan_law` | 0/1 | `0` = Linear, `1` = Constant-power (−3 dB centre) |

## Behaviour notes

### Constant-power vs linear
With **constant-power** law the perceived loudness stays even as you sweep across the field
(the −3 dB centre pan law), using a branchless sine/cosine extraction via a phase offset — no
runtime trig. **Linear** law is a straight amplitude crossfade (centre is louder), occasionally
useful for hard-panned mono sources.

### Smoothed sweeps
Pan position is smoothed in Q16.16 (`smoothed_pan`) toward the 14-bit target with an
`ema_shift`-controlled rate, so automated pan moves and LFO-driven auto-pan are free of zipper
artifacts.

## Related
- Usually the last node in a voice, fed by the [VCA](vca.md).
- The summed stereo result is what the [Global EFX bus](../effects.md) and master output receive.

---

[← Node Reference](README.md) · [Manual index](../README.md)
