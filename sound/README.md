# Part II — Building Sound

The blocks you patch together, the effects bus, the parameter model, and the file format.

- **[Node Reference](../nodes/README.md)** — every node type, its parameters, ranges and live status
  - [Oscillator](../nodes/oscillator.md) — multi-waveform, LDF-BLEP anti-aliasing, linear FM
  - [Filter (TPT-SVF)](../nodes/filter.md) — zero-delay-feedback state-variable; LP/BP/HP/Notch
  - [Envelope (ADSR)](../nodes/envelope.md) — 5-stage, 4 curve shapes, click-free release
  - [LFO](../nodes/lfo.md) — sub-audio modulator; tempo-syncable
  - [VCA](../nodes/vca.md) — Q16.16 gain, EMA convergence, optional tanh saturation
  - [Panner](../nodes/panner.md) — constant-power stereo, EMA smoothing
  - [Mixer](../nodes/mixer.md) — multi-input summing bus, per-input gain/mute
  - [Exciter](../nodes/exciter.md) — entropy tap: colored noise, particle dust, S&H
  - [Oversamplers](../nodes/oversampling.md) — polyphase 1x<->2x half-band FIR
  - [GFX effect nodes](../nodes/gfx.md) — the six master-domain effects (delay/gain/env/APF/FDN/mod)
  - [Master Bus](../nodes/master-bus.md) — final stereo accumulator — inactive placeholder
  - [ROM Reader](../nodes/rom-reader.md) — flash wavetable reader — inactive placeholder
  - [Feedback](../nodes/feedback.md) — explicit z-1 delay line — inactive placeholder
  - [Macro Delay](../nodes/macro-delay.md) — block-length delay — inactive placeholder
  - [FDN (legacy)](../nodes/fdn-legacy.md) — per-voice FDN slot — superseded by GFX_FDN
- **[Effects & the Global EFX Bus](effects.md)** — master-domain processing and the GFX family (delay, gain, env, APF, FDN, mod)
- **[Parameters, Ranges & Values](parameters.md)** — the 14-bit CV convention, the base-vs-modulation model, the ID index
- **[Patch Management (.gvp)](patches.md)** — the JSON patch format, routing semantics, the factory example library

[← Manual home](../README.md)
