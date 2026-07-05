from pydantic import BaseModel, Field

class Translation(BaseModel):
    """Pydantic model representing a translation of a Gita verse."""
    author: str = Field(..., description="Name of the translator/author.")
    language: str = Field(..., description="Language code of translation (e.g. 'en', 'hi').")
    description: str = Field(..., description="The translated text.")

class Commentary(BaseModel):
    """Pydantic model representing a commentary of a Gita verse."""
    author: str = Field(..., description="Name of the commentator/author.")
    language: str = Field(..., description="Language code of commentary (e.g. 'en', 'hi', 'sa').")
    description: str = Field(..., description="The commentary text.")
