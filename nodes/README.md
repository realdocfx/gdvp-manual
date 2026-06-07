# 4 · Node Reference

[← Performance & Expression](../performance.md) · [Manual index](../README.md) · Next: [Effects →](../effects.md)

Every sound in GDVP is built from **nodes** wired into a [graph](../dag.md). This section
documents each node type: what it does, every parameter, its range, and — critically — whether
it is **live in the current build**.

## Status at a glance

The engine dispatches node processing through a table (`gdvp_node_processors[]` in
`gdvp_dsp_dispatch.c`). A node type with a `NULL` entry is **silently skipped** by the voice
executor — it can appear in a patch and in the editor, but it produces no audio. This table is
the single source of truth below; it does **not** always match the optimistic status comments
in `gdvp_nodes.h`.

| Node | Enum | Status | Page |
|---|---|---|---|
| Oscillator | `GDVP_NODE_OSCILLATOR` | ✅ Active | [oscillator.md](oscillator.md) |
| Filter | `GDVP_NODE_FILTER` | ✅ Active | [filter.md](filter.md) |
| Envelope | `GDVP_NODE_ENVELOPE` | ✅ Active | [envelope.md](envelope.md) |
| LFO | `GDVP_NODE_LFO` | ✅ Active | [lfo.md](lfo.md) |
| VCA | `GDVP_NODE_VCA` | ✅ Active | [vca.md](vca.md) |
| Panner | `GDVP_NODE_PANNER` | ✅ Active | [panner.md](panner.md) |
| Mixer | `GDVP_NODE_MIXER` | ✅ Active (usually auto-injected) | [mixer.md](mixer.md) |
| Exciter (entropy tap) | `GDVP_NODE_EXCITER` | ✅ Active | [exciter.md](exciter.md) |
| Upsampler | `GDVP_NODE_UPSAMPLER` | ✅ Active (auto-injected) | [oversampling.md](oversampling.md) |
| Downsampler | `GDVP_NODE_DOWNSAMPLER` | ✅ Active (auto-injected) | [oversampling.md](oversampling.md) |
| GFX Delay | `GDVP_NODE_GFX_DELAY` | ✅ Active (master-domain) | [gfx.md#delay](gfx.md#delay) |
| GFX Gain | `GDVP_NODE_GFX_GAIN` | ✅ Active (master-domain) | [gfx.md#gain](gfx.md#gain) |
| GFX Env detector | `GDVP_NODE_GFX_ENV` | ✅ Active (master-domain) | [gfx.md#env](gfx.md#env) |
| GFX All-pass | `GDVP_NODE_GFX_APF` | ✅ Active (master-domain) | [gfx.md#apf](gfx.md#apf) |
| GFX FDN reverb | `GDVP_NODE_GFX_FDN` | ✅ Active (master-domain) | [gfx.md#fdn](gfx.md#fdn) |
| GFX Modulator | `GDVP_NODE_GFX_MOD` | ✅ Active (master-domain) | [gfx.md#mod](gfx.md#mod) |
| Master Bus | `GDVP_NODE_MASTER_BUS` | ⛔ Inactive (NULL) | — |
| ROM Reader | `GDVP_NODE_ROM_READER` | ⛔ Inactive (NULL) | — |
| Feedback | `GDVP_NODE_FEEDBACK` | ⛔ Inactive (NULL) | — |
| Macro Delay | `GDVP_NODE_MACRO_DELAY` | ⛔ Inactive (NULL) | — |
| FDN (legacy slot) | `GDVP_NODE_FDN` | ⛔ Inactive (NULL) | — |

> **Reading the GFX rows.** The GFX-family DSP source files exist (`gdvp_dsp_gfx_*.c`) and
> all GFX nodes are now fully implemented with registered processors and updaters in the
> dispatch tables. They run on the Global EFX bus (master-domain, post-mix, monophonic) for
> spatial acoustics and global modulation. See [Effects](../effects.md) for details.

## How to read a node page

Each page follows the same layout:

1. **What it is** — one paragraph, the role in a patch.
2. **Signal & ports** — what feeds in (port 0 audio / port 1 control) and what comes out.
3. **Parameters** — a table of every operator-facing parameter with type, range and meaning.
4. **Behaviour notes** — the DSP details that change how it sounds.
5. **Source** — the files to check the claims against.

Parameter ranges use the [conventions in §6](../parameters.md): 14-bit CV `0–16383` unless
noted, `8192` = bipolar centre.

## The active signal-path nodes

These are the nodes you actually build voices from today:

- **[Oscillator](oscillator.md)** — the tone generator. Six waveforms, linear FM, PWM, per-read detune, intrinsic glide.
- **[Filter](filter.md)** — TPT state-variable filter, LP/BP/HP/Notch, cascaded 6–24 dB/oct, optional FM.
- **[Envelope](envelope.md)** — five-stage ADSR, four curve shapes per stage, velocity, legato, click-free release.
- **[LFO](lfo.md)** — multi-timescale modulator (meso/micro/macro) with chaos drift and key-sync.
- **[VCA](vca.md)** — the amplifier/gate, with optional saturation.
- **[Mixer](mixer.md)** — multi-input summing bus (up to 6 inputs); usually inserted for you.
- **[Panner](panner.md)** — constant-power stereo placement.
- **[Exciter](exciter.md)** — entropy tap: colored noise / particle dust / sample-and-hold sources.
- **[Oversamplers](oversampling.md)** — band-limited 2× up/down conversion at oversampled-node boundaries.
- **[GFX Effects](gfx.md)** — master-domain effects: delay, gain, envelope detector, all-pass, FDN reverb, modulator.

---

[← Performance & Expression](../performance.md) · [Manual index](../README.md) · Next: [Effects →](../effects.md)
