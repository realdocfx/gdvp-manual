# GDVP — Evidence Register

The public companion to the white paper [*The Determinism Dividend*](https://gdvp.net/engineering). The paper claims gates rather than adjectives; this file is where those gates are written down, verbatim, with identifiers an auditor can match.

- **Reconciled against:** engine `a4654a0` on **2026-07-19**
- **Engine repository:** `realdocfx/gdvp-core-dsp` (private — see *Auditability* below)
- **Generated**, not hand-written: emitted from `whitepaper_evidence.py` by `tools/gen_evidence_dossier.py`, so this register and the published page cannot disagree.

> This register is kept in a **public git repository on purpose.** A claim on a web page can be edited silently; a claim in git carries an immutable, timestamped history. If a verdict below ever changed, the diff would say so.

---

## A. Constraint enforcement

The prohibitions, quoted as the machine states them. Each excerpt is the literal enforcement text at the reconciled commit — not a paraphrase.

### §2 CR-001 — No runtime floating point: the compiler is denied the FPU registers.

**Verdict:** `PASS` · **Locus:** engine · .github/workflows/engine-ci.yml — “CR-001 Hard Gate: all engine TUs”

```
CR001_CFLAGS="-std=c11 -Wall -Wextra -Werror -pedantic \
  -Werror=float-conversion -Werror=double-promotion -Werror=float-equal \
  -mgeneral-regs-only ..."
```

*Every engine translation unit is compiled through this gate; a float cannot be emitted.*

### §2 CR-001 — Exactly two Airlock translation units are exempt, and the gate names them.

**Verdict:** `PASS` · **Locus:** engine · engine-ci.yml, same step

```
# Airlock TUs exempt from CR-001 (float-to-fixed boundary by design)
EXEMPT="gdvp_ui_controller.c|gdvp_client_api.c"
```

*The paper says “the gate lists them by name.” It does — these two, and no others.*

### §2 CR-002 — Node slots are exactly 32 bytes, enforced at compile time.

**Verdict:** `PASS` · **Locus:** engine · gdvp/include/gdvp_nodes.h:629–630

```
_Static_assert(sizeof(gdvp_node_t) == 32,
               "CR-002 FATAL: Polymorphic node must be exactly 32 bytes");
_Static_assert(alignof(gdvp_node_t) == 32,
               "CR-002 FATAL: Polymorphic node lacks 32-byte alignment");
```

*Not a convention — a translation failure if violated.*

### §2 CR-002 — One static arena of 900 KB; capacities are specification.

**Verdict:** `PASS` · **Locus:** engine · gdvp/include/gdvp_client_api.h:109–111

```
/* Total: 460,800 16-bit words = 900KB */
#define GDVP_CLIENT_ARENA_SIZE_WORDS 460800U
```

*460 800 × 2 bytes = 921 600 B = 900 KiB. The arithmetic is checkable from the constant.*

### §3.2 — ThreadSanitizer is a blocking gate, with the flip's commit and green-run recorded in the gate file.

**Verdict:** `PASS` · **Locus:** engine · engine-ci.yml — job `tsan`

```
# F-06 flipped to blocking 2026-07-15 (run 29423142308, commit 3d736e4): the
# full race register S1 + R1..R5 is closed (atomic node flags byte + patch-load
# is_active barrier + block_gen grace + EFX Dekker). Any new data race now blocks.
tsan:
  name: Linux ThreadSanitizer (blocking gate)
  continue-on-error: false
```

*The paper's claim about recorded identifiers is literally true: run 29423142308, commit 3d736e4.*

### §4 — A coverage floor is enforced at the measured value, and the number is published unglamorously.

**Verdict:** `PASS` · **Locus:** engine · engine-ci.yml — “Coverage report (blocking floor gate)”

```
# enforces COVERAGE_FLOOR (82; measured 82.1%)
```

*82 % lines is the enforced floor (58 -> 59 -> 76 -> 81 -> 82 across 2026-07-20/21). Functions 86.1 %, branches 66.3 %. The paper states all three; the gate is where the line floor lives.*

### §4 — Reproducible builds verified by hash identity across independent runners.

**Verdict:** `PASS` · **Locus:** engine · .github/workflows/reproducible-build.yml

```
#   1. Same-runner determinism: two clean builds on ONE runner must hash-match
#   2. Cross-runner determinism: a second, independent runner rebuilds the same
```

*Nightly. Both tiers, not just the cheap one.*

### §6 — A behavioural contract of eleven measured clauses.

**Verdict:** `PASS` · **Locus:** orchestrator · docs/GDVP-PVA-001.md §3.2 “The Prosumer Covenant”

```
C1 Determinism · C2 True black · C3 No pops · C4 Poison values · C5 Latency truth
C6 Frontier fidelity · C7 Deadline · C8 Honest bypass · C9 Zipper-free
C10 State round-trip · C11 Resurrection

C3: transition energy <= -72 dBFS RMS per 5 ms window; no single-sample
    step > -48 dBFS outside musical content
```

*Eleven clauses, specified and numbered. Measurement status is in the GAPS table.*

### §6 — Binaries are signed over the hash of the validation dossier; no green dossier, no artifact.

**Verdict:** `PASS` · **Locus:** orchestrator · docs/GDVP-PVA-001.md §1

```
The release signer signs over H(binary + dossier-manifest); absent a complete
green dossier for that exact SHA, the fail-closed `-signed` contract refuses,
and no installable artifact exists.
```

*Specified as the release mechanism's type system.*

---

## B. Gate ledger

Workflow state at the reconciliation date. Run numbers are on the private engine repository and are immutable — they cannot be retro-fabricated without rewriting history.

| Gate | Trigger | Run | Commit | Verdict |
|---|---|---|---|---|
| Engine CI — MISRA/cppcheck (blocking), CR-001, unit suite, sanitizers | push + nightly 00:00 UTC | `29688513786` | `a4654a0` | `PASS` |
| Linux ThreadSanitizer (blocking gate) | push (engine paths) + nightly | `29688513786` | `a4654a0` | `PASS` |
| Audio determinism corpus (C1 — 14 patches, all node families) | push (engine paths) + nightly | `29688513786` | `a4654a0` | `PASS` |
| Coverage report (blocking floor gate, ≥ 81 %) | push (engine paths) + nightly | `29688513786` | `a4654a0` | `PASS` |
| Continuous Fuzzing (libFuzzer, GVP parser) + guard-page crash replay | nightly 00:00 UTC + on demand | `29668340654` | `b190494` | `PASS` |
| Reproducible Build (same-runner + cross-runner hash identity) | nightly 04:00 UTC | `29676582069` | `b190494` | `PASS` |
| Engine API Docs (Doxygen build + warning ratchet) | push (engine/doc paths) | `29643700381` | `b190494` | `PASS` |
| Secret Scan (Gitleaks) | push | `29643700376` | `b190494` | `PASS` |
| Engine Timing Gate (Tier 2) — WCET on pinned bare metal | nightly 03:00 UTC | `29675514003` | `b190494` | `GAP` |

---

## C. Declared, not yet evidenced

The uncomfortable table, set in the same type as the rest. A register that records only passes is marketing.

### §2 CR-003 / §4 / §7 — “WCET ≤ 1.3 ms, gated on pinned bare metal, published with artifacts”

**Status:** Gate exists; not currently producing evidence.

The Tier-2 timing job is guarded by `if: vars.BARE_METAL_RUNNER == 'online'` on a `[self-hosted, bare-metal]` runner. With no bare-metal runner online it reports `skipped`, which is the correct behaviour — timing measured on a shared cloud runner would be astrology, as the paper says — but it means the 1.3 ms figure is NOT backed by a live run in this register. It is a design target and a historical bench result, not a currently-green gate. Treat it as unevidenced until the runner is online.

### §6 — “eleven measured clauses”

**Status:** Specified in full; measurement partial.

GDVP-PVA-001 §3.1 records V2 Covenant as “Partially exists (null test, toxic payload, pop-safety); this spec completes it.” C1 (determinism) is gated in CI today. The remaining clauses are specified and numbered but not all continuously measured. “Published contract” is accurate; “all eleven measured on every release” is not yet.

### §6 / §7 — plugin format conformance

**Status:** Deferred by decision.

GDVP-PVA-001 §3.1 V1 records “pluginval = F-18 flip; SDK validator currently OFF in build — turn ON.” The out-of-process proxy architecture produces expected-fail results under some strictness levels, so the flip to blocking is deliberately pending rather than quietly green.

### Auditability of this register

**Status:** Access-bounded.

The engine and infrastructure repositories are private. The excerpts above are verbatim and the run numbers immutable, but a public reader cannot open them. Full artefacts — gate logs, MISRA report, coverage, hash manifest, corpus renders — are released to diligence under NDA. We state this rather than implying public verifiability.

---

## D. What you can inspect today

The engine and infrastructure repositories are private, so the gate logs above are not publicly clickable. These are:

- [`gdvp-manual`](https://github.com/realdocfx/gdvp-manual) — The operator's manual SSOT
- [The licence](https://gdvp.net/legal) — the agreement in force, published on the site

Full artefacts — gate logs, MISRA report with enumerated deviations, coverage against the declared floor, reproducible-build hash manifest, corpus renders — are released to diligence under NDA. We state that rather than implying a public verifiability we do not offer.

---

*General Digital Voicing Program · the pipeline, not this register, is authoritative. Technical contact: contact@gdvp.net*
