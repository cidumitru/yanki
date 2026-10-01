#!/usr/bin/env python3
"""Build the ".NET Interview - Top 100" Anki deck as an .apkg file.

Usage:
    pip install genanki
    python3 build_deck.py [output.apkg]

Note type: "System Design Concept" with fields Question, Answer, WhyItMatters, Example, Source.
Deck:      Interview::.NET
Card content lives in cards/*.py (small markup: `code`, **bold**, ``` fenced blocks).
Note GUIDs are derived from the stable card id, so re-importing a rebuilt deck updates
existing notes in place instead of duplicating them.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import genanki

from cards import ALL_CARDS

HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "dotnet-interview-top100.apkg"

# Fixed ids: Anki matches note types and decks by id, so keep these stable across rebuilds.
MODEL_ID = 1727740800101
DECK_ID = 1727740800102
MODEL_NAME = "System Design Concept"
DECK_NAME = "Interview::.NET"
GUID_NAMESPACE = "dotnet-interview-top100"

EXPECTED_CARD_COUNT = 100

FENCE = re.compile(r"```[a-zA-Z0-9]*\n(.*?)```", re.S)
INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
EMPH = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")


def render_inline(text: str) -> str:
    """Escape HTML, then apply inline markup and line breaks."""
    text = html.escape(text.strip(), quote=False)
    text = INLINE_CODE.sub(r"<code>\1</code>", text)
    text = BOLD.sub(r"<b>\1</b>", text)
    text = EMPH.sub(r"<i>\1</i>", text)
    return text.replace("\n", "<br>")


def render(text: str) -> str:
    """Render a field: prose segments with inline markup, fenced blocks as <pre><code>."""
    parts = FENCE.split(text.strip())
    out: list[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # fenced code
            out.append("<pre><code>" + html.escape(part.rstrip("\n"), quote=False) + "</code></pre>")
        else:
            prose = render_inline(part)
            if prose:
                out.append(f"<div class=\"p\">{prose}</div>")
    return "".join(out)


def render_source(url: str) -> str:
    label = re.sub(r"^https?://", "", url)
    return f'<a href="{html.escape(url)}">{html.escape(label)}</a>'


CSS = """
/* Colors live in custom properties so night mode only has to override them.
   Anki desktop puts both "card" and "night_mode"/"nightMode" on <body>; AnkiDroid nests
   .card under the night class, so both selector shapes are covered. */
.card {
  --bg: #fafafa; --fg: #1f2937; --muted: #6b7280; --rule: #d1d5db;
  --why-bg: #fffbeb; --why-edge: #f59e0b; --ex-bg: #eff6ff; --ex-edge: #3b82f6;
  --code-bg: rgba(0,0,0,.06); --pre-bg: #1e1e1e; --pre-fg: #d4d4d4; --link: #2563eb;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 18px; line-height: 1.45; color: var(--fg); background: var(--bg);
  text-align: left; padding: 14px 18px; max-width: 780px; margin: 0 auto;
}
.card.night_mode, .night_mode .card, .card.nightMode, .nightMode .card {
  --bg: #111827; --fg: #e5e7eb; --muted: #9ca3af; --rule: #374151;
  --why-bg: #3a2e0c; --why-edge: #fbbf24; --ex-bg: #0f2749; --ex-edge: #60a5fa;
  --code-bg: rgba(255,255,255,.12); --pre-bg: #0b1220; --pre-fg: #d4d4d4; --link: #60a5fa;
}
.hdr { font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
.q { font-size: 22px; font-weight: 600; }
hr#answer { border: 0; border-top: 1px solid var(--rule); margin: 16px 0; }
.a { font-size: 18px; }
.box { margin-top: 14px; padding: 10px 14px; border-radius: 8px; border-left: 4px solid; }
.why { background: var(--why-bg); border-color: var(--why-edge); }
.ex { background: var(--ex-bg); border-color: var(--ex-edge); }
.lbl { font-size: 12px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; opacity: .75; margin-bottom: 4px; }
.p + .p, .p + pre, pre + .p { margin-top: 8px; }
code { font-family: "JetBrains Mono", "Cascadia Code", Menlo, Consolas, monospace; font-size: .92em;
       background: var(--code-bg); padding: 1px 4px; border-radius: 4px; }
pre { background: var(--pre-bg); color: var(--pre-fg); padding: 10px 12px; border-radius: 6px; overflow-x: auto;
      font-size: 14px; line-height: 1.4; margin: 0; white-space: pre; text-align: left; }
pre code { background: none; padding: 0; color: inherit; font-size: inherit; }
.src { margin-top: 14px; font-size: 13px; color: var(--muted); word-break: break-all; }
.src a { color: var(--link); text-decoration: none; }
.tags { margin-top: 6px; font-size: 12px; color: var(--muted); opacity: .8; }
"""

FRONT = """<div class="hdr">Interview &middot; .NET</div>
<div class="q">{{Question}}</div>"""

BACK = """{{FrontSide}}
<hr id="answer">
<div class="a">{{Answer}}</div>
{{#WhyItMatters}}<section class="box why"><div class="lbl">Why it matters</div>{{WhyItMatters}}</section>{{/WhyItMatters}}
{{#Example}}<section class="box ex"><div class="lbl">Example</div>{{Example}}</section>{{/Example}}
{{#Source}}<div class="src">Source: {{Source}}</div>{{/Source}}
<div class="tags">{{Tags}}</div>"""

MODEL = genanki.Model(
    MODEL_ID,
    MODEL_NAME,
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
        {"name": "WhyItMatters"},
        {"name": "Example"},
        {"name": "Source"},
    ],
    templates=[{"name": "Card 1", "qfmt": FRONT, "afmt": BACK}],
    css=CSS,
)

DECK_DESCRIPTION = (
    "Top 100 most frequently asked .NET interview questions: CLR &amp; memory, C#, async, "
    "ASP.NET Core, EF Core, architecture, testing and security. One concept per card; "
    "the back shows the answer, why it matters, a short example and a Microsoft Learn source."
)


def validate(cards: list[dict]) -> None:
    ids = [c["id"] for c in cards]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f"duplicate card ids: {sorted(dupes)}")
    if len(cards) != EXPECTED_CARD_COUNT:
        raise SystemExit(f"expected {EXPECTED_CARD_COUNT} cards, found {len(cards)}")
    questions = [c["q"].strip().lower() for c in cards]
    dup_q = {q for q in questions if questions.count(q) > 1}
    if dup_q:
        raise SystemExit(f"duplicate questions: {sorted(dup_q)}")
    for c in cards:
        for key in ("q", "a", "why", "ex", "src"):
            if not str(c.get(key, "")).strip():
                raise SystemExit(f"card {c['id']}: field '{key}' is empty")
        if not c["src"].startswith("https://"):
            raise SystemExit(f"card {c['id']}: source must be an https URL")
        if c["q"].count("```"):
            raise SystemExit(f"card {c['id']}: question must not contain a code block")
        for tag in c["tags"]:
            if " " in tag:
                raise SystemExit(f"card {c['id']}: tag '{tag}' contains a space")


def build(output: Path) -> int:
    validate(ALL_CARDS)
    deck = genanki.Deck(DECK_ID, DECK_NAME, description=DECK_DESCRIPTION)
    for card in ALL_CARDS:
        note = genanki.Note(
            model=MODEL,
            fields=[
                render(card["q"]),
                render(card["a"]),
                render(card["why"]),
                render(card["ex"]),
                render_source(card["src"]),
            ],
            tags=["interview", "dotnet", *card["tags"]],
            guid=genanki.guid_for(GUID_NAMESPACE, card["id"]),
        )
        deck.add_note(note)
    output.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck).write_to_file(str(output))
    return len(ALL_CARDS)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    count = build(out)
    print(f"wrote {count} notes to {out}")
