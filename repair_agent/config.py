import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def check_config() -> None:
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        raise RuntimeError("GROQ_API_KEY is missing. Copy .env.example to .env and add your key.")


if __name__ == "__main__":
    check_config()
    print(f"Config OK (model: {GROQ_MODEL}, key loaded, {len(GROQ_API_KEY)} characters)")