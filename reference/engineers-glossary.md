# The engineer's glossary

[← Manual index](../README.md)

Terms used throughout the manual and the GDVP codebase, in plain operator language.

### Airlock {#airlock}
The transactional hand-off between the Host/UI thread (Producer) and the audio thread (Consumer).
Edits are staged, a new plan is compiled, and an atomic flag swaps it in at a block boundary so
re-patching never clicks or crashes. See [DAG §2.5](../concepts/dag.md#live-editing-and-the-airlock).

### Block / frame
A fixed chunk of audio processed at once: **64 samples** normally, **128** when a node is
oversampled. All DSP loops run a fixed number of iterations per block (determinism, CR-003).

### CV (Control Value) {#cv}
A 14-bit integer `0–16383` that expresses a parameter. `8192` is the bipolar centre. The common
currency of knobs, patches and MIDI. See [Parameters §6.1](../sound/parameters.md#cv).

### DAG (Directed Acyclic Graph)
The node-and-wire structure of a patch. Acyclic so a stable execution order exists. See
[The Node Graph](../concepts/dag.md).

### EMA (Exponential Moving Average)
The integer smoothing used everywhere (pitch glide, gain, pan, filter mod). A "shift" factor sets
the rate; `0` = instant, larger = slower/smoother.

### Kahn's algorithm {#kahn}
The topological sort that orders nodes so each runs after its inputs. Run by the DAG compiler at
patch load. See [DAG §2.3](../concepts/dag.md#compilation-from-your-wiring-to-the-execution-plan).

### LBM / UBM
Local Bus Matrix (intra-voice routing, 4096 buses) and Universal Bus Matrix (the global fabric,
256 buses). The "elastic" two-tier routing that lets dense patches avoid bus starvation.

### Master domain / Global EFX bus
A single monophonic processing chain on the *summed* output of all voices — where reverb/delay
belong. Flagged `GDVP_NODE_FLAG_MASTER_DOMAIN`. See [Effects](../sound/effects.md).

### MIS (MIDI Implementation Schema)
GDVP's machine-readable MIDI map; **v0.9.1** lives in `gdvp/config/gdvp_canonical_map.json` and
`gdvp/docs/schema/mis/`. See [MIDI §8.4](../control/midi.md#map).

### OSAC (Oversampling Accuracy Correction) {#osac}
Using mathematically exact coefficient LUTs for the active rate (64 vs 128) instead of
approximating by halving — notably in the [filter](../nodes/filter.md). Keeps tuning correct when
oversampled.

### Part
One of 16 independent instruments, mapped 1:1 to a MIDI channel. Has its own patch and voice mode.
See [Concepts §1.1](../concepts/concepts.md).

### PPQN
Pulses Per Quarter Note — the sequencer clock resolution. GDVP runs at **96 PPQN**. Drives the
[arpeggiator](../concepts/performance.md#the-arpeggiator) and tempo sync.

### Q16.16 {#q1616}
The engine's fixed-point number: a signed 32-bit value with 16 integer and 16 fractional bits.
Gives sub-unit precision for smooth glides/sweeps without floating point. See
[Concepts §1.2](../concepts/concepts.md#q1616--the-engines-internal-precision).

### SPSC (Single-Producer Single-Consumer) {#spsc}
The lock-free queue type carrying events/parameters from the Host thread to the audio thread. Part
of the [Airlock](#airlock). See [Concepts §1.4](../concepts/concepts.md#the-three-thread-model-and-why-it-shapes-the-feel).

### Staging pool
The Host-side mirror of a Part's nodes where parameter edits land before being atomically consumed
by the audio thread. The base/macro half of the [bifurcated model](../sound/parameters.md#bifurcation).

### Tick pulse mask
A 64-bit value (one bit per sample-frame) marking which frames land on a transport tick. Computed
once per block and passed by value to every node for sample-accurate sync. See
[Performance §3.8](../concepts/performance.md#tempo).

### TPT-SVF / ZDF
Topology-Preserving Transform State-Variable Filter with Zero-Delay Feedback — GDVP's
unconditionally stable [filter](../nodes/filter.md).

### VAM (Voice Allocation Manager)
The subsystem that turns notes into voices: modes, stealing, unison, chords, arp, the EFX bus.
`gdvp_voice_manager.c/.h`. See [Performance](../concepts/performance.md).

### Voice
A single sounding instance of a patch, with its own node copies and state. 128 in the global pool;
up to 16 per Part. See [Concepts §1.1](../concepts/concepts.md).

---

[← Manual index](../README.md)
