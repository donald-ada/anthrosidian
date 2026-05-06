#!/usr/bin/env python3
"""Fetch a URL into an Anthrosidian raw Markdown note."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


SKIP_TAGS = {
    "script",
    "style",
    "noscript",
    "svg",
    "canvas",
    "nav",
    "header",
    "footer",
    "form",
    "aside",
}
HEADING_TAGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}
BLOCK_TAGS = {
    "article",
    "blockquote",
    "body",
    "br",
    "div",
    "li",
    "main",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "tr",
    "ul",
}
PUNCTUATION = set(".,;:!?)]}%")


class ReadableHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = True
            return
        if tag in HEADING_TAGS:
            self._newline()
            self.parts.append("#" * HEADING_TAGS[tag] + " ")
        elif tag == "li":
            self._newline()
            self.parts.append("- ")
        elif tag in BLOCK_TAGS:
            self._newline()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.skip_depth:
            if tag in SKIP_TAGS:
                self.skip_depth -= 1
            return
        if tag == "title":
            self.in_title = False
            return
        if tag in HEADING_TAGS or tag in BLOCK_TAGS:
            self._newline()

    def handle_data(self, data: str) -> None:
        text = normalize_inline_text(data)
        if not text:
            return
        if self.in_title:
            self.title_parts.append(text)
            return
        if self.skip_depth:
            return
        if (
            self.parts
            and not self.parts[-1].endswith((" ", "\n"))
            and text[0] not in PUNCTUATION
        ):
            self.parts.append(" ")
        self.parts.append(text)

    def _newline(self) -> None:
        if self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    @property
    def title(self) -> str:
        return normalize_inline_text(" ".join(self.title_parts))

    @property
    def markdown(self) -> str:
        return normalize_markdown("".join(self.parts))


def normalize_inline_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_markdown(value: str) -> str:
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r" +([.,;:!?])", r"\1", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def html_to_markdown(value: str) -> tuple[str, str]:
    parser = ReadableHTMLParser()
    parser.feed(value)
    title = parser.title
    markdown = parser.markdown
    if not title:
        for line in markdown.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
    return title, markdown


def looks_like_html(value: str) -> bool:
    return bool(re.search(r"<(?:html|head|body|title|article|main|p|h[1-6])\b", value, re.I))


def title_from_url(url: str) -> str:
    parsed = urlparse(url)
    stem = Path(parsed.path).stem
    if stem:
        return stem.replace("-", " ").replace("_", " ").strip()
    return parsed.netloc or "web-source"


def slugify(title: str, url: str) -> str:
    base = title or title_from_url(url)
    base = unicodedata.normalize("NFKC", base).lower()
    base = re.sub(r"[^\w\s.-]+", "", base, flags=re.UNICODE)
    base = re.sub(r"[\s_.]+", "-", base).strip("-")
    return (base[:80].strip("-") or "web-source")


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def unique_path(raw_dir: Path, slug: str) -> Path:
    candidate = raw_dir / f"{slug}.md"
    counter = 2
    while candidate.exists():
        candidate = raw_dir / f"{slug}-{counter}.md"
        counter += 1
    return candidate


def save_raw_note(
    vault: Path,
    url: str,
    title: str,
    markdown: str,
    fetched_date: dt.date,
) -> Path:
    raw_dir = vault / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    display_title = normalize_inline_text(title) or title_from_url(url)
    output = unique_path(raw_dir, slugify(display_title, url))
    fetched = fetched_date.isoformat()
    content = "\n".join(
        [
            "---",
            "tags: [raw, web]",
            f"source: {yaml_quote(url)}",
            f"title: {yaml_quote(display_title)}",
            f'fetched: "{fetched}"',
            "---",
            "",
            f"# {display_title}",
            "",
            f"Source: {url}",
            f"Fetched: {fetched}",
            "",
            normalize_markdown(markdown),
            "",
        ]
    )
    output.write_text(content, encoding="utf-8")
    return output


def fetch_url(url: str, timeout: int) -> tuple[str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Anthrosidian/1.0 (+https://github.com/donald-ada/anthrosidian)"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read().decode(charset, errors="replace")
    return body, content_type


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a URL and save it as a raw Anthrosidian Markdown note."
    )
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--vault", required=True, help="Obsidian vault path")
    parser.add_argument("--title", help="Override the detected title")
    parser.add_argument("--timeout", type=int, default=20, help="Fetch timeout in seconds")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    vault = Path(args.vault).expanduser()
    if not vault.is_dir():
        print(f"Vault path does not exist or is not a directory: {vault}", file=sys.stderr)
        return 2

    try:
        body, content_type = fetch_url(args.url, args.timeout)
    except urllib.error.HTTPError as exc:
        print(f"Failed to fetch {args.url}: HTTP {exc.code} {exc.reason}", file=sys.stderr)
        return 2
    except urllib.error.URLError as exc:
        print(f"Failed to fetch {args.url}: {exc.reason}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Failed to fetch {args.url}: {exc}", file=sys.stderr)
        return 2

    if "html" in content_type.lower() or looks_like_html(body):
        detected_title, markdown = html_to_markdown(body)
    else:
        detected_title, markdown = title_from_url(args.url), normalize_markdown(body)

    title = args.title or detected_title or title_from_url(args.url)
    if not markdown:
        print(f"Fetched {args.url} but no readable content was extracted.", file=sys.stderr)
        return 3

    try:
        output = save_raw_note(vault, args.url, title, markdown, dt.date.today())
    except OSError as exc:
        print(f"Failed to write raw note for {args.url}: {exc}", file=sys.stderr)
        return 2

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
