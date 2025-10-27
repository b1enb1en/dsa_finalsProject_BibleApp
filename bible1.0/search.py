import re
import bibleVerses

def normalize_book_part(s: str) -> str:
    """Normalize book name part for comparison by removing non-letters."""
    return re.sub(r'[^a-zA-Z]', '', s).lower()

def map_book_name(user_book_part: str):
    """Map a user's input to a canonical book name using the inverted mapping."""
    normalized = normalize_book_part(user_book_part)
    if not normalized:
        return None

    # Exact match against inverted keys (which are lowercased canonical names)
    if normalized in bibleVerses.inverted_bible:
        return bibleVerses.inverted_bible[normalized]

    # Try prefix matching: find canonical book names whose normalized form startswith the input
    candidates = []
    for key_norm, canonical in bibleVerses.inverted_bible.items():
        # key_norm is already lowercased canonical name; normalize it further (remove non-letters)
        kn = re.sub(r'[^a-zA-Z]', '', key_norm).lower()
        if kn.startswith(normalized):
            candidates.append(canonical)

    if len(candidates) == 1:
        return candidates[0]

    # As a fallback, try matching first 3 letters (common abbreviation length)
    if len(normalized) <= 3:
        short_candidates = []
        for key_norm, canonical in bibleVerses.inverted_bible.items():
            kn = re.sub(r'[^a-zA-Z]', '', key_norm).lower()
            if kn.startswith(normalized[:3]):
                short_candidates.append(canonical)
        if len(short_candidates) == 1:
            return short_candidates[0]

    # Could not disambiguate
    return None

def kmp_search(pattern, text):
    """Knuth-Morris-Pratt string search algorithm."""
    if not pattern or not text:
        return False
    text = text.lower()
    pattern = pattern.lower()
    
    # Build failure function
    failure = [0] * len(pattern)
    i = 1
    j = 0
    while i < len(pattern):
        if pattern[i] == pattern[j]:
            failure[i] = j + 1
            i += 1
            j += 1
        elif j > 0:
            j = failure[j-1]
        else:
            failure[i] = 0
            i += 1
            
    # Find pattern
    i = 0  # text index
    j = 0  # pattern index
    while i < len(text):
        if pattern[j] == text[i]:
            if j == len(pattern) - 1:
                return True
            i += 1
            j += 1
        elif j > 0:
            j = failure[j-1]
        else:
            i += 1
    return False

def parse_reference(text):
    """Parse a text reference like 'Genesis 1:1' into (book, chapter, verse)."""
    if not text:
        return None
        
    # Split on whitespace and : to separate book/chapter/verse
    parts = re.split(r'[\s:]+', text.strip())
    if len(parts) < 3:
        return None
        
    # Try to map the book part (may be multiple words)
    book_parts = [] # gather book name parts
    verse_part = parts[-1]  # last part is verse
    chapter_part = parts[-2]  # second-to-last is chapter
    book_parts = parts[:-2]  # rest is book name
    
    # Join book parts and try to map to canonical name
    book_text = ' '.join(book_parts) # 
    book = map_book_name(book_text) # 
    if not book:
        return None
        
    # Parse chapter and verse numbers
    try:
        chapter = int(chapter_part)
        verse = int(verse_part)
        return (book, chapter, verse)
    except ValueError:
        return None

def search_verse(query):
    """Search for verses using either a reference or multi-token AND search."""
    ref = parse_reference(query)
    results = []
    
    # First try parsing as a reference
    if ref:
        book, chapter, verse = ref
        chap_dict = bibleVerses.bible.get(book)
        if chap_dict:
            verse_text = chap_dict.get(chapter, {}).get(verse)
            if verse_text:
                results.append((book, chapter, verse, verse_text))
        bibleVerses.search_history.append(query)
        return results

    # If not a reference, do a text search
    tokens = [t for t in re.findall(r"\w+", query.lower()) if t]
    if not tokens:
        bibleVerses.search_history.append(query)
        return results

    # Search through all verses requiring all tokens to match
    for book, chapters in bibleVerses.bible.items():
        for chap, verses in chapters.items():
            for vnum, text in verses.items():
                matched = True
                for tok in tokens:
                    if not kmp_search(tok, text):
                        matched = False
                        break
                if matched:
                    results.append((book, chap, vnum, text))

    bibleVerses.search_history.append(query)
    return results

def highlight_text(text: str, term: str) -> str:
    """Highlight search terms in text by wrapping in ** markers."""
    if not term or not text:
        return text
        
    highlighted = text
    terms = re.findall(r"\w+", term.lower())
    for t in terms:
        pattern = re.compile(re.escape(t), re.IGNORECASE) #checks for term in text
        highlighted = pattern.sub(f"\033[93m{t}\033[0m", highlighted)  # 93 is bright yellow, 0 resets color
    return highlighted