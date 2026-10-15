def get_book_text(filepath):
    with open(filepath) as f:
        content = f.read()
    return content


def get_word_count(content):
    return len(content.split())


def get_char_count(content):
    map = {}
    for char in content:
        e_char = char.lower()
        if e_char not in map:
            map[e_char] = 1
            continue
        map[e_char] += 1
    return map


def get_sorted_chars(char_map):
    lst = []
    for key in char_map:
        lst.append({"char": key, "num": char_map[key]})
    lst.sort(key=lambda d: d["num"], reverse=True)
    return lst
