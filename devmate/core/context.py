from ast import Continue
from pathlib import Path
from typing import List

MAX_FILE_SIZE = 4_000  # chars
MAX_FILES = 10



class RepoContextBuilder:
    """

    Lightweight repo context builder (RAG-lite)

    """


    def __init__(self, root: str="."):
        self.root=Path(root)


    def build(self) -> str:
        files= self._select_files()
        sections=[]


        for file in files:
            try:
                content=file.read_text(encoding="utf-8")
                content=content[:MAX_FILE_SIZE]
                sections.append(
                    f"--- FILE: {file.relative_to(self.root)} ---\n{content}"
                )

            except Exception:
                continue

        return "\n\n".join(sections)


    
    def _select_files(self) -> List[Path]:
        candidates=[]


        for path in self.root.rglob("*"):
            if not path.is_file():
                continue


            if path.suffix not in {".py", ".md", ".txt"}:
                continue


            if path.stat().st_size > MAX_FILE_SIZE:
                continue


            candidates.append(path)

            if len(candidates) >= MAX_FILES:
                break


        return candidates



    def read_files(self, paths: List[str]) -> str:
        sections = []

        for rel_path in paths:
            path = self.root / rel_path
            if not path.exists() or not path.is_file():
                continue

            try:
                content = path.read_text(encoding="utf-8")
                content = content[:MAX_FILE_SIZE]
                sections.append(
                    f"--- FILE: {rel_path} ---\n{content}"
                )
            except Exception:
                continue

        return "\n\n".join(sections)




