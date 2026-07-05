import json
import sys
from pathlib import Path

PROCESSED_DIR = Path("C:/OpenGita/dataset/processed")

def validate_dataset():
    errors = []
    
    # 1. Check folder existence
    if not PROCESSED_DIR.exists():
        print(f"Error: Processed directory {PROCESSED_DIR} does not exist.")
        sys.exit(1)
        
    # Check all four required files exist
    required_files = ["chapters.json", "verses.json", "metadata.json", "search_index.json"]
    for fname in required_files:
        fpath = PROCESSED_DIR / fname
        if not fpath.exists():
            errors.append(f"Missing processed file: {fname}")
            
    if errors:
        for err in errors:
            print(f"Validation Error: {err}")
        sys.exit(1)
        
    # 2. Validate chapters
    print("Validating chapters.json...")
    with open(PROCESSED_DIR / "chapters.json", "r", encoding="utf-8") as f:
        chapters = json.load(f)
        
    if not isinstance(chapters, list):
        errors.append("chapters.json must contain a list of chapters.")
    else:
        if len(chapters) != 18:
            errors.append(f"Expected 18 chapters, found {len(chapters)}")
            
        total_declared_verses = 0
        for i, ch in enumerate(chapters, 1):
            ch_num = ch.get("number")
            if ch_num != i:
                errors.append(f"Chapter at index {i-1} has incorrect number: {ch_num}")
            
            verses_count = ch.get("verses_count")
            if not isinstance(verses_count, int) or verses_count <= 0:
                errors.append(f"Chapter {i} has invalid verses_count: {verses_count}")
            else:
                total_declared_verses += verses_count
                
            # Verify translation, transliteration, meaning, summary are present
            for field in ["name", "translation", "transliteration", "meaning", "summary"]:
                if field not in ch:
                    errors.append(f"Chapter {i} is missing field: {field}")
                    
        if total_declared_verses != 701:
            errors.append(f"Expected sum of verses_count across all chapters to be 701, found {total_declared_verses}")

    # 3. Validate verses
    print("Validating verses.json...")
    with open(PROCESSED_DIR / "verses.json", "r", encoding="utf-8") as f:
        verses = json.load(f)
        
    if not isinstance(verses, list):
        errors.append("verses.json must contain a list of verses.")
    else:
        # 701 canonical + 18 pushpikas = 719 total entries
        if len(verses) != 719:
            errors.append(f"Expected 719 total verse entries (701 canonical + 18 pushpikas), found {len(verses)}")
            
        for v in verses:
            vid = v.get("id")
            ch = v.get("chapter")
            v_num = v.get("verse")
            
            if not vid or not vid.startswith("BG"):
                errors.append(f"Verse has invalid ID: {vid}")
            if not isinstance(ch, int) or ch < 1 or ch > 18:
                errors.append(f"Verse {vid} has invalid chapter number: {ch}")
            if not isinstance(v_num, int) or v_num < 1:
                errors.append(f"Verse {vid} has invalid verse number: {v_num}")
                
            # Check for translation and commentary fields
            if "translations" not in v or not isinstance(v["translations"], list):
                errors.append(f"Verse {vid} is missing 'translations' list.")
            if "commentaries" not in v or not isinstance(v["commentaries"], list):
                errors.append(f"Verse {vid} is missing 'commentaries' list.")

    # 4. Validate metadata
    print("Validating metadata.json...")
    with open(PROCESSED_DIR / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
        
    for field in ["total_chapters", "total_verses", "total_files", "languages", "translators", "commentators", "last_processed"]:
        if field not in metadata:
            errors.append(f"metadata.json is missing field: {field}")
            
    if metadata.get("total_chapters") != 18:
        errors.append(f"Metadata total_chapters must be 18, found {metadata.get('total_chapters')}")
    if metadata.get("total_verses") != 701:
        errors.append(f"Metadata total_verses must be 701, found {metadata.get('total_verses')}")
    if metadata.get("total_files") != 719:
        errors.append(f"Metadata total_files must be 719, found {metadata.get('total_files')}")

    # 5. Validate search_index
    print("Validating search_index.json...")
    with open(PROCESSED_DIR / "search_index.json", "r", encoding="utf-8") as f:
        index = json.load(f)
        
    if "words" not in index or not isinstance(index["words"], dict):
        errors.append("search_index.json must contain a 'words' object.")
    else:
        words_count = len(index["words"])
        if words_count == 0:
            errors.append("search_index.json 'words' dictionary is empty.")
        else:
            print(f"Search index contains {words_count} unique indexed tokens.")
            # Verify sample entry is correct
            sample_key = next(iter(index["words"].keys()))
            if not isinstance(index["words"][sample_key], list):
                errors.append(f"Index values must be lists of verse IDs. Key '{sample_key}' is invalid.")

    # Output results
    if errors:
        print("\n--- DATASET VALIDATION FAILED ---")
        for err in errors:
            print(f"Validation Error: {err}")
        sys.exit(1)
    else:
        print("\n--- DATASET VALIDATION SUCCESSFUL ---")
        print("All schema, key, and value integrity checks passed.")

if __name__ == "__main__":
    validate_dataset()
