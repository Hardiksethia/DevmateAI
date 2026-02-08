import unittest
from unittest.mock import patch, MagicMock
from devmate.core.planner import Planner


class TestLLMPlanner(unittest.TestCase):

    @patch("devmate.core.planner.LLMClient")
    def test_llm_planner_valid_plan(self, MockLLM):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = """
        [
          {"action": "noop"},
          {"action": "print", "payload": {"message": "Hello"}}
        ]
        """
        MockLLM.return_value = mock_llm

        planner = Planner()
        plan = planner.create_plan("say hello")

        self.assertEqual(len(plan), 2)
        self.assertEqual(plan[0]["action"], "noop")
        self.assertEqual(plan[1]["payload"]["message"], "Hello")

    @patch("devmate.core.planner.LLMClient")
    def test_llm_planner_invalid_json(self, MockLLM):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "not json"
        MockLLM.return_value = mock_llm

        planner = Planner()

        with self.assertRaises(ValueError):
            planner.create_plan("break it")


    

    @patch("devmate.core.planner.LLMClient")
    def test_planner_generates_filesystem_plan(self, MockLLM):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = """
        [
          {"action": "read_file", "payload": {"path": "README.md"}},
          {"action": "print", "payload": {"message": "File read"}}
        ]
        """
        MockLLM.return_value = mock_llm

        planner = Planner()
        plan = planner.create_plan("read the readme")

        self.assertEqual(plan[0]["action"], "read_file")
        self.assertEqual(plan[0]["payload"]["path"], "README.md")

    @patch("devmate.core.planner.LLMClient")
    def test_planner_rejects_unknown_action(self, MockLLM):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = """
        [
          {"action": "delete_everything"}
        ]
        """
        MockLLM.return_value = mock_llm

        planner = Planner()

        with self.assertRaises(ValueError):
            planner.create_plan("do something dangerous")




    

    @patch("devmate.core.planner.RepoContextBuilder")
    @patch("devmate.core.planner.LLMClient")
    def test_planner_includes_repo_context(self, MockLLM, MockContext):
        mock_llm = MockLLM.return_value
        mock_llm.generate.return_value = '[{"action": "noop"}]'

        mock_builder = MockContext.return_value
        mock_builder.read_files.return_value = "--- FILE: test.py ---\nprint('hello')"

        planner = Planner()

        # Force selected files
        planner._select_relevant_files = lambda intent: ["test.py"]

        planner.create_plan("do something")

        prompt = mock_llm.generate.call_args[0][0]

        self.assertIn("Repository context", prompt)
        self.assertIn("test.py", prompt)
        self.assertIn("print('hello')", prompt)




    
    @patch("devmate.core.planner.LLMClient")
    def test_context_selection_called(self, MockLLM):
        mock_llm = MockLLM.return_value

        # First call: context selection
        mock_llm.generate.side_effect = [
        '["devmate/core/executor.py"]',
        '[{"action": "noop"}]'
        ]

        planner = Planner()
        planner.create_plan("explain executor")

        self.assertEqual(mock_llm.generate.call_count, 2)


