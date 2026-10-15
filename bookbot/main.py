import sys

from stats import (get_book_text, get_char_count, get_sorted_chars,
                   get_word_count)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)

    path = sys.argv[1]

    content = get_book_text(path)
    word_num = get_word_count(content)
    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {path}...")
    print("----------- Word Count ----------")
    print(f"Found {word_num} total words")
    print("--------- Character Count -------")
    chars_count = get_char_count(content)
    sorted_chars = get_sorted_chars(chars_count)
    for char in sorted_chars:
        if char["char"].isalpha():
            print(f"{char["char"]}: {char["num"]}")
    print("============= END ===============")


main()
