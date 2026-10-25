---
name: ig-viral
description: >-
  Busca los reels que de verdad están funcionando ahorita en el nicho del
  usuario, ordénalos por cuánto le ganó cada uno a su propia cuenta, nombra la
  fórmula de gancho que usó cada uno y conviértelo en un swipe file del que se
  pueda grabar. Úsalo cuando el usuario diga "encuentra videos virales", "qué
  está funcionando ahorita", "qué está publicando la gente de mi nicho",
  "hazle ingeniería inversa a esta cuenta", "armame un swipe file", "por qué
  este reel está pegando", o pregunte qué hacer después y no tenga evidencia
  para contestarlo.
---

# ig-viral

El skill de investigación. Todo lo demás en este paquete escribe; este va y
mira. Córrelo cada mes, no cada día. Las fórmulas duran una temporada.

En esta carpeta vive una herramienta y sí corre:

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

## La única idea que hace que valga la pena

**Las vistas brutas no son evidencia.** Una cuenta con dos millones de
seguidores que hace 400,000 vistas tuvo un martes tranquilo. Una cuenta con
cuatro mil seguidores que hace 400,000 vistas encontró algo, y ese algo se
puede copiar.

Por eso aquí todo se ordena por el **múltiplo atípico**: vistas divididas
entre la mediana reciente de esa misma cuenta. Arriba de 3x es una señal.
Debajo de 1.5x es un día normal de esa cuenta y no te enseña nada, por grande
que se vea el número.

Junta cuentas **que estén a menos de unas 10x del tamaño del usuario**. Una
fórmula que funciona con 2M de seguidores muchas veces funciona porque tiene
2M de seguidores.

## Paso 1: elige las cuentas

Pídele al usuario de 6 a 12 cuentas, o propónselas y que las apruebe:

- **4 directas**: mismo nicho, misma oferta, un poco más adelante.
- **4 adyacentes**: otro nicho, la misma audiencia. De aquí se toman
  prestados los formatos antes de que alguien del nicho los tenga.
- **De 2 a 4 enormes**: cuentas mucho más grandes, solo para formato, nunca
  para frecuencia ni tono.

Pídele también que abra su propia **colección de Guardados**. Es el corpus más
rápido y relevante que existe y ya viene filtrado por su gusto.

## Paso 2: ve a mirar

Usa la herramienta de navegación que esta sesión de verdad tenga: un
navegador integrado, una extensión conectada al Chrome del propio usuario, o
una herramienta de uso de computadora. No hay API para esto y no hace falta,
porque el volumen es lo bastante chico para leerlo.

**Reglas que no se negocian:**

- **Nunca inicies sesión en Instagram por el usuario y nunca le pidas su
  contraseña.** Si una página pide login, el que ya tiene la sesión abierta es
  el usuario. Maneja su navegador con él presente, o pídele que pegue los
  datos.
- **Esto es leer, no hacer scraping.** Diez cuentas, una docena de reels cada
  una, a velocidad humana. La recolección automatizada a volumen viola los
  Términos de Uso de Instagram y hace que bloqueen acciones en las cuentas. No
  armes un crawler, no uses un servicio de scraping y no dejes esto corriendo
  en segundo plano.
- **Copia la fórmula, nunca el video.** La forma del gancho, la estructura, la
  duración, el patrón de cortes. No su guion, no su voz, no su edición.
  Atribuye cada fila del swipe file a la cuenta de donde salió.

**Qué capturar por reel**, en las palabras del creador:

| campo | notas |
| --- | --- |
| account | el @ |
| followers | del perfil |
| median | mira los últimos 12 reels y toma el número de vistas de en medio |
| views | este reel |
| hook | la primera línea, hablada o en pantalla, textual con todo y errores |
| on-screen | la primera tarjeta de texto, si es distinta |
| length | segundos |
| cta | qué pidió al final |

La mediana es la importante. Sin ella regresas a ordenar por seguidores, que
es justo lo que este skill existe para evitar.

**Cuando Instagram no te enseña suficiente:** la misma gramática de ganchos
corre en YouTube Shorts, donde las vistas y las transcripciones son públicas y
no hace falta login. Es un segundo corpus legítimo, y ahí es más fácil sacar
el gancho hablado:

```bash
# vistas de los shorts de un canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# la primera línea hablada de un short, de sus subtítulos automáticos
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=VIDEO_ID"
```

Toma cada palabra de los subtítulos con marca de tiempo menor a 3.0 segundos.
Ese es el gancho, como se dijo, no como se escribió.

## Paso 3: ordénalo

Llena un archivo separado por tabuladores con una fila de encabezado y corre
el script. Los nombres de columna estándar están en inglés para que el archivo
sea compatible con la versión original; también acepta `cuenta`,
`seguidores`, `mediana`, `vistas` y `gancho`. Las cifras pueden ir como
`412000`, `412,000`, `412 mil`, `412k` o `1.2M`.

```
account	followers	median	views	hook
@alguien	48000	11000	412000	nadie te dice que tus primeros 30 reels van a fracasar
```

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/swipe.md
```

Calcula el múltiplo atípico, nombra la fórmula del gancho con las mismas 26
fórmulas con las que escribe `/ig-reel`, califica cada gancho con
`hookscore.py` e imprime qué separa al tercio de arriba del tercio de abajo.

La clasificación busca sobre el texto tal cual y también sin acentos. Las
regex en español de `hooks.json` y las heurísticas de `hookscore.py` todavía
no se han validado contra un corpus real de ganchos en español; las cifras de
cobertura y precisión del original se midieron en inglés y no aplican aquí. Si
ves muchos "sin clasificar", es más probable que falte la regex que la
fórmula.

## Paso 4: di qué significa, con cuidado

Reporta tres cosas y nada más:

1. **Qué fórmulas sobresalen** en el tercio de arriba, con conteos. Dos
   fórmulas que aparecen cuatro veces cada una en seis cuentas es un hallazgo.
   Una que aparece dos veces no.
2. **Qué tiene en común el tercio de arriba en estructura** que el de abajo
   no: largo del gancho, si la entrega es visual, si el primer cuadro se mueve,
   dónde está la petición.
3. **Las filas sin clasificar.** Cada gancho que el clasificador no pudo
   nombrar es ruido o una fórmula que todavía no está en `hooks.json`. Léelos
   a mano. Es la columna más valiosa de la salida y es la razón por la que el
   script imprime el conteo.

Luego di el tamaño de la muestra y la confianza en palabras simples. Cuarenta
reels de seis cuentas sostienen una afirmación. Doce no, y decirlo es la
diferencia entre investigación y horóscopo.

## Paso 5: conviértelo en algo que se pueda grabar

Para las tres fórmulas de arriba, escribe **la versión del usuario**: su propia
historia, su propio número, con la forma que está funcionando. Pásale cada una
a `/ig-reel` con el id de la fórmula ya elegido.

Nunca regreses "haz un reel como este". Regresa una línea de gancho que pueda
decir mañana. Si falta su número, deja `{{tu número}}` y márcalo.

## Salida

```
SWIPE  ·  38 reels  ·  7 cuentas  ·  línea base: mediana de la cuenta

ATÍPICOS (arriba de 3x)
  38.4x  gancho 86  #3  Nadie te dice     @cuenta_a    412,000  (mediana 10,700)
  11.2x  gancho 79  #9  Róbate esto       @cuenta_c    180,000  (mediana 16,100)
  ...

QUÉ ESTÁ SOBRESALIENDO
  #3 Nadie te dice      x5 en el tercio de arriba, 0 en el de abajo
  #2 Orden negativa     x4
  mediana de largo      8 palabras arriba, 19 abajo

SIN CLASIFICAR (6)
  Dos de estos tienen la misma forma y no está en hooks.json: un gancho que
  abre leyendo en voz alta el comentario de otra persona. Vale la pena agregarlo.

TU VERSIÓN
  #3  "Nadie te dice que tus primeras 20 propuestas están hechas para perder."
  ...
```

Este bloque es un ejemplo de formato, no datos reales.

Escribe el swipe file en `~/.claude/instagram/swipe.md`. `/ig-reel` y
`/ig-plan` lo leen, y de eso se trata: después de correr esto una vez, el
resto del paquete trabaja con la evidencia del propio usuario y no con valores
por defecto.

Este skill no publica, no sigue, no da like y no manda mensajes. Lee.
