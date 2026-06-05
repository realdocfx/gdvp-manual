# Oscillator — `GDVP_NODE_OSCILLATOR` ✅

[← Node Reference](README.md) · [Manual index](../README.md)

The tone generator. A LUT-based oscillator with a 32-bit phase accumulator (for >90 dB SNR),
six waveforms, linear FM, pulse-width control, per-read detune, and intrinsic pitch glide.
Source: `gdvp_dsp_oscillator.c`, payload `gdvp_node_osc_t` in `gdvp_nodes.h`.

## Signal & ports

- **Output (port 0):** audio (`int16_t`).
- **Mod input:** a `mod_buffer` carries audio-rate linear FM when another node is wired into the
  oscillator's modulation input. FM depth is set by `fm_depth_cv`.
- Pitch is **not** a wire — it comes from the played note (via the voice) plus the parameters
  below.

## Parameters

| Parameter | Param ID / patch key | Range | Meaning |
|---|---|---|---|
| **Waveform** | patch `waveform` | 0–5 | `0`=Sine, `1`=Square, `2`=Triangle, `3`=Sawtooth, `4`=Pulse, `5`=Noise |
| **Pitch (note CV)** | `GDVP_PARAM_PITCH_CV` / patch `pitch` | 0–16383 | Target pitch as 14-bit CV; **128 CV = 1 semitone**, `8192` = centre |
| **Pitch target** | `GDVP_PARAM_PITCH_TARGET` | 0–16383 | Glide target for the slew limiter (see [pitch](#pitch)) |
| **Portamento / glide** | `GDVP_PARAM_OSC_PORTAMENTO` | 0–255 | `0` = instant snap, higher = slower exponential glide |
| **FM depth** | `GDVP_PARAM_OSC_FM_DEPTH_CV` (NRPN 1/0) | 0–16383 | Linear FM index from the mod input |
| **FM ratio** | `GDVP_PARAM_OSC_FM_RATIO_CV` (NRPN 1/1) | 0–16383 | Carrier:modulator ratio |
| **Pulse width** | patch `pulse_width` / `GDVP_PARAM_OSC1_PWM_CV` | 0–16383 | `8192` ≈ 50% square; for Pulse/Square shaping |
| **Amplitude** | `GDVP_PARAM_OSC_AMPLITUDE_CV` / patch `amplitude` | 0–16383 | Oscillator output level |
| **Detune** | `GDVP_PARAM_OSC_DETUNE_CV` / patch `detune` | −128…+127 (stored signed) | Read-time detune, **±1 semitone, ~1 cent/step** — see [detune](#detune) |
| **Hard reset** | `GDVP_CMD_HARD_RESET` (command) | — | Snaps phase + pitch instantly (cold strike) |

> Patch files store `pitch`, `detune`, `amplitude`, etc. as the field values shown in the
> example library. `detune` appears as a large unsigned number in some patches (e.g. `8128`)
> because of how the UI offset is encoded; treat the audible result as a small ±cents trim.

## Behaviour notes

### Pitch slewing — glide that is musically correct {#pitch}
The oscillator keeps a high-precision `smoothed_pitch_cv` (Q16.16) that chases the
`target_pitch_cv` via an EMA whose rate is `portamento_shift`. Because the engine slews the
*linear* pitch CV and pitch→frequency is exponential, the resulting frequency contour is an
exponential glide with (approximately) constant glide time regardless of interval — the correct
behaviour for portamento. With `portamento_shift = 0`, or on a HARD_RESET, the pitch snaps
instantly. This is the mechanism behind MONO/LEGATO [glide](../performance.md#glide).

### Detune vs. pitch — calibration separated from intent {#detune}
GDVP deliberately separates *musical intent* (the note → `target_pitch_cv`) from *hardware
calibration* (the detune knob → `detune_bias`). Detune is applied **additively after** the
portamento EMA, every read, with hard saturation to protect the LUT. Range is ±128 CV steps =
±1 semitone at roughly 1 cent per step. This means detuning never disturbs the glide target and
two oscillators can be fanned a few cents apart for analog thickness without affecting tracking.

### Noise waveform
Waveform `5` uses a dedicated per-oscillator PRNG (`prng_state`) with a sample-and-hold latch
(`noise_latch`) for phase-synced noise. For richer noise/particle sources (colored noise,
Poisson dust, sample-and-hold voltages) use the dedicated [Exciter](exciter.md) node.

### Anti-aliasing
The implemented waveforms use LDF-BLEP-style band-limiting on the discontinuous shapes
(square/saw/pulse) so high notes don't alias harshly. For very bright patches the oscillator may
run oversampled, in which case the compiler inserts [up/down-samplers](oversampling.md) around it.

## Related
- [Performance: glide](../performance.md#glide) · [Parameters: pitch CV](../parameters.md#pitch)
- Modulate pitch/PWM from an [LFO](lfo.md) (vibrato/PWM) or [Envelope](envelope.md).

---

[← Node Reference](README.md) · [Manual index](../README.md)
