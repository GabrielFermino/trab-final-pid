from PIL import Image
import matplotlib.pyplot as plt
import utils
import numpy as np

def otsu(imagemOtsu):
    def otsu_threshold(image):
        gray_image = image.convert("L")
        pixels = list(gray_image.getdata())
        width, height = gray_image.size
        total_pixels = width * height
        hist = [0] * 256
        for pixel in pixels:
            hist[pixel] += 1
            
        max_variance = 0
        best_threshold = 0
        sum_total = sum(i * hist[i] for i in range(256))
        sum_background = 0
        weight_background = 0
        
        for i in range(256):
            weight_background += hist[i]
            if weight_background == 0:
                continue
            weight_foreground = total_pixels - weight_background
            if weight_foreground == 0:
                break
            sum_background += i * hist[i]
            mean_background = sum_background / weight_background
            mean_foreground = (sum_total - sum_background) / weight_foreground
            variance_between = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
            if variance_between > max_variance:
                max_variance = variance_between
                best_threshold = i

        return best_threshold

    def segment_image(image, threshold):
        gray_image = image.convert("L")
        pixels = list(gray_image.getdata())
        
        segmented_pixels = [255 if pixel > threshold else 0 for pixel in pixels]
        
        segmented_image = Image.new("L", gray_image.size)
        segmented_image.putdata(segmented_pixels)
        
        return segmented_image
    
    grayscale_image = imagemOtsu.convert("L")
    threshold = otsu_threshold(grayscale_image)
    print("Limiar ótimo de Otsu:", threshold)

    segmented_image = segment_image(grayscale_image, threshold)
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(grayscale_image, cmap="gray")
    axes[0].set_title("Imagem Grayscale")
    axes[0].axis("off")

    axes[1].imshow(segmented_image, cmap="gray")
    axes[1].set_title("Segmentação Otsu")
    axes[1].axis("off")

    plt.show()

    return segmented_image, threshold