from typing import  Any, Dict
from devmate.logger import get_logger
from devmate.tools import filesystem, git, github
from pathlib import Path







logger=get_logger("executor")


class Executor:
    """
    Executes concrete actions requested by higher-level components
    (agent / planner).

    This is the ONLY layer allowed to cause side effects.
    """

    def execute(self, action:str, payload: Dict[str, Any] | None=None)-> Any:
        """
        Execute a single action with an optional payload.

        Example:
            execute("noop")
            execute("print_message", {"message": "hello"})
        """

        payload=payload or {}

        logger.info(f"Executor received action='{action}' payload={payload}")

        handler_name=f"_handle_{action}"
        handler=getattr(self,handler_name,None)

        if not handler:
            raise ValueError(f"Unknown action :{action}")

        
        return handler(payload)


        
        
    # ------------------------
    # Action handlers (internal)
    # ------------------------

    def _handle_noop(self, payload: Dict[str, Any]):
        """
        No-op action. Useful for testing the executor pipeline.
        """
        logger.info("No-op action executed")
        return {"status": "ok"}

    def _handle_print(self, payload: Dict[str, Any]):
        """
        Print a message to stdout.
        Payload:
            { "message": str }
        """
        message = payload.get("message", "")
        print(message)
        return {"printed": message}







    def _handle_read_file(self, payload):
        path = payload.get("path")
        if not path:
            raise ValueError("read_file requires 'path'")

        p = Path(path)

        if not p.exists():
            return {
            "content": "",
            "exists": False
            }

        return {
            "content": p.read_text(encoding="utf-8"),
            "exists": True
        }

    def _handle_write_file(self, payload):
        path = payload.get("path")
        content = payload.get("content", "")
        if not path:
            raise ValueError("write_file requires 'path'")
        filesystem.write_file(path, content)
        return {"written": path}

    def _handle_list_files(self, payload):
        path = payload.get("path", ".")
        return {"files": filesystem.list_files(path)}






    def _handle_git_status(self, payload):
        output = git.status()
        return {"status": output}

    def _handle_git_diff(self, payload):
        output = git.diff()
        return {"diff": output}


    def _handle_git_commit(self, payload):
        message = payload.get("message")
        if not message:
            raise ValueError("git_commit requires 'message'")
        return {"commit": git.commit(message)}






    def _handle_github_list_prs(self, payload):
        repo = payload.get("repo")
        if not repo:
            raise ValueError("github_list_prs requires 'repo'")
        return {"prs": github.list_open_prs(repo)}

    def _handle_github_get_pr(self, payload):
        repo = payload.get("repo")
        pr = payload.get("pr")
        if not repo or not pr:
            raise ValueError("github_get_pr requires 'repo' and 'pr'")
        return {"pr": github.get_pr(repo, pr)}

    def _handle_github_get_pr_comments(self, payload):
        repo = payload.get("repo")
        pr = payload.get("pr")
        if not repo or not pr:
            raise ValueError("github_get_pr_comments requires 'repo' and 'pr'")
        return {"comments": github.get_pr_comments(repo, pr)}




    def _handle_github_list_review_comments(self, payload):
        repo = payload.get("repo")
        pr = payload.get("pr_number")

        if not repo or not pr:
            raise ValueError("github_list_review_comments requires repo and pr_number")

        from devmate.tools import github
        return {
        "comments": github.list_pr_review_comments(repo, pr)
        }











    


        