---
name: ig-repurpose
description: >-
  Convierte un contenido largo (un video de YouTube, un podcast, un live, un
  newsletter, un artículo de blog o una llamada con un cliente) en una semana
  de reels y carruseles. Úsalo cuando el usuario diga "reutiliza esto",
  "sácale reels a esto", "tengo un video/podcast/transcripción", "córtalo en
  pedazos", o pegue algo largo y lo quiera en Instagram.
---

# ig-repurpose

Un buen contenido largo trae dentro de cuatro a seis posts. La mayoría saca
uno y tira el resto.

## Entrada

Una transcripción, un artículo, un newsletter, un guion, el resumen de una
llamada, un live. Si el usuario da una URL y esta sesión tiene una herramienta
de transcripción, úsala; si no, pídele que lo pegue. Lee todo antes de
extraer nada.

Si la fuente es un video del propio usuario, pide también el archivo. Un Reel
hecho con su propio material gana a uno hecho con sus propias palabras leídas
otra vez.

## Extrae, no resumas

El resumen de un video no es un Reel. Nadie quiere el resumen. Recorre el
material y saca lo que se sostiene solo:

| qué sacar | qué es |
| --- | --- |
| **Afirmaciones** | cada oración que armaría una discusión |
| **Números** | cada cifra, costo, duración, porcentaje |
| **Historias** | cada momento con una persona, una escena y un costo |
| **Mecanismos** | cada "la forma en que esto funciona en realidad es..." |
| **Errores** | cada vez que admite algo que salió mal |
| **Frases** | cada oración que ya se puede citar tal cual |

Haz la lista de lo que encontraste, con conteos, antes de escribir nada. Si el
material da menos de cuatro piezas, está flaco, y cuatro posts exprimidos de
ahí van a salir flacos también. Dilo.

## Luego elige el formato para cada pieza

No todo es Reel.

- **Afirmación, error, historia** a Reel. Necesitan una voz y una cara.
- **Mecanismo, lista numerada** a carrusel. Necesitan releerse.
- **Una frase citable** a una historia, no a un post.

## Luego arma la semana

Cada pieza se vuelve un post y cada post se sostiene completamente solo. Quien
lo ve no ha visto la fuente y nunca la va a ver. Nunca escribas "como dije en
mi último video". El post es la cosa.

Asigna a cada uno una fórmula de gancho de `ig-reel/hooks.json` y varíalas.
Cinco posts de una misma fuente con la misma forma de gancho se leen como
fábrica de contenido, porque lo son.

Si la fuente es un video del usuario, **usa el material real**. El clip donde
dijo la frase, con la reacción real, le gana a regrabarlo siempre. Corta en la
oración, no en la respiración.

Ordena la semana para que la afirmación más fuerte vaya primero, la historia
caiga a mitad de semana y el mecanismo vaya al final, cuando la gente a la que
le gustaron los anteriores ya lo está esperando.

## Salida

El plan, con la fuente, los conteos de lo encontrado y la semana día por día.
Las fórmulas van por número de `ig-reel/hooks.json`:

```
FUENTE: "Por qué dejamos de hacer llamadas de diagnóstico" (podcast de 42 min, 8,900 palabras)

ENCONTRADO  5 afirmaciones, 9 números, 3 historias, 4 mecanismos, 2 errores, 7 frases citables

SEMANA
MAR  REEL       #2   Deja de hacer llamadas de diagnóstico
                     usa el clip del 14:20, se ríe al final
MIÉ  CARRUSEL        El formulario de 4 preguntas que reemplazó la llamada
VIE  REEL       #21  "...y nueve días después pidió que le devolviéramos el dinero"
DOM  REEL       #5   Seis horas a la semana de vuelta, un link borrado

Dime "escribe el martes" y lo redacto.
```

Después redacta cuando te lo pidan, uno por uno, cada uno por `/ig-reel` y
`/ig-human`. No sueltes cuatro guiones terminados de golpe. Todos van a sonar
igual y el usuario no va a grabar ninguno.
