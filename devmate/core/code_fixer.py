from devmate.core.llm_client import LLMClient

FIX_PROMPT = """
You are a senior software engineer.

Given:
- source code
- a review comment

Return ONLY the updated full file content.

Rules:
- Do NOT explain
- Do NOT use markdown
- Output ONLY code
"""

class CodeFixer:
    def __init__(self):
        self.llm = LLMClient()

    def fix(self, code: str, comment: str) -> str:
        prompt = f"""
{FIX_PROMPT}

Review comment:
{comment}

Original code:
{code}
"""
        return self.llm.generate(prompt)
