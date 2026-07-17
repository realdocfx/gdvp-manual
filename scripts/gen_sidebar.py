#!/usr/bin/env python3
"""Generate the GitHub Wiki sidebar (``_Sidebar.md``) from ``SUMMARY.md`` — the
manual's single navigation SSOT.

Every surface (public ``/manual``, the gated Knowledge Base, the CMS editor and
this wiki) derives its navigation from ``SUMMARY.md``. This script is the wiki's
projection of it, run by the wiki-publish workflow on every push to main.

GitHub Wiki URL model (verified against the live wiki, not assumed):

* Wiki pages are addressed by their **basename**, flattened — a page mirrored to
  ``nodes/oscillator.md`` is served at ``/wiki/oscillator`` (``/wiki/nodes/oscillator``
  is a 404). So every link target is ``<repo>/wiki/<basename>``.
* The root ``README.md`` is mirrored as ``Home`` (``/wiki/Home``).
* The seven section ``README.md`` landings all flatten to the same ``/wiki/README``
  (a collision), so they are NOT linkable — they render as plain section labels.
* ``_Sidebar.md`` renders on every page and browsers resolve relative links against
  the current page URL, so links are **root-relative absolute** (``/owner/name/wiki/…``)
  to resolve correctly from any nested page.

Usage:
    gen_sidebar.py --summary SUMMARY.md --out _Sidebar.md --repo owner/name
"""

from __future__ import annotations

import argparse
import re


def parse_summary(text: str):
    """Return (intro_entry, parts) mirroring the server's ``_summary_nav``.

    ``intro_entry`` is the pre-heading landing link (``[Introduction](README.md)``);
    ``parts`` is ``[{"title", "entries": [{"title", "path", "depth"}]}]``.
    """
    intro = None
    parts: list[dict] = []
    cur: dict | None = None
    for line in text.splitlines():
        head = re.match(r"^##\s+(.+?)\s*$", line)
        if head:
            cur = {"title": head.group(1), "entries": []}
            parts.append(cur)
            continue
        item = re.match(r"^(\s*)-\s+\[([^\]]+)\]\(([^)]+)\)", line)
        if item and item.group(3).endswith(".md"):
            entry = {
                "title": item.group(2),
                "path": item.group(3),
                "depth": len(item.group(1)) // 2,
            }
            if cur is None:
                intro = intro or entry
            else:
                cur["entries"].append(entry)
            continue
        if cur is None and intro is None:
            bare = re.match(r"^\[([^\]]+)\]\(([^)]+\.md)\)\s*$", line.strip())
            if bare:
                intro = {"title": bare.group(1), "path": bare.group(2), "depth": 0}
    return intro, parts


def _basename(path: str) -> str:
    leaf = path.rsplit("/", 1)[-1]
    return leaf[:-3] if leaf.endswith(".md") else leaf


def _is_landing(path: str) -> bool:
    """A section/sub-section landing — a ``README.md`` in a folder. These collide
    at ``/wiki/README`` so they render as labels, not links."""
    return _basename(path).lower() == "readme"


def _wiki_link(repo: str, title: str, path: str) -> str:
    if path == "README.md":  # root landing → the wiki Home page
        return f"[{title}](/{repo}/wiki/Home)"
    return f"[{title}](/{repo}/wiki/{_basename(path)})"


def render(intro, parts, repo: str) -> str:
    out: list[str] = [
        "<!-- Generated from SUMMARY.md by scripts/gen_sidebar.py — do not edit by hand. -->",
    ]
    home = intro["path"] if intro else "README.md"
    home_title = intro["title"] if intro else "Home"
    out.append(f"### {_wiki_link(repo, home_title, home)}")
    out.append("")

    for part in parts:
        entries = part["entries"]
        if not entries:
            continue
        out.append(f"**{part['title']}**")
        out.append("")
        for e in entries:
            if e["depth"] == 0 and _is_landing(e["path"]):
                # The section landing is already the bold header above — skip.
                continue
            indent = "  " * max(0, e["depth"] - 1)
            if _is_landing(e["path"]):
                # Sub-section landing (e.g. Node Reference → nodes/README): a
                # non-linkable group label (README pages collide on the wiki).
                out.append(f"{indent}- **{e['title']}**")
            else:
                out.append(f"{indent}- {_wiki_link(repo, e['title'], e['path'])}")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--summary", required=True, help="path to SUMMARY.md")
    ap.add_argument("--out", required=True, help="path to write _Sidebar.md")
    ap.add_argument("--repo", required=True, help="owner/name for absolute wiki links")
    args = ap.parse_args()

    with open(args.summary, encoding="utf-8") as f:
        intro, parts = parse_summary(f.read())
    md = render(intro, parts, args.repo)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(f"Wrote {args.out} from {args.summary} ({len(parts)} sections).")


if __name__ == "__main__":
    main()
