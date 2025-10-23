import os
from collections import Counter

# Diretório com os arquivos de labels
labels_dir = "dataset/labels"

# Contador para as classes
class_counter = Counter()
# Dicionário para rastrear arquivos com classes textuais
text_class_files = {}

# Percorrer todos os arquivos .txt no diretório
for filename in os.listdir(labels_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(labels_dir, filename)
        
        # Ler o arquivo e extrair as classes
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Ignorar linhas vazias
                    # O primeiro valor é a classe
                    class_id = line.split()[0]
                    # Tentar converter para int, se não conseguir, manter como string
                    try:
                        class_id = int(class_id)
                    except ValueError:
                        # É uma classe textual
                        if class_id not in text_class_files:
                            text_class_files[class_id] = []
                        if filename not in text_class_files[class_id]:
                            text_class_files[class_id].append(filename)
                    class_counter[class_id] += 1

# Imprimir os resultados
print("Classes encontradas nos arquivos:")
print("-" * 40)
# Ordenar: números primeiro, depois strings
sorted_classes = sorted(class_counter.keys(), key=lambda x: (isinstance(x, str), x))
for class_id in sorted_classes:
    print(f"Classe {class_id}: {class_counter[class_id]} vezes")

print("-" * 40)
print(f"Total de anotações: {sum(class_counter.values())}")
print(f"Total de classes diferentes: {len(class_counter)}")

# Mostrar arquivos com classes textuais
if text_class_files:
    print("\n" + "=" * 40)
    print("Arquivos com classes textuais:")
    print("=" * 40)
    for class_name, files in sorted(text_class_files.items()):
        print(f"\nClasse '{class_name}':")
        for file in files:
            print(f"  - {file}")

