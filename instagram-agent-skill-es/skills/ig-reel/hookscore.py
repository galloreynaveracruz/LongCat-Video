#!/usr/bin/env python3
"""
hookscore.py - califica la primera línea de un Reel en las cinco cosas que
tienen en común los ganchos fuertes, y ordena un lote de ganchos entre sí.

Qué es:  cinco heurísticas locales, calculadas en tu máquina a partir del
texto. Miden propiedades que suelen compartir los ganchos que retienen: una
longitud que se dice en menos de tres segundos, un dato concreto, algo en
juego, lo importante al principio y no al final, y una persona a quien va
dirigido.

Qué NO es:  un predictor de vistas. La versión original en inglés se probó
con 74 ganchos reales en inglés, transcritos de los primeros tres segundos de
los ocho mejores y los ocho peores videos de cinco canales. Separando un
gancho real de uno escrito a propósito para ser malo, le fue bien: AUC 0.83,
y 9 de 10 ganchos malos quedaron debajo de la mediana real. Separando los
éxitos de un buen creador de los fracasos de ese mismo creador, casi nada:
AUC 0.56, donde 0.50 es una moneda al aire.

IMPORTANTE: esos números son del original en inglés. Las listas de palabras
de esta versión se reconstruyeron para español (números dichos en voz alta,
palabras de dinero, de tensión, aperturas débiles, imperativos, tú/usted) y
NO se han validado todavía con un corpus de ganchos reales en español. Tómalo
como una revisión de higiene, no como una medición.

Úsalo para lo que sí detecta: saludos, preámbulos, ganchos sin nada concreto
y ganchos que tardan cinco segundos en decirse. No te va a decir cuál de dos
ganchos decentes va a viajar, y nada que lea texto puede, porque eso lo
deciden tu cara, tu edición, tu audio y a quién se lo enseña Instagram.
Confía más en la gráfica de retención que en este script.

Cada revisión da de 0 a 100. Más alto es mejor.

Uso
  python3 hookscore.py ganchos.txt            # un gancho por línea, ordenados
  python3 hookscore.py --hook "Perdí $18,000 por una cláusula que no puse."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py ganchos.txt --json
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

LETTERS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
WORD_RE = re.compile(r"[" + LETTERS + r"0-9$%'’-]+")
NUMBER_RE = re.compile(
    r"\$\s?\d[\d,.]*"                                   # dinero, completo
    r"|\b\d[\d,.]*\s?"                                  # una cifra, con o
    r"(?:%|k\b|x\b|mil\b|millones\b|mdp\b|pesos\b"      # sin unidad
    r"|d[oó]lares\b|varos\b|euros\b|hrs?\b|horas?\b|mins?\b|minutos?\b"
    r"|seg\b|segundos?\b|d[ií]as?\b|semanas?\b|mes(?:es)?\b|a[nñ]os?\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúüñ]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")
PRICE_RE = re.compile(r"\$\s?\d|\b\d[\d,.]*\s*(?:mil\s+)?(?:pesos|d[oó]lares|varos|euros|mxn|usd)\b",
                      re.IGNORECASE)
# Antes de una mayúscula, esto marca inicio de oración: no es nombre propio.
SENTENCE_START = ".!?¿¡\"“«:…"


def fold(text):
    """Minúsculas y sin acentos: "Cómo" y "como" cuentan igual. La ñ pasa a n."""
    nfd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower()


# Los ganchos hablados dicen sus números en voz alta. "Cero pesos" y "veinte
# mil" son tan concretos como "$0" y "$20,000", y contar solo dígitos los
# perdía. "uno", "una" y "primero" no están a propósito: casi siempre son
# relleno y no una cantidad. Todo va sin acentos porque se compara con fold().
SPOKEN_NUMBERS = {
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "quince", "veinte", "treinta", "cuarenta",
    "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien", "ciento",
    "cientos", "doscientos", "trescientos", "quinientos", "mil", "millon",
    "millones", "billon", "billones", "docena", "mitad", "doble", "triple",
}
MONEY_WORDS = {
    "pesos", "peso", "dolares", "dolar", "varos", "lana", "euros", "centavos",
    "mil", "ciento", "porciento", "mdp", "millonario", "millonaria",
    "ventas", "ganancia", "ganancias", "utilidad", "ingresos", "sueldo",
    "salario", "renta", "facture", "facturo", "facturamos", "facturacion",
    "cobre", "cobro", "presupuesto",
}


def is_spoken_number(token):
    """Compuestos que no caben en un set: veinticinco, setecientos."""
    return (token in SPOKEN_NUMBERS or token.startswith("veinti")
            or (token.endswith("cientos") and len(token) > 7))


# Palabras que ponen algo en juego. Un gancho sin ninguna es una afirmación;
# con una, es una razón para seguir viendo. Sin acentos, como sale de fold().
# "ya" no está: en español abre la mitad de las frases y no tensa nada.
STAKES = {
    "deja", "dejes", "nunca", "jamas", "nadie", "nada", "no", "ni",
    "error", "errores", "equivocado", "equivocada", "mal",
    "perdi", "perdimos", "perder", "perdiendo", "pierdes", "pierden", "perdida",
    "costo", "cuesta", "cuestan", "costar", "caro", "carisimo",
    "quebre", "quiebra", "fracase", "fracaso", "falle", "falla", "fallan",
    "renuncie", "renuncia", "despedi", "despidieron", "corrieron",
    "borre", "borra", "elimine", "mato", "mata", "matando",
    "reemplazo", "reemplaza", "gratis", "pague", "pagas", "pagando", "cobran",
    "cobre", "contrate", "ahorre", "ahorra", "primer", "primera", "primeros",
    "prohibido", "ilegal", "peor", "odio", "odie", "desperdicie", "tirando",
    "estafa", "mentira", "mintieron", "mienten", "verdad", "neta", "secreto",
    "oculto", "escondido", "robo", "robaron", "antes", "hasta", "sino",
    "excepto", "menos", "problema", "riesgo", "peligro", "cuidado", "aguas",
    "ojo", "arrepiento", "ojala", "deberia", "deberias", "todavia", "aun",
    "solo", "sin", "vs", "versus", "contra", "realmente", "tardaba", "tarde",
}

# Aperturas que gastan el primer segundo sin decir nada. Se comparan contra
# las primeras cuatro palabras, sin acentos, palabra completa.
WEAK_OPENERS = [
    "hola", "que onda", "que tal", "hey", "ok", "okey", "bueno", "entonces",
    "pues", "o sea", "oigan", "oye", "bienvenidos", "bienvenidas",
    "bienvenido", "bienvenida", "buenos dias", "buenas tardes", "buenas noches",
    "hoy", "en este video", "en este reel", "en el video de hoy",
    "quiero hablar", "quiero contarles", "quiero contarte", "les quiero",
    "les voy a", "te voy a", "vamos a", "la verdad es", "basicamente",
    "sabias que", "sabian que", "alguna vez", "te ha pasado", "les ha pasado",
    "una de las", "uno de los", "mucha gente", "muchas personas", "hay muchos",
    "hay muchas", "esto es", "este es", "es que", "como un", "como una",
    "cuando se trata",
]

# Imperativos que se ganan el primer lugar. Sin acentos y sin pronombre
# pegado: "róbate", "guárdalo" y "mándaselo" se reconocen por su raíz.
IMPERATIVES = {
    "deja", "dejen", "roba", "copia", "borra", "prueba", "mira", "guarda",
    "usa", "haz", "escribe", "manda", "empieza", "nunca", "jamas", "siempre",
    "pon", "checa", "revisa", "lee", "quita", "cambia", "sube", "cobra",
    "aprende", "olvida", "evita", "toma", "graba", "publica", "vende",
    "corre", "apunta", "anota", "comparte", "envia",
}
CLITICS = ("selos", "selas", "selo", "sela", "tela", "telo", "melo", "mela",
           "los", "las", "les", "nos", "lo", "la", "le", "te", "me")

# Formas de tú, usted y ustedes que no se confunden con otra cosa. Las
# terminaciones -as/-es solas no sirven (mesas, clientes, reels), así que
# los verbos van en una lista cerrada de los más comunes en ganchos.
ADDRESS_WORDS = {
    "tu", "tus", "te", "ti", "contigo", "tuyo", "tuya", "tuyos", "tuyas",
    "usted", "ustedes", "vosotros", "vosotras", "os",
}
TU_VERBS = {
    "eres", "estas", "tienes", "puedes", "sabes", "quieres", "haces", "vas",
    "necesitas", "ocupas", "debes", "deberias", "sigues", "usas", "publicas",
    "cobras", "vendes", "subes", "pagas", "pierdes", "ganas", "crees",
    "piensas", "buscas", "sientes", "trabajas", "estabas", "eras",
    "tenias", "podrias", "harias", "imaginas", "conoces", "das", "dices",
}
FIRST_PERSON = {
    "yo", "mi", "mis", "me", "conmigo", "nosotros", "nosotras", "nuestro",
    "nuestra", "nuestros", "nuestras", "soy", "estoy", "tengo", "hice", "fui",
    "tuve", "puse", "dije", "pude", "llevo", "estuve", "era", "tenia",
}

DEALBREAKERS = [
    (re.compile(r"^\s*[¡¿]?\s*(?:deja(?:n)? de (?:hacer |dar(?:le)? )?scroll\w*|no (?:hagas|le des|des) scroll"
                r"|no scrollees|deja de scrollear|espera,? no te vayas)"),
     "Abre con \"deja de hacer scroll\". Pedir atención demuestra que no te la has ganado."),
    (re.compile(r"\b(?:en (?:este|el) (?:video|reel)(?: de hoy)?|en el (?:video|reel) de hoy"
                r"|(?:hoy )?(?:te|les) voy a (?:ensenar|mostrar|explicar|platicar|contar)"
                r"|(?:hoy )?vamos a (?:ver|hablar))\b"),
     "Preámbulo de video. Bórralo y abre con lo que prometes."),
    (re.compile(r"^\s*[¡¿]?\s*(?:hola|que onda|que tal|hey|buen(?:os|as) (?:dias|tardes|noches)"
                r"|bienvenid[oa]s?)\b"),
     "Saludo. Nadie entra al feed para que lo saluden."),
    (HASHTAG_RE,
     "Hashtag en el gancho. Los hashtags van al final del caption, si es que van."),
    (EMOJI_RE,
     "Emoji en el gancho. El texto en pantalla a tamaño de gancho tiene espacio para palabras o para un emoji, no para ambos."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "$18,000" y "$18.000" son una palabra al decirlos, así que aquí también.
    return WORD_RE.findall(re.sub(r"(?<=\d)[,.](?=\d{3}(?!\d))", "", text))


def tokens(text):
    return [fold(w).strip("'’-") for w in words(text)]


def propers(text):
    """Palabras con mayúscula que no están al inicio de una oración."""
    found = []
    for m in PROPER_RE.finditer(text):
        before = text[:m.start()].rstrip()
        if not before or before[-1] in SENTENCE_START:
            continue
        found.append(m.group())
    return found


def imperative_root(token):
    """'robate' -> 'roba', 'guardalo' -> 'guarda', 'mandaselo' -> 'manda'."""
    if token in IMPERATIVES:
        return token
    for c in CLITICS:
        if token.endswith(c) and token[:-len(c)] in IMPERATIVES:
            return token[:-len(c)]
    return None


def check_length(text):
    """Un gancho tiene que llegar antes de que se mueva el pulgar. Unos dos segundos."""
    w = words(text)
    n = len(w)
    secs = n / 2.75                      # ~165 palabras por minuto, hablado
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 60:                       # dos líneas de texto grande en pantalla
        score -= 12
    return clamp(score), f"{n} palabras, {chars} caracteres, ~{secs:.1f}s hablado (ideal 5-12 palabras)"


def check_specificity(text):
    """Una cosa concreta le gana a tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    names = set(propers(text))
    low = tokens(text)
    spoken = [w for w in low if is_spoken_number(w) or w in MONEY_WORDS]
    hits = len(nums) + len(names) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(names)[:2] + spoken[:2])
    return score, (f"{hits} dato(s) concreto(s)" + (f": {found}" if found else
                   ", ni número, ni nombre, nada comprobable"))


def check_stakes(text):
    """Tensión, costo, negación. Algo que el espectador podría perder."""
    hits = [x for x in tokens(text) if x in STAKES]
    markers = sorted(set(hits))
    if PRICE_RE.search(text):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                               ", en esta línea no hay nada en juego")
    return clamp(score), detail


def check_frontload(text):
    """La palabra interesante no puede estar en la posición nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = tokens(text)
    opener = " ".join(low[:4]) + " "
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if opener.startswith(weak + " "):
            penalty, hit_opener = 30, weak
            break
    names = set(propers(text))
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or is_spoken_number(token) or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or (i and w[i] in names)):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "ninguna palabra fuerte en toda la línea"
    elif payload <= 3:
        base = 100.0
        where = f"lo fuerte en la palabra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"lo fuerte en la palabra {payload + 1}, puede ir antes"
    else:
        base = 40.0
        where = f"lo fuerte en la palabra {payload + 1}, demasiado tarde"
    detail = where + (f"; apertura débil \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Dirigido a una persona, o flotando en el aire."""
    w = tokens(text)
    raw = [x.lower() for x in words(text)]
    if any(x in ADDRESS_WORDS or x in TU_VERBS for x in w):
        return 100.0, "le habla al espectador"
    # "has visto", "has hecho": perfecto de tú.
    if re.search(r"\bhas \w+(?:ado|ido|isto|echo|ho)\b", " ".join(w)):
        return 100.0, "le habla al espectador"
    if w and imperative_root(w[0]):
        return 90.0, f"abre con imperativo (\"{w[0]}\")"
    # "No publiques", "No hagas": imperativo negativo, siempre de tú.
    if len(w) > 1 and w[0] == "no" and re.search(r"(?:es|as|ues|gas|jes|zcas)$", w[1]):
        return 90.0, f"abre con imperativo negativo (\"no {w[1]}\")"
    # Primera persona: lista cerrada, o pretérito en -é con acento escrito
    # ("facturé", "empecé"). Sin acento no se distingue, así que no se adivina.
    if any(x in FIRST_PERSON for x in w) or any(len(x) >= 4 and x.endswith("é") for x in raw):
        return 70.0, "primera persona, sin nombrar al espectador"
    return 35.0, "tercera persona, no hay nadie en el cuarto"


CHECKS = ["LONGITUD", "ESPECIFICIDAD", "TENSION", "AL_FRENTE", "DIRIGIDO"]


def run(text):
    results = {
        "LONGITUD": check_length(text),
        "ESPECIFICIDAD": check_specificity(text),
        "TENSION": check_stakes(text),
        "AL_FRENTE": check_frontload(text),
        "DIRIGIDO": check_address(text),
    }
    folded = fold(text)
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(folded)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más débil pone el techo, igual que en detect.py: con una
    # sola propiedad mala basta para que el pulgar siga de largo.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "STRONG" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "WEAK")
    return results, overall, verdict, flags


VERDICT_ES = {"STRONG": "FUERTE", "OK": "OK", "WEAK": "DÉBIL"}


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nCALIFICACIÓN DEL GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'GANCHO':<13} {bar(overall)} {overall:5.1f}   {VERDICT_ES[verdict]}", file=out)
    for f in flags:
        print(f"\n  DESCALIFICA  {f}", file=out)
    if verdict != "STRONG":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propiedad más débil: {weakest}. Arregla esa y vuelve a correrlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {VERDICT_ES[r['verdict']]:<7} {hook}", file=out)
        print(f"        más débil: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        descalifica: {f}", file=out)
    print("\nGraba el primero. Si el primero está debajo de 50, ninguno de estos es el gancho.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Califica el gancho de un Reel en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un gancho por línea, o -")
    ap.add_argument("--hook", help="califica un solo gancho escrito en la línea de comandos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada que calificar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
