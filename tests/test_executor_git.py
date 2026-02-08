import unittest
from unittest.mock import patch

from devmate.core.executor import Executor


class TestExecutorGit(unittest.TestCase):

    def setUp(self):
        self.executor = Executor()

    @patch("devmate.tools.git.subprocess.check_output")
    def test_git_status(self, mock_check_output):
        mock_check_output.return_value = " M file.txt"

        result = self.executor.execute("git_status")

        self.assertIn("status", result)
        self.assertIn("file.txt", result["status"])

    @patch("devmate.tools.git.subprocess.check_output")
    def test_git_diff(self, mock_check_output):
        mock_check_output.return_value = "diff --git a/file.txt b/file.txt"

        result = self.executor.execute("git_diff")

        self.assertIn("diff", result)
        self.assertIn("diff --git", result["diff"])

    @patch("devmate.tools.git.subprocess.check_output")
    def test_git_commit(self, mock_check_output):
        mock_check_output.return_value = "[main abc123] commit message"

        result = self.executor.execute(
            "git_commit",
            {"message": "commit message"}
        )

        self.assertIn("commit", result)
        self.assertIn("commit message", result["commit"])
