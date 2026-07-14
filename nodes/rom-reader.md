# ROM Reader

**Author:** François-Xavier Briollais  
**Copyright:** All rights reserved.

**Node type:** `GDVP_NODE_ROM_READER`  
**Status:** ⛔ Inactive (NULL processor)  
**Version:** 1.4.0

## What it is

The ROM Reader node was planned to stream or trigger data from the `gdvp-data-rom` submodule (WAV tables, multi-samples, or large LUT sections) into a voice graph. It has not been wired into the dispatch table.

## Signal & ports

| Port | Type | Expected use |
|------|------|--------------|
| 0 | Audio | Trigger/gate input |
| 1 | CV | Index or sample-select CV |
| Output | Audio | ROM data output |

## Parameters

No operator parameters are currently wired because the node is inactive.

## Source

- `include/gdvp_nodes.h` (`GDVP_NODE_ROM_READER`)
- `src/gdvp_dsp_dispatch.c` (NULL processor)
- `gdvp-core-dsp/vendor/gdvp-data-rom/README.md`

## Notes

Use the `Oscillator` node with sampled-waveform wave tables for sample-like playback. The ROM Reader may be activated in a future release when multi-sample streaming is needed.

## License

Copyright François-Xavier Briollais. All rights reserved.
