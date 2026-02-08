import unittest
from unittest.mock import patch, MagicMock
from devmate.core.llm_client import LLMClient
from devmate.config import Settings


class TestLLMClient(unittest.TestCase):
    """Sanity tests for LLM client module"""

    @patch('devmate.core.llm_client.settings')
    @patch('devmate.core.llm_client.OpenAI')
    def test_llm_client_initialization(self, mock_openai, mock_settings):
        """Test that LLMClient initializes correctly"""
        # Setup mock
        mock_settings.OPENAI_API_KEY = "test-key-123"
        mock_settings.validate = MagicMock()
        mock_client_instance = MagicMock()
        mock_openai.return_value = mock_client_instance

        # Create client
        client = LLMClient()

        # Assertions
        mock_settings.validate.assert_called_once()
        mock_openai.assert_called_once_with(api_key="test-key-123")
        self.assertEqual(client.client, mock_client_instance)

    @patch('devmate.core.llm_client.settings')
    def test_llm_client_initialization_validates_settings(self, mock_settings):
        """Test that LLMClient calls settings.validate() on init"""
        mock_settings.OPENAI_API_KEY = "test-key"
        mock_settings.validate = MagicMock()

        with patch('devmate.core.llm_client.OpenAI'):
            client = LLMClient()
        
        mock_settings.validate.assert_called_once()

    @patch('devmate.core.llm_client.settings')
    @patch('devmate.core.llm_client.OpenAI')
    def test_llm_client_generate(self, mock_openai, mock_settings):
        """Test that generate() method calls OpenAI API correctly"""
        # Setup mocks
        mock_settings.OPENAI_API_KEY = "test-key-123"
        mock_settings.validate = MagicMock()
        
        mock_client_instance = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Generated response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client_instance.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client_instance

        # Create client and generate
        client = LLMClient()
        result = client.generate("Test prompt")

        # Assertions
        self.assertEqual(result, "Generated response")
        mock_client_instance.chat.completions.create.assert_called_once()
        call_args = mock_client_instance.chat.completions.create.call_args
        
        # Check model
        self.assertEqual(call_args.kwargs['model'], "gpt-4o-mini")
        self.assertEqual(call_args.kwargs['temperature'], 0.2)
        
        # Check messages
        messages = call_args.kwargs['messages']
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['role'], "user")
        self.assertEqual(messages[0]['content'], "Test prompt")

    @patch('devmate.core.llm_client.settings')
    def test_llm_client_initialization_fails_when_validation_fails(self, mock_settings):
        """Test that LLMClient raises error when settings validation fails"""
        mock_settings.validate = MagicMock(side_effect=RuntimeError("API key missing"))
        
        with patch('devmate.core.llm_client.OpenAI'):
            with self.assertRaises(RuntimeError) as context:
                client = LLMClient()
            self.assertIn("API key missing", str(context.exception))


if __name__ == "__main__":
    unittest.main()

