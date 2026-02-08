from openai import OpenAI
from devmate.config import settings
from devmate.logger import get_logger

logger=get_logger("llm")

class LLMClient:
    """
    Thin wrapper around the OpenAI client.
    This is the ONLY place where we talk to an LLM.
    """

    def __init__(self):
        settings.validate()
        self.client=OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, prompt: str)-> str:
        """
        Simple text generation.
        """

        logger.info("sending prompt to llm")

        response=self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content":  prompt
                }
            ],
            temperature=0.2,
        )
        
        return response.choices[0].message.content
        