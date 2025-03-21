import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def cadeiaFreeman(imagem):

    def binarizeImage(imagem, threshold=128):
        grayscaleImage = imagem.convert("L")
        imgArray = np.array(grayscaleImage)
        binaryArray = np.where(imgArray > threshold, 255, 0)
        return binaryArray.astype(np.uint8)

    def freemanChainCode(binaryImage):

        def findStartPoint(image):
            for row in range(image.shape[0]):
                for col in range(image.shape[1]):
                    if image[row, col] == 255:
                        return row, col
            return None

        def getNeighbor(row, col, direction):
            if direction == 0: 
                return row, col + 1
            elif direction == 1:  
                return row + 1, col + 1
            elif direction == 2:  
                return row + 1, col
            elif direction == 3:  
                return row + 1, col - 1
            elif direction == 4: 
                return row, col - 1
            elif direction == 5: 
                return row - 1, col - 1
            elif direction == 6:  
                return row - 1, col
            elif direction == 7:  
                return row - 1, col + 1
            else:
                return None

        def findNextBoundaryPixel(image, currentRow, currentCol, previousDirection):
            searchOrder = [(previousDirection + i) % 8 for i in range(1, 9)]
            for direction in searchOrder:
                newRow, newCol = getNeighbor(currentRow, currentCol, direction)
                if 0 <= newRow < image.shape[0] and 0 <= newCol < image.shape[1]:
                    if image[newRow, newCol] == 255:
                        return newRow, newCol, direction
            return None

        startPoint = findStartPoint(binaryImage)
        if startPoint is None:
            print("No object found in the image.")
            return None

        chainCode = ""
        currentRow, currentCol = startPoint
        previousDirection = 7
        firstPixel = True
        visitedPixels = set()
        boundaryPixels = [(currentRow, currentCol)]

        while True:
            if firstPixel:
                nextPixelInfo = findNextBoundaryPixel(binaryImage, currentRow, currentCol, previousDirection)
                firstPixel = False
            else:
                nextPixelInfo = findNextBoundaryPixel(binaryImage, currentRow, currentCol, (previousDirection + 4) % 8)

            if nextPixelInfo is None:
                break
            
            nextRow, nextCol, direction = nextPixelInfo

            if (nextRow, nextCol) in visitedPixels:
                if (nextRow, nextCol) == startPoint:
                    break
                else:
                    print("Loop detected. Ending iteration.")
                    break

            visitedPixels.add((nextRow, nextCol))
            boundaryPixels.append((nextRow, nextCol))

            chainCode += str(direction)
            currentRow, currentCol = nextRow, nextCol
            previousDirection = direction

        return chainCode, boundaryPixels

    originalImage = imagem
    binaryImage = binarizeImage(imagem)
    
    if binaryImage is not None:
        chainCode, boundaryPixels = freemanChainCode(binaryImage)
        if chainCode:

            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(originalImage)
            plt.title("Grayscale Image")

            plt.subplot(1, 2, 2)
            plt.imshow(binaryImage, cmap='gray')
            rows, cols = zip(*boundaryPixels)
            plt.plot(cols, rows, 'b-', linewidth=2)
            plt.title("Connected Boundary")
            plt.show()
        else:
            print("Cannot generate chain code.")
