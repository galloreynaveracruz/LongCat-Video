---
name: ig-caption
description: >-
  Escribe el caption de Instagram: la línea que sobrevive al corte de "... más",
  el cuerpo, la única petición, los términos de búsqueda y los hashtags, y lo
  revisa antes de publicar. Úsalo cuando el usuario diga "escribe el caption",
  "ponle texto a esto", "qué pongo en la descripción", tenga un reel o un
  carrusel listo y le falte el texto, o pregunte por hashtags.
---

# ig-caption

En esta carpeta vive una herramienta y funciona:

```bash
python3 caption.py caption.txt
python3 caption.py caption.txt --keywords "cotizaciones para clientes,precios de agencia"
```

Imprime el caption como lo imprime el feed: los primeros 125 caracteres dentro
de un recuadro y todo lo demás detrás del toque. Lee ese recuadro antes que
cualquier otra cosa que hayas escrito.

Revisa el texto en español sin importar los acentos: "escribeme" y "escríbeme"
cuentan igual, y "clausula de pago" encuentra "cláusula de pago". Reconoce las
peticiones típicas en español: "comenta CONTRATO", "escríbeme por DM",
"guárdalo", "compártelo", "sígueme", "link en bio", "desliza", "dime cuál
prefieres". Para el gancho cuenta cifras, montos, porcentajes, números dichos
con palabras ("tres años", "mil pesos") y nombres propios a media oración.

## Primero, decide qué trabajo tiene este caption

Esta es la decisión que arruina captions cuando te la saltas.

**Trabajo A: el video ya los enganchó.** Un Reel trae su propio gancho en los
primeros dos segundos, dicho y en pantalla. El caption no es un segundo gancho,
y competir con el video es la forma de perder los dos. Su trabajo es la
petición, el contexto que hace que la petición tenga sentido y las palabras
que la gente busca.

**Trabajo B: el caption es el contenido.** Una foto, una imagen sola, una
portada de carrusel que abre una duda. Aquí la primera línea es el gancho y
funciona igual que el gancho de un Reel: concreta, corta y cortada en un
momento de intriga, no a media subordinada.

Pregunta cuál de los dos estás escribiendo. Si el usuario tiene un Reel con un
gancho fuerte, escribe el A y explica por qué.

## La forma

```
Línea 1     125 caracteres de espacio visible. Trabajo A: la petición, clara.
            Trabajo B: el gancho.
            Nunca un saludo, nunca un hashtag, nunca un emoji como primer
            carácter.
Cuerpo      párrafos cortos, con una línea en blanco entre cada uno. De dos a
            seis. Aquí viven los términos de búsqueda.
Petición    una. Comentar una palabra clave, guardarlo o escribir por DM. Una.
Hashtags    hasta cinco, en su propia línea al final, o ninguno.
```

El límite es de 2,200 caracteres y casi nada necesita 2,200. Un caption que se
gana el toque y luego entrega 600 caracteres le gana a uno que entrega 1,800.

## Hashtags, con honestidad

Los hashtags ya no son una palanca de alcance, y la plataforma lo dijo con un
cambio de producto. **Instagram limitó los hashtags a cinco por publicación el
18 de diciembre de 2025**, antes eran treinta, y les dijo a los creadores que
"usar menos hashtags (hasta 5) y más específicos, en lugar de muchos
genéricos" funciona mejor. Adam Mosseri ya había dicho en febrero de 2025 que
los hashtags no sirven para aumentar el alcance y que son una etiqueta, no una
palanca de distribución.

Entonces: hasta cinco, específicos, como etiquetas de tema. Si el usuario tiene
un bloque de veinte guardado en sus notas, ese bloque ahora es peso muerto y el
revisor lo va a marcar como FAIL.

`#viral`, `#parati`, `#fyp`, `#explorepage`, `#tendencias` no describen nada.
Quítalos.

## Los términos de búsqueda importan más que los hashtags

La búsqueda de Instagram lee el texto del caption. Así que la frase con la que
el usuario quiere que lo encuentren va en el caption como la escribiría una
persona, dentro de una oración que se lea normal. "Cotizaciones para clientes"
como palabras en la línea tres, no "#cotizacionesparaclientes" en un bloque al
final.

Pide dos o tres de esos términos y pásaselos al revisor:

```bash
python3 caption.py borrador.txt --keywords "cotizaciones para clientes,precios de agencia"
```

## Reglas

- **Nada de links en el caption.** En el caption no se puede dar clic. Una URL
  en el texto es texto muerto que dice "no uso esta plataforma". Bio o DM.
- **Una sola petición.** Dos peticiones es lo mismo que ninguna. `caption.py`
  las cuenta.
- **La petición de palabra clave necesita una palabra que se pueda escribir.**
  Una palabra, sin espacios, sin emoji, en mayúsculas, y dila en voz alta en el
  video también. `Comenta CONTRATO` funciona. `Comenta "la guía del contrato"`
  no. Evita acentos en la palabra clave (`GUIA` mejor que `GUÍA`): mucha gente
  la escribe sin acento y la respuesta automática puede no reconocerla.
- **Escribe el primer comentario por separado** si hay un link. Dilo en el
  resumen.
- **Emojis como puntuación, no como decoración.** El revisor marca cualquier
  cosa arriba de 4 por cada 100 caracteres.
- **El texto alternativo vale 20 segundos.** En carruseles y fotos, escríbelo.
  Lo leen los lectores de pantalla y lo lee Instagram.

## El ciclo

1. Decide Trabajo A o Trabajo B y dilo.
2. Escribe el borrador.
3. Pásalo por `/ig-human`. Los captions son cortos, así que el texto genérico
   se nota más aquí que en cualquier otra parte del paquete.
4. Corre `caption.py` con los términos de búsqueda del usuario. Corrige cada
   FAIL. Decide cada WARN en voz alta, no en silencio.
5. Imprime el bloque listo para copiar y luego el resumen:

```
CAPTION LISTO
trabajo:    A, el reel trae el gancho
visible:    118 de 125 caracteres usados antes del corte
petición:   una, comenta CONTRATO
hashtags:   3
búsqueda:   "cotizaciones para clientes" en la línea 3, "precios de agencia" en la línea 5
revisor:    READY
```

Los códigos del revisor (PASS, WARN, FAIL y el veredicto READY, REVIEW, FIX) se
quedan en inglés porque son el contrato de `--json` que usan las otras
herramientas. El script imprime al lado lo que significa cada veredicto.

No se publica nada. El usuario lo pega.
