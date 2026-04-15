import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestDataset:
    def test_class_to_idx_mapping(self):
        from src.dataset import SkinLesionDataset
        from src.config import CLASS_NAMES
        
        mock_paths = {
            'img1': {
                'path': '/fake/path/img1.jpg',
                'lesion_type': 'nv',
                'dx_type': 'CONFOCAL',
                'age': 50,
                'sex': 'male',
                'localization': 'back'
            }
        }
        
        with patch('PIL.Image.Image.convert', return_value=MagicMock()):
            dataset = SkinLesionDataset(mock_paths)
        
        assert dataset.class_to_idx['nv'] == 0
        assert dataset.class_to_idx['mel'] == 1
    
    def test_dataset_length(self):
        from src.dataset import SkinLesionDataset
        
        mock_paths = {
            f'img{i}': {
                'path': f'/fake/path/img{i}.jpg',
                'lesion_type': 'nv',
                'dx_type': 'CONFOCAL',
                'age': 50,
                'sex': 'male',
                'localization': 'back'
            }
            for i in range(5)
        }
        
        with patch('PIL.Image.Image.convert', return_value=MagicMock()):
            dataset = SkinLesionDataset(mock_paths)
        
        assert len(dataset) == 5
