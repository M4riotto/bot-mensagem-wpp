import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

# Carregar a planilha com os dados
dados = pd.read_excel("./leads fulltimeexperience.xlsx")  # Altere para o caminho da sua planilha

# Caminho da imagem que você quer enviar
caminho_imagem = r"C:\xampp\htdocs\bot-mensagem-wpp\img2.jpg"  # Use 'r' para lidar corretamente com caminhos no Windows


# Inicializar o navegador uma vez
navegador = webdriver.Chrome()  # Caminho do driver, se necessário
navegador.get("https://web.whatsapp.com")
input("Faça login no WhatsApp Web e pressione Enter para continuar...")

# Loop para enviar a mensagem e a imagem
for index, row in dados.iterrows():
    nome = row['Nome']
    telefone = row['Telefone']

    # Mensagem personalizada
    # mensagem = f"Olá {nome}%0A%0A✨Gratuito com vagas Limitadas!✨%0A%0AFaça sua inscrição agora e venha participar dessa experiência de conexão, desenvolvimento e expansão de negócios e mentalidade.%0A%0ASaiba mais:%0A🔗 https://fulltimenetworking.com.br/experience/%0A%0AAtt.%0ACássio Moreira%0AFulltime Networking"
    mensagem = f"{nome}%0A%0A🌟 Convite Especial 🌟%0A%0ANo dia 18/06 as 19hs, Empresários e Empreendedores estarão reunidos no 2° Fulltime Networking Experience em Caraguatatuba-SP.%0A%0AUma noite exclusiva de conexões estratégicas, negócios e crescimento.%0A%0AVenha fazer parte desse ambiente.%0A%0A🎯 Vagas limitadas!%0AGaranta a sua participação  gratuita agora mesmo clicando no link abaixo.%0A%0A🔗 https://fulltimenetworking.com.br/experience"


    try:
        # Abrir conversa no WhatsApp Web
        navegador.get(f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem}")
        sleep(5)  # Tempo para o WhatsApp Web carregar a conversa

        # Confirmar o envio da mensagem (pressionando Enter)
        navegador.find_element(By.XPATH, "//span[@data-icon='send']").click()
        sleep(2)

        # 1. Clique no ícone de anexar (mais) para abrir o menu de opções
        anexo = navegador.find_element(By.XPATH, "//span[@data-icon='plus']")
        anexo.click()
        sleep(1)  # Aguarde o menu abrir

    #    # 3. Localizar o campo de upload e enviar a imagem
        input_file = navegador.find_element(By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
        input_file.send_keys(caminho_imagem)
        sleep(2)  # Espera o upload da imagem
        
        # Confirmar o envio da mensagem (pressionando Enter)
        navegador.find_element(By.XPATH, "//span[@data-icon='send']").click()
        sleep(3)

        print(f"Mensagem enviada para {nome} com sucesso!")
        sleep(1)  # Tempo para evitar problemas com o envio contínuo

    except Exception as e:
        print(f"Erro ao enviar mensagem para {nome}: {e}")

# Fechar o navegador ao final
navegador.quit()
