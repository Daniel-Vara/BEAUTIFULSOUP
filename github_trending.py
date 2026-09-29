"""Coletor de repositórios em alta no GitHub Trending."""

from datetime import date

from bs4 import BeautifulSoup

ARQUIVO_SAIDA = "repositorios_trending.csv"


def montar_url(linguagem: str = "python", periodo: str = "daily") -> str:
    """Constrói a URL dinâmica baseada na linguagem e no período solicitado."""
    return f"https://github.com/trending/{linguagem}?since={periodo}"


def extrair_repositorios(html: str) -> list[dict]:
    """Extrai nome, descrição, linguagem, estrelas e link de cada repositório."""
    soup = BeautifulSoup(html, "html.parser")
    repositorios = []

    # Percorre cada elemento de repositório na lista do GitHub Trending
    for artigo in soup.select("article.Box-row"):
        link_titulo = artigo.select_one("h2 a")
        nome = " ".join(link_titulo.get_text().split()) if link_titulo else "N/A"

        descricao_tag = artigo.select_one("p")
        descricao = descricao_tag.get_text(strip=True) if descricao_tag else ""

        linguagem_tag = artigo.select_one('[itemprop="programmingLanguage"]')
        linguagem = linguagem_tag.get_text(strip=True) if linguagem_tag else "N/A"

        estrelas_tag = artigo.select_one('a[href$="/stargazers"]')
        estrelas = estrelas_tag.get_text(strip=True) if estrelas_tag else "N/A"

        link = "https://github.com" + link_titulo["href"] if link_titulo else "N/A"

        repositorios.append({
            "repositorio": nome,
            "descricao": descricao,
            "linguagem": linguagem,
            "estrelas": estrelas,
            "link": link,
        })

    return repositorios


def exibir_resumo(dados: list[dict], linguagem: str = "python") -> None:
    """Imprime um resumo amigável dos repositórios coletados no terminal."""
    print(f"\n📊 Repositórios {linguagem} em alta no GitHub — {date.today()}\n")
    print(f"{'Repositório':<40} {'Linguagem':<12} {'Estrelas':<10}")
    print("-" * 65)
    for repo in dados:
        print(f"{repo['repositorio'][:38]:<40} {repo['linguagem']:<12} {repo['estrelas']:<10}")
    print(f"\nTotal de repositórios coletados: {len(dados)}")