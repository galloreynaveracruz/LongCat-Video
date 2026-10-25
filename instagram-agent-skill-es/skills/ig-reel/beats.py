#!/usr/bin/env python3
"""
beats.py - convierte el guion de un Reel en una hoja de beats con tiempos,
antes de grabarlo.

Estima cuánto tardas en decir cada línea, las apila en códigos de tiempo y
marca las cuatro cosas que matan un Reel en la edición: un gancho que pasa de
los tres segundos, un beat tan largo que da tiempo de irse, una racha de
líneas sin nada concreto, y una duración total que no cuadra con lo que dijiste
que ibas a hacer.

Los tiempos son una estimación a partir del conteo de palabras y una
velocidad en palabras por minuto. Sirven para planear la edición, no
sustituyen grabarlo. El valor por defecto, 165, viene del original en inglés
y no está calibrado para español: en español una misma idea suele llevar más
palabras y el ritmo cambia mucho de persona a persona y de país a país. No hay
aquí un promedio "del español" porque no tenemos uno medido. Cronométrate
leyendo un guion en voz alta, cuenta las palabras, y pasa tu propio ritmo con
--wpm.

Uso
  python3 beats.py guion.txt
  python3 beats.py guion.txt --target 30
  python3 beats.py guion.txt --wpm 185 --target 45
  pbpaste | python3 beats.py -
  python3 beats.py guion.txt --json
"""

import argparse
import json
import re
import sys
import unicodedata

WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9$%'’-]+")
SENT_RE = re.compile(r"[^.!?…]+[.!?…]*")
NUMBER_RE = re.compile(r"\$\s?\d|\b\d[\d,.]*\b")
PROPER_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúüñ]{2,}\b")
SENTENCE_START = ".!?¿¡\"“«:…"   # una mayúscula después de esto no es un nombre
# Palabras vacías del español, sin acentos porque se comparan con fold().
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    "y", "e", "o", "u", "pero", "si", "de", "a", "en", "con", "por", "para",
    "que", "como", "cuando", "donde", "este", "esta", "esto", "estos", "estas",
    "ese", "esa", "eso", "es", "son", "era", "fue", "ser", "estar",
    "tu", "tus", "te", "ti", "yo", "mi", "mis", "me", "nos", "nuestro", "se",
    "su", "sus", "le", "les", "ella", "ellos", "ellas", "usted", "ustedes",
    "ya", "solo", "no", "ni", "muy", "mas", "hay", "ha", "he", "has", "han",
    "hacer", "hace", "va", "voy", "vas", "puede", "puedes", "todo", "todos",
    "uno", "sin", "sobre", "entre", "hasta", "desde", "pues", "asi", "tambien",
}


def fold(text):
    """Minúsculas y sin acentos: "Cómo" y "como" cuentan como la misma palabra."""
    nfd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower()


# Números dichos con letra: en un guion hablado "cinco horas" es tan concreto
# como "5 horas". "uno" y "una" quedan fuera porque casi siempre son artículo.
SPOKEN_NUMBERS = {
    "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
    "once", "doce", "quince", "veinte", "treinta", "cuarenta", "cincuenta",
    "cien", "mil", "millon", "millones", "docena", "mitad", "doble",
}


def concrete(text):
    """Cuántas cosas comprobables hay: cifras, precios, números dichos y nombres propios."""
    n = len(NUMBER_RE.findall(text))
    n += sum(1 for w in words(text) if fold(w) in SPOKEN_NUMBERS)
    for m in PROPER_RE.finditer(text):
        before = text[:m.start()].rstrip()
        if before and before[-1] not in SENTENCE_START:
            n += 1
    return n

HOOK_WINDOW = 3.0        # segundos. Después de esto, el pulgar ya decidió.
MAX_BEAT = 4.0           # segundos en una idea sin cambio en pantalla.
ABSTRACT_RUN = 3         # beats seguidos sin nada comprobable.


def words(text):
    # "$18,000" y "$18.000" son una palabra al decirlos, así que aquí también.
    return WORD_RE.findall(re.sub(r"(?<=\d)[,.](?=\d{3}(?!\d))", "", text))


def pretty(token):
    """Regresa el separador de miles para mostrarlo."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1,", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, wps):
    """Una línea es un beat, a menos que sea demasiado larga para serlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Párrafo largo: se parte en los finales de oración para que los
        # tiempos signifiquen algo.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=165, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": n,
            "text": text,
            "concrete": concrete(text),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Etiqueta las posiciones sobre las que de verdad se arma un Reel.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "GANCHO" else "GANCHO/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MITAD"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"el gancho dura {rows[0]['dur']:.1f}s, pasa de los {HOOK_WINDOW:.0f}s")
        notes.append(f"El beat 1 tarda {rows[0]['dur']:.1f}s en decirse. Recórtalo a "
                     f"{int(HOOK_WINDOW * wps)} palabras o menos, o el gancho llega cuando "
                     "la decisión ya se tomó.")
    if rows[0]["concrete"] == 0:
        notes.append("El beat 1 no tiene ni un número ni un nombre. Los ganchos sin algo "
                     "comprobable son los que se pasan de largo.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s en un solo beat")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Beat(s) {', '.join(map(str, long_beats))} pasan de {MAX_BEAT:.0f}s. "
                     "Parte la línea o cambia lo que hay en pantalla a la mitad. "
                     "Un cuadro quieto es donde la gente se va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Los beats {start}-{r['n']} no tienen nada concreto. "
                             "Pon un número, un nombre o un precio en alguno.")
        else:
            run, start = 0, None

    # ¿La última línea te regresa a la primera? Sin acentos, para que
    # "más" y "mas" cuenten como la misma palabra.
    first = {fold(w) for w in words(rows[0]["text"]) if fold(w) not in STOPWORDS}
    last = {fold(w) for w in words(rows[-1]["text"]) if fold(w) not in STOPWORDS}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Hay loop: el último beat repite \"{', '.join(loop[:3])}\" del gancho. "
                     "Las segundas vistas son alcance gratis.")
    else:
        notes.append("No hay loop. El último beat no comparte ninguna palabra con el gancho, "
                     "así que el video termina plano. Repetir una palabra del beat 1 es la "
                     "segunda vista más barata que vas a conseguir.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"La duración está en el objetivo ({total:.1f}s contra {target:g}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s arriba del objetivo. Recorta unas {int(delta * wps)} palabras.")
        else:
            notes.append(f"{-delta:.1f}s debajo del objetivo. Agrega {int(-delta * wps)} palabras "
                         "o grábalo corto. Corto casi siempre es lo correcto.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"HOJA DE BEATS  ·  {a['total_words']} palabras  ·  ~{a['total_seconds']:.1f}s "
            f"a {a['wpm']:g} ppm" + (f"  ·  objetivo {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<11}" if r["label"] else " " * 11
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<11}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Convierte el guion de un Reel en una hoja de beats con tiempos.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del guion, o - para stdin")
    ap.add_argument("--wpm", type=float, default=165,
                    help="palabras por minuto al hablar (165 por defecto, viene del original "
                         "en inglés; calibra el tuyo)")
    ap.add_argument("--target", type=float, help="duración objetivo en segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("el guion está vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
