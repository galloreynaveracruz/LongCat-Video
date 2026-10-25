# Instagram agent skill, en español

Trece skills de Claude para operar una cuenta de Instagram, adaptadas al
español. Gratis, MIT, sin registro, sin API key, sin conectar nada.

Esta es una adaptación al español del repo original de Jake Schincariol,
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
No es solo una traducción: las listas de palabras, las expresiones regulares y
el léxico del humanizador se reconstruyeron para cómo se habla y se escribe en
español (acentos, ñ, ¿ ¡, números dichos en voz alta, muletillas y clichés de
Instagram en español).

**Nada se publica hasta que tú digas que sí.** Estas skills escriben. Tú publicas.

## Lo que hay que saber antes de usarla

Las mediciones del original (AUC 0.83 para detectar hooks malos, AUC 0.56 para
separar hits de fracasos, 74 hooks reales, cobertura del clasificador de 8% a
49%) se hicieron **con hooks en inglés**. Las heurísticas en español de esta
versión **todavía no están validadas** contra un corpus real. Úsalas para
descartar lo obviamente débil, no para predecir qué va a funcionar. Si las
mides con tus propios Reels y obtienes otro resultado, ese resultado manda.

## Instalación

Pégale esto a Claude:

```
Instala las skills de la carpeta instagram-agent-skill-es de este repo y confirma que /ig-reel funciona.
```

O tú mismo, en Claude Code, desde la raíz de este repo:

```bash
cp -r instagram-agent-skill-es/skills/ig-* ~/.claude/skills/
```

Para un solo proyecto, copia las mismas carpetas a `.claude/skills/` de ese
repo. ¿Sin Claude Code? Pega cualquier `SKILL.md` al inicio de un chat y
funciona como modo. Pierdes las herramientas de Python, que son lo principal de
`/ig-reel` y `/ig-human`, pero lo demás funciona.

Luego dedica diez minutos a `templates/voice.md`. Cópialo a
`~/.claude/instagram/voice.md` y llénalo, o mándale a Claude tres de tus Reels
y dile "escribe mi voice.md a partir de estos". Todas las skills leen ese
archivo. Aquí importa más que en otras redes, porque las palabras las tienes
que decir en voz alta.

## Las trece

| comando | qué hace |
| --- | --- |
| `/ig-reel` | Una idea convertida en Reel. Tres hooks a partir de [26 fórmulas](skills/ig-reel/hooks.json), con puntaje, luego el guion, el texto en pantalla y un beat sheet con tiempos. |
| `/ig-viral` | Busca lo que está funcionando en tu nicho, lo ordena por cuántas veces supera la mediana de su propia cuenta, nombra la fórmula y arma tu swipe file. |
| `/ig-caption` | El caption, revisado. Te muestra los ~125 caracteres que el feed enseña antes del "más". |
| `/ig-carousel` | Carruseles. La portada que gana el deslizamiento, el texto de cada slide y los archivos de 1080x1350. |
| `/ig-story` | La secuencia diaria de historias, qué sticker cumple qué función y el embudo a DM. |
| `/ig-profile` | Califica tu perfil con una [rúbrica de 12 partes](skills/ig-profile/rubric.json) sobre 100 y lo reescribe empezando por lo que más resta. |
| `/ig-plan` | La semana. Qué publicar, en qué formato, cuándo y con qué 10 cuentas interactuar. |
| `/ig-human` | El humanizador. Dos scripts que sí corren. |
| `/ig-comment` | Comentarios en publicaciones de otros. Nueve tipos, elegidos según lo que realmente es el post. Nunca "🔥🔥🔥". |
| `/ig-reply` | Las respuestas bajo tu propio post, ordenadas por prioridad: palabra clave, prospecto, sustancia, pregunta, apoyo, ruido. |
| `/ig-dm` | La entrega de la palabra clave, el primer mensaje, la propuesta de colaboración y dos seguimientos. Dos. |
| `/ig-repurpose` | Un video, podcast o newsletter convertido en una semana de Reels y carruseles que se sostienen solos. |
| `/ig-audit` | Análisis de lo que ya publicaste. Ordena por múltiplo sobre tu mediana y por envíos por alcance, no por vistas. |

## Las herramientas que sí corren

Sin dependencias, sin red, nada se sube. Corren en tu máquina, sobre tu texto.

```bash
python3 skills/ig-reel/hookscore.py hooks.txt               # ordena tus hooks
python3 skills/ig-reel/beats.py guion.txt --target 30       # cronometra el guion antes de grabar
python3 skills/ig-caption/caption.py caption.txt --keywords "contratos freelance,precios"
python3 skills/ig-human/humanize.py borrador.txt --report   # limpia y muestra cada cambio
python3 skills/ig-human/detect.py borrador.txt              # puntaje en cinco revisiones
python3 skills/ig-human/detect.py antes.txt despues.txt     # compara antes y después
python3 skills/ig-viral/swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

- **`hookscore.py`** califica el primer enunciado de un Reel en cinco
  propiedades: longitud, algo concreto, algo en juego, la carga al frente y a
  quién le habla. Marca los descalificadores, como abrir con "hola", "en este
  video" o "deja de hacer scroll".
- **`beats.py`** estima cuánto tarda cada línea en decirse, arma los
  tiempos y señala lo que mata un Reel en edición: un hook que pasa de tres
  segundos, un beat largo sin cambio en pantalla, varias líneas seguidas sin
  nada concreto y un final que no regresa al inicio. La velocidad por defecto
  es 165 palabras por minuto; mide la tuya y pásala con `--wpm`.
- **`caption.py`** te enseña la ventana del feed y revisa longitud, primera
  línea, hook concreto, hashtags, una sola llamada a la acción y términos de
  búsqueda. Aplica el límite actual de **cinco hashtags por post**, que
  Instagram fijó en diciembre de 2025.
- **`humanize.py`** quita caracteres invisibles, corrige tipografía (sin
  tocar ¿ ni ¡) y reemplaza el léxico trillado de [`slop.json`](skills/ig-human/slop.json),
  que está hecho para editarse. Lo que requiere criterio (estructuras como
  "no es solo X, es Y", tríadas, preámbulos, listas con emojis) lo marca en
  lugar de cambiarlo.
- **`detect.py`** da un puntaje con cinco revisiones locales.
- **`swipe.py`** ordena Reels por múltiplo sobre la mediana de cada cuenta.
  Las vistas brutas no son evidencia: 400,000 vistas en una cuenta de
  2,000,000 de seguidores es un martes tranquilo; en una de 4,000 es un
  hallazgo.

## La letra chica

**Estas skills no publican en Instagram.** Existe una API oficial de
publicación para cuentas profesionales, pero requiere una app de desarrollador
de Meta, una página vinculada, un token de larga duración y revisión de la
app. Todo lo demás que se usa para automatizar publicaciones, comentarios,
follows o DMs es automatización de navegador o herramientas de terceros, y
ambas violan los [Términos de uso de Instagram](https://help.instagram.com/581066165581870).
Por eso cada skill termina igual: un bloque listo para copiar, y tú lo publicas.

La excepción son las respuestas automáticas por palabra clave en DMs, que
Instagram permite con sus propias herramientas y socios aprobados, y que solo
se activan después de que alguien comenta primero. `/ig-dm` explica dónde está
ese límite.

**`/ig-viral` lee, no hace scraping.** Diez cuentas, una docena de Reels cada
una, a velocidad humana y en tu propio navegador. Nunca pide tu contraseña ni
inicia sesión por ti.

**Las cinco revisiones de detección son heurísticas locales**, no APIs de
detectores. No son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no los
llaman y no prometen sus veredictos. Nadie puede venderte honestamente
"indetectable".

**El filtro de caracteres invisibles es real y es acotado.** Quita los
caracteres de ancho cero y de formato que acaban en texto generado y
sobreviven al copiar y pegar. No pretende vencer ningún esquema criptográfico
de marca de agua.

**Nada aquí se inventa.** Ninguna métrica, cliente o resultado inventado va con
tu nombre. Si un borrador necesita un número que no has dado, regresa con
`{{tu número}}` y una advertencia, siempre.

**Los datos de la plataforma caducan.** El límite de hashtags pasó de 30 a 5
en diciembre de 2025. Si algo aquí contradice lo que Instagram hace cuando lo
leas, Instagram tiene la razón.

## Archivos

```
skills/ig-reel/hooks.json          26 fórmulas de hook: plantilla, ejemplo, texto en pantalla,
                                   para qué sirve, cómo se arruina y una regex para detectarla
skills/ig-reel/hookscore.py        el panel de cinco propiedades del hook
skills/ig-reel/beats.py            del guion a un beat sheet con tiempos
skills/ig-caption/caption.py       la vista previa del feed y el revisor del caption
skills/ig-human/slop.json          el léxico: términos trillados, caracteres invisibles, señales
skills/ig-human/humanize.py        las tres pasadas de limpieza
skills/ig-human/detect.py          el panel de cinco revisiones
skills/ig-viral/swipe.py           ranking por múltiplo y clasificación de fórmulas
skills/ig-profile/rubric.json      el puntaje de perfil sobre 100
templates/voice.md                 tu perfil de voz. Llénalo primero.
```

## Créditos y licencia

Original: Jake Schincariol, [opusjake.ai](https://opusjake.ai),
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
Adaptación al español: Gallo Reyna.

MIT. Ver [LICENSE](LICENSE), que conserva el aviso de copyright original como
exige la licencia.
