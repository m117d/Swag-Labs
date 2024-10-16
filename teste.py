import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Classe principal que define os testes
class MainTest():
    
    # Inicializa o driver do navegador e configura as opções
    def __init__(self):
        options = Options()
        options.add_argument('--no-sandbox')  # Necessário para evitar problemas com permissões no sandbox
        options.add_argument('--disable-dev-shm-usage')  # Desativa o uso de espaço compartilhado na memória
        options.add_argument('--headless')  # Executa o navegador em modo headless (sem interface gráfica)
        options.add_argument('--start-maximized')  # Inicia o navegador maximizado (mesmo em headless)
        service = Service(ChromeDriverManager().install())  # Instala e gerencia o driver do Chrome automaticamente
        self.driver = webdriver.Chrome(service=service, options=options)  # Inicia o navegador com as opções definidas
        self.tried_usernames = set()  # Conjunto para armazenar usuários já tentados (evita repetir logins)

    # Método principal para execução dos testes
    def main_method(self):
        wait = WebDriverWait(self.driver, 20)  # Tempo de espera explícito até 20 segundos para encontrar elementos

        # Acessa a página inicial do site de login
        self.driver.get("https://www.saucedemo.com/")

        # Obtém a lista de usernames a partir do conteúdo na página
        usernames_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_credentials"]')))
        usernames = usernames_element.text.splitlines()  # Divide o texto em linhas separadas (uma para cada username)

        # Filtra os usernames válidos, removendo linhas desnecessárias
        filtered_usernames = [username for username in usernames if username not in ["Password for all users:", "Accepted usernames are:"]]

        total_users = len(filtered_usernames)  # Número total de usuários válidos
        user_count = 0  # Contador para acompanhar quantos usuários já foram testados

        # Loop para testar o login de cada usuário
        for _ in range(total_users):
            # Seleciona usuários ainda não tentados
            available_usernames = [username for username in filtered_usernames if username not in self.tried_usernames]

            # Se todos os usuários já foram tentados, encerra o loop
            if not available_usernames:
                print("Todos os usuários foram tentados.")
                break

            # Escolhe um usuário aleatoriamente da lista de disponíveis
            selected_username = random.choice(available_usernames)
            self.tried_usernames.add(selected_username)  # Adiciona o usuário à lista de tentados

            user_count += 1  # Incrementa o contador de usuários testados
            print(f"Inserindo o usuário {selected_username} para realizar o login ({user_count} de {total_users})")

            # Obtém a senha (a mesma para todos os usuários)
            password_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]')))
            passwords = password_element.text.splitlines()

            # Filtra a senha correta
            filtered_passwords = [password for password in passwords if password not in ["Password for all users:"]]
            selected_password = filtered_passwords[0]
            print(f"Inserindo a senha do usuário {selected_password}")

            # Insere o username e a senha nos campos de login
            self.driver.find_element(By.XPATH, '//*[@id="user-name"]').send_keys(selected_username)
            self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(selected_password)
            self.driver.find_element(By.XPATH, '//*[@id="login-button"]').click()

            # Aguarda um tempo para que o login seja processado
            time.sleep(3)

            try:
                # Verifica se o login foi bem-sucedido, checando o contêiner de inventário
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="inventory_container"]')))
            except Exception as e:
                # Se houver um erro (usuário bloqueado, por exemplo), exibe a mensagem e tenta outro usuário
                print(f"Usuário {selected_username} está bloqueado.")
                print("Tentando outro usuário.")
                self.driver.get("https://www.saucedemo.com/")  # Retorna à página inicial para tentar outro login
                continue

            print("Verificando títulos")

            try:
                titles = []
                # Recupera os títulos dos produtos disponíveis na página
                for i in range(5):
                    title_xpath = f'//*[@id="item_{i}_title_link"]/div'
                    title_element = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
                    titles.append(title_element.text)

                print(f"Títulos recuperados: {titles}")

                # Prepara os dados para exibição e conversão em JSON
                page_title = self.driver.title
                data = {
                    "username": selected_username,
                    "password": selected_password,
                    "page_title": page_title,
                    "product_titles": titles
                }

                # Exibe os dados no formato JSON
                print(json.dumps(data, indent=4))

            except Exception as e:
                # Se houver erro ao recuperar os títulos, exibe uma mensagem
                print(f"Erro ao recuperar os títulos dos produtos: {e}")

            # Retorna à página inicial após concluir o teste com o usuário atual
            self.driver.get("https://www.saucedemo.com/")
            time.sleep(2)  # Aguarda um tempo antes de iniciar o próximo teste

        print(f"Teste com {total_users} usuários concluídos.")  # Exibe mensagem ao final do teste de todos os usuários

    # Método para fechar o navegador
    def close(self):
        self.driver.quit()

# Ponto de entrada do script
if __name__ == "__main__":
    test = MainTest()  # Instancia a classe principal
    test.main_method()  # Executa o método principal de teste
    test.close()  # Fecha o navegador ao finalizar os testes
