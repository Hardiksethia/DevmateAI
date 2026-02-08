import unittest
from unittest.mock import patch, MagicMock

from devmate.core.agent import Agent


class TestPRAutoFix(unittest.TestCase):
    def setUp(self):
        self.agent = Agent()

    @patch("devmate.core.agent.CodeFixer")
    @patch("devmate.core.agent.Executor")
    @patch("devmate.core.agent.Planner")
    def test_autofix_pr_review_comments(
        self,
        mock_planner_cls,
        mock_executor_cls,
        mock_fixer_cls,
    ):
        """
        Test that PR review comments are auto-fixed:
        - comments fetched
        - files read
        - fixes applied
        - files written
        - commit created
        """

        # -------- Planner mock --------
        mock_planner = MagicMock()
        mock_planner.create_plan.return_value = [
            {
                "action": "github_list_pr_review_comments",
                "payload": {"repo": "owner/repo", "pr": 1},
            }
        ]
        mock_planner_cls.return_value = mock_planner

        # -------- Executor mock --------
        mock_executor = MagicMock()

        mock_executor.execute.side_effect = [
            # github_list_pr_review_comments
            {
                "comments": [
                    {
                        "path": "foo.py",
                        "body": "Use better variable names",
                        "line": 10,
                    }
                ]
            },
            # read_file
            {"content": "x=1"},
            # write_file
            {},
            # git_commit
            {},
        ]

        mock_executor_cls.return_value = mock_executor

        # -------- CodeFixer mock --------
        mock_fixer = MagicMock()
        mock_fixer.fix.return_value = "better_name = 1"
        mock_fixer_cls.return_value = mock_fixer

        # -------- Run agent --------
        agent = Agent()
        results = agent.run("fix review comments for PR 1 in owner/repo")

        # -------- Assertions --------

        # Planner used
        mock_planner.create_plan.assert_called_once()

        # Executor calls
        calls = mock_executor.execute.call_args_list

        self.assertEqual(calls[0][0][0], "github_list_pr_review_comments")
        self.assertEqual(calls[1][0][0], "read_file")
        self.assertEqual(calls[2][0][0], "write_file")
        self.assertEqual(calls[3][0][0], "git_commit")

        # Fixer called
        mock_fixer.fix.assert_called_once_with("x=1", "Use better variable names")

        # Final result sanity
        self.assertEqual(results[0]["action"], "github_list_pr_review_comments")
