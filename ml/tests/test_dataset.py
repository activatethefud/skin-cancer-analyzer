import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

torch_available = False
try:
    import torch
    torch_available = True
except ImportError:
    pytest.skip("PyTorch not installed", allow_module_level=True)


class TestDataset:
    def test_class_to_idx_mapping(self):
        from src.dataset import BinarySkinLesionDataset
        from src.config import CLASS_NAMES
        
        mock_paths = {
            'img1': {
                'path': '/fake/path/img1.jpg',
                'label': 'benign'
            }
        }
        
        with patch('PIL.Image.Image.convert', return_value=MagicMock()):
            dataset = BinarySkinLesionDataset(mock_paths)
        
        assert dataset.class_to_idx['benign'] == 0
        assert dataset.class_to_idx['malignant'] == 1
    
    def test_dataset_length(self):
        from src.dataset import BinarySkinLesionDataset
        
        mock_paths = {
            f'img{i}': {
                'path': f'/fake/path/img{i}.jpg',
                'label': 'benign'
            }
            for i in range(5)
        }
        
        with patch('PIL.Image.Image.convert', return_value=MagicMock()):
            dataset = BinarySkinLesionDataset(mock_paths)
        
        assert len(dataset) == 5
