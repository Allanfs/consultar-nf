from bs4 import BeautifulSoup
import json

# Carregar o HTML do arquivo
with open("./nf2.html", "r", encoding="ISO-8859-1") as file:
    soup = BeautifulSoup(file, "html.parser")

# Encontrar a tabela de produtos
prod_table = soup.find("div", {"id": "prod"}).find("table")
children = list(prod_table.children)

produto = ""
preco_unitario = 0.0
desconto = 0.0
qtd_prod = 0.0
for x in range(len(children)):
    if not children[x].name: continue

    # se for uma tr detalhe de produto
    if children[x].find("div") and children[x].find("div")["id"].startswith("prod"): 
        
        preco_desconto_str = children[x].find("div").find_all("tr")[2].find("input", {"name": "edtCodProd"})["value"]
        if preco_desconto_str.strip(): 
            desconto = float(preco_desconto_str.replace(".", "").replace(",", "."))

        preco_unitario_str = children[x].find("div").find_all("tr")[3].find("input", {"name": "edtvlUniCom"})["value"]
        if preco_unitario_str.strip(): 
            preco_unitario = float(preco_unitario_str.replace(".", "").replace(",", "."))

    else:
        inputs = children[x].find("input", {"name":"edtDescProd"})
        if inputs: 
            produto = inputs['value']
            # print("produto:", produto, end=" ")
        qtd_prod_str = children[x].find("input", {"name":"edtQtdProd"})
        if qtd_prod_str and qtd_prod_str['value'].strip(): 
            qtd_prod = float(qtd_prod_str['value'].replace(".", "").replace(",", "."))
    if preco_unitario > 0.0:
        print(f"{qtd_prod}x ({produto})", end=" ")
        print("por", preco_unitario - (desconto/qtd_prod))
    
    preco_unitario = 0.0
    desconto = 0.0
    
