# 01 · Cómo nos organizamos

## El reparto

Somos 25 y trabajamos por igual: cada quien recolecta cuentos e ilustraciones en la misma cantidad. La cuota de cada persona es 600 cuentos y 600 ilustraciones. La cuenta nos sale así: 25 personas por 600 nos da 15,000 cuentos y 15,000 ilustraciones, que es el mínimo que pidió el profe para cada modelo. Si juntas más, mejor para todos.

Todo está escrito, persona por persona, en `coordinacion/asignaciones.csv`: ahí encuentras tu género asignado, tu fuente de cuentos y tu fuente de ilustraciones.

## El problema central: no juntar lo mismo

Si dos personas bajan los mismos cuentos o las mismas imágenes, el modelo ve el ejemplo repetido, no aprende a generalizar y se sesga. Lo atacamos en dos capas.

### Capa 1 — Repartir antes de empezar

En `asignaciones.csv` a cada quien le toca una combinación distinta de género y fuente. Así dos personas no buscan en el mismo sitio el mismo tipo de material, y es muy difícil que junten lo mismo. Además, al repartir todos los géneros entre el grupo, garantizamos que el dataset salga variado. Antes de empezar, confirma que estás trabajando la combinación que te tocó.

### Capa 2 — Quitar duplicados al unir

Cuando juntamos todo, los scripts `fusionar_cuentos.py` y `fusionar_ilustraciones.py` calculan una huella (un hash) de cada cuento y de cada imagen y eliminan automáticamente los repetidos exactos. En cuentos, además marcan los títulos repetidos por si son la misma historia con otro nombre (por ejemplo, las muchas versiones de Pinocho). A quien le salga un duplicado, lo repone con material nuevo.

## Roles

- Recolectores: todos. Cada quien sus 600 cuentos y 600 ilustraciones.
- Coordinador de datos (1 persona): corre los scripts de fusión cada cierto tiempo, revisa el reporte de duplicados y avisa a quien tenga que reponer.
- Encargado de entrenamiento (1 o 2 personas): cuando los datasets estén listos, corren el entrenamiento en Colab y comparten los modelos.

## Calendario sugerido

Tenemos unos 2 meses y medio. La recolección coordinada es lo que más tarda, así que no la dejemos para el final.

- Semanas 1-2: cada quien confirma su asignación y prueba los scripts con 20 o 30 muestras para agarrarle la mano.
- Semanas 3-6: recolección fuerte. Hacemos una fusión intermedia cada semana para cachar duplicados temprano.
- Semanas 7-8: cerramos los datasets, reponemos lo duplicado y congelamos la versión final.
- Semanas restantes: entrenamos los modelos, generamos ejemplos y armamos la presentación.
