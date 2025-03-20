from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
from algoritmos.otsu import otsu

def find_objects(labeled_array):
    objetos = []
    labels = set()
    linhas, colunas = len(labeled_array), len(labeled_array[0])
    
    for i in range(linhas):
        for j in range(colunas):
            if labeled_array[i][j] != 0:
                labels.add(labeled_array[i][j])
    
    for label in labels:
        x_min, x_max, y_min, y_max = colunas, 0, linhas, 0
        
        for i in range(linhas):
            for j in range(colunas):
                if labeled_array[i][j] == label:
                    x_min = min(x_min, j)
                    x_max = max(x_max, j)
                    y_min = min(y_min, i)
                    y_max = max(y_max, i)
        
        objetos.append((slice(y_min, y_max + 1), slice(x_min, x_max + 1)))
    
    return objetos

def flood_fill(image, labeled_array, x, y, label):
    stack = [(x, y)]
    while stack:
        i, j = stack.pop()
        if 0 <= i < len(image) and 0 <= j < len(image[0]) and image[i][j] and labeled_array[i][j] == 0:
            labeled_array[i][j] = label
            stack.extend([(i-1, j), (i+1, j), (i, j-1), (i, j+1)])

def contar_objetos(imagem):
    def load_and_binarize(image):
        segmentedImage, threshold = otsu(image)
        return segmentedImage
        # img = image.point(lambda p: 255 if p > threshold else 0)
        # return segmentedImage.convert("L")
    
    def dilation(imagem, SE, centrox, centroy):
        linhas = len(imagem)
        colunas = len(imagem[0])
        tam_SE = (len(SE), len(SE[0]))
        
        ImgDilat = np.zeros((linhas, colunas), dtype=int)
        for x in range(linhas):
            for y in range(colunas):
                if imagem[x][y] == 1:
                    for u in range(-centrox, tam_SE[0] - centrox):
                        for v in range(-centroy, tam_SE[1] - centroy):
                            if 0 <= x + u < linhas and 0 <= y + v < colunas:
                                if SE[u + centrox][v + centroy] == 1:
                                    ImgDilat[x + u][y + v] = 1
        
        return ImgDilat
    
    def erosion(imagem, SE, centrox, centroy):
        linhas = len(imagem)
        colunas = len(imagem[0])
        ImgErode = np.copy(imagem)
        for x in range(linhas):
            for y in range(colunas):
                if imagem[x][y] == 1:
                    for u in range(-centrox, len(SE) - centrox):
                        for v in range(-centroy, len(SE[0]) - centroy):
                            if 0 <= x + u < linhas and 0 <= y + v < colunas:
                                if SE[u + centrox][v + centroy] == 1 and imagem[x + u][y + v] == 0:
                                    ImgErode[x][y] = 0
                                    break
        return ImgErode
    
    def count_objects_and_draw_boxes(binary_image):
        img_array = np.array(binary_image.convert("L")) == 0
        # SE = np.array([[0, 0, 1, 0, 0], 
        #                [0, 1, 1, 1, 0], 
        #                [1, 1, 1, 1, 1], 
        #                [0, 1, 1, 1, 0], 
        #                [0, 0, 1, 0, 0]])
        SE = np.array( [[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]])
        img_array = dilation(erosion(img_array, SE, 1, 1), SE, 1, 1)
        
        labeled_array = np.zeros_like(img_array, dtype=int)
        label_counter = 1
        for i in range(len(img_array)):
            for j in range(len(img_array[0])):
                if img_array[i][j] and labeled_array[i][j] == 0:
                    flood_fill(img_array, labeled_array, i, j, label_counter)
                    label_counter += 1
        
        objects_slices = find_objects(labeled_array)
        
        marked_image = Image.fromarray(np.uint8(img_array))
        draw = ImageDraw.Draw(marked_image)
        
        for obj_slice in objects_slices:
            if obj_slice:
                y_slice, x_slice = obj_slice
                x_min, x_max = x_slice.start, x_slice.stop
                y_min, y_max = y_slice.start, y_slice.stop
                draw.rectangle([x_min, y_min, x_max, y_max], outline=(170), width=5)
        
        return label_counter - 1, marked_image
    
    imagem = imagem
    binary_image = load_and_binarize(imagem)
    
    object_count, final_image = count_objects_and_draw_boxes(binary_image)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Imagem Original")
    plt.imshow(binary_image, cmap="gray")
    plt.axis("off")
    
    plt.subplot(1, 2, 2)
    plt.title(f"Objetos Detectados: {object_count}")
    plt.imshow(final_image, cmap="gray")
    plt.axis("off")
    
    plt.show()
    
    return object_count