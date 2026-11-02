---
name: ig-profile
description: >-
  Califica un perfil de Instagram sobre 100 con una rúbrica de 12 puntos y
  reescribe las partes que pierden puntos: campo de nombre, bio, link,
  destacadas, los tres fijados y el grid. Úsalo cuando el usuario diga "optimiza
  mi perfil", "arregla mi bio", "califica mi Instagram", "por qué no me siguen",
  o pegue su perfil y pregunte cómo se lee.
---

# ig-profile

Casi todo mundo optimiza lo que no es. El perfil no es un aparador que la gente
recorre con calma. Es una **pantalla de decisión** a la que se llega desde un
solo reel, y tiene unos tres segundos para contestar una pregunta: ¿aquí hay
más de eso, y es para mí?

## Entrada

Pídele al usuario que pegue o mande captura de: el campo de nombre, el
@usuario, la bio, a dónde lleva el link, los nombres de las destacadas, qué
está fijado y las primeras nueve portadas del grid. Una captura de la parte de
arriba del perfil más las dos primeras filas del grid basta para una primera
revisión.

No inicies sesión en Instagram por el usuario.

## Califícalo

Lee `rubric.json` en esta carpeta. Doce puntos, 100 en total, cada uno con cómo
se ve la calificación completa y cómo suele fallar. Califica cada punto,
muestra la tabla y da el total. Sé honesto. La mayoría de los perfiles caen
entre 30 y 49 en la primera revisión, y una calificación generosa no sirve.

```
CALIFICACIÓN DEL PERFIL  38/100

  campo de nombre     2/12   solo el nombre, ninguna palabra que alguien busque
  primera línea bio   3/12   tres sustantivos y un emoji de café
  los tres fijados    0/10   nada fijado
  destacadas          2/8    "Random", "Vida", "2023"
  grid legible        4/8    seis de nueve portadas son una cara a media frase
  ...
```

## Luego reescribe, en este orden

Corrige de mayor a menor según los puntos que se pierden. No reescribas todo de
golpe: el usuario tiene que ir a cambiar cada cosa con su mano.

**1. El campo de nombre (30 caracteres).** La línea en negritas debajo de la
foto, no el @usuario. Es el campo que la búsqueda de Instagram compara, y la
mayoría de las cuentas ponen ahí un nombre y nada más. El formato que
funciona: `{Nombre} | {lo que haces, en palabras que se buscan}`. Por ejemplo
`Dana Ruiz | Contratos para freelancers`. Da tres opciones. Ojo con los
acentos: escribe las palabras como las escribe la gente al buscar, y si dudas,
da una opción con la forma más común.

**2. La primera línea de la bio.** Para quién es y qué cambia. No un puesto, no
adjetivos, no una lista de identidades separadas por barras. El resto de los
150 caracteres lleva una prueba o una oferta clara.

**3. Los tres fijados.** Tres espacios, tres trabajos distintos: la mejor
prueba, la explicación más clara de la oferta y la mejor presentación de la
persona. Es el arreglo con más impacto de todo el perfil y toma cuatro toques.
Un grid sin fijados muestra lo último que se publicó, que es un volado.

**4. Destacadas.** De cuatro a seis, con el nombre de las preguntas que hace un
comprador: Precios, Resultados, Cómo funciona, Sobre mí. No "Random". Borra el
resto.

**5. El link.** Un solo destino que coincida con lo que la bio acaba de
prometer. Se permiten cinco; dos ya es un menú, y un menú convierte peor que
una puerta.

**6. Portadas del grid.** Las primeras nueve, en tamaño miniatura. Las portadas
de los reels se eligen, no se dejan con el cuadro que haya tocado. Cuatro
palabras de texto en una portada hacen que el grid se entienda de un vistazo.

## Salida

La tabla de calificación, y luego las reescrituras como bloques listos para
copiar, en el orden de qué arreglar primero, cada una pasada por `/ig-human`.
Vuelve a calificar al final y muestra la diferencia con honestidad. Si la
reescritura llega a 84 y no a 98, di 84, y di qué necesita el resto, que casi
siempre es un grid, el hábito de subir historias y una publicación fijada que
todavía no existe. Nada de eso es una reescritura.

Esta skill no guarda nada en Instagram. El usuario edita cada campo.
