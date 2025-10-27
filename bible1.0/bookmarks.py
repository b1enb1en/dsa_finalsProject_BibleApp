import bibleVerses
from search import parse_reference

def add_bookmark(book, chapter, verse):
    """Add a bookmark for a specific verse."""
    key = f"{book} {chapter}:{verse}"
    verse_text = bibleVerses.bible.get(book, {}).get(chapter, {}).get(verse)
    if verse_text:
        bibleVerses.bookmarks[key] = verse_text
        return True
    return False

def add_bookmark_by_ref(ref):
    """Add a bookmark using a text reference (e.g., 'Genesis 1:1')."""
    parsed = parse_reference(ref)
    if not parsed:
        return False
    book, chapter, verse = parsed
    return add_bookmark(book, chapter, verse)

def remove_bookmark(reference):
    """Remove a bookmark by its reference."""
    if reference in bibleVerses.bookmarks:
        del bibleVerses.bookmarks[reference]
        return True
    return False

def get_bookmarks():
    """Get all bookmarks."""
    return bibleVerses.bookmarks

def list_bookmarks():
    """List all bookmarks with their verses."""
    bookmarks = []
    for ref, verse in bibleVerses.bookmarks.items():
        bookmarks.append({
            'reference': ref,
            'verse': verse
        })
    return bookmarks