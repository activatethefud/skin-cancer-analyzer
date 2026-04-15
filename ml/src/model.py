import torch
import torch.nn as nn
from torchvision import models


class SkinCancerClassifier(nn.Module):
    def __init__(self, num_classes: int = 7, pretrained: bool = True):
        super().__init__()
        self.model = models.mobilenet_v3_small(weights='IMAGENET1K_V1' if pretrained else None)
        
        in_features = self.model.classifier[-1].in_features
        self.model.classifier[-1] = nn.Linear(in_features, num_classes)
    
    def forward(self, x):
        return self.model(x)


def load_model(model_path: str, num_classes: int = 7, device: str = 'cpu') -> SkinCancerClassifier:
    model = SkinCancerClassifier(num_classes=num_classes, pretrained=False)
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


def predict(model: SkinCancerClassifier, image_tensor: torch.Tensor, device: str = 'cpu') -> tuple:
    model.eval()
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    return predicted.item(), confidence.item(), probabilities[0].cpu().numpy()
