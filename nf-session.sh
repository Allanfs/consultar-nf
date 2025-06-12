#!/bin/bash

# Defina a URL para a requisição
URL="https://www4.sefaz.pb.gov.br/atf/seg/SEGf_AcessarFuncao.jsp?cdFuncao=FIS_1410&chNFe="

# Arquivo temporário para armazenar os cookies
COOKIE_FILE="cookies.txt"

# Fazer a requisição e salvar os cookies
curl -c $COOKIE_FILE -s $URL > /dev/null

# Extrair o valor do JSESSIONID do arquivo de cookies
JSESSIONID=$(grep 'JSESSIONID' $COOKIE_FILE | awk '{print $NF}')

# Exibir o valor do JSESSIONID
echo $JSESSIONID

# Remover o arquivo temporário de cookies
rm -f $COOKIE_FILE