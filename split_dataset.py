import os
import shutil
from pathlib import Path

def create_batch_directories(base_dir, batch_size=1000):
    # Diretórios de origem
    images_dir = os.path.join(base_dir, 'dataset/images')
    labels_dir = os.path.join(base_dir, 'dataset/labels')
    
    # Lista todas as imagens
    image_files = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    for file in os.listdir(images_dir):
        if file.lower().endswith(valid_extensions):
            image_files.append(file)
    
    # Calcula número de lotes
    total_images = len(image_files)
    num_batches = (total_images + batch_size - 1) // batch_size
    
    print(f'Total de imagens: {total_images}')
    print(f'Número de lotes: {num_batches}')
    
    # Cria e preenche os lotes
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, total_images)
        batch_images = image_files[start_idx:end_idx]
        
        # Cria diretório do lote
        batch_dir = os.path.join(base_dir, f'dataset_batch_{batch_num + 1}')
        batch_images_dir = os.path.join(batch_dir, 'images')
        batch_labels_dir = os.path.join(batch_dir, 'labels')
        
        os.makedirs(batch_images_dir, exist_ok=True)
        os.makedirs(batch_labels_dir, exist_ok=True)
        
        print(f'\nProcessando lote {batch_num + 1}:')
        print(f'Imagens {start_idx + 1} até {end_idx}')
        
        # Copia imagens e labels
        for img_name in batch_images:
            # Copia imagem
            src_img = os.path.join(images_dir, img_name)
            dst_img = os.path.join(batch_images_dir, img_name)
            shutil.copy2(src_img, dst_img)
            
            # Copia label se existir
            label_name = os.path.splitext(img_name)[0] + '.txt'
            src_label = os.path.join(labels_dir, label_name)
            if os.path.exists(src_label):
                dst_label = os.path.join(batch_labels_dir, label_name)
                shutil.copy2(src_label, dst_label)
        
        print(f'Lote {batch_num + 1} concluído: {len(batch_images)} imagens processadas')

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    create_batch_directories(base_dir)
    print('\nDivisão do dataset concluída!') 