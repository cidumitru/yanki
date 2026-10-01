# .NET Interview – Top 100 (Anki deck)

`dotnet-interview-top100.apkg` contains the 100 most frequently asked .NET interview
questions as Anki flashcards, ready to import.

## Format

- **Deck:** `Interview::.NET`
- **Note type:** `System Design Concept` with fields `Question`, `Answer`, `WhyItMatters`,
  `Example`, `Source` (one card per note, front = question, back = everything else).
- **Tags:** every note carries `interview`, `dotnet` and a hierarchical topic tag, e.g.
  `dotnet::csharp::linq`, `dotnet::aspnetcore`, `dotnet::efcore`, `dotnet::architecture::solid`.

| Area                         | Cards |
| ---------------------------- | ----- |
| CLR, memory, runtime         | 12    |
| C# language, types, LINQ     | 32    |
| Async & threading            | 11    |
| ASP.NET Core                 | 17    |
| EF Core                      | 9     |
| Architecture & SOLID         | 10    |
| Testing                      | 4     |
| Performance & security       | 5     |

## Card design rules

- One concept per card (minimum-information principle); the question is specific enough
  to have a single answer.
- Answers are short (2–4 sentences) and stated in interview-ready wording.
- `WhyItMatters` gives the interview angle so the fact is anchored to a reason.
- `Example` is a 1–8 line snippet or a concrete scenario, never a second explanation.
- `Source` links to Microsoft Learn (or an official .NET blog post) for deeper reading.

## Importing

Anki Desktop → **File → Import…** → pick the `.apkg`. Anki matches note types by internal id,
so if you already have a note type called `System Design Concept`, the import will add the deck's
own copy (same five fields) under a suffixed name; use **Browse → Notes → Change Note Type** to
move the notes onto your existing type if you want them merged.

## Rebuilding

```bash
pip install genanki
python3 decks/dotnet-interview/build_deck.py            # writes dotnet-interview-top100.apkg next to the script
python3 decks/dotnet-interview/build_deck.py out.apkg   # custom output path
```

Card content lives in `cards/*.py`. Each card is a dict with `id`, `tags`, `q`, `a`, `why`,
`ex`, `src`. Fields accept a tiny markup: `` `inline code` ``, `**bold**`, and ``` fenced blocks
for multi-line code. Note GUIDs derive from the stable `id`, so re-importing a rebuilt deck
updates existing notes instead of duplicating them.
