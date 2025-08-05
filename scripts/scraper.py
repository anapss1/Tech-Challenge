import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

data = []

BASE_URL = "https://books.toscrape.com/catalogue/"


def extrair_livros():
    pagina = 1

    while True:
        url = f"https://books.toscrape.com/catalogue/page-{pagina}.html"

        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        dado_livros = soup.find_all("article", class_="product_pod")

        for article in dado_livros:
            titulo = article.h3.a["title"]
            preco = article.find("p", class_="price_color").text
            rating = article.p["class"][1]
            disponibilidade = article.select_one(".availability").text.strip()
            imagem = "https://books.toscrape.com/" + article.img["src"].replace(
                "../", ""
            )

            # Procurando a categoria
            detalhe_href = article.find("div", class_="image_container").a["href"]
            url_detalhe = BASE_URL + detalhe_href
            detalhe_resp = requests.get(url_detalhe)
            soup_categoria = BeautifulSoup(detalhe_resp.text, "html.parser")
            categoria = soup_categoria.select("ul.breadcrumb li a")[2].text

            data.append(
                {
                    "titulo": titulo,
                    "preco": preco,
                    "rating": rating,
                    "disponibilidade": disponibilidade,
                    "imagem": imagem,
                    "categoria": categoria,
                }
            )

        print(f"{pagina} Concluida")
        pagina += 1


def salvar_csv():
    df = pd.DataFrame(data)
    df.to_csv("data/livros.csv", index=False, encoding="utf-8-sig")
    print("Arquivo CSV salvo em data/livros.csv")


if __name__ == "__main__":
    print(extrair_livros())
    salvar_csv()
