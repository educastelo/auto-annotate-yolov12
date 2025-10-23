from ultralytics import YOLO
import os
import gc
import torch

# Mapeamento das classes originais para as novas
# Original YOLO -> Novo ID
CLASS_MAPPING = {
    0: 0,  # person -> person
    1: 1,  # bicycle -> bicycle
    2: 2,  # car -> car
    3: 3,  # motorbike -> motorbike
    5: 4,  # bus -> bus
    7: 5,  # truck -> truck
}

def remap_label_file(label_path):
    """Remapeia os IDs das classes em um arquivo de label."""
    if not os.path.exists(label_path):
        return
    
    # Lê o arquivo original
    with open(label_path, 'r') as f:
        lines = f.readlines()
    
    # Remapeia as classes
    new_lines = []
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split()
            old_class_id = int(parts[0])
            
            # Remapeia o ID da classe
            if old_class_id in CLASS_MAPPING:
                new_class_id = CLASS_MAPPING[old_class_id]
                parts[0] = str(new_class_id)
                new_lines.append(' '.join(parts) + '\n')
    
    # Salva o arquivo remapeado
    with open(label_path, 'w') as f:
        f.writelines(new_lines)

def process_images_one_by_one(path):
    model = YOLO('models/yolo12x.pt')
    
    # Obtém lista de todas as imagens no diretório
    image_files = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(valid_extensions):
                image_files.append(os.path.join(root, file))
    
    # Processa as imagens uma por uma
    for i, image_file in enumerate(image_files, 1):
        if i % 100 == 0:
            print(f'Processando imagem {i} de {len(image_files)}')
        
        try:
            # Processa uma única imagem
            results = model.predict(image_file, save_txt=True, classes=[0, 1, 2, 3, 5, 7], conf=0.1)
            
            # Encontra o arquivo de label gerado e remapeia as classes
            # O YOLO geralmente salva em runs/detect/predictX/labels/
            if results and len(results) > 0:
                # Pega o caminho onde o YOLO salvou o resultado
                save_dir = results[0].save_dir
                if save_dir:
                    # Constrói o caminho do arquivo de label
                    image_name = os.path.splitext(os.path.basename(image_file))[0]
                    label_path = os.path.join(save_dir, 'labels', f'{image_name}.txt')
                    
                    # Remapeia as classes no arquivo
                    remap_label_file(label_path)
            
            # Limpa a memória CUDA
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
        except Exception as e:
            print(f'Erro ao processar imagem {image_file}: {str(e)}')
            continue
        
        # A cada 1000 imagens, recarrega o modelo para evitar acúmulo de memória
        if i % 1000 == 0:
            del model
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            model = YOLO('models/yolo12x.pt')
    
    print('Processamento concluído!')

# Executa o processamento
path = 'dataset'
process_images_one_by_one(path)