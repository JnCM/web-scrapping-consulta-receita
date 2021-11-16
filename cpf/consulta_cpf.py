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
import json # Para exibir o resultado da consulta
from matplotlib import pyplot as plt # Apenas para abrir o captcha automaticamente
import urllib.request as urllib # Para salvar o captcha da página

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
    URL = "https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublicaSonoro.asp"
    driver.get(URL)

    # Encontrando o campo de CPF
    input_cpf = driver.find_element("id", "txtCPF")
    # Encontrando o campo de data de nascimento
    input_data_nasc = driver.find_element("id", "txtDataNascimento")
    # Encontrando o campo de digitar o captcha
    input_captcha = driver.find_element("id", "txtTexto_captcha_serpro_gov_br")

    # Processo de capturar o captcha da página:

    # Encontrando a imagem na página
    img = driver.find_element("id", "imgCaptcha")
    # Pegando a URL da imagem
    src = img.get_attribute("src")
    # Salvando o captcha
    urllib.urlretrieve(src, "captcha.png")
    # Exibindo o captcha automaticamente
    img_captcha = plt.imread('captcha.png')
    plt.imshow(img_captcha)
    plt.axis('off')
    plt.show(block=False)
    

    # Lendo do terminal o CPF, data de nascimento e o captcha digitados
    cpf = input("Digite o CPF (somente números): ")
    data_nasc = input("Digite a data de nascimento (DD/MM/AAAA): ").replace("/", "")
    captcha = input("Digite os caracteres da imagem exibida: ")

    # Escrevendo na página o CPF, data de nascimento e captcha recebidos via terminal
    driver.execute_script("arguments[0].value='{}';".format(cpf), input_cpf)
    driver.execute_script("arguments[0].value='{}';".format(data_nasc), input_data_nasc)
    driver.execute_script("arguments[0].value='{}';".format(captcha), input_captcha)

    # Realizando o submit do formulário da página da receita
    retorno = driver.find_element("id", "theForm").submit()

    # Processo de retirar as informações do resultado da consulta:

    # Verifica se o resultado da consulta foi uma mensagem de erro
    temp = driver.find_elements("class name", "clConteudoDados")
    #print(driver.page_source)
    if len(temp) == 0:
        print("\nErro na consulta: Dados incorretos.")
    else: # Se não foi uma mensagem de erro, realiza o processo de obtenção dos resultados
        dados = []
        for t in temp:
            element = t.find_element("tag name", "b").text
            dados.append(element)

        # Monta o JSON que será retornado
        final_json = {
            "cpf": dados[0],
            "nome": dados[1],
            "data_nascimento": dados[2],
            "situacao_cadastral": dados[3],
            "data_inscricao": dados[4],
            "digito_verificador": dados[5]
        }

        # Exibe o resultado formatado
        print("\nRESULTADO DA CONSULTA:")
        print(json.dumps(final_json, indent=4, sort_keys=False))

    # Encerra a sessão do selenium
    driver.quit()
except UnexpectedAlertPresentException as e:
    print("\n{}".format(e.alert_text))
except Exception as e:
    print("\nErro interno!")
