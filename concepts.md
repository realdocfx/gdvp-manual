# 1 · Global Concepts & Signal Model

[← Manual index](README.md) · Next: [The Node Graph →](dag.md)

This chapter is the mental model everything else hangs on. Read it once and the rest of
the manual stops being a list of features and starts being a coherent instrument.

---

## 1.1 The shape of the instrument

GDVP is a **modular, polyphonic, multitimbral** synthesizer. Three words, three layers:

- **Multitimbral** — there are **16 Parts**. Each Part is an independent instrument with its
  own patch, its own voice-allocation behaviour, and its own slice of the voice pool. Parts
  map 1:1 onto MIDI channels (Part 0 = channel 1, … Part 15 = channel 16). See
  [MIDI](midi.md#channels).
- **Polyphonic** — each Part plays many notes at once by allocating **Voices** from a shared
  global pool of **128 voices**. How notes claim voices is the Part's *voice mode*
  ([Performance & Expression](performance.md)).
- **Modular** — a Part's *sound* is not fixed. It is a **graph of DSP nodes** (oscillators,
  filters, envelopes…) wired together. That graph is the patch. See [The Node Graph](dag.md).

```
System
 ├── 16 Parts ────────────── one per MIDI channel
 │     └── a patch (node graph) + a voice mode
 ├── 128 Voices (global pool) ─ claimed by Parts on note-on
 ├── 8192 DSP nodes (global pool) ─ provisioned per voice from the patch
 ├── 4096 local buses (intra-voice routing)
 ├── 256 universal buses (the global routing fabric)
 └── 1 Global EFX bus ──────── monophonic, post-mix (reverb/delay live here)
```

Source: `gdvp_system.h` (`gdvp_system_t`), `gdvp_voice_manager.h` (`gdvp_vam_elastic_t`).

### Parts, voices, nodes — who owns what

A **patch** describes *one voice's worth* of nodes and wiring. When a Part needs to sound a
note polyphonically, the Voice Allocation Manager (VAM) hands it a free voice and
**provisions** a private copy of the patch's nodes for that voice from the 8192-node global
pool. Ten notes of the same patch = ten voices, each with its own node instances and its own
filter/envelope state. This is why one voice's filter sweep never bleeds into another's.

The exception is the **Global EFX bus** (master domain): a single monophonic chain that
processes the *sum* of all voices. Reverb and delay belong here — you want one room, not one
room per note. See [Effects & the Global EFX Bus](effects.md).

---

## 1.2 The fixed-point world (no floating point, ever)

GDVP performs **no runtime floating-point arithmetic** (constraint **CR-001**, see
[Appendix B](appendix-constraints.md)). Everything an operator touches resolves to integers.
Two formats dominate, and understanding them explains every number you'll meet:

### 14-bit Control Values (CV) — the operator's unit
Most parameters are expressed as a **14-bit CV**: an integer from **0 to 16383**.

- For **unipolar** parameters (cutoff, amplitude, gain…) `0` is minimum and `16383` is maximum.
- For **bipolar** parameters (pitch bend, modulation offsets, pan position…) **`8192` is the
  centre/zero point**; below it is negative, above it is positive.

14 bits is the resolution of high-resolution MIDI, which is why the engine speaks it natively
(see [MIDI 14-bit pairing](midi.md#highres)). Full detail and the per-parameter table is in
[Parameters, Ranges & Values](parameters.md).

### Q16.16 — the engine's internal precision
Internally, smoothing and accumulation happen in **Q16.16**: a signed 32-bit value with 16
integer and 16 fractional bits. You never type a Q16.16 number, but it is why pitch glides,
gain changes and pan sweeps are *smooth* rather than stepped — the engine tracks them with 16
bits of sub-unit precision and converges toward your target with an integer EMA (exponential
moving average). See the [Glossary](glossary.md#q1616) and, e.g., the oscillator's
`smoothed_pitch_cv` in [Oscillator](nodes/oscillator.md).

### Audio samples
Audio is signed 16-bit PCM (`int16_t`) flowing between nodes. The system runs at the host's
sample rate (the standalone host asks the OS for its native rate; `44100` Hz is the reference
configuration) in **blocks of 64 samples** (or 128 when a node is oversampled — see
[Oversamplers](nodes/oversampling.md)).

---

## 1.3 Pitch as control voltage

GDVP models pitch the way a modular synth does — as a control voltage, not a note number.
The conversion is fixed and worth memorising:

> **1 semitone = 128 CV units.** One octave = 1536 CV units.

So a 14-bit pitch CV spans 16384 / 128 = **128 semitones** of range, and `8192` sits at the
centre. This is the same unit the [chord presets](performance.md#chords) use to express
intervals (a major third is `512` = 4 × 128) and the same unit oscillator **detune** trims in
(`±128` CV steps = ±1 semitone, ~1 cent per step). See [Oscillator](nodes/oscillator.md#detune).

---

## 1.4 The three-thread model (and why it shapes the feel)

GDVP strictly segregates work across threads. You don't manage this, but it explains latency,
smoothness, and a couple of the known issues.

| Layer | Thread | Job |
|---|---|---|
| **Producer** | Host / UI | Receives your input (notes, knob turns, MIDI). Does the *heavy* allocation math: voice stealing, unison spreads, arpeggiator scheduling. Stages results. |
| **Bridge (Airlock)** | — | A set of **lock-free SPSC queues** and a **staging pool** that carry parameter changes and commands from Producer to Consumer without locks. |
| **Consumer** | Audio (hard real-time) | Renders the DSP graph block by block. Pulls staged changes at block boundaries, never blocks, never allocates. |

Key consequences for you:

- **Knob moves are smoothed and quantised in time.** The bridge applies *mathematical
  decimation* (a CC noise floor and a max-latency cap) so a flood of MIDI CCs can't swamp the
  audio thread. Tiny jitter below the noise floor is intentionally ignored. See
  [MIDI: Smart CC immunity](midi.md#immunity).
- **Two parameter domains, deliberately separate.** A patch/UI value (the *base*, e.g. base
  cutoff) and a live modulation offset (from MIDI/LFO, *bipolar around 8192*) target
  **different fields** of the same node and are merged at audio rate. This "bifurcated"
  routing is why automating cutoff over MIDI doesn't fight the knob position. See
  [Parameters](parameters.md#bifurcation).
- **Transport is a bus, not a master.** A 64-bit *tick pulse mask* is computed once per block
  and passed by value to every node, so tempo-synced features (LFO sync, arp) line up
  sample-accurately. Clock runs at **96 PPQN**. See [Performance: tempo](performance.md#tempo).

The full architecture write-ups live in the developer docs (`gdvp/docs/THREAD_SEGREGATION.md`,
`FABRIC_BRIDGE.md`, `PRODUCER.md`, `CONSUMER.md`); this manual only surfaces what changes how
the instrument *plays*.

---

## 1.5 Determinism as a feature

Every processing path is **O(N)-bounded** with a fixed iteration count per block (**CR-003**),
there is **no dynamic allocation** after boot (**CR-002**), and the codebase targets **MISRA C
2012** (**CR-004**). For an operator this means: no glitches from a garbage-collector pause, no
allocation hiccup when you stack voices, and identical output for identical input. The cost is
that everything is bounded — fixed pools, fixed node budgets — so a patch has hard ceilings
(64 nodes per patch graph, 16 voices per Part, etc.). Those ceilings are listed where they bite,
and collected in [Appendix B](appendix-constraints.md).

---

[← Manual index](README.md) · Next: [The Node Graph →](dag.md)
