'''
ATENÇÃO(!): Este código utiliza como navegador o Microsoft Edge, para outros navegadores
            consultar: https://www.selenium.dev/selenium/docs/api/py/
'''

# Importação dos módulos necessários para a consulta
from selenium import webdriver # Necessário para inicializar o browser
from selenium.webdriver.edge.service import Service # Mudar "edge" para o navegador em uso
from selenium.webdriver.edge.options import Options # Mudar "edge" para o navegador em uso
# Exceção quando a página exibe um alerta
from selenium.common.exceptions import UnexpectedAlertPresentException
import cv2 as cv # Para cortar o print da página
import json # Para exibir o resultado da consulta
from matplotlib import pyplot as plt # Apenas para abrir o captcha automaticamente

try:
    # Caminho do driver do navegador utilizado (MUDAR PARA O DRIVER QUE FOR UTILIZAR)
    PATH_TO_DRIVER = "C:/edge_driver/msedgedriver.exe"
    serv = Service(PATH_TO_DRIVER)

    # Definindo as opções de utilização do selenium
    options = Options()
    # Desabilitando as mensagens do selenium no terminal (apenas erros serão exibidos)
    options.add_argument("--log-level=3")
    # Desabilitando a abertura automática de uma janela do navegador com a página da receita
    options.add_argument("--headless")

    # Inicializando o selenium (MUDAR PARA O NAVEGADOR QUE FOR UTILIZAR)
    driver = webdriver.Edge(service=serv, service_log_path="NUL", options=options)

    # Fazendo o GET da página da receita
    URL = "http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/Cnpjreva_Solicitacao_CS.asp"
    driver.get(URL)

    # Encontrando o campo de CNPJ
    input_cnpj = driver.find_element("id", "cnpj")
    # Encontrando o campo de digitar o captcha
    input_captcha = driver.find_element("id", "txtTexto_captcha_serpro_gov_br")

    # Processo de capturar o captcha da página:

    # Salvando o print da página
    driver.save_screenshot("screenshot.png")
    # Encontrando a imagem na página
    img = driver.find_element("id", "imgCaptcha")
    # Armazenando as coordenadas (x,y) do captcha na tela
    loc = img.location
    # Realizando o processo de cortar a imagem do print
    image = cv.imread('screenshot.png')
    desloc_x = 185
    desloc_y = 55
    cropped_image = image[loc['y']:loc['y']+desloc_y, loc['x']:loc['x']+desloc_x]
    cv.imwrite('captcha.png', cropped_image)
    # Exibindo o captcha automaticamente
    img_captcha = cv.imread('captcha.png')
    plt.imshow(img_captcha)
    plt.xticks([])
    plt.yticks([])
    plt.show(block=False)

    # Lendo do terminal o CNPJ e o captcha digitados
    cnpj = input("Digite o CNPJ (somente números): ")
    captcha = input("Digite os caracteres da imagem exibida: ")

    # Escrevendo na página o CNPJ e captcha recebidos via terminal
    driver.execute_script("arguments[0].value='{}';".format(cnpj), input_cnpj)
    driver.execute_script("arguments[0].value='{}';".format(captcha), input_captcha)

    # Realizando o submit do formulário da página da receita
    retorno = driver.find_element("id", "frmConsulta").submit()

    # Processo de retirar as informações do resultado da consulta:

    # Verifica se o resultado da consulta foi uma mensagem de erro
    temp = driver.find_elements("tag name", "b")
    verifica = []
    for t in temp:
        verifica.append(t.text)
    if len(verifica) == 1:
        print("\n{}: Captcha inválido".format(verifica[0]))
    else: # Se não foi uma mensagem de erro, realiza o processo de obtenção dos resultados
        linha = driver.find_elements("tag name", "font")
        for i in range(len(linha)):
            if linha[i].text == "NÚMERO DE INSCRIÇÃO":
                insc = linha[i+1].find_elements("tag name", "b")
                final_cnpj = insc[0].text
                tipo_empresa = insc[1].text
            elif linha[i].text == "DATA DE ABERTURA":
                data_abertura = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "NOME EMPRESARIAL":
                nome_empresarial = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "TÍTULO DO ESTABELECIMENTO (NOME DE FANTASIA)":
                nome_fantasia = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "LOGRADOURO":
                logradouro = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "NÚMERO":
                numero = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "COMPLEMENTO":
                complemento = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "CEP":
                cep = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "BAIRRO/DISTRITO":
                bairro = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "MUNICÍPIO":
                municipio = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "UF":
                estado = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "ENDEREÇO ELETRÔNICO":
                email = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "TELEFONE":
                telefone = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "SITUAÇÃO CADASTRAL":
                situacao_cadastral = linha[i+1].find_element("tag name", "b").text
            elif linha[i].text == "DATA DA SITUAÇÃO CADASTRAL":
                data_situacao_cadastral = linha[i+1].find_element("tag name", "b").text

        # Monta o JSON que será retornado
        final_json = {
            "cnpj": final_cnpj,
            "tipo_empresa": tipo_empresa,
            "data_abertura": data_abertura,
            "nome_empresarial": nome_empresarial,
            "nome_fantasia": nome_fantasia,
            "endereco": {
                "logradouro": logradouro,
                "numero": numero,
                "complemento": complemento,
                "cep": cep,
                "bairro": bairro,
                "municipio": municipio,
                "estado": estado
            },
            "email": email,
            "telefone": telefone,
            "situacao_cadastral": situacao_cadastral,
            "data_situacao_cadastral": data_situacao_cadastral
        }

        # Exibe o resultado formatado
        print("\nRESULTADO DA CONSULTA:")
        print(json.dumps(final_json, indent=4, sort_keys=False))

    # Encerra a sessão do selenium
    driver.quit()
except UnexpectedAlertPresentException as e:
    print("\n{}".format(e.alert_text))
except:
    print("\nErro interno!")
