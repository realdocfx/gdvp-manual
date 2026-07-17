#!/usr/bin/env python3
"""Cross-surface link normaliser for the GDVP manual SSOT.

The manual is edited across surfaces that resolve links differently — the public
``/manual`` and MkDocs use relative ``.md`` links; the GitHub Wiki flattens pages
to their basename and its web editor *rewrites* links (turning ``[X](#A)`` into a
mangled ``[[X](…/wiki/…/_edit#A)](#A)`` that then reconciles back and poisons the
SSOT). This tool keeps every surface honest:

  repair   Undo the wiki-editor mangling and drop stray ``…/wiki/…/_edit`` URLs.
           Lower-case anchor fragments so they match the auto-generated slugs
           every renderer (python-markdown ``toc``, MkDocs, GitHub) emits.
  to-ssot  reconcile leg (wiki → SSOT): ``repair`` — sanitise incoming wiki edits.
  to-wiki  publish leg (SSOT → wiki): rewrite ``dir/page.md#a`` links to the wiki's
           flat ``page#a`` form and strip ``{#explicit}`` heading anchors (GitHub
           wikis auto-anchor headings; the braces would render literally).

Operates in place on a single ``--file`` or every ``*.md`` under ``--dir``.
Idempotent: running any mode twice is a no-op.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

# [[TEXT](http…url…)](TARGET)  →  [TEXT](TARGET)   — the wiki-editor mangling.
_MANGLE = re.compile(r"\[\[([^\]]+)\]\(https?://[^)]+\)\]\(([^)]+)\)")
# [TEXT](https://github.com/…/wiki/…#ANCHOR)  →  [TEXT](#ANCHOR)   — stray wiki URL.
_WIKI_URL = re.compile(
    r"\[([^\]]+)\]\(https?://github\.com/[^)]*?/wiki/[^)]*?#([^)]+)\)"
)
# A link target's #fragment (in `](#frag)` or `](path#frag)`).
_FRAG = re.compile(r"(\]\([^)#]*#)([A-Za-z0-9_.-]+)(\))")
# A relative .md link target (not http/anchor/absolute): `](dir/page.md#a)`.
_MD_LINK = re.compile(r"\]\((?!https?://|/|#|mailto:)([^)]+?)\.md(#[^)]+)?\)")
# An explicit heading anchor: `## Title {#id}` → group 1 is the heading text.
_HEAD_ANCHOR = re.compile(r"^(#{1,6}\s+.*?)\s*\{#[^}]+\}\s*$")


def _lower_frag(text: str) -> str:
    return _FRAG.sub(lambda m: m.group(1) + m.group(2).lower() + m.group(3), text)


def repair(text: str) -> str:
    text = _MANGLE.sub(r"[\1](\2)", text)
    text = _WIKI_URL.sub(r"[\1](#\2)", text)
    return _lower_frag(text)


def to_ssot(text: str) -> str:
    return repair(text)


def _md_to_basename(m: re.Match) -> str:
    target, anchor = m.group(1), m.group(2) or ""
    base = target.rsplit("/", 1)[-1]  # flat wiki page name
    return f"]({base}{anchor.lower()})"


def to_wiki(text: str) -> str:
    text = repair(text)
    out = []
    for line in text.split("\n"):
        line = _HEAD_ANCHOR.sub(r"\1", line)  # drop {#id} — wiki auto-anchors
        out.append(line)
    text = "\n".join(out)
    return _MD_LINK.sub(_md_to_basename, text)


_MODES = {"repair": repair, "to-ssot": to_ssot, "to-wiki": to_wiki}


def _process(path: Path, fn) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    fixed = fn(original)
    if fixed != original:
        path.write_text(fixed, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", required=True, choices=sorted(_MODES))
    ap.add_argument("--file", help="a single markdown file")
    ap.add_argument("--dir", help="process every *.md under this directory")
    args = ap.parse_args()
    fn = _MODES[args.mode]

    if args.file:
        targets = [Path(args.file)]
    elif args.dir:
        targets = [p for p in Path(args.dir).rglob("*.md") if ".git" not in p.parts]
    else:
        ap.error("one of --file / --dir is required")

    changed = 0
    for p in targets:
        if _process(p, fn):
            changed += 1
            print(f"linkfix[{args.mode}]: {p}")
    print(f"linkfix[{args.mode}]: {changed} file(s) changed of {len(targets)}.")


if __name__ == "__main__":
    main()
