import shutil
from pathlib import Path

PROCESSED_DIR = Path("C:/OpenGita/dataset/processed")
PACKAGE_DATA_DIR = Path("C:/OpenGita/packages/python/opengita/data")

def package_data():
    if not PROCESSED_DIR.exists():
        print(f"Error: Processed dataset directory {PROCESSED_DIR} does not exist. Run normalize_dataset.py first.")
        return
        
    PACKAGE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    required_files = ["chapters.json", "verses.json", "metadata.json", "search_index.json"]
    print(f"Packaging dataset files into {PACKAGE_DATA_DIR}...")
    
    for fname in required_files:
        src = PROCESSED_DIR / fname
        dest = PACKAGE_DATA_DIR / fname
        
        if not src.exists():
            print(f"Error: Source file {src} is missing.")
            continue
            
        print(f"Copying {fname}...")
        shutil.copy2(src, dest)
        
    print("Dataset successfully packaged inside the opengita library.")

if __name__ == "__main__":
    package_data()
