# General Digital Voicing Program (GDVP)

*A digital synthesizer built like an instrument, engineered to the discipline of safety-critical software.*

Welcome to the official Wiki and Operator's Manual for the **General Digital Voicing Program (GDVP) — Producer Engine**. 

GDVP is a 128-voice, 16-part multitimbral digital synthesizer that behaves less like standard audio software and more like professional, fail-safe hardware[cite: 2]. It operates flawlessly as a standalone application and a VST3 plug-in across Windows and macOS, driven by a deeply optimized C11 core[cite: 2].

---

## 🏗️ Repository Architecture

The GDVP ecosystem is bifurcated into highly specialized submodules managed by a monorepo orchestrator[cite: 2, 5].

*   **[`general_digital_voicing_program`](https://github.com/realdocfx/general_digital_voicing_program)**
    The monorepo orchestrator[cite: 2, 5]. Contains the global build scripts (`build-all.ps1`), CI/CD YAML definitions, deployment tooling, and the overarching project structure[cite: 2, 5].
*   **[`gdvp-core-dsp`](https://github.com/realdocfx/gdvp-core-dsp)**
    The heart of the instrument[cite: 2, 5]. Contains the C11 DSP synthesis engine (`gdvp/`), the SDL2 Immediate-Mode GUI client (`client/`), and the C++ VST3 proxy facade (`proxy/`)[cite: 2, 5].
*   **[`gdvp-data-rom`](https://github.com/realdocfx/gdvp-data-rom)** *(Submodule of Core DSP)*
    The immutable mathematical substrate[cite: 3]. Contains the generated Q16.16 LUT tables (sine, TPT-SVF filter coefficients, etc.) and the Python scripts used to build and cryptographically seal them[cite: 3].
*   **[`gdvp-server-web`](https://github.com/realdocfx/gdvp-server-web)**
    The distribution and licensing backend[cite: 4, 5]. Contains the FastAPI Python server (`server/`) and the Vite/React web portal (`web/`) for managing testers, first-party analytics, and machine-bound Ed25519 licenses[cite: 4, 5].
*   **[`gdvp-manual`](https://github.com/realdocfx/gdvp-manual)**
    This repository[cite: 1, 6]. It houses the markdown files, architectural Milestone specifications, and the operator's manual[cite: 1, 6].

---

## ⚙️ The Determinism Dividend

Most music software is written to ship; GDVP is written to a strict safety-critical standard. The engine operates under four unyielding architectural constraints that guarantee phase-coherent repeatability, zero audio dropouts, and immunity to session crashes:

*   **CR-001: Zero Runtime Floating-Point Math:** All DSP loops, envelopes, and exponential sweeps are resolved using pre-calculated Look-Up Tables (LUTs) and signed 32-bit fixed-point arithmetic in Q16.16 format[cite: 2, 5]. There is no rounding drift and no reliance on math.h in the hot paths.
*   **CR-002: Zero Dynamic Memory Allocation:** Exactly zero calls to `malloc` or `free` at runtime. The entire application universe—including the 128-voice pool, 8192 DSP nodes, and 4096 local buses—is instantiated into a strict 900 KB static arena during boot[cite: 4, 5].
*   **CR-003: Deterministic Hard Real-Time Execution:** Every processing path is bounded in constant time. Voice processing is O(1), ensuring under 10% CPU load at full 128-voice polyphony[cite: 4, 5].
*   **CR-004: MISRA C:2012 Compliance:** The C11 core is verified against aerospace-grade static analysis quality gates, ensuring unparalleled operational safety[cite: 2, 5].

---

## 📚 Wiki Directory

Navigate the GDVP documentation using the links below. 

### Part I: Architecture & Concepts
*   **[Global Concepts & Signal Model](concepts/concepts.md)** — Parts, voices, fixed-point math, and the lock-free SPSC three-thread model[cite: 1, 6].
*   **[The Node Graph (DAG)](concepts/dag.md)** — Understanding patches as Directed Acyclic Graphs, ports, fan-in, and Kahn's topological compilation[cite: 1, 6].
*   **[Performance & Expression](concepts/performance.md)** — Voice allocation modes (Mono, Legato, Poly, Unison, Chord, Arp), glide logic, and MPE pressure[cite: 1, 6].

### Part II: Building Sound
*   **[Node Reference](nodes/README.md)** — The definitive guide to the 32-byte DSP blocks[cite: 1, 6].
    *   [Oscillator](nodes/oscillator.md) | [Filter (TPT-SVF)](nodes/filter.md) | [Envelope (ADSR)](nodes/envelope.md) | [LFO](nodes/lfo.md) | [VCA](nodes/vca.md) | [Exciter](nodes/exciter.md) | [Panner](nodes/panner.md) | [Mixer](nodes/mixer.md) | [Oversamplers](nodes/oversampling.md) | [GFX](nodes/gfx.md)[cite: 1, 6]
*   **[Effects & the Global EFX Bus](sound/effects.md)** — Master-domain processing, including the GFX family (Delay, Gain, Env, APF, FDN Reverb, Mod)[cite: 1, 6].
*   **[Parameters, Ranges & Values](sound/parameters.md)** — The 14-bit CV convention, the bifurcated parameter model (Base vs. Modulation), and the complete ID index[cite: 1, 6].
*   **[Patch Management (`.gvp`)](sound/patches.md)** — The JSON patch format, routing semantics, and the factory example library[cite: 1, 6].

### Part III: Control & Interface
*   **[The Front Panel (GUI)](control/gui.md)** — The CRT-phosphor SDL2 interface, grid-based Wabi-Sabi layout, and the real-time zero-crossing oscilloscope[cite: 1, 6].
*   **[MIDI Implementation](control/midi.md)** — Channel-to-Part mapping, the Canonical CC/NRPN map, 14-bit high-resolution pairing, and Smart CC Immunity[cite: 1, 6].
*   **[Standalone & Hosts](control/hosts.md)** — Differences between running `GDVP_Standalone.exe` natively vs. DAW-hosted `GDVP_Proxy.vst3`[cite: 1, 6].

### Part IV: Reference & Appendices
*   **[Beta Tester & Activation Guide](guide/beta-tester-guide.md)** — Walkthrough for machine-ID binding and unlocking the engine[cite: 1, 6].
*   **[Parameter Index](reference/parameter-index.md)** — Alphabetical lookup of every parameter ID[cite: 1, 6].
*   **[Glossary](reference/glossary.md)** — Terminology reference (Airlock, OSAC, TPT-SVF, VAM)[cite: 1, 6].
*   **[Appendix A: Engine Status & Known Divergences](appendix/engine-status.md)** — Ground-truth documentation of live vs. stubbed node types[cite: 1, 6].
*   **[Appendix B: Constraint Set & Hard Limits](appendix/constraint-set.md)** — The exact numerical ceilings of the engine (e.g., 64 maximum nodes per patch)[cite: 1, 6].