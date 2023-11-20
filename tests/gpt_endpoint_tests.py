import unittest
from flask import Flask
from api.gpt import gpt_api_blueprint
from unittest.mock import patch


class TestRatePageEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.app.register_blueprint(gpt_api_blueprint)
        self.client = self.app.test_client()

    @patch('api.gpt.validate_token')
    @patch('api.gpt.insert_feedback')
    def test_rate_page_route_success(self, mock_insert_feedback, mock_validate_token):
        mock_validate_token.return_value = True

        headers = {'Authorization': 'Bearer your_valid_token'}

        response = self.client.post(
            '/rate',
            json={'justification': 'good_reason', 'feedback': 'positive', 'rating': 5},
            headers=headers
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Feedback submitted successfully')

    @patch('api.gpt.validate_token')
    def test_rate_page_route_token_not_provided(self, mock_validate_token):
        mock_validate_token.return_value = False

        response = self.client.post('/rate')
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Token not provided')


class TestQueryPageEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.app.register_blueprint(gpt_api_blueprint)
        self.client = self.app.test_client()

    @patch('api.gpt.validate_token')
    @patch('api.gpt.build_url')
    @patch('api.gpt.get_justification')
    @patch('api.gpt.parse_html')
    @patch('api.gpt.generate_justification')
    @patch('api.gpt.extract_first_sentences')
    @patch('api.gpt.extract_last_sentences')
    def test_query_page_route_success(self, mock_extract_last_sentences, mock_extract_first_sentences,
                                      mock_generate_justification, mock_parse_html, mock_get_justification,
                                      mock_build_url, mock_validate_token):
        mock_validate_token.return_value = True

        mock_build_url.return_value = 'mocked_url'
        mock_get_justification.return_value = 'mocked_justification'
        mock_parse_html.return_value = 'mocked_parsed_html'
        mock_extract_first_sentences.return_value = 'mocked_intro_sentences'
        mock_generate_justification.return_value = 'mocked_generated_justification'
        mock_extract_last_sentences.side_effect = ['-mocked_last_sentences', '-mocked_last_sentences',
                                                   '-mocked_last_sentences']

        headers = {'Authorization': 'Bearer your_valid_token'}
        response = self.client.post(
            '/query',
            json={'justification_to_generate': 'mocked_justification'},
            headers=headers

        )
        data = response.get_json()

        self.assertEqual(200, response.status_code)
        self.assertIn('justification', data)

    def test_query_page_route_token_not_provided(self):
        response = self.client.post('/query')
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Token not provided')


if __name__ == '__main__':
    unittest.main()
