import heapq
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def watershed(imagem):
    def loadImage(imagePath):
        img = imagem
        pixels = np.array(img, dtype=np.uint8)
        return pixels

    def thresholdManual(image):
        threshold = 150
        grayscale = np.array(image.convert("L"))
        binary = np.where(grayscale > threshold, 255, 0).astype(np.uint8)
        return binary

    def distanceTransform(binary):
        dist = np.full(binary.shape, np.inf)
        queue = []
        for y in range(binary.shape[0]):
            for x in range(binary.shape[1]):
                if binary[y, x] == 255:
                    dist[y, x] = 0
                    heapq.heappush(queue, (0, y, x))
        while queue:
            d, y, x = heapq.heappop(queue)
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < binary.shape[0] and 0 <= nx < binary.shape[1]:
                    newD = d + 1
                    if newD < dist[ny, nx]:
                        dist[ny, nx] = newD
                        heapq.heappush(queue, (newD, ny, nx))
        return dist

    def connectedComponents(binary):
        labels = np.zeros(binary.shape, dtype=np.int32)
        labelId = 1

        def floodFill(y, x):
            stack = [(y, x)]
            while stack:
                cy, cx = stack.pop()
                if labels[cy, cx] == 0 and binary[cy, cx] == 255:
                    labels[cy, cx] = labelId
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < binary.shape[0] and 0 <= nx < binary.shape[1]:
                            stack.append((ny, nx))

        for y in range(binary.shape[0]):
            for x in range(binary.shape[1]):
                if binary[y, x] == 255 and labels[y, x] == 0:
                    floodFill(y, x)
                    labelId += 1

        return labels

    def watershedAlgorithm(image):
        binary = thresholdManual(image)
        dist = distanceTransform(binary)
        markers = connectedComponents(binary)
        segmented = np.zeros_like(image, dtype=np.uint8)
        for label in np.unique(markers):
            if label == 0:
                continue
            segmented[markers == label] = 50 + (label * 50) % 200
        return image, segmented

    image = imagem
    original, segmentedImage = watershedAlgorithm(image)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(original, cmap="gray")
    axes[0].set_title("Imagem Grayscale")
    axes[0].axis("off")
    axes[1].imshow(segmentedImage, cmap="gray")
    axes[1].set_title("Watershed")
    axes[1].axis("off")
    plt.show()
