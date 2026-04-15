import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from pathlib import Path
from typing import Optional

from src.config import IMG_SIZE, BATCH_SIZE, NUM_WORKERS, CLASS_NAMES


class BinarySkinLesionDataset(Dataset):
    def __init__(self, image_paths: dict, transform: Optional[transforms.Compose] = None):
        self.image_ids = list(image_paths.keys())
        self.image_paths = image_paths
        self.transform = transform or self._default_transform()
        self.class_to_idx = {name: idx for idx, name in enumerate(CLASS_NAMES)}
    
    def _default_transform(self):
        return transforms.Compose([
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def __len__(self):
        return len(self.image_ids)
    
    def __getitem__(self, idx):
        image_id = self.image_ids[idx]
        info = self.image_paths[image_id]
        
        image = Image.open(info['path']).convert('RGB')
        image = self.transform(image)
        label = self.class_to_idx[info['label']]
        
        return image, label


def create_data_loaders(train_paths: dict, val_paths: dict, test_paths: dict) -> tuple:
    train_dataset = BinarySkinLesionDataset(train_paths)
    val_dataset = BinarySkinLesionDataset(val_paths)
    test_dataset = BinarySkinLesionDataset(test_paths) if test_paths else None
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available()
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available()
    )
    
    test_loader = None
    if test_dataset:
        test_loader = DataLoader(
            test_dataset,
            batch_size=BATCH_SIZE,
            shuffle=False,
            num_workers=NUM_WORKERS,
            pin_memory=torch.cuda.is_available()
        )
    
    return train_loader, val_loader, test_loader
