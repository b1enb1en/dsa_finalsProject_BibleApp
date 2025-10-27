import bibleVerses
import random

def get_verse_of_day():
    """Get a random verse as the verse of the day."""
    if not bibleVerses.bible:
        return '', 0, 0, 'No bible data loaded'
        
    # Choose random book
    book = random.choice(list(bibleVerses.bible.keys()))
    
    # Choose random chapter from that book
    chapter = random.choice(list(bibleVerses.bible[book].keys()))
    
    # Choose random verse from that chapter
    verse = random.choice(list(bibleVerses.bible[book][chapter].keys()))
    
    # Get the verse text
    verse_text = bibleVerses.bible[book][chapter][verse]
    
    return book, chapter, verse, verse_text