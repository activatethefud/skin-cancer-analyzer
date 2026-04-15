import pytest
from src.config import CLASS_NAMES, IMG_SIZE, BATCH_SIZE


class TestConfig:
    def test_class_names_length(self):
        assert len(CLASS_NAMES) == 7
    
    def test_class_names_unique(self):
        assert len(CLASS_NAMES) == len(set(CLASS_NAMES))
    
    def test_class_names_valid(self):
        expected = ['nv', 'mel', 'bkl', 'vasc', 'bcc', 'akiec', 'df']
        assert sorted(CLASS_NAMES) == sorted(expected)
    
    def test_img_size_positive(self):
        assert IMG_SIZE > 0
    
    def test_batch_size_positive(self):
        assert BATCH_SIZE > 0
