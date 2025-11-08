import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    model_name = 'llama-3.1-8b-instant'
    temperature = 0.9
    max_retries = 3

settings = Settings()