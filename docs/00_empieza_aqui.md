# 00 · Empieza aquí

Bienvenido al proyecto. Esta guía es para que en cinco minutos entiendas qué estamos haciendo, por qué, y qué te toca a ti. Si solo vas a leer un archivo, que sea este.

## Qué estamos construyendo

Un sistema que genera cuentos ilustrados. Le pedimos un cuento de cierto género y nos devuelve dos cosas: el texto del cuento y una imagen que lo ilustra, las dos del mismo género. Para lograrlo entrenamos dos modelos de IA nuestros, desde cero, sin usar ChatGPT ni nada parecido.

## Por qué los datos son lo más importante

Como entrenamos los modelos desde cero, no parten de "saber" nada: aprenden únicamente de los ejemplos que les damos. Si les damos pocos ejemplos, o repetidos, o de mala calidad, el modelo sale malo. Por eso el trabajo grande de todos no es programar, sino conseguir muchos cuentos e imágenes, variados y bien etiquetados. Esa es la parte que el profe dijo que es la más difícil, y tiene razón: lo difícil es coordinarnos para no juntar lo mismo.

## Cómo nos repartimos el trabajo

Lo hacemos por igual: todos hacemos lo mismo. Cada persona recolecta cuentos y también ilustraciones, en la misma cantidad. No hay un grupo que solo busca texto y otro que solo busca imágenes; cada quien aporta de las dos cosas.

## Por qué clasificamos por género

A cada cuento e imagen le ponemos una etiqueta de género: `infantil`, `fabula`, `fantasia`, `terror`, `ciencia_ficcion`, `aventura`, `historico`, `misterio`, `romance`, `realista` u `otro`. Esa etiqueta es lo que después le dice al modelo qué tipo de cuento tiene que escribir y qué tipo de imagen dibujar. También es lo que conecta los dos modelos: el de texto y el de imagen usan la misma etiqueta, así el cuento y el dibujo quedan del mismo género.

## Qué te toca a ti

1. Busca tu nombre en `coordinacion/asignaciones.csv`. Verás tu género y de qué fuentes te toca sacar cuentos e imágenes. Te asignamos fuentes distintas a las de tus compañeros para que no junten lo mismo.
2. Reúne 600 cuentos siguiendo `docs/02_recoleccion_cuentos.md`.
3. Reúne 600 ilustraciones siguiendo `docs/03_recoleccion_ilustraciones.md`.
4. Pasa ambas cosas por su script, que te deja un archivo CSV limpio, y súbelo al repo.

Eso es tu parte. Cuando todos terminemos, unimos lo de cada quien, entrenamos los modelos y analizamos resultados (eso lo explican `docs/05` y `docs/06`).

## Una expectativa honesta

Con la cantidad de datos que vamos a juntar y entrenando desde cero, los cuentos van a salir cortos y con errores, y las ilustraciones borrosas. Eso es normal y está bien: el proyecto se califica por armar todo el sistema funcionando de punta a punta y por la coordinación de los datos, no por competir con las IA comerciales que se entrenaron con millones de ejemplos.
