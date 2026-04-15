CLASS_NAMES = ['nv', 'mel', 'bkl', 'vasc', 'bcc', 'akiec', 'df']

CLASS_LABELS = {
    'nv': 'Melanocytic nevi (benign)',
    'mel': 'Melanoma (malignant)',
    'bkl': 'Benign keratosis',
    'vasc': 'Vascular lesions',
    'bcc': 'Basal cell carcinoma',
    'akiec': 'Actinic keratoses',
    'df': 'Dermatofibroma',
}

IMG_SIZE = 224
BATCH_SIZE = 32
NUM_WORKERS = 4
EPOCHS = 10
LEARNING_RATE = 0.001
MODEL_NAME = 'mobilenet_v3_small'

DATA_DIR = 'data/HAM10000'
MODEL_DIR = 'models'
