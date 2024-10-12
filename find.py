import os


def search_files(directory, word):
    """
    Searches all .txt files in a directory for a specific word.

    Args:
        directory: The directory to search.
        word: The word to search for.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                for line_number, line in enumerate(f):
                    if word in line:
                        print(f"Found '{word}' in {filename} on line {line_number + 1}")

search_files("../2024/May/chats", "family")
