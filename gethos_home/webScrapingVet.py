# FUNÇÃO PARA PEGAR DADOS DO SIMPLES VET DO CLIENTE

import requests
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
from schedule import repeat, every
import json
import re
import time
import os
from .models import Contato
from datetime import datetime



caminho_chromedriver = r'C:\Users\hostilio.neto\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
servico = Service(caminho_chromedriver)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Ativar o modo headless
chrome_options.add_argument("--disable-gpu")  # Opcional, pode melhorar performance
chrome_options.add_argument("--window-size=1920x1080")  # Definir tamanho da janela virtual (importante para layouts)
chrome_options.add_argument("--no-sandbox")  # Boa prática em alguns ambientes (ex: servidores Linux)
chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas com memória compartilhada em alguns sistemas
chrome_options.add_experimental_option("detach", True)

# navegador = webdriver.Chrome(service=servico, options=chrome_options)
# servico = Service(ChromeDriverManager().install())


def realizar_login():
    try:
        linkAcesso = "https://app.simples.vet/login/login.php"
        navegador = webdriver.Chrome(service=servico, options=chrome_options)
        navegador.get(linkAcesso)
        print('Automação Gethos Software sendo iniciada...')
        
        print("Automação Gethos Software sendo iniciada...")
        navegador.implicitly_wait(2)
        #  realiza o login
        insereEmail = navegador.find_element(by=By.ID, value="l_usu_var_email")
        insereEmail.send_keys("hostilio.neto@cesmac.edu.br")
        print('Preenchendo e-mail: hostilio.neto@cesmac.edu.br')
        navegador.implicitly_wait(1)
        print('E-mail validado com sucesso!')
        insereSenha = navegador.find_element(by=By.ID, value="l_usu_var_senha")
        print('Preenchendo senha: ********')
        insereSenha.send_keys("Neto03@@")
        print('Senha validada com sucesso!')

        # Clicar no botão de login
        navegador.find_element(By.CSS_SELECTOR, "button").click()
        print("Login realizado com sucesso!")

        # Retorne o navegador para continuar a extração de dados
        return navegador
    
    except Exception as e:
        print(f"Erro ao realizar o login: {e}")
        return None
    

def buscar_dados():
    navegador = realizar_login()
    if not navegador:
        return {"erro": "Não foi possível realizar o login."}

    try:
        navegador.find_element(By.XPATH, "/html/body/div[3]/div[1]/ul/li[3]").click()
        time.sleep(2)
        navegador.find_element(By.XPATH, "/html/body/div[3]/div[1]/ul/li[3]/ul/li[1]/a").click()
        time.sleep(5)
        # acessar_agenda = navegador.find_element(By.XPATH, "/html/body/div[3]/div[1]/ul/li[3]/ul/li[1]/a").click()
        # time.sleep(5)
        navegador.find_element(By.XPATH, '//*[@id="proximo"]').click() # avançar agenda 1 click
        time.sleep(1)
        navegador.find_element(By.XPATH, '//*[@id="proximo"]').click() # avançar agenda 1 click
        time.sleep(1)
        navegador.find_element(By.XPATH, '//*[@id="proximo"]').click() # avançar agenda 1 click
        time.sleep(1)
        navegador.find_element(By.XPATH, '//*[@id="proximo"]').click() # avançar agenda 1 click
        time.sleep(1)


                # Buscar todos os elementos com a classe 'event-content'
        eventos = navegador.find_elements(By.CLASS_NAME, 'event-content')
        
        titulos = []
        agendamentos = []
        # Lista para armazenar os títulos
        
        # Iterar pelos elementos encontrados e buscar os títulos
        for evento in eventos:
            try:
                # Encontrar o título dentro do elemento (ajuste 'event-title' se necessário)
                titulo_element = evento.find_element(By.CLASS_NAME, 'event-title')
                titulo = titulo_element.text.strip()  # Capturar o texto do título e remover espaços extras
                titulos.append(titulo)  # Adicionar o título à lista
            except Exception as e:
                print(f"Erro ao buscar título em um elemento: {e}")
        
        # Exibir os títulos encontrados
        print("Títulos encontrados:")
        print(titulos)
        print("\n\n")
        
        # Iterar pelos elementos encontrados
        for evento in eventos:
            try:
                # Encontrar o título dentro do elemento
                titulo_element = evento.find_element(By.CLASS_NAME, 'event-title')
                titulo = titulo_element.text.strip()  # Capturar o texto do título
                # print(f"Clicando no evento com título: {titulo}")
        
                # Clicar no elemento
                evento.click()
        
                # Esperar o menu ou os dados carregarem
                WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="btn_fechar"]'))
                )
                time.sleep(2)  # Ajuste conforme necessário
        
                # Capturar os dados após o clique
                try:
                    # Captar a data do evento
                    evento_data = WebDriverWait(navegador, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="date-header"]'))
                    ).text
        
                    # Captar o status do agendamento
                    status_agendamento = navegador.find_element(By.XPATH, '//*[@id="status-content"]/div').text
        
                    # Captar o nome do cliente e o ID
                    cliente_nome = navegador.find_element(By.XPATH, '//*[@id="btn_editarcliente"]/div[1]/h4[1]').text.strip()
        
                    # Captar o nome do animal, raça e cor
                    animal_info = navegador.find_element(By.XPATH, '//*[@id="btn_editarcliente"]/div[1]/h4[2]').text.strip()
        
                    # Captar o telefone do cliente
                    telefone = navegador.find_element(By.XPATH, '//*[@id="btn_editarcliente"]/div[1]/h4[3]').text.strip()
        
                    # Captar o responsável pelo atendimento
                    responsavel = navegador.find_element(By.XPATH, '//*[@id="appointment-content"]/div/div/h4[2]').text.strip()
        
                    # Captar o tipo de atendimento
                    tipo_atendimento = navegador.find_element(By.XPATH, '//*[@id="appointment-content"]/div/div/h4[1]').text.strip()
        
        
                    # Captar observação do atendimento, se existir
                    try:
                        obs_atendimento = navegador.find_element(By.XPATH, '//*[@id="appointment-content"]/div/div/h4[3]').text.strip()
                    except Exception:
                        obs_atendimento = "Sem observação"  # Valor padrão caso o elemento não exista
                            
        
                    # Remover o texto entre parênteses (como "(2501)") no nome do cliente
                    cliente_nome_limpo = re.sub(r"\(\d+\)", "", cliente_nome).strip()
        
        
                    # Construir o objeto com as informações capturadas
                    agendamento = {
                        'nomeCliente': cliente_nome_limpo,
                        'numeroCliente': telefone,
                        'nomeAnimal': animal_info.split(" ")[0],
                        'nomeVet': responsavel,
                        'statusAgendamento': status_agendamento,
                        'dataConsulta': evento_data.split(" às ")[0],
                        'horaConsulta': evento_data.split(" às ")[1],
                        'tipoatendimento': tipo_atendimento,
                        'obsAtendimento': obs_atendimento,
                    }
        
                    # Exibir o objeto no console
                    
                    # print(f"{agendamento},")
                    # Imprimir o dicionário formatado
                    print(json.dumps(agendamento, indent=4, ensure_ascii=False))
        
                except Exception as e:
                    # print(f"Erro ao capturar os dados do evento '{titulo}': {e}")
                    print(f" ")
        
        
                # Fechar o menu lateral (se necessário)
                fechar_menu_lateral = navegador.find_element(By.XPATH, '//*[@id="btn_fechar"]').click()
                time.sleep(2)
        
            except Exception as e:
                print(f"Erro ao clicar no elemento com título '{titulo}': {e}")
        
    # Fechar navegador
        # navegador.quit()

        # Salvar os dados no banco
        for agendamento in agendamentos:
            salvar_dados_no_banco(agendamentos)
        
        print('Todos os agendamentos foram processados e salvos no banco de dados.')
        navegador.quit()

        return agendamentos


    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        navegador.quit()
        return {"erro": str(e)}

    # except Exception as e:
    #     print(f"Erro ao buscar dados: {e}")
    #     navegador.quit()
    #     return {"erro": str(e)}
    


# buscar_dados()


def salvar_dados_no_banco(agendamento):
    """
    Função para salvar os dados no banco de dados.
    :param dados: lista de dicionários com os dados raspados
    """
    try:
        contato = Contato(
            nome=agendamento['nomeCliente'],
            telefone=agendamento['numeroCliente'],
            nomeAnimal=agendamento['nomeAnimal'],
            nomeVet=agendamento['nomeVet'],
            status=agendamento['statusAgendamento'],
            dataConsulta=agendamento['dataConsulta'],
            horaConsulta=agendamento['horaConsulta'],
            tipoAtendimento=agendamento['tipoatendimento'],
            obsAtendimento=agendamento['obsAtendimento'],
        )
        contato.save()
        print(f"Contato {agendamento['nomeCliente']} salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o contato {agendamento['nomeCliente']}: {e}")