---
name: ig-comment
description: >-
  Escribe comentarios en posts y reels de otras cuentas de Instagram que se
  lean como una persona con opinión, no como un bot. Úsalo cuando el usuario
  pegue un post o un reel y quiera un comentario, diga "comenta esto",
  "ayúdame a interactuar con esto", "¿qué le pongo aquí?", o quiera una tanda
  para su ronda diaria de interacción.
---

# ig-comment

Comentar son los veinte minutos que más rinden en Instagram y los más fáciles
de hacer mal. Un comentario arriba de todo en un reel con 40,000 vistas lo ve
más gente que la mayoría de los posts de esa misma cuenta, y es el único lugar
donde un desconocido puede tocar y llegar directo a un perfil.

Un comentario genérico es peor que no comentar. Gasta un toque que no lleva a
ningún lado y te marca como cuenta de "pod de interacción" ante la única
persona cuya opinión importaba: quien creó el contenido.

## Entrada

El usuario pega el texto del post o del reel, o una captura, con el nombre de
la cuenta. Si te da una URL que no puedes abrir, pídele que la pegue. No uses
una herramienta de navegador para scrapear el feed y no publiques nada.

## Los nueve tipos de comentario

Elige según lo que el post realmente es. Nunca te vayas por default al tipo 1.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Suma un dato** | el post hace una afirmación que puedes respaldar con un número | "A nosotros igual: el 40% de..." |
| 2 | **Suma el caso que falta** | el post tiene razón pero está incompleto | "Esto aplica hasta que {condición}." |
| 3 | **Desacuerdo con respeto** | de verdad crees que está mal | primero en qué coincides, luego dónde te separas |
| 4 | **Estira una línea** | hay una frase que es la buena | cítala y construye sobre ella |
| 5 | **Haz la pregunta de fondo** | el post se saltó la parte difícil | una sola pregunta, concreta |
| 6 | **La prueba** | tú ya hiciste lo que describen | qué pasó, en dos oraciones |
| 7 | **La corrección** | hay un error de dato | ten razón, sé breve, sé amable, asegúrate |
| 8 | **El otro ángulo** | datos correctos, encuadre equivocado | "Otra forma de verlo:" |
| 9 | **El de una línea** | el post no necesita nada, solo quieres presencia | menos de 10 palabras, tiene que ser gracioso o cierto |

## Reglas

- **De una a tres oraciones.** Los comentarios de Instagram se leen en una
  columna angosta debajo de un video. Un párrafo se colapsa detrás de "más" y
  nadie lo abre.
- **Nunca empieces con** "Excelente post", "Me encanta", "Tal cual", "Esto 👏",
  "Lo necesitaba hoy", "Qué gran contenido" ni con el nombre de quien publicó
  seguido de signo de exclamación. Todos son invisibles.
- **Nada de comentarios solo con emojis** y ningún emoji como primer carácter.
- **Nunca repitas lo que dice el reel.** Todos los que lo están viendo
  acaban de verlo.
- **Una sola idea.** Un comentario con dos puntos se lee como que te estás
  adueñando del post.
- **Di lo concreto.** Si el comentario podría ir debajo de cualquier post
  sobre el tema, no es un comentario, es ruido.
- **Cero autopromoción, nunca.** Ni la oferta, ni el link, ni "pásate por mi
  perfil". Es la forma más rápida de que te bloquee justo la persona a la que
  querías llegar.
- **Llegar temprano pesa más aquí que en cualquier otro lado.** Un comentario
  en la primera hora de un reel que luego se mueve, se mueve con él.

## Salida

Da **dos opciones de tipos distintos**, etiquetadas, más una línea sobre cuál
publicarías y por qué. Pasa las dos por `/ig-human` primero: los comentarios
son cortos, así que una raya o una frase hecha se nota proporcionalmente más
que en un caption.

```
OPCIONES DE COMENTARIO  (en el reel de @cuenta sobre precios)

[6 · La prueba]
Subimos precios 40% en marzo y perdimos exactamente un cliente, el que nos
llenaba medio inbox. Tardé ocho meses en dejar de tenerle miedo.

[3 · Desacuerdo con respeto]
Coincido en lo del ancla. Donde no estoy tan seguro es en hacerlo a mitad de
proyecto. Lo intentamos así y nos costó una renovación que iba bien.

Publica el primero. Reconoce algo y trae un número.
```

## Modo tanda

Para una ronda de interacción, pide los 5 a 10 posts como texto pegado en un
solo mensaje, devuelve un comentario por post en un solo bloque y lleva una
nota en `~/.claude/instagram/log.md` de a quién ya comentaste esta semana.
Comentar todos los días en las mismas tres cuentas se nota, y se ve
exactamente como lo que es.

## Nunca

No publiques automáticamente, no automatices comentarios y no uses una
herramienta de navegador para publicar en nombre del usuario. La interacción
automatizada viola las Condiciones de uso de Instagram y hace que bloqueen
acciones de la cuenta. Esta skill escribe el comentario. El usuario lo publica.
