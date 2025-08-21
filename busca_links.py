# -*- coding: utf-8 -*-
"""
Busca links de compra de forma confiável usando a Google Custom Search JSON API.

Pré-requisitos:
- Crie um projeto no Google Cloud e habilite a "Custom Search API".
- Crie um mecanismo de pesquisa personalizado (CSE) e anote o ID (CSE_ID).
- Defina as variáveis de ambiente GOOGLE_API_KEY e CSE_ID:
    export GOOGLE_API_KEY="SUA_CHAVE"
    export CSE_ID="SEU_CSE_ID"

Uso:
    python busca_links.py "Notebook i7 16GB 512GB site:amazon.com.br"
    python busca_links.py --arquivo consultas.txt
"""
import os
import sys
import json
import argparse
import requests

API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("CSE_ID")

def buscar(query, num=5):
    if not API_KEY or not CSE_ID:
        raise RuntimeError("Defina GOOGLE_API_KEY e CSE_ID nas variáveis de ambiente.")
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num,
        "safe": "active",
        "hl": "pt-BR"
    }
    resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    resultados = []
    for item in data.get("items", []):
        resultados.append({
            "titulo": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })
    return resultados

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", help="Consulta a ser buscada")
    parser.add_argument("--arquivo", help="Arquivo com uma consulta por linha")
    parser.add_argument("--num", type=int, default=5, help="Número de resultados por consulta")
    args = parser.parse_args()

    consultas = []
    if args.arquivo:
        with open(args.arquivo, "r", encoding="utf-8") as f:
            consultas = [l.strip() for l in f if l.strip()]
    elif args.query:
        consultas = [args.query]
    else:
        parser.error("Forneça uma 'query' ou '--arquivo'.")

    saida = []
    for q in consultas:
        try:
            resultados = buscar(q, num=args.num)
            saida.append({"consulta": q, "resultados": resultados})
        except Exception as e:
            saida.append({"consulta": q, "erro": str(e), "resultados": []})

    print(json.dumps(saida, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
