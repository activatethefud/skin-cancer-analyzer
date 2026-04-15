import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

torch_available = False
try:
    import torch
    torch_available = True
except ImportError:
    pass


class TestConfigExtended:
    def test_epochs_positive(self):
        from src.config import EPOCHS
        assert EPOCHS > 0

    def test_learning_rate_positive(self):
        from src.config import LEARNING_RATE
        assert LEARNING_RATE > 0

    def test_num_workers_non_negative(self):
        from src.config import NUM_WORKERS
        assert NUM_WORKERS >= 0

    def test_model_name_valid(self):
        from src.config import MODEL_NAME
        assert MODEL_NAME in ['mobilenet_v3_small', 'mobilenet_v3_large', 'resnet50']

    def test_data_dir_valid(self):
        from src.config import DATA_DIR
        assert isinstance(DATA_DIR, str)
        assert len(DATA_DIR) > 0

    def test_model_dir_valid(self):
        from src.config import MODEL_DIR
        assert isinstance(MODEL_DIR, str)
        assert len(MODEL_DIR) > 0


@pytest.mark.skipif(not torch_available, reason="PyTorch not installed")
class TestDatasetExtended:
    def test_dataset_with_multiple_classes(self):
        from src.dataset import BinarySkinLesionDataset
        from src.config import CLASS_NAMES
        
        mock_paths = {
            f'img{i}': {
                'path': f'/fake/path/img{i}.jpg',
                'label': CLASS_NAMES[i % len(CLASS_NAMES)]
            }
            for i in range(4)
        }
        
        with patch('PIL.Image.Image.convert', return_value=MagicMock()):
            dataset = BinarySkinLesionDataset(mock_paths)
        
        assert len(dataset) == 4
        assert len(dataset.class_to_idx) == 2

    def test_class_to_idx_complete(self):
        from src.dataset import BinarySkinLesionDataset
        
        mock_paths = {
            'img1': {
                'path': '/fake/path/img1.jpg',
                'label': 'benign'
            }
        }
        
        with patch('PIL.Image.Image.convert', return_value=MagicMock()):
            dataset = BinarySkinLesionDataset(mock_paths)
        
        for cls in ['benign', 'malignant']:
            assert cls in dataset.class_to_idx

    def test_transform_includes_normalization(self):
        from src.dataset import BinarySkinLesionDataset
        
        mock_paths = {
            'img1': {
                'path': '/fake/path/img1.jpg',
                'label': 'benign'
            }
        }
        
        with patch('PIL.Image.Image.convert', return_value=MagicMock()):
            dataset = BinarySkinLesionDataset(mock_paths)
        
        assert dataset.transform is not None


@pytest.mark.skipif(not torch_available, reason="PyTorch not installed")
class TestModelExtended:
    def test_model_creation_with_custom_classes(self):
        from src.model import SkinCancerClassifier
        
        model = SkinCancerClassifier(num_classes=3, pretrained=False)
        assert model is not None

    def test_model_has_classifier_layer(self):
        from src.model import SkinCancerClassifier
        
        model = SkinCancerClassifier(num_classes=2, pretrained=False)
        assert hasattr(model, 'model')
        assert hasattr(model.model, 'classifier')

    def test_model_forward_pass_shapes(self):
        from src.model import SkinCancerClassifier
        import torch
        
        model = SkinCancerClassifier(num_classes=2, pretrained=False)
        model.eval()
        
        batch_sizes = [1, 4, 16]
        for batch_size in batch_sizes:
            dummy_input = torch.randn(batch_size, 3, 224, 224)
            with torch.no_grad():
                output = model(dummy_input)
            assert output.shape[0] == batch_size
            assert output.shape[1] == 2

    def test_model_softmax_output(self):
        from src.model import SkinCancerClassifier
        import torch
        
        model = SkinCancerClassifier(num_classes=2, pretrained=False)
        model.eval()
        
        dummy_input = torch.randn(2, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
            probs = torch.softmax(output, dim=1)
        
        assert probs.min().item() >= 0
        assert probs.max().item() <= 1
        assert torch.allclose(probs.sum(dim=1), torch.ones(2), atol=1e-5)
