from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
from algoritmos.otsu import otsu
from algoritmos.operacoes import Opening, Closing

def findObjects(labeledArray):
    objetos = []
    labels = set()
    linhas, colunas = len(labeledArray), len(labeledArray[0])
    
    for i in range(linhas):
        for j in range(colunas):
            if labeledArray[i][j] != 0:
                labels.add(labeledArray[i][j])
    
    for label in labels:
        x_min, x_max, y_min, y_max = colunas, 0, linhas, 0
        
        for i in range(linhas):
            for j in range(colunas):
                if labeledArray[i][j] == label:
                    x_min = min(x_min, j)
                    x_max = max(x_max, j)
                    y_min = min(y_min, i)
                    y_max = max(y_max, i)
        
        objetos.append((slice(y_min, y_max + 1), slice(x_min, x_max + 1)))
    
    return objetos

def floodFill(image, labeledArray, x, y, label):
    stack = [(x, y)]
    while stack:
        i, j = stack.pop()
        if 0 <= i < len(image) and 0 <= j < len(image[0]) and image[i][j] and labeledArray[i][j] == 0:
            labeledArray[i][j] = label
            stack.extend([(i-1, j), (i+1, j), (i, j-1), (i, j+1)])

def contarObjetos(imagem):
    def loadAndBinarize(image):
        segmentedImage, threshold = otsu(image)
        return segmentedImage
    
    def countObjectsAndDrawBoxes(binaryImage):
        imgArray = np.array(binaryImage.convert("L")) == 0
        SE = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]])
        
        imgArray = Closing(Opening(imgArray, SE, 1, 1), SE, 1, 1)
        
        labeledArray = np.zeros_like(imgArray, dtype=int)
        labelCounter = 1
        for i in range(len(imgArray)):
            for j in range(len(imgArray[0])):
                if imgArray[i][j] and labeledArray[i][j] == 0:
                    floodFill(imgArray, labeledArray, i, j, labelCounter)
                    labelCounter += 1
        
        objectsSlices = findObjects(labeledArray)
        
        markedImage = binaryImage.copy()
        draw = ImageDraw.Draw(markedImage)
        
        for objSlice in objectsSlices:
            if objSlice:
                ySlice, xSlice = objSlice
                x_min, x_max = xSlice.start, xSlice.stop
                y_min, y_max = ySlice.start, ySlice.stop
                draw.rectangle([x_min, y_min, x_max, y_max], outline=(170), width=5)
        
        return labelCounter - 1, markedImage
    
    imagem = imagem
    binaryImage = loadAndBinarize(imagem)
    
    objectCount, finalImage = countObjectsAndDrawBoxes(binaryImage)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(binaryImage, cmap="gray")
    
    plt.subplot(1, 2, 2)
    plt.title(f"Detected Objects: {objectCount}")
    plt.imshow(finalImage, cmap="gray")
    
    plt.show()
    
    return objectCount
