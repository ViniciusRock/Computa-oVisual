*Sobre o projeto*
---

*Leitura e detecção de texto dentro de imagens para auxílio de leitores de tela*

O mesmo script também ser adaptado para visualização de placas de trânsito, pois o script possibilita o redimensionamento de imagem para melhor nitidez, bem como, a detecção de palavras, podendo ser aplicado a muitos outros tipos de soluções.

*Documentação e instalação*
---
**Pré-Requisitos: Python 3.1X ou superior**

**Passo 1.Extraia o projeto em uma pasta**

**Passo 2.Entrar na pasta do projeto via linha de comando**

**Passo 3.Execute os comandos a seguir**
```
cd nomedapasta/
```
```
python -m venv venv 
```
>Obs: Acima, criará uma nova pasta chamada venv no seu diretório, que conterá o ambiente virtual.

**Passo 4. Ativar o ambiente virtual no Windows(cmd/Powershell)**
```
.\venv\Scripts\Activate
```
**Passo 4. Ativar o ambiente virtual no Linux**
```
venv\Scripts\activate
``` 
**Passo 5: Instalando as dependências**
**Instalando rede neural Tesseract OCR:**

[Clique aqui para assistir ao vídeo](https://github.com/ViniciusRock/ComputacaoVisual/tree/main/trabalho.mp4)

**Instalando os módulos de requisitos**
```
pip install -r requirements.txt
```
---

**Como usar**
---
> python leia.py
![Foto do prompt](/docs/prompt.png "Foto do prompt")

**Resultado da detecção**
![Foto do resultado](/docs/teste.png "Foto do resultado")

