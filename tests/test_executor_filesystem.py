import unittest
import tempfile
from pathlib import Path

from devmate.core.executor import Executor


class TestExecutorFilesystem(unittest.TestCase):

    def setUp(self):
        self.executor = Executor()
        self.tmpdir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_write_and_read_file(self):
        file_path = self.base_path / "test.txt"

        write_result = self.executor.execute(
            "write_file",
            {"path": str(file_path), "content": "hello"}
        )
        self.assertEqual(write_result["written"], str(file_path))

        read_result = self.executor.execute(
            "read_file",
            {"path": str(file_path)}
        )
        self.assertEqual(read_result["content"], "hello")

    def test_list_files(self):
        (self.base_path / "a.txt").write_text("a")
        (self.base_path / "b.txt").write_text("b")

        result = self.executor.execute(
            "list_files",
            {"path": str(self.base_path)}
        )

        self.assertIn(str(self.base_path / "a.txt"), result["files"])
        self.assertIn(str(self.base_path / "b.txt"), result["files"])
