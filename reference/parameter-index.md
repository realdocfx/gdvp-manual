# Parameter Index

[← Manual index](../README.md) · Full table with domains: [Parameters §6.4](../sound/parameters.md#complete-parameter-id-table)

Alphabetical lookup of every `gdvp_param_id_t`. "→" gives the node/feature page.

| Parameter ID | MIDI | Page |
|---|---|---|
| `GDVP_PARAM_CHANNEL_PRESSURE_CV` | channel AT | [Performance: MPE](../concepts/performance.md#mpe-per-note-expression) |
| `GDVP_PARAM_ENV_ATTACK_RATE` | (CC 73) | [Envelope](../nodes/envelope.md) |
| `GDVP_PARAM_ENV_DECAY_RATE` | — | [Envelope](../nodes/envelope.md) |
| `GDVP_PARAM_ENV_RELEASE_RATE` | (CC 72) | [Envelope](../nodes/envelope.md) |
| `GDVP_PARAM_ENV_SUSTAIN_LEVEL` | — | [Envelope](../nodes/envelope.md) |
| `GDVP_PARAM_EXCITER_COLOR` | — | [Exciter](../nodes/exciter.md) |
| `GDVP_PARAM_EXCITER_CRUSH_BITS` | — | [Exciter](../nodes/exciter.md) |
| `GDVP_PARAM_EXCITER_DECORR_OFFSET` | — | [Exciter](../nodes/exciter.md) |
| `GDVP_PARAM_EXCITER_FLAGS` | — | [Exciter](../nodes/exciter.md) |
| `GDVP_PARAM_EXCITER_LEVEL` | — | [Exciter](../nodes/exciter.md) |
| `GDVP_PARAM_EXCITER_PARAM_A` | — | [Exciter](../nodes/exciter.md) |
| `GDVP_PARAM_EXCITER_RATE` | — | [Exciter](../nodes/exciter.md) |
| `GDVP_PARAM_EXCITER_SOURCE_MODE` | — | [Exciter](../nodes/exciter.md) |
| `GDVP_PARAM_FILTER_ATTACK_CV` | CC 75 | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_FILTER_CUTOFF_CV` | CC 74 | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_FILTER_DECAY_CV` | CC 76 | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_FILTER_DRIVE_CV` | NRPN 2/0 | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_FILTER_RELEASE_CV` | CC 78 | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_FILTER_RESONANCE_CV` | CC 71 | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_FILTER_SLOPE` | — | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_FILTER_SUSTAIN_CV` | CC 77 | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_FILTER_TYPE_CV` | NRPN 2/1 | [Filter](../nodes/filter.md) |
| `GDVP_PARAM_MIXER_INPUT_GAIN_0…5` | CC 88–90+ | [Mixer](../nodes/mixer.md) |
| `GDVP_PARAM_MIXER_MASTER_GAIN` | CC 87 | [Mixer](../nodes/mixer.md) |
| `GDVP_PARAM_MIXER_MUTE` | — | [Mixer](../nodes/mixer.md) |
| `GDVP_PARAM_MOD_WHEEL_CV` | CC 1 | [Parameters](../sound/parameters.md#channel--global-modulation) |
| `GDVP_PARAM_OSC1_PITCH_BEND_CV` | CC 16 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC1_PWM_CV` | CC 17 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC1_SHAPE_CV` | CC 18 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC2_DETUNE_CV` | CC 23 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC2_PITCH_BEND_CV` | CC 20 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC2_PWM_CV` | CC 21 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC2_SHAPE_CV` | CC 22 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC_AMPLITUDE_CV` | — | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC_BASE_PHASE_INC` | — | *deprecated* |
| `GDVP_PARAM_OSC_DETUNE_CV` | — | [Oscillator](../nodes/oscillator.md#detune) |
| `GDVP_PARAM_OSC_FM_DEPTH_CV` | NRPN 1/0 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC_FM_RATIO_CV` | NRPN 1/1 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC_MIX_CV` | CC 24 | [Oscillator](../nodes/oscillator.md) |
| `GDVP_PARAM_OSC_PORTAMENTO` | — | [Performance: glide](../concepts/performance.md#glide--portamento) |
| `GDVP_PARAM_PAN_CV` | CC 10 | [Panner](../nodes/panner.md) |
| `GDVP_PARAM_PAN_LAW` | — | [Panner](../nodes/panner.md) |
| `GDVP_PARAM_PITCH_BEND_CV` | pitch-bend | [Performance: pitch bend](../concepts/performance.md#pitch-bend) |
| `GDVP_PARAM_PITCH_CV` | (note) | [Oscillator](../nodes/oscillator.md#pitch) |
| `GDVP_PARAM_PITCH_TARGET` | — | [Oscillator](../nodes/oscillator.md#pitch) |
| `GDVP_PARAM_POLY_PRESSURE_CV` | poly AT | [Performance: MPE](../concepts/performance.md#mpe-per-note-expression) |
| `GDVP_PARAM_VCA_GAIN_CV` | — | [VCA](../nodes/vca.md) |
| `GDVP_PARAM_VCA_MUTE` | — | [VCA](../nodes/vca.md) |
| `GDVP_PARAM_VCA_SATURATION` | — | [VCA](../nodes/vca.md) |
| `GDVP_PARAM_VOLUME_CV` | CC 7 | [Parameters](../sound/parameters.md#channel--global-modulation) |

*Sentinels `GDVP_PARAM_INVALID` and `GDVP_PARAM_COUNT` are not user parameters.*

---

[← Manual index](../README.md)
