# Feedback

**Author:** François-Xavier Briollais  
**Copyright:** All rights reserved.

**Node type:** `GDVP_NODE_FEEDBACK`  
**Status:** ⛔ Inactive (NULL processor)  
**Version:** 1.4.0

## What it is

The Feedback node was intended to provide an explicit, controllable feedback path around filters, delays, and distortion nodes. The DAG compiler currently resolves implicit feedback loops with internal delays instead.

## Signal & ports

| Port | Type | Expected use |
|------|------|--------------|
| 0 | Audio | Input signal |
| 1 | CV | Feedback amount (0–16383) |
| Output | Audio | Output with feedback applied |

## Parameters

No operator parameters are currently wired because the node is inactive.

## Source

- `include/gdvp_nodes.h` (`GDVP_NODE_FEEDBACK`)
- `src/gdvp_dsp_dispatch.c` (NULL processor)
- `gdvp-core-dsp/gdvp/docs/DAG_COMPILER.md`

## Notes

Patches that need feedback should rely on the `Filter` node’s internal resonance and the `Delay` / `GFX Delay` nodes with low feedback levels. Explicit feedback routing is a planned future enhancement.

## License

Copyright François-Xavier Briollais. All rights reserved.
