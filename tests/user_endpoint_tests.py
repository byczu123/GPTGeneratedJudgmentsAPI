import unittest
from flask import Flask
from jwt import ExpiredSignatureError

from api.user import user_api_blueprint
from unittest.mock import patch


class TestTokenEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.app.register_blueprint(user_api_blueprint)
        self.client = self.app.test_client()

    @patch('api.user.query_user')
    def test_create_token_route_invalid_credentials(self, mock_query_user):
        mock_query_user.return_value = None

        response = self.client.post('/token', json={'email': 'invalid@example.com', 'password': 'invalid_password'})
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid credentials')


class TestValidateTokenEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.app.register_blueprint(user_api_blueprint)
        self.client = self.app.test_client()

    @patch('api.user.decode_token')
    def test_validate_token_route_valid_token(self, mock_decode_token):
        mock_decode_token.return_value = {'sub': 'test@example.com'}

        response = self.client.post('/validate-token', headers={'Authorization': 'Bearer valid_token'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['valid'])
        self.assertEqual(data['message'], 'test@example.com')

    @patch('api.user.decode_token')
    def test_validate_token_route_invalid_token(self, mock_decode_token):
        mock_decode_token.side_effect = Exception("Invalid token")

        response = self.client.post('/validate-token', headers={'Authorization': 'Bearer invalid_token'})
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['valid'])
        self.assertEqual(data['message'], 'Invalid token')

    @patch('api.user.decode_token')
    def test_validate_token_route_expired_token(self, mock_decode_token):
        mock_decode_token.side_effect = ExpiredSignatureError("Token has expired")

        response = self.client.post('/validate-token', headers={'Authorization': 'Bearer expired_token'})
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['valid'])
        self.assertEqual(data['message'], 'Token has expired')

    def test_validate_token_route_token_not_provided(self):
        response = self.client.post('/validate-token')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Token not provided')


if __name__ == '__main__':
    unittest.main()
