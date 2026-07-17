# 6 · Parameters, Ranges & Values

[← Effects](effects.md) · [Manual index](../README.md) · Next: [Patch Management →](patches.md)

This chapter is the reference for *values*: the CV conventions, the scaling math, and the
complete table of parameter IDs the engine exposes (`gdvp_param_id_t` in
`gdvp_parameter_bridge.h`). For an alphabetical lookup see the [Parameter Index](../reference/parameter-index.md).

---

## 6.1 The CV convention {#cv}

Almost every continuous parameter is a **14-bit control value**: integer `0–16383`.

- **Unipolar** parameters (cutoff, gain, amplitude, rate, level…): `0` = minimum, `16383` = maximum.
- **Bipolar** parameters (pitch bend, modulation offsets, pan): **`8192` = centre/zero**, below is
  negative, above is positive.

The engine speaks 14 bits because that is high-resolution MIDI's resolution; a 7-bit MIDI CC is
expanded to 14-bit on entry (see [MIDI 14-bit](../control/midi.md#highres)). The UI knobs and the `.gvp`
file use the same 14-bit currency, so a value is portable between knob, file and MIDI.

A few discrete parameters break the mould: enums (waveform `0–5`, filter mode `0–3`, slope
`0–3`), booleans (mute, saturation, pan law), and the **detune** field which is a signed 8-bit
trim (±128 ≈ ±1 semitone). Voice-allocation params (glide, unison, arp…) are **UI-space `0–255`
or small enums**, not 14-bit CV — see [Performance](../concepts/performance.md).

---

## 6.2 Scaling math you can rely on

All integer, all deterministic (CR-001). The conversions that affect what you hear:

- **Pitch:** `128 CV = 1 semitone`, `1536 CV = 1 octave`. A 14-bit pitch CV spans 128 semitones,
  centre `8192`. ([Concepts §1.3](../concepts/concepts.md#pitch-as-control-voltage).)
- **Envelope time CV → rate:** inverted (`0`=fastest, `16383`=slowest) then **x⁶** expansion, with
  a +1 floor so it can't hang. ([Envelope §time](../nodes/envelope.md#time).)
- **Filter cutoff CV → coefficient index:** **x³** perceptual curve so the sweep sounds even.
  ([Filter §cutoff](../nodes/filter.md#cutoff).)
- **LFO rate CV → increment:** logarithmic via LUT. ([LFO](../nodes/lfo.md).)
- **Sustain CV → amplitude:** 14-bit `0–16383` expanded to 16-bit `0–65535` by bit replication
  (no division). ([Envelope](../nodes/envelope.md).)

You don't compute these — you turn a knob and the engine applies the curve — but they explain why
e.g. the bottom of the cutoff range isn't where the audible action is.

---

## 6.3 The bifurcated parameter model {#bifurcation}

This is the single most important idea for controlling GDVP live. Each modulatable parameter has
**two destinations** in the node, written by two different paths:

| Path | Writes | Math | Example |
|---|---|---|---|
| **Host / patch (macro)** | the **base** field | absolute unsigned value | UI cutoff knob → `base_cutoff_q16` |
| **DSP / MIDI / LFO (micro)** | the **modulation** field | bipolar offset **centred at 8192** | CC 74 / LFO → `mod_cutoff_q16` |

The DSP merges base + modulation at audio rate. The consequences:

- **MIDI automation does not fight the knob.** Sending CC 74 adds a *bipolar offset* around the
  knob's base position; `8192` over MIDI means "no change". Pull below `8192` to subtract, push
  above to add.
- **Patches store the base; performance rides the modulation.** Loading a patch sets bases; your
  controller and LFOs ride on top without overwriting them.

The registry that enforces this (`gdvp_param_registry[]`, `gdvp_parameter_registry.h`) holds two
handlers per parameter — one for the host path, one for the DSP path — so the math can never drift
between them.

---

## 6.4 Complete parameter ID table

Every entry in `gdvp_param_id_t`. "Domain" notes whether the value is unipolar 14-bit, bipolar
14-bit (centre 8192), or discrete. CC/NRPN columns show the default MIDI mapping where one exists
([full MIDI map](../control/midi.md#map)).

### Core voice
| Parameter ID | Domain | MIDI | Target |
|---|---|---|---|
| `GDVP_PARAM_PITCH_CV` | pitch 14-bit | (note) | Oscillator pitch — primary |
| `GDVP_PARAM_PITCH_TARGET` | pitch 14-bit | — | Glide target |
| `GDVP_PARAM_OSC_PORTAMENTO` | 0–255 | — | Glide rate |
| `GDVP_PARAM_OSC_FM_DEPTH_CV` | unipolar | NRPN 1/0 | Oscillator FM depth |
| `GDVP_PARAM_OSC_FM_RATIO_CV` | unipolar | NRPN 1/1 | Oscillator FM ratio |
| `GDVP_PARAM_OSC_AMPLITUDE_CV` | unipolar | — | Oscillator amplitude |
| `GDVP_PARAM_OSC_DETUNE_CV` | signed ±128 | — | Oscillator detune (±1 semitone) |
| `GDVP_PARAM_OSC_BASE_PHASE_INC` | — | — | **Deprecated** (use PITCH_CV) |

### Filter
| Parameter ID | Domain | MIDI | Target |
|---|---|---|---|
| `GDVP_PARAM_FILTER_CUTOFF_CV` | unipolar | CC 74 | Cutoff |
| `GDVP_PARAM_FILTER_RESONANCE_CV` | unipolar | CC 71 | Resonance |
| `GDVP_PARAM_FILTER_DRIVE_CV` | unipolar | NRPN 2/0 | Drive |
| `GDVP_PARAM_FILTER_TYPE_CV` | discrete | NRPN 2/1 | Mode LP/BP/HP/Notch |
| `GDVP_PARAM_FILTER_SLOPE` | discrete 0–3 | — | 6/12/18/24 dB/oct |
| `GDVP_PARAM_FILTER_ATTACK_CV` | unipolar | CC 75 | Filter-env attack |
| `GDVP_PARAM_FILTER_DECAY_CV` | unipolar | CC 76 | Filter-env decay |
| `GDVP_PARAM_FILTER_SUSTAIN_CV` | unipolar | CC 77 | Filter-env sustain |
| `GDVP_PARAM_FILTER_RELEASE_CV` | unipolar | CC 78 | Filter-env release |

### Amplitude envelope / VCA
| Parameter ID | Domain | MIDI | Target |
|---|---|---|---|
| `GDVP_PARAM_ENV_ATTACK_RATE` | unipolar | (CC 73) | Envelope attack |
| `GDVP_PARAM_ENV_DECAY_RATE` | unipolar | — | Envelope decay |
| `GDVP_PARAM_ENV_SUSTAIN_LEVEL` | unipolar | — | Envelope sustain |
| `GDVP_PARAM_ENV_RELEASE_RATE` | unipolar | (CC 72) | Envelope release |
| `GDVP_PARAM_VCA_GAIN_CV` | unipolar | — | VCA gain |
| `GDVP_PARAM_VCA_SATURATION` | bool | — | VCA tanh enable |
| `GDVP_PARAM_VCA_MUTE` | bool | — | VCA mute |

### Per-oscillator extended (MIS canonical map)
| Parameter ID | Domain | MIDI | Target |
|---|---|---|---|
| `GDVP_PARAM_OSC1_PITCH_BEND_CV` | bipolar | CC 16 | Osc1 bend offset |
| `GDVP_PARAM_OSC1_PWM_CV` | unipolar | CC 17 | Osc1 pulse width |
| `GDVP_PARAM_OSC1_SHAPE_CV` | unipolar | CC 18 | Osc1 waveform morph |
| `GDVP_PARAM_OSC2_PITCH_BEND_CV` | bipolar | CC 20 | Osc2 bend offset |
| `GDVP_PARAM_OSC2_PWM_CV` | unipolar | CC 21 | Osc2 pulse width |
| `GDVP_PARAM_OSC2_SHAPE_CV` | unipolar | CC 22 | Osc2 waveform morph |
| `GDVP_PARAM_OSC2_DETUNE_CV` | bipolar | CC 23 | Osc2 detune |
| `GDVP_PARAM_OSC_MIX_CV` | unipolar | CC 24 | Osc1/Osc2 crossfade |

### Channel / global modulation
| Parameter ID | Domain | MIDI | Target |
|---|---|---|---|
| `GDVP_PARAM_MOD_WHEEL_CV` | unipolar | CC 1 | Mod wheel |
| `GDVP_PARAM_VOLUME_CV` | unipolar | CC 7 | Channel volume |
| `GDVP_PARAM_PAN_CV` | bipolar | CC 10 | Pan |

### MPE / expression {#mpe}
| Parameter ID | Domain | MIDI | Target |
|---|---|---|---|
| `GDVP_PARAM_PITCH_BEND_CV` | bipolar | (pitch-bend) | MPE pitch bend |
| `GDVP_PARAM_CHANNEL_PRESSURE_CV` | unipolar | (channel AT) | MPE channel pressure |
| `GDVP_PARAM_POLY_PRESSURE_CV` | unipolar | (poly AT) | MPE poly pressure |

### Mixer
| Parameter ID | Domain | MIDI | Target |
|---|---|---|---|
| `GDVP_PARAM_MIXER_MASTER_GAIN` | unipolar | CC 87 | Mixer master |
| `GDVP_PARAM_MIXER_INPUT_GAIN_0…5` | unipolar | CC 88–90 + | Mixer inputs |
| `GDVP_PARAM_MIXER_MUTE` | bool | — | Mixer mute |
| `GDVP_PARAM_PAN_LAW` | bool | — | Panner law |

### Exciter
| Parameter ID | Domain | Target |
|---|---|---|
| `GDVP_PARAM_EXCITER_SOURCE_MODE` | discrete 0–4 | Source family |
| `GDVP_PARAM_EXCITER_COLOR` | discrete 0–4 | Noise color |
| `GDVP_PARAM_EXCITER_FLAGS` | bitmask | Bipolar/Tempo/Gaussian/Crush |
| `GDVP_PARAM_EXCITER_CRUSH_BITS` | small int | Bit-crush depth |
| `GDVP_PARAM_EXCITER_RATE` | unipolar | S&H rate / density |
| `GDVP_PARAM_EXCITER_LEVEL` | unipolar | Output level |
| `GDVP_PARAM_EXCITER_PARAM_A` | unipolar | slew/steps/dust amp |
| `GDVP_PARAM_EXCITER_DECORR_OFFSET` | unipolar | Per-voice decorrelation |

> **MIDI columns in parentheses** (e.g. CC 72/73, channel/poly aftertouch) indicate controllers the
> canonical map or MIDI processor *names* but which are routed via generic sound-controller
> handling rather than an explicit per-parameter binding in `gdvp_canonical_map.json`. The
> explicit, guaranteed bindings are CC 1, 7, 10, 16–24, 71, 74–78, and NRPN 1/0, 1/1, 2/0, 2/1.
> See [MIDI](../control/midi.md#map).

---

## 6.5 Discrete value cheat-sheet

| Field | Values |
|---|---|
| Oscillator waveform | 0 Sine · 1 Square · 2 Triangle · 3 Saw · 4 Pulse · 5 Noise |
| Filter mode | 0 LP · 1 BP · 2 HP · 3 Notch |
| Filter slope | 0 = 6 · 1 = 12 · 2 = 18 · 3 = 24 dB/oct |
| Envelope curve (each stage) | 0 Linear · 1 Log · 2 Exp · 3 Sigmoid |
| LFO shape | 0 Sine · 1 Square · 2 Triangle · 3 Saw · 4 S&H · 5 Noise |
| LFO sync | 0 Free · 1 Transport (⚠️ inactive) · 2 Key |
| Panner law | 0 Linear · 1 Constant-power |
| Exciter source | 0 Audio · 1 Particle · 2 S&H step · 3 S&H quant · 4 S&H smooth |
| Exciter color | 0 White · 1 Pink · 2 Red · 3 Blue · 4 Violet |
| Voice mode | 0 Mono · 1 Legato · 2 Poly · 3 Unison · 4 Duo · 5 Chord · 6 Delay · 7 Arp |

---

[← Effects](effects.md) · [Manual index](../README.md) · Next: [Patch Management →](patches.md)
