# Contributing to the GDVP Manual

This repository is the **absolute single source of truth (SSOT)** for the GDVP user
manual. It is edited from several surfaces at once — the maintainer's IDE, the author's
Obsidian vault, the GitHub Wiki, and the in-app server CMS (`/admin/manual`) — and every
consumer (the public `gdvp.net/manual` pages, the gated MkDocs Knowledge Base, and future
SDL2 / API / B2B integrations) is a **derived mirror** of what lives here. Nothing is
canonical except `main` in this repo.

## The consensus model (why edits never collide destructively)

Git itself is the consensus layer. There is no central lock; instead every editing surface
is a **bidirectional git client**, and GitHub's refusal of non-fast-forward pushes is the
single atomic arbiter that linearizes concurrent writes:

- **Before pushing, always `git pull --rebase`.** Replay your change on top of the current
  `main`, then push. If the push is rejected (someone landed first), rebase again and retry.
  Automated writers (CMS, Obsidian's git plugin, the wiki bridge) do this in a bounded retry
  loop; humans do it by habit.
- **Markdown merges by hunk.** Independent edits to different sections auto-merge. A genuine
  conflict on the same lines is **never** resolved by overwriting — open a PR or an issue and
  reconcile by hand. No edit is silently lost.
- **Automated commits are marked.** The wiki bridge and CMS tag their commits with a distinct
  author and `[skip-ci]` so the sync bridges never echo each other into a loop.

The actors here are cooperative, not adversarial, so this is the practical
"Byzantine-generals equivalent" — strong eventual consistency with no lost updates, without
the machinery of true Byzantine fault tolerance.

## Editing surfaces

| Surface | How it syncs |
|---------|--------------|
| IDE (maintainer) | Submodule / clone; ordinary `git pull --rebase` → `git push`. |
| Obsidian (author) | Vault = a clone of this repo; the `obsidian-git` plugin auto pull-commit-pushes. |
| GitHub Wiki | Bidirectional reconciler Action mirrors `main` ⇄ `gdvp-manual.wiki`. |
| Server CMS | `/admin/manual`, gated by `CAP_EDIT_MANUAL`; commits **and pushes** here. |

## House rules

- One document per file, `.md`, kebab-case names; node reference pages live under `nodes/`.
- Keep changes small and section-scoped — small hunks merge cleanly, large rewrites conflict.
- Do not commit per-user Obsidian state (see `.gitignore`).
- Prefer relative links between pages so every mirror (web, wiki, KB) resolves them.
