# 8 · MIDI Implementation

[← Patch Management](patches.md) · [Manual index](README.md) · Next: [The Front Panel →](gui.md)

GDVP is a "Universal Host" MIDI device: 16-channel multitimbral, 14-bit-capable, with NRPN
support and a defined CC map (Canonical MIDI Implementation Schema, **MIS v0.9.1**). This chapter
documents the control surface and — importantly — which messages are fully wired vs. tracked but
stubbed. Sources: `gdvp_midi_processor.c/.h`, `gdvp/config/gdvp_canonical_map.json`.

---

## 8.1 Channels map to Parts {#channels}

**MIDI channel N → Part (N−1).** Channel 1 = Part 0, … channel 16 = Part 15. Each Part is an
independent instrument with its own patch and voice mode ([Concepts §1.1](concepts.md)). There are
16 of each, so the mapping is exact and fixed. The MIDI state matrix tracks all 128 CCs across all
16 channels independently (`gdvp_midi_state_matrix_t`).

> **Manufacturer / model IDs:** GDVP = 125, model "Producer Engine" = 1 (from the canonical map).

---

## 8.2 Notes, velocity, panic

- **Note-on / note-off** drive the Part's [voice mode](performance.md#voice-modes) via the VAM. The
  host-side entry points are `gdvp_system_host_note_on/off(system, part_id, note, velocity)`.
- **Velocity** (0–127) is carried into the voice and scales the [envelope](nodes/envelope.md#velocity).
- **All Notes Off (CC 123)** → graceful envelope release of the channel's voices
  (`gdvp_client_all_notes_off`).
- **All Sound Off (CC 120)** → hard panic, bypassing envelopes (`gdvp_client_panic`).
- **Reset All Controllers (CC 121)** → re-initialises the MIDI state matrix to GM defaults.

---

## 8.3 High-resolution 14-bit CC pairing {#highres}

GDVP natively wants **14-bit** control values ([Parameters §6.1](parameters.md#cv)). The processor
handles standard MIDI 14-bit CC pairing automatically:

- A **CC 0–31** message is the **MSB**: it is latched *and* routed immediately (with zero LSB) so
  coarse moves respond instantly.
- The matching **CC 32–63** message is the **LSB**: it is combined with the latched MSB
  (`MSB<<7 | LSB`) for a full 14-bit update.
- A standalone 7-bit CC is expanded `value << 7` to 14-bit.

So you get smooth high-resolution control if your controller sends MSB/LSB pairs, and sane
behaviour if it sends 7-bit only.

---

## 8.4 The control map {#map}

These are the **explicit, guaranteed** bindings from `gdvp_canonical_map.json`.

### Control Change (CC)
| CC | Name | Parameter |
|---|---|---|
| 1 | Mod Wheel | `GDVP_PARAM_MOD_WHEEL_CV` |
| 7 | Volume | `GDVP_PARAM_VOLUME_CV` |
| 10 | Pan | `GDVP_PARAM_PAN_CV` |
| 16 | Osc1 Pitch Bend | `GDVP_PARAM_OSC1_PITCH_BEND_CV` |
| 17 | Osc1 Pulse Width | `GDVP_PARAM_OSC1_PWM_CV` |
| 18 | Osc1 Shape | `GDVP_PARAM_OSC1_SHAPE_CV` |
| 20 | Osc2 Pitch Bend | `GDVP_PARAM_OSC2_PITCH_BEND_CV` |
| 21 | Osc2 Pulse Width | `GDVP_PARAM_OSC2_PWM_CV` |
| 22 | Osc2 Shape | `GDVP_PARAM_OSC2_SHAPE_CV` |
| 23 | Osc2 Detune | `GDVP_PARAM_OSC2_DETUNE_CV` |
| 24 | Osc Mix | `GDVP_PARAM_OSC_MIX_CV` |
| 71 | Filter Resonance (Timbre) | `GDVP_PARAM_FILTER_RESONANCE_CV` |
| 74 | Filter Cutoff (Brightness) | `GDVP_PARAM_FILTER_CUTOFF_CV` |
| 75 | Filter Env Attack | `GDVP_PARAM_FILTER_ATTACK_CV` |
| 76 | Filter Env Decay | `GDVP_PARAM_FILTER_DECAY_CV` |
| 77 | Filter Env Sustain | `GDVP_PARAM_FILTER_SUSTAIN_CV` |
| 78 | Filter Env Release | `GDVP_PARAM_FILTER_RELEASE_CV` |

### NRPN
| NRPN (MSB/LSB) | Name | Parameter |
|---|---|---|
| 1 / 0 | Oscillator FM Depth | `GDVP_PARAM_OSC_FM_DEPTH_CV` |
| 1 / 1 | Oscillator FM Ratio | `GDVP_PARAM_OSC_FM_RATIO_CV` |
| 2 / 0 | Filter Drive | `GDVP_PARAM_FILTER_DRIVE_CV` |
| 2 / 1 | Filter Type | `GDVP_PARAM_FILTER_TYPE_CV` |

NRPN selection uses the standard CC 99/98 (MSB/LSB) sequence; data entry follows.

### Mixer (front-panel CCs)
The mixer master/input gains are exposed on CC 87–90+ (`GDVP_PARAM_MIXER_MASTER_GAIN`,
`GDVP_PARAM_MIXER_INPUT_GAIN_0…5`) for hands-on mixing from a controller.

---

## 8.5 What is tracked but NOT yet acted on {#stubs}

Several standard messages are **received and stored** in the MIDI matrix but currently perform **no
engine action** — the handler returns success without doing anything. Don't rely on these yet:

| Message | Status |
|---|---|
| CC 64 Damper / Sustain pedal | ⚠️ tracked, no sustain action (facade hook not wired) |
| CC 65 Portamento on/off | ⚠️ tracked, no action |
| CC 66 Sostenuto | ⚠️ tracked, no action |
| CC 68 Legato footswitch | ⚠️ tracked, no action |
| CC 126 Mono Mode On | ⚠️ acknowledged, does not reconfigure the VAM |
| CC 127 Poly Mode On | ⚠️ acknowledged, does not reconfigure the VAM |
| CC 91 Reverb depth, CC 93 Chorus depth | routed as generic sound-controllers, but the [GFX effects](effects.md) they would drive are inactive |

To change voice mode today, use the [front-panel control](performance.md#voice-modes) /
`gdvp_param_bridge_update_voice_mode`, not CC 126/127. See [Appendix A](appendix-status.md).

---

## 8.6 Pitch bend & aftertouch {#pitchbend}

The parameter space defines MPE-style targets — `GDVP_PARAM_PITCH_BEND_CV`,
`GDVP_PARAM_CHANNEL_PRESSURE_CV`, `GDVP_PARAM_POLY_PRESSURE_CV` ([Parameters §6.4](parameters.md#mpe)).
Pitch bend is applied per-Part in the voice executor with a default ±2 semitone range (0–48
configurable), added to all sounding voices ([Performance §3.7](performance.md#pitch-bend)). The CC
matrix reserves tracking slots for pitch-bend and aftertouch alongside the 128 CCs (130 tracking
targets per Part).

---

## 8.7 Smart CC immunity {#immunity}

To protect the real-time audio thread, host CCs pass through a decimation layer
(`gdvp_host_push_smart_cc`) before reaching the engine:

- **Noise floor:** changes smaller than `GDVP_CC_NOISE_FLOOR` (8, in 14-bit CV) are ignored —
  controller jitter doesn't flood the queue.
- **Max latency:** a value is force-pushed at least every `GDVP_CC_MAX_LATENCY_MS` (50 ms) even if
  below the noise floor, so slow sweeps still track.
- **Load-aware routing:** routing adapts to SPSC queue capacity under heavy traffic.

This is why ultra-fine CC dithering may not register, but musical moves always do — and why a busy
MIDI stream can't glitch the audio. See [Concepts §1.4](concepts.md#the-three-thread-model-and-why-it-shapes-the-feel).

---

[← Patch Management](patches.md) · [Manual index](README.md) · Next: [The Front Panel →](gui.md)
