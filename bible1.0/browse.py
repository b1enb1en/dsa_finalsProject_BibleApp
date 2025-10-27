import bibleVerses

def list_all_books():
    """List all available books in the Bible."""
    return list(bibleVerses.bible.keys())

def get_chapters(book):
    """Get all chapters available for a given book."""
    if book in bibleVerses.bible:
        return list(bibleVerses.bible[book].keys())
    return []

def get_verses(book, chapter):
    """Get all verses available for a given book and chapter."""
    if book in bibleVerses.bible and chapter in bibleVerses.bible[book]:
        return list(bibleVerses.bible[book][chapter].keys())
    return []

def get_verse_text(book, chapter, verse):
    """Get the text of a specific verse."""
    try:
        return bibleVerses.bible[book][chapter][verse]
    except KeyError:
        return None

def browse_structure():
    """Return the complete structure of the Bible."""
    structure = {}
    for book in bibleVerses.bible:
        structure[book] = {}
        for chapter in bibleVerses.bible[book]:
            structure[book][chapter] = list(bibleVerses.bible[book][chapter].keys())
    return structure