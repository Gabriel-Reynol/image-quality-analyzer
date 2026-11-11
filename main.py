import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime
from uuid import uuid4

# Caminhos
BASE_DIR = Path(__file__).resolve().parent
PASTA_RESULTADOS = BASE_DIR / "resultados"

def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def calcular_nitidez(imagem_cinza):
    laplaciano = cv2.Laplacian(imagem_cinza, cv2.CV_64F)
    variancia = laplaciano.var()
    return float(variancia)

def calcular_luminosidade(imagem_cinza):
    return float(np.mean(imagem_cinza))

def calcular_contraste(imagem_cinza):
    return float(np.std(imagem_cinza))

def verificar_desfoque(nitidez):
    # Limiares experimentais, não universais
    if nitidez < 100:
        return "desfocada"
    elif nitidez <= 500:
        return "indeterminada"
    else:
        return "nitida"

def desfocar_imagem(image):
    # Aplica o filtro Gaussiano mantendo as cores
    imagem_desfocada = cv2.GaussianBlur(image, (9, 9), 0)
    return imagem_desfocada

def visualizar_imagens(original, cinza, processada,
                       foi_desfocada, pasta_execucao):

    original_rgb = cv2.cvtColor(
        original, cv2.COLOR_BGR2RGB
    )

    processada_rgb = cv2.cvtColor(
        processada, cv2.COLOR_BGR2RGB
    )

    if foi_desfocada:
        titulo_final = "Imagem Desfocada pelo Programa"
    else:
        titulo_final = "Imagem Mantida sem Alterações"

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))

    axes[0].imshow(original_rgb)
    axes[0].set_title("Imagem Original")

    axes[1].imshow(cinza, cmap="gray", vmin=0, vmax=255)
    axes[1].set_title("Escala de Cinza")

    axes[2].imshow(processada_rgb)
    axes[2].set_title(titulo_final)

    for ax in axes:
        ax.axis("off")

    fig.tight_layout()

    fig.savefig(
        pasta_execucao / "comparacao.png",
        dpi=150
    )

    plt.show()
    plt.close(fig)

def main():
    print("=== IMAGE QUALITY ANALYZER ===")

    caminho = input("Digite o nome ou caminho da imagem: ").strip().strip('"')

    if not caminho:
        print("Nenhuma imagem informada.")
        return

    caminho_imagem = Path(caminho)

    # Caminhos relativos partem da pasta do main.py
    if not caminho_imagem.is_absolute():
        caminho_imagem = BASE_DIR / caminho_imagem

    image = cv2.imread(str(caminho_imagem))

    if image is None:
        print("Erro: não foi possível carregar a imagem.")
        return

    print("\nImagem carregada com sucesso!")
    print("Dimensões:", image.shape)

    # Análise da imagem
    imagem_cinza = convert_to_grayscale(image)

    nitidez_original = calcular_nitidez(imagem_cinza)
    luminosidade = calcular_luminosidade(imagem_cinza)
    contraste = calcular_contraste(imagem_cinza)

    print("\n--- ANÁLISE DE QUALIDADE ---")
    print(f"Nitidez: {nitidez_original:.2f}")
    print(f"Luminosidade média: {luminosidade:.2f}")
    print(f"Contraste: {contraste:.2f}")

    # Classifica a nitidez da imagem
    classificacao = verificar_desfoque(nitidez_original)

    if classificacao == "desfocada":
        print("\nImagem possivelmente já desfocada.")
        print("Nenhum desfoque adicional será aplicado.")

        imagem_processada = image.copy()
        foi_desfocada = False

    elif classificacao == "indeterminada":
        print("\nNitidez indeterminada.")
        print("Imagem mantida sem alterações.")

        imagem_processada = image.copy()
        foi_desfocada = False

    else:
        print("\nImagem possivelmente nítida.")
        print("Aplicando filtro Gaussiano...")

        imagem_processada = desfocar_imagem(image)
        foi_desfocada = True

    # Calcula as métricas após o processamento
    processada_cinza = convert_to_grayscale(
        imagem_processada
    )

    nitidez_final = calcular_nitidez(processada_cinza)
    luminosidade_final = calcular_luminosidade(
        processada_cinza
    )
    contraste_final = calcular_contraste(
        processada_cinza
    )

    print("\n--- RESULTADOS ---")
    print(f"Classificação: {classificacao}")
    print(f"Nitidez original: {nitidez_original:.2f}")
    print(f"Nitidez final: {nitidez_final:.2f}")
    print(f"Luminosidade final: {luminosidade_final:.2f}")
    print(f"Contraste final: {contraste_final:.2f}")

    if foi_desfocada:
        operacao = "desfocada"
    else:
        operacao = "sem_alteracoes"

    # Cria uma pasta diferente para cada execução
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    identificador = uuid4().hex[:8]

    pasta_execucao = (
        PASTA_RESULTADOS /
        f"{timestamp}_{identificador}_{operacao}"
    )

    pasta_execucao.mkdir(
        parents=True, exist_ok=False
    )

    # Salva a imagem final
    cv2.imwrite(
        str(pasta_execucao / "imagem_final.png"),
        imagem_processada
    )

    # Salva a versão em escala de cinza
    cv2.imwrite(
        str(pasta_execucao / "imagem_cinza.png"),
        imagem_cinza
    )

    # Salva a comparação visual
    visualizar_imagens(
        image,
        imagem_cinza,
        imagem_processada,
        foi_desfocada,
        pasta_execucao
    )

    # Salva as métricas da execução
    with open(
        pasta_execucao / "metricas.txt",
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(f"Imagem: {caminho_imagem.name}\n")
        arquivo.write(f"Classificação: {classificacao}\n")
        arquivo.write(f"Operação: {operacao}\n")
        arquivo.write(
            "Limiares experimentais: 100 e 500\n"
        )
        arquivo.write(
            f"Nitidez original: {nitidez_original:.2f}\n"
        )
        arquivo.write(
            f"Nitidez final: {nitidez_final:.2f}\n"
        )
        arquivo.write(
            f"Luminosidade original: {luminosidade:.2f}\n"
        )
        arquivo.write(
            f"Luminosidade final: {luminosidade_final:.2f}\n"
        )
        arquivo.write(
            f"Contraste original: {contraste:.2f}\n"
        )
        arquivo.write(
            f"Contraste final: {contraste_final:.2f}\n"
        )

    print("\nArquivos salvos em:")
    print(pasta_execucao)

if __name__ == "__main__":
    main()