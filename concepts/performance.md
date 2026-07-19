# 3 · Performance & Expression

[← The Node Graph](dag.md) · [Manual index](../README.md) · Next: [Node Reference →](../nodes/README.md)

This chapter covers how GDVP turns your *playing* into voices: the eight voice modes, glide,
unison, chords, the arpeggiator, the strum/delay allocator, and expressive control (velocity,
pitch bend, pressure). All of this is per-Part and lives in the Voice Allocation Manager (VAM),
`gdvp_voice_manager.c/.h`.

---

## 3.1 Voice modes

Each Part runs in exactly one of **eight voice modes** (`gdvp_voice_mode_t`). The mode decides
how incoming notes claim voices from the pool.

| # | Mode | Behaviour |
|---|---|---|
| 0 | **MONO** | One voice. Re-triggers itself on each new note. **No portamento** — glide is LEGATO-only (see [GLIDE](../reference/glossary.md#glide)). |
| 1 | **LEGATO** | One voice. Overlapping notes glide **without** re-triggering envelopes or resetting oscillator phase. |
| 2 | **POLY** | Standard polyphony, LRU voice stealing, up to 16 simultaneous voices. The default for most patches. |
| 3 | **UNISON** | One note → *N* detuned voices stacked. Spread set by the unison spread parameter. |
| 4 | **DUO** | Two-note polyphony; the voice budget is split, ~N/2 voices per held note. |
| 5 | **CHORD** | One note triggers *N* voices at fixed harmonic intervals from a chord preset. |
| 6 | **DELAY** | Strum/echo: one note spawns several voices with staggered onset times. |
| 7 | **ARP** | Arpeggiator: held notes are played back as a timed sequence. |

Source: `gdvp_voice_mode_t` in `gdvp_voice_manager.h`. Internally the engine separates the
**allocation strategy** (poly/mono/legato/unison/duo/chord, `gdvp_voice_allocation_t`) from two
**interceptors** (Arp and Delay) that sit *in front of* allocation — which is why, in patches,
you'll see both a `mode` field and independent `arp_enabled` / `delay_enabled` flags
([patch voice section](../sound/patches.md#voice)).

Switching mode performs a clean **state-transition flush**: all active voices are hard-cut and
mode-specific buffers (e.g. arpeggiator memory) are cleared, so you never get ghost notes
bleeding across a mode change (`gdvp_part_set_voice_mode`).

---

## 3.2 Glide / portamento

In MONO and LEGATO, successive notes **glide** in pitch instead of jumping. Glide is a single
parameter:

- **Glide time** — UI range `0–255`, where `0` = instant (no glide) and `255` = slowest.
  It maps to the oscillator's `portamento_shift` (an EMA slew factor). Because the engine slews
  the *linear pitch CV* in Q16.16, the resulting frequency contour is exponential — i.e.
  constant-time, musically correct portamento. See [Oscillator: pitch slewing](../nodes/oscillator.md#pitch).

Voice-param key `0` (`glide_time`) via `gdvp_param_bridge_update_voice_param`.

---

## 3.3 Unison

UNISON stacks several detuned copies of every note for thickness.

- **Unison count** — `2–16` voices, default 4. (Voice-param key `1`.)
- **Unison spread** — UI `0–255`, scaled internally to a 14-bit detune CV that fans the voices
  symmetrically around the played pitch. (Voice-param key `2`.)

Spread is in the same pitch-CV currency as everything else (128 CV = 1 semitone), so modest
spread values stay within a few cents — the classic "supersaw" thickening rather than a chord.
The `SuperSaw.gvp` example is built on this ([library](../sound/patches.md#library)).

---

## 3.4 Chords

CHORD mode turns a single key into a voiced chord using one of **12 built-in presets**
(`gdvp_chord_presets[]`). Intervals are expressed in pitch CV (128 = 1 semitone):

| Idx | Name | Notes | Intervals (CV) | In semitones |
|---|---|---|---|---|
| 0 | MAJ | 3 | 512, 896 | +4, +7 |
| 1 | MIN | 3 | 384, 896 | +3, +7 |
| 2 | MAJ7 | 4 | 512, 896, 1408 | +4, +7, +11 |
| 3 | MIN7 | 4 | 384, 896, 1280 | +3, +7, +10 |
| 4 | DOM7 | 4 | 512, 896, 1280 | +4, +7, +10 |
| 5 | DIM | 4 | 384, 768, 1152 | +3, +6, +9 |
| 6 | AUG | 3 | 512, 1024 | +4, +8 |
| 7 | SUS4 | 3 | 640, 896 | +5, +7 |
| 8 | SUS2 | 3 | 256, 896 | +2, +7 |
| 9 | PWR | 2 | 896 | +7 (fifth) |
| 10 | OCT | 2 | 1536 | +12 (octave) |
| 11 | 5+OCT | 3 | 896, 1536 | +7, +12 |

The played note is the root; intervals add on top. Each chord tone consumes a voice, so a MAJ7
chord uses four voices per key. Chord preset is voice-param key `3`. Source:
`gdvp_chord_presets[]` in `gdvp_voice_manager.h`.

---

## 3.5 The arpeggiator

ARP mode (mode 7, or the `arp_enabled` interceptor) is a true multi-key arpeggiator with its own
DSP-side state (`gdvp_arp_dsp_state_t`): it holds up to 16 depressed keys (sorted, with
velocities), a playhead, and a tick countdown synced to transport.

### Arp parameters

| Parameter | Values | Notes | Key |
|---|---|---|---|
| **Type** | UP / DOWN / UP+DOWN / RANDOM | Sequence direction (`gdvp_arp_type_t`). RANDOM uses an LCG PRNG. | 4 |
| **Tempo / division** | 0=1/4, 1=1/8, 2=1/8T, 3=1/16, 4=1/16T, 5=1/32 | Step length against the 96-PPQN clock. | 10 |
| **Gate** | `0–255` (128 = 50%) | Fraction of each step the note sounds. | 5 |
| **Latch** | on/off | Keeps the arp running after you release the keys. | 6 |
| **Octaves** | 0=1oct … 3=4oct | Octave-span the pattern walks through. | 7 |
| **Voicing** | 0=MONO, 1=MULTI, 2+=chord preset | Each step can be a single note or a voiced chord. | 8 |
| **Steps** | 0=Auto, 1–64 | Truncate the pattern to a fixed number of steps. | 9 |
| **Env mode** | 0=Legato (sustain-through), 1=Soft-retrigger | Whether each step re-strikes the envelope. | — |

Division maps to PPQN ticks directly (1/16 = 24 ticks; see `gdvp_arp_division_t`). Configure via
`gdvp_vam_set_arp_config` (host) or the per-mode voice params; latching is also intercepted so
releasing all physical keys clears the latch tracking (`physical_keys_down`). Source:
`gdvp_arp_dsp_state_t`, `gdvp_voice_manager_state_t`.

---

## 3.6 Strum / Delay allocation

DELAY mode (mode 6, or the `delay_enabled` interceptor) spawns several voices from one note with
**staggered onsets** — a strum or echo built from real voices rather than a delay line.

| Parameter | Values | Meaning | Key |
|---|---|---|---|
| **Delay time** | `0–255` | Stagger interval between successive voices (maps to a PPQN offset). | 11 |
| **Delay voices** | `1–6` | How many strummed voices. | 12 |
| **Delay drift** | `0–255` | Pitch drift added per successive voice, for human-strum detune. | 13 |

Source: `gdvp_voice_manager_state_t` delay fields. This is distinct from the audio
[delay effect node](../nodes/gfx.md#delay) — DELAY mode is a *voice-allocation* effect.

---

## 3.7 Expression: velocity, pitch bend, pressure

### Velocity
Note-on velocity is carried into the voice and read by the envelope as `velocity_scale`,
scaling dynamic range. With the envelope's **Expressive** flag set, the envelope also tracks
continuous pressure (MPE). See [Envelope](../nodes/envelope.md#velocity).

### Pitch bend {#pitchbend}
Pitch bend is applied **per Part, in the voice executor**, as a signed CV offset added to every
voice's note CV each block:

- **Bend offset** — signed CV (`pitch_bend_offset_cv`).
- **Bend range** — `0–48` semitones, default **2** (`pitch_bend_range`).

Because bend is added downstream of allocation, it tracks all sounding voices uniformly. Source:
`gdvp_voice_manager_state_t` pitch-bend fields. MIDI pitch-bend routing: [MIDI](../control/midi.md#pitchbend).

### MPE / per-note expression
The parameter space includes MPE targets — **channel pressure**, **poly pressure**, and a
dedicated **pitch-bend CV** (`GDVP_PARAM_CHANNEL_PRESSURE_CV`, `GDVP_PARAM_POLY_PRESSURE_CV`,
`GDVP_PARAM_PITCH_BEND_CV`). See [Parameters](../sound/parameters.md#mpe). Continuous pressure reaches the
envelope when its Expressive flag is enabled.

---

## 3.8 Tempo & transport {#tempo}

The engine keeps a fixed-point sequencer at **96 PPQN**. Tempo is set with
`gdvp_system_set_tempo(system, bpm)`. Each audio block the executor computes a 64-bit
**tick pulse mask** (one bit per sample-frame that lands on a tick) and passes it by value to
every node, so tempo-synced features can resolve *within* the block, sample-accurately.

> ⚠️ **Status note.** The transport bus and tick mask are fully plumbed, and the arpeggiator
> uses them. The **LFO transport-sync** path, however, is staged but not yet active in the LFO
> kernel — `tick_mask` is currently received and cast to `(void)` there (see
> [LFO §sync](../nodes/lfo.md#sync) and [Appendix A](../appendix/engine-status.md)). Key-sync (phase reset on
> note) does work; tempo-sync does not yet.

### Setting tempo

Tempo is shown at the right of the header bar as a **BPM** readout. Drag it vertically to
change it, within **20–300 BPM**.

Under the VST3 form, transport (play state and BPM) follows the **host DAW**: the readout
tracks the project tempo, is dimmed, and is tagged `DAW` to show where the value comes from.
Dragging it does nothing there by design — the DAW is the master clock, and the engine refuses
tempo writes from the UI for as long as the host is driving the transport. Change the tempo in
your DAW instead. Under standalone, tempo is internal and the readout is yours to set.

See [Hosts](../control/hosts.md).

---

[← The Node Graph](dag.md) · [Manual index](../README.md) · Next: [Node Reference →](../nodes/README.md)
