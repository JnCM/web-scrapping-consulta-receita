# Consulta de CPF e CNPJ na Receita Federal com Web-Scraping
Repositório contendo scripts Python que realizam a consulta de CPF e CNPJ diretamente no site da Receita Federal.

## Requerimentos
* Python 3.x instalado;
* Driver do navegador que será utilizado. Clique [aqui](https://www.selenium.dev/selenium/docs/api/py/#drivers) para mais informações;
* Caminho do driver baixado adicionado ao PATH.

## Instalação
Na pasta do repositório, execute o comando:
```bash
pip install -r requirements.txt
```

## Alterações necessárias
Para a execução, é necessário adaptar o código para o navegador que será utilizado. Por padrão o código utiliza o navegador Microsoft Edge. Modificar se necessário:

* Importações dos módulos. Mudar `edge` para o navegador que será usado:
```python
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
```

* Caminho do driver baixado:
```python
PATH_TO_DRIVER = "C:/edge_driver/msedgedriver.exe"
```

* Inicialização do webdriver. Mudar `Edge` para o navegador que será usado:
```python
driver = webdriver.Edge(service=serv, service_log_path="NUL", options=options)
```

## Consulta de CNPJ - Exemplo
Na pasta do repositório, execute o comando:
```bash
python cnpj/consulta_cnpj.py
```

Digite os campos necessários:
```bash
Digite o CNPJ (somente números): 06990590000395
Digite os caracteres da imagem exibida: ZaQO5z
```

Com os dados inseridos corretamente, a consulta exibirá um JSON de retorno:
```json
{
    "cnpj": "06.990.590/0003-95",
    "tipo_empresa": "FILIAL",
    "data_abertura": "11/01/2008",
    "nome_empresarial": "GOOGLE BRASIL INTERNET LTDA.",
    "nome_fantasia": "********",
    "endereco": {
        "logradouro": "AV DOS ANDRADAS",
        "numero": "3000",
        "complemento": "ANDAR 5 14 15 16 17 EDIF BOULEVARD CORPORATE",
        "cep": "30.260-070",
        "bairro": "SANTA EFIGENIA",
        "municipio": "BELO HORIZONTE",
        "estado": "MG"
    },
    "email": "GOOGLEBRASILCONTATOCNPJ@GOOGLE.COM",
    "telefone": "(11) 2395-8400",
    "situacao_cadastral": "ATIVA",
    "data_situacao_cadastral": "11/01/2008"
}
```

## Consulta de CPF - Exemplo
Na pasta do repositório, execute o comando:
```bash
python cpf/consulta_cpf.py
```

Digite os campos necessários:
```bash
Digite o CPF (somente números): 12345678901
Digite a data de nascimento (DD/MM/AAAA): 25/12/2000
Digite os caracteres da imagem exibida: 9XETCm
```

Com os dados inseridos corretamente, a consulta exibirá um JSON de retorno:
```json
{
    "cpf": "123.456.789-01",
    "nome": "FULANO BELTRANO CICLANO",
    "data_nascimento": "25/12/2000",
    "situacao_cadastral": "REGULAR",
    "data_inscricao": "12/04/2006",
    "digito_verificador": "00"
}
```
