#!/usr/bin/env python3
"""
detect.py - un panel de cinco revisiones que mide qué tan escrito-por-máquina
se ve un borrador en español.

Qué es:  cinco heurísticas locales basadas en las señales que miden los
detectores públicos de IA: variación en el largo de las oraciones,
concreción, vocabulario trillado, huella tipográfica y voz. Cada puntaje se
calcula en tu máquina a partir del texto. No se sube nada.

Qué NO es:  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llama a
sus APIs y no puede prometer su veredicto. Detecta las cosas en las que todos
se fijan, y por eso corregirlas suele mover también sus números, pero la única
afirmación honesta es la de esta línea.

Calibración:  los umbrales vienen del original en inglés y se ajustaron a mano
para español (sin contracciones, sujeto omitido, ¿ ¡). NO están validados con
un corpus en español. Tómalos como guía, no como medición.

Cada revisión regresa un puntaje HUMANO de 0 a 100. Más alto es mejor.

Uso
  python3 detect.py borrador.txt
  pbpaste | python3 detect.py -
  python3 detect.py borrador.txt --json
  python3 detect.py antes.txt despues.txt      # compara dos borradores
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

L = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
# Una oración termina en . ! ? o en puntos suspensivos. ¿ y ¡ abren, no
# cierran, así que quedan dentro de su oración: "¿Cuánto cobras? $800." son dos.
SENT_RE = re.compile(r"[^.!?…\n]+[.!?…]*")
WORD_RE = re.compile(r"[" + L + r"]+(?:'[" + L + r"]*)?")
# El español no tiene contracciones como el inglés. Lo que delata a una
# persona hablando son las muletillas y el registro oral. Se cuentan
# las del español de México y Latinoamérica más comunes en captions y guiones.
COLLOQUIAL = re.compile(
    r"(?<!\w)(?:o sea|osea|la neta|neta|pues|oye|mira,|bueno,|aj[aá]|[oó]rale|chid[oa]s?|"
    r"g[uü]ey|wey|ni modo|qu[eé] onda|la verdad|nom[aá]s|ahorita|pa'|pa|sale|chale|"
    r"igual y|ya ves|o algo as[ií]|tipo que|ja(?:ja)+|eh|¿no\?|¿verdad\?|¿sabes\?|¿va\?)(?!\w)",
    re.IGNORECASE)
PRONOUNS = re.compile(
    r"(?<!\w)(?:yo|me|mi|mis|m[ií]o|m[ií]a|conmigo|nosotr[oa]s|nos|nuestr[oa]s?|"
    r"t[uú]|tus|te|ti|contigo|tuy[oa]s?|ustedes|vos)(?!\w)", re.IGNORECASE)
# Números en cifra, montos y porcentajes, más los números dichos en voz alta,
# que en un guion de Reel aparecen escritos con letra. "uno/una" se excluyen:
# en español son artículos casi siempre.
NUMBERS = re.compile(r"\b\d[\d,.]*%?|\$\s?\d")
SPOKEN = re.compile(
    r"(?<!\w)(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|"
    r"quince|diecis[eé]is|dieciocho|veinte|veinti\w+|treinta|cuarenta|cincuenta|sesenta|"
    r"setenta|ochenta|noventa|cien|ciento|doscient[oa]s|trescient[oa]s|quinient[oa]s|mil|"
    r"mill[oó]n|millones|media hora|docena)(?!\w)", re.IGNORECASE)
# Nombre propio: mayúscula que no está al inicio de oración (ni después de ¿ ¡).
PROPER = re.compile(r"(?<![.!?…]\s)(?<![.!?…]\s[¿¡\"])(?<![¿¡\"])(?<!^)"
                    r"(?<!\w)[A-ZÁÉÍÓÚÑ][a-záéíóúüñ]{2,}(?!\w)", re.MULTILINE)
FOLD = {"a": "aá", "e": "eé", "i": "ií", "o": "oó", "u": "uúü", "ñ": "nñ"}


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Mapea value a 0-100, donde `human` -> 100 y `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def term_regex(find):
    """Igual que en humanize.py: ignora acentos, mayúsculas y espacios extra."""
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


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """La gente varía mucho el largo de sus oraciones. Los modelos escriben parejo."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "muy corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variación {cv:.2f} en {len(lens)} oraciones (lo ideal: 0.55+)"


def check_specificity(text):
    """Números, nombres y cosas concretas. El relleno es abstracto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    hits = (len(NUMBERS.findall(text)) + len(SPOKEN.findall(text))
            + len(set(PROPER.findall(text))))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} marcadores concretos, {density:.1f} por cada 100 palabras (lo ideal: 4+)"


def check_slop(text, lex):
    """Densidad de vocabulario trillado según el léxico."""
    w = words(text)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    # Las más largas primero, y lo que ya contó se tapa: "desbloquear tu
    # potencial" no debe contar también como "desbloquear".
    entries = sorted(lex["words"] + lex["phrases"], key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern = term_regex(entry["find"])
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(entry["find"])
            text = pattern.sub(" ", text)
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} términos trillados, {density:.1f} por cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que el teclado de un celular no produce por sí solo."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    # « » son correctas en español formal, pero en un caption casi siempre
    # llegan pegadas desde un generador o un procesador de texto.
    curly = sum(text.count(c) for c in "‘’“”«»‹›")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "    ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibles, {em} rayas, {curly} comillas curvas o angulares, "
              f"{ellip} puntos suspensivos de un carácter, {nbsp} espacios duros")
    return score, detail


def check_voice(text, lex):
    """Registro oral, persona y las formas por defecto de un modelo."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    colloquial = len(COLLOQUIAL.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(colloquial, human=2.0, machine=0.0) * 0.30
             + scale(person, human=7.0, machine=1.0) * 0.40
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("vinetas-parejas")
    detail = (f"{colloquial:.1f} marcas coloquiales, {person:.1f} pronombres de 1a/2a persona "
              f"por cada 100 palabras, {tells} señal(es) estructural(es)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIACIÓN", "ESPECIFICIDAD", "DENSIDAD SLOP", "HUELLA", "VOZ"]


def run(text, lex):
    text = unicodedata.normalize("NFC", text)
    results = {}
    results["VARIACIÓN"] = check_burstiness(text)
    results["ESPECIFICIDAD"] = check_specificity(text)
    results["DENSIDAD SLOP"] = check_slop(text, lex)
    results["HUELLA"] = check_fingerprint(text)
    results["VOZ"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # La revisión más débil arrastra el veredicto: a un detector le basta una señal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASS" if overall >= 70 and min(scores) >= 55 else (
        "REVIEW" if overall >= 50 else "FLAGGED")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL DE DETECCIÓN DE IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<14} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<14} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'PUNTAJE HUMANO':<14} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASS":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Señal más débil: {weakest}. Corrige eso primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Mide qué tan escrito-por-máquina se ve un borrador en español.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para ver antes y después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
