from bs4 import BeautifulSoup
import json

# Carregar o HTML do arquivo
with open("./nf2.html", "r", encoding="ISO-8859-1") as file:
    soup = BeautifulSoup(file, "html.parser")

# Encontrar a tabela de produtos
prod_table = soup.find("div", {"id": "prod"}).find("table")

# Lista para armazenar os produtos
produtos = []

# Encontrar todas as linhas que contêm produtos
rows = prod_table.find_all("tr")[2:]  # Ignorar cabeçalhos

for row in rows:
    inputs = row.find_all("input")

    # Garantir que a linha tem campos necessários
    if len(inputs) >= 3:
        nome = inputs[1]["value"]
        quantidade = inputs[2]["value"]
        valor_unitario = inputs[-1]["value"]  # Último input na linha principal

        # Converter valores para os formatos corretos
        quantidade = quantidade#float(quantidade.replace(",", "."))
        valor_unitario = valor_unitario#float(valor_unitario.replace(",", "."))

        produtos.append({
            "nome": nome,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario
        })

# Converter para JSON
json_result = json.dumps(produtos, indent=4, ensure_ascii=False)

# Exibir o resultado
print(json_result)
