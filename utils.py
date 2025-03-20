import matplotlib.image as mpimg
import numpy as np
from PIL import Image

def Binarizar(imagem):
    # Convert the image to a NumPy array
    imagem = np.array(imagem)

    aux = np.shape(imagem)

    if np.size(aux) > 2: 
        imagem = imagem[0:, 0:, 0]
        aux = np.shape(imagem)

    # Binary image: 0 if less than 128, 1 if greater than or equal to 128
    ImgBin = np.zeros(aux)

    for x in range(aux[0]):
        for y in range(aux[1]):
            if imagem[x][y] >= 128:
                ImgBin[x][y] = 1
            else:
                ImgBin[x][y] = 0

    return ImgBin
