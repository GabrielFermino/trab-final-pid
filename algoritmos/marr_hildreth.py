import numpy as np
from PIL import Image
import scipy.ndimage
import matplotlib.pyplot as plt

def marrHildreth(image):

    def gaussianKernel(size, sigma):
        ax = np.linspace(-(size // 2), size // 2, size)
        gauss = np.exp(-0.5 * (ax ** 2) / (sigma ** 2))
        kernel = np.outer(gauss, gauss)
        return kernel / np.sum(kernel)

    def applyGaussianFilter(imageArray, size=5, sigma=2.0):
        kernel = gaussianKernel(size, sigma)
        return scipy.ndimage.convolve(imageArray, kernel, mode='reflect')

    def applyLaplacian(imageArray):
        laplacianKernel = np.array([[0, 1, 0],
                                     [1, -4, 1],
                                     [0, 1, 0]])
        return scipy.ndimage.convolve(imageArray, laplacianKernel, mode='reflect')

    def detectZeroCrossings(logImage, threshold):
        rows, cols = logImage.shape
        edges = np.zeros_like(logImage, dtype=np.uint8)
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                patch = logImage[i-1:i+2, j-1:j+2]
                minVal, maxVal = patch.min(), patch.max()
                if minVal < 0 and maxVal > 0 and (maxVal - minVal) > threshold:
                    edges[i, j] = 255
        return edges

    def marrHildrethEdgeDetection(image, size=7, sigma=2.5):
        image = image.convert("L")
        imageArray = np.array(image, dtype=np.float32)
        smoothed = applyGaussianFilter(imageArray, size, sigma)
        logImage = applyLaplacian(smoothed)
        logImage = (logImage - logImage.min()) / (logImage.max() - logImage.min())
        logImage = logImage * 255 - 128
        edges = detectZeroCrossings(logImage, threshold=15.0)
        result = Image.fromarray(edges)
        
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(image, cmap="gray")
        axes[0].set_title("Grayscale Image")

        axes[1].imshow(result, cmap="gray")
        axes[1].set_title("Marr-Hildreth Edges")
        plt.show()

    marrHildrethEdgeDetection(image)

"""
O algoritmo Marr-Hildreth baseia-se na detecção de bordas por meio do operador Laplaciano do Gaussiano (LoG). Seu funcionamento segue estas etapas:

Aplica-se um filtro gaussiano para reduzir o ruído
Por meio do cálculo do Laplaciano obtém a segunda derivada da imagem, evidenciando variações bruscas de intensidade.
Identifica os locais onde a função Laplaciana cruza o eixo zero, correspondendo a possíveis bordas

Resultado: Bordas mais grossas e possiveis bordas falsas
"""
