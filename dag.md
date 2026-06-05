# 2 · The Node Graph (DAG)

[← Global Concepts](concepts.md) · [Manual index](README.md) · Next: [Performance & Expression →](performance.md)

A GDVP patch is not a fixed signal path with a few switches — it is a **directed acyclic
graph** (DAG) of DSP nodes that you wire freely. This chapter explains how that graph works,
because once you understand ports and compilation, programming any node becomes the same act.

---

## 2.1 Nodes, ports and edges

A patch is **nodes** + **edges**.

- A **node** is one DSP block: an oscillator, a filter, an envelope, a VCA, and so on. Every
  node is exactly 32 bytes internally (a hard architectural invariant) and carries its own
  parameters and state. The full catalogue is the [Node Reference](nodes/README.md).
- An **edge** is a wire from one node's **output port** to another node's **input port**.
  In the `.gvp` patch file an edge is `{src, dst, src_port, dst_port}` — see
  [Patches](patches.md#routing).

### Port conventions

Ports are small integers. The convention that runs through every stock patch:

| Port | Meaning | Typical use |
|---|---|---|
| **0** | Primary **audio** path | osc → filter → vca → panner |
| **1** | **Control / gate** input | envelope → filter **port 1** (cutoff modulation); envelope → vca **port 1** (amplitude/gate) |

So a classic subtractive voice reads, in edges:

```
osc(0) ──0──▶ filter(0)         ; audio into the filter
env(0) ──1──▶ filter(0)         ; envelope modulates filter cutoff
filter(0) ──0──▶ vca(0)          ; filtered audio into the amp
env2(0) ──1──▶ vca(0)            ; envelope shapes amplitude (the "gate")
vca(0) ──0──▶ panner(0)          ; amp into stereo placement
```

That is essentially the `acid_squelch` example patch ([see the example library](patches.md#library)).
The node *number* (`id`) is arbitrary and need not be ordered; the **edges** define the
topology, and the compiler sorts execution order for you.

---

## 2.2 Why it must be acyclic

The graph is **acyclic** — no node may feed back into itself through the graph. This is what
lets the engine compute a single, stable execution order every block with bounded cost. Genuine
feedback (delay lines, FDN reverb) is provided by **dedicated nodes** that hold their own
internal delay memory rather than by looping an edge back; see the
[GFX effect nodes](nodes/gfx.md) and [Effects](effects.md). If you author a `.gvp` with a cycle,
the parser/compiler will reject it ([patch errors](patches.md#errors)).

---

## 2.3 Compilation: from your wiring to the execution plan

When a patch loads, the engine doesn't run your edges directly. It **compiles** them:

1. **Parse** the `.gvp` into an abstract topology (the AST). Source: `gdvp_gvp_parser.c`.
2. **Topologically sort** the nodes with Kahn's algorithm so every node runs *after* the nodes
   that feed it. Source: `gdvp_dag_compiler.c`. See [Glossary: Kahn sort](glossary.md#kahn).
3. **Auto-inject** structural helpers where needed (below).
4. Emit an **execution plan** (`execution_order[]`) that the voice executor walks in order.

Because of this, two things are true that surprise newcomers:

- **Node order in the file is irrelevant.** Put nodes in any order; wiring decides everything.
- **The compiled graph can contain nodes you didn't draw** — see auto-injection next.

### Auto-injected nodes

The compiler silently inserts helper nodes so you don't have to manage plumbing:

- **Mixer** — when more than one edge fans **into** the same input port (fan-in > 1), the
  compiler inserts a [Mixer node](nodes/mixer.md) to sum them. You hear this as "I wired three
  oscillators into one filter and it just worked."
- **Up/Down-samplers** — when a node runs oversampled (2×) but its neighbours don't, the
  compiler inserts [polyphase up/down-samplers](nodes/oversampling.md) at the rate boundary so
  the conversion is band-limited rather than naive.

The patch stores **two edge lists** as a result: your original *user edges* (what you drew, and
what gets saved back) and the *cached post-compilation edges* (including injected MIX/UP/DN),
which the [front panel](gui.md) renders so the picture matches what actually executes. Source:
`gdvp_elastic_part_t` fields `user_edge_*` and `cached_edge_*` in `gdvp_voice_manager.h`.

---

## 2.4 Per-voice instantiation

The compiled plan describes **one voice**. When the Part sounds notes, each voice gets its own
provisioned copy of every node in the plan (drawn from the 8192-node global pool). Per-voice
state — oscillator phase, filter integrators, envelope stage — is therefore private. See
[Global Concepts §1.1](concepts.md#parts-voices-nodes--who-owns-what).

The hard ceiling is **64 nodes per patch graph** (`GDVP_MAX_PATCH_NODES`). The compiler parses
into a 256-node sandbox first, then sorts down into the dense staging pool; exceeding the node
or edge budget is a load-time error ([patch errors](patches.md#errors)).

---

## 2.5 Live editing and the Airlock

Editing topology while audio is running is dangerous — you're changing the structure the audio
thread is mid-way through executing. GDVP handles this with a transactional swap:

- You edit the **staging** copy (host side).
- A new plan is compiled into `next_plan`.
- An atomic `pending_topology_swap` flag tells the audio thread to switch to it **at a block
  boundary**, flushing voices cleanly so no orphaned envelope/VCA state survives the swap.

This Producer↔Consumer hand-off is the **Airlock**. You never operate it directly; it is why
re-patching doesn't click or crash. Source: `gdvp_voice_manager.c`
(`gdvp_vam_flush_part_voices`, the `_Atomic` swap flags), discussed in
`gdvp/docs/THREAD_SEGREGATION.md`. See also [Glossary: Airlock](glossary.md#airlock).

---

[← The Node Graph](dag.md) · [Manual index](README.md) · Next: [Performance & Expression →](performance.md)
