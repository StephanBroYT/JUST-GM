import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

TOKEN = os.getenv("TOKEN")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
INLESS_GUILD = int(os.getenv("INLESS_GUILD"))
INLESS_CHANNEL = int(os.getenv("INLESS_CHANNEL"))


client = Groq(
    api_key=os.getenv("api_key"),
)