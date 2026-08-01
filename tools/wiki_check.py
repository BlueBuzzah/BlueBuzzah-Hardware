#!/usr/bin/env python3
"""Check the BlueBuzzah v3 wiki for broken links and v2 leakage.

Usage: python3 tools/wiki_check.py ../BlueBuzzah-Hardware.wiki
"""
import re
import sys
from pathlib import Path

# The single sanctioned v2 reference, allowlisted by exact path, not pattern.
V2_ALLOWED = "Instructions/Blue Buzzah Build Documentation.pdf"

# Anything else v2-ish is a failure.
V2_FORBIDDEN = re.compile(r"PCB/v2|archive/|BlueBuzzah 2\.0|Legacy[- ]v2", re.IGNORECASE)

# GitHub alert marker lines, e.g. "> [!NOTE]". Captures the bang-token and
# anything trailing it on the same line (which must be empty, or the alert
# silently renders as a plain blockquote instead of an alert).
ALERT_MARKER = re.compile(r"^>\s*\[!([^\]]*)\](.*)$")
ALERT_TYPES = {"NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"}

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
# Image embeds: ![alt](path). Relative paths under images/ are correct here and
# resolve fine in GitHub wikis - check that the file exists rather than reject it.
IMGLINK = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
# Page links: [text](url), excluding image embeds via the negative lookbehind.
MDLINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def check(wiki: Path) -> list[str]:
    errors = []
    pages = sorted(wiki.glob("*.md"))
    names = {p.stem.replace("-", " ").lower() for p in pages}

    if (wiki / "archive").exists():
        errors.append("archive/ still exists - it is public surface and must be deleted")

    for page in pages:
        text = page.read_text(encoding="utf-8")

        for line_no, line in enumerate(text.splitlines(), 1):
            stripped = line.replace(V2_ALLOWED, "")
            if V2_FORBIDDEN.search(stripped):
                errors.append(f"{page.name}:{line_no}: forbidden v2 reference")

            alert = ALERT_MARKER.match(line)
            if alert:
                token, trailing = alert.group(1), alert.group(2)
                if token not in ALERT_TYPES:
                    errors.append(f"{page.name}:{line_no}: malformed alert type "
                                  f"'[!{token}]' - must be one of {sorted(ALERT_TYPES)}")
                if trailing.strip():
                    errors.append(f"{page.name}:{line_no}: alert marker has body text "
                                  "on the same line - must be on its own line")

        for target in WIKILINK.findall(text):
            if target.strip().lower() not in names:
                errors.append(f"{page.name}: broken wikilink [[{target}]]")

        images = set(IMGLINK.findall(text))
        for src in images:
            if src.startswith(("http://", "https://")):
                continue
            if not (wiki / src).is_file():
                errors.append(f"{page.name}: missing image '{src}'")

        for url in MDLINK.findall(text):
            if url in images:
                continue
            if url.startswith(("http://", "https://", "#")):
                continue
            errors.append(f"{page.name}: non-absolute link '{url}' "
                          "- wiki pages cannot use repo-relative paths")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    wiki = Path(sys.argv[1])
    if not wiki.is_dir():
        print(f"not a directory: {wiki}")
        return 2

    errors = check(wiki)
    for e in errors:
        print(e)
    print(f"\n{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
