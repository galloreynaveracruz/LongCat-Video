#!/usr/bin/env python3
"""
humanize.py - quita la huella de máquina de un borrador en español.

Tres pasadas, en este orden:

  1. INVISIBLES  borra o normaliza los caracteres que un teclado humano nunca
                 produce: uniones de ancho cero, word joiners, guiones suaves,
                 BOMs, caracteres de etiqueta Unicode, espacios duros y
                 estrechos. Sobreviven al copiar y pegar y son la señal más
                 mecánica de cualquier texto generado.
  2. TIPOGRAFÍA  raya -> coma (la raya de diálogo al inicio de línea pasa a
                 guion), semirraya -> guion, comillas curvas y angulares
                 « » -> rectas, puntos suspensivos de un carácter -> tres
                 puntos, viñeta -> guion. Los signos de apertura ¿ ¡ NUNCA se
                 tocan: son ortografía, no tipografía.
  3. LÉXICO      reemplaza el léxico trillado de slop.json con palabras llanas,
                 conserva mayúsculas, ignora acentos al buscar y no toca URLs.

Las señales estructurales (tríadas, "no es solo X, es Y", muros de hashtags)
se REPORTAN, nunca se reescriben solas: cambiar la forma de una oración
requiere criterio, así que eso le toca al modelo, no a una regex.

Uso
  python3 humanize.py borrador.txt
  python3 humanize.py borrador.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py borrador.txt --json
  python3 humanize.py borrador.txt -o limpio.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?…\n]+[.!?…]*")
UPPER = "A-ZÁÉÍÓÚÜÑ"
LOWER = "a-záéíóúüñ"

# Cada vocal acepta su forma con y sin acento: la gente escribe "como" por
# "cómo" y "sumergete" por "sumérgete" todo el tiempo en el celular.
FOLD = {"a": "aá", "e": "eé", "i": "ií", "o": "oó", "u": "uúü", "ñ": "nñ"}


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def term_regex(find):
    """'sumérgete en' -> regex que ignora acentos, mayúsculas y espacios extra.

    Usa lookarounds en lugar de \\b para que funcione también con términos
    que empiezan o terminan en signo ("¿qué opinas?").
    """
    out = []
    for ch in find:
        base = unicodedata.normalize("NFD", ch)[0].lower()
        if ch.lower() == "ñ":
            out.append("[nñ]")
        elif base in FOLD:
            out.append("[" + FOLD[base] + "]")
        elif ch == " ":
            out.append(r"\s+")
        else:
            out.append(re.escape(ch))
    return re.compile(r"(?<!\w)" + "".join(out) + r"(?!\w)", re.IGNORECASE)


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (inicio, fin)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Cambia las URLs por marcadores para que ninguna pasada reescriba un enlace."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Borra o convierte en espacio los caracteres invisibles. Regresa (texto, hits)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Cualquier carácter Cf (de formato) que quede es invisible por definición.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "otros caracteres de formato invisibles", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(espacio)"})
        if ch == "—":
            # Raya de diálogo al inicio de línea: "—Hola —dijo." Pasarla a coma
            # dejaría ", Hola", así que se vuelve guion de teclado.
            text = re.sub(r"(?m)^([ \t]*)—\s*", r"\1- ", text)
            # Incisos e interrupciones: "dato —y es real— que" -> "dato, y es real, que".
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # usada como raya
            text = text.replace("–", "-")
        elif ch in "«‹":
            text = re.sub(re.escape(ch) + r"[ \t ]*", entry["to"], text)   # « hola » -> "hola"
        elif ch in "»›":
            text = re.sub(r"[ \t ]*" + re.escape(ch), entry["to"], text)
        else:
            text = text.replace(ch, entry["to"])
    # Una coma insertada antes de otra puntuación se lee mal. La coma antes de
    # ¿ o ¡ es correcta en español ("Oye, ¿sabías?") y no se toca.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    text = re.sub(r"([¿¡])\s*,\s*", r"\1", text)      # "¿—Y eso?" -> "¿, Y eso?" -> "¿Y eso?"
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    lead = src.lstrip("¿¡")
    if lead and lead[0].isupper():
        i = len(repl) - len(repl.lstrip("¿¡"))
        return repl[:i] + repl[i:i + 1].upper() + repl[i + 1:]
    return repl


def pass_lexical(text, lex):
    """Reemplaza palabras y frases trilladas. Las más largas primero para que la frase gane."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        pattern = term_regex(find)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(borrado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpieza después de borrar. Quitar una cláusula entera deja puntuación
    # huérfana ("sistema. ." o "¡!" o una línea que abre con coma), y eso se
    # lee peor que el relleno.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"¡[\s,]*!", "", text)                 # "¡Sígueme para más!" -> "¡!" -> nada
    text = re.sub(r"¿[\s,]*\?", "", text)
    text = re.sub(r"([¿¡])[ \t]+", r"\1", text)          # "¡ Hola" -> "¡Hola"
    text = re.sub(r"([¿¡])[,;:]\s*", r"\1", text)        # "¿, y eso?" -> "¿y eso?"
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # un espacio que dejó un borrado.
                                                      # Sangrías más hondas son a propósito.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # una raya se volvió coma y luego
                                                      # se borró la cláusula que seguía
    text = text.replace("...", "\x00ELL\x00")          # protege los puntos suspensivos reales
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    # "Más lejos. Sin lugar a dudas, esta..." deja "lejos., esta": la coma
    # que abría la cláusula borrada sobra. Tras ? o ! la coma sí es válida en
    # español ("¿Cuánto cobras?, me preguntó"), así que ahí no se toca.
    text = re.sub(r"(?<!\.)\.[ \t]*,[ \t]*", ". ", text)
    # Una conjunción que quedó sola ("Guarda este post y etiqueta a..." -> "y.").
    text = re.sub(r"(?im)(^|[.!?][ \t]+)(?:y|e|o|u|pero|ni)[ \t]*[.!?]+[ \t]*", r"\1", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)[ \t]+$", "", text)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Una raya que se volvió coma, seguida de un conector, deja una oración
    # empalmada ("es clave, también, demuestra"). Se promueve a punto.
    text = re.sub(r",\s*(también|así que|aun así|básicamente|al final|total)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # La uniformidad en el largo de las oraciones también es estructural.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Oraciones del mismo largo (variación {cv:.2f})",
                "count": len(lens),
                "fix": "Parte una oración a la mitad. Deja que otra se alargue. Las máquinas escriben parejo.",
            })
    return flags


def restore_capitals(original, text):
    """Borrar una apertura deja la siguiente palabra en minúscula.

    Solo se corrige para quien escribe con mayúscula inicial: una voz en
    minúsculas a propósito es un estilo, no un defecto, y gritarle encima sería
    justo lo que este script existe para evitar. Mira a través de ¿ ¡ y
    comillas: "¿qué" -> "¿Qué".
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*[¿¡\"'(]*([" + UPPER + LOWER + "])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    # (?<=[^.][.!?] ) deja en paz lo que sigue a unos puntos suspensivos:
    # "y luego... nada" es español correcto.
    return re.sub(r"(?:^|(?<=[^.][.!?] )|(?<=[.!?]\n)|(?<=\n))(\s*[¿¡\"]*)([" + LOWER + "])",
                  lambda m: m.group(1) + m.group(2).upper(), text)


def humanize(text, lex):
    text = unicodedata.normalize("NFC", text)   # acentos compuestos -> un solo carácter
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("REPORTE DEL HUMANIZADOR")
    print(f"{total} artefactos de máquina eliminados, "
          f"{len(report['structures'])} señales estructurales marcadas para reescribir", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LÉXICO TRILLADO")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. SEÑALES ESTRUCTURALES  (no se corrigen solas, reescríbelas tú)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPIO")
        print("  No hay nada que quitar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Quita la huella de máquina de un borrador en español.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("-o", "--out", help="escribe el texto limpio aquí en vez de stdout")
    ap.add_argument("--report", action="store_true", help="muestra qué cambió, en stderr")
    ap.add_argument("--json", action="store_true", help="emite {text, report} como JSON")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"escrito en {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
