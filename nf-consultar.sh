#!/bin/bash

# Verifica se os parâmetros foram passados
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <JSESSIONID> <Número da NF>"
    exit 1
fi

# Atribui os parâmetros às variáveis
JID="$1"
NF="$2"

# Executa o comando curl com os parâmetros informados
curl -X POST 'https://www4.sefaz.pb.gov.br/atf/fis/FISf_ExibirNFCE.do' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H "Cookie: JSESSIONID=$JID; _ga_94F98Z50C5=GS1.1.1729530279.1.1.1729530447.0.0.0" \
  --data-raw "edtID=$NF&hidAcao=consultar&hidHistorico=-1" > nf2.html

echo "NF salva em nf2.html"
