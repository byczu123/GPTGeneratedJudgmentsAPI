import unittest

from utils.html_parser import extract_last_sentences, extract_first_sentences, parse_html


class TestExtracLastSentences(unittest.TestCase):
    def test_extract_last_sentences(self):
        text = "This is a sample text. It has multiple sentences. We want to extract the last two sentences."
        result = extract_last_sentences(text, 1)
        expected_result = " It has multiple sentences. We want to extract the last two sentences."
        self.assertEqual(result, expected_result)

    def test_extract_last_sentences_empty_text(self):
        text = ""
        result = extract_last_sentences(text, 2)
        expected_result = ""
        self.assertEqual(result, expected_result)


class TestExtractFirstSentences(unittest.TestCase):
    def test_extract_first_sentences(self):
        text = "This is a sample text. It has multiple sentences. We want to extract the first two sentences."
        result = extract_first_sentences(text, 2)
        expected_result = "This is a sample text. It has multiple sentences."
        self.assertEqual(result, expected_result)

    def test_extract_first_sentences_not_enough_sentences(self):
        text = "This is a sample text with only one sentence."
        result = extract_first_sentences(text, 2)
        expected_result = "This is a sample text with only one sentence."
        self.assertEqual(result, expected_result)

    def test_extract_first_sentences_empty_text(self):
        text = ""
        result = extract_first_sentences(text, 2)
        expected_result = ""
        self.assertEqual(result, expected_result)


class TestParseHtml(unittest.TestCase):
    def test_parse_html(self):
        html_text = "<html><body><p>This is a <b>sample</b> HTML text.</p></body></html>"
        result = parse_html(html_text)
        expected_result = "This is a sample HTML text."
        self.assertEqual(result, expected_result)

    def test_parse_html_with_newlines(self):
        html_text = "<html><body><p>This is a <b>sample</b> HTML text.</p></body></html>"
        result = parse_html(html_text + "\n")
        expected_result = "This is a sample HTML text."
        self.assertEqual(result, expected_result)

    def test_parse_empty_html(self):
        html_text = ""
        result = parse_html(html_text)
        expected_result = ""
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
