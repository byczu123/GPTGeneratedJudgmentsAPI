from bs4 import BeautifulSoup


def html_parser(text):
    return BeautifulSoup(text, "html.parser").get_text()
