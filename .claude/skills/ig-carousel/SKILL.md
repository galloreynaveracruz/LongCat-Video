---
name: ig-carousel
description: >-
  Arma un carrusel de Instagram: la portada que se gana el deslizar, el texto
  diapositiva por diapositiva y los archivos de 1080x1350 para subir. Úsalo
  cuando el usuario diga "carrusel", "diapositivas", "slides", "post para
  deslizar", "conviértelo en carrusel", o tenga una idea en forma de lista o de
  pasos que se moriría como imagen sola.
---

# ig-carousel

Los carruseles son el formato del grid donde la gente se queda más tiempo,
porque deslizar es una interacción y hacer scroll no. Además tienen una segunda
oportunidad: Instagram puede volver a mostrar un carrusel a partir de una
diapositiva posterior a alguien que no interactuó la primera vez, así que la
diapositiva dos también tiene que sostenerse sola.

El formato premia una idea partida en pasos. Castiga un caption cortado en
pedazos.

## Cuándo usarlo en lugar de un Reel

Usa un carrusel cuando la idea tiene **secuencia y necesita releerse**: pasos,
un método con partes, un antes y después, una lista que vale la pena guardar en
captura. Usa un Reel cuando la idea tiene movimiento, una cara, o un remate que
hay que ver suceder.

Si la idea es una sola afirmación, no es ninguno de los dos. Pásasela a
`/ig-reel` y dilo.

## Estructura

De 6 a 10 diapositivas. El tope es 20, y 20 casi siempre es un libro que nadie
termina. Con menos de 5 el deslizar nunca arranca.

```
1         PORTADA   el gancho. 6 palabras o menos, a un tamaño que se lea en
                    el grid en miniatura. Una línea de promesa debajo.
2         LO QUE    por qué importa, en una oración. Esta diapositiva también
          ESTÁ EN   es una segunda portada, así que no puede ser preámbulo.
          JUEGO
3 a N     UNA IDEA POR DIAPOSITIVA. Un título de 3 a 7 palabras y máximo 25
                    palabras debajo. Si una diapositiva necesita un párrafo,
                    son dos diapositivas.
N+1       RESUMEN   todo como lista. Esta es la diapositiva de la captura.
ÚLTIMA    CTA       una acción. Guardar, comentar una palabra clave o seguir.
                    Una.
```

## Reglas para el texto de las diapositivas

- **La portada es el 80% del resultado.** Seis palabras. Grandes. Nada del
  resto del carrusel salva una portada que nadie desliza.
- **Diseña para el recorte del grid.** El grid del perfil recorta a un
  rectángulo vertical, más alto que ancho, y la proporción exacta ya cambió más
  de una vez. Construye a 1080x1350 y deja el texto de la portada bien adentro
  del centro, lejos de los 120 píxeles de cada orilla, y el recorte deja de
  importar.
- **Numera las diapositivas** (3/8). Más gente llega al final cuando puede ver
  dónde termina.
- **Ninguna diapositiva es un párrafo.** Si no se puede decir en 25 palabras,
  pártela.
- **La diapositiva de resumen es la que la gente captura y manda.** Los envíos
  son la señal más fuerte que te puedes ganar. Hazla independiente y que se
  entienda sin contexto.
- **Tu @usuario en cada diapositiva**, chiquito, en una esquina de abajo. Las
  capturas viajan sin ti.
- **Texto alternativo en la portada, como mínimo.** Lo leen los lectores de
  pantalla y lo lee Instagram.
- **Ojo con el largo del español.** El mismo mensaje suele ocupar más palabras
  en español que en inglés. Si una portada no cabe en seis palabras, recorta la
  idea, no el tamaño de la letra.

## Cómo hacer los archivos

Instagram pide 1080x1350 (4:5), JPEG o PNG, hasta 20 elementos. Hazlo en HTML e
imprime cada diapositiva:

```bash
# un <section> por diapositiva, 1080x1350, page-break-after: always
# luego Chrome headless --print-to-pdf, o el convertidor de HTML a imagen que ya uses
```

Escribe el HTML con `width:1080px; height:1350px`, un solo color de acento y
letra de 32px como mínimo, porque se lee en un celular a un tercio de su tamaño
real. Pon `<html lang="es">` y una fuente que tenga acentos, ñ, ¿ y ¡. Si el
proyecto tiene una skill de marca o un sistema de diseño, úsalo y no inventes
una paleta.

## Salida

Primero el texto diapositiva por diapositiva, como lista numerada que el
usuario pueda leer en diez segundos y editar antes de generar nada. Luego el
**caption**, que en un carrusel es el Trabajo B de `/ig-caption`: aquí el
caption sí trabaja, porque la portada ya gastó sus seis palabras.

Pasa los dos por `/ig-human`. Genera los archivos solo cuando el usuario
apruebe el texto.

```
CARRUSEL  ·  8 diapositivas

1  PORTADA  LA CLÁUSULA DE $18,000
            Una línea que ahora va en todos mis contratos.
2  EN JUEGO Aprobé el trabajo. Nueve días después me pidieron el dinero de vuelta.
3           QUÉ DICE
            Pago contra entrega, no contra aprobación.
...
7  RESUMEN  Las cuatro líneas, en orden.
8  CTA      Comenta CONTRATO y te mando la cláusula completa.

Caption: Trabajo B, gancho en la línea 1, una petición, 3 hashtags.
```

No se sube nada. El usuario lo publica.
