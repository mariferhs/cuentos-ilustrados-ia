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
            tematica = fila["tematica"].strip()
            if texto and tematica:
                cuentos.append((tematica, texto))
    return cuentos


def construir_vocabularios(cuentos):
    caracteres = {PAD, INICIO, FIN}
    tematicas = set()
    for tematica, texto in cuentos:
        caracteres.update(texto)
        tematicas.add(tematica)
    char_a_idx = {c: i for i, c in enumerate(sorted(caracteres))}
    tematica_a_idx = {t: i for i, t in enumerate(sorted(tematicas))}
    return char_a_idx, tematica_a_idx


def preparar_ventanas(cuentos, char_a_idx, tematica_a_idx, longitud):
    ventanas = []
    for tematica, texto in cuentos:
        ids = [char_a_idx[INICIO]]
        ids += [char_a_idx[c] for c in texto if c in char_a_idx]
        ids += [char_a_idx[FIN]]
        t = tematica_a_idx[tematica]
        for i in range(0, len(ids) - 1, longitud):
            trozo = ids[i:i + longitud + 1]
            if len(trozo) >= 2:
                ventanas.append((t, trozo))
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
    entradas, objetivos, tematicas = [], [], []
    for tematica, seq in lote:
        seq = seq + [pad_idx] * (max_len - len(seq))
        entradas.append(seq[:-1])
        objetivos.append(seq[1:])
        tematicas.append(tematica)
    return (torch.tensor(entradas), torch.tensor(tematicas), torch.tensor(objetivos))


class GeneradorCuentos(nn.Module):
    def __init__(self, n_chars, n_tematicas, dim_char=96, dim_tematica=16, dim_oculto=256, capas=2):
        super().__init__()
        self.embed_char = nn.Embedding(n_chars, dim_char)
        self.embed_tematica = nn.Embedding(n_tematicas, dim_tematica)
        self.lstm = nn.LSTM(dim_char + dim_tematica, dim_oculto,
                            num_layers=capas, batch_first=True, dropout=0.2)
        self.salida = nn.Linear(dim_oculto, n_chars)

    def forward(self, x_chars, x_tematica, estado=None):
        b, t = x_chars.shape
        e_char = self.embed_char(x_chars)
        e_tematica = self.embed_tematica(x_tematica).unsqueeze(1).expand(b, t, -1)
        entrada = torch.cat([e_char, e_tematica], dim=2)
        h, estado = self.lstm(entrada, estado)
        return self.salida(h), estado


def main():
    parser = argparse.ArgumentParser(description="Entrena nuestro generador de cuentos (LSTM condicionada por tematica).")
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
    char_a_idx, tematica_a_idx = construir_vocabularios(cuentos)
    pad_idx = char_a_idx[PAD]
    print(f"Caracteres: {len(char_a_idx)}  Tematicas: {len(tematica_a_idx)}")

    ventanas = preparar_ventanas(cuentos, char_a_idx, tematica_a_idx, args.longitud)
    print(f"Ventanas de entrenamiento: {len(ventanas)}")

    cargador = DataLoader(
        CuentosDataset(ventanas), batch_size=args.lote, shuffle=True,
        collate_fn=lambda lote: colar(lote, pad_idx),
    )

    modelo = GeneradorCuentos(len(char_a_idx), len(tematica_a_idx),
                              dim_oculto=args.dim_oculto, capas=args.capas).to(dispositivo)
    optimizador = torch.optim.Adam(modelo.parameters(), lr=args.lr)
    criterio = nn.CrossEntropyLoss(ignore_index=pad_idx)

    for epoca in range(1, args.epocas + 1):
        modelo.train()
        perdida_total = 0.0
        for entradas, tematicas, objetivos in cargador:
            entradas = entradas.to(dispositivo)
            tematicas = tematicas.to(dispositivo)
            objetivos = objetivos.to(dispositivo)

            logits, _ = modelo(entradas, tematicas)
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
        json.dump({"char_a_idx": char_a_idx, "tematica_a_idx": tematica_a_idx}, f, ensure_ascii=False)

    print("Modelo guardado en", args.salida)


if __name__ == "__main__":
    main()
