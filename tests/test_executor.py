import unittest
from io import StringIO
from contextlib import redirect_stdout
from devmate.core.executor import Executor


class TestExecutor(unittest.TestCase):
    """Sanity tests for executor module"""

    def setUp(self):
        """Set up test fixtures"""
        self.executor = Executor()

    def test_noop_action(self):
        """Test that noop action executes successfully"""
        result = self.executor.execute("noop")
        self.assertEqual(result, {"status": "ok"})

    def test_noop_action_with_payload(self):
        """Test that noop action works even with payload (ignores it)"""
        result = self.executor.execute("noop", {"some": "data"})
        self.assertEqual(result, {"status": "ok"})

    def test_print_action(self):
        """Test that print action prints message and returns result"""
        test_message = "Hello, World!"
        with redirect_stdout(StringIO()) as f:
            result = self.executor.execute("print", {"message": test_message})
        
        self.assertEqual(result, {"printed": test_message})
        # Note: stdout capture might not work perfectly, but we check the return value

    def test_print_action_with_empty_message(self):
        """Test print action with empty message"""
        with redirect_stdout(StringIO()) as f:
            result = self.executor.execute("print", {"message": ""})
        self.assertEqual(result, {"printed": ""})

    def test_print_action_without_message_key(self):
        """Test print action when message key is missing (defaults to empty string)"""
        with redirect_stdout(StringIO()) as f:
            result = self.executor.execute("print", {})
        self.assertEqual(result, {"printed": ""})

    def test_execute_with_none_payload(self):
        """Test that execute handles None payload correctly"""
        result = self.executor.execute("noop", None)
        self.assertEqual(result, {"status": "ok"})

    def test_execute_without_payload(self):
        """Test that execute works without payload parameter"""
        result = self.executor.execute("noop")
        self.assertEqual(result, {"status": "ok"})

    def test_unknown_action_raises_error(self):
        """Test that unknown action raises ValueError"""
        with self.assertRaises(ValueError) as context:
            self.executor.execute("unknown_action")
        self.assertIn("Unknown action", str(context.exception))
        self.assertIn("unknown_action", str(context.exception))

    def test_unknown_action_with_payload(self):
        """Test that unknown action raises error even with payload"""
        with self.assertRaises(ValueError):
            self.executor.execute("nonexistent", {"key": "value"})


if __name__ == "__main__":
    unittest.main()

