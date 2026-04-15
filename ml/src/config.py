CLASS_NAMES = ['benign', 'malignant']

CLASS_LABELS = {
    'benign': 'Benign lesion',
    'malignant': 'Malignant lesion',
}

IMG_SIZE = 224
BATCH_SIZE = 32
NUM_WORKERS = 4
EPOCHS = 10
LEARNING_RATE = 0.001
MODEL_NAME = 'mobilenet_v3_small'

DATA_DIR = 'data/skin_lesion_binary'
MODEL_DIR = 'models'

HF_DATASET = 'preetsojitra/binary-2K-samples-skin-lesion-HM10000'
