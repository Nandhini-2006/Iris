import os
from pathlib import Path
from dotenv import load_dotenv

from langfuse.openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise RuntimeError(
        "NVIDIA_API_KEY was not found in backend/.env"
    )


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)


MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"


def generate_response(prompt: str) -> str:

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        top_p=0.95,
        max_tokens=8192,
        name="debugger-llm"
    )

    return completion.choices[0].message.content