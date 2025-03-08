import os
import box
import cadeia_freeman
import canny
import contar_objetos
import intensidade
import marr_hildreth
import otsu
import watershed
from Operacoes import *

def listar_imagens(diretorio="imagens"):
    """Lista todas as imagens no diretório especificado."""
    imagens = [f for f in os.listdir(diretorio) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))]
    return imagens

def exibir_titulo(titulo):
    """Exibe um título formatado."""
    print("\n" + "=" * 50)
    print(f"{titulo:^50}")
    print("=" * 50)

def exibir_opcoes(opcoes):
    """Exibe as opções disponíveis."""
    for key, (nome, _) in opcoes.items():
        print(f"{key} - {nome}")

def escolher_metodo(metodos):
    """Permite ao usuário escolher um método."""
    exibir_titulo("Escolha um Método")
    exibir_opcoes(metodos)
    escolha = input("\nDigite o número do método desejado: ")
    return escolha

def escolher_imagem(imagens):
    """Permite ao usuário escolher uma imagem."""
    exibir_titulo("Escolha uma Imagem")
    for idx, img in enumerate(imagens, 1):
        print(f"{idx} - {img}")
    escolha = input("\nDigite o número da imagem desejada: ")
    return escolha

def main():
    # Dicionário de métodos disponíveis
    metodos = {
        "1": ("Box", box.all_box),
        "2": ("Cadeia Freeman", cadeia_freeman.all_cadeia_freeman),
        "3": ("Canny", canny.all_canny),
        "4": ("Contar Objetos", contar_objetos.all_contar_objetos),
        "5": ("Intensidade", intensidade.all_intensidade),
        "6": ("Marr-Hildreth", marr_hildreth.all_marr_hildreth),
        "7": ("Otsu", otsu.all_otsu),
        "8": ("Watershed", watershed.all_watershed),
    }

    # Lista as imagens disponíveis
    imagens = listar_imagens()
    if not imagens:
        print("\nNenhuma imagem encontrada no diretório 'imagens/'.")
        return

    # Escolha do método
    escolha_metodo = escolher_metodo(metodos)
    if escolha_metodo not in metodos:
        print("\nOpção inválida. Tente novamente.")
        return

    # Escolha da imagem
    escolha_img = escolher_imagem(imagens)
    if not escolha_img.isdigit() or int(escolha_img) not in range(1, len(imagens) + 1):
        print("\nOpção inválida. Tente novamente.")
        return

    # Executa o método escolhido na imagem selecionada
    imagem_escolhida = f"{imagens[int(escolha_img) - 1]}"
    funcao = metodos[escolha_metodo][1]
    exibir_titulo(f"Executando {metodos[escolha_metodo][0]} na Imagem {imagem_escolhida}")
    funcao(imagem_escolhida)

if __name__ == '__main__':
    while True:
        main()
        continuar = input("\nDeseja continuar? (s/n): ")
        if continuar.lower() != "s":
            print("\nObrigado por usar o programa. Até logo!")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o console