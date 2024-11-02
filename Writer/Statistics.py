def GetWordCount(text: str) -> int:
    return len(text.split())

def IsValidChapter(text: str, min_words: int = 120) -> bool:
    return GetWordCount(text) >= min_words