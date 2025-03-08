from PIL import Image
import matplotlib.pyplot as plt

def all_contar_objetos(imagem):
    def load_and_binarize(image_path, threshold=128):
        img = Image.open(image_path).convert("L")  # Converte para escala de cinza
        img = img.point(lambda p: 255 if p > threshold else 0)  # Binariza (0 = preto, 255 = branco)
        return img

    def count_objects_in_red_zones(binary_image, marked_image):
        rows, cols = binary_image.size[1], binary_image.size[0]
        object_count = 0  # Contador de objetos
        visited = [[False for _ in range(cols)] for _ in range(rows)]  # Matriz de visitados

        # Função para flood fill (preenchimento por inundação)
        def flood_fill(x, y):
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if 0 <= cx < rows and 0 <= cy < cols:
                    if not visited[cx][cy] and binary_image.getpixel((cy, cx)) == 255:
                        visited[cx][cy] = True
                        stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])

        # Percorre a imagem para contar objetos dentro das zonas vermelhas
        for i in range(rows):
            for j in range(cols):
                # Verifica se o pixel é vermelho na imagem marcada
                if marked_image.getpixel((j, i)) == (255, 0, 0):  # Vermelho
                    # Verifica se há um objeto branco não visitado
                    if binary_image.getpixel((j, i)) == 255 and not visited[i][j]:
                        flood_fill(i, j)  # Marca todos os pixels do objeto
                        object_count += 1  # Incrementa o contador de objetos

        return object_count

    image_path = f"./imagens/{imagem}"

    # Carrega a imagem original e binariza
    original_image = Image.open(image_path)
    binary_image = load_and_binarize(image_path)

    # Cria uma cópia da imagem binarizada para marcar os pixels
    marked_image = binary_image.convert("RGB")

    # Percorre todos os pixels da imagem para pintar os vizinhos de vermelho
    rows, cols = binary_image.size[1], binary_image.size[0]
    for i in range(rows):
        for j in range(cols):
            if binary_image.getpixel((j, i)) == 255:  # Se o pixel for branco (objeto)
                # Verifica os 4 vizinhos (cima, baixo, esquerda, direita)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < rows and 0 <= ny < cols:  # Verifica se está dentro dos limites da imagem
                        if binary_image.getpixel((ny, nx)) == 0:  # Se o vizinho for preto (fundo)
                            marked_image.putpixel((ny, nx), (255, 0, 0))  # Pinta o vizinho de vermelho

    # Conta os objetos dentro das zonas vermelhas
    object_count = count_objects_in_red_zones(binary_image, marked_image)

    # Exibe a imagem binarizada e a imagem com os vizinhos pintados
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Imagem Binarizada (Preto e Branco)")
    plt.imshow(binary_image, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title(f"Objetos Dentro das Linhas Vermelhas: {object_count}")
    plt.imshow(marked_image)
    plt.axis("off")

    plt.show()

# Exemplo de uso
# all_contar_objetos("sua_imagem.jpg")