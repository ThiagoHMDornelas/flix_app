from unittest import TestCase
from unittest.mock import patch, Mock

from api.service import Auth


class AuthServiceTestCase(TestCase):
    def setUp(self):
        self.auth = Auth()

    @patch('api.service.requests.post')
    def test_get_token_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access': 'access-token', 'refresh': 'refresh-token'}
        mock_post.return_value = mock_response

        result = self.auth.get_token('usuario', 'senha')

        self.assertEqual(result, {'access': 'access-token', 'refresh': 'refresh-token'})
        mock_post.assert_called_once()

    @patch('api.service.requests.post')
    def test_get_token_invalid_credentials(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        result = self.auth.get_token('usuario', 'senha_errada')

        self.assertIn('error', result)
        self.assertIn('401', result['error'])
