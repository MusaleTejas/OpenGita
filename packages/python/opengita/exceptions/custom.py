class GitaException(Exception):
    """Base exception for all OpenGita SDK errors."""
    pass

class VerseNotFound(GitaException):
    """Raised when the requested verse does not exist in the dataset."""
    pass

class ChapterNotFound(GitaException):
    """Raised when the requested chapter does not exist in the dataset."""
    pass

class DatasetNotLoaded(GitaException):
    """Raised when the processed dataset files cannot be located or loaded."""
    pass

class LanguageNotSupported(GitaException):
    """Raised when an unsupported language code is requested."""
    pass
