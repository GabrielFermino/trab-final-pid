import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

def canny(image):
    def applyGaussianFilter(image, kernelSize=5, sigma=1.0):
        kernel = np.fromfunction(
            lambda x, y: (1 / (2 * np.pi * sigma**2)) *
                         np.exp(-((x - (kernelSize // 2))**2 + (y - (kernelSize // 2))**2) / (2 * sigma**2)),
            (kernelSize, kernelSize)
        )
        kernel /= np.sum(kernel)
        return image.filter(ImageFilter.Kernel((kernelSize, kernelSize), kernel.flatten(), scale=np.sum(kernel)))

    def computeSobelGradients(image):
        sobelX = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobelY = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        
        grayImage = np.array(image.convert("L"), dtype=np.float32)
        gradientX = np.zeros_like(grayImage)
        gradientY = np.zeros_like(grayImage)
        
        for i in range(1, grayImage.shape[0] - 1):
            for j in range(1, grayImage.shape[1] - 1):
                gradientX[i, j] = np.sum(sobelX * grayImage[i-1:i+2, j-1:j+2])
                gradientY[i, j] = np.sum(sobelY * grayImage[i-1:i+2, j-1:j+2])
        
        magnitude = np.sqrt(gradientX**2 + gradientY**2)
        direction = np.arctan2(gradientY, gradientX)
        return magnitude, direction

    def suppressNonMaximum(magnitude, direction):
        suppressed = np.zeros_like(magnitude)
        angle = direction * (180 / np.pi) % 180
        
        for i in range(1, magnitude.shape[0] - 1):
            for j in range(1, magnitude.shape[1] - 1):
                neighbor1, neighbor2 = 255, 255
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    neighbor1, neighbor2 = magnitude[i, j+1], magnitude[i, j-1]
                elif (22.5 <= angle[i, j] < 67.5):
                    neighbor1, neighbor2 = magnitude[i+1, j-1], magnitude[i-1, j+1]
                elif (67.5 <= angle[i, j] < 112.5):
                    neighbor1, neighbor2 = magnitude[i+1, j], magnitude[i-1, j]
                elif (112.5 <= angle[i, j] < 157.5):
                    neighbor1, neighbor2 = magnitude[i-1, j-1], magnitude[i+1, j+1]
                
                if magnitude[i, j] >= neighbor1 and magnitude[i, j] >= neighbor2:
                    suppressed[i, j] = magnitude[i, j]
        
        return suppressed

    def applyDoubleThreshold(image, lowThreshold, highThreshold):
        strongPixel = 255
        weakPixel = 75
        edges = np.zeros_like(image)
        strongI, strongJ = np.where(image >= highThreshold)
        weakI, weakJ = np.where((image >= lowThreshold) & (image < highThreshold))
        edges[strongI, strongJ] = strongPixel
        edges[weakI, weakJ] = weakPixel
        return edges

    def performHysteresis(image):
        strongPixel = 255
        weakPixel = 75
        for i in range(1, image.shape[0] - 1):
            for j in range(1, image.shape[1] - 1):
                if image[i, j] == weakPixel:
                    if (image[i+1, j] == strongPixel or image[i-1, j] == strongPixel or 
                        image[i, j+1] == strongPixel or image[i, j-1] == strongPixel or 
                        image[i+1, j+1] == strongPixel or image[i-1, j-1] == strongPixel or 
                        image[i+1, j-1] == strongPixel or image[i-1, j+1] == strongPixel):
                        image[i, j] = strongPixel
                    else:
                        image[i, j] = 0
        return image

    def cannyEdgeDetection(image, lowThreshold=50, highThreshold=150):
        smoothedImage = applyGaussianFilter(image)
        magnitude, direction = computeSobelGradients(smoothedImage)
        suppressedImage = suppressNonMaximum(magnitude, direction)
        thresholdedImage = applyDoubleThreshold(suppressedImage, lowThreshold, highThreshold)
        finalEdges = performHysteresis(thresholdedImage)
        
        finalEdges = finalEdges.astype(np.uint8)
        resultImage = Image.fromarray(finalEdges)

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        axes[0].imshow(image, cmap="gray")
        axes[0].set_title("Grayscale Image")
        
        axes[1].imshow(resultImage, cmap="gray")
        axes[1].set_title("Canny Edge Detection")
        
        plt.show()

    cannyEdgeDetection(image)

"""
O algoritmo de Canny funciona em etapas:

Aplica-se um filtro gaussiano para reduzir ruído.
Utiliza-se um operador de derivada (como Sobel) para calcular a magnitude e direção do gradiente da imagem.
Mantêm-se apenas os pixels que representam máximos locais, reduzindo espessura da borda.
Histerese:
    Bordas fortes (acima do limiar superior) são mantidas.
    Bordas fracas (entre os dois limiares) são mantidas apenas se estiverem conectadas a bordas fortes.

Resultado:
Melhor desempenho em imagens com ruído
Reduz falsas detecções
Produz bordas finas e bem definidas

"""