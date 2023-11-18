import re
from bs4 import BeautifulSoup


def parse_html(text):
    return BeautifulSoup(text, "html.parser").get_text().replace("\n", "")


def split_text(text):
    splitted_text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)', text)

    first_ten = splitted_text[:15]

    first_ten_join = ''.join(first_ten)

    return first_ten_join


def split_text_reverse(text):
    split_text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)', text)

    last_ten = split_text[-8:]

    last_ten_join = ''.join(last_ten)

    return last_ten_join


def split_text_reverse1(text):
    split_text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)', text)

    last_ten = split_text[-5:]

    last_ten_join = ''.join(last_ten)

    return last_ten_join



