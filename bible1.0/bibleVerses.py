from collections import deque
import random
import json
import os
import re

# Main data structures
bible = {}  # {Book: {chapter_int: {verse_int: text}}}
bookmarks = {}  # {reference_string: verse_text}
search_history = deque(maxlen=5)  # Recent search queries

# Mapping for book name lookup
inverted_bible = {}  # {lowercase_name: canonical_name}

def rebuild_inverted():
    """Rebuild the inverted book name mapping."""
    global inverted_bible
    if isinstance(bible, dict):
        inverted_bible = {k.lower(): k for k in bible.keys()}
    else:
        inverted_bible = {}

def load_bible_data(filename):
    """Load Bible data from a JSON file."""
    if not os.path.exists(filename):
        return False
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Normalize flat mapping like "Genesis 1:1" -> "In the beginning..."
            # into nested structure {Book: {chapter_int: {verse_int: text}}}
            global bible
            bible = {}

            if isinstance(data, dict):
                # detect flat style by presence of ':' in keys
                flat = any(isinstance(k, str) and ':' in k for k in data.keys())
                if flat:
                    pattern = re.compile(r"^(.+?)\s+(\d+):(\d+)$")
                    for k, v in data.items():
                        if not isinstance(k, str):
                            continue
                        m = pattern.match(k.strip())
                        if not m:
                            # fallback: skip weird keys
                            continue
                        book = m.group(1).strip()
                        chap = int(m.group(2))
                        verse = int(m.group(3))
                        bible.setdefault(book, {})
                        bible[book].setdefault(chap, {})
                        bible[book][chap][verse] = v
                else:
                    # assume already nested mapping
                    bible = data

            rebuild_inverted()
            return True
    except (json.JSONDecodeError, IOError):
        return False

def random_choice(seq):
    """Safe random choice that handles empty sequences."""
    if not seq:
        return None
    return random.choice(list(seq))