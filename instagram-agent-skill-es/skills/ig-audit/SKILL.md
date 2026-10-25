---
name: ig-audit
description: >-
  Análisis post mortem de lo que el usuario ya publicó: qué reels funcionaron
  de verdad, por qué, y qué dejar de hacer. Úsalo cuando el usuario pegue sus
  estadísticas de Instagram o posts anteriores y pregunte "¿qué está
  funcionando?", "¿por qué no pegó esto?", "lee mis estadísticas", "audita mi
  contenido", o quiera saber de qué hacer más.
---

# ig-audit

La única fuente honesta de qué funciona para una cuenta es esa misma cuenta.
Cada regla de cada guía de Instagram, incluidas las de este pack, es una
suposición previa. Los últimos 30 posts del usuario son la evidencia.

## Entrada

Pide lo que el usuario tenga:

- Estadísticas por post: reproducciones, alcance, interacciones, tiempo de
  visualización, guardados, compartidos, seguidores nuevos y qué parte del
  alcance vino de gente que no lo sigue. Las capturas sirven.
- O la gráfica de retención de sus mejores y peores reels recientes. Esa sola
  captura vale más que todo lo demás junto.
- O solo los posts y sus reproducciones, que alcanza para una primera pasada.

Lee también `~/.claude/instagram/log.md` si existe, porque ahí queda qué
fórmula de gancho usó cada post.

## Qué medir de verdad

Las reproducciones a secas son el número menos útil de la pantalla, porque
dependen sobre todo de cuánta gente ya sigue la cuenta. Calcula esto en su
lugar y muestra las cuentas:

| métrica | cómo | qué te dice |
| --- | --- | --- |
| **Múltiplo outlier** | reproducciones / mediana de reproducciones de la propia cuenta | si fue un éxito real o un día normal |
| **Alcance a no seguidores** | % del alcance de gente que no sigue la cuenta | si viajó o no |
| **Retención a 3 s** | quienes siguen a los 3 s / quienes empezaron | si el gancho funcionó. Esta es la calificación del gancho. |
| **Tiempo promedio de visualización** | directo de las estadísticas | si funcionó la parte de en medio |
| **Envíos por alcance** | compartidos / alcance | la señal individual más fuerte que puedes ganarte. Un envío es alguien poniendo su nombre detrás. |
| **Seguidores por alcance** | seguidores nuevos / alcance | si el perfil convirtió la atención |

Ordena por múltiplo outlier y envíos por alcance, no por reproducciones. Un
reel con 4,000 reproducciones y 90 envíos le ganó al de 60,000 con 11.

## Luego encuentra el patrón

Con los cinco mejores y los cinco peores lado a lado, busca qué los separa, y
atrévete a concluir algo que al usuario no le va a gustar:

- **Retención a 3 segundos.** Si los de arriba y los de abajo difieren aquí,
  es el gancho y nada más, y todo lo que viene después es distracción.
- **Fórmula de gancho.** ¿Qué ids de `ig-reel/hooks.json` están en los cinco
  mejores?
- **Formato.** Reel, carrusel, imagen sola.
- **Duración.** Agrupa en menos de 15 s, 15 a 30 s, 30 a 60 s, más de 60 s.
- **Tema.**
- **Si el usuario respondió comentarios en la primera hora.**
- **Día y hora.** Revisa esto **al final** y solo si lo demás no muestra
  nada. Casi nunca es la causa y es donde la gente quiere que esté.

Plantea el hallazgo como una afirmación con la evidencia al lado, y di qué tan
seguro estás. Con 30 posts se puede ver un patrón. Con 6 no, y decirlo es
mejor que inventar uno.

## La distinción que ahorra meses

**Un reel que tiene reproducciones y no trae seguidores no es un reel
fallido, es un problema de perfil.** Un reel sin reproducciones es un problema
de gancho. Separa las dos cosas antes de recomendar nada. Si el alcance a no
seguidores es alto y los seguidores por alcance son bajos, deja de reescribir
ganchos y ve a `/ig-profile`.

## Salida

```
AUDITORÍA  ·  31 posts  ·  12 jun - 5 sep  ·  mediana 4,100 reproducciones

TOP 5 POR MÚLTIPLO OUTLIER
  18.2x  #3   74,600 reprod.  62% no seguidores  ret. 3 s 71%  128 envíos
   6.4x  #1   26,300 reprod.  48% no seguidores  ret. 3 s 64%   71 envíos
  ...

LOS 5 DE ABAJO
   0.3x  #11   1,200 reprod.   9% no seguidores  ret. 3 s 31%    2 envíos
  ...

LO QUE DICEN LOS DATOS
1. La retención a 3 segundos lo explica todo. Los cinco mejores promedian 66%,
   los cinco peores 33%. Todo lo demás que te preocupa depende de los primeros
   dos segundos.
2. Los posts donde tú quedabas mal: promedio de 8.1x contra 0.9x del resto.
   n=5. Es la señal más fuerte aquí y no hay comparación.
3. Las listas de herramientas traen reproducciones y nada más. Mucho alcance,
   cero envíos, cero seguidores. Son tres de tus cinco peores.
4. El día de la semana no muestra nada. Tus promedios de martes y viernes
   están dentro del ruido. Deja de optimizarlo.

DEJA DE HACER: listas de herramientas.
HAZ MÁS: los que traen algo que te costó y un número.
```

Los números del ejemplo son ilustrativos: en una auditoría real salen solo de
los datos que pegó el usuario.

Luego pásale las conclusiones a `/ig-plan` para que la siguiente semana se
arme con la evidencia del propio usuario y no con valores por default, y a
`/ig-viral` para que el archivo de referencias se filtre a las fórmulas que
funcionan para esta cuenta en específico.
