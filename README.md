# auto-annotate-yolov12

Projeto de anotação automática de datasets usando YOLO v12 para detecção de veículos e pessoas.

## Estrutura do Projeto

```
auto-annotate-yolov12/
├── dataset/
│   ├── images/              # Imagens do dataset
│   └── labels/              # Anotações em formato YOLO
├── models/
│   └── yolo12x.pt          # Modelo YOLO v12
├── images_with_detections/  # Imagens com detecções visualizadas
├── label.py                 # Script de anotação automática
├── count_classes.py         # Contador de classes no dataset
├── save_images_with_detections.py  # Salva imagens com detecções visualizadas
├── split_dataset.py         # Divide dataset em train/val/test
└── requirements.txt         # Dependências do projeto
```

## Classes Detectadas

0. **person** - Pessoas
1. **bicycle** - Bicicletas
2. **car** - Carros
3. **motorbike** - Motos
4. **bus** - Ônibus
5. **truck** - Caminhões

## Scripts Disponíveis

### `label.py`
Script principal para anotação automática de imagens usando YOLO v12. Processa todas as imagens do diretório `dataset/images/` e salva as anotações em formato YOLO no diretório `dataset/labels/`. Aplica automaticamente o remapeamento de classes conforme definido no código.

### `count_classes.py`
Conta quantas anotações de cada classe existem no dataset.

### `save_images_with_detections.py`
Salva imagens com as detecções desenhadas para visualização.

### `split_dataset.py`
Divide o dataset em lotes de 1000 imagens e suas respectivas anotações. Cada lote é criado em um diretório separado (`dataset_batch_1`, `dataset_batch_2`, etc.) contendo:
- `images/` - Imagens do lote
- `labels/` - Anotações correspondentes em formato YOLO
- `classes.txt` - Arquivo com a lista de classes

Cada diretório de lote é automaticamente compactado em um arquivo ZIP separado (`dataset_batch_1.zip`, `dataset_batch_2.zip`, etc.).

## Instalação

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## Uso

### Anotar novas imagens

```bash
python label.py
```

### Contar classes no dataset

```bash
python count_classes.py
```

### Dividir dataset em lotes

```bash
python split_dataset.py
```

Este script divide o dataset em lotes de 1000 imagens, cria a estrutura de diretórios necessária e gera arquivos ZIP para cada lote.

## Configuração YOLO

O projeto usa o modelo YOLO v12 (yolo12x.pt) para detecção automática. As detecções são filtradas para incluir apenas as 6 classes de interesse (person, bicycle, car, motorbike, bus, truck).