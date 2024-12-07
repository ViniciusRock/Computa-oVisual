import cv2
import pytesseract
import numpy as np
import os
import glob

# Caminho para o executável do tesseract (alterar conforme necessário no Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Vinicius\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Caminho no Windows

# Função para imprimir mensagem amarela no console
def print_yellow_message(message):
    print(f"\033[93m{message}\033[0m")  # Código ANSI para cor amarela

# Função para encontrar e circundar o texto específico na imagem com quadrados
def find_and_square_text(image_path, target_text):
    # Carregar a imagem
    img = cv2.imread(image_path)

    # Verificar se a imagem foi carregada corretamente
    if img is None:
        print(f"Erro ao carregar a imagem {image_path}")
        return False  # Retorna False se não encontrar a imagem

    # Se a imagem for muito pequena, aumentá-la para melhorar a detecção
    height, width = img.shape[:2]
    if height < 500 or width < 500:
        img = cv2.resize(img, (width * 2, height * 2))  # Aumenta a imagem para o dobro do tamanho

    # Usar pytesseract para realizar OCR e extrair as caixas de texto
    custom_oem_psm_config = r'--oem 3 --psm 6'  # Oem = 3 (usa LSTM OCR) e PSM = 6 (mode 6 para OCR em imagens)
    details = pytesseract.image_to_data(img, config=custom_oem_psm_config, lang='por', output_type=pytesseract.Output.DICT)

    # Iterar pelas palavras e procurar o texto alvo
    num_boxes = len(details['text'])
    found = False  # Variável para verificar se encontramos a palavra

    for i in range(num_boxes):
        word = details['text'][i].strip()
        
        # Se encontrar o texto alvo, desenha um quadrado em volta dele
        if target_text.lower() in word.lower():  # Busca sem distinguir maiúsculas/minúsculas
            (x, y, w, h) = (details['left'][i], details['top'][i], details['width'][i], details['height'][i])
            
            # Desenhar um quadrado ao redor do texto
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Cor verde e espessura 2

            # Opcional: Adicionar um rótulo no quadrado (o texto encontrado)
            cv2.putText(img, word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            found = True  # Marcamos como encontrado
    
    # Se encontrou o texto, exibe a imagem com o quadrado
    if found:
        # Exibir mensagem no console com cor amarela
        print_yellow_message("Texto encontrado!\nClique na foto e pressione qualquer tecla para continuar a pesquisa")
        
        # Criar uma janela para exibir a imagem no centro da tela
        window_name = f"Resultado da Detecção - {target_text}"

        # Obter a largura e altura da tela (depende do sistema operacional)
        screen_res = 1920, 1080  # Ajuste conforme a resolução do seu monitor
        screen_width, screen_height = screen_res

        # Calcular a posição para centralizar a imagem
        window_x = int((screen_width - img.shape[1]) / 2)
        window_y = int((screen_height - img.shape[0]) / 2)

        # Criar janela em cima de todas as outras
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(window_name, window_x, window_y)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)  # A janela ficará no topo

        # Mostrar a imagem
        cv2.imshow(window_name, img)
        cv2.waitKey(0)  # Aguarda o pressionamento de qualquer tecla
        cv2.destroyAllWindows()

    return found  # Retorna True se encontrou o texto, False caso contrário

# Função para processar todas as imagens em um diretório
def process_images_in_directory(directory, target_texts):
    # Usando glob para pegar arquivos .jpg, .png e .webp no diretório
    image_paths = glob.glob(os.path.join(directory, '*.jpg')) + \
                  glob.glob(os.path.join(directory, '*.png')) + \
                  glob.glob(os.path.join(directory, '*.webp')) + \
                  glob.glob(os.path.join(directory, '*.jpeg'))

    # Processar cada imagem no diretório
    for image_path in image_paths:
        print(f"\nAnalisando a imagem: {image_path}")
        
        for target_text in target_texts:
            print(f"Procurando por: {target_text}")
            
            # Se encontrar o texto na imagem, exibe a imagem com o quadrado
            found = find_and_square_text(image_path, target_text)
            
            if found:
                # Espera o usuário pressionar qualquer tecla para passar para a próxima imagem
                print(f"Texto encontrado na imagem {image_path}. Pressione qualquer tecla para continuar...")
                cv2.waitKey(0)  # Espera pressionar qualquer tecla
                break  # Se encontrar o texto, não precisa continuar buscando nessa imagem

# Função principal
if __name__ == "__main__":
    # Diretório atual onde as imagens estão localizadas
    current_directory = './imagens'  # Diretório atual, altere se necessário
    
    # Solicitar entrada do usuário para palavras a serem pesquisadas
    user_input = input("Informe as palavras que deseja pesquisar (Ex: nao,mecanismo,diversao): ").strip()
    
    # Converter a entrada para uma lista de palavras
    target_texts = [text.strip() for text in user_input.split(',')]
    
    print("\nProcessando imagens...\n")
    
    # Processar todas as imagens no diretório
    process_images_in_directory(current_directory, target_texts)

