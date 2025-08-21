import requests
from bs4 import BeautifulSoup

# lista de itens que queremos buscar
itens = [
    "Notebook i7 16GB SSD 512GB site:amazon.com.br",
    "Seguro notebook educacional site:porto.com.br",
    "Sistema de rastreamento notebook site:mercadolivre.com.br",
    "Bolsa case notebook 15.6 site:magazineluiza.com.br",
    "Roteador Wi-Fi 6 site:kabum.com.br"
]

# cabeçalho para simular navegador
headers = {"User-Agent": "Mozilla/5.0"}

def buscar_links(query):
    url = f"https://www.google.com/search?q={query}&hl=pt-BR"
    resposta = requests.get(url, headers=headers)
    sopa = BeautifulSoup(resposta.text, "html.parser")
    
    links = []
    for a in sopa.select("a"):
        href = a.get("href")
        if href and "http" in href and "google" not in href:
            links.append(href)
    return links[:5]  # retorna só os 5 primeiros links "bons"

# executar para cada item
for item in itens:
    print(f"\n🔎 Resultados para: {item}")
    for link in buscar_links(item):
        print("➡", link)
