# 03 · Recolección de ilustraciones

Igual que con los cuentos, aquí dejas tus imágenes listas y subes un CSV. Tu meta son 600 ilustraciones del género que te tocó. Recolectamos cuentos e ilustraciones por igual, así que esta parte es tan importante como la de texto.

## 1. Confirma tu asignación

En `coordinacion/asignaciones.csv` busca tu **género** y tu **fuente de ilustraciones** (es distinta a la de tus compañeros, para no repetir). Las fuentes y cómo descargar de ellas están en `docs/04_fuentes.md`. Usa solo imágenes libres o de dominio público.

## 2. Prepara tu carpeta

Crea una carpeta `mis_ilustraciones/` en la raíz del repo (tampoco se sube). Guarda ahí tus imágenes. Sirven `.png`, `.jpg` o `.jpeg`, y deben medir al menos 64x64 píxeles (las más chicas no sirven para entrenar).

```
mis_ilustraciones/
├── img_001.png
├── img_002.png
└── ...
```

Elige imágenes coherentes con el género: para `infantil` ilustraciones simples y coloridas, para `terror` algo más sombrío. Esa coherencia es la que el modelo va a aprender.

## 3. Llena tu tabla de metadatos

Copia `plantillas/metadata_ilustraciones_ejemplo.csv` a la raíz como `metadata_ilustraciones.csv`, un renglón por imagen:

```
archivo,genero,descripcion,fuente
img_001.png,infantil,animal de granja a colores,Wikimedia Commons
img_002.png,fantasia,bosque con un castillo,Openclipart
```

La `descripcion` es una frase corta de lo que se ve; nos sirve para el análisis y para emparejar estilos con los cuentos.

## 4. Indexa tus imágenes

```bash
python scripts/procesar_ilustraciones.py --usuario TU_USUARIO
```

El script revisa que cada imagen sea válida, anota su tamaño, le calcula una huella para detectar repetidas y arma `datos/ilustraciones/parciales/parcial_TU_USUARIO.csv`. Te avisa si descartó alguna (corrupta, muy chica o repetida).

Qué obtienes: un CSV que es el índice de tus imágenes (nombre, género, tamaño, descripción, fuente, tu nombre y la huella). Las imágenes en sí no van al CSV ni a GitHub: las juntamos todas en una carpeta compartida por Drive llamada `imagenes/`, que es de donde el modelo las leerá al entrenar.

## 5. Sube tu CSV y tus imágenes

Sube el CSV al repo con Git (`git add .`, `git commit -m "ilustraciones de TU_USUARIO"`, `git push`). Sube las imágenes a la carpeta compartida del Drive del equipo, no a GitHub (pesan demasiado).
