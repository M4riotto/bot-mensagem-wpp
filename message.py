import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

# Carregar a planilha com os dados
dados = pd.read_excel("./teste.xlsx")  # Altere para o caminho da sua planilha

# Caminho da imagem que você quer enviar
caminho_imagem = r"C:\Users\vitor\Downloads\imagem-teste.png"  # Use 'r' para lidar corretamente com caminhos no Windows

# Inicializar o navegador uma vez
navegador = webdriver.Chrome()  # Caminho do driver, se necessário
navegador.get("https://web.whatsapp.com")
input("Faça login no WhatsApp Web e pressione Enter para continuar...")

# Loop para enviar a mensagem e a imagem
for index, row in dados.iterrows():
    nome = row['Nome']
    telefone = row['Telefone']

    # Mensagem personalizada
    mensagem = f"Olá {nome}, esta é uma mensagem automática com uma imagem."

    try:
        # Abrir conversa no WhatsApp Web
        navegador.get(f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem}")
        sleep(5)  # Tempo para o WhatsApp Web carregar a conversa

        # Confirmar o envio da mensagem (pressionando Enter)
        navegador.find_element(By.XPATH, "//span[@data-icon='send']").click()
        sleep(1)

        # 1. Clique no ícone de anexar (mais) para abrir o menu de opções
        anexo = navegador.find_element(By.XPATH, "//span[@data-icon='plus']")
        anexo.click()
        sleep(1)  # Aguarde o menu abrir

        # # 2. Selecionar o botão de fotos e vídeos
        # botao_fotos = navegador.find_element(By.XPATH, "//li[@data-animate-dropdown-item='true']//span[text()='Fotos e vídeos']")
        # botao_fotos.click()
        # sleep(2)  # Espera o seletor de arquivos abrir

       # 3. Localizar o campo de upload e enviar a imagem
        input_file = navegador.find_element(By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
        input_file.send_keys(caminho_imagem)
        sleep(2)  # Espera o upload da imagem

        # Adicionar legenda na imagem (se necessário)
        # legenda = navegador.find_element(By.XPATH, "//div[@data-testid='media-caption-text']")
        # legenda.send_keys(mensagem)
        # sleep(1)

        # Confirmar o envio da mensagem (pressionando Enter)
        navegador.find_element(By.XPATH, "//span[@data-icon='send']").click()
        sleep(3)

        print(f"Mensagem enviada para {nome} com sucesso!")
        sleep(1)  # Tempo para evitar problemas com o envio contínuo

    except Exception as e:
        print(f"Erro ao enviar mensagem para {nome}: {e}")

# Fechar o navegador ao final
navegador.quit()
