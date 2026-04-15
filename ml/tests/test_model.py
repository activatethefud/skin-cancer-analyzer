import pytest
from unittest.mock import patch, MagicMock
import torch


class TestModel:
    @pytest.fixture
    def mock_torch(self):
        with patch('torch.cuda.is_available', return_value=False):
            yield
    
    def test_model_output_shape(self, mock_torch):
        from src.model import SkinCancerClassifier
        
        model = SkinCancerClassifier(num_classes=7, pretrained=False)
        model.eval()
        
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
        
        assert output.shape == (1, 7)
    
    def test_model_prediction_range(self, mock_torch):
        from src.model import SkinCancerClassifier
        
        model = SkinCancerClassifier(num_classes=7, pretrained=False)
        model.eval()
        
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
            probs = torch.softmax(output, dim=1)
        
        assert probs.sum().item() == pytest.approx(1.0, rel=1e-5)
        assert (probs >= 0).all()
        assert (probs <= 1).all()
