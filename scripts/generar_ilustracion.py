import argparse
import json
import os

import torch
from PIL import Image

from entrenar_ilustraciones import VAECondicional, LADO


def cargar(carpeta):
    with open(os.path.join(carpeta, "generos_ilustracion.json"), encoding="utf-8") as f:
        genero_a_idx = json.load(f)["genero_a_idx"]
    estado = torch.load(os.path.join(carpeta, "vae_ilustracion.pt"), map_location="cpu")
    modelo = VAECondicional(len(genero_a_idx), dim_z=estado["dim_z"])
    modelo.load_state_dict(estado["estado"])
    modelo.eval()
    return modelo, genero_a_idx


def main():
    parser = argparse.ArgumentParser(description="Genera una ilustracion de un genero dado.")
    parser.add_argument("--modelo", default="modelos")
    parser.add_argument("--genero", required=True, help="Genero, ej. fantasia")
    parser.add_argument("--salida", default="ilustracion.png")
    parser.add_argument("--cantidad", type=int, default=1)
    args = parser.parse_args()

    modelo, genero_a_idx = cargar(args.modelo)
    if args.genero not in genero_a_idx:
        raise ValueError(f"Genero '{args.genero}' no existe. Disponibles: {sorted(genero_a_idx)}")

    dim_z = modelo.fc_mu.out_features
    with torch.no_grad():
        for i in range(args.cantidad):
            z = torch.randn(1, dim_z)
            genero = torch.tensor([genero_a_idx[args.genero]])
            img = modelo.decode(z, genero)[0]
            arr = (img.permute(1, 2, 0).numpy() * 255).astype("uint8")
            ruta = args.salida if args.cantidad == 1 else args.salida.replace(".png", f"_{i + 1}.png")
            Image.fromarray(arr, "RGB").save(ruta)
            print("Guardada", ruta)


if __name__ == "__main__":
    main()
