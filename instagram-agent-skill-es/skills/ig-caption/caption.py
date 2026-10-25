#!/usr/bin/env python3
"""
caption.py - revisa un caption de Instagram en español y te enseña exactamente
lo que muestra el feed antes del "... más".

Instagram le da al caption unos 125 caracteres en el feed y esconde el resto
detrás de un toque. Casi todos los captions que fallan, fallan ahí: el gancho
está en la tercera oración, la primera línea es un saludo, o todo abre con un
hashtag. Este script imprime la ventana visible dentro de un recuadro para que
la leas como la lee un desconocido que va scrolleando, y luego revisa las ocho
cosas que vale la pena revisar.

El corte de 125 caracteres es una aproximación. El número real cambia con el
dispositivo, el tamaño de letra y dónde caen tus saltos de línea, y por eso
conviene dejar margen en vez de diseñar un caption que termine justo en 125.
Cámbialo con --truncate si quieres probar uno más estricto.

Todo el texto se compara sin acentos y en minúsculas: "escribeme" y
"escríbeme" cuentan igual, porque mucha gente escribe sin acentos en el
celular. Los signos ¿ ¡ « » se respetan y nunca se borran del texto.

Los códigos de estado (PASS / WARN / FAIL) y el veredicto (READY / REVIEW /
FIX) se quedan en inglés a propósito: son el contrato de --json y del código de
salida que comparten las demás herramientas del paquete.

Uso
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "cotizaciones para clientes,precios de agencia"
  pbpaste | python3 caption.py -
  python3 caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap
import unicodedata

LIMIT = 2200             # Límite duro de Instagram para un caption.
TRUNCATE = 125           # Más o menos donde el feed corta a "... más".
HASHTAG_LIMIT = 5        # Tope de Instagram por post o reel desde el 18 de
                         # diciembre de 2025, antes eran 30. Lo anunció la
                         # cuenta @Creators: "using fewer (up to 5) more
                         # targeted hashtags, rather than many generic ones,
                         # can improve both your content's performance and
                         # people's experience".

# \w en Python 3 ya acepta letras con acento, ü y ñ, así que #diseñoGráfico
# y @maría.lópez se leen completos.
HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+"
                     r"|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app|mx|es|lat)(?:\.mx)?/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")

# Lo "concreto" en español: cifras, montos, porcentajes, números dichos con
# palabras y nombres propios a media oración. "Una" y "uno" no cuentan porque
# casi siempre son artículos, no cantidades.
DIGITS_RE = re.compile(r"\$\s?\d|\d[\d,.]*\s?%?")
SPOKEN_NUMBERS = (
    "dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce "
    "quince dieciseis diecisiete dieciocho diecinueve veinte veintiun veintiuno "
    "veintidos veintitres veinticuatro veinticinco treinta cuarenta cincuenta "
    "sesenta setenta ochenta noventa cien ciento doscientos doscientas "
    "trescientos trescientas cuatrocientos quinientos quinientas seiscientos "
    "setecientos ochocientos novecientos mil millon millones docena media"
).split()
SPOKEN_RE = re.compile(r"\b(?:" + "|".join(SPOKEN_NUMBERS) + r")\b")
CAPITAL_RE = re.compile(r"\b[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]{2,}\b")
SENTENCE_START_RE = re.compile(r"(?:^|[.!?¿¡:;\"«“(\n…-])\s*$")


def fold(text):
    """Minúsculas y sin acentos, para comparar como escribe la gente."""
    nfd = unicodedata.normalize("NFD", text.lower())
    return "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")


def concrete_hits(window):
    """Cifras, números dichos y nombres propios que no abren oración."""
    hits = DIGITS_RE.findall(window)
    hits += SPOKEN_RE.findall(fold(window))
    for m in CAPITAL_RE.finditer(window):
        # En español solo se usa mayúscula al inicio de oración y en nombres
        # propios. Si va después de un punto, ¿, ¡ o al inicio, no cuenta.
        if not SENTENCE_START_RE.search(window[:m.start()]):
            hits.append(m.group(0))
    return hits


# Las peticiones se buscan en el texto ya "doblado" (sin acentos, minúsculas),
# excepto la palabra clave, que necesita las mayúsculas para distinguirse:
# "Comenta CONTRATO" es una palabra clave, "comenta qué opinas" es una pregunta.
KEYWORD_ASK_RE = re.compile(
    r"(?i:\b(?:coment[aáe]|escrib[ea]|d[eé]ja(?:me)?|pon)\b(?:\s+(?:aqu[ií]|abajo))?"
    r"(?:\s+(?:la\s+)?palabra)?)\s*[\"«“']?\s*[A-ZÁÉÍÓÚÑ0-9]{2,}\b")

ASKS = [
    (re.compile(r"\bescribeme\b|\bmandame\s+(?:un\s+)?(?:dm|md|mensaje|inbox)\b"
                r"|\benviame\s+(?:un\s+)?(?:dm|md|mensaje)\b|\bmensaje\s+directo\b"
                r"|\b(?:por|al)\s+(?:dm|md|inbox)\b"), "escríbeme por DM"),
    (re.compile(r"\bguarda(?:lo|la|los|las)?\b|\bguardate\s+est"), "guárdalo"),
    (re.compile(r"\bcomparte(?:lo|la|los|las)?\b|\bmanda(?:selo|sela)\b"
                r"|\benvia(?:selo|sela)\b|\betiqueta\s+a\b"), "compártelo"),
    (re.compile(r"\bsigueme\b|\bsiguenos\b|\bsigue(?:me)?\s+para\b"), "sígueme"),
    (re.compile(r"\b(?:link|enlace)\s+(?:en|de)\s+(?:mi\s+|la\s+)?(?:bio|biografia|perfil)\b"),
     "link en bio"),
    (re.compile(r"\bdesliza(?:te)?\b|\bswipe\b|\bpasa\s+a\s+la\s+siguiente\b"
                r"|\btoca\s+(?:aqui|para|el\s+enlace|el\s+link)\b"), "desliza o toca"),
    (re.compile(r"\bdime\b|\bcuentame\b|\bcuentanos\b|\bque\s+harias\b|\bque\s+opinas\b"
                r"|\bcual\s+(?:eliges|prefieres|escogerias|te\s+late)\b"
                r"|\bcomenta(?:me)?\s+(?:abajo|aqui|que|cual|si|como)\b"), "responder una pregunta"),
]

# Etiquetas genéricas que no describen nada, en español y las que se copian
# del inglés. Se comparan sin acentos.
FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#explorar", "#foryou",
               "#foryoupage", "#parati", "#paratii", "#paratipage", "#trending",
               "#tendencia", "#tendencias", "#instagood", "#love", "#amor", "#follow",
               "#sigueme", "#siguemeytesigo", "#like4like", "#likeforlike", "#megusta",
               "#reels", "#reelsinstagram", "#viralreels", "#reelsviral", "#instadaily",
               "#fotodeldia", "#instamood"}


def visible_window(text, cut):
    """Lo que muestra el feed. Instagram corta a media palabra, y esto también."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE MUESTRA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(el caption cabe completo)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    folded = fold(stripped)
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = (["comentar una palabra clave"] if KEYWORD_ASK_RE.search(stripped) else [])
    asks += [name for pattern, name in ASKS if pattern.search(folded)]
    filler = [t for t in tags if fold(t) in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]
    concrete = concrete_hits(window)

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LONGITUD", "FAIL" if chars > LIMIT else "PASS",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} por encima del límite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "FAIL", "el caption abre con una línea en blanco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMERA LÍNEA", "FAIL",
            "abre con un hashtag o una mención, justo en el único lugar que merece una frase")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "WARN",
            f"{len(first_line)} caracteres, así que se corta en {cut} a media idea. "
            "Está bien si el corte deja intriga, mal si cae en una subordinada")
    else:
        add("PRIMERA LÍNEA", "PASS", f"{len(first_line)} caracteres, se ve completa")

    add("GANCHO CONCRETO", "PASS" if concrete else "WARN",
        f"{len(concrete)} cifra(s), número(s) o nombre(s) en la ventana visible"
        + ("" if concrete else ": nada comprobable antes del toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FAIL", f"{len(tags)} etiquetas, más del tope de Instagram de "
                                f"{HASHTAG_LIMIT}. Las que pasan de la quinta no cuentan "
                                "y el bloque se ve viejo")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "WARN", f"{len(tags)} etiquetas, en el tope, y {len(filler)} "
                                "genéricas. Usa las cinco en temas")
    elif filler:
        add("HASHTAGS", "WARN", f"{len(tags)} etiquetas, {len(filler)} genéricas "
                                f"({', '.join(filler[:3])}). Esas no describen nada")
    else:
        add("HASHTAGS", "PASS", f"{len(tags)} etiqueta(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("UBICACIÓN TAGS", "PASS", "no hay etiquetas que acomodar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("UBICACIÓN TAGS", "WARN", "hay un hashtag dentro de la ventana visible, "
                                      "gastando espacio del feed en una etiqueta")
    else:
        add("UBICACIÓN TAGS", "PASS", "las etiquetas quedan debajo del corte")

    add("ENLACES", "WARN" if links else "PASS",
        f"{len(links)} enlace(s) en el caption, y en el caption no se puede dar clic. "
        f"Pásalo a la bio o al DM" if links else "no hay enlaces muertos en el texto")

    if len(asks) == 1:
        add("UNA PETICIÓN", "PASS", f"un solo llamado a la acción: {asks[0]}")
    elif not asks:
        add("UNA PETICIÓN", "WARN", "no hay llamado a la acción. Decide para qué es este post")
    else:
        add("UNA PETICIÓN", "WARN", f"{len(asks)} peticiones ({', '.join(asks)}). "
                                    "Dos peticiones es lo mismo que ninguna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "WARN" if density > 4 else "PASS",
        f"{len(emoji)} emoji(s), {density:.1f} por cada 100 caracteres"
        + (": se leen como decoración" if density > 4 else ""))

    if keywords:
        low = re.sub(r"\s+", " ", folded)
        win = re.sub(r"\s+", " ", fold(window))
        found = [k for k in keywords if fold(k) in low]
        missing = [k for k in keywords if fold(k) not in low]
        in_window = [k for k in found if fold(k) in win]
        status = "PASS" if not missing else ("WARN" if found else "FAIL")
        add("BÚSQUEDA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la ventana visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FAIL")
    warns = sum(1 for c in checks if c["status"] == "WARN")
    verdict = "FIX" if fails else ("REVIEW" if warns else "READY")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


VERDICT_ES = {"READY": "listo para publicar", "REVIEW": "revísalo",
              "FIX": "hay que corregir"}


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DE CAPTION  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} petición(es)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<17} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDICTO  {a['verdict']} ({VERDICT_ES[a['verdict']]})\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa un caption de Instagram en español.")
    ap.add_argument("input", nargs="?", default="-",
                    help="archivo con el caption, o - para leer de stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres que se ven antes de '... más' (por defecto {TRUNCATE})")
    ap.add_argument("--keywords", default="",
                    help="términos separados por comas con los que quieres que te encuentren")
    ap.add_argument("--json", action="store_true", help="salida en JSON")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "READY" else 1)


if __name__ == "__main__":
    main()
