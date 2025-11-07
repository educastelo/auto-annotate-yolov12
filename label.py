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

def process_images_one_by_one(path):
    model = YOLO('models/yolo12x.pt')
    
    # Cria o diretório labels se não existir
    labels_dir = 'dataset/labels'
    os.makedirs(labels_dir, exist_ok=True)
    
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
            # Processa uma única imagem (sem salvar automaticamente)
            results = model.predict(image_file, save=False, classes=[0, 1, 2, 3, 5, 7], conf=0.3)
            
            # Processa os resultados e salva no diretório labels
            if results and len(results) > 0:
                result = results[0]
                image_name = os.path.splitext(os.path.basename(image_file))[0]
                label_path = os.path.join(labels_dir, f'{image_name}.txt')
                
                # Extrai as detecções e salva no formato YOLO
                detections = []
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        # Obtém o ID da classe original
                        old_class_id = int(box.cls.item())
                        
                        # Remapeia o ID da classe
                        if old_class_id in CLASS_MAPPING:
                            new_class_id = CLASS_MAPPING[old_class_id]
                            
                            # Converte as coordenadas para o formato YOLO (normalizadas)
                            # box.xywhn retorna [x_center, y_center, width, height] normalizados
                            xywhn = box.xywhn[0].cpu().numpy()
                            x_center, y_center, width, height = xywhn
                            
                            # Formata a linha no formato YOLO: class_id x_center y_center width height
                            detections.append(f'{new_class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')
                
                # Salva o arquivo de label
                with open(label_path, 'w') as f:
                    f.writelines(detections)
            
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