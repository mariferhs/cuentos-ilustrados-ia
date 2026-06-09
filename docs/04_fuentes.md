# 04 · Fuentes

Esta lista está revisada para que de verdad se pueda **descargar el texto completo** (o copiarlo de la página), no catálogos de venta. Cada quien tiene su fuente asignada en `coordinacion/asignaciones.csv`. Usa material gratuito y, de preferencia, de dominio público o licencia libre.

## Atajo: datasets ya armados

Antes de recolectar a mano, vale la pena aprovechar dos datasets que ya existen (scrapeados de cuentos en español). El coordinador puede integrarlos y repartir solo lo que falte:

- **Hugging Face `Fernandoefg/cuentos_es`** — unos 7,239 cuentos en CSV, con autor, país, título, categoría y texto completo. Atajo enorme.
- **GitHub `karen-pal/borges`** — 719 cuentos de 58 autores latinoamericanos (Borges, Cortázar, Rulfo, etc.) en CSV, uso libre con atribución.

Nota: ambos provienen de Ciudad Seva, así que hay que deduplicar entre ellos, y su licencia no es totalmente clara, conviene usarlos con fines académicos.

## Fuentes para descarga masiva (dominio público)

- **Project Gutenberg en español** (gutenberg.org/browse/languages/es) — clásicos y cuentos del s.XIX-XX, descarga directa en .txt y ePub. Para bajar en lote existe el scraper oficial openzim/gutenberg (filtra por idioma `es`).
- **Wikisource en español** (es.wikisource.org, Categoría:Cuentos) — más de mil páginas de cuentos; texto en HTML para copiar y descargable como PDF; también accesible por la API de MediaWiki para lote.
- **Internet Archive** (archive.org, filtro idioma español) — muchos ítems traen "Full Text" en .txt descargable. Para lote, la herramienta `ia` de Python.
- **Biblioteca Virtual Miguel de Cervantes** (cervantesvirtual.com) — literatura en español a texto completo en HTML/PDF; tiene portal de Literatura Infantil y Juvenil.
- **Elejandría** (elejandria.com) — clásicos por categorías (terror, ciencia ficción, infantil, aventura), descarga directa en ePub/PDF sin registro.
- **Biblioteca Digital Hispánica / BNE** (bdh.bne.es) — obras digitalizadas con PDF y texto OCR; hay dataset de datos abiertos en datos.gob.es con enlaces al texto.

## Fuentes por tipo de cuento (recolección uno por uno)

- **Ciudad Seva** (ciudadseva.com) — miles de cuentos de autores clásicos (Poe, Chéjov, Quiroga, Cortázar…), texto completo en la web. Ideal para `fantasmas_y_misterio`, `mar_y_oceano`, `heroes_y_aventuras`.
- **Cuentos para Dormir** (cuentosparadormir.com) — cientos de cuentos infantiles originales, descargables en PDF. Bueno para `animales`, `princesas_y_castillos`, `dinosaurios_y_prehistoria`.
- **Bosque de Fantasías** (bosquedefantasias.com) — cuentos infantiles cortos y fábulas, texto en la web. Para `animales`, `magia_y_brujas`, `dinosaurios_y_prehistoria`.
- **Rincón Castellano** (rinconcastellano.com/cuentos) — cuentos clásicos de Andersen, Grimm, Perrault. Para `magia_y_brujas`, `princesas_y_castillos`.
- **Cuentos para Algernon** (cuentosparaalgernon.wordpress.com) — ciencia ficción, fantasía y terror traducidos, texto completo en la web. Para `espacio`, `robots_y_tecnologia`, `monstruos_y_criaturas`.
- **Cactus Pink** (cactuspink.net) — ciencia ficción, terror y fantástico en español. Para `espacio`, `monstruos_y_criaturas`.
- **Ciencia Ficción México** (cienciaficcionmexico.com) — relatos de CF y terror de autores mexicanos. Para `robots_y_tecnologia`, `espacio`.

Ojo: los sitios contemporáneos (Cuentos para Dormir, Bosque de Fantasías, Cactus Pink, Algernon, Ciencia Ficción México) tienen derechos de autor; sirven para este proyecto académico, pero no son dominio público.

## Fuentes de ilustraciones (estilo plano a color, ver docs/03)

Elegimos fuentes que tienen mucho material en estilo plano/caricatura, que es el que acordamos:

- **Openclipart** (openclipart.org) — clipart vectorial plano, dominio público (CC0). La más recomendada.
- **Pixabay** (pixabay.com, filtro "ilustraciones/vectores") — ilustraciones planas gratis, sin atribución obligatoria.
- **Wikimedia Commons** (commons.wikimedia.org, categoría clip art / ilustraciones) — imágenes libres.
- **Vecteezy** (vecteezy.com, sección gratis) — ilustraciones vectoriales planas (atribución en el plan gratuito).
- **Rawpixel** (rawpixel.com, sección dominio público) — ilustraciones libres.

## Recordatorio importante

No juntes material generado por IA. Si entrenamos con texto o imágenes hechas por otra IA, nuestro modelo aprende los patrones de esa IA y no los de cuentos e ilustraciones reales. Siempre material humano.
