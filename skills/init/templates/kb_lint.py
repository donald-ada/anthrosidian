#!/usr/bin/env python3
"""Structural lint for an anthrosidian knowledge base.

Checks only machine-decidable protocol rules (see AGENTS.md). Content judgment —
what to store, which side of a contradiction is right, whether a note is atomic —
is the agent's job, never lint's.

Usage: python3 scripts/kb_lint.py [kb-root]   (default: cwd)
Exit codes: 0 = clean or warnings only, 1 = errors present.
Output: one "ERROR path: message" / "WARN  path: message" line per finding.
"""
import re
import sys
from pathlib import Path

TYPES = {"fact", "procedure", "pitfall", "decision", "entity", "reference"}
STATUSES = {"active", "superseded", "deprecated"}
CONFIDENCES = {"verified", "reported", "inferred"}
REQUIRED_KEYS = ["type", "status", "created", "updated", "confidence", "source", "keywords"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
EPISODE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")

errors, warnings = [], []


def err(path, msg):
    errors.append(f"ERROR {path}: {msg}")


def warn(path, msg):
    warnings.append(f"WARN  {path}: {msg}")


def parse_frontmatter(lines):
    """Minimal YAML-ish frontmatter parser. Returns dict or None if malformed."""
    if not lines or lines[0].strip() != "---":
        return None
    fm, key = {}, None
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            fm[key] = val
        elif line.strip().startswith("- ") and key:
            fm[key] = (fm.get(key, "") + ", " + line.strip()[2:]).strip(", ")
    return None  # no closing ---


def lint_note(kb, note, rel):
    lines = note.read_text(encoding="utf-8").splitlines()
    fm = parse_frontmatter(lines)
    if fm is None:
        err(rel, "missing or unterminated frontmatter block")
        return None
    for k in REQUIRED_KEYS:
        if not fm.get(k):
            err(rel, f"missing frontmatter key: {k}")
    if fm.get("type") and fm["type"] not in TYPES:
        err(rel, f"invalid type: {fm['type']!r} (allowed: {', '.join(sorted(TYPES))})")
    if fm.get("status") and fm["status"] not in STATUSES:
        err(rel, f"invalid status: {fm['status']!r} (allowed: {', '.join(sorted(STATUSES))})")
    if fm.get("confidence") and fm["confidence"] not in CONFIDENCES:
        err(rel, f"invalid confidence: {fm['confidence']!r}")
    for k in ("created", "updated"):
        if fm.get(k) and not DATE_RE.match(fm[k]):
            err(rel, f"{k} is not YYYY-MM-DD: {fm[k]!r}")
    kw = fm.get("keywords", "").strip("[] ")
    if "keywords" in fm and not kw:
        err(rel, "keywords list is empty")
    if fm.get("status") == "superseded":
        target = fm.get("superseded_by", "").strip()
        if not target:
            err(rel, "status is superseded but superseded_by is missing")
        elif not (kb / target).is_file():
            err(rel, f"superseded_by target does not exist: {target}")
    n = len(lines)
    if n > 200:
        err(rel, f"note is {n} lines (>200) — split it (protocol target: ≤150)")
    elif n > 150:
        warn(rel, f"note is {n} lines (protocol target: ≤150) — consider splitting")
    # broken relative links
    for m in MD_LINK_RE.finditer("\n".join(lines)):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:")) or not target.endswith(".md"):
            continue
        if "<" in target or ">" in target:
            continue  # placeholder in a format example, not a real link
        if not (note.parent / target).resolve().is_file() and not (kb / target).is_file():
            err(rel, f"broken link: {target}")
    return fm


def main():
    kb = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    if not (kb / "AGENTS.md").is_file():
        print(f"ERROR {kb}: not a knowledge base (AGENTS.md missing)")
        return 1
    index = kb / "index.md"
    if not index.is_file():
        print(f"ERROR {kb}: index.md missing")
        return 1

    index_text = index.read_text(encoding="utf-8")
    index_lines = len(index_text.splitlines())
    if index_lines > 200:
        err("index.md", f"index is {index_lines} lines (>200 hard budget) — apply the overflow rule")
    elif index_lines > 180:
        warn("index.md", f"index is {index_lines} lines — nearing the 200-line budget, apply the overflow rule soon")

    notes_dir = kb / "notes"
    domain_indexes = {}   # domain -> text
    statuses = {}         # rel path -> status
    for note in sorted(notes_dir.rglob("*.md")) if notes_dir.is_dir() else []:
        rel = note.relative_to(kb).as_posix()
        if note.name == "index.md":
            domain_indexes[note.parent.name] = note.read_text(encoding="utf-8")
            continue
        fm = lint_note(kb, note, rel)
        statuses[rel] = (fm or {}).get("status", "")

    # reachability: every active note in root index, or via its domain index
    for rel, status in statuses.items():
        domain = rel.split("/")[1] if rel.count("/") >= 2 else ""
        in_root = rel in index_text
        via_domain = (
            domain in domain_indexes
            and f"notes/{domain}/index.md" in index_text
            and Path(rel).name in domain_indexes[domain]
        )
        if status == "active" and not (in_root or via_domain):
            err(rel, "active note is not reachable from index.md — add it (or its domain index)")
        if status in ("superseded", "deprecated") and (in_root or via_domain):
            err(rel, f"{status} note is still listed in the index — remove it")

    # index entries must point at existing, active notes
    for name, text in [("index.md", index_text)] + [
        (f"notes/{d}/index.md", t) for d, t in domain_indexes.items()
    ]:
        base = kb if name == "index.md" else kb / Path(name).parent
        for m in MD_LINK_RE.finditer(text):
            target = m.group(1)
            if not target.endswith(".md") or target.startswith(("http://", "https://")):
                continue
            if "<" in target or ">" in target:
                continue  # placeholder in a format example, not a real link
            resolved = (base / target).resolve()
            if not resolved.is_file():
                err(name, f"index entry points at missing file: {target}")
                continue
            rel = resolved.relative_to(kb).as_posix() if resolved.is_relative_to(kb) else target
            if rel in statuses and statuses[rel] != "active":
                err(name, f"index entry points at {statuses[rel]} note: {target}")

    core = kb / "core"
    for f in sorted(core.glob("*.md")) if core.is_dir() else []:
        n = len(f.read_text(encoding="utf-8").splitlines())
        if n > 100:
            warn(f"core/{f.name}", f"{n} lines (protocol target: ≤100) — trim or move detail into notes/")

    episodes = kb / "episodes"
    for f in sorted(episodes.rglob("*.md")) if episodes.is_dir() else []:
        if not EPISODE_RE.match(f.name) or not re.match(r"^\d{4}$", f.parent.name):
            warn(f.relative_to(kb).as_posix(), "episode files must be episodes/<YYYY>/<YYYY-MM-DD>.md")

    for line in errors + warnings:
        print(line)
    print(f"kb_lint: {len(statuses)} notes checked, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
