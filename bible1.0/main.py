import bibleVerses
import search
import browse
import bookmarks
import verse_of_day
import history
import os, sys 

def display_menu():
    """Display the main menu options."""
    print('\nMenu')
    print('[0] Search')
    print('[1] Browse')
    print('[2] My bookmarks')
    print('[3] Verse of the day')
    print('[4] History')
    print('[5] Exit\n')

def handle_search():
    """Handle the search functionality."""
    search_active = True
    while search_active:
        query = input("\nEnter a book verse (example: gen 1:1 or genesis 1:1) or press Enter to cancel: ").strip()
        if query == '':
            return False
            
        results = search.search_verse(query)
        if results:
            for book, chap, ver, text in results:
                display_text = text
                if ':' not in query:  # Not a reference search
                    display_text = search.highlight_text(text, query)
                print(f"{book} {chap}:{ver} - {display_text}")
        else:
            print('No verses found.')
            
        post = input("Type 's' to search again, 'a' to add a bookmark by reference, Enter to return to main menu, or 'exit' to quit: ").strip().lower()
        if post == 'exit':
            return True
        if post == 's':
            continue
        if post == 'a':
            ref = input("Enter reference to bookmark (e.g. 'Genesis 1:1'): ").strip()
            if ref:
                if bookmarks.add_bookmark_by_ref(ref):
                    print('Bookmark added.')
                else:
                    print("Couldn't add bookmark; ensure format is 'Book Chapter:Verse' and that the verse exists.")
            continue
        break
    return False

def handle_browse():
    """Handle the browse functionality."""
    structure = browse.browse_structure()
    for book in structure:
        print(f"- {book}")
        for chapter in structure[book]:
            print(f"  Chapter {chapter}: {structure[book][chapter]}")
    
    post = input("Press Enter to return to main menu or type 'exit' to quit: ").strip().lower()
    return post == 'exit'

def handle_bookmarks():
    """Handle the bookmarks functionality."""
    bm_active = True
    while bm_active:
        action = input("Press Enter to view bookmarks or  type 'back' to return to main menu, type a reference to add (e.g. 'Genesis 1:1, gen 1:1'), type 'remove' to delete,or 'exit' to quit: ").strip()
        
        if action == '':
            bms = bookmarks.get_bookmarks()
            if bms:
                for ref, verse in bms.items():
                    print(f"{ref} - {verse}")
            else:
                print('No bookmarks yet.')
                
        elif action.lower() == 'remove':
            bms = list(bookmarks.get_bookmarks().items())
            if not bms:
                print('No bookmarks to remove.')
            else:
                for idx, (ref, verse) in enumerate(bms, 1):
                    print(f"{idx}. {ref} - {verse}")
                try:
                    i = int(input('Enter index to remove: ').strip())
                    if 1 <= i <= len(bms):
                        key = bms[i-1][0]
                        bookmarks.remove_bookmark(key)
                        print('Bookmark removed.')
                    else:
                        print('Invalid index.')
                except ValueError:
                    print('Invalid input.')
        elif action.lower() == 'back':
            return False              
        elif action.lower() == 'exit':
            return True
            
        else:
            if bookmarks.add_bookmark_by_ref(action):
                print('Bookmark added.')
            else:
                print("Couldn't add bookmark; ensure format is 'Book Chapter:Verse' and that the verse exists.")
    
    return False

def handle_verse_of_day():
    """Handle the verse of the day functionality."""
    book, chapter, verse, text = verse_of_day.get_verse_of_day()
    if not book:
        print(f"Verse of the Day:\n{text}")
    else:
        print(f"Verse of the Day:\n{book} {chapter}:{verse} - {text}")
        
    post = input("Press Enter to return to main menu or type 'exit' to quit: ").strip().lower()
    return post == 'exit'

def handle_history():
    """Handle the search history functionality."""
    hist = history.get_history()
    print('Search History:')
    if hist:
        for query in hist:
            print(f"- {query}")
    else:
        print('No search history yet.')
        
    post = input("Press Enter to return to main menu or type 'exit' to quit: ").strip().lower()
    return post == 'exit'

def run_app():
    """Main application loop."""
    # Load the Bible data
    # Use script-relative path so app works regardless of current working directory
    script_dir = os.path.dirname(__file__)
    data_file = os.path.join(script_dir, 'verses-1769.json')
    if not bibleVerses.load_bible_data(data_file):
        print("Error: Could not load Bible data.")
        return

    print('Welcome to the Terminal Bible App!')
    is_app_close = False
    
    while not is_app_close:
        display_menu()
        choice = input('Choose an option: ').strip()
        
        if choice == '0':
            is_app_close = handle_search()
        elif choice == '1':
            is_app_close = handle_browse()
        elif choice == '2':
            is_app_close = handle_bookmarks()
        elif choice == '3':
            is_app_close = handle_verse_of_day()
        elif choice == '4':
            is_app_close = handle_history()
        elif choice == '5':
            print('Goodbye!')
            break
        else:
            print('Unknown option. Please enter a number from 0 to 5.')

if __name__ == '__main__':
    run_app()