#!/usr/bin/env python3
"""test_config:
Test the applications configs
"""
import unittest
from unittest.mock import patch
from app.config import Config


class TestConfig(unittest.TestCase):
    """ Test cases for Config class.
    """

    @patch('os.getenv')
    def test_secret_key(self, mock_getenv):
        '''Test if SECRET_KEY is loaded correctly.
        '''

        mock_getenv.return_value = 'test_secret'
        config = Config()
        self.assertEqual(config.secret_key, 'test_secret')

    @patch('os.getenv')
    def test_sqlalchemy_database_uri(self, mock_getenv):
        ''' Test if SQLALCHEMY_DATABASE_URI is loaded correctly.
        '''
        mock_getenv.return_value = 'mysql://username:password.@host/db'
        config = Config()
        self.assertEqual(
            config.sqlalchemy_database_uri,
            'mysql://username:password.@host/db')

    def test_sqlalchemy_track_modifications(self):
        '''Test if SQLALCHEMY_TRACK_MODIFICATIONS is set to False
        '''
        config = Config()
        self.assertFalse(config.SQLALCHEMY_TRACK_MODIFICATIONS)


if __name__ == '__main__':
    unittest.main()
