# Oversamplers — `GDVP_NODE_UPSAMPLER` / `GDVP_NODE_DOWNSAMPLER` ✅ (auto-injected)

[← Node Reference](README.md) · [Manual index](../README.md)

A matched pair of polyphase half-band FIR converters that move signal between the base rate and
2× oversampled rate without aliasing. **You never place these manually** — the
[DAG compiler](../concepts/dag.md#auto-injected-nodes) inserts them automatically around any node that runs
oversampled, so the rate boundary is band-limited rather than naive. Source:
`gdvp_dsp_oversampling.c`, payloads `gdvp_node_upsampler_t` / `gdvp_node_downsampler_t`.

## What they do

- **Upsampler (1×→2×):** interpolates a band-limited sample between each input sample, doubling the
  rate ahead of an oversampled node. Carries a 5-sample tail across blocks.
- **Downsampler (2×→1×):** low-pass filters and decimates the 2× signal back to base rate after the
  oversampled node. Carries a 10-sample tail.

Both use the same **11-tap symmetric half-band FIR** with its corner at fs/4 (Nyquist/2 of the
base rate), stored as three Q15 coefficients (the other taps are zero or the unity centre tap).
Filter gain bookkeeping is handled by the shift amounts (`>>14` up, `>>15` down) so levels are
preserved across the conversion.

## Parameters

None that you set. These nodes have **no operator parameters** and no parameter-updater entry —
they are pure structural plumbing inserted by the compiler. Their only state is the FIR tail and
an ownership link back to the node they wrap (`parent_node_id`), used so re-compilation stays
idempotent.

## Why a node would be oversampled

Oversampling is requested via the node header flag `GDVP_NODE_FLAG_OVERSAMPLED` (which makes that
node process 128-sample blocks instead of 64). It's used where a nonlinearity would otherwise
alias — bright/aggressive [filter](filter.md) settings, saturating [VCA](vca.md) drive, FM. When a
node is flagged oversampled but its neighbours are not, the compiler brackets it with an
upsampler/downsampler pair so the rate change itself doesn't introduce aliasing.

This is also where the [filter's OSAC](filter.md) correction matters: an oversampled filter uses a
different, exact coefficient LUT for the 128-sample rate rather than approximating.

## Related
- [DAG: auto-injected nodes](../concepts/dag.md#auto-injected-nodes) · [Glossary: OSAC](../reference/glossary.md#osac)

---

[← Node Reference](README.md) · [Manual index](../README.md)
