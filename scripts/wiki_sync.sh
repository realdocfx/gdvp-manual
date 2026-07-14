#!/usr/bin/env bash
# Content mapping between the SSOT working tree and the GitHub wiki clone.
#
#   root README.md  <->  Home.md          (wiki landing page)
#   every other *.md      mirror 1:1       (including nodes/**)
#
# Never mirrored into the wiki: CONTRIBUTING.md, README (mapped), .github/**,
# scripts/**, and any dotfile/dotdir. Wiki-only special pages (_Sidebar.md,
# _Footer.md) are preserved and never pushed back to the SSOT.
#
# Usage: SSOT=ssot WIKI=wiki bash scripts/wiki_sync.sh {publish|reconcile}
set -euo pipefail
DIR="${1:?publish|reconcile}"
SSOT="${SSOT:-.}"
WIKI="${WIKI:-wiki}"

# repo-management files that must never appear in the wiki
excluded() {
  case "$1" in
    README.md|CONTRIBUTING.md) return 0 ;;        # README maps to Home; CONTRIBUTING is repo-only
    .github/*|scripts/*|docs/*|.*|*/.*) return 0 ;; # workflows, scripts, contributor docs, dotfiles
  esac
  return 1
}

list_md() { ( cd "$1" && find . -name '*.md' -not -path './.git/*' | sed 's|^\./||' ); }

case "$DIR" in
  publish)  # SSOT is authoritative: mirror content, incl. deletions
    list_md "$SSOT" | while read -r f; do
      excluded "$f" && continue
      mkdir -p "$WIKI/$(dirname "$f")"; cp "$SSOT/$f" "$WIKI/$f"
    done
    cp "$SSOT/README.md" "$WIKI/Home.md"
    list_md "$WIKI" | while read -r f; do
      case "$f" in Home.md|_Sidebar.md|_Footer.md) continue ;; esac
      [ -f "$SSOT/$f" ] || rm -f "$WIKI/$f"   # drop pages removed from the SSOT
    done
    ;;
  reconcile)  # wiki edits flow in: add/update only, never delete SSOT files
    list_md "$WIKI" | while read -r f; do
      case "$f" in _Sidebar.md|_Footer.md) continue ;; esac
      if [ "$f" = Home.md ]; then
        cp "$WIKI/Home.md" "$SSOT/README.md"
      else
        excluded "$f" && continue
        mkdir -p "$SSOT/$(dirname "$f")"; cp "$WIKI/$f" "$SSOT/$f"
      fi
    done
    ;;
  *) echo "unknown direction: $DIR" >&2; exit 2 ;;
esac
