"""Write the harmony course into a book folder: songs/*.md (one per lesson part) and tags.yaml.

    <builder>/.venv/bin/python generator/make_book.py <book folder>
    then <builder>/cancionero.py publish <book>

Lessons are in lessons.py; music.py spells scales and chords and leads the voices
(`python music.py` runs its self-checks).

Every songs/*.md in the folder is replaced (the folder holds only this course).
"""

import json
import sys
import textwrap
from pathlib import Path

# The builder: next to hymn_books/ (this file is in hymn_books/<book>/generator/).
ROOT = Path(__file__).resolve().parents[3] / "cancionero-builder"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))

from builder.lyrics import LABEL_RE, is_chord_line  # noqa: E402
from lessons import BLOCKS, INTRO  # noqa: E402

WIDTH = 46


def prose(text):
    """Lesson text -> body lines: paragraphs wrapped, `- ` bullets, `## ` bold headers,
    `|` lines verbatim (chord lines, note names)."""
    out, wrapped = [], []
    for raw in textwrap.dedent(text).strip().split("\n"):
        line = raw.strip()
        if not line:
            out.append("")
        elif line.startswith("## "):
            out += ["", "**", line[3:], "**"]
        elif line.startswith("|"):
            out.append(line[1:])
        else:
            for width in range(WIDTH, 30, -1):  # narrower until no line is only chord-like words
                lines = (textwrap.wrap(line[2:], width, initial_indent="- ", subsequent_indent="  ")
                         if line.startswith("- ") else textwrap.wrap(line, width))
                if not any(is_chord_line(x) for x in lines):
                    break
            out += lines
            wrapped += lines
    for line in wrapped:  # a sentence must not be read as chords or as "Intro: ..." chords
        if is_chord_line(line) or LABEL_RE.fullmatch(line):
            raise ValueError(f"line would be read as chords: {line!r}")
    return out


def song(title, tags, p):
    head = ["---", f"title: {json.dumps(title, ensure_ascii=False)}"]
    if tags:
        tag, sub = tags
        head += ["song_tags:", f"  {tag}:", f"    - {sub}"]
    if p["abc"]:
        head.append("melody: |")
        head += ["  " + line for line in p["abc"].split("\n")]
    head.append("---")
    body = [f"⏱ {p['minutes']} min", ""] + prose(p["text"])
    if p["chords"]:
        body += ["", p["chords"]]
    return "\n".join(head) + "\n\n" + "\n".join(body).replace("\n\n\n", "\n\n").strip() + "\n"


def main(folder):
    folder = Path(folder)
    songs = folder / "songs"
    songs.mkdir(parents=True, exist_ok=True)
    for old in songs.glob("*.md"):
        old.unlink()
    (songs / "00.md").write_text(song("00 · Cómo usar este curso", ("inicio", "como_usar"), INTRO), encoding="utf-8")
    tags = ["# Bloques y lecciones del curso, en orden.", "", "inicio:", '  label: "0 · Empieza aquí"', "  subtags:",
            '    como_usar: "Cómo usar este curso"', ""]
    number, parts, minutes = 0, 0, []
    for tag, label, lessons in BLOCKS:
        tags += [f"{tag}:", f"  label: {json.dumps(label, ensure_ascii=False)}", "  subtags:"]
        for title, lesson_parts in lessons:
            number += 1
            sub = f"leccion_{number:02d}"
            tags.append(f"    {sub}: {json.dumps(f'Lección {number} · {title}', ensure_ascii=False)}")
            minutes.append(sum(p["minutes"] for p in lesson_parts))
            for letter, p in zip("abcdefgh", lesson_parts):
                name = f"{number:02d}{letter} · {p['title']}"
                (songs / f"{number:02d}{letter}.md").write_text(song(name, (tag, sub), p), encoding="utf-8")
                parts += 1
        tags.append("")
    (folder / "tags.yaml").write_text("\n".join(tags), encoding="utf-8")
    print(f"{number} lessons, {parts} parts; minutes per lesson {min(minutes)}-{max(minutes)}")
    off = [(i + 1, m) for i, m in enumerate(minutes) if not 25 <= m <= 35]
    if off:
        print("lessons not 25-35 min:", off)


if __name__ == "__main__":
    main(sys.argv[1])
