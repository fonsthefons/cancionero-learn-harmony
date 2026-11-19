"""Music helpers for the harmony course: spelling, scales, chords, voice leading, ABC.

A note is (name, octave) with the octave of its letter (B#3 is written B, not C):
("C", 4) is middle C, as in ABC "C".
"""

import re

LETTERS = "CDEFGAB"
NATURAL = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]


def split(name):
    return name[0], name[1:].count("#") - name[1:].count("b")


def pc(name):
    letter, acc = split(name)
    return (NATURAL[letter] + acc) % 12


def spell(letter, pitch):
    acc = (pitch - NATURAL[letter] + 6) % 12 - 6
    return letter + ("#" * acc if acc > 0 else "b" * -acc)


def step(name, letters, semitones):
    """The note `letters` letter names and `semitones` above `name`, spelled right."""
    letter = LETTERS[(LETTERS.index(name[0]) + letters) % 7]
    return spell(letter, pc(name) + semitones)


def scale_names(tonic, kind="major"):
    steps = list(MAJOR if kind == "major" else MINOR)
    if kind in ("harmonic", "melodic"):
        steps[6] = 11
    if kind == "melodic":
        steps[5] = 9
    return [step(tonic, i, s) for i, s in enumerate(steps)]


def midi(note):
    name, octave = note
    letter, acc = split(name)
    return 12 * (octave + 1) + NATURAL[letter] + acc


def scale_notes(tonic, kind, octave, octaves=1):
    """Ascending notes from (tonic, octave), 7*octaves + 1 of them."""
    names, first = scale_names(tonic, kind), LETTERS.index(tonic[0])
    return [(names[i % 7], octave + (first + i) // 7) for i in range(7 * octaves + 1)]


def place(name, near):
    """(name, octave) whose pitch is closest to midi `near` (lower on a tie)."""
    options = [(name, o) for o in range(0, 9)]
    return min(options, key=lambda n: (abs(midi(n) - near), midi(n)))


def above(name, note):
    """The lowest (name, octave) higher than `note`."""
    octave = note[1] - 1
    while midi((name, octave)) <= midi(note):
        octave += 1
    return (name, octave)


# ---- key signatures and ABC ----

def key_parts(key):
    """"F#m" -> ("F#", "natural"); "Bb" -> ("Bb", "major")."""
    return (key[:-1], "natural") if key.endswith("m") else (key, "major")


def signature(key):
    tonic, kind = key_parts(key)
    return dict(split(n) for n in scale_names(tonic, kind))


def signature_text(key):
    accs = [n for n in scale_names(*key_parts(key)) if len(n) > 1]
    if not accs:
        return "sin sostenidos ni bemoles"
    sharps = "#" in accs[0]
    order = "FCGDAEB" if sharps else "BEADGCF"
    accs.sort(key=lambda n: order.index(n[0]))
    word = ("sostenido" if sharps else "bemol") if len(accs) == 1 else ("sostenidos" if sharps else "bemoles")
    return f"{len(accs)} {word} ({', '.join(accs)})"


ACC_ABC = {2: "^^", 1: "^", 0: "=", -1: "_", -2: "__"}


class Voice:
    """One ABC voice; tracks accidentals so each bar is written correctly."""

    def __init__(self, key):
        self.sig, self.state, self.tokens = signature(key), {}, []

    def pitch(self, note):
        name, octave = note
        letter, acc = split(name)
        current = self.state.get((letter, octave), self.sig.get(letter, 0))
        self.state[(letter, octave)] = acc
        text = letter if octave <= 4 else letter.lower()
        text += "'" * max(0, octave - 5) + "," * max(0, 4 - octave)
        return ("" if acc == current else ACC_ABC[acc]) + text

    def add(self, notes, length="", finger=None, label=None):
        """A note or chord (list of notes); a label is a chord name shown above."""
        head = (f'"{label}"' if label else "") + (f"!{finger}!" if finger else "")
        if isinstance(notes, tuple):
            self.tokens.append(head + self.pitch(notes) + length)
        else:
            self.tokens.append(head + "[" + "".join(self.pitch(n) for n in notes) + "]" + length)

    def rest(self, length=""):
        self.tokens.append("z" + length)

    def bar(self, end=False):
        self.state = {}
        self.tokens.append("|]" if end else "|")

    def text(self):
        return " ".join(self.tokens)


def grand(key, rh, lh, meter=None, tempo=None):
    """ABC body for a melody: field: two staves joined by a brace."""
    head = []
    if meter:
        head.append(f"M:{meter}")
    if tempo:
        head.append(f"Q:1/4={tempo}")
    head += [f"K:{key}", "%%staves {RH LH}", "V:RH clef=treble", rh.text(), "V:LH clef=bass", lh.text()]
    return "\n".join(head)


def single(key, voice, clef="treble", tempo=None):
    head = [f"Q:1/4={tempo}"] if tempo else []
    return "\n".join(head + [f"K:{key} clef={clef}", voice.text()])


# ---- fingerings (ascending, one octave) ----

RH_MAJOR = {"C": "12312345", "G": "12312345", "D": "12312345", "A": "12312345", "E": "12312345",
            "B": "12312345", "F#": "23412312", "Gb": "23412312", "Db": "23123412", "C#": "23123412",
            "Ab": "34123123", "Eb": "31234123", "Bb": "41231234", "F": "12341234"}
LH_MAJOR = {"C": "54321321", "G": "54321321", "D": "54321321", "A": "54321321", "E": "54321321",
            "B": "43214321", "F#": "43213214", "Gb": "43213214", "Db": "32143213", "C#": "32143213",
            "Ab": "32143213", "Eb": "32143213", "Bb": "32143213", "F": "54321321"}
RH_MINOR = {"A": "12312345", "E": "12312345", "D": "12312345", "G": "12312345", "C": "12312345",
            "B": "12312345", "F#": "34123123", "C#": "34123123", "G#": "34123123",
            "Eb": "31234123", "D#": "31234123", "Bb": "21231234", "F": "12341234"}
LH_MINOR = {"A": "54321321", "E": "54321321", "D": "54321321", "G": "54321321", "C": "54321321",
            "B": "43214321", "F#": "43213214", "C#": "32143213", "G#": "32143213",
            "Eb": "21432132", "D#": "21432132", "Bb": "21321432", "F": "54321321"}


def fingers(tonic, kind, hand, octaves):
    """Fingers for the ascending notes; the pattern repeats each octave (RH upwards,
    LH downwards from the top), as in the usual scale books."""
    table = (RH_MAJOR if hand == "RH" else LH_MAJOR) if kind == "major" else (RH_MINOR if hand == "RH" else LH_MINOR)
    one = [int(f) for f in table[tonic]]
    if hand == "LH":
        one = one[::-1]
    out = one[:7] * octaves + [one[7]]
    return out if hand == "RH" else out[::-1]


def scale_bars(voice, notes, fing, kind, tonic):
    """Up in one bar, down in the next (melodic minor comes down natural)."""
    for note, f in zip(notes, fing):
        voice.add(note, finger=f)
    voice.bar()
    if len(notes) > 8:  # two octaves: the way down on its own staff line, readable on a phone
        voice.tokens.append("\n")
    down = list(reversed(notes))[1:]
    if kind == "melodic":
        nat = scale_notes(tonic, "natural", notes[0][1], (len(notes) - 1) // 7)
        down = list(reversed(nat))[1:]
    for note, f in zip(down, list(reversed(fing))[1:]):
        voice.add(note, finger=f)


def scale_abc(tonic, kind="major", hands="HS", octaves=1, contrary=False):
    key = tonic + ("" if kind == "major" else "m")
    rh_oct = 4 if octaves == 1 or tonic[0] in "CDEFG" else 3
    lh_oct = rh_oct - 1
    rh, lh = Voice(key), Voice(key)
    rh_notes = scale_notes(tonic, kind, rh_oct, octaves)
    rh_f = fingers(tonic, kind, "RH", octaves)
    if contrary:
        lh_notes = [place(n[0], midi(n) - 12 - 2 * (midi(n) - midi(rh_notes[0]))) for n in rh_notes]
        lh_f = [int(f) for f in (LH_MAJOR if kind == "major" else LH_MINOR)[tonic]][::-1]
        for n, f, m, g in zip(rh_notes, rh_f, lh_notes, lh_f):
            rh.add(n, finger=f)
            lh.add(m, finger=g)
        rh.bar(), lh.bar()
        for n, f, m, g in list(zip(rh_notes, rh_f, lh_notes, lh_f))[-2::-1]:
            rh.add(n, finger=f)
            lh.add(m, finger=g)
        rh.bar(end=True), lh.bar(end=True)
        return grand(key, rh, lh)
    lh_notes = scale_notes(tonic, kind, lh_oct, octaves)
    lh_f = fingers(tonic, kind, "LH", octaves)
    n = 7 * octaves + 1
    if hands == "HS":
        scale_bars(rh, rh_notes, rh_f, kind, tonic)
        rh.bar(), rh.rest(str(n)), rh.bar(), rh.rest(str(n - 1)), rh.bar(end=True)
        lh.rest(str(n)), lh.bar(), lh.rest(str(n - 1)), lh.bar()
        scale_bars(lh, lh_notes, lh_f, kind, tonic)
        lh.bar(end=True)
    else:
        scale_bars(rh, rh_notes, rh_f, kind, tonic)
        scale_bars(lh, lh_notes, lh_f, kind, tonic)
        rh.bar(end=True), lh.bar(end=True)
    return grand(key, rh, lh)


# ---- chords ----

# quality -> [(letters, semitones)] above the root, in stacking order
QUALITY = {
    "": [(0, 0), (2, 4), (4, 7)], "m": [(0, 0), (2, 3), (4, 7)],
    "dim": [(0, 0), (2, 3), (4, 6)], "aug": [(0, 0), (2, 4), (4, 8)],
    "sus4": [(0, 0), (3, 5), (4, 7)], "sus2": [(0, 0), (1, 2), (4, 7)],
    "6": [(0, 0), (2, 4), (4, 7), (5, 9)], "m6": [(0, 0), (2, 3), (4, 7), (5, 9)],
    "7": [(0, 0), (2, 4), (4, 7), (6, 10)], "maj7": [(0, 0), (2, 4), (4, 7), (6, 11)],
    "m7": [(0, 0), (2, 3), (4, 7), (6, 10)], "mmaj7": [(0, 0), (2, 3), (4, 7), (6, 11)],
    "m7b5": [(0, 0), (2, 3), (4, 6), (6, 10)], "dim7": [(0, 0), (2, 3), (4, 6), (6, 9)],
    "add9": [(0, 0), (1, 2), (2, 4), (4, 7)],
    "9": [(0, 0), (2, 4), (4, 7), (6, 10), (1, 2)], "maj9": [(0, 0), (2, 4), (4, 7), (6, 11), (1, 2)],
    "m9": [(0, 0), (2, 3), (4, 7), (6, 10), (1, 2)],
}
CHORD_NAME_RE = re.compile(r"^([A-G][#b]?)(.*?)(?:/([A-G][#b]?))?$")


def chord_tones(name):
    """"G7/B" -> (["G", "B", "D", "F"], "B")."""
    root, quality, bass = CHORD_NAME_RE.match(name).groups()
    tones = [step(root, l, s) for l, s in QUALITY[quality]]
    return tones, bass or root


def stack(names, bottom_octave):
    notes = [(names[0], bottom_octave)]
    for name in names[1:]:
        notes.append(above(name, notes[-1]))
    return notes


def voicings(names, low, high):
    """Close voicings (every rotation) whose bottom note is in midi [low, high]."""
    out = []
    for r in range(len(names)):
        order = names[r:] + names[:r]
        for octave in range(1, 8):
            notes = stack(order, octave)
            if low <= midi(notes[0]) <= high:
                out.append(notes)
    return out


def movement(a, b):
    pa, pb = [midi(n) for n in a], [midi(n) for n in b]
    if len(pa) == len(pb):
        return sum(abs(x - y) for x, y in zip(sorted(pa), sorted(pb)))
    return sum(min(abs(x - y) for y in pa) for x in pb)


def lead(chords, low=57, high=67, center=64, first_root=True, rootless=False):
    """Right-hand voicings that move as little as possible from chord to chord."""
    out, prev = [], None
    for name in chords:
        tones, _ = chord_tones(name)
        if rootless and len(tones) > 3:
            tones = tones[1:]
        options = voicings(tones, low, high)
        if prev is None:
            if first_root:
                options = [v for v in options if v[0][0] == tones[0]] or options
            best = min(options, key=lambda v: abs(sum(map(midi, v)) / len(v) - center))
        else:
            best = min(options, key=lambda v: (movement(prev, v), abs(sum(map(midi, v)) / len(v) - center)))
        out.append(best)
        prev = best
    return out


def basses(chords, near=48, low=40, high=55):
    out, prev = [], near
    for name in chords:
        _, bass = chord_tones(name)
        options = [(bass, o) for o in range(1, 5) if low <= midi((bass, o)) <= high]
        note = min(options, key=lambda n: abs(midi(n) - prev))
        out.append(note)
        prev = midi(note)
    return out


# ---- roman numerals ----

RN_RE = re.compile(r"^(b|#)?(VII|VI|IV|V|III|II|I|vii|vi|iv|v|iii|ii|i)(o|ø|\+)?(maj7|maj9|7|6|9|sus4|sus2|add9)?$")
ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii"]


def roman(key, numeral):
    """Chord name of a numeral in a key: roman("C", "V7/V") -> "D7"; "V7@1" -> "G7/B"
    (@1 third in the bass, @2 fifth, @3 seventh)."""
    numeral, _, inversion = numeral.partition("@")
    numeral, _, target = numeral.partition("/")
    tonic, kind = key_parts(key)
    if target:
        tonic, kind = roman(key, target), "major"
        tonic = CHORD_NAME_RE.match(tonic).group(1)
    alter, deg, mark, ext = RN_RE.match(numeral).groups()
    d = ROMAN.index(deg.lower())
    use = "harmonic" if kind != "major" and deg == "vii" and not alter else kind
    root = scale_names(tonic, use)[d]
    if alter:
        root = spell(root[0], pc(root) + (1 if alter == "#" else -1))
    upper = deg.isupper()
    ext = ext or ""
    if mark == "o":
        q = "dim7" if ext == "7" else "dim"
    elif mark == "ø":
        q = "m7b5"
    elif mark == "+":
        q = "aug"
    elif upper:
        q = ext
    else:
        q = {"": "m", "7": "m7", "maj7": "mmaj7", "6": "m6", "9": "m9"}[ext]
    name = root + q
    if inversion:
        name += "/" + chord_tones(name)[0][int(inversion)]
    return name


# ---- progressions ----

def progression_abc(key, chords, pattern="block", rootless=False, tempo=None):
    """Two-hand ABC of a chord progression: one chord per bar, names above."""
    rh_chords = lead(chords, rootless=rootless)
    bass = basses(chords)
    rh, lh = Voice(key), Voice(key)
    meter = "3/4" if pattern == "waltz" else None
    for i, (name, v, b) in enumerate(zip(chords, rh_chords, bass)):
        tones, _ = chord_tones(name)
        fifth = above(tones[2] if len(tones) > 2 else tones[-1], b)
        third = above(tones[1], b)
        if pattern == "block":
            rh.add(v, "4", label=name), lh.add(b, "4")
        elif pattern == "pulse":
            rh.add(v, label=name), rh.add(v), rh.add(v), rh.add(v), lh.add(b, "4")
        elif pattern == "158":
            rh.add(v, "4", label=name)
            for n in (b, fifth, (b[0], b[1] + 1), fifth):
                lh.add(n)
        elif pattern == "ballad":
            rh.add(v, "2", label=name), rh.add(v, "2")
            tenth = (third[0], third[1] + 1)
            for n in (b, fifth, (b[0], b[1] + 1), tenth):
                lh.add(n)
        elif pattern == "waltz":
            rh.rest(), rh.add(v, label=name), rh.add(v), lh.add(b, "3")
        elif pattern == "pop":
            rh.add(v, "3/2", label=name), rh.add(v, "3/2"), rh.add(v), lh.add(b, "2"), lh.add(b, "2")
        elif pattern == "alberti":
            rh.add(v, "4", label=name)
            low = lead([name], low=45, high=55, center=50)[0][:3]
            for k in (0, 2, 1, 2, 0, 2, 1, 2):
                lh.add(low[k], "/")
            eighths = lh.tokens[-8:]  # no spaces between them: beamed in fours
            lh.tokens[-8:] = ["".join(eighths[:4]), "".join(eighths[4:])]
        elif pattern == "shell":  # LH root + 7th (or 3rd), RH the rest
            guide = tones[3] if len(tones) > 3 else tones[1]
            rh.add(v, "4", label=name), lh.add([b, above(guide, b)], "4")
        else:
            raise ValueError(pattern)
        last = i == len(chords) - 1
        rh.bar(end=last), lh.bar(end=last)
        if i % 4 == 3 and not last:  # 4 bars per staff line
            rh.tokens.append("\n"), lh.tokens.append("\n")
    return grand(key, rh, lh, meter=meter, tempo=tempo)


def chord_triads_abc(key, chords, hand="RH", root_position=True, length="2"):
    """Chords one after another, root position (or led), for one hand on one staff."""
    v = Voice(key)
    if root_position:
        voicing = [stack(chord_tones(c)[0], 4 if hand == "RH" else 3) for c in chords]
    else:
        voicing = lead(chords) if hand == "RH" else lead(chords, low=45, high=55, center=50)
    for c, notes in zip(chords, voicing):
        v.add(notes, length, label=c)
    v.bar(end=True)
    return single(key, v, "treble" if hand == "RH" else "bass")


def arpeggio_abc(chord, octaves=2, key=None):
    tones, _ = chord_tones(chord)
    key = key or (chord if chord.endswith("m") or chord in RH_MAJOR else "C")
    rh, lh = Voice(key), Voice(key)
    white = chord[0] in "CDEFGAB" and len(chord.rstrip("m")) == 1 and chord.rstrip("m") in "CFGADE"
    rh_n = stack(tones * octaves + [tones[0]], 4)
    lh_n = stack(tones * octaves + [tones[0]], 3 if octaves == 1 else 2)
    rf = ([1, 2, 3] * octaves + [5]) if white else [None] * len(rh_n)
    lf = ([5, 4, 2] + [1, 4, 2] * (octaves - 1) + [1]) if white else [None] * len(lh_n)
    for v, notes, f in ((rh, rh_n, rf), (lh, lh_n, lf)):
        for n, g in zip(notes, f):
            v.add(n, "/", finger=g)
        v.bar()
        for n, g in list(zip(notes, f))[-2::-1]:
            v.add(n, "/", finger=g)
        v.add([notes[0]] + [above(t, notes[0]) for t in tones[1:]], "2", label=chord if v is rh else None)
        v.bar(end=True)
    rh.tokens[0] = f'"{chord}"' + rh.tokens[0]
    return grand(key, rh, lh)


def chord_line(chords, numerals=None, width=None):
    """Aligned text lines: chord names, and the numerals under them."""
    cells = [max(len(c), len(n)) + 2 for c, n in zip(chords, numerals or chords)]
    top = "".join(c.ljust(w) for c, w in zip(chords, cells)).rstrip()
    if not numerals:
        return top
    return top + "\n" + "".join(n.ljust(w) for n, w in zip(numerals, cells)).rstrip()


if __name__ == "__main__":
    assert scale_names("F#") == ["F#", "G#", "A#", "B", "C#", "D#", "E#"]
    assert scale_names("G#", "harmonic")[6] == "F##"
    assert scale_names("Eb") == ["Eb", "F", "G", "Ab", "Bb", "C", "D"]
    assert fingers("C", "major", "LH", 2) == [5, 4, 3, 2, 1, 3, 2, 1, 4, 3, 2, 1, 3, 2, 1]
    assert fingers("C", "major", "RH", 2) == [1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 4, 5]
    assert roman("C", "V7/V") == "D7" and roman("C", "V7@1") == "G7/B"
    assert roman("Am", "viio7") == "G#dim7" and roman("Am", "V") == "E" and roman("C", "viio") == "Bdim"
    assert roman("C", "bVII") == "Bb" and roman("Bb", "ii7") == "Cm7" and roman("C", "iiø7") == "Dm7b5"
    assert chord_tones("Bm7b5")[0] == ["B", "D", "F", "A"]
    v = Voice("Am")
    v.add(("G#", 4)), v.add(("G", 4)), v.bar(), v.add(("G#", 4))
    assert v.text() == "^G =G | ^G"
    # I-IV-V-I in C: the common tone stays (C - F/C - G/B - C)
    lc = lead(["C", "F", "G", "C"])
    assert [midi(n) for n in lc[1]] == [60, 65, 69], lc
    print("music.py ok")
