---
name: ig-human
description: >-
  Quita la huella de máquina de cualquier borrador en español (rayas, léxico
  trillado de IA, caracteres invisibles de marca de agua) y lo califica con un
  panel de cinco revisiones antes de que salga. Úsala siempre que un texto
  tenga que sonar humano, cuando el usuario diga humaniza, "¿esto suena a
  IA?", "quita las rayas", "quítale lo de ChatGPT", "esto suena a robot", o
  antes de mostrarle al usuario cualquier caption, guion, comentario,
  respuesta o DM.
---

# ig-human

En esta carpeta hay dos herramientas y las dos corren de verdad. Úsalas. No
lo hagas a ojo.

```bash
python3 humanize.py borrador.txt --report        # lo limpia y muestra qué cambió
python3 detect.py borrador.txt                    # lo califica, cinco revisiones
python3 detect.py antes.txt despues.txt           # demuestra la diferencia
```

Las dos leen `slop.json`: 230 palabras y frases trilladas con reemplazos en
español llano, 18 clases de caracteres invisibles, 15 sustituciones
tipográficas y 18 señales estructurales. El léxico se armó para español, no se
tradujo del inglés: hay una entrada por género y número cuando hace falta
("innovador", "innovadora", "innovadores") para que la oración siga siendo
gramatical después del reemplazo. Las búsquedas ignoran mayúsculas y acentos,
así que "sumergete" sin acento también se detecta. El último bloque de cada
lista es específico de Instagram: el vocabulario que solo aparece en captions
y voz en off. Está hecho para editarse. Si el usuario siempre usa una palabra
que el léxico quita ("fundamental", "esencial", "optimizar"), sácala del
archivo.

## Por qué esto pesa más en Instagram de lo que parece

Los captions son cortos y los guiones se dicen en voz alta. Una línea que
suena a texto escrito ocupa más espacio en un caption de 600 caracteres que en
un ensayo, y una voz en off que nadie diría así se nota desde la primera toma.
La señal aquí no es que un detector marque el post. La señal es una persona
que sigue de largo porque aquello suena a marca, o un creador que se traba con
su propio guion.

## Qué se corrige solo

**1. Caracteres invisibles.** Espacios y uniones de ancho cero, word joiners,
guiones suaves, marcas de orden de bytes, caracteres de etiqueta Unicode,
separadores invisibles, espacios duros y estrechos. Un teclado no los produce.
Sobreviven al copiar y pegar, no se ven en ningún editor y son lo más mecánico
de un texto generado. `humanize.py` borra todos, incluido cualquier otro
carácter de formato Unicode que no tenga en la lista.

**2. Tipografía.** Raya a coma, semirraya a guion, comillas curvas y angulares
(« ») a rectas, el carácter de puntos suspensivos a tres puntos, viñeta a
guion. Los signos de apertura **¿ y ¡ nunca se tocan**: son ortografía, no
adorno. La raya es la pasada que importa: un inciso como "el dato, y es real,
cambia todo" queda con comas y luego se limpia la puntuación doble que eso
deja. La raya de diálogo al inicio de línea pasa a guion en lugar de coma,
para no romper el texto ("- ¿Cuánto cobras?, me preguntó").

**3. El léxico trillado.** sumérgete, potenciar, desbloquear tu potencial,
cabe destacar, sin lugar a dudas, es importante destacar, en conclusión, un
antes y un después, en el mundo actual, anglicismos como engagement, insights
y mindset, más el bloque de Instagram: "deja de hacer scroll", "en el video de
hoy", "sígueme para más", "guarda este post", "etiqueta a alguien que necesite
esto", "el algoritmo ama". Cada uno se cambia por una palabra llana o se
borra, respetando mayúsculas (también después de ¿ o ¡) y sin tocar URLs.

## Qué NO se corrige solo

Las señales estructurales se **marcan, no se reescriben**, porque cambiar la
forma de una oración necesita criterio:

- "No es solo X, es Y", "No es un destino, es un viaje" y "No solo X, sino también Y"
- "No se trata de X. Se trata de Y."
- Tríadas: "auténtico, relevante y constante."
- Preguntas retóricas de una línea: "¿El resultado?"
- El preámbulo de video: "en este video te voy a enseñar"
- La apertura "¿Sabías que...?"
- Listas con viñetas de emoji (✅ 👉)
- Tres o más palabras gritadas seguidas
- Muros de hashtags: Instagram limita a 5 hashtags por publicación desde
  diciembre de 2025, así que 6 o más se marcan
- Carnada por reflejo: "sígueme para más", "etiqueta a alguien", "dale like si",
  "guarda este post", "¿qué opinas?"

Esa lista es tu trabajo. Reescribe a mano cada línea marcada, conservando el
sentido, y vuelve a correr `detect.py`. Esta es la parte que mueve el puntaje
de REVIEW a PASS, y es la parte que un script no puede hacer.

## Las cinco revisiones

`detect.py` califica cinco señales de 0 a 100, más alto es más humano:

| revisión | qué mide | cómo se ve la máquina |
| --- | --- | --- |
| VARIACIÓN | variación en el largo de las oraciones | todas las oraciones miden lo mismo |
| ESPECIFICIDAD | cifras, números dichos con letra, nombres propios por cada 100 palabras | sustantivos abstractos, cero datos |
| DENSIDAD SLOP | términos del léxico por cada 100 palabras | vocabulario de plantilla |
| HUELLA | invisibles, rayas, comillas curvas o angulares por cada 1,000 caracteres | tipografía perfecta |
| VOZ | registro oral (o sea, la neta, pues, ¿no?), primera y segunda persona, señales estructurales | cero muletillas, revelaciones montadas |

El español no tiene contracciones como el inglés, así que la revisión VOZ
cuenta muletillas y marcas orales en su lugar. Los pronombres pesan un poco
menos de lo que pesaría en inglés porque el español omite el sujeto.

El veredicto pesa el promedio al 60% y la **revisión más débil** al 40%,
porque basta con una señal. PASS necesita 70 o más en total y ninguna revisión
debajo de 55. Los códigos de veredicto (PASS, REVIEW, FLAGGED) se dejan en
inglés para que otros scripts puedan leerlos.

## Dilo con honestidad

Son cinco heurísticas locales basadas en las señales en las que se fijan los
detectores públicos. Corren completas en la máquina del usuario y no se sube
nada. **No** son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no
llaman a esas APIs y no pueden prometer sus veredictos. Corregir lo que miden
suele mover esos números porque miden lo mismo de fondo. Esa es la
afirmación. No hagas una más grande en nombre del usuario y nunca le digas
que su texto es indetectable.

Los umbrales vienen del original en inglés y se ajustaron a mano para español.
**No se han validado con un corpus de textos en español**, así que trata el
puntaje como una guía para encontrar qué arreglar, no como una medición. En
las pruebas un caption humano bien escrito puede quedar en REVIEW por la
revisión VARIACIÓN; si pasa eso, léelo antes de cambiarlo.

## Orden de trabajo

1. `humanize.py borrador.txt -o limpio.txt --report`
2. Lee las señales estructurales. Reescribe esas líneas tú.
3. `detect.py borrador.txt limpio.txt` para mostrar el antes y el después.
4. Si el veredicto no es PASS, corrige la revisión más débil que indica la
   salida y repite. Dos rondas es normal. Cinco quiere decir que el borrador
   se escribió con fórmula, y la solución es otro borrador, no más pasadas.
5. Muéstrale al usuario el texto limpio y el puntaje. Nunca el puntaje solo.
