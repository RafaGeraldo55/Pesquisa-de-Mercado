import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

 

BASE_URL = "https://lista.mercadolivre.com.br/borracha-geladeira#D[A:borracha%20geladeira]"

# Cabeçalho para simular navegador

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}


def scrape_page(url):

    response = requests.get(url, headers=headers)

    if response.status_code != 200:

        print(f"Erro ao acessar {url}")

        return []

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select(".ui-search-layout__item")

 

    produtos = []

    for item in items:

        titulo = item.select_one(".poly-component__title")

        preco_inteiro = item.select_one(".andes-money-amount__fraction")

        preco_centavos = item.select_one(".andes-money-amount__cents")

 

        if titulo and preco_inteiro:

            preco = preco_inteiro.get_text()

            if preco_centavos:

                preco += "," + preco_centavos.get_text()

            produtos.append({

                "titulo": titulo.get_text().strip(),

                "preco": preco

            })

    return produtos

 

# Loop de paginação

all_produtos = []

offset = 1

while True:

    url = BASE_URL.format(offset=offset)

    print(f"Coletando: {url}")

    produtos = scrape_page(url)

 

    if not produtos:

        print("Sem mais resultados.")

        break

 

    all_produtos.extend(produtos)

    offset += 50
    
    time.sleep(2) # respeitar servidor

 

# Salva em CSV

if all_produtos:

    df = pd.DataFrame(all_produtos)

    df.to_csv("mercadolivre_borracha_geladeira.csv", index=False, encoding="utf-8-sig")

    print("Arquivo CSV salvo: mercadolivre_borracha_geladeira.csv")

else:

    print("Nenhum produto encontrado.")