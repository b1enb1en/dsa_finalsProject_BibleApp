import json
import platform
import subprocess
import random

book_mapping = {
    1: "Genesis",
    2: "Exodus",
    3: "Leviticus",
    4: "Numbers",
    5: "Deuteronomy",
    6: "Joshua",
    7: "Judges",
    8: "Ruth",
    9: "1 Samuel",
    10: "2 Samuel",
    11: "1 Kings",
    12: "2 Kings",
    13: "1 Chronicles",
    14: "2 Chronicles",
    15: "Ezra",
    16: "Nehemiah",
    17: "Esther",
    18: "Job",
    19: "Psalms",
    20: "Proverbs",
    21: "Ecclesiastes",
    22: "Song of Solomon",
    23: "Isaiah",
    24: "Jeremiah",
    25: "Lamentations",
    26: "Ezekiel",
    27: "Daniel",
    28: "Hosea",
    29: "Joel",
    30: "Amos",
    31: "Obadiah",
    32: "Jonah",
    33: "Micah",
    34: "Nahum",
    35: "Habakkuk",
    36: "Zephaniah",
    37: "Haggai",
    38: "Zechariah",
    39: "Malachi",
    40: "Matthew",
    41: "Mark",
    42: "Luke",
    43: "John",
    44: "Acts",
    45: "Romans",
    46: "1 Corinthians",
    47: "2 Corinthians",
    48: "Galatians",
    49: "Ephesians",
    50: "Philippians",
    51: "Colossians",
    52: "1 Thessalonians",
    53: "2 Thessalonians",
    54: "1 Timothy",
    55: "2 Timothy",
    56: "Titus",
    57: "Philemon",
    58: "Hebrews",
    59: "James",
    60: "1 Peter",
    61: "2 Peter",
    62: "1 John",
    63: "2 John",
    64: "3 John",
    65: "Jude",
    66: "Revelation"
}
def read_json_data(filename):
  try:
    with open(filename, "r") as file:
      data = json.load(file)
      resultset = data.get("resultset")
      if resultset and "row" in resultset:
        rows = resultset["row"]
        return rows
      else:
        print("Invalid JSON format: Missing 'resultset' or 'row' key.")
        return None
  except FileNotFoundError:
    print(f"File '{filename}' not found.")
    return None
  except json.JSONDecodeError:
    print(f"Error decoding JSON in '{filename}'.")
    return None


filename = "c:/Users/Sis. Acel Rodriguez/Downloads/bible/kjv.json"
rows = read_json_data(filename)


def main():
  is_app_close = False
  menus = ["Search", "Browse", "My bookmarks", "Verse of the day", "Exit"]
  while not is_app_close:
    print("Menu")
    for index, menu in enumerate(menus):
      print(f"[{index}] {menu}")

    user_input = handle_user_input("Choose an option: ", [0, 1, 2, 3, 4])

    if user_input == 0:
      search(rows)
    if user_input == 1:
      browse(rows)
    if user_input == 2:
      bookmarks(rows)
    if user_input == 3:
      verse_of_the_day(rows)
    if user_input == 4:
      is_app_close = True

  print("App closed")

def search(rows):
    search_text = input("Enter text to search: ").lower()
    found_verses = []
    for row in rows:
        book_id = row["field"][1]
        book_name = book_mapping.get(book_id, "Unknown")
        chapter = row["field"][2]
        verse = row["field"][3]
        verse_text = row["field"][4].lower()

        if search_text in verse_text:
            found_verses.append((book_name, chapter, verse, row["field"][4]))

    if found_verses:
        print("Matching verses found:")
        for book_name, chapter, verse, verse_text in found_verses:
            print(f"{book_name} {chapter}:{verse}") 
            print(f"{verse_text}\n")
    else:
        print("No matching verses found.")
def browse(rows):
  book_name = input("Enter the Book name (e.g., 'Genesis', 'Exodus'): ")
  chapter = int(input("Enter the Chapter number: "))
  verse = int(input("Enter the Verse number: "))

 
  inverted_book_mapping = {v.lower(): k for k, v in book_mapping.items()}
  book_id = inverted_book_mapping.get(book_name.lower())

  if book_id is not None:
      matching_verses = [row["field"][4] for row in rows if 
                         row["field"][1] == book_id and
                         row["field"][2] == chapter and
                         row["field"][3] == verse]

      if matching_verses:
          print("Matching verse found:")
          for verse_text in matching_verses:
              print(verse_text)
      else:
          print("Verse not found.")
  else:
      print("Book not found.")


bookmarks_list = []

def bookmarks(rows):
    while True:
        print("Bookmarks Menu")
        print("[1] Add Bookmark")
        print("[2] View Bookmarks")
        print("[3] Remove Bookmark")
        print("[4] Back to Main Menu")

        choice = handle_user_input("Choose an option: ", [1, 2, 3, 4])

        if choice == 1:
            add_bookmark(rows)
        elif choice == 2:
            view_bookmarks()
        elif choice == 3:
            remove_bookmark()
        elif choice == 4:
            return

def add_bookmark(rows):
    print("Enter the details for the bookmark:")
    book_name = input("Enter the Book name: ")
    chapter = int(input("Enter the Chapter number: "))
    verse = int(input("Enter the Verse number: "))

    inverted_book_mapping = {v.lower(): k for k, v in book_mapping.items()}
    book_id = inverted_book_mapping.get(book_name.lower())

    if book_id is not None:
        matching_verses = [row for row in rows if 
                           row["field"][1] == book_id and
                           row["field"][2] == chapter and
                           row["field"][3] == verse]

        if matching_verses:
            bookmarks_list.extend(matching_verses)
            print("Bookmark added successfully.")
        else:
            print("Verse not found.")
    else:
        print("Book not found.")

def view_bookmarks():
    if bookmarks_list:
        print("Your Bookmarks:")
        for idx, bookmark in enumerate(bookmarks_list, 1):
            book_id = bookmark["field"][1]
            book_name = book_mapping.get(book_id, "Unknown")
            chapter = bookmark["field"][2]
            verse_number = bookmark["field"][3]
            verse_text = bookmark["field"][4]
            print(f"{idx}. {book_name} {chapter}:{verse_number} - {verse_text}")
    else:
        print("No bookmarks saved yet.")

def remove_bookmark():
    if bookmarks_list:
        view_bookmarks()
        index_to_remove = int(input("Enter the index of the bookmark to remove: "))
        if 1 <= index_to_remove <= len(bookmarks_list):
            del bookmarks_list[index_to_remove - 1]
            print("Bookmark removed successfully.")
        else:
            print("Invalid index.")
    else:
        print("No bookmarks available to remove.")





def verse_of_the_day(rows):
  random_verse = random.choice(rows)
  book_id = random_verse["field"][1]
  book_name = book_mapping.get(book_id, "Unknown")
  chapter = random_verse["field"][2]
  verse_number = random_verse["field"][3]
  verse_text = random_verse["field"][4]

  print("Verse of the Day:")
  print(f"{book_name} {chapter}:{verse_number} - {verse_text}")

def handle_user_input(message, options):
  while True:
    user_input = input(message)
    try:
      user_input = int(user_input)
      if user_input in options:
        return user_input
      else:
        print("Invalid input. Please choose from the available options.")
    except ValueError:
      print("Invalid input. Please enter a valid integer.")


def clear_screen():
  if platform.system() == 'Windows':
    subprocess.call('cls', shell=True)
  else:
    subprocess.call('clear', shell=True)


main()