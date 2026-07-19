# Standalone & Hosts

[← Manual index](../README.md)

GDVP's engine is the same in every form; what differs is who owns audio I/O, transport and the UI.
This page covers the three operator-facing forms. Sources: `standalone/`, `proxy/`, `client/`.

---

## Standalone {#standalone}

`GDVP_Standalone.exe` (`standalone/src/main_standalone.c`) is a self-contained host. On launch it:

1. Initialises cross-platform paths (`gdvp_paths`).
2. **Validates licence** — if none is found it runs in **DEMO mode**:
   > ⚠️ In demo mode, audio is interrupted with noise after **60 seconds**. A valid licence unlocks
   > full, uninterrupted operation.
3. Opens the audio device via **miniaudio**, asking the OS for its **native sample rate** (the
   engine adapts; 44.1 kHz is the reference). Output is stereo float at the device; the engine works
   in 16-bit PCM internally.
4. Starts **hardware MIDI** input (`gdvp_standalone_midi.c`, Win32 backend
   `client_hw_midi_win32.c`).
5. Sets up **IPC shared memory** and **spawns the CRT client** (`gdvp_client.exe`) as a separate
   process, connected over that shared memory (`--ipc "Local\\GDVP_Standalone_IPC"`).

So in standalone use, the **host process** does sound + MIDI and the **client process** does the
UI; they communicate lock-free over shared memory (`proxy/include/gdvp_ipc_shm*.h`). Transport
(tempo/PPQN clock) is **internal** — set tempo in-app; the [arpeggiator](../concepts/performance.md#the-arpeggiator)
and LFO key-sync run off this clock.

---

## VST3 plug-in {#vst3}

The VST3 form lives in `proxy/` (`gdvp_vst3_processor.cpp`, `_controller.cpp`, `_factory.cpp`,
bridged to the C engine via `gdvp_vst3_bridge.c`). Here the **DAW is the host**:

- The DAW owns **audio I/O** and the **sample rate / block size**.
- The DAW owns **transport** — play state and BPM follow the DAW timeline, so tempo-synced features
  align to the project (subject to the [LFO transport-sync status note](../concepts/performance.md#tempo)).
  The header-bar tempo readout is dimmed and tagged `DAW` while hosted: it reports the project
  tempo but cannot set it. Set tempo in your DAW. See [Tempo & transport](../concepts/performance.md#tempo).
- **Automation** arrives as parameter changes through the same bridge the
  [MIDI map](midi.md#map) feeds, using the canonical parameter IDs.

The plug-in uses the same IPC/shared-memory and tri-buffer visualisation plumbing
(`gdvp_viz_tribuf.h`) as standalone for any out-of-process UI/metering.

---

## The client (front panel) {#client}

`gdvp_client.exe` is the [front-panel](gui.md) UI and runs under both forms above. It renders the
active Part's compiled graph, edits parameters and topology, browses and saves
[`.gvp` patches](../sound/patches.md), and shows the oscilloscope. It holds **no audio engine of its own** —
it drives the engine in the host process over IPC.

---

## Which form for what

- **Sketching, hardware-MIDI jamming, no DAW:** Standalone.
- **In a session, with automation and project tempo:** VST3 in your DAW.
- Either way you get the identical deterministic engine and the same patches.

---

[← Manual index](../README.md)
