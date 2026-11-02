---
name: ig-reel
description: >-
  Escribe un Reel de Instagram a partir de una idea en bruto: opciones de
  gancho con 26 fórmulas, el guion hablado, el texto en pantalla y una hoja de
  beats con tiempos, en la voz del usuario y calificado antes de grabar. Úsalo
  cuando el usuario quiera un Reel, un guion de video corto, un gancho, un
  voiceover, "hazme un reel sobre X", "qué digo en este video", o cuando está
  por grabar y todavía no tiene la primera línea.
---

# ig-reel

Convierte una idea en bruto en un Reel que alguien termina de ver.

En esta carpeta viven dos herramientas y las dos de verdad corren. Úsalas. No
calcules el gancho a ojo y no adivines la duración.

```bash
python3 hookscore.py ganchos.txt            # ordena tus opciones de gancho
python3 hookscore.py --hook "una línea"     # califica una sola
python3 beats.py guion.txt --target 30      # hoja de beats con tiempos antes de grabar
```

Las dos están adaptadas al español: números dichos con letra, acentos, ñ,
¿ ¡, tú y usted, y aceptan texto escrito sin acentos. Lo que no tienen todavía
es validación: las cifras de precisión del original (AUC 0.83 contra ganchos
malos, 0.56 entre éxitos y fracasos del mismo creador) se midieron con ganchos
en inglés. Las heurísticas en español no se han probado contra un corpus real.
Úsalas como revisión de higiene, no como juez.

## Antes de escribir

1. Lee `~/.claude/instagram/voice.md` si existe. Es el perfil de voz del
   usuario: cómo habla a cámara, qué nunca dice, a quién le habla. Si no
   existe, pide **tres de sus propios reels**, transcríbelos o léelos, deduce
   la voz y escribe el archivo. Un guion en la voz equivocada no sirve, porque
   lo tiene que decir en voz alta.
2. Lee `hooks.json` en esta carpeta. 26 fórmulas, cada una con plantilla,
   ejemplo lleno, versión en pantalla, para qué sirve y cómo se arruina.
   Cuatro están ahí porque aparecían una y otra vez en ganchos reales del
   original en inglés, no porque completaran un patrón.
3. Si la idea está flaca, no la rellenes. Haz una sola pregunta agrupada: qué
   pasó, a quién, y cuánto costó o cuánto dejó. Un Reel necesita una cosa
   concreta y verdadera. Consíguela antes de escribir.
4. Si existe `~/.claude/instagram/swipe.md`, léelo. Lo escribe `/ig-viral` y
   es la evidencia del propio usuario sobre qué fórmulas están funcionando en
   su nicho ahorita. Pesa más que lo que dice este archivo por defecto.

## La forma

Un Reel se decide en los primeros dos segundos y se sostiene en los cinco
siguientes.

```
0:00 - 0:02   GANCHO      la afirmación. Línea hablada y línea en pantalla, escritas
                          por separado. Movimiento en el primer cuadro, no una cara quieta.
0:02 - 0:07   LO QUE ESTÁ EN JUEGO   por qué le importa a quien está viendo. Una línea.
0:07 - ...    EL CUERPO   una idea por beat, y el cuadro cambia en cada beat.
ÚLTIMOS 3s    LA ENTREGA  cumple lo que prometió el gancho, luego la única petición.
ÚLTIMA LÍNEA  EL LOOP     repite una palabra del gancho para que la segunda vista enganche.
```

Duración: de 15 a 45 segundos es el rango que funciona. Los Reels llegan a 3
minutos y casi nadie debería usarlos. Debajo de 7 segundos se inflan los loops
y nada más.

## El ciclo

**1. Elige tres ganchos, no uno.** Pasa la idea por `hooks.json`, escoge tres
fórmulas que de verdad le queden y escribe la línea hablada más la línea en
pantalla de cada una. Fórmulas distintas, no tres versiones de la misma.

**2. Califícalos.** Pon las tres líneas habladas en un archivo, una por línea,
y corre `hookscore.py`. Enséñale el ranking al usuario. Si el primero está
debajo de 50, todavía no tienes el gancho y ninguna edición lo arregla.

**3. Escribe el guion** sobre el gancho ganador. Lenguaje hablado, como de
verdad habla el usuario. Frases cortas. Ninguna oración que tenga que ensayar.

**4. Tómale el tiempo.** Corre `beats.py guion.txt --target {duración}`.
Arregla cada marca: un gancho de más de 3 segundos, cualquier beat de más de
4 segundos, una racha de beats sin nada concreto, falta de loop. Vuelve a
correrlo hasta que salga limpio.

El ritmo por defecto es 165 palabras por minuto, que viene del original en
inglés. En español no hay un promedio medido que podamos darte, y cambia mucho
entre personas. Pídele al usuario que lea un guion en voz alta con
cronómetro, cuenta palabras y pasa su ritmo con `--wpm`.

**5. Humanízalo.** Pasa el guion por `/ig-human` antes de enseñarlo. Una línea
que suena escrita se nota en cuanto alguien la dice en voz alta.

**6. Imprime el bloque.** El guion en un bloque de código, el texto en
pantalla como lista aparte con tiempos, y luego:

```
REEL LISTO
gancho:       #5 Colapso de tiempo, calificado 83 FUERTE
duración:     26.0s en 7 beats a 150 ppm
en pantalla:  6 tarjetas
humanizador:  4 artefactos quitados, puntuación humana 81 PASA
caption:      corre /ig-caption después

Responde "sí" para registrarlo, o dime qué cambio.
```

**7. Nunca publiques.** Este skill produce un guion. El usuario lo graba y lo
publica. Con un "sí", agrega a `~/.claude/instagram/log.md` la fecha, la
fórmula de gancho usada y la primera línea, para que `/ig-audit` tenga
historial después.

## El texto en pantalla es otro guion

Escríbelo aparte, siempre. Se lee antes de que se escuche.

- **Seis palabras o menos por tarjeta.** Lo está leyendo a la distancia de
  un brazo alguien que todavía no está escuchando.
- **La tarjeta del gancho está desde el cuadro 1**, no después de un silencio.
- **Mantenlo dentro de la zona segura.** En un cuadro de 1080x1920, nada arriba
  de y=230 ni debajo de y=1440, y deja libres los 230 píxeles de la derecha.
  La interfaz tapa todo lo que queda fuera de esa caja: el caption, la barra
  de acciones, la franja del audio.
- **Nunca pongas el gancho donde va el caption.** Es la parte de abajo del
  cuadro y queda tapada.
- **Subtítulos quemados en el cuerpo.** La mayoría ve primero sin sonido.

## Reglas que hacen la diferencia

- **Una idea por Reel.** Si el guion tiene dos, son dos Reels. Dilo.
- **Números en vez de adjetivos.** "$4,200" le gana a "un buen de lana". Si el
  usuario no dio un número, pídelo en lugar de escribir alrededor del hueco.
- **Corta la intro.** Sin saludo, sin "en este video", sin nombre, sin logo.
  El video empieza en la frase a la que normalmente llegarías en el segundo
  seis.
- **Cambia el cuadro en cada beat.** Una toma fija de 8 segundos es donde la
  gente se va, y `beats.py` lo va a marcar.
- **Una sola petición al final.** Comentar una palabra, guardar o seguir. Una.
- **Nunca inventes.** Nada de métricas, clientes, ingresos o resultados
  inventados a nombre del usuario, ni como relleno. Si hace falta un número y
  no lo sabes, deja `{{tu número}}` en el guion y márcalo.
- **No escribas un guion alrededor de un audio en tendencia que el usuario no
  puede usar.** Si la idea necesita su propia voz, dilo.

## Ejemplo

```
/ig-reel bajamos el tiempo de cada propuesta de 5 horas a 20 minutos con una plantilla
```

```
GANCHOS  (calificados)
  83  FUERTE  #5  Colapso de tiempo    "Antes me tardaba cinco horas en una propuesta. Ahora veinte minutos."
                                       en pantalla: 5 HORAS -> 20 MIN
  79  FUERTE  #1  Confesión de costo   "Me costó dos años cobrar cuatro horas de formato a la semana."
                                       en pantalla: 2 AÑOS TIRADOS
  61  OK      #9  Róbate esto          "Róbate la plantilla de propuesta que me ahorró cuatro horas."
                                       en pantalla: RÓBATE ESTO

Grabamos el #5: la proporción es creíble, se lee de un vistazo en pantalla
y el número es tuyo.
```

Las calificaciones y la clasificación de este ejemplo salen de correr los
scripts de esta carpeta sobre esas tres líneas. Las cifras del humanizador en
el bloque REEL LISTO son de formato, no de una corrida real.
