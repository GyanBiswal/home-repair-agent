import os
from dotenv import load_dotenv

load_dotenv()  # reads .env from the project root into environment variables

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def check_config() -> None:
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        raise RuntimeError("GROQ_API_KEY is missing. Copy .env.example to .env and add your key.")


if __name__ == "__main__":
    check_config()
    print(f"Config OK (key loaded, {len(GROQ_API_KEY)} characters)")