from pathlib import Path
from typing import List

def read_file(path: str)-> str:
    return Path(path).read_text(encoding="utf-8")


def write_file(path:str,content:str):
    Path(path).write_text(content,encoding="utf-8")


def list_files(path:str=".")-> List[str]:
    return [str(p) for p in Path(path).iterdir()]

    