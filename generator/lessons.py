"""The lessons of the harmony course, as data. make_book.py writes them as songs."""

from music import (arpeggio_abc, chord_line, chord_triads_abc, grand, progression_abc, roman, scale_abc,
                   scale_names, signature_text, Voice)

KIND_NAME = {"major": "mayor", "natural": "menor natural", "harmonic": "menor armónica", "melodic": "menor melódica"}


def part(title, minutes, text, abc=None, chords=None):
    return dict(title=title, minutes=minutes, text=text, abc=abc, chords=chords)


def scale(tonic, kind="major", hands="HS", octaves=1, contrary=False, minutes=10, extra=""):
    """A scale part: staff with fingers and a text made from the scale itself."""
    names = scale_names(tonic, kind)
    key = tonic + ("" if kind == "major" else "m")
    how = "movimiento contrario" if contrary else ("manos separadas" if hands == "HS" else "manos juntas")
    octs = "1 octava" if octaves == 1 else f"{octaves} octavas"
    title = f"Escala de {tonic} {KIND_NAME[kind]}, {how} ({octs})"
    notes = " ".join(names + [names[0]])
    text = f"""
    |Armadura: {signature_text(key)}.
    |Notas: {notes}
    """
    if kind == "melodic":
        text += "\nSube con 6ª y 7ª elevadas y baja como la menor natural.\n"
    if kind == "harmonic":
        text += f"\nLa 7ª ({names[6]}) está elevada: no está en la armadura y se escribe con alteración.\n"
    text += f"""
    Los números sobre las notas son los dedos (1 pulgar, 5 meñique).
    {extra}
    ## Cómo practicar
    - Escucha primero con ▶.
    - {"Primero la mano derecha (compases 1-2), luego la izquierda (3-4)." if hands == "HS" and not contrary else "Las dos manos a la vez, cada una con sus dedos."}
    - Muy lento, legato, mirando los cambios de dedo (cuando el pulgar pasa por debajo o un dedo cruza por encima).
    - Meta: 4 veces seguidas sin parar ni equivocarte. Luego sube la velocidad un poco.
    """
    return part(title, minutes, text, scale_abc(tonic, kind, hands, octaves, contrary))


def arpeggio(chord, octaves=2, minutes=8):
    text = f"""
    Un arpegio es el acorde tocado nota a nota: {chord} subiendo y bajando, y al final el acorde entero.
    Mano derecha arriba, izquierda abajo: practica cada mano sola y luego juntas.
    El pulgar pasa por debajo para empezar la siguiente octava; la muñeca se mueve en línea, sin saltos.
    Si no hay dedos escritos: pulgar siempre en tecla blanca, y busca la digitación que te deje pasar el pulgar sin girar la mano.
    """
    return part(f"Arpegio de {chord} ({octaves} octavas)", minutes, text, arpeggio_abc(chord, octaves))


def prog(title, minutes, text, key, items, pattern="block", rootless=False, numerals=True):
    """A progression part. `items` are roman numerals (in `key`) or chord names."""
    is_rn = items[0].lstrip("b#")[0] in "IViv"
    chords = [roman(key, i) for i in items] if is_rn else list(items)
    shown = [i.replace("@1", "").replace("@2", "").replace("@3", "") for i in items] if is_rn else None
    lines = []
    for k in range(0, len(chords), 4):  # 4 per line keeps lines short on a phone
        lines.append(chord_line(chords[k:k + 4], shown[k:k + 4] if numerals and shown else None))
    return part(title, minutes, text, progression_abc(key, chords, pattern, rootless), "\n\n".join(lines))


def chords_part(title, minutes, text, key, chords, hand="RH", root_position=True, numerals=None):
    abc = chord_triads_abc(key, chords, hand, root_position)
    return part(title, minutes, text, abc, chord_line(chords, numerals))


def abc_part(title, minutes, text, abc, chords=None):
    return part(title, minutes, text, abc, chords)


def notes_abc(key, groups, length="", clef="treble"):
    """Staff from ABC note groups written by hand (each group one bar)."""
    return f"K:{key} clef={clef}\n" + rows(" | ".join(groups) + " |]")


ODE = ('"C"E E F G | "G"G F E D | "C"C C D E | "G"E3/2 D/ D2 | '
       '"C"E E F G | "G"G F E D | "C"C C D E | "G"D3/2 C/ "C"C2 |]')
ODE_PLAIN = 'E E F G | G F E D | C C D E | E3/2 D/ D2 | E E F G | G F E D | C C D E | D3/2 C/ C2 |]'
ODE_LH = '[C,E,G,]4 | [B,,D,G,]4 | [C,E,G,]4 | [B,,D,G,]4 | [C,E,G,]4 | [B,,D,G,]4 | [C,E,G,]4 | [B,,D,G,]2 [C,E,G,]2 |]'
SILENT = ('"C"G3/2 A/ G E3 | "C"G3/2 A/ G E3 | "G"d2 d B3 | "C"c2 c G3 | "F"A2 A c3/2 B/ A | '
          '"C"G3/2 A/ G E3 | "F"A2 A c3/2 B/ A | "C"G3/2 A/ G E3 | "G7"d2 d f3/2 d/ B | "C"c3 e3 | '
          '"C"c3/2 G/ E "G7"G3/2 F/ D | "C"C6 |]')
SILENT_PLAIN = ('G3/2 A/ G E3 | G3/2 A/ G E3 | d2 d B3 | c2 c G3 | A2 A c3/2 B/ A | G3/2 A/ G E3 | '
                'A2 A c3/2 B/ A | G3/2 A/ G E3 | d2 d f3/2 d/ B | c3 e3 | c3/2 G/ E G3/2 F/ D | C6 |]')


SILENT_LH = ('[C,E,G,]6 | [C,E,G,]6 | [B,,F,G,]6 | [C,E,G,]6 | [C,F,A,]6 | [C,E,G,]6 | [C,F,A,]6 | [C,E,G,]6 | '
             '[B,,F,G,]6 | [C,E,G,]6 | [C,E,G,]3 [B,,F,G,]3 | [C,E,G,]6 |]')


def rows(abc, bars=4):
    """A staff line break after every `bars` bars, so a phone shows the notes big enough."""
    parts = abc.split(" | ")
    return " |\n".join(" | ".join(parts[i:i + bars]) for i in range(0, len(parts), bars))


def two_hands(key, rh_text, lh_text, meter=None, length=None):
    rh, lh = Voice(key), Voice(key)
    rh.tokens, lh.tokens = [rows(rh_text)], [rows(lh_text)]
    abc = grand(key, rh, lh, meter=meter)
    return abc.replace(f"K:{key}", (f"L:{length}\n" if length else "") + f"K:{key}")


INTRO = part("Cómo usar este curso", 5, """
    Lecciones de unos 30 minutos, de lo más fácil a lo más difícil. Haz una o dos por semana, en orden.
    Cada lección tiene partes (a, b, c...) con los minutos que llevan. Si una parte no sale, repítela al día siguiente antes de seguir: es normal.
    ## En cada parte
    - El pentagrama de arriba es la mano derecha (clave de sol); el de abajo, la izquierda (clave de fa).
    - Los números pequeños sobre las notas son los dedos: 1 pulgar, 2 índice, 3 medio, 4 anular, 5 meñique.
    - El botón ▶ toca el ejercicio y marca cada nota. Escucha antes de tocar.
    - Los nombres de los acordes (C, Dm, G7...) están sobre el pentagrama y en las líneas de acordes.
    - Los números romanos (I, IV, V...) dicen qué grado de la escala es cada acorde: así una progresión sirve en todas las tonalidades.
    ## Transportar
    El botón de transportar de cada parte mueve el pentagrama y los acordes a otra tonalidad. Úsalo para tocar las progresiones en todas las tonalidades. Ojo: los números de dedos no cambian, y en otra tonalidad pueden no servir.
    ## Rutina de 30 minutos
    - 5 min: calentar con la escala de la lección anterior.
    - 20 min: las partes nuevas, en orden.
    - 5 min: tocar algo que te guste del cancionero con lo aprendido.
    ## Nombres de las notas
    |C  D  E  F  G  A  B
    Do Re Mi Fa Sol La Si
    """)

# Blocks: (tag id, label, [lessons]); a lesson: (title, [parts]).
BLOCKS = []


def block(tag, label, lessons):
    BLOCKS.append((tag, label, lessons))


block("fundamentos", "1 · Fundamentos", [
    ("El teclado y la escala de C", [
        abc_part("Geografía del teclado", 5, """
            Las teclas negras van en grupos de 2 y de 3. La tecla blanca justo a la izquierda de cada grupo de 2 negras es C (Do).
            Desde C, las blancas son C D E F G A B y vuelve a empezar. El C más cercano al centro del piano es el C central (el C del pentagrama).
            Toca todos los C del piano, luego todos los F (a la izquierda del grupo de 3 negras). Después di y toca las 7 notas subiendo desde el C central.
            """, notes_abc("C", ["C D E F G A B c"])),
        scale("C", hands="HS", minutes=10, extra="Mano derecha: tras el 3 (en E), el pulgar pasa por debajo hasta F. Mano izquierda: tras el pulgar (en G), el 3 cruza por encima hasta A."),
        abc_part("Tono y semitono", 5, """
            Un semitono es la distancia de una tecla a la de al lado (sin saltar ninguna, blanca o negra). Un tono son dos semitonos.
            Entre E-F y entre B-C no hay tecla negra: son semitonos. Las demás blancas vecinas están a un tono.
            Toca y escucha: C-D (tono), E-F (semitono), A-B (tono), B-C (semitono). El semitono suena más "apretado".
            """, notes_abc("C", ["C2 D2", "E2 F2", "A2 B2", "B2 c2"])),
        abc_part("Pulso y mano quieta", 10, """
            Posición de 5 dedos: mano derecha con el pulgar en C y un dedo por tecla hasta G; mano izquierda con el meñique en C (una octava abajo) hasta G.
            Toca este ejercicio con las dos manos a la vez, contando 1-2-3-4 en voz alta. Los dedos curvos, la muñeca suelta.
            """, two_hands("C", "!1!C !2!D !3!E !4!F | !5!G !4!F !3!E !2!D | !1!C4 |]",
                           "!5!C, !4!D, !3!E, !2!F, | !1!G, !2!F, !3!E, !4!D, | !5!C,4 |]")),
    ]),
    ("La escala mayor y G mayor", [
        abc_part("La fórmula de la escala mayor", 5, """
            Toda escala mayor tiene los mismos pasos: tono, tono, semitono, tono, tono, tono, semitono.
            |T  T  S  T  T  T  S
            En C sale con solo teclas blancas. Si empiezas en G, para cumplir la fórmula el F tiene que subir a F#.
            Por eso G mayor tiene un sostenido. Cada escala mayor tiene su armadura: las alteraciones que la fórmula necesita.
            """, notes_abc("G", ["G A B c d e f g"])),
        scale("G", hands="HS", extra="La misma digitación que C. En la mano derecha el F# lo toca el 4."),
        scale("C", hands="HT", contrary=True, minutes=7, extra="Movimiento contrario: las manos se alejan en espejo, con los mismos dedos a la vez. Es la forma más fácil de empezar con manos juntas."),
        scale("C", hands="HT", minutes=8, extra="Manos juntas en paralelo: los pasos del pulgar no coinciden. Para en cada cambio de dedo si hace falta."),
    ]),
    ("Intervalos", [
        abc_part("Contar intervalos", 10, """
            Un intervalo es la distancia entre dos notas, contada por nombres de nota: de C a E hay 3 nombres (C, D, E), así que es una 3ª.
            Toca desde C: 2ª (D), 3ª (E), 4ª (F), 5ª (G), 6ª (A), 7ª (B), 8ª u octava (C).
            Primero una nota tras otra, luego las dos a la vez. Escucha cuáles suenan tranquilas (3ª, 5ª, 6ª, 8ª) y cuáles tensas (2ª, 7ª).
            """, notes_abc("C", ["C D [CD]2", "C E [CE]2", "C F [CF]2", "C G [CG]2", "C A [CA]2", "C B [CB]2", "C c [Cc]2"])),
        abc_part("Terceras mayores y menores", 5, """
            Hay dos terceras: la mayor (4 semitonos, como C-E) y la menor (3 semitonos, como D-F).
            La mayor suena luminosa; la menor, más oscura. Son las piezas de los acordes: aprender a oírlas es la base de todo.
            Toca las terceras de la escala de C: C-E mayor, D-F menor, E-G menor, F-A mayor, G-B mayor, A-C menor, B-D menor.
            """, notes_abc("C", ["[CE]2 [DF]2 [EG]2 [FA]2", "[GB]2 [Ac]2 [Bd]2 [ce]2"])),
        scale("G", hands="HT", minutes=10),
        abc_part("Quintas en la mano izquierda", 5, """
            La 5ª justa (7 semitonos, C-G) suena vacía y fuerte: es el sonido de los bajos de rock y del acompañamiento más simple.
            Con la mano izquierda (5 en la nota de abajo, 1 en la de arriba) toca quintas sobre C, F, G y C.
            """, notes_abc("C", ['"C"[C,G,]4', '"F"[F,C]4', '"G"[G,D]4', '"C"[C,G,]4'], clef="bass")),
    ]),
    ("La tríada: mayor y menor", [
        chords_part("El acorde mayor", 8, """
            Una tríada son tres notas en terceras: raíz, 3ª y 5ª. Mayor: una 3ª mayor y encima una 3ª menor (C-E-G).
            Mano derecha con dedos 1-3-5. Toca cada acorde, escucha, y nómbralo en voz alta.
            C, F y G son todo teclas blancas. D, E y A tienen la nota del medio negra.
            """, "C", ["C", "F", "G", "D", "E", "A"]),
        chords_part("El acorde menor", 8, """
            Menor: primero la 3ª menor y encima la mayor (A-C-E). Basta con bajar un semitono la nota del medio de un acorde mayor: C se vuelve Cm.
            Dm, Em y Am son de teclas blancas. Toca cada par mayor-menor y escucha el cambio de color.
            """, "C", ["C", "Cm", "D", "Dm", "E", "Em", "A", "Am"]),
        scale("F", hands="HS", extra="F es diferente: en la mano derecha el pulgar pasa después del 4 (en Bb), porque el pulgar nunca toca una negra."),
        chords_part("Acordes con la mano izquierda", 4, """
            Los mismos acordes con la mano izquierda (dedos 5-3-1). Fíjate: el meñique toca la raíz.
            """, "C", ["C", "Am", "F", "G"], hand="LH"),
    ]),
    ("Los siete acordes de C", [
        chords_part("Un acorde sobre cada nota", 8, """
            Si haces una tríada sobre cada nota de la escala de C usando solo sus notas, salen 7 acordes: los acordes diatónicos de C.
            Tres son mayores (C, F, G), tres menores (Dm, Em, Am) y uno disminuido (Bdim).
            Súbelos y bájalos con la mano derecha, dedos 1-3-5 sin cambiar la forma de la mano.
            """, "C", ["C", "Dm", "Em", "F", "G", "Am", "Bdim"], numerals=["I", "ii", "iii", "IV", "V", "vi", "vii°"]),
        abc_part("Números romanos", 5, """
            Cada acorde se nombra con el número de su nota en la escala: mayúscula si es mayor, minúscula si es menor, ° si es disminuido.
            |I  ii  iii  IV  V  vi  vii°
            Este patrón es el mismo en todas las tonalidades mayores. En G: G Am Bm C D Em F#dim. Por eso los músicos hablan de "un I-IV-V" sin decir el tono.
            """, chord_triads_abc("G", ["G", "Am", "Bm", "C", "D", "Em", "F#dim"]), chord_line(["G", "Am", "Bm", "C", "D", "Em", "F#dim"], ["I", "ii", "iii", "IV", "V", "vi", "vii°"])),
        chords_part("El acorde disminuido y el aumentado", 5, """
            Disminuido: dos 3ª menores (B-D-F). Suena tenso, inestable: quiere ir a algún sitio.
            Aumentado: dos 3ª mayores (C-E-G#). Suena a suspense, de película.
            Compara C, Cm, Cdim y Caug: solo se mueven la 3ª y la 5ª.
            """, "C", ["C", "Cm", "Cdim", "Caug"]),
        scale("F", hands="HT", minutes=12),
    ]),
    ("Primer acompañamiento: I, IV y V", [
        prog("Los acordes primarios", 8, """
            I, IV y V son los acordes principales de una tonalidad: con ellos se acompañan miles de canciones.
            Mano izquierda: la raíz. Mano derecha: el acorde en estado fundamental. Cuenta 4 por acorde.
            """, "C", ["I", "IV", "V", "I"]),
        prog("Ritmo de negras", 7, """
            Ahora la mano derecha toca el acorde en cada pulso (4 veces por compás) y la izquierda sostiene la raíz.
            Mantén el pulso aunque el cambio no salga perfecto: es mejor un acorde tarde que parar.
            """, "C", ["I", "I", "IV", "IV", "V", "V", "I", "I"], pattern="pulse"),
        abc_part("Oda a la alegría", 10, """
            Melodía de Beethoven con dos acordes: C y G. Paso 1: toca la melodía con la derecha. Paso 2: la melodía con la derecha y la raíz del acorde con la izquierda (C o G) al principio de cada compás.
            Paso 3: la izquierda toca los acordes completos, como en el pentagrama.
            """, two_hands("C", ODE, ODE_LH)),
        scale("D", hands="HS", minutes=5, extra="Dos sostenidos: F# y C#. La digitación de C sirve."),
    ]),
])

block("inversiones", "2 · Inversiones y conducción", [
    ("Inversiones", [
        chords_part("Las tres posiciones de C", 8, """
            Las mismas notas en otro orden: fundamental (C-E-G), 1ª inversión (E-G-C) y 2ª inversión (G-C-E).
            Sigue siendo C. La nota de abajo cambia el color: la 1ª inversión suena más ligera; la 2ª, abierta.
            Dedos mano derecha: fundamental 1-3-5, 1ª inversión 1-2-5, 2ª inversión 1-3-5.
            """, "C", ["C", "C/E", "C/G", "C"], root_position=False),
        abc_part("Subir por inversiones", 10, """
            Sube y baja C, F y G por sus tres posiciones, sin mirar las manos. Luego lo mismo con Am, Dm y Em.
            Así encuentras cualquier acorde en cualquier zona del teclado.
            """, notes_abc("C", ['"C"[CEG]', "[EGc]", "[Gce]", "[ceg]2", '"F"[FAc]', "[Acf]", "[cfa]", "[fac']2", '"G"[G,B,D]', "[B,DG]", "[DGB]", "[GBd]2"])),
        scale("D", hands="HT", minutes=12),
    ]),
    ("Conducir las voces: el camino más corto", [
        prog("La regla de la nota común", 10, """
            Para cambiar de acorde sin saltar: la nota que comparten los dos acordes se queda quieta y las demás se mueven a la nota más cercana.
            I-IV-V-I en C: el C se queda en F (F/C), y para ir a G el acorde baja a G/B. Casi no se mueve la mano y suena unido, como un coro.
            """, "C", ["I", "IV", "V", "I"]),
        prog("I-IV-V-I en G", 5, """
            La misma idea en G. Busca tú las inversiones antes de mirar el pentagrama.
            """, "G", ["I", "IV", "V", "I"]),
        prog("I-IV-V-I en F", 5, """
            Y en F. Luego usa el botón de transportar para tocarlo en D y en A.
            """, "F", ["I", "IV", "V", "I"]),
        scale("A", hands="HS", minutes=10, extra="Tres sostenidos: F#, C#, G#."),
    ]),
    ("La progresión pop: I-V-vi-IV", [
        prog("I-V-vi-IV en C", 8, """
            C G Am F: la progresión de cientos de canciones pop y de alabanza. Mano derecha con conducción de voces, izquierda en la raíz.
            """, "C", ["I", "V", "vi", "IV"]),
        prog("Bajo 1-5-8-5", 10, """
            La mano izquierda toca raíz, 5ª, octava y 5ª (una negra cada una) mientras la derecha sostiene el acorde.
            Mano izquierda dedos 5-2-1-2. Da movimiento sin complicar la derecha.
            """, "C", ["I", "V", "vi", "IV"], pattern="158"),
        prog("En G y en D", 5, """
            G D Em C. Después transporta a D: D A Bm G. Son los mismos números.
            """, "G", ["I", "V", "vi", "IV"], pattern="158"),
        scale("A", hands="HT", minutes=7),
    ]),
    ("Arpegios", [
        arpeggio("C", minutes=10),
        arpeggio("G", minutes=5),
        arpeggio("Am", minutes=5),
        scale("E", hands="HS", minutes=10, extra="Cuatro sostenidos: F#, C#, G#, D#."),
    ]),
    ("La escala menor", [
        scale("A", "natural", hands="HS", minutes=7,
              extra="A menor es la relativa de C mayor: mismas notas, empieza en la 6ª nota de C. Toda escala mayor tiene su relativa menor una 3ª menor por debajo."),
        scale("A", "harmonic", hands="HS", minutes=8,
              extra="Con G# el acorde sobre E es mayor (E) y el G# empuja hacia A: así la tonalidad menor tiene una dominante fuerte."),
        scale("A", "melodic", hands="HS", minutes=7),
        scale("E", hands="HT", minutes=8),
    ]),
    ("Progresiones en menor", [
        chords_part("Los acordes de A menor", 7, """
            Con la escala armónica: Am Bdim C Dm E F G#dim. El V es mayor (E) gracias al G#.
            En las canciones también se usa G (de la menor natural) como VII.
            """, "Am", ["Am", "Bdim", "C", "Dm", "E", "F", "G#dim"], numerals=["i", "ii°", "III", "iv", "V", "VI", "vii°"]),
        prog("i-iv-V-i", 7, """
            Am Dm E Am: la cadencia menor clásica. Escucha cómo el G# del E pide volver a A.
            """, "Am", ["i", "iv", "V", "i"]),
        prog("La cadencia andaluza", 8, """
            Am G F E: baja paso a paso hasta el V. Es el sonido del flamenco. Repítela en bucle, con la izquierda en 1-5-8-5.
            """, "Am", ["i", "bVII", "bVI", "V"], pattern="158", numerals=False),
        scale("A", "harmonic", hands="HT", minutes=8),
    ]),
])

block("funciones", "3 · Armonía funcional", [
    ("Tónica, subdominante, dominante", [
        abc_part("Tres familias de acordes", 8, """
            Cada acorde tiene una función:
            - Tónica (reposo, casa): I, vi, iii.
            - Subdominante (salir de casa): IV, ii.
            - Dominante (tensión, quiere volver): V, vii°.
            El orden natural es tónica, subdominante, dominante, tónica. Por eso funciona I-IV-V-I, y también I-ii-V-I o I-vi-IV-V.
            """, chord_triads_abc("C", ["C", "Am", "F", "Dm", "G", "Bdim", "C"]), chord_line(["C", "Am", "F", "Dm", "G", "Bdim", "C"], ["T", "T", "S", "S", "D", "D", "T"])),
        prog("I-vi-ii-V", 7, """
            Sustituye cada acorde por otro de su familia: en lugar de I-I-IV-V, toca I-vi-ii-V. El famoso cambio de los años 50.
            """, "C", ["I", "vi", "ii", "V", "I", "vi", "ii", "V"]),
        prog("ii-V-I", 5, """
            Dm G C: el camino más fuerte hacia la tónica. Practícalo en C y transpórtalo a G y F.
            """, "C", ["ii", "V", "I", "I"]),
        scale("E", "harmonic", hands="HS", minutes=10, extra="E menor, relativa de G mayor. La 7ª elevada es D#."),
    ]),
    ("Cadencias", [
        prog("Cadencia auténtica: V-I", 6, """
            Dominante a tónica: el final más claro. Termina casi cualquier canción.
            """, "C", ["I", "IV", "V", "I"]),
        prog("Cadencia plagal: IV-I", 6, """
            El "amén" de los himnos. Más suave que la auténtica.
            """, "F", ["I", "IV", "I", "IV", "I"]),
        prog("Semicadencia y cadencia rota", 8, """
            Semicadencia: la frase para en el V, como una pregunta. Cadencia rota: V va a vi en lugar de a I; sorprende y alarga la canción.
            """, "C", ["I", "ii", "V", "V", "I", "IV", "V", "vi"]),
        scale("E", "harmonic", hands="HT", minutes=10),
    ]),
    ("Leer un cancionero", [
        part("Acordes sobre la letra", 8, """
            En un cancionero el acorde se escribe encima de la sílaba donde cambia. Lo tocas justo en esa sílaba y lo mantienes hasta el siguiente.
            Toca estos acordes a pulso lento (un acorde por compás), cantando o diciendo la letra.
            """, chords=chord_line(["C", "G", "Am", "F"]) + "\nCanto al sol que sale cada día,\n" + chord_line(["C", "G", "F", "C"]) + "\ncanto al mar que nunca se detiene."),
        abc_part("Encontrar la tonalidad", 7, """
            Pistas: el primer y el último acorde suelen ser el I. El acorde mayor que aparece justo antes del I suele ser el V.
            Si ves C, F, G y Am: tono de C. Si ves G, C, D y Em: tono de G. Con D, G, A y Bm: tono de D.
            Abre una canción del cancionero y di en qué tono está y qué número tiene cada acorde.
            """, chord_triads_abc("D", ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"]), chord_line(["D", "Em", "F#m", "G", "A", "Bm", "C#dim"], ["I", "ii", "iii", "IV", "V", "vi", "vii°"])),
        part("Transportar con números", 5, """
            Para cambiar una canción de tono: escribe sus acordes como números, y vuelve a ponerles nombre en el tono nuevo.
            Ejemplo: C G Am F en C es I V vi IV; en D es D A Bm G. El botón de transportar lo hace solo, pero entenderlo te deja tocar de oído.
            """, chords=chord_line(["C", "G", "Am", "F"], ["I", "V", "vi", "IV"]) + "\n\n" + chord_line(["D", "A", "Bm", "G"], ["I", "V", "vi", "IV"])),
        scale("B", hands="HS", minutes=10, extra="Cinco sostenidos. La mano izquierda empieza con el 4 en B."),
    ]),
    ("Patrones de acompañamiento", [
        prog("Balada", 8, """
            Izquierda: 1-5-8-10 (raíz, 5ª, octava y la 3ª de arriba). Derecha: el acorde en blancas. Es amplio y suena a piano de balada.
            """, "C", ["I", "vi", "IV", "V"], pattern="ballad"),
        prog("Vals en 3/4", 7, """
            Izquierda la raíz en el pulso 1; derecha el acorde en 2 y 3: bum-chas-chas.
            """, "F", ["I", "IV", "V7", "I"], pattern="waltz"),
        prog("Bajo Alberti", 8, """
            Acorde partido en la izquierda: abajo-arriba-medio-arriba, en corcheas. Es el acompañamiento de Mozart. Empieza muy lento y con la mano relajada.
            """, "C", ["I", "IV", "V", "I"], pattern="alberti"),
        prog("Ritmo pop 3-3-2", 7, """
            La derecha toca en 1, en el "y" del 2 y en el 4: tres, tres, dos corcheas. La izquierda en 1 y 3. Cuenta "1 y 2 y 3 y 4 y" en voz alta.
            """, "G", ["I", "V", "vi", "IV"], pattern="pop"),
    ]),
    ("Acordes sus y add", [
        prog("sus4 y sus2", 8, """
            sus4: la 3ª sube a la 4ª (C-F-G). sus2: la 3ª baja a la 2ª (C-D-G). No son ni mayores ni menores: suenan abiertos.
            El sus4 suele resolver a su acorde normal: Csus4 a C, Gsus4 a G.
            """, "C", ["Csus4", "C", "Gsus4", "G", "Fsus2", "F", "Csus4", "C"]),
        prog("add9", 7, """
            Al acorde se le añade la 9ª (la 2ª una octava arriba; en la mano derecha, pegada a la raíz). Cadd9 = C-D-E-G. Brillo moderno sin cambiar la función.
            """, "C", ["Cadd9", "Gsus4", "Am", "Fadd9"]),
        scale("B", hands="HT", minutes=15),
    ]),
    ("Bajos con barra y líneas de bajo", [
        prog("Acordes con barra", 5, """
            C/E significa acorde de C con E en el bajo: es una inversión escrita en el cancionero. La izquierda toca la nota después de la barra.
            """, "C", ["C", "C/E", "F", "G/B", "C"]),
        prog("Bajo que baja", 10, """
            C C/B Am Am/G F C/E Dm G: el bajo baja la escala nota a nota mientras los acordes cambian. Uno de los recursos más bonitos del piano.
            """, "C", ["C", "C/B", "Am", "Am/G", "F", "C/E", "Dm", "G"]),
        prog("Bajo que sube", 5, """
            C Dm C/E F G: el bajo sube de C a G. Útil para levantar un estribillo.
            """, "C", ["C", "Dm", "C/E", "F", "G"]),
        scale("Bb", hands="HS", minutes=10, extra="Dos bemoles. Mano derecha empieza con el 4 en Bb; izquierda con el 3."),
    ]),
    ("Dominantes secundarias", [
        prog("El V del V", 8, """
            D7 en tono de C no es del tono (tiene F#), pero lleva a G como si G fuera el I: es la dominante de la dominante, V/V.
            C D7 G C: el F# empuja hacia G.
            """, "C", ["I", "V7/V", "V", "I"]),
        prog("V/vi, V/ii y V/IV", 10, """
            Cualquier acorde del tono puede tener su propia dominante: E7 lleva a Am (V/vi), A7 a Dm (V/ii), C7 a F (V/IV).
            """, "C", ["I", "V7/vi", "vi", "V7/ii", "ii", "V7", "I", "V7/IV", "IV", "V7", "I"]),
        prog("Cadena de dominantes", 4, """
            E7 A7 D7 G7 C: cada acorde es la dominante del siguiente. Va bajando por quintas hasta casa.
            """, "C", ["E7", "A7", "D7", "G7", "C"]),
        scale("Bb", hands="HT", minutes=8),
    ]),
    ("Préstamos del modo menor", [
        prog("El iv menor", 8, """
            En tono mayor, cambiar el IV por iv (F por Fm en C) da un golpe de nostalgia. C F Fm C: escucha el Ab.
            """, "C", ["I", "IV", "iv", "I"]),
        prog("bVII y bVI", 8, """
            Bb y Ab prestados de C menor. C Bb F C suena a rock; C Ab Bb C a final épico.
            """, "C", ["I", "bVII", "IV", "I", "I", "bVI", "bVII", "I"]),
        scale("Eb", hands="HS", minutes=14, extra="Tres bemoles: Bb, Eb, Ab. Derecha empieza con el 3; izquierda con el 3."),
    ]),
])

block("septimas", "4 · Acordes de séptima", [
    ("Los tipos de séptima", [
        chords_part("Cinco acordes de séptima", 8, """
            Añade otra 3ª encima de la tríada:
            - maj7 (C-E-G-B): suave, soñador.
            - 7 o dominante (C-E-G-Bb): tenso, quiere resolver.
            - m7 (C-Eb-G-Bb): cálido, relajado.
            - m7b5 o semidisminuido (C-Eb-Gb-Bb): oscuro.
            - dim7 (C-Eb-Gb-A): muy tenso, de suspense.
            """, "C", ["Cmaj7", "C7", "Cm7", "Cm7b5", "Cdim7"]),
        chords_part("Séptimas del tono de C", 8, """
            Sobre cada nota de la escala, con solo notas del tono: Cmaj7 Dm7 Em7 Fmaj7 G7 Am7 Bm7b5. Solo el V tiene una séptima dominante.
            """, "C", ["Cmaj7", "Dm7", "Em7", "Fmaj7", "G7", "Am7", "Bm7b5"], numerals=["Imaj7", "ii7", "iii7", "IVmaj7", "V7", "vi7", "viiø7"]),
        scale("Eb", hands="HT", minutes=14),
    ]),
    ("La séptima de dominante", [
        prog("El tritono resuelve", 8, """
            G7 tiene B y F: un tritono (3 tonos), el intervalo más tenso. Al ir a C, B sube a C y F baja a E. Ese movimiento es lo que da fuerza al V7-I.
            """, "C", ["I", "V7", "I", "IV", "V7", "I"]),
        prog("Inversiones de G7", 8, """
            G7/B, G7/D y G7/F: con la séptima (F) en el bajo, el bajo baja a E: G7/F va a C/E.
            """, "C", ["V7", "I", "V7@1", "I", "V7@2", "I", "V7@3", "I@1"]),
        scale("Ab", hands="HS", minutes=14, extra="Cuatro bemoles: Bb, Eb, Ab, Db."),
    ]),
    ("ii-V-I con séptimas", [
        prog("Notas guía", 8, """
            Dm7 G7 Cmaj7. Las notas guía de cada acorde son la 3ª y la 7ª: deciden su color. Aquí la derecha toca el acorde sin la raíz (que va en la izquierda) y casi no se mueve.
            """, "C", ["ii7", "V7", "Imaj7", "Imaj7"], rootless=True),
        prog("ii-V-I en F y Bb", 8, """
            Gm7 C7 Fmaj7 y luego Cm7 F7 Bbmaj7. Transpórtalo también a G y D.
            """, "F", ["ii7", "V7", "Imaj7", "Imaj7", "ii7/IV", "V7/IV", "IVmaj7", "IVmaj7"], rootless=True, numerals=False),
        prog("ii-V-i en menor", 6, """
            Bm7b5 E7 Am: el ii es semidisminuido y el V lleva la 7ª elevada (G#).
            """, "Am", ["iiø7", "V7", "i", "i"], rootless=True),
        scale("Ab", hands="HT", minutes=8),
    ]),
    ("Voicings a dos manos", [
        prog("Raíz y séptima abajo", 10, """
            Izquierda: raíz y séptima (una 7ª de distancia). Derecha: el resto, cerca del centro. Suena lleno, a piano de jazz o de alabanza moderna.
            """, "C", ["Imaj7", "vi7", "ii7", "V7"], pattern="shell", rootless=True),
        prog("Turnaround con ritmo", 8, """
            La misma vuelta Cmaj7 Am7 Dm7 G7 con ritmo 3-3-2 en la derecha. Repítela hasta que salga sin mirar.
            """, "C", ["Imaj7", "vi7", "ii7", "V7"], pattern="pop", rootless=True),
        scale("D", "harmonic", hands="HS", minutes=6, extra="D menor, relativa de F. 7ª elevada: C#."),
        scale("G", "harmonic", hands="HS", minutes=6, extra="G menor, relativa de Bb. 7ª elevada: F#."),
    ]),
    ("Disminuidos y aumentados", [
        prog("Disminuido de paso", 8, """
            C C#dim7 Dm7 G7: el C#dim7 une C y Dm subiendo un semitono. Un dim7 se repite cada 3 semitonos: solo hay 3 distintos.
            """, "C", ["C", "C#dim7", "Dm7", "G7", "C"]),
        prog("viiº7 en menor", 6, """
            G#dim7 a Am: la sensible (G#) sube a A. Funciona como dominante.
            """, "Am", ["i", "viio7", "i", "iv", "viio7", "i"]),
        prog("Línea cromática", 6, """
            Am Am(maj7) Am7 Am6: el acorde se queda y una voz baja de semitono en semitono (A, G#, G, F#). Muy usado en baladas.
            """, "Am", ["Am", "Ammaj7", "Am7", "Am6"]),
        scale("Db", hands="HS", minutes=10, extra="Cinco bemoles. Pulgares en C y F."),
    ]),
    ("Sextas y novenas", [
        chords_part("Acordes de 6ª y 9ª", 8, """
            C6 (C-E-G-A) es un final suave. Las novenas (C9, Cmaj9, Dm9) añaden la 9ª sobre la 7ª. En la derecha se toca sin la raíz.
            """, "C", ["C6", "Cmaj7", "Cmaj9", "Dm9", "G9"], root_position=False),
        prog("Progresión con color", 8, """
            Cmaj9 Am7 Dm9 G9: la misma armonía de I-vi-ii-V, ahora con color.
            """, "C", ["Cmaj9", "Am7", "Dm9", "G9", "Cmaj9"], rootless=True),
        scale("Db", hands="HT", minutes=14),
    ]),
])

block("clasica", "5 · Armonía clásica", [
    ("Escritura a cuatro voces", [
        abc_part("Soprano, contralto, tenor y bajo", 10, """
            En un coral cada acorde tiene 4 voces: soprano y contralto en la derecha, tenor y bajo en la izquierda. En tríadas se dobla la raíz.
            I-IV-V-I en C. Mira cómo cada voz se mueve poco: la contralto mantiene el G y el C cuando puede.
            """, two_hands("C", '"C"[Ge]4 | "F"[Af]4 | "G"[Gd]4 | "C"[Ge]4 |]',
                           '[C,C]4 | [F,C]4 | [G,,B,]4 | [C,C]4 |]')),
        part("Las reglas principales", 8, """
            - Nada de quintas ni octavas paralelas: dos voces no van de una 5ª (u 8ª) a otra igual.
            - La sensible (la 7ª de la escala) sube a la tónica.
            - La 7ª de un acorde baja por grado.
            - Las voces superiores, cuanto más quietas mejor; el bajo puede saltar.
            Toca el coral anterior cantando cada voz por separado mientras tocas las otras.
            """),
        scale("F#", hands="HS", minutes=12, extra="Seis sostenidos. Pulgares solo en B y E#."),
    ]),
    ("Inversiones en la armonía clásica", [
        prog("Bajo melódico con inversiones", 8, """
            I V6 I: C G/B C. La 1ª inversión (el 6 del cifrado) hace que el bajo se mueva por grados.
            """, "C", ["I", "V@1", "I", "IV", "I@1", "ii@1", "V", "I"]),
        prog("La 6/4 cadencial", 8, """
            C/G G7 C: antes del V7 final, el acorde de tónica en 2ª inversión (I6/4) sobre el bajo G. Es la firma de los finales clásicos.
            """, "C", ["I", "IV", "I@2", "V7", "I"]),
        scale("F#", hands="HT", minutes=14),
    ]),
    ("Cadencias clásicas completas", [
        prog("I-ii6-V7-I", 8, """
            Dm/F como subdominante: el bajo F sube a G. La cadencia más común en Bach y Mozart.
            """, "C", ["I", "ii@1", "V7", "I"]),
        prog("Cadencia completa en G", 7, """
            I-IV-I6/4-V7-I en G. Transpórtalo a D y F.
            """, "G", ["I", "IV", "I@2", "V7", "I"]),
        prog("Cadencia rota con séptima", 5, """
            V7-vi: G7 a Am. La sensible sube igual (B a C), pero el bajo va a A.
            """, "C", ["I", "IV", "V7", "vi", "ii@1", "V7", "I"]),
        scale("C", "harmonic", hands="HS", minutes=5, extra="C menor, relativa de Eb."),
        scale("F", "harmonic", hands="HS", minutes=5, extra="F menor, relativa de Ab. Mano derecha como F mayor."),
    ]),
    ("Modular", [
        prog("A la dominante", 10, """
            Modular es cambiar de tono. Se usa un acorde pivote que es de los dos tonos: Am es vi en C y ii en G. Luego D7 confirma G.
            C Am D7 G: hemos llegado a G mayor. Vuelve con G7 C.
            """, "C", ["C", "Am", "D7", "G", "G", "G7", "C"]),
        prog("A la relativa menor", 6, """
            C E7 Am: el E7 (V de Am) cambia el centro a A menor. Para volver: Dm G7 C.
            """, "C", ["C", "F", "E7", "Am", "Dm", "G7", "C"]),
        scale("B", "harmonic", hands="HS", minutes=7, extra="B menor, relativa de D. 7ª elevada: A#."),
        scale("F#", "harmonic", hands="HS", minutes=7, extra="F# menor, relativa de A. 7ª elevada: E#."),
    ]),
    ("Armonizar una melodía", [
        abc_part("Cómo elegir los acordes", 10, """
            En cada tiempo fuerte, elige un acorde que contenga la nota de la melodía. Las notas de paso entre medias no cuentan.
            Usa I, IV y V primero; al final de cada frase, una cadencia (V-I, o V sola en una semicadencia).
            Aquí está la Oda a la alegría sin acordes. Decide uno por compás (C o G) y luego compara con la lección 6.
            """, "K:C\n" + rows(ODE_PLAIN)),
        abc_part("Noche de paz", 15, """
            En 6/8 (dos pulsos por compás). Melodía en la derecha, acordes en la izquierda. Los acordes: C, F y G7.
            Primero toca solo la melodía. Luego añade la raíz en la izquierda. Al final, acordes completos con conducción de voces.
            """, two_hands("C", SILENT, SILENT_LH, meter="6/8", length="1/8")),
        abc_part("Tu armonización", 5, """
            Sin mirar los acordes, toca la melodía de Noche de paz e intenta los acordes de oído. Pista: cambia en los compases 3, 4, 5, 6, 7, 8, 9, 10 y 11.
            """, "M:6/8\nL:1/8\nK:C\n" + rows(SILENT_PLAIN)),
    ]),
    ("Secuencias", [
        prog("Círculo de quintas en el tono", 10, """
            C F Bdim Em Am Dm G C: cada raíz baja una quinta. Toda la escala en una cadena; es el motor de muchas piezas barrocas.
            """, "C", ["I", "IV", "viio", "iii", "vi", "ii", "V", "I"]),
        prog("Con séptimas", 8, """
            Cmaj7 Fmaj7 Bm7b5 Em7 Am7 Dm7 G7 Cmaj7. Con la raíz en la izquierda, la derecha baja por grados.
            """, "C", ["Imaj7", "IVmaj7", "viiø7", "iii7", "vi7", "ii7", "V7", "Imaj7"], rootless=True),
        prog("El canon de Pachelbel", 7, """
            C G Am Em F C F G: la progresión del canon de Pachelbel, también de muchas canciones actuales.
            """, "C", ["I", "V", "vi", "iii", "IV", "I", "IV", "V"], pattern="ballad"),
        scale("C#", "harmonic", hands="HS", minutes=5, extra="C# menor, relativa de E. 7ª elevada: B#."),
    ]),
])

block("todas", "6 · Todas las tonalidades", [
    ("El círculo de quintas", [
        part("Orden de los sostenidos y los bemoles", 8, """
            Sostenidos, en orden: F C G D A E B. Bemoles: B E A D G C F (al revés).
            Tonos mayores, sumando una alteración cada vez:
            |Con #: G(1) D(2) A(3) E(4) B(5) F#(6)
            |Con b: F(1) Bb(2) Eb(3) Ab(4) Db(5) Gb(6)
            Cada tono mayor tiene su relativo menor 3 semitonos abajo, con la misma armadura:
            |Mayor: C  G  D  A   E   B   F#
            |Menor: Am Em Bm F#m C#m G#m D#m
            |Mayor: F  Bb Eb Ab Db  Gb
            |Menor: Dm Gm Cm Fm Bbm Ebm
            """),
        prog("I-IV-V-I por el círculo", 12, """
            C, luego G, D, A... Cada vez el I-IV-V-I del tono siguiente. Aquí van los 6 primeros; transporta para los demás.
            """, "C", ["C", "F", "G", "C", "G", "C", "D", "G", "D", "G", "A", "D", "A", "D", "E", "A", "E", "A", "B", "E", "B", "E", "F#", "B"]),
        scale("G#", "harmonic", hands="HS", minutes=5, extra="G# menor, relativa de B. 7ª elevada: F## (doble sostenido, la tecla de G)."),
        scale("Eb", "harmonic", hands="HS", minutes=5, extra="Eb menor, relativa de Gb."),
    ]),
    ("Escalas de sostenidos a dos octavas", [
        scale("C", hands="HT", octaves=2, minutes=5),
        scale("G", hands="HT", octaves=2, minutes=5),
        scale("D", hands="HT", octaves=2, minutes=5),
        scale("A", hands="HT", octaves=2, minutes=5),
        scale("E", hands="HT", octaves=2, minutes=5),
        scale("B", hands="HT", octaves=2, minutes=5),
    ]),
    ("Escalas de bemoles a dos octavas", [
        scale("F", hands="HT", octaves=2, minutes=5),
        scale("Bb", hands="HT", octaves=2, minutes=5),
        scale("Eb", hands="HT", octaves=2, minutes=5),
        scale("Ab", hands="HT", octaves=2, minutes=5),
        scale("Db", hands="HT", octaves=2, minutes=5),
        scale("F#", hands="HT", octaves=2, minutes=5, extra="F# y Gb son la misma escala con otros nombres."),
    ]),
    ("Escalas menores a dos octavas", [
        scale("A", "harmonic", hands="HT", octaves=2, minutes=5),
        scale("E", "harmonic", hands="HT", octaves=2, minutes=5),
        scale("D", "harmonic", hands="HT", octaves=2, minutes=5),
        scale("B", "harmonic", hands="HT", octaves=2, minutes=5),
        scale("G", "harmonic", hands="HT", octaves=2, minutes=5),
        scale("A", "melodic", hands="HT", octaves=2, minutes=5),
    ]),
    ("Las menores que faltan", [
        scale("C", "harmonic", hands="HT", minutes=5),
        scale("F", "harmonic", hands="HT", minutes=5),
        scale("F#", "harmonic", hands="HT", minutes=5),
        scale("C#", "harmonic", hands="HT", minutes=5),
        scale("Bb", "harmonic", hands="HS", minutes=5, extra="Bb menor, relativa de Db."),
        scale("Bb", "harmonic", hands="HT", minutes=5),
    ]),
    ("Arpegios en todas las tonalidades", [
        arpeggio("F", minutes=5),
        arpeggio("D", minutes=5),
        arpeggio("Em", minutes=5),
        arpeggio("Dm", minutes=5),
        part("Arpegios en las demás", 10, """
            Con el botón de transportar del arpegio de D, recorre todos los tonos mayores; con el de Dm, todos los menores.
            Regla: el pulgar no toca teclas negras. Si la raíz es negra, empieza con el 2 (derecha) o el 2-3 (izquierda).
            """),
    ]),
    ("Repaso final: tu rutina", [
        prog("ii-V-I en todas las tonalidades", 10, """
            Por el círculo de quintas: Dm7 G7 Cmaj7, Gm7 C7 Fmaj7, Cm7 F7 Bbmaj7... Cada I es el V del siguiente ii-V-I.
            """, "C", ["Dm7", "G7", "Cmaj7", "Gm7", "C7", "Fmaj7", "Cm7", "F7", "Bbmaj7", "Fm7", "Bb7", "Ebmaj7"], rootless=True),
        prog("Todo junto", 10, """
            Todo lo aprendido en una vuelta: I-vi-ii-V con una dominante secundaria (A7), el iv prestado (Fm) y la cadencia con 6/4 (C/G G7 C).
            """, "C", ["I", "V7/ii", "ii7", "V7", "I", "V7/IV", "IV", "iv", "I@2", "V7", "I"]),
        part("Rutina para seguir", 10, """
            Cada día, 30 minutos:
            - 10 min: dos escalas mayores y su relativa menor, manos juntas a dos octavas, y sus arpegios. Ve rotando por el círculo de quintas.
            - 10 min: una progresión (I-V-vi-IV, ii-V-I, cadencia andaluza...) en un tono nuevo, con un patrón de acompañamiento distinto.
            - 10 min: una canción del cancionero, primero leyendo los acordes, luego con inversiones y bajo propio, y al final de oído en otro tono.
            """),
    ]),
])
