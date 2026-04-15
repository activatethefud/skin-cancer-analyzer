import torch
import torch.nn as nn
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import os
from pathlib import Path

from src.model import SkinCancerClassifier
from src.dataset import SkinLesionDataset, create_data_loaders
from src.config import (
    CLASS_NAMES, EPOCHS, LEARNING_RATE, 
    MODEL_DIR, DATA_DIR, BATCH_SIZE
)


def train_epoch(model: nn.Module, train_loader, criterion, optimizer, device: str) -> float:
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for images, labels in tqdm(train_loader, desc="Training"):
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    return running_loss / len(train_loader), 100 * correct / total


def validate(model: nn.Module, val_loader, criterion, device: str) -> tuple:
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc="Validating"):
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    return running_loss / len(val_loader), 100 * correct / total


def train(
    train_paths: dict,
    val_paths: dict,
    epochs: int = EPOCHS,
    device: str = 'cpu'
) -> SkinCancerClassifier:
    train_loader, val_loader, _ = create_data_loaders(train_paths, val_paths, {})
    
    model = SkinCancerClassifier(num_classes=len(CLASS_NAMES), pretrained=True)
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=2)
    
    best_val_acc = 0.0
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    
    for epoch in range(epochs):
        print(f"\nEpoch {epoch+1}/{epochs}")
        
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        scheduler.step(val_loss)
        
        print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            model_path = os.path.join(MODEL_DIR, 'best_model.pth')
            torch.save(model.state_dict(), model_path)
            print(f"Saved best model with val acc: {val_acc:.2f}%")
    
    return model


if __name__ == "__main__":
    from prepare_dataset import organize_by_metadata
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Training on {device}")
    
    image_paths = organize_by_metadata(DATA_DIR)
    
    train_paths, temp_paths = train_test_split(
        list(image_paths.keys()), 
        test_size=0.2, 
        random_state=42
    )
    val_paths, test_paths = train_test_split(
        temp_paths, 
        test_size=0.5, 
        random_state=42
    )
    
    train_dict = {k: image_paths[k] for k in train_paths}
    val_dict = {k: image_paths[k] for k in val_paths}
    test_dict = {k: image_paths[k] for k in test_paths}
    
    model = train(train_dict, val_dict, epochs=EPOCHS, device=device)
    
    print("Training complete!")
