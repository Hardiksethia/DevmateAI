import subprocess


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        # Return git's error output as text instead of crashing
        return e.output.strip()




def status()-> str:
    return _run(["git", "status", "--short"])




def diff() -> str:
    return _run(["git", "diff"])


def commit(message: str) -> str:
    _run(["git", "add", "."])
    return _run(["git", "commit", "-m", message])


