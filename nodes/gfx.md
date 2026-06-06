# GFX Effect Nodes — `GDVP_NODE_GFX_*` ✅

[← Node Reference](README.md) · [Manual index](../README.md)

The GFX family is GDVP's in-graph effects engine, designed around a "G×T decomposition" (a small set of primitive cells — gain curves, delay lines, all-pass chains, envelope detectors — that recombine into many named effects). The payload structs are fully designed and constrained to a strict 28-byte footprint for optimal performance.

> ## ✅ Current build status: Fully Implemented
>
> **Every GFX node is currently implemented and wired.** Their processor and updater functions are successfully registered in the main dispatch tables.
>
> Example patches referencing these nodes (like `organic_pad_reverb.gvp` using `gfx_fdn`) will now render their spatial acoustics and modulation tails as intended. See [Patches](../patches.md) and [Build Status](../appendix-status.md).

The GFX nodes are **master-domain** effects: they run on the [Global EFX bus](../effects.md) (post-mix, monophonic) rather than per-voice — adding spatial acoustics and global modulation to the summed mix.

---

## GFX Delay — `GDVP_NODE_GFX_DELAY` {#delay}
A tapped delay line used for echo, chorus, flanger, doubler, BBD, and comb filtering.
* **Architecture:** Utilizes up to 3 active taps. Audio samples live in the external effects pool, while the node holds the indexing geometry.
* **Tap Controls:** Each tap features integer delay length, fractional lerp weight, output level, and feedback.
* **Routing & Mix:** Supports standard and all-pass interpolation, mixed via `wet` and `dry` levels.

## GFX Gain — `GDVP_NODE_GFX_GAIN` {#gain}
A nonlinear gain cell utilized for saturation, wavefold, µ-law, [VCA](vca.md), tremolo, AM, ring-mod, and compressor make-up.
* **Curve Selection:** The `lut_id` selects the transfer curve accessed from the shared ROM (0=linear, 1=soft, 2=hard, 3=fold, 4=µ-law, 5=rectify).
* **Dynamics:** A `drive` parameter scales input into the LUT. A dynamic `sidechain` multiplier can be written directly by an [Envelope](envelope.md) or MOD node.
* **Parameters:** Includes static/output gain, compression threshold, knee width, and a 1-pole HP DC blocker state.

## GFX Env detector — `GDVP_NODE_GFX_ENV` {#env}
An envelope follower enabling dynamics processing: compressors, limiters, expanders, duckers, gates, and auto-wah.
* **Detection:** Supports peak, RMS, and external-key modes, tracking via a running state and peak-hold accumulator.
* **Response:** Dictated by attack, release, and hold coefficients. Detection mapping follows a linear, log, or exponential law.
* **Output:** Calculates gain reduction using a threshold, ratio, soft knee, and makeup gain. It explicitly writes its control output to a target node via byte offset.

## GFX All-pass — `GDVP_NODE_GFX_APF` {#apf}
A modular all-pass chain powering phasers, reverb diffusers, and dispersion networks.
* **Stages:** Supports 1 to 8 active TDF-II stages, each with a specific coefficient.
* **State:** Requires no external buffers; the one-multiplier APF state per stage fits entirely inline.
* **Modulation:** A `mod_mask` byte dictates which specific stages are modulated by an [LFO](lfo.md) (bit *i* modulates stage *i*).

## GFX FDN reverb — `GDVP_NODE_GFX_FDN` {#fdn}
A Feedback Delay Network reverb powering plate, room, hall, and gated reverb models.
* **Matrix:** Utilizes a 4-line Hadamard mixing matrix.
* **Delay & Damping:** Prime-ratio delay lines sit in the external pool. Includes per-line 1-pole damping defining the RT60 HF slope, and broadband feedback decay per revolution.
* **Spatialization:** Includes stereo width decorrelation, with pre-delay and stereo-enable mapped inside the flags bitfield.

## GFX Modulator — `GDVP_NODE_GFX_MOD` {#mod}
A parameter modulator implementing "G×T coupling". It routes an internal [LFO](lfo.md), [Envelope](envelope.md), velocity, aftertouch, or mod-wheel to **any field of up to two target nodes** (see [Parameters](../parameters.md)).
* **Source:** Selectable via `src` (LFO, ENV, VEL, AT, WHEEL). The LFO features multiple shapes (sin, tri, sqr, saw, s&h, rand).
* **Routing:** Supports a primary target and an optional secondary target.
* **Controls:** Allows modulation depth, bias offset, rate, tempo sync, and a dedicated slew limiter (portamento) on the control signal itself. The [DAG Compiler](../dag.md) guarantees a MOD node ticks before its target.

---

## What to use today

All `GDVP_NODE_GFX_*` payload structs and DSP execution loops are now actively bridged to the global DSP graph. You can safely assign them inside your `.gvp` patch files (see [Patches](../patches.md)) to utilize spatial acoustics, complex saturation, macro dynamics, and continuous parameter modulation.

See [Effects & the Global EFX Bus](../effects.md) for the bigger picture.

---

[← Node Reference](README.md) · [Manual index](../README.md)