def Erosion(imagem, SE, centrox, centroy):
    linhas = len(imagem)
    colunas = len(imagem[0])

    # Se imagem for RGB (3D), pega apenas a matriz de cor
    if isinstance(imagem[0][0], list):
        imagem = [linha[0] for linha in imagem]
        linhas = len(imagem)
        colunas = len(imagem[0])
    
    # Cria o complemento da imagem
    for x in range(linhas):
        for y in range(colunas):
            imagem[x][y] = 1 - imagem[x][y]

    ImgErode = Dilation(imagem, SE, centrox, centroy)  # Dilata o complemento

    # Tira o complemento da imagem erodida
    for x in range(linhas):
        for y in range(colunas):
            ImgErode[x][y] = 1 - ImgErode[x][y]

    # Corrige valores das bordas
    for i in range(linhas):
        ImgErode[i][0] = ImgErode[i][1]
        ImgErode[i][-1] = ImgErode[i][-2]

    for j in range(colunas):
        ImgErode[0][j] = ImgErode[1][j]
        ImgErode[-1][j] = ImgErode[-2][j]

    return ImgErode

def Dilation(imagem, SE, centrox, centroy):
    linhas = len(imagem)
    colunas = len(imagem[0])
    tam_SE = (len(SE), len(SE[0]))  # Tamanho do elemento estruturante

    ImgDilat = []  # Array para a imagem dilatada
    check = 0  # Flag para indicar se o SE está contido
    total = sum(SE[u][v] != 0 for u in range(tam_SE[0]) for v in range(tam_SE[1]))

    for x in range(linhas):
        ImgLinha = []
        for y in range(colunas):
            if imagem[x][y] == 1:  # Verifica se o pixel é branco
                for u in range(-centrox, tam_SE[0] - centrox):
                    for v in range(-centroy, tam_SE[1] - centroy):
                        if 0 <= x + u < linhas and 0 <= y + v < colunas:
                            check += SE[u + centrox][v + centroy] * imagem[x + u][y + v]
                if check == total:
                    ImgLinha.append(1)
                else:
                    ImgLinha.append(0)
                check = 0
            else:
                ImgLinha.append(0)
        ImgDilat.append(ImgLinha)
    return ImgDilat

def Opening(imagem, SE, centrox, centroy):
    return Dilation(Erosion(imagem, SE, centrox, centroy), SE, centrox, centroy)

def Closing(imagem, SE, centrox, centroy):
    return Erosion(Dilation(imagem, SE, centrox, centroy), SE, centrox, centroy)
