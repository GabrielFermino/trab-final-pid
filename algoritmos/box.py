import matplotlib.pyplot as plt
from PIL import Image

def box(imagem):
    def readImage(filename):
        img = filename.convert("L")
        width, height = img.size
        pixels = list(img.getdata())
        grayscale = [pixels[i * width:(i + 1) * width] for i in range(height)]
        return grayscale, width, height

    def applyBoxFilter(image, width, height, kernelSize):
        if kernelSize == 2:
            return applyBoxFilter2x2(image, width, height)
        
        offset = kernelSize // 2
        newImage = [[0] * width for _ in range(height)]

        for y in range(offset, height - offset):
            for x in range(offset, width - offset):
                total = 0
                count = 0
                
                for ky in range(-offset, offset + 1):
                    for kx in range(-offset, offset + 1):
                        total += image[y + ky][x + kx]
                        count += 1

                newImage[y][x] = total // count
        
        return newImage
    
    def applyBoxFilter2x2(image, width, height):
        newImage = [[0] * width for _ in range(height)]
        for y in range(0, height - 1, 2):
            for x in range(0, width - 1, 2):
                total = image[y][x] + image[y][x + 1] + image[y + 1][x] + image[y + 1][x + 1]
                avg = total // 4
                newImage[y][x] = avg
                newImage[y][x + 1] = avg
                newImage[y + 1][x] = avg
                newImage[y + 1][x + 1] = avg
        return newImage

    def plotImages(original, filtered2x2, filtered3x3, filtered5x5, filtered7x7):
        fig, axs = plt.subplots(1, 5, figsize=(15, 5))
        axs[0].imshow(original, cmap='gray')
        axs[0].set_title("Grayscale")

        axs[1].imshow(filtered2x2, cmap='gray')
        axs[1].set_title("2x2 filter")

        axs[2].imshow(filtered3x3, cmap='gray')
        axs[2].set_title("3x3 filter")

        axs[3].imshow(filtered5x5, cmap='gray')
        axs[3].set_title("5x5 filter")

        axs[4].imshow(filtered7x7, cmap='gray')
        axs[4].set_title("7x7 filter")

        for ax in axs:
            ax.axis("off")

        plt.show()
    
    image, width, height = readImage(imagem)
    filtered2x2 = applyBoxFilter(image, width, height, 2)
    filtered3x3 = applyBoxFilter(image, width, height, 3)
    filtered5x5 = applyBoxFilter(image, width, height, 5)
    filtered7x7 = applyBoxFilter(image, width, height, 7)
    plotImages(image, filtered2x2, filtered3x3, filtered5x5, filtered7x7)
