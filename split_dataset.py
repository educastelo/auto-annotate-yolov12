import os
import shutil
import zipfile
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
        
        # Cria o arquivo classes.txt no diretório do lote
        classes_file = os.path.join(batch_dir, 'classes.txt')
        classes_content = 'person\nbicycle\ncar\nmotorbike\nbus\ntruck\n'
        with open(classes_file, 'w') as f:
            f.write(classes_content)
        
        # Cria o arquivo ZIP do lote
        zip_path = os.path.join(base_dir, f'dataset_batch_{batch_num + 1}.zip')
        print(f'Criando arquivo ZIP para o lote {batch_num + 1}...')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Adiciona todos os arquivos do diretório do lote ao ZIP
            for root, dirs, files in os.walk(batch_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calcula o caminho relativo dentro do ZIP
                    arcname = os.path.relpath(file_path, batch_dir)
                    zipf.write(file_path, arcname)
        
        print(f'Lote {batch_num + 1} concluído: {len(batch_images)} imagens processadas e zipado em {zip_path}')

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    create_batch_directories(base_dir)
    print('\nDivisão do dataset concluída!') 