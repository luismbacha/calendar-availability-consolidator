import unittest
from unittest.mock import patch
import os
from src.auth import get_credentials
from google.oauth2.credentials import Credentials

class TestAuth(unittest.TestCase):
    
    @patch.dict(os.environ, {
        'GOOGLE_CLIENT_ID': 'test_client_id_123',
        'GOOGLE_CLIENT_SECRET': 'test_client_secret_abc',
        'GOOGLE_REFRESH_TOKEN': '1//test_refresh_token_xyz'
    }, clear=True)
    def test_get_credentials_success(self):
        """Verifies successful creation of Credentials when all env vars are present."""
        creds = get_credentials()
        self.assertIsInstance(creds, Credentials)
        self.assertEqual(creds.client_id, 'test_client_id_123')
        self.assertEqual(creds.client_secret, 'test_client_secret_abc')
        self.assertEqual(creds.refresh_token, '1//test_refresh_token_xyz')
        self.assertIsNone(creds.token)
        self.assertEqual(creds.token_uri, "https://oauth2.googleapis.com/token")

    @patch.dict(os.environ, {
        'GOOGLE_CLIENT_ID': 'test_client_id_123'
        # Deliberately missing GOOGLE_CLIENT_SECRET and GOOGLE_REFRESH_TOKEN
    }, clear=True)
    def test_get_credentials_missing_env_vars(self):
        """Verifies that missing environment variables trigger a strict EnvironmentError."""
        with self.assertRaisesRegex(EnvironmentError, "Missing required environment variables: GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN"):
            get_credentials()

if __name__ == '__main__':
    unittest.main()
