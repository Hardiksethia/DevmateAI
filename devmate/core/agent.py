from typing import List, Dict, Any
from devmate.logger import get_logger
from devmate.core.planner import Planner
from devmate.core.executor import Executor
from devmate.core.code_fixer import CodeFixer


logger = get_logger("agent")


class Agent:
    """
    High-level orchestrator that connects planning and execution.
    """

    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()

    
    def run(self, intent: str):
        logger.info(f"Agent received intent: {intent}")

        plan = self.planner.create_plan(intent)
        logger.info(f"Execution plan created: {plan}")

        results = []
        fixer = CodeFixer()

        for step in plan:
           action = step["action"]
           payload = step.get("payload") or {}

           logger.info(f"Executing step: {action}")

           # ---- NORMAL EXECUTION ----
           result = self.executor.execute(action, payload)

           # ---- SPECIAL: PR REVIEW AUTOFIX ----
           if action == "github_list_review_comments":
               comments = result.get("comments", [])

               for comment in comments:
                   path = comment.get("path")
                   body = comment.get("body")

                   if not path or not body:
                       continue

                   file_content = self.executor.execute(
                       "read_file", {"path": path}
                   )["content"]

                   fixed_content = fixer.fix(file_content, body)

                   self.executor.execute(
                       "write_file",
                        {"path": path, "content": fixed_content},
                   )

               if comments:
                   self.executor.execute(
                      "git_commit",
                      {"message": "Auto-fix PR review comments"},
                   )

           results.append(
              {
                "action": action,
                "result": result,
              }
           )

        return results

     