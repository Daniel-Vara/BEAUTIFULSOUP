"""
Projeto Beautiful Soup — coletores de dados web
===============================================

Uso:
    python main.py livros                  # livros de books.toscrape.com
    python main.py github                  # repositórios Python em alta (hoje)
    python main.py github -l javascript -p weekly
    python main.py tudo                    # roda os dois coletores
"""

import argparse
import sys

import requests

import github_trending
import livros
from utils import baixar_pagina, salvar_csv


def rodar_livros() -> bool:
    """Executa o pipeline do coletor de livros: download, extração, exibição e salvamento."""
    print("🔎 Coletando livros...")
    try:
        html = baixar_pagina(livros.URL)
    except requests.RequestException as erro:
        print(f"Erro ao acessar a página: {erro}", file=sys.stderr)
        return False

    dados = livros.extrair_livros(html)
    if not dados:
        print("Nenhum livro encontrado. A estrutura do site pode ter mudado.")
        return False

    livros.exibir_resumo(dados)
    salvar_csv(dados, livros.ARQUIVO_SAIDA)
    print(f"\n✅ Dados salvos em: {livros.ARQUIVO_SAIDA}")
    return True


def rodar_github(linguagem: str, periodo: str) -> bool:
    """Executa o pipeline do coletor do GitHub: monta URL, baixa, extrai e salva em CSV."""
    print("🔎 Coletando dados do GitHub Trending...")
    try:
        html = baixar_pagina(github_trending.montar_url(linguagem, periodo))
    except requests.RequestException as erro:
        print(f"Erro ao acessar a página: {erro}", file=sys.stderr)
        return False

    dados = github_trending.extrair_repositorios(html)
    if not dados:
        print("Nenhum repositório encontrado. A estrutura do site pode ter mudado.")
        return False

    github_trending.exibir_resumo(dados, linguagem)
    salvar_csv(dados, github_trending.ARQUIVO_SAIDA)
    print(f"\n✅ Dados salvos em: {github_trending.ARQUIVO_SAIDA}")
    return True


def main() -> None:
    """Função principal que gerencia os argumentos via linha de comando (argparse)."""
    parser = argparse.ArgumentParser(description="Coletores web com Requests + Beautiful Soup")
    parser.add_argument("coletor", choices=["livros", "github", "tudo"],
                        help="qual coletor executar")
    parser.add_argument("-l", "--linguagem", default="python",
                        help="linguagem no GitHub Trending (padrão: python)")
    parser.add_argument("-p", "--periodo", default="daily",
                        choices=["daily", "weekly", "monthly"],
                        help="período do GitHub Trending (padrão: daily)")
    args = parser.parse_args()

    resultados = []
    if args.coletor in ("livros", "tudo"):
        resultados.append(rodar_livros())
    if args.coletor in ("github", "tudo"):
        resultados.append(rodar_github(args.linguagem, args.periodo))

    if not all(resultados):
        sys.exit(1)


if __name__ == "__main__":
    main()