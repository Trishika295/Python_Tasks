import re


def analyze_text(text):
    """
    Analyze text and return character, word,
    sentence, and space counts.
    """

    if text is None:
        text = ""

    # Count all characters including spaces and punctuation
    character_count = len(text)

    # Count normal space characters
    space_count = text.count(" ")

    # Count words using split()
    words = text.split()
    word_count = len(words)

    # Count sentences ending with ., ! or ?
    sentence_matches = re.findall(r"[.!?]+", text)
    sentence_count = len(sentence_matches)

    return {
        "characters": character_count,
        "words": word_count,
        "sentences": sentence_count,
        "spaces": space_count
    }