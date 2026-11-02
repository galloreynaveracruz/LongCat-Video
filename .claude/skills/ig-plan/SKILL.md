---
name: ig-plan
description: >-
  Arma la semana en Instagram: qué publicar, en qué formato, cuándo y con quién
  interactuar. Úsalo cuando el usuario diga "planea mi semana", "qué publico",
  "calendario de contenido", "no tengo nada que publicar", o quiera un horario
  de publicación y una lista de cuentas para interactuar.
---

# ig-plan

El cuarto de control. Todo lo demás en este paquete ejecuta; esto decide qué se
ejecuta. Córrelo una vez por semana, el mismo día.

## Entrada

Si existen `~/.claude/instagram/voice.md`, `swipe.md` y `log.md`, léelos. El
archivo swipe es la evidencia del propio usuario, sacada con `/ig-viral`, de
qué fórmulas están funcionando en su nicho ahorita, y pesa más que cualquier
cosa de este archivo. El log evita que el plan repita un tema de las últimas
dos semanas.

Si no existen, pide cuatro cosas y anótalas:

1. Qué vende el usuario, y a quién.
2. Los tres o cuatro temas por los que quiere que lo conozcan.
3. Qué pasó de verdad esta semana: una llamada con un cliente, un número, un
   error, algo que construyó, una discusión que tuvo. De ahí salen las
   publicaciones.
4. Diez cuentas ante las que vale la pena ser visible.

## Qué publicar

De cuatro a cinco publicaciones a la semana, y al menos tres de ellas Reels.
Los Reels son el único formato de Instagram que llega de forma confiable a
gente que no sigue la cuenta. Los carruseles profundizan con la gente que ya la
sigue. Las historias son diarias y se planean aparte.

Mezcla a lo largo de la semana, nunca dos del mismo tipo seguidas:

| tipo | cuántas | trabajo |
| --- | --- | --- |
| **Prueba** | 1 por semana | algo que pasó, con un número. Reel. |
| **Enseñanza** | 1 a 2 por semana | una cosa que el espectador puede hacer hoy. Reel o carrusel. |
| **Opinión** | 1 por semana | una postura que te podría costar seguidores. Reel. |
| **Historia** | 1 cada dos semanas | una escena con un costo. Reel. |
| **Oferta** | 1 cada dos semanas | lo que vendes, dicho claro, sin pedir perdón. Carrusel o historias. |

Para cada espacio da: el tema, el ángulo específico sacado de lo que pasó esta
semana, el formato y el número de fórmula de gancho de `ig-reel/hooks.json`.
No un tema, un ángulo. "IA" no es un plan. "La propuesta que perdimos porque el
borrador sonaba a ChatGPT" es un Reel.

## Cuándo publicar

Publica cuando la audiencia del usuario esté despierta y no esté trabajando.
Para la mayoría de las audiencias de consumo eso es temprano en la noche, hora
local; para una audiencia de negocios, temprano en la mañana.

Pero dilo claro: **la hora importa mucho menos que los primeros dos segundos.**
Instagram sigue mostrando un Reel durante días si funciona, y entierra uno
publicado a la hora perfecta si no funciona. Si el usuario está optimizando
horarios antes de que sus ganchos funcionen, está puliendo lo que no es, y se
lo tienes que decir.

Usa la zona horaria de la audiencia, no la del usuario, si son distintas. En
Latinoamérica es común que no coincidan: una audiencia repartida entre CDMX,
Bogotá y Buenos Aires abarca hasta tres horas de diferencia.

## La ronda de interacción, que no es opcional

20 minutos al día, antes de publicar, no después. Arma una lista de 10:

- **5 de alcance**: cuentas con la audiencia que el usuario quiere, donde un
  buen comentario se ve. Comenta temprano, antes de que el hilo tenga 200
  comentarios.
- **3 pares**: mismo tamaño, mismo campo. Este es el grupo que corresponde.
- **2 compradores**: gente que de verdad podría comprar. Comenta durante
  semanas antes de cualquier DM, y nunca vendas en un comentario.

Pásale la lista a `/ig-comment`.

## Salida

```
SEMANA DEL 15 DE SEPTIEMBRE

LUN  solo interacción  (20 min, lista abajo)
MAR  7:30pm  REEL      PRUEBA     #5   de 5 horas de cotización a 20 minutos
MIÉ  solo historias + interacción
JUE  7:00pm  CARRUSEL  ENSEÑANZA  caption Trabajo B   la cláusula explicada en 4 diapositivas
VIE  7:30pm  REEL      OPINIÓN    #2   deja de hacer llamadas de descubrimiento
SÁB  -
DOM  6:00pm  REEL      HISTORIA   #21  el correo del reembolso

HISTORIAS  todos los días, de 3 a 5 cuadros, caja de preguntas el jueves.

INTERACCIÓN  (5 de alcance / 3 pares / 2 compradores)
  ...

Di "escribe el martes" y lo redacto.
```

Los números (#5, #2, #21) son los `id` de las fórmulas en
`ig-reel/hooks.json`; busca ahí el nombre de cada una.

Escribe el plan en `~/.claude/instagram/plan.md` para que las demás skills lo
puedan leer. No se programa ni se publica nada en ningún lado. Esto es un plan
y el usuario lo ejecuta.
