# Master Bus

**Author:** François-Xavier Briollais  
**Copyright:** All rights reserved.

**Node type:** `GDVP_NODE_MASTER_BUS`  
**Status:** ⛔ Inactive (NULL processor)  
**Version:** 1.4.0

## What it is

The Master Bus node was intended to host the final master summing, fold-down, and master-domain effects insertion after the per-voice mixer. In the current build, the master fold-down and Global EFX bus are handled by dedicated code in `gdvp_dsp_iron_ceiling.c` and the GFX effect pipeline, leaving this node slot inactive.

## Signal & ports

| Port | Type | Expected use |
|------|------|--------------|
| 0 | Audio | Multi-channel summed input |
| 1 | CV | Not yet wired |
| Output | Audio | Final stereo output |

## Parameters

No operator parameters are currently wired because the node is inactive.

## Source

- `include/gdvp_nodes.h` (`GDVP_NODE_MASTER_BUS`)
- `src/gdvp_dsp_dispatch.c` (NULL processor)
- `gdvp-core-dsp/gdvp/docs/ADR/ADR-002-gfx-effect-nodes.md`

## Notes

Active patches should route per-voice audio through the `Mixer` and `Panner` nodes. Master-domain effects should use GFX nodes through the Global EFX bus.

## License

Copyright François-Xavier Briollais. All rights reserved.
