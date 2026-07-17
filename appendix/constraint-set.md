# Appendix B · Constraint Set (CR-001…CR-004 / MISRA) & Hard Limits

[← Manual index](../README.md)

GDVP is built to a strict engineering contract. These constraints are *why* the instrument behaves
deterministically — and why it has fixed ceilings. As an operator you mostly feel them as
"it never glitches, but it has hard limits."

---

## B.1 The four core constraints

| ID | Name | What it means | Operator-visible effect |
|---|---|---|---|
| **CR-001** | No runtime floating-point | All DSP uses integer math + LUTs; no `math.h` in hot paths. | Bit-exact, reproducible output; perceptual curves (x³ cutoff, x⁶ env, log LFO) instead of float formulas. |
| **CR-002** | No dynamic allocation | All memory is pre-allocated at boot from an arena; no malloc/free at runtime. | No allocation hiccups when stacking voices; but **fixed pools** (hard ceilings below). |
| **CR-003** | Deterministic / bounded execution | Every path is O(N)-bounded with fixed per-block iteration counts; O(1) dispatch. | No timing jitter; predictable CPU; identical timing run to run. |
| **CR-004** | MISRA C 2012 | Coding-standard compliance (typed bit-fields, unsigned shifts, explicit casts, no side-effecting booleans). | Robustness/safety; relevant if GDVP is embedded or certified. |

These are enforced in the build: pre-commit validators (`.githooks/cr001_validator.py`,
`cr002_buffer_validator.py`, `misra_rule_17_7_validator.py`, graph/node-size checks) and CI gate
against them. Developer detail: `gdvp/docs/MISRA.md`, `gdvp/docs/architecture/pre-commit-validation.md`.

---

## B.2 Hard limits you can hit

Because of CR-002, everything is a fixed pool. The ceilings that affect patches and performance:

| Limit | Value | Source |
|---|---|---|
| Parts (multitimbral) | **16** | `GDVP_VAM_MAX_PARTS` |
| Voices, global pool | **128** | voice pool |
| Voices per Part | **16** | `voice_indices[16]` |
| DSP nodes, global pool | **8192** | node pool |
| Nodes per patch graph | **64** | `GDVP_MAX_PATCH_NODES` |
| Parse sandbox nodes | **256** | pre-sort sandbox |
| Local buses (LBM) | **4096** | local bus pool |
| Universal buses (UBM) | **256** | bus matrix |
| Local buses per voice | **16** | `assigned_buses[16]` |
| Global EFX nodes | **8** | `efx_pool[8]` |
| Node size | **32 bytes** exactly | `_Static_assert` in `gdvp_nodes.h` |
| `.gvp` file size | **32 KB** | `GVP_MAX_FILE_SIZE` |
| `.gvp` JSON tokens | **1024** | `GVP_MAX_TOKENS` |
| Audio block | **64** (128 oversampled) | executor |
| Sequencer clock | **96 PPQN** | sequencer |
| Voice modes | **8** | `gdvp_voice_mode_t` |
| Chord presets | **12** | `gdvp_chord_presets[]` |
| Mixer inputs | **6** | `gdvp_node_mixer_t` |

Exceeding a `.gvp` limit is a clean load-time error ([Patches §7.2](../sound/patches.md#errors)), not a
crash. Running out of voices triggers voice stealing (LRU) rather than failure.

---

## B.3 Why this matters to you

The trade GDVP makes: **no surprises at runtime, in exchange for fixed budgets at design time.**
You can rely on it never glitching from memory or GC pressure, the output being identical every
time, and CPU being predictable. In return, you plan within the ceilings above — which for musical
patches (a handful of nodes, ≤16 voices) are generous.

---

[← Manual index](../README.md)
