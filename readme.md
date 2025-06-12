```sh
JSESSIONID=$(./nf-session.sh)
echo -n "Informe chave de acesso NFCe: " ; read -r NFCE
./nf-consultar.sh $JSESSIONID $NFCE
```