import os
from dotenv import load_dotenv


import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        # Load env vars at instance creation time (NOT import time)
        load_dotenv()

        self.APP_NAME = "devmate"
        self.ENV = os.getenv("ENV", "dev")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    def validate(self):
        if not self.OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Please add it to your .env file."
            )



settings= Settings()




