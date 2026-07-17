# Mixer — `GDVP_NODE_MIXER` ✅ (usually auto-injected)

[← Node Reference](README.md) · [Manual index](../README.md)

A multi-input summing bus with per-input and master gain. In normal use you **don't place it
yourself** — the [DAG compiler](../concepts/dag.md#auto-injected-nodes) inserts a mixer automatically
whenever more than one edge fans into the same input port. You can also place one explicitly in a
`.gvp` (the example patches do, e.g. `organic_pad_reverb`). Source: `gdvp_dsp_mixer.c`, payload
`gdvp_node_mixer_t` in `gdvp_nodes.h`.

## Signal & ports

- **Inputs:** up to **6** sources, summed.
- **Output (port 0):** the mix.

## Parameters

| Parameter | Param ID / patch key | Range | Meaning |
|---|---|---|---|
| **Master gain** | `GDVP_PARAM_MIXER_MASTER_GAIN` (CC 87) / patch `master_gain` | 0–16383 | Output level of the mix, EMA-smoothed |
| **Input gain 0–5** | `GDVP_PARAM_MIXER_INPUT_GAIN_0…5` (CC 88–90 + …) / patch `input_*_gain` | 0–16383 | Per-input level |
| **Mute** | `GDVP_PARAM_MIXER_MUTE` | 0/1 | Silence the mix output |
| **Input count** | (node `input_count`) | 1–6 | Active inputs (set by the compiler when auto-injected) |

> Patch files name the per-input gains positionally (`input_a_gain`, `input_b_gain`, …). The
> engine exposes six numbered input-gain parameter IDs for live/MIDI control.

## Behaviour notes

- **Auto-injection.** When you wire three oscillators into one filter input, the compiler places a
  mixer in front of the filter and routes the three sources through it. The patch's
  *post-compilation* edge list (what the [front panel](../control/gui.md) draws) will show the injected
  mixer even though you didn't add it. See [DAG §2.3](../concepts/dag.md#auto-injected-nodes).
- **Integer-only smoothing.** Master gain is Q16.16 EMA-smoothed (`ema_shift`), so level changes
  don't zipper.
- **Bounded.** Six inputs maximum, fixed 28-byte state — consistent with the no-allocation rule.

## Related
- [DAG: auto-injected nodes](../concepts/dag.md#auto-injected-nodes) explains when and why a mixer appears.

---

[← Node Reference](README.md) · [Manual index](../README.md)
