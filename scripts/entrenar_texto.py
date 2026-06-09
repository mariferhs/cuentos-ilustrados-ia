import argparse
import csv
import json
import os

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

csv.field_size_limit(10 * 1024 * 1024)

PAD = "\x00"      # relleno para igualar longitudes en el lote
INICIO = "\x02"   # marca el inicio de un cuento
FIN = "\x03"      # marca el final de un cuento


def cargar_dataset(ruta):
    cuentos = []
    with open(ruta, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            texto = fila["texto"].strip()
            genero = fila["genero"].strip()
            if texto and genero:
                cuentos.append((genero, texto))
    return cuentos


def construir_vocabularios(cuentos):
    caracteres = {PAD, INICIO, FIN}
    generos = set()
    for genero, texto in cuentos:
        caracteres.update(texto)
        generos.add(genero)
    char_a_idx = {c: i for i, c in enumerate(sorted(caracteres))}
    genero_a_idx = {g: i for i, g in enumerate(sorted(generos))}
    return char_a_idx, genero_a_idx


def preparar_ventanas(cuentos, char_a_idx, genero_a_idx, longitud):
    ventanas = []
    for genero, texto in cuentos:
        ids = [char_a_idx[INICIO]]
        ids += [char_a_idx[c] for c in texto if c in char_a_idx]
        ids += [char_a_idx[FIN]]
        g = genero_a_idx[genero]
        for i in range(0, len(ids) - 1, longitud):
            trozo = ids[i:i + longitud + 1]
            if len(trozo) >= 2:
                ventanas.append((g, trozo))
    return ventanas


class CuentosDataset(Dataset):
    def __init__(self, ventanas):
        self.ventanas = ventanas

    def __len__(self):
        return len(self.ventanas)

    def __getitem__(self, i):
        return self.ventanas[i]


def colar(lote, pad_idx):
    max_len = max(len(seq) for _, seq in lote)
    entradas, objetivos, generos = [], [], []
    for genero, seq in lote:
        seq = seq + [pad_idx] * (max_len - len(seq))
        entradas.append(seq[:-1])
        objetivos.append(seq[1:])
        generos.append(genero)
    return (torch.tensor(entradas), torch.tensor(generos), torch.tensor(objetivos))


class GeneradorCuentos(nn.Module):
    def __init__(self, n_chars, n_generos, dim_char=96, dim_genero=16, dim_oculto=256, capas=2):
        super().__init__()
        self.embed_char = nn.Embedding(n_chars, dim_char)
        self.embed_genero = nn.Embedding(n_generos, dim_genero)
        self.lstm = nn.LSTM(dim_char + dim_genero, dim_oculto,
                            num_layers=capas, batch_first=True, dropout=0.2)
        self.salida = nn.Linear(dim_oculto, n_chars)

    def forward(self, x_chars, x_genero, estado=None):
        b, t = x_chars.shape
        e_char = self.embed_char(x_chars)
        e_genero = self.embed_genero(x_genero).unsqueeze(1).expand(b, t, -1)
        entrada = torch.cat([e_char, e_genero], dim=2)
        h, estado = self.lstm(entrada, estado)
        return self.salida(h), estado


def main():
    parser = argparse.ArgumentParser(description="Entrena nuestro generador de cuentos (LSTM condicionada por genero).")
    parser.add_argument("--dataset", default="datos/cuentos/dataset_cuentos.csv")
    parser.add_argument("--salida", default="modelos")
    parser.add_argument("--longitud", type=int, default=160)
    parser.add_argument("--lote", type=int, default=64)
    parser.add_argument("--epocas", type=int, default=20)
    parser.add_argument("--lr", type=float, default=0.002)
    parser.add_argument("--dim_oculto", type=int, default=256)
    parser.add_argument("--capas", type=int, default=2)
    args = parser.parse_args()

    dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    print("Dispositivo:", dispositivo)

    cuentos = cargar_dataset(args.dataset)
    print(f"Cuentos cargados: {len(cuentos)}")
    char_a_idx, genero_a_idx = construir_vocabularios(cuentos)
    pad_idx = char_a_idx[PAD]
    print(f"Caracteres: {len(char_a_idx)}  Generos: {len(genero_a_idx)}")

    ventanas = preparar_ventanas(cuentos, char_a_idx, genero_a_idx, args.longitud)
    print(f"Ventanas de entrenamiento: {len(ventanas)}")

    cargador = DataLoader(
        CuentosDataset(ventanas), batch_size=args.lote, shuffle=True,
        collate_fn=lambda lote: colar(lote, pad_idx),
    )

    modelo = GeneradorCuentos(len(char_a_idx), len(genero_a_idx),
                              dim_oculto=args.dim_oculto, capas=args.capas).to(dispositivo)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=args.lr)
    criterio = nn.CrossEntropyLoss(ignore_index=pad_idx)

    for epoca in range(1, args.epocas + 1):
        modelo.train()
        perdida_total = 0.0
        for entradas, generos, objetivos in cargador:
            entradas = entradas.to(dispositivo)
            generos = generos.to(dispositivo)
            objetivos = objetivos.to(dispositivo)

            logits, _ = modelo(entradas, generos)
            perdida = criterio(logits.reshape(-1, logits.size(-1)), objetivos.reshape(-1))

            optimizador.zero_grad()
            perdida.backward()
            torch.nn.utils.clip_grad_norm_(modelo.parameters(), 5.0)
            optimizador.step()
            perdida_total += perdida.item()

        print(f"Epoca {epoca}/{args.epocas}  perdida={perdida_total / len(cargador):.4f}")

    os.makedirs(args.salida, exist_ok=True)
    torch.save({
        "estado": modelo.state_dict(),
        "dim_oculto": args.dim_oculto,
        "capas": args.capas,
    }, os.path.join(args.salida, "generador_texto.pt"))
    with open(os.path.join(args.salida, "vocabularios.json"), "w", encoding="utf-8") as f:
        json.dump({"char_a_idx": char_a_idx, "genero_a_idx": genero_a_idx}, f, ensure_ascii=False)

    print("Modelo guardado en", args.salida)


if __name__ == "__main__":
    main()
