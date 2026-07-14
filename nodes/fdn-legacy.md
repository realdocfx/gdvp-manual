# FDN (Legacy Slot)

**Author:** François-Xavier Briollais  
**Copyright:** All rights reserved.

**Node type:** `GDVP_NODE_FDN`  
**Status:** ⛔ Inactive (NULL processor)  
**Version:** 1.4.0

## What it is

This node slot was originally reserved for a per-voice Feedback Delay Network reverb. The current reverb implementation has moved to the `GFX FDN` node on the Global EFX bus, leaving this slot inactive.

## Signal & ports

| Port | Type | Expected use |
|------|------|--------------|
| 0 | Audio | Input signal |
| 1 | CV | Reverb amount / decay |
| Output | Audio | Reverberated output |

## Parameters

No operator parameters are currently wired because the node is inactive.

## Source

- `include/gdvp_nodes.h` (`GDVP_NODE_FDN`)
- `src/gdvp_dsp_dispatch.c` (NULL processor)
- `gdvp-core-dsp/gdvp/docs/ADR/ADR-002-gfx-effect-nodes.md`

## Notes

Use the `GFX FDN` node for feedback-delay-network reverb. This legacy slot is preserved for API compatibility and may be reused in a future architecture revision.

## License

Copyright François-Xavier Briollais. All rights reserved.
