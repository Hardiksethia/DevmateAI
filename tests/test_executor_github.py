import unittest
from unittest.mock import patch

from devmate.core.executor import Executor


class TestExecutorGithub(unittest.TestCase):

    def setUp(self):
        self.executor = Executor()

    @patch("devmate.tools.github.list_open_prs")
    def test_list_prs(self, mock_list):
        mock_list.return_value = [{"number": 1, "title": "Test PR", "author": "me"}]

        result = self.executor.execute(
            "github_list_prs",
            {"repo": "me/repo"}
        )

        self.assertEqual(result["prs"][0]["number"], 1)

    @patch("devmate.tools.github.get_pr_comments")
    def test_get_pr_comments(self, mock_comments):
        mock_comments.return_value = [{"path": "file.py", "body": "Fix this"}]

        result = self.executor.execute(
            "github_get_pr_comments",
            {"repo": "me/repo", "pr": 1}
        )

        self.assertEqual(result["comments"][0]["path"], "file.py")
