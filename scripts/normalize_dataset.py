import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List

RAW_CHAPTER_DIR = Path("C:/OpenGita/dataset/raw/chapter")
RAW_SLOK_DIR = Path("C:/OpenGita/dataset/raw/slok")
PROCESSED_DIR = Path("C:/OpenGita/dataset/processed")

def clean_text(text: str) -> str:
    """Normalize whitespace and strip text."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def is_valid_text(text: str) -> bool:
    """Filter out empty text or placeholder 'did not comment' messages."""
    if not text:
        return False
    txt_lower = text.lower()
    if "did not comment" in txt_lower:
        return False
    return True

def tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase alphanumeric words of length > 2."""
    if not text:
        return []
    # Match words (including unicode characters for Hindi/Sanskrit)
    words = re.findall(r'\b\w+\b', text.lower(), re.UNICODE)
    return [w for w in words if len(w) > 2]

def normalize_dataset():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Process Chapters (Sort numerically)
    print("Normalizing chapters...")
    processed_chapters = []
    chapter_files = sorted(
        RAW_CHAPTER_DIR.glob("*.json"),
        key=lambda p: int(re.search(r'\d+', p.name).group())
    )
    
    for fpath in chapter_files:
        with open(fpath, "r", encoding="utf-8") as f:
            raw_ch = json.load(f)
        
        normalized_ch = {
            "number": int(raw_ch["chapter_number"]),
            "verses_count": int(raw_ch["verses_count"]),
            "name": clean_text(raw_ch["name"]),
            "translation": clean_text(raw_ch["translation"]),
            "transliteration": clean_text(raw_ch["transliteration"]),
            "meaning": {
                "en": clean_text(raw_ch["meaning"].get("en", "")),
                "hi": clean_text(raw_ch["meaning"].get("hi", ""))
            },
            "summary": {
                "en": clean_text(raw_ch["summary"].get("en", "")),
                "hi": clean_text(raw_ch["summary"].get("hi", ""))
            }
        }
        processed_chapters.append(normalized_ch)
    
    # 2. Process Verses and Build Search Index
    print("Normalizing verses and indexing...")
    processed_verses = []
    search_index: Dict[str, List[str]] = {}
    
    all_translators = set()
    all_commentators = set()
    languages = {"sa", "en", "hi"}
    
    # Sort slok files by chapter and then by verse
    def get_chapter_verse(p: Path) -> List[int]:
        # Filename format: bhagavadgita_chapter_{ch}_slok_{v}.json
        match = re.findall(r'\d+', p.name)
        return [int(x) for x in match]
        
    slok_files = sorted(RAW_SLOK_DIR.glob("*.json"), key=get_chapter_verse)
    
    for fpath in slok_files:
        with open(fpath, "r", encoding="utf-8") as f:
            raw_slok = json.load(f)
            
        ch_num = int(raw_slok["chapter"])
        v_num = int(raw_slok["verse"])
        verse_id = f"BG{ch_num}.{v_num}"
        
        slok_text = clean_text(raw_slok.get("slok", ""))
        transliteration_text = clean_text(raw_slok.get("transliteration", ""))
        
        translations = []
        commentaries = []
        
        # Scan author entries dynamically
        for key, val in raw_slok.items():
            if isinstance(val, dict) and "author" in val:
                author_name = clean_text(val["author"])
                
                # Check for translations
                if "et" in val:
                    desc = clean_text(val["et"])
                    if is_valid_text(desc):
                        translations.append({
                            "author": author_name,
                            "language": "en",
                            "description": desc
                        })
                        all_translators.add(author_name)
                        
                if "ht" in val:
                    desc = clean_text(val["ht"])
                    if is_valid_text(desc):
                        translations.append({
                            "author": author_name,
                            "language": "hi",
                            "description": desc
                        })
                        all_translators.add(author_name)
                
                # Check for commentaries
                if "ec" in val:
                    desc = clean_text(val["ec"])
                    if is_valid_text(desc):
                        commentaries.append({
                            "author": author_name,
                            "language": "en",
                            "description": desc
                        })
                        all_commentators.add(author_name)
                        
                if "hc" in val:
                    desc = clean_text(val["hc"])
                    if is_valid_text(desc):
                        commentaries.append({
                            "author": author_name,
                            "language": "hi",
                            "description": desc
                        })
                        all_commentators.add(author_name)
                        
                if "sc" in val:
                    desc = clean_text(val["sc"])
                    if is_valid_text(desc):
                        commentaries.append({
                            "author": author_name,
                            "language": "sa",
                            "description": desc
                        })
                        all_commentators.add(author_name)
        
        normalized_verse = {
            "id": verse_id,
            "chapter": ch_num,
            "verse": v_num,
            "slok": slok_text,
            "transliteration": transliteration_text,
            "translations": translations,
            "commentaries": commentaries
        }
        processed_verses.append(normalized_verse)
        
        # Build search index
        # Index slok, transliteration, translations, and commentaries
        text_to_index = [slok_text, transliteration_text]
        for t in translations:
            text_to_index.append(t["description"])
        for c in commentaries:
            text_to_index.append(c["description"])
            
        full_text = " ".join(text_to_index)
        tokens = set(tokenize(full_text))
        for token in tokens:
            search_index.setdefault(token, []).append(verse_id)
            
    # 3. Create Metadata
    # Standard verses (excluding pushpikas/colophons)
    canonical_verses = [v for v in processed_verses if v["verse"] <= next(
        ch["verses_count"] for ch in processed_chapters if ch["number"] == v["chapter"]
    )]
    
    metadata = {
        "total_chapters": len(processed_chapters),
        "total_verses": len(canonical_verses),
        "total_files": len(processed_verses), # includes pushpikas
        "languages": sorted(list(languages)),
        "translators": sorted(list(all_translators)),
        "commentators": sorted(list(all_commentators)),
        "last_processed": datetime.now(timezone.utc).isoformat()
    }
    
    # Save outputs
    print(f"Writing outputs to {PROCESSED_DIR}...")
    with open(PROCESSED_DIR / "chapters.json", "w", encoding="utf-8") as f:
        json.dump(processed_chapters, f, indent=4, ensure_ascii=False)
        
    with open(PROCESSED_DIR / "verses.json", "w", encoding="utf-8") as f:
        json.dump(processed_verses, f, indent=4, ensure_ascii=False)
        
    with open(PROCESSED_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
        
    with open(PROCESSED_DIR / "search_index.json", "w", encoding="utf-8") as f:
        json.dump({"words": search_index}, f, indent=4, ensure_ascii=False)
        
    print("Dataset normalization completed successfully.")

if __name__ == "__main__":
    normalize_dataset()
