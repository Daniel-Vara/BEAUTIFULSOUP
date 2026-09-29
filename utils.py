"""Funções compartilhadas pelos dois coletores (download e CSV)."""

import csv

import requests

# Definição de User-Agent personalizado para evitar bloqueios por requisições automatizadas
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PesquisaBS/1.0)"}


def baixar_pagina(url: str, timeout: int = 15) -> str:
    """Baixa o HTML de uma página. Levanta requests.RequestException em caso de falha."""
    resposta = requests.get(url, headers=HEADERS, timeout=timeout)
    resposta.raise_for_status()
    resposta.encoding = "utf-8"  # evita "Â£" no lugar de "£"
    return resposta.text


def salvar_csv(dados: list[dict], caminho: str) -> None:
    """Grava uma lista de dicionários em CSV (utf-8-sig abre certo no Excel)."""
    if not dados:
        return
    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=dados[0].keys())
        escritor.writeheader()
        escritor.writerows(dados)