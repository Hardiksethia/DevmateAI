import unittest
from unittest.mock import MagicMock, patch
from devmate.core.agent import Agent


class TestAgent(unittest.TestCase):
    """Tests for Agent"""

    @patch("devmate.core.agent.Planner")
    @patch("devmate.core.agent.Executor")
    def test_agent_run_executes_plan(self, MockExecutor, MockPlanner):
        # Arrange
        mock_planner = MagicMock()
        mock_planner.create_plan.return_value = [
            {"action": "noop"},
            {"action": "print", "payload": {"message": "Hello"}},
        ]

        mock_executor = MagicMock()
        mock_executor.execute.side_effect = [
            {"status": "ok"},
            {"printed": "Hello"},
        ]

        MockPlanner.return_value = mock_planner
        MockExecutor.return_value = mock_executor

        agent = Agent()

        # Act
        results = agent.run("health")

        # Assert
        mock_planner.create_plan.assert_called_once_with("health")
        self.assertEqual(mock_executor.execute.call_count, 2)

        self.assertEqual(results[0]["action"], "noop")
        self.assertEqual(results[1]["result"]["printed"], "Hello")


if __name__ == "__main__":
    unittest.main()
