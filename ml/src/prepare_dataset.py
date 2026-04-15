import os
from pathlib import Path
from tqdm import tqdm
from datasets import load_dataset
from PIL import Image
import io

from src.config import DATA_DIR, HF_DATASET, IMG_SIZE


def download_hf_dataset(data_dir: str = DATA_DIR) -> dict:
    data_path = Path(data_dir)
    
    if data_path.exists() and (data_path / "train").exists() and (data_path / "test").exists():
        print(f"Dataset already exists at {data_dir}")
        return load_local_metadata(data_dir)
    
    print(f"Downloading dataset from HuggingFace: {HF_DATASET}")
    
    dataset = load_dataset(HF_DATASET, split="train")
    
    train_dir = data_path / "train"
    test_dir = data_path / "test"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Dataset loaded with {len(dataset)} samples")
    
    total = len(dataset)
    for idx, example in enumerate(tqdm(dataset, desc="Downloading images")):
        image = example['image']
        label = example['label']
        
        class_dir = train_dir / str(label)
        class_dir.mkdir(exist_ok=True)
        
        img_filename = f"image_{idx:05d}.jpg"
        img_path = class_dir / img_filename
        
        if isinstance(image, Image.Image):
            image.save(img_path, "JPEG")
        else:
            img = Image.open(io.BytesIO(image))
            img.save(img_path, "JPEG")
    
    metadata = {
        'train': [],
        'test': []
    }
    
    for label_dir in train_dir.iterdir():
        if label_dir.is_dir():
            label_name = label_dir.name
            for img_file in label_dir.glob("*.jpg"):
                metadata['train'].append({
                    'path': str(img_file),
                    'label': label_name
                })
    
    metadata_path = data_path / "metadata.json"
    import json
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)
    
    print(f"Downloaded {len(metadata['train'])} images to {data_dir}")
    return metadata


def load_local_metadata(data_dir: str = DATA_DIR) -> dict:
    import json
    metadata_path = Path(data_dir) / "metadata.json"
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return {'train': [], 'test': []}


def get_image_paths(data_dir: str = DATA_DIR) -> dict:
    data_path = Path(data_dir)
    image_paths = {}
    
    for split in ['train', 'test']:
        split_dir = data_path / split
        if not split_dir.exists():
            continue
        
        for class_dir in split_dir.iterdir():
            if class_dir.is_dir():
                label = class_dir.name
                for img_file in class_dir.glob("*.jpg"):
                    image_paths[img_file.stem] = {
                        'path': str(img_file),
                        'label': label,
                        'split': split
                    }
    
    return image_paths


if __name__ == "__main__":
    metadata = download_hf_dataset()
    print(f"Dataset prepared with {len(metadata.get('train', []))} training images")
