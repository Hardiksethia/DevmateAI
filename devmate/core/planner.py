from multiprocessing import Value
from typing import List, Dict, Any
from devmate.logger import get_logger
import json
from devmate.core.llm_client import LLMClient
from devmate.core.context import RepoContextBuilder







logger=get_logger("planner")


SYSTEM_PROMPT = """
You are a planning engine for a developer CLI agent.

Your task is to convert a user intent into a JSON execution plan.

Rules (VERY IMPORTANT):
- Output MUST be valid JSON
- Output MUST be a list
- Each list item MUST be an object
- Each object MUST contain an "action" field
- Optional "payload" field may be included
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include text outside JSON

Allowed actions (ONLY these are permitted):
- noop
- print
- read_file
- write_file
- list_files
- git_status
- git_diff
- git_commit
- github_list_prs
- github_get_pr
- github_get_pr_comments
- github_list_review_comments


Action payload rules:
- read_file → { "path": "<file path>" }
- write_file → { "path": "<file path>", "content": "<new content>" }
- list_files → { "path": "<directory path>" }
- git_commit → { "message": "<commit message>" }
- print → { "message": "<text>" }
- github_list_prs → { "repo": "<owner/repo>" }
- github_get_pr → { "repo": "<owner/repo>", "pr": <number> }
- github_get_pr_comments → { "repo": "<owner/repo>", "pr": <number> }
- github_list_pr_review_comments → {
  "repo": "<owner/repo>",
  "pr": <number>
}


If the intent is to explain or analyze code:
- Read the relevant files using read_file
- Then return a print action summarizing the explanation

If the intent is to fix PR review comments:
- ONLY fetch review comments using github_list_review_comments
- Do NOT generate read_file or write_file steps (these are handled automatically)
- Do NOT use placeholder paths like "path/to/relevant/file.py"
- The agent will automatically read files, apply fixes, and commit based on the review comments


If the intent is unclear or unsafe:
- Return a single step with action "print" explaining the limitation.


Example output:
[
  {"action": "git_status"},
  {"action": "print", "payload": {"message": "Repository status checked"}}
]

Example output:
[
  {"action": "github_list_review_comments", "payload": {"repo": "owner/repo", "pr": 12}},
  {"action": "read_file", "payload": {"path": "devmate/tools/git.py"}},
  {"action": "write_file", "payload": {"path": "devmate/tools/git.py", "content": "<updated code>"}},
  {"action": "git_commit", "payload": {"message": "Fix PR review comments"}}
]


Example (explanation intent):
User intent: "explain how git commits are handled"

Output:
[
  {"action": "read_file", "payload": {"path": "devmate/tools/git.py"}},
  {"action": "print", "payload": {"message": "Git commits are handled by staging all changes and calling git commit with a message."}}
]

"""





CONTEXT_SELECTION_PROMPT = """
You are helping decide which files from a repository are relevant.

Given:
- a user intent
- a list of file paths

Return ONLY a JSON list of file paths that should be read.

Rules:
- Output MUST be valid JSON
- Output MUST be a list of strings
- Do NOT include explanations
- Do NOT include markdown

If no files are relevant, return an empty list.

Example:
[
  "devmate/core/executor.py",
  "devmate/tools/git.py"
]
"""






class Planner:
    """
    LLM-powered planner that converts user intent into an execution plan.
    """

    def __init__(self):
        self.llm=LLMClient();

    def create_plan(self,intent: str)-> List[Dict[str, Any]]:
        logger.info(f"Creating LLM-based plan for intent: {intent}")

        # Build repo context (RAG-lite)
        builder = RepoContextBuilder()
        selected_files = self._select_relevant_files(intent)
        context = builder.read_files(selected_files)
        context_block = f"\nRepository context:\n{context}\n" if context else ""


        full_prompt = f"""
        {SYSTEM_PROMPT}

        {context_block}


        User intent:
        {intent}
        """

        response = self.llm.generate(full_prompt)


        logger.info(f"Raw LLM response: {response}")


        try:
            plan=json.loads(response)
        
        except json.JSONDecodeError as e:
            raise ValueError("LLM returned invalid JSON") from e


        self._validate_plan(plan)

        return plan



    def _select_relevant_files(self, intent: str) -> List[str]:
        builder = RepoContextBuilder()
        all_files = [
            str(p.relative_to(builder.root))
            for p in builder._select_files()
        ]

        prompt = f"""
        {CONTEXT_SELECTION_PROMPT}

        User intent:
        {intent}

        Available files:
        {json.dumps(all_files, indent=2)}
        """

        response = self.llm.generate(prompt)

        try:
            selected = json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Context selector returned invalid JSON")
            return []

        if not isinstance(selected, list):
            return []

        return [f for f in selected if isinstance(f, str)]



    
    def _validate_plan(self, plan: Any):
        allowed_actions = {
            "noop",
            "print",
            "read_file",
            "write_file",
            "list_files",
            "git_status",
            "git_diff",
            "git_commit",
            "github_list_prs",
            "github_get_pr",
            "github_get_pr_comments",
            "github_list_review_comments",

        }

        if not isinstance(plan, list):
            raise ValueError("Plan must be a list")

        for step in plan:
            if not isinstance(step, dict):
                raise ValueError("Each plan step must be a dict")

            action = step.get("action")
            if not action:
                raise ValueError("Each plan step must include 'action'")

            if action not in allowed_actions:
                raise ValueError(f"Action '{action}' is not allowed")

            payload = step.get("payload")
            if payload is not None and not isinstance(payload, dict):
                raise ValueError("Payload must be a dict if provided")






    