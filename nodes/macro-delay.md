# Macro Delay

**Author:** François-Xavier Briollais  
**Copyright:** All rights reserved.

**Node type:** `GDVP_NODE_MACRO_DELAY`  
**Status:** ⛔ Inactive (NULL processor)  
**Version:** 1.4.0

## What it is

The Macro Delay node was intended to provide a long, tempo-synchronized delay buffer with multiple taps and feedback. The smaller `GFX Delay` node on the Global EFX bus handles the current delay use cases.

## Signal & ports

| Port | Type | Expected use |
|------|------|--------------|
| 0 | Audio | Input signal |
| 1 | CV | Delay time / modulation |
| Output | Audio | Multi-tap output |

## Parameters

No operator parameters are currently wired because the node is inactive.

## Source

- `include/gdvp_nodes.h` (`GDVP_NODE_MACRO_DELAY`)
- `src/gdvp_dsp_dispatch.c` (NULL processor)
- `gdvp-core-dsp/gdvp/docs/ADR/ADR-002-gfx-effect-nodes.md`

## Notes

Use `GFX Delay` for echo, chorus, and flanger effects. Macro Delay is reserved for future expansion when per-voice or long-form delay lines are required.

## License

Copyright François-Xavier Briollais. All rights reserved.
