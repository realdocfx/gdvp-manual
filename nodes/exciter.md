# Exciter (Entropy Tap) — `GDVP_NODE_EXCITER` ✅

[← Node Reference](README.md) · [Manual index](../README.md)

A noise / randomness source — but a clever one. The Exciter **generates nothing of its own**; it
taps a single shared noise engine, selects a *color*, a per-voice *read offset* (for
decorrelation across a chord), and a *shaping mode*, then forwards that palette. This gives you
everything from colored audio noise to Geiger-counter dust to Buchla-style stepped voltages.
Source: `gdvp_dsp_exciter.c`, payload `gdvp_node_exciter_t` in `gdvp_nodes.h`.

> **Note on status.** `gdvp_nodes.h` prose lists EXCITER as "PENDING", but it is **wired and
> active** in the live dispatch table (`gdvp_dsp_dispatch.c`) — both its processor and updater are
> registered. It produces sound on the current build.

## Signal & ports

- **Output (port 0):** the generated/shaped entropy signal — route it as an audio source (noise
  layers, percussion excitation) or as a modulation source (random CV).

## Parameters

| Parameter | Param ID | Range | Meaning |
|---|---|---|---|
| **Source mode** | `GDVP_PARAM_EXCITER_SOURCE_MODE` | 0–4 | `0`=Audio noise, `1`=Particle (Poisson dust), `2`=S&H step, `3`=S&H quantized, `4`=S&H smooth |
| **Color** | `GDVP_PARAM_EXCITER_COLOR` | 0–4 | `0`=White, `1`=Pink, `2`=Red, `3`=Blue, `4`=Violet |
| **Rate / density** | `GDVP_PARAM_EXCITER_RATE` | 0–16383 | S&H clock rate, or particle density |
| **Level** | `GDVP_PARAM_EXCITER_LEVEL` | 0–16383 | Output level |
| **Param A** | `GDVP_PARAM_EXCITER_PARAM_A` | 0–16383 | Context-dependent: slew amount \| quantize steps \| dust amplitude |
| **Decorrelation offset** | `GDVP_PARAM_EXCITER_DECORR_OFFSET` | 0–16383 | Per-voice read-phase spacing into the shared ring (see [decorrelation](#decorr)) |
| **Flags** | `GDVP_PARAM_EXCITER_FLAGS` | bitmask | bit0 Bipolar, bit1 Tempo-sync, bit2 Gaussian, bit3 Crush |
| **Crush bits** | `GDVP_PARAM_EXCITER_CRUSH_BITS` | 0–… | Bit-depth reduction mask power (`0` = off) |

## Behaviour notes

### Source families
- **Audio (0):** continuous colored noise — beds, wind, breath, filter excitation.
- **Particle (1):** density-gated Poisson impulses — dust, crackle, Geiger/rain textures. `Param A`
  sets impulse amplitude; **Rate** sets density.
- **S&H step (2):** classic sample-and-hold staircase random voltage.
- **S&H quantized (3):** stepped random snapped to a grid (Buchla 266 flavour); `Param A` = steps.
- **S&H smooth (4):** slew-limited fluctuating random — a "drunk walk" / Wogglebug; `Param A` = slew.

### Color
The five colors are spectral tilts of the shared white source: **White** (flat), **Pink**
(−3 dB/oct), **Red/Brown** (−6 dB/oct), **Blue** (+3), **Violet** (+6). Pink/red are smoother and
darker; blue/violet are brighter and hissier.

### Per-voice decorrelation {#decorr}
Because all exciters tap one shared noise ring, a chord could otherwise sound mono-coherent (every
voice identical). The **decorrelation offset** shifts each voice's read point by
`voice_idx × offset` (clamped to the history window), so each voice reads independent past
samples. Offset `0` across a chord = one unified mono bed; spread offsets = a diffuse,
statistically independent field. The voice index is published to the kernel by the executor just
before dispatch (`gdvp_noise_set_voice_context`), the same pattern the [filter](filter.md#slope)
cascade uses.

### Tempo-sync & crush
With the **tempo-sync** flag, the S&H clock latches on transport ticks from the executor's
`tick_mask` (sample-accurate). The **crush** flag plus `crush_bits` applies bit-depth reduction
for lo-fi/digital grit. **Gaussian** sums two draws for softer noise statistics; **bipolar**
swings the output around zero rather than unipolar.

## Related
- Percussion: pair with a fast [Envelope](envelope.md) and [Filter](filter.md) — see
  `noise_snare`, `metallic_hat`, `vinyl_dust` examples ([library](../patches.md#library)).

---

[← Node Reference](README.md) · [Manual index](../README.md)
