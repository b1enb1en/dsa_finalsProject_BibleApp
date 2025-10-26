import random
import re
from collections import deque

# Book -> Chapter -> Verse hierarchical storage
bible = {
    'Genesis': {
        1: {
            1: 'In the beginning God created the heaven and the earth.',
            2: 'And the earth was without form, and void; and darkness was upon the face of the deep.'
        },
        2: {
            7: 'And the LORD God formed man of the dust of the ground.'
        }
    },
    'John': {
        3: {
            16: 'For God so loved the world, that he gave his only begotten Son...'
        }
    }
}

bookmarks = {}
search_history = deque(maxlen=5)

# helper to map lowercase book names to canonical keys
inverted_bible = {k.lower(): k for k in bible.keys()}

def normalize_book_part(s: str) -> str:
    """Normalize a book name fragment to a compact lowercase key."""
    s = s.strip().lower()
    # remove punctuation except spaces and digits
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s

def map_book_name(user_book_part: str):
    """Return canonical book name or None. Uses normalization and prefix matching.

    Accepts abbreviations like 'Gen' or 'Gen.' and lower-case input.
    """
    key = normalize_book_part(user_book_part)

    # exact canonical name match
    if key in inverted_bible:
        return inverted_bible[key]

    # collapsed form (no spaces) exact match
    collapsed = key.replace(' ', '')
    if collapsed in inverted_bible:
        return inverted_bible[collapsed]

    # prefix match: try to match user key as prefix of canonical names
    candidates = []
    for canon_lower, canon in inverted_bible.items():
        if canon_lower.startswith(key) or canon_lower.replace(' ', '').startswith(collapsed) or canon_lower.startswith(collapsed):
            candidates.append(canon)

    if len(candidates) == 1:
        return candidates[0]

    # try the reverse: user key might be longer (e.g. '1sam' vs '1 samuel')
    for canon_lower, canon in inverted_bible.items():
        if key.startswith(canon_lower) or collapsed.startswith(canon_lower.replace(' ', '')):
            candidates.append(canon)

    if len(candidates) == 1:
        return candidates[0]

    return None


# KMP substring search
def kmp_search(pattern, text):
    lps = [0] * len(pattern)
    j = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j-1]
            else:
                lps[i] = 0
                i += 1
    i = j = 0
    while i < len(text):
        if text[i].lower() == pattern[j].lower():
            i += 1
            j += 1
            if j == len(pattern):
                return True
        else:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return False

def search_verse(query):
    # detect reference format like 'Genesis 1:1'
    ref = parse_reference(query)
    results = []
    if ref:
        book, chapter, verse = ref
        chap_dict = bible.get(book)
        if chap_dict:
            verse_text = chap_dict.get(chapter, {}).get(verse)
            if verse_text:
                results.append((book, chapter, verse, verse_text))
        # still record the original query in history
        search_history.append(query)
        return results

    # fallback to substring search across all verses
    for book, chapters in bible.items():
        for chap, verses in chapters.items():
            for vnum, text in verses.items():
                if kmp_search(query, text):
                    results.append((book, chap, vnum, text))
    search_history.append(query)
    return results


def parse_reference(text):
    """Try to parse a Bible reference in the form 'BookName Chapter:Verse'.
    Returns (BookCanonicalName, chapter:int, verse:int) or None if not a ref.
    """
    if ':' not in text:
        return None
    left, right = text.split(':', 1)
    right = right.strip()
    try:
        verse = int(right)
    except ValueError:
        return None

    left = left.strip()
    if ' ' not in left:
        return None
    # split book name and chapter (chapter is last token)
    book_part, chap_part = left.rsplit(' ', 1)
    try:
        chapter = int(chap_part)
    except ValueError:
        return None

    # use map_book_name which accepts synonyms and normalized forms
    book_key = map_book_name(book_part)
    if not book_key:
        return None

    return book_key, chapter, verse

def add_bookmark(book, chapter, verse):
    key = f"{book} {chapter}:{verse}"
    # ensure verse exists
    verse_text = bible.get(book, {}).get(chapter, {}).get(verse)
    if verse_text:
        bookmarks[key] = verse_text
        return True
    return False


def add_bookmark_by_ref(ref):
    parsed = parse_reference(ref)
    if not parsed:
        return False
    book, chapter, verse = parsed
    return add_bookmark(book, chapter, verse)

def get_bookmarks():
    return bookmarks

def verse_of_the_day():
    book = random.choice(list(bible.keys()))
    chapter = random.choice(list(bible[book].keys()))
    verse = random.choice(list(bible[book][chapter].keys()))
    return book, chapter, verse, bible[book][chapter][verse]

def view_history():
    return list(search_history)

def help_menu():
    return '''Commands:
    search <query>
    bookmark <book> <chapter> <verse>
    bookmarks
    verse_of_the_day
    history
    help
    quit'''

def run_app():
    print('Welcome to the Terminal Bible App!')
    while True:
        print('''\nMenu
[0] Search
[1] Browse
[2] My bookmarks
[3] Verse of the day
[4] History
[5] Exit
''')
        choice = input('Choose an option: ').strip()

        if choice == '0':
            # keep prompting until a valid input is provided or user cancels with empty input
            while True:
                query = input("\nEnter a book verse (example: gen 1:1 or genesis 1:1) or press Enter to cancel: ").strip()
                if query == '':
                    # user chose to cancel search
                    break

                # If input looks like a reference (contains ':' and at least one digit),
                # require a valid reference format; otherwise allow normal text search.
                looks_like_ref = (':' in query) and any(ch.isdigit() for ch in query)
                if looks_like_ref:
                    parsed = parse_reference(query)
                    if not parsed:
                        print("Invalid reference format. Use 'Book Chapter:Verse' (e.g. 'Gen 1:1'). Please try again.")
                        continue

                results = search_verse(query)
                if results:
                    for book, chap, ver, text in results:
                        print(f"{book} {chap}:{ver} - {text}")
                else:
                    print('No verses found.')
                break
        elif choice == '1':
            for book in bible:
                print(f"- {book}")
                for chap in bible[book]:
                    print(f"  Chapter {chap}: {list(bible[book][chap].keys())}")
        elif choice == '2':
            # Bookmarks interaction: add by reference or view
            action = input("Press Enter to view bookmarks, or type a reference to add (e.g. 'Genesis 1:1'), or type 'remove' to delete: ").strip()
            if action == '':
                bookmarks = get_bookmarks()
                if bookmarks:
                    for ref, verse in bookmarks.items():
                        print(f"{ref} - {verse}")
                else:
                    print('No bookmarks yet.')
            elif action.lower() == 'remove':
                bookmarks = list(get_bookmarks().items())
                if not bookmarks:
                    print('No bookmarks to remove.')
                else:
                    for idx, (ref, verse) in enumerate(bookmarks, 1):
                        print(f"{idx}. {ref} - {verse}")
                    try:
                        i = int(input('Enter index to remove: ').strip())
                        if 1 <= i <= len(bookmarks):
                            key = bookmarks[i-1][0]
                            del get_bookmarks()[key]
                            print('Bookmark removed.')
                        else:
                            print('Invalid index.')
                    except ValueError:
                        print('Invalid input.')
            else:
                # try to add bookmark by reference
                ok = add_bookmark_by_ref(action)
                if ok:
                    print('Bookmark added.')
                else:
                    print("Couldn't add bookmark; ensure format is 'Book Chapter:Verse' and that the verse exists.")
        elif choice == '3':
            b, c, v, t = verse_of_the_day()
            print(f"Verse of the Day:\n{b} {c}:{v} - {t}")
        elif choice == '4':
            history = view_history()
            print('Search History:')
            if history:
                for q in history:
                    print(f"- {q}")
            else:
                print('No search history yet.')
        elif choice == '5':
            print('Goodbye!')
            break
        else:
            print('Unknown option. Please enter a number from 0 to 5.')

# Run the app
run_app()