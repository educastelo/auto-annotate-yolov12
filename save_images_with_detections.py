import os
from PIL import Image, ImageDraw

# Diretórios
images_dir = 'dataset/images'
labels_dir = 'dataset/labels'
output_dir = 'images_with_detections'

# Cria o diretório de saída se não existir
os.makedirs(output_dir, exist_ok=True)

# Lista de imagens
valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(valid_extensions)]
image_files = image_files[:200]  # Limita para 200 imagens

for img_name in image_files:
    img_path = os.path.join(images_dir, img_name)
    label_name = os.path.splitext(img_name)[0] + '.txt'
    label_path = os.path.join(labels_dir, label_name)
    
    # Abre a imagem
    image = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(image)
    w, h = image.size

    # Se existir o label correspondente, desenha as caixas
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                cls, x_center, y_center, width, height = map(float, parts)
                # YOLO: valores normalizados
                x_center *= w
                y_center *= h
                width *= w
                height *= h
                x0 = x_center - width / 2
                y0 = y_center - height / 2
                x1 = x_center + width / 2
                y1 = y_center + height / 2
                draw.rectangle([x0, y0, x1, y1], outline='red', width=2)
                draw.text((x0, y0), str(int(cls)), fill='red')

    # Salva a imagem com as detecções
    out_path = os.path.join(output_dir, img_name)
    image.save(out_path)

print('Processamento concluído!')
