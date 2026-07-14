# manual — GDVP Operator's Manual

**Author:** François-Xavier Briollais  
**Copyright:** All rights reserved.

[![Version](https://img.shields.io/badge/version-1.4.0-blue)](#)
[![License](https://img.shields.io/badge/license-All%20rights%20reserved-black)](../LICENSE.md)

**General Digital Voicing Program — Producer Engine**
Engine v1.4.0 · Canonical MIDI Schema (MIS) v0.9.1 · Manual revision 1

---

This manual describes how to *operate* GDVP: how to play it, program patches, route
modulation, manage parts, and drive it over MIDI. It is produced from Codebase Documentation via Doxygen
 **as-built behaviour** — what the compiled
engine actually does, including the places where the running code diverges from its own
header comments. Where that divergence matters to you as an operator, it is flagged
explicitly (see [Engine Status & Known Divergences](appendix-status.md)).

> **As-built, not as-marketed.** The [node reference](nodes/README.md) marks each node ✅ Active
> or ⛔ Inactive against the dispatch table in `gdvp_dsp_dispatch.c`, not against prose. The GFX
> effect family and Exciter are now active and produce audio; `master_bus` and the legacy FDN slot
> remain inactive. See [Engine Status & Known Divergences](appendix-status.md).

## How GDVP reaches your ears

GDVP ships in three operator-facing forms, all driving the same deterministic core engine:

| Form | What it is | Entry point |
|---|---|---|
| **Standalone** | A host process (`GDVP_Standalone.exe`) that owns the audio device and hardware MIDI, and spawns the CRT client UI over shared memory. | [Standalone & Hosts](hosts.md#standalone) |
| **VST3 plug-in** | A DAW-hosted processor; the DAW owns transport, audio I/O and automation. | [Standalone & Hosts](hosts.md#vst3) |
| **Client (front panel)** | The SDL2/CRT-phosphor interface (`gdvp_client.exe`) that renders the patch as a panel and edits it. Runs under both forms above. | [The Front Panel](gui.md) |

## Table of contents

### Part I — Concepts
1. [Global Concepts & Signal Model](concepts.md) — parts, voices, nodes, buses, the fixed-point world, the thread model
2. [The Node Graph (DAG)](dag.md) — how patches are graphs, ports, fan-in, compilation order
3. [Performance & Expression](performance.md) — voice modes, glide, unison, chords, arpeggiator, pitch bend, MPE

### Part II — Building sound
4. [Node Reference](nodes/README.md) — every node type, its parameters, ranges and status
   - [Oscillator](nodes/oscillator.md) · [Filter](nodes/filter.md) · [Envelope](nodes/envelope.md) · [LFO](nodes/lfo.md) · [VCA](nodes/vca.md) · [Mixer](nodes/mixer.md) · [Panner](nodes/panner.md) · [Exciter (entropy tap)](nodes/exciter.md) · [Oversamplers](nodes/oversampling.md) · [GFX effect nodes](nodes/gfx.md)
5. [Effects & the Global EFX Bus](effects.md) — master-domain processing, the GFX family, current status
6. [Parameters, Ranges & Values](parameters.md) — the canonical parameter table, CV conventions, scaling math
7. [Patch Management (`.gvp`)](patches.md) — the file format, the example library, loading and saving

### Part III — Control
8. [MIDI Implementation](midi.md) — channel→part mapping, the CC/NRPN map, notes, panic, what is and isn't wired
9. [The Front Panel](gui.md) — the CRT interface, the oscilloscope, node panels, the patch browser

### Reference
- [Parameter Index](parameter-index.md) — every parameter ID, alphabetical, with links
- [Glossary](glossary.md) — Airlock, SPSC, Q16.16, PPQN, OSAC and the rest
- [Appendix A — Engine Status & Known Divergences](appendix-status.md)
- [Appendix B — Constraint Set (CR-001…CR-004 / MISRA)](appendix-constraints.md)

## Conventions used in this manual

- **CV** means a 14-bit control value in the range `0–16383` unless stated otherwise. `8192` is the bipolar centre. See [Parameters](parameters.md#cv).
- **Q16.16** is the engine's internal fixed-point format: a signed 32-bit integer holding 16 integer bits and 16 fractional bits. See [Glossary](glossary.md#q1616).
- Source references look like `gdvp_voice_executor.c` and point into the live tree so any claim here can be checked against code.
- ✅ = active in the live build · ⛔ = present in source but not wired (silent) · ⚠️ = wired but stubbed/partial.

---

*GDVP and the Producer Engine are the work of François-Xavier Briollais. This manual documents the engine as it stands in the source tree; it is a reference, not a warranty of behaviour.*

## License

Copyright François-Xavier Briollais. All rights reserved.

See [`../README.md`](../README.md) for the parent `gdvp-server-web` overview.

## Engineering reference

- **[`gdvp-core-dsp/gdvp/docs/adr/README.md`](../../gdvp-core-dsp/gdvp/docs/adr/README.md)** — Architectural decisions behind the engine.
- **[`gdvp-server-web/deploy/runbooks/README.md`](../deploy/runbooks/README.md)** — Operational runbooks for the license server.
