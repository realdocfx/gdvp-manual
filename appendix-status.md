# Appendix A · Engine Status & Known Divergences

[← Manual index](README.md)

This manual documents **as-built behaviour**. Where the running code diverges from its own header
comments, example patches, or obvious intent, it is listed here so you are never surprised. All
claims are against the live dispatch tables and kernels, not prose.

> **How to verify any item:** the ground truth for node activity is `gdvp_dsp_dispatch.c`
> (`gdvp_node_processors[]` / `gdvp_node_updaters[]`). A `NULL` entry = silently skipped = no audio.

---

## A.1 Inactive node types (NULL in dispatch) ⛔

These node types exist in the enum (and most have payload structs and/or DSP source files) but are
`NULL` in the processor table, so the voice executor skips them and they produce no sound:

- `GDVP_NODE_MASTER_BUS` — the dedicated stereo master accumulator node.
- `GDVP_NODE_ROM_READER`, `GDVP_NODE_FEEDBACK`, `GDVP_NODE_MACRO_DELAY`, `GDVP_NODE_FDN` (legacy
  reverb slot).

The **GFX effect family** (`GDVP_NODE_GFX_DELAY`, `_GFX_GAIN`, `_GFX_ENV`, `_GFX_APF`, `_GFX_FDN`,
`_GFX_MOD`) is **active** and fully wired in the dispatch tables. They run on the Global EFX Bus
(master domain, post-mix, monophonic) and produce audio. See [Effects](effects.md) and
[GFX nodes](nodes/gfx.md).

**Impact on patches:** any `.gvp` that includes `master_bus` or one of the legacy inactive nodes
**loads and plays its synthesis graph**, but the listed node is dropped. The `*_reverb`,
`*_phaser`, `*_chorus`, `*_hall`, `*_fuzz`, `*_fold`, `*_compressed`, `*_tremolo`, `*_warm` and
similar effects-suffixed patches now render their GFX tails. See [Patches §7.4](patches.md#library).

---

## A.2 Resolved divergences ✅

- `GDVP_NODE_EXCITER` and `GDVP_NODE_MIXER` are now documented as active in `gdvp_nodes.h` and
  are registered in `gdvp_dsp_dispatch.c`. See [Exciter](nodes/exciter.md) and [Mixer](nodes/mixer.md).
- The GFX effect family (`GDVP_NODE_GFX_*`) is documented as active in `gdvp_nodes.h` and fully
  wired in the dispatch tables. See [Effects](effects.md) and [GFX nodes](nodes/gfx.md).

The header's "NODE TYPE STATUS SUMMARY" comment block is now aligned with the dispatch table.

---

## A.3 LFO transport-sync not yet wired ⚠️

The [LFO](nodes/lfo.md#sync) kernel receives the transport `tick_mask` but casts it to `(void)`
(commented "Phase 2"). Therefore:

- **Key sync (mode 2):** works — phase resets on note.
- **Transport sync (mode 1):** selectable but **does not** lock the LFO to tempo yet.

The [arpeggiator](performance.md#the-arpeggiator) *does* consume the transport clock, so tempo sync
works there. See [Performance §3.8](performance.md#tempo).

---

## A.4 MIDI messages tracked but not acted on ⚠️

Received and stored in the MIDI matrix, but currently no engine action ([MIDI §8.5](midi.md#stubs)):

- CC 64 Sustain pedal, CC 65 Portamento on/off, CC 66 Sostenuto, CC 68 Legato footswitch.
- CC 126 Mono Mode On, CC 127 Poly Mode On (do not reconfigure the VAM — change voice mode via the
  front panel / `gdvp_param_bridge_update_voice_mode` instead).
- CC 91/93 (reverb/chorus depth) route as generic sound-controllers but drive the active GFX
  effects.

---

## A.5 Things that DO work and might surprise you ✅

- **DELAY voice mode** is a real, working strum/echo built from staggered voices — independent of
  the GFX delay line. See [Performance §3.6](performance.md#strum--delay-allocation).
- **Per-voice filter decorrelation / cascade** uses a voice-indexed static bank, so steep slopes
  and section-2 state are correct and per-voice. See [Filter §slope](nodes/filter.md#slope).
- **Exciter per-voice decorrelation** spreads chord voices across the shared noise ring. See
  [Exciter §decorr](nodes/exciter.md#decorr).

---

## A.6 Demo-mode limitation

In **standalone** without a valid licence, audio is interrupted with noise after **60 seconds**
([Hosts §standalone](hosts.md#standalone)). Not a bug — the licence gate.

---

*This appendix reflects the source tree as analysed for manual revision 1. As GFX processors and
the LFO transport path are wired in, the corresponding items here should be retired.*

---

[← Manual index](README.md)
