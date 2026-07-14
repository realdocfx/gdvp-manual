# Editing the manual in Obsidian

This repository **is** the manual's single source of truth. Editing it in Obsidian
just means opening a git clone of it as a vault and letting the **Obsidian Git**
plugin keep it synced with everyone else (the IDE, the server CMS, the wiki).
Your edits flow to the live site and the wiki automatically; other people's edits
flow to you. No copy-paste, no "final_v2" files.

## One-time setup

1. **Clone the repo** somewhere local:
   ```
   git clone git@github.com:realdocfx/gdvp-manual.git
   ```
   (Or use GitHub Desktop if you prefer a UI.)
2. **Open it as a vault**: Obsidian → *Open folder as vault* → pick the cloned folder.
   Trust the folder when asked.
3. **Install the Git plugin**: Settings → *Community plugins* → *Browse* →
   search **"Git"** (by Vinzent) → *Install* → *Enable*.
4. **Configure it for safe multi-writer sync** (Settings → *Git*):
   - **Vault backup interval (minutes): `10`** — auto commit-and-push your changes.
   - **Auto pull interval (minutes): `10`** — pull everyone else's changes.
   - **Pull updates on startup: `on`**.
   - **Push on backup: `on`**.
   - **Pull before push / rebase: `on`** — this is the important one. It replays
     your edits on top of the latest instead of clashing (see below).

## How conflicts are handled (so nothing is ever lost)

Everyone edits at once, and git reconciles it. When you save, the plugin pulls the
latest first, replays your change on top (rebase), then pushes. If two people edited
**different** parts of a page, both changes are kept automatically. If two people
edited the **same lines**, git pauses on a conflict — Obsidian Git surfaces it, and
you pick the right text. The rule the whole team follows: **your change is never
silently discarded, and you never silently discard someone else's.** Full detail is
in [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## House rules that keep syncing painless

- **Small, frequent saves beat big rewrites** — small edits to different sections
  merge cleanly; sweeping rewrites of a whole page are what cause conflicts.
- **One topic per file**, kept where it lives now (node pages under `nodes/`).
- **Links**: use Obsidian's normal `[text](page.md)` relative links — they resolve
  the same on the website, the wiki, and in the vault.
- **Don't rename or move many files at once** without a heads-up — renames are the
  one thing that reconciles poorly across surfaces.
- The plugin ignores your personal Obsidian layout/state (that's handled by
  `.gitignore`), so your workspace never fights anyone else's.
