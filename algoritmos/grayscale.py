from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def grayscale(image):
    def segmentImage(image):
        grayscaleImage = image.convert("L")
        imageArray = np.array(grayscaleImage)

        segmentedArray = np.select(
            [
                (imageArray >= 0) & (imageArray <= 50),
                (imageArray >= 51) & (imageArray <= 100),
                (imageArray >= 101) & (imageArray <= 150),
                (imageArray >= 151) & (imageArray <= 200),
                (imageArray >= 201) & (imageArray <= 255),
            ],
            [25, 75, 125, 175, 255]
        )
        segmentedImage = Image.fromarray(segmentedArray.astype(np.uint8))

        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(image, cmap="gray")
        axes[0].set_title("Original Image")

        axes[1].imshow(segmentedImage, cmap="gray")
        axes[1].set_title("Segmented Image")

        plt.show()

    segmentImage(image)
