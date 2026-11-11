# Image Quality Analyzer

Projeto desenvolvido em **Python**, utilizando OpenCV, NumPy e Matplotlib para análise de qualidade de imagens e aplicação automática de desfoque Gaussiano.

## Funcionalidades

- Conversão de imagens para escala de cinza.
- Cálculo de nitidez pela variância do Laplaciano.
- Análise de luminosidade e contraste.
- Classificação experimental de nitidez.
- Aplicação automática de desfoque Gaussiano em imagens classificadas como nítidas.
- Visualização e salvamento dos resultados.

## Tecnologias

**Python | OpenCV | NumPy | Matplotlib**

## Resultados

### Imagem com nitidez elevada

Aplicação do filtro Gaussiano em uma imagem com nitidez acima do limite experimental.

![Comparação da imagem nítida](resultados/teste_imagem_nitida/comparacao.png)

### Imagem desfocada

Identificação de possível desfoque, mantendo a imagem sem alterações.

![Comparação da imagem desfocada](resultados/teste_imagem_desfocada/comparacao.png)

## Como executar

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute:

```bash
python main.py
```

Informe o caminho da imagem, por exemplo:

```text
imagens/canva-filhote-de-cachorro.jpg
```

**Observação:** a classificação utiliza limiares experimentais da variância do Laplaciano (100 e 500), que podem não funcionar adequadamente para todas as imagens.