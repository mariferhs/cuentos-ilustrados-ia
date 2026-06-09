import argparse
import csv
import hashlib
import os
import re
import unicodedata
from pathlib import Path

# Generos con los que clasificamos todo el proyecto.
GENEROS_VALIDOS = {"infantil", "fabula", "fantasia", "terror", "ciencia_ficcion",
                   "aventura", "historico", "misterio", "romance", "realista", "otro"}

MIN_PALABRAS = 100
MAX_PALABRAS = 20000


def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"\s+", " ", texto)
    texto = re.sub(r"[^a-z0-9 ]", "", texto)
    return texto


def hash_texto(texto):
    return hashlib.sha1(normalizar(texto).encode("utf-8")).hexdigest()


def limpiar(texto):
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def cargar_metadata(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description="Procesa nuestros cuentos crudos y genera el CSV parcial de una persona.")
    parser.add_argument("--usuario", required=True, help="Tu usuario, ej. angel_reyes")
    parser.add_argument("--carpeta", default="mis_cuentos", help="Carpeta con los .txt")
    parser.add_argument("--metadata", default="metadata_cuentos.csv", help="CSV con archivo,titulo,autor,genero,fuente")
    parser.add_argument("--salida", default=None)
    args = parser.parse_args()

    salida = args.salida or f"datos/cuentos/parciales/parcial_{args.usuario}.csv"
    os.makedirs(os.path.dirname(salida), exist_ok=True)

    filas = []
    vistos = set()
    descartados = []

    for i, meta in enumerate(cargar_metadata(args.metadata), start=1):
        archivo = meta["archivo"].strip()
        ruta = Path(args.carpeta) / archivo
        if not ruta.exists():
            descartados.append((archivo, "archivo no encontrado"))
            continue

        texto = limpiar(ruta.read_text(encoding="utf-8", errors="ignore"))
        genero = meta["genero"].strip().lower()
        if genero not in GENEROS_VALIDOS:
            descartados.append((archivo, f"genero invalido: {genero}"))
            continue

        n = len(texto.split())
        if n < MIN_PALABRAS or n > MAX_PALABRAS:
            descartados.append((archivo, f"longitud fuera de rango: {n} palabras"))
            continue

        h = hash_texto(texto)
        if h in vistos:
            descartados.append((archivo, "duplicado dentro de tu carpeta"))
            continue
        vistos.add(h)

        filas.append({
            "id": f"{args.usuario}_{i:04d}",
            "titulo": meta["titulo"].strip(),
            "autor": (meta.get("autor") or "Anonimo").strip(),
            "genero": genero,
            "idioma": "es",
            "num_palabras": n,
            "fuente": meta.get("fuente", "").strip(),
            "recolector": args.usuario,
            "hash_texto": h,
            "texto": texto,
        })

    campos = ["id", "titulo", "autor", "genero", "idioma",
              "num_palabras", "fuente", "recolector", "hash_texto", "texto"]
    with open(salida, "w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)

    print(f"Guardados {len(filas)} cuentos en {salida}")
    if descartados:
        print(f"Descartados {len(descartados)}:")
        for archivo, motivo in descartados:
            print(f"  - {archivo}: {motivo}")


if __name__ == "__main__":
    main()
