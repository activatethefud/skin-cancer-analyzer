import torch
import numpy as np
import json
from pathlib import Path

from src.model import SkinCancerClassifier
from src.config import CLASS_NAMES, MODEL_DIR


def export_model(
    model_path: str = f"{MODEL_DIR}/best_model.pth",
    output_path: str = "../backend/models/skin_cancer_model.pth",
    class_names: list = CLASS_NAMES
):
    model = SkinCancerClassifier(num_classes=len(class_names), pretrained=False)
    state_dict = torch.load(model_path, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    
    inner_state_dict = model.model.state_dict()
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        'model_state_dict': inner_state_dict,
        'class_names': class_names,
        'num_classes': len(class_names)
    }, output_path)
    
    print(f"Model exported to {output_path}")
    
    metadata = {
        'class_names': class_names,
        'num_classes': len(class_names),
        'model_type': 'mobilenet_v3_small'
    }
    metadata_path = output_path.replace('.pth', '_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata exported to {metadata_path}")


if __name__ == "__main__":
    export_model()
