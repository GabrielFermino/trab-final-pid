import os
from PIL import Image
import algoritmos.otsu as otsu
import algoritmos.canny as canny
import algoritmos.contar_objetos as contar_objetos
import algoritmos.grayscale as grayscale
import algoritmos.marr_hildreth as marr_hildreth
import algoritmos.watershed as watershed
import algoritmos.box as box
import algoritmos.cadeia_freeman as cadeia_freeman

def listar_imagens(diretorio="imagens"):
    imagens = [f for f in os.listdir(diretorio) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))]
    return imagens

def exibir_titulo(titulo):
    print("\n" + "=" * 50)
    print(f"{titulo:^50}")
    print("=" * 50)

def exibir_opcoes(opcoes):
    for key, (nome, _) in opcoes.items():
        print(f"{key} - {nome}")

def escolher_metodo(metodos):
    exibir_titulo("Escolha um Método")
    exibir_opcoes(metodos)
    escolha = input("\nDigite o número do método desejado: ")
    return escolha

def escolher_imagem(imagens):
    exibir_titulo("Escolha uma Imagem")
    for idx, img in enumerate(imagens, 1):
        print(f"{idx} - {img}")
    escolha = input("\nDigite o número da imagem desejada: ")
    return escolha

def main():
    metodos = {
        "1": ("Otsu", otsu.otsu),
        "2": ("Canny", canny.canny),
        "3": ("Contar Objetos", contar_objetos.contarObjetos),
        "4": ("Intensidade", grayscale.grayscale),
        "5": ("Marr-Hildreth", marr_hildreth.marrHildreth),
        "6": ("Watershed", watershed.watershed),
        "7": ("Box", box.box),
        "8": ("Cadeia de Freeman", cadeia_freeman.cadeiaFreeman)
    }

    imagens = listar_imagens()
    if not imagens:
        print("\nNenhuma imagem encontrada no diretório 'imagens/'.")
        return
    
    escolha_img = escolher_imagem(imagens)
    if not escolha_img.isdigit() or int(escolha_img) not in range(1, len(imagens) + 1):
        print("\nOpção inválida. Tente novamente.")
        return

    imagem_escolhida = f"{imagens[int(escolha_img) - 1]}"
    caminho_imagem = os.path.join("imagens", imagem_escolhida)
    imagem = Image.open(caminho_imagem)

    escolha_metodo = escolher_metodo(metodos)
    if escolha_metodo not in metodos:
        print("\nOpção inválida. Tente novamente.")
        return
    
    funcao = metodos[escolha_metodo][1]
    exibir_titulo(f"Executando {metodos[escolha_metodo][0]} na Imagem {imagem_escolhida}")
    funcao(imagem)

if __name__ == '__main__':
    while True:
        main()
        continuar = input("\nDeseja continuar? (s/n): ")
        if continuar.lower() != "s":
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o console