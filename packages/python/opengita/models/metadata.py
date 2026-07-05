from typing import List
from pydantic import BaseModel, Field

class Metadata(BaseModel):
    """Pydantic model representing processed dataset metadata."""
    total_chapters: int = Field(..., description="Total number of chapters.")
    total_verses: int = Field(..., description="Total number of canonical verses.")
    total_files: int = Field(..., description="Total records including pushpikas.")
    languages: List[str] = Field(..., description="Supported languages (e.g. ['sa', 'en', 'hi']).")
    translators: List[str] = Field(..., description="List of translators in the dataset.")
    commentators: List[str] = Field(..., description="List of commentators in the dataset.")
    last_processed: str = Field(..., description="UTC timestamp of processing completion.")

class GitaStatistics(BaseModel):
    """Pydantic model representing SDK statistics exposed to developers."""
    total_chapters: int = Field(..., description="Total chapters in Gita.")
    total_verses: int = Field(..., description="Total canonical verses in Gita.")
    total_files: int = Field(..., description="Total database file records (including pushpikas).")
    languages: List[str] = Field(..., description="Supported translation/commentary languages.")
    translators_count: int = Field(..., description="Number of distinct translators.")
    commentators_count: int = Field(..., description="Number of distinct commentators.")
    translators: List[str] = Field(..., description="Names of all translators.")
    commentators: List[str] = Field(..., description="Names of all commentators.")
