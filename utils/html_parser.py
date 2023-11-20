import re
from bs4 import BeautifulSoup


def parse_html(text):
    return BeautifulSoup(text, "html.parser").get_text().replace("\n", "")


def extract_first_sentences(text, number_of_sentences):
    split_text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?!])', text)
    split_array = split_text[:number_of_sentences]
    combined_sentences = ''.join(split_array)
    return combined_sentences


def extract_last_sentences(text, number_of_sentences):
    split_text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?!])', text)
    split_array = split_text[number_of_sentences:]
    combined_sentences = ''.join(split_array)
    return combined_sentences
