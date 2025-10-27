import bibleVerses

def add_to_history(query):
    """Add a search query to history."""
    if query:
        bibleVerses.search_history.append(query)

def get_history():
    """Get the search history."""
    return list(bibleVerses.search_history)

def clear_history():
    """Clear the search history."""
    bibleVerses.search_history.clear()