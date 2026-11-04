# 9 · The Front Panel

[← MIDI](midi.md) · [Manual index](../README.md) · Next: [Parameter Index →](../reference/parameter-index.md)

The GDVP client (`gdvp_client.exe`) is the operator interface: an SDL2 application rendered in a
deliberate **CRT-phosphor** aesthetic, driven entirely by software framebuffer compositing. It is
not a fixed-layout editor — it **walks the active Part's compiled DAG** and draws a panel for each
node, so the interface *is* the patch. Sources: `client/` tree, panel walker
`client_gdvp_front_panel.c`, UI organisms `client_ui_org_*.c`.

---

## 9.1 How the panel is built

`render_front_panel()` is a pure, React-style function that runs every UI frame:

1. **Sync MIDI bindings** from engine state (so on-screen controls track incoming MIDI).
2. **Read the active Part's topology** (`gdvp_client_get_part_topology`) — including the
   compiler's injected mixer/up/down nodes, so the picture matches what executes.
3. **Render node panels in a grid** (4 per row), one *organism* per node.
4. **Dispatch by node type** to the right organism (envelope, filter, exciter, mixer, …).
5. **Route control edits** back to the engine as parameter updates.

Because it renders the *compiled* graph in topological order, the panel reorganises itself when
you load a different patch — there's no fixed "oscillator section"; there's whatever the patch
contains.

### The node organisms
Each node type has a dedicated panel (`client_ui_org_*.c`):
`oscillator`/`synth_panels`, `filter`, `envelope`, `exciter`, `matrix` (routing), `multi`
(multitimbral/part), `part_mixer`, `oscilloscope`, `header_bar`, `status_bar`, `save_modal`. The UI
is layered atoms → molecules → organisms (`client_ui_atoms.c`, `client_ui_molecules.c`,
`client_ui_organisms*`), a small design system rendered to the framebuffer.

---

## 9.2 Reading and editing values

- Controls show the live value and accept edits (mouse/keyboard via `client_input.c`), which become
  parameter updates through the same [bridge](../concepts/concepts.md#the-three-thread-model-and-why-it-shapes-the-feel)
  MIDI uses — so editing on-screen and automating over MIDI are equivalent and consistent
  ([bifurcated model](../sound/parameters.md#bifurcation)).
- Values are the 14-bit CV / enums in [Parameters §6](../sound/parameters.md). The panels apply the same
  perceptual curves the DSP does, so a cutoff knob *feels* even across its travel.
- **Playing notes.** The piano roll at the bottom is playable with the mouse: click a key to sound
  it, drag across keys to glide, release to stop. Black keys sit on top of the whites, exactly as
  drawn. The `A–K` key row plays the same notes from the keyboard (`Z`/`X` shift octave, `F1–F12`
  select part, `Esc` panic), and both routes drive the identical note path MIDI uses.

---

## 9.3 The oscilloscope

An on-panel oscilloscope organism (`client_ui_org_oscilloscope.c`) visualises the live output for
metering and waveform inspection — useful for confirming a patch is actually producing signal
(handy given some [effect nodes are dormant](../sound/effects.md)). It taps the engine's audio output for
display.

---

## 9.4 The patch browser, Save / Save As {#saving}

- A **patch browser** (`client_patch_registry.c`, tested by `test_client_patch_browser.c`) lists
  available `.gvp` patches ([the example library](../sound/patches.md#library)) for loading.
- **Save / Save As** is handled by the save modal organism (`client_ui_org_save_modal.c`) and the
  writer ([Patches §7.3](../sound/patches.md#loading-and-saving)). Saving serialises the Part's **user edge
  list**, so what you drew is what's written — injected plumbing nodes are not persisted.

---

## 9.5 The DAG topology editor

The panel includes an interactive node-graph editor (the `client_ui_dag_*.c` family: layout,
edges, grid, solver, render, delete). It provides a gravity-based layout solver and orthogonal edge
routing so the graph stays readable as you add nodes, with the [Airlock](../concepts/dag.md#live-editing-and-the-airlock)
ensuring edits swap in cleanly at a block boundary without audio glitches. Editing topology here is
the visual equivalent of editing the `routing` section of a [`.gvp`](../sound/patches.md#routing).

---

## 9.6 CRT aesthetic (and why it's not just looks)

The phosphor look is produced by a real framebuffer pipeline (`client_crt.c`,
`client_framebuffer.c`, `client_gfx.c`) with BDF bitmap fonts (`client/fonts/`, compiled by
`tools/bdf_compiler.py`) and a generated CRT lookup table (`tools/generate_crt_lut.py`). It is in
keeping with the engine's philosophy: pre-2000 methods on modern hardware as a *quality* choice —
deterministic, legible, and self-contained rather than dependent on a heavy GPU UI stack.

---

## 9.7 The header bar {#header-bar}

The top row of the window, from left to right:

| Control | What it does |
|---|---|
| `GDVP x.y.z` | The engine version. |
| `SYSTEM` … `ARENA` | The mode tabs. |
| `MSTR` | Opens the mix and master console. |
| ● (REC) | Arms the **retro tape**. While armed, the engine keeps the last 31 seconds of the master output. The dot is lit red while the tape is armed; click again to stop. What was recorded stays available until you arm the tape again. |
| ◀◀ (capture) | Saves the last 30 seconds of the tape as a WAV file in the `captures` folder of your data folder, named `GDVP-<date>-<time>.wav`. |
| `DAC:<mode>` | The output converter: `16RAW` (16-bit, undithered, the default), `16TPD` (16-bit with TPDF dither) or `24DIR` (24-bit direct). Click to step to the next mode. |
| \|◀ ▶ `1.1.00` `120 BPM` `INT` | The transport: return to zero, play / stop, the song position (bar.beat.tick), the tempo (drag up or down) and who drives it: `INT` (this panel), `CLK` (an external MIDI clock) or `DAW`. |

**Capture after the fact.** The tape runs the whole time it is armed, so you never have to press record before
the moment happens: when you play something worth keeping, capture it afterwards. A capture is 16-bit, or 24-bit
when the DAC is in `24DIR`. It is written in the background, so playing carries on undisturbed. The status bar then
shows `SAVED <file>`. If the file could not be written, it shows `CAPTURE FAILED <file>`. A click while the previous
capture is still being written shows `CAPTURE BUSY`: click again a moment later.

**Where the files go.** In the data folder: `~/Library/Application Support/RealDocFX/GDVP/captures` on macOS,
`%APPDATA%\RealDocFX\GDVP\captures` on Windows, and next to the program in a portable install.

**In the plug-in.** The tape deck is dimmed in the plug-in for now: it records nothing until the plug-in's
multi-output update. The DAC badge works there too.

---

[← MIDI](midi.md) · [Manual index](../README.md) · Next: [Parameter Index →](../reference/parameter-index.md)
