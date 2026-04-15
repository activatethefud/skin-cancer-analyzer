import os
import zipfile
import kagglehub
from pathlib import Path
import shutil
from tqdm import tqdm


def download_ham10000(data_dir: str = "data/HAM10000") -> str:
    data_path = Path(data_dir)
    if data_path.exists() and (data_path / "HAM10000_images_part_1").exists():
        print(f"Dataset already exists at {data_dir}")
        return str(data_path)
    
    print("Downloading HAM10000 dataset from Kaggle...")
    path = kagglehub.dataset_download("kmader/skin-cancer-mnist-ham10000")
    
    os.makedirs(data_dir, exist_ok=True)
    
    for item in os.listdir(path):
        src = os.path.join(path, item)
        dst = os.path.join(data_dir, item)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
        elif os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
    
    print(f"Dataset downloaded to {data_dir}")
    return str(data_path)


def organize_by_metadata(data_dir: str = "data/HAM10000", metadata_file: str = "HAM10000_metadata.csv") -> dict:
    import pandas as pd
    
    metadata_path = os.path.join(data_dir, metadata_file)
    df = pd.read_csv(metadata_path)
    
    image_paths = {}
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Organizing images"):
        image_id = row['image_id']
        lesion_type = row['dx']
        
        for part in ['HAM10000_images_part_1', 'HAM10000_images_part_2']:
            img_path = os.path.join(data_dir, part, f"{image_id}.jpg")
            if os.path.exists(img_path):
                image_paths[image_id] = {
                    'path': img_path,
                    'lesion_type': lesion_type,
                    'dx_type': row['dx_type'],
                    'age': row['age'],
                    'sex': row['sex'],
                    'localization': row['localization']
                }
                break
    
    return image_paths


if __name__ == "__main__":
    data_dir = download_ham10000()
    image_paths = organize_by_metadata(data_dir)
    print(f"Organized {len(image_paths)} images")
