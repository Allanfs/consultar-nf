from dataclasses import dataclass
import sys
from typing import List

from bs4 import BeautifulSoup

DEFAULT_HTML_PATH = "./nf2.html"
HTML_ENCODING = "ISO-8859-1"

FIELD_DESC = "edtDescProd"
FIELD_QTD = "edtQtdProd"
FIELD_DESCONTO = "edtCodProd"
FIELD_PRECO_UNIT = "edtvlUniCom"
FIELD_UNIDADE = "edtUnidTrib"


@dataclass
class ItemNF:
    descricao: str
    unidade: str
    quantidade: float
    preco_unitario: float
    desconto: float
    preco_unitario_liquido: float


def load_html(path: str) -> BeautifulSoup:
    """Carrega o HTML da NF e retorna o objeto BeautifulSoup."""
    try:
        with open(path, "r", encoding=HTML_ENCODING) as file:
            return BeautifulSoup(file, "html.parser")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Arquivo não encontrado: {path}") from exc
    except OSError as exc:
        raise OSError(f"Não foi possível ler o arquivo: {path}") from exc


def parse_decimal_br(value: str) -> float:
    """Converte número no formato brasileiro para float."""
    if not value:
        return 0.0

    normalized = value.strip().replace(".", "").replace(",", ".")
    if not normalized:
        return 0.0

    try:
        return float(normalized)
    except ValueError:
        return 0.0


def get_input_value(node, field_name: str) -> str:
    """Obtém o valor de um input por name; retorna string vazia se ausente."""
    if node is None:
        return ""

    input_node = node.find("input", {"name": field_name})
    if input_node is None:
        return ""
    return input_node.get("value", "")


def extract_detail_fields(detail_div) -> dict[str, str]:
    """Extrai pares label/valor da tabela de detalhe de um produto."""
    if detail_div is None:
        return {}

    table = detail_div.find("table")
    if table is None:
        return {}

    fields: dict[str, str] = {}

    for tr in table.find_all("tr"):
        for td in tr.find_all("td"):
            label_node = td.find("b")
            input_node = td.find("input")
            if label_node is None or input_node is None:
                continue

            label = label_node.get_text(" ", strip=True)
            if not label:
                continue

            fields[label] = input_node.get("value", "").strip()

    return fields


def compute_unit_price(preco_unitario: float, desconto: float, qtd: float) -> float:
    """Calcula preço unitário líquido com proteção para quantidade zero."""
    if qtd <= 0:
        return preco_unitario
    return preco_unitario - (desconto / qtd)


def extract_items(soup: BeautifulSoup) -> List[ItemNF]:
    """Extrai itens da seção de produtos da NFC-e."""
    prod_div = soup.find("div", {"id": "prod"})
    if prod_div is None:
        raise ValueError("HTML inválido: seção de produtos (div#prod) não encontrada.")

    prod_table = prod_div.find("table")
    if prod_table is None:
        raise ValueError("HTML inválido: tabela de produtos não encontrada.")

    items: List[ItemNF] = []
    produto = ""
    qtd_prod = 0.0
    unidade = ""

    for row in prod_table.find_all("tr", recursive=False):
        detail_div = row.find("div", id=lambda value: bool(value and value.startswith("prod")))
        if detail_div is None:
            desc = get_input_value(row, FIELD_DESC)
            if desc:
                produto = desc

            qtd = parse_decimal_br(get_input_value(row, FIELD_QTD))
            if qtd > 0:
                qtd_prod = qtd
            
            und = get_input_value(row, FIELD_UNIDADE)
            if und:
                unidade = und

            continue

        detail_fields = extract_detail_fields(detail_div)
        desconto = parse_decimal_br(detail_fields.get("Valor de Desconto", ""))
        preco_unitario = parse_decimal_br(detail_fields.get("Valor unitário de comercialização", ""))

        if preco_unitario == 0.0:
            continue

        preco_liquido = compute_unit_price(preco_unitario, desconto, qtd_prod)
        items.append(
            ItemNF(
                descricao=produto,
                unidade=unidade,
                quantidade=qtd_prod,
                preco_unitario=preco_unitario,
                desconto=desconto,
                preco_unitario_liquido=preco_liquido,
            )
        )

    return items


def main() -> int:
    """Executa parsing do arquivo de NF e imprime os itens encontrados."""
    try:
        soup = load_html(DEFAULT_HTML_PATH)
        items = extract_items(soup)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    for item in items:
        print(f"{item.quantidade} {item.unidade} de ({item.descricao}) por {item.preco_unitario_liquido}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
