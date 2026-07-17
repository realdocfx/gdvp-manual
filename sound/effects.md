# 5 · Effects & the Global EFX Bus

[← Node Reference](../nodes/README.md) · [Manual index](../README.md) · Next: [Parameters →](parameters.md)

GDVP has two distinct places effects can live, and one of them is largely dormant on the current
build. This chapter explains both honestly so you know what actually processes sound.

---

## 5.1 Two domains: per-voice vs. master

- **Per-voice (local domain).** Nodes inside a patch run once *per sounding voice*. Filtering,
  amplitude, panning and (designed) per-voice GFX happen here. Ten notes = ten independent copies.
- **Master domain (Global EFX bus).** A single, **monophonic** chain that processes the *summed*
  output of all voices. This is the right place for reverb and delay — you want one shared room,
  not one per note. The VAM reserves a dedicated EFX node pool for it (`efx_pool[8]`,
  `efx_active_plan`, with its own SPSC staging), flagged `GDVP_NODE_FLAG_MASTER_DOMAIN`. Source:
  `gdvp_vam_elastic_t` in `gdvp_voice_manager.h`.

The design intent: spatial acoustics (reverb/delay/diffusion) on the master bus; tone-shaping
(filter, saturation) per voice.

---

## 5.2 The GFX family (active effects)

The [GFX nodes](../nodes/gfx.md) are the in-graph effects engine — delay, FDN reverb, all-pass
phaser/diffuser, nonlinear gain (sat/fold/µ-law/ring), envelope-follower dynamics, and a
universal parameter modulator. They're built on a small set of reusable primitives ("G×T
decomposition") so many named effects share a few DSP cells.

> ## ✅ Status: the GFX family is fully wired
>
> Every GFX slot in `gdvp_node_processors[]` and `gdvp_node_updaters[]` is now populated. The
> voice executor runs them on the **Global EFX Bus** (master domain, post-mix, monophonic) so
> spatial acoustics and global modulation are rendered as designed. The `master_bus` node type
> remains reserved/inactive; master fold-down and Global EFX scheduling are handled by the
> `gdvp_dsp_iron_ceiling` pipeline.
>
> Full per-node design detail is on the [GFX page](../nodes/gfx.md).

---

## 5.3 What actually shapes sound today

Working, audible processing on the current build:

| Effect | Where | How |
|---|---|---|
| **Saturation / soft-clip** | [VCA](../nodes/vca.md) | tanh LUT on the amp output (`saturation_enabled`) |
| **Filter drive** | [Filter](../nodes/filter.md) | pre-gain into the filter saturation stage |
| **Filter sweeps / wah** | [LFO](../nodes/lfo.md) or [Envelope](../nodes/envelope.md) → filter port 1 | modulate cutoff |
| **Vibrato / PWM** | [LFO](../nodes/lfo.md) → oscillator | modulate pitch / pulse width |
| **Tremolo / auto-pan** | [LFO](../nodes/lfo.md) → VCA / Panner | modulate gain / pan |
| **Noise & texture** | [Exciter](../nodes/exciter.md) | colored noise, dust, S&H |
| **Strum / echo (voices)** | [DELAY voice mode](../concepts/performance.md#strum--delay-allocation) | staggered-onset voices — *not* a delay line, but it works |
| **Stereo width (per voice)** | [Panner](../nodes/panner.md) | constant-power placement |

So while the dedicated reverb/delay/phaser nodes are dormant, you can still build expressive,
moving, saturated, stereo patches today using modulation routing and the VCA/filter nonlinearities.

---

[← Node Reference](../nodes/README.md) · [Manual index](../README.md) · Next: [Parameters →](parameters.md)
