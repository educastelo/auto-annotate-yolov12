# auto-annotate-yolov12

Projeto de anotação automática de datasets usando YOLO v12 para detecção de veículos e pessoas.

## Estrutura do Projeto

```
auto-annotate-yolov12/
├── dataset/
│   ├── images/              # Imagens do dataset
│   └── labels/              # Anotações em formato YOLO
│       └── classes.txt      # Lista de classes (person, bicycle, car, motorbike, bus, truck)
├── models/
│   └── yolo12x.pt          # Modelo YOLO v12
├── labelimg-custom/         # Versão customizada do labelImg
│   ├── README.md           # Documentação das customizações
│   ├── CHANGELOG.md        # Histórico de mudanças
│   └── run_labelimg.sh     # Script para executar o labelImg
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
Script principal para anotação automática de imagens usando YOLO v12.

### `count_classes.py`
Conta quantas anotações de cada classe existem no dataset.

### `save_images_with_detections.py`
Salva imagens com as detecções desenhadas para visualização.

### `split_dataset.py`
Divide o dataset em conjuntos de treino, validação e teste.

## labelImg Customizado

Este projeto inclui uma versão customizada do [labelImg](https://github.com/HumanSignal/labelImg) com correções para compatibilidade com PyQt5/PyQt6 mais recentes.

### Como usar o labelImg customizado

```bash
# Usando o script de execução
./labelimg-custom/run_labelimg.sh dataset/images dataset/labels/classes.txt

# Ou diretamente com Python
python labelimg-custom/labelImg/labelImg.py dataset/images dataset/labels/classes.txt
```

Para mais detalhes sobre as customizações, consulte [labelimg-custom/README.md](labelimg-custom/README.md).

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

### Verificar anotações com labelImg

```bash
./labelimg-custom/run_labelimg.sh dataset/images dataset/labels/classes.txt
```

### Contar classes no dataset

```bash
python count_classes.py
```

## Configuração YOLO

O projeto usa o modelo YOLO v12 (yolo12x.pt) para detecção automática. As detecções são filtradas para incluir apenas as 6 classes de interesse (person, bicycle, car, motorbike, bus, truck).