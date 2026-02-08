import unittest
import os
from unittest.mock import patch
from devmate.config import Settings


class TestConfig(unittest.TestCase):
    """Sanity tests for config module"""

    def test_settings_initialization(self):
        """Test that Settings class initializes with default values"""
        settings = Settings()
        self.assertEqual(settings.APP_NAME, "devmate")
        self.assertIn(settings.ENV, ["dev", "prod", "test"])

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-123"})
    def test_settings_with_api_key(self):
        """Test settings when OPENAI_API_KEY is set"""
        # Reload settings to pick up the env var
        settings = Settings()
        self.assertEqual(settings.OPENAI_API_KEY, "test-key-123")
        # Should not raise an error
        settings.validate()

    @patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=True)
    def test_settings_validation_fails_without_api_key(self):
        """Test that validate() raises RuntimeError when API key is missing"""
        settings = Settings()
        settings.OPENAI_API_KEY = None
        with self.assertRaises(RuntimeError) as context:
            settings.validate()
        self.assertIn("OPENAI_API_KEY", str(context.exception))

    @patch.dict(os.environ, {}, clear=True)
    def test_settings_validation_fails_when_key_is_none(self):
        """Test validation when OPENAI_API_KEY is None"""
        settings = Settings()
        settings.OPENAI_API_KEY = None
        with self.assertRaises(RuntimeError):
            settings.validate()

    def test_env_defaults_to_dev(self):
        """Test that ENV defaults to 'dev' when not set"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            self.assertEqual(settings.ENV, "dev")


if __name__ == "__main__":
    unittest.main()

