# GFX Effect Nodes — `GDVP_NODE_GFX_*` ⛔

[← Node Reference](README.md) · [Manual index](../README.md)

The GFX family is GDVP's in-graph effects engine, designed around a "G×T decomposition" (a small
set of primitive cells — gain curves, delay lines, all-pass chains, envelope detectors — that
recombine into many named effects). The payload structs are fully designed and the DSP source
files exist (`gdvp_dsp_gfx_*.c`).

> ## ⛔ Current build status: not wired
>
> **Every GFX node is `NULL` in the live dispatch table** (`gdvp_dsp_dispatch.c`). The voice
> executor's non-NULL guard therefore **silently skips** any GFX node. On the current build these
> nodes produce **no audio**, even though:
> - the DSP source files are present, and
> - several example patches reference them (e.g. `organic_pad_reverb.gvp` declares a `gfx_fdn`;
>   `*_phaser.gvp`, `*_chorus.gvp`, `*_fuzz.gvp`, `*_hall.gvp` reference GFX cells).
>
> Those patches **load and play their synthesis graph** (osc → filter → vca → panner); the GFX
> node in them is skipped. The reverb tail / chorus / phaser you might expect from the patch name
> is not rendered on this build. See [Effects](../effects.md) and [Appendix A](../appendix-status.md).
>
> The rest of this page documents the **intended** design (from the payload structs) so you can
> recognise these nodes in patches and understand what they will do once activated. Treat all
> parameter detail here as design intent, not current behaviour.

The GFX nodes are **master-domain** effects: they're meant to run on the [Global EFX bus](../effects.md)
(post-mix, monophonic) rather than per-voice — spatial acoustics on the sum, not the source.

---

## GFX Delay — `GDVP_NODE_GFX_DELAY` {#delay}
Tapped delay line: echo, chorus, flanger, doubler, BBD, comb. Up to 3 taps, each with integer +
fractional (Q0.8) delay, output gain (Q0.7) and feedback (Q0.7); wet/dry mix; optional
interpolation. Audio lives in a shared effects pool; the node holds indices and tap geometry.
Payload: `gdvp_node_gfx_delay_t`.

## GFX Gain — `GDVP_NODE_GFX_GAIN` {#gain}
Nonlinear gain cell: saturation, wavefold, µ-law, VCA, tremolo, AM, ring-mod, compressor make-up.
A `lut_id` selects the transfer curve (`0`=linear, `1`=soft, `2`=hard, `3`=fold, `4`=µ-law,
`5`=rectify); `drive` scales into the curve; a live `sidechain` field can be written by an ENV/MOD
node for dynamics. Optional DC blocker. Payload: `gdvp_node_gfx_gain_t`.

## GFX Env detector — `GDVP_NODE_GFX_ENV` {#env}
Envelope follower for dynamics: compressor, limiter, expander, ducker, gate, auto-wah driver.
Peak / RMS / external-key detection, attack/release/hold coefficients, threshold, ratio, knee,
makeup. Writes its control output into a target node's sidechain field by byte offset. Payload:
`gdvp_node_gfx_env_t`.

## GFX All-pass — `GDVP_NODE_GFX_APF` {#apf}
All-pass chain (1–8 stages): phaser, reverb diffuser, dispersion. Per-stage Q0.7 coefficient; a
`mod_mask` marks which stages are LFO-modulated; wet/dry mix. State fits inline (no external
buffer). Payload: `gdvp_node_gfx_apf_t`.

## GFX FDN reverb — `GDVP_NODE_GFX_FDN` {#fdn}
Feedback Delay Network reverb: plate, room, hall, gated. 4 delay lines with a Hadamard mixing
matrix, per-line 1-pole damping (HF decay slope), broadband decay, stereo width/decorrelation,
optional pre-delay. Audio + filter state live in the effects pool. Payload: `gdvp_node_gfx_fdn_t`.
This is the node `organic_pad_reverb.gvp` declares as `gfx_fdn` with `size`/`damping`/`decay`/
`wet`/`dry` — currently skipped.

## GFX Modulator — `GDVP_NODE_GFX_MOD` {#mod}
Parameter modulator implementing the "G×T coupling": routes an internal LFO / envelope / velocity
/ aftertouch / mod-wheel source to **any field of any node** by byte offset (with a second target
too). Depth, offset, rate, shape (sin/tri/sqr/saw/s&h/rand), tempo division, and a slew limiter on
the control signal. The DAG topo-sort guarantees a MOD node ticks *before* its target. Payload:
`gdvp_node_gfx_mod_t`.

---

## What to use today

Until the GFX table is populated, the available shaping is:
- **Saturation** at the [VCA](vca.md) (tanh soft-clip) and in the [Filter](filter.md) drive stage.
- **Modulation** via the [LFO](lfo.md) node wired to a target (filter sweep, vibrato, tremolo, PWM).
- **Noise/texture** via the [Exciter](exciter.md).
- **Strum/echo** as a *voice-allocation* effect via [DELAY mode](../performance.md#strum--delay-allocation),
  which is distinct from the GFX delay line and **does** work.

See [Effects & the Global EFX Bus](../effects.md) for the bigger picture.

---

[← Node Reference](README.md) · [Manual index](../README.md)
