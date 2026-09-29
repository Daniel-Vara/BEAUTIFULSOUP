"""Coletor de livros do site de práticas books.toscrape.com."""

from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
ARQUIVO_SAIDA = "livros.csv"


def extrair_livros(html: str) -> list[dict]:
    """Extrai título, preço e disponibilidade de cada livro da página."""
    soup = BeautifulSoup(html, "html.parser")
    livros = []

    # Percorre cada cartão de produto encontrado na página
    for livro in soup.select("article.product_pod"):
        titulo = livro.h3.a["title"]  # o texto visível costuma vir truncado
        preco = livro.select_one("p.price_color").get_text(strip=True)
        disponibilidade = livro.select_one("p.instock.availability").get_text(strip=True)
        livros.append({
            "titulo": titulo,
            "preco": preco,
            "disponibilidade": disponibilidade,
        })

    return livros


def exibir_resumo(dados: list[dict]) -> None:
    """Imprime uma tabela formatada no terminal com os dados coletados."""
    print("\n📚 Livros em books.toscrape.com\n")
    print(f"{'Título':<45} {'Preço':<10} {'Disponibilidade'}")
    print("-" * 75)
    for livro in dados:
        print(f"{livro['titulo'][:43]:<45} {livro['preco']:<10} {livro['disponibilidade']}")
    print(f"\nTotal de livros coletados: {len(dados)}")