# 7 · Patch Management (`.gvp`)

[← Parameters](parameters.md) · [Manual index](../README.md) · Next: [MIDI →](../control/midi.md)

A GDVP patch is a `.gvp` file: human-readable JSON describing a node graph, its wiring, and its
voice-allocation settings. This chapter is the file format reference plus a guide to the bundled
example library. Parser source: `gdvp_gvp_parser.c/.h`; writer: `gdvp_gvp_writer.c/.h`.

---

## 7.1 The `.gvp` format

A patch is one JSON object under the key `gdvp_patch`, with up to four sections:

```json
{"gdvp_patch": {
  "meta":    { "name": "...", "version": "", "author": "", "category": "" },
  "nodes":   [ { "id": 0, "type": "oscillator", "params": { ... } }, ... ],
  "routing": [ { "src": 0, "dst": 1, "src_port": 0, "dst_port": 0 }, ... ],
  "voice":   { "mode": 1, "glide_time": 47, ... }
}}
```

### `meta`
Display metadata, **not consumed by the engine** — `name`, `version`, `author`, `category`
(strings; category values like `"fx"` appear in the library). Buffer limits: name ≤ 64 chars,
the others ≤ 32.

### `nodes` {#nodes}
An array of node objects. Each has:
- **`id`** — an arbitrary unique integer. **Order is irrelevant**; wiring defines execution
  ([DAG §2.3](../concepts/dag.md#compilation-from-your-wiring-to-the-execution-plan)). Duplicate IDs are a
  parse error.
- **`type`** — a string naming the node: `oscillator`, `filter`, `envelope`, `lfo`, `vca`,
  `mixer`, `panner`, `exciter`, the active `gfx_*` types, and the inactive `master_bus` type.
- **`params`** — type-specific fields. The names match the node pages; e.g. an oscillator takes
  `waveform`, `pitch`, `amplitude`, `fm_depth`, `pulse_width`, `detune`; a filter takes `mode`,
  `cutoff`, `resonance`, `slope`; an envelope takes `attack`, `decay`, `sustain`, `release`,
  `*_curve`, `velocity_scale`.

Parameter values are the **14-bit CV** (or the discrete enum) described in
[Parameters §6](parameters.md). Out-of-range values are a parse error (`GVP_ERR_PARAM_OUT_OF_RANGE`).

### `routing` {#routing}
The edge list. Each edge is `{src, dst, src_port, dst_port}` — connect output `src_port` of node
`src` to input `dst_port` of node `dst`. Port convention: **0 = audio, 1 = control/gate**
([DAG §2.1](../concepts/dag.md#port-conventions)). An edge referencing a non-existent node is a dangling-edge
error. These are your **user edges**; the compiler may inject extra mixer/up/down edges at load
([DAG §2.3](../concepts/dag.md#auto-injected-nodes)), but those injected edges are not stored in your file.

### `voice` {#voice}
Optional voice-allocation block (parsed into `gvp_patch_meta_t`). Fields:

`mode`, `glide_time`, `unison_count`, `unison_spread`, `chord_preset`, `arp_enabled`, `arp_type`,
`arp_gate`, `arp_latch`, `arp_octaves`, `arp_voicing`, `arp_steps`, `arp_tempo`, `delay_enabled`,
`delay_time`, `delay_voices`, `delay_drift`.

Note `mode` and the `arp_enabled`/`delay_enabled` flags are independent — Arp and Delay are
interceptors layered on the base allocation mode ([Performance §3.1](../concepts/performance.md#voice-modes)).
All these are UI-space `0–255` / small enums, not 14-bit CV.

---

## 7.2 Limits and errors {#errors}

The parser is zero-allocation and bounded (CR-002/CR-003):

- **File size:** ≤ 32 KB (`GVP_MAX_FILE_SIZE`). Larger → `GVP_ERR_FILE_TOO_LARGE`.
- **Tokens:** ≤ 1024 JSON tokens (`GVP_MAX_TOKENS`).
- **Nodes:** ≤ 64 in the compiled graph (`GDVP_MAX_PATCH_NODES`); parsing uses a 256-node sandbox
  first. Over → `GVP_ERR_NODE_OVERFLOW`.
- **Edges:** bounded by `GDVP_MAX_EDGES`; over → `GVP_ERR_EDGE_OVERFLOW`.

Common parse errors (`gvp_error_t`) and what they mean:

| Error | Meaning |
|---|---|
| `GVP_ERR_MALFORMED_JSON` | Not valid JSON / structure broken |
| `GVP_ERR_MISSING_NODES` | No `nodes` array |
| `GVP_ERR_DUPLICATE_NODE_ID` | Two nodes share an `id` |
| `GVP_ERR_UNKNOWN_NODE_TYPE` | `type` string not recognised |
| `GVP_ERR_PARAM_OUT_OF_RANGE` | A param value exceeds its valid range |
| `GVP_ERR_DANGLING_EDGE` | An edge references a missing node |
| `GVP_ERR_MISSING_NODE_ID` / `_TYPE` | A node lacks `id` / `type` |

The result struct also reports a **byte offset** and a context detail (e.g. the offending node ID)
so the UI can point at the fault.

---

## 7.3 Loading and saving

- **Load:** `gvp_load(path, &ast, &meta, staging_pool)` reads the file (the only stdio touchpoint,
  `gvp_read_file`) and parses straight into the AST, optionally deserialising parameters directly
  into a Part's staging pool. The AST then goes to the DAG compiler and is swapped in via the
  [Airlock](../concepts/dag.md#live-editing-and-the-airlock).
- **Save:** the writer (`gdvp_gvp_writer.c`) serialises a Part back to `.gvp`. It writes from the
  Part's **user edge list** (`user_edge_*`), so what you save is what you drew — the compiler's
  injected mixer/up/down nodes are not persisted, keeping files clean and re-compilable. The
  front-panel Save / Save-As flow is in the [GUI chapter](../control/gui.md#saving).

> When in doubt about an exact serialized field name or numeric encoding, the authoritative
> sources are `gdvp_gvp_parser.c` (read side) and `gdvp_gvp_writer.c` (write side). The schema
> JSON under `gdvp/docs/schema/mis/` documents the MIDI side.

---

## 7.4 The example library {#library}

The engine ships ~50 example patches in `gdvp/examples/`. They double as a tutorial: open them in
the [front panel](../control/gui.md) and read the graph. Grouped by what they teach:

**Subtractive / classic**
`simple_synth`, `bass_lead`, `super_bass`, `pluck`, `analog_brass`, `detuned_strings`,
`overdriven_organ`, `organic_analog_pad`, `aurora_pad_pink`.

**Acid / resonant filter**
`acid_squelch`, `random_squelch`, `psycho_lead`, `Hyperkinetic`.

**FM (DX-style)**
`dx7_bell`, `dx7_brass`, `dx7_choir`, `dx7_epiano`, `dx7_marimba`, `fm_pad`, `fm_rim`.

**LFO routing demos**
`lfo_vibrato`, `lfo_tremolo`, `lfo_pwm`, `lfo_filter_sweep`.

**Unison / supersaw**
`SuperSaw`, `revolution`, `french_stapple`.

**Percussion / noise (Exciter)**
`808_kick`, `Grime 808 kick`, `sub_kick`, `noise_snare`, `metallic_hat`, `vinyl_dust`.

**Effects-suffixed (✅ GFX effects active)**
`*_chorus`, `*_phaser`, `*_reverb`, `*_hall`, `*_echo`, `*_fuzz`, `*_fold`, `*_saturated`,
`*_compressed`, `*_tremolo`, `*_warm` (e.g. `bass_lead_chorus`, `organic_pad_reverb`,
`acid_squelch_hall`, `simple_synth_echo`, `overdriven_organ_fuzz`).

> ✅ **Effects-suffixed patches.** These declare [GFX nodes](../nodes/gfx.md) (delay, FDN reverb,
> phaser, fold, etc.). The GFX family is now fully wired in the dispatch tables and runs on the
> Global EFX Bus (master-domain, post-mix). The synthesis graph plus the effect tail are rendered.
> Patches that also include a `master_bus` will skip only that inactive node. See
> [Effects §5.2](effects.md#the-gfx-family-designed-effects) and [Appendix A](../appendix/engine-status.md).

---

[← Parameters](parameters.md) · [Manual index](../README.md) · Next: [MIDI →](../control/midi.md)
