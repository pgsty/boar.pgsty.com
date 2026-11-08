#!/usr/bin/env python3
"""Validate the pinned toolchain, bilingual source contract, and built site."""

from __future__ import annotations

import html
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"
SITE_ORIGIN = "https://boar.pgsty.com"
SITE_HOST = urlsplit(SITE_ORIGIN).netloc


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.lang = values.get("lang", "").lower()
        for key in ("id", "name"):
            if values.get(key):
                self.ids.add(values[key])
        for key in ("href", "src", "action", "poster"):
            if values.get(key):
                self.references.append((key, html.unescape(values[key].strip())))
        if values.get("srcset"):
            for candidate in values["srcset"].split(","):
                url = candidate.strip().split(" ", 1)[0]
                if url:
                    self.references.append(("srcset", html.unescape(url)))


def command_output(*args: str) -> str:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout.strip()


def web_path(path: Path) -> str:
    relative = path.relative_to(PUBLIC).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative[: -len("index.html")]
    return "/" + relative


def output_target(path: str) -> Path | None:
    clean = unquote(path)
    if not clean.startswith("/"):
        return None
    candidate = PUBLIC / clean.lstrip("/")
    if clean.endswith("/"):
        return candidate / "index.html"
    if candidate.is_file():
        return candidate
    if candidate.is_dir():
        return candidate / "index.html"
    if not candidate.suffix:
        return candidate / "index.html"
    return candidate


def check_toolchain(errors: list[str]) -> None:
    try:
        go = command_output("go", "version")
        hugo = command_output("hugo", "version")
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"toolchain probe failed: {exc}")
        return
    go_version = re.search(r"go(\d+)\.(\d+)\.(\d+)", go)
    if not go_version or tuple(map(int, go_version.groups())) < (1, 27, 3):
        errors.append(f"expected Go 1.27.3 or newer, got: {go}")
    hugo_version = re.search(r"hugo v(\d+)\.(\d+)\.(\d+)(?:-[0-9a-f]+)?\+extended", hugo)
    if not hugo_version or tuple(map(int, hugo_version.groups())) < (0, 168, 0):
        errors.append(f"expected Hugo Extended 0.168.0 or newer, got: {hugo}")
    go_mod = (ROOT / "go.mod").read_text(encoding="utf-8")
    if "go 1.27.3" not in go_mod:
        errors.append("go.mod does not pin Go 1.27.3")
    if "github.com/pgsty/oink v1.5.1" not in go_mod:
        errors.append("go.mod does not pin Oink v1.5.1")


def check_source_contract(errors: list[str]) -> tuple[int, int]:
    english = sorted(path for path in CONTENT.rglob("*.md") if not path.name.endswith(".zh.md"))
    chinese = sorted(CONTENT.rglob("*.zh.md"))
    for source in english:
        translated = source.with_name(f"{source.stem}.zh.md")
        if not translated.is_file():
            errors.append(f"missing Chinese translation: {translated.relative_to(ROOT)}")
        if re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", source.read_text(encoding="utf-8")):
            errors.append(f"untranslated Chinese text in English source: {source.relative_to(ROOT)}")
    for source in chinese:
        translated = source.with_name(source.name.removesuffix(".zh.md") + ".md")
        if not translated.is_file():
            errors.append(f"missing English translation: {translated.relative_to(ROOT)}")

    article_files = [
        path
        for path in (CONTENT / "blog" / "article").glob("*.md")
        if not path.name.startswith("_index")
    ]
    if article_files:
        errors.append("Blog/article must remain intentionally empty")

    design_en = [
        path
        for path in (CONTENT / "blog" / "design").glob("*.md")
        if not path.name.startswith("_index") and not path.name.endswith(".zh.md")
    ]
    if len(design_en) < 15:
        errors.append(f"expected at least 15 English design notes, found {len(design_en)}")
    return len(english), len(chinese)


def check_required_outputs(errors: list[str]) -> None:
    required = (
        "index.html",
        "zh/index.html",
        "docs/index.html",
        "zh/docs/index.html",
        "blog/index.html",
        "zh/blog/index.html",
        "blog/article/index.html",
        "zh/blog/article/index.html",
        "blog/design/index.html",
        "zh/blog/design/index.html",
        "blog/release/index.html",
        "zh/blog/release/index.html",
        "docs/llms-full.txt",
        "zh/docs/llms-full.txt",
        "llms.txt",
        "zh/llms.txt",
        "navigation.json",
        "zh/navigation.json",
        "favicon.svg",
        "icons/logo.svg",
    )
    for relative in required:
        if not (PUBLIC / relative).is_file():
            errors.append(f"missing generated output: public/{relative}")


def check_html(errors: list[str]) -> tuple[int, int]:
    documents: dict[Path, DocumentParser] = {}
    for path in sorted(PUBLIC.rglob("*.html")):
        parser = DocumentParser()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
            continue
        documents[path] = parser
        expected_lang = "zh" if path.relative_to(PUBLIC).parts[0] == "zh" else "en"
        if not parser.lang.startswith(expected_lang):
            errors.append(
                f"wrong html lang in {path.relative_to(ROOT)}: expected {expected_lang}, got {parser.lang or 'missing'}"
            )

    checked = 0
    seen: set[tuple[Path, str]] = set()
    for source, parser in documents.items():
        base = SITE_ORIGIN + web_path(source)
        for attribute, raw in parser.references:
            if not raw or raw.startswith(("data:", "javascript:", "mailto:", "tel:")):
                continue
            absolute = urlsplit(urljoin(base, raw))
            if absolute.scheme not in ("http", "https") or absolute.netloc != SITE_HOST:
                continue
            target = output_target(absolute.path)
            if target is None:
                continue
            key = (source, raw)
            if key in seen:
                continue
            seen.add(key)
            checked += 1
            if not target.is_file():
                errors.append(
                    f"broken {attribute} in {source.relative_to(ROOT)}: {raw} -> {target.relative_to(ROOT)}"
                )
                continue
            fragment = unquote(absolute.fragment)
            if fragment and not fragment.startswith(":~:") and target.suffix == ".html":
                target_doc = documents.get(target)
                if target_doc is not None and fragment not in target_doc.ids:
                    errors.append(
                        f"missing anchor in {source.relative_to(ROOT)}: {raw} -> #{fragment}"
                    )
    return len(documents), checked


def main() -> int:
    errors: list[str] = []
    check_toolchain(errors)
    english, chinese = check_source_contract(errors)
    check_required_outputs(errors)
    documents, references = check_html(errors)

    if errors:
        print(f"site validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors[:100]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 100:
            print(f"- ... {len(errors) - 100} more", file=sys.stderr)
        return 1

    print(
        "site validation passed: "
        f"{english} English + {chinese} Chinese source pages, "
        f"{documents} HTML outputs, {references} internal references"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
