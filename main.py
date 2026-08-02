import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key: str | None = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("Openrouter API Key not found in .env file.")


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    client: OpenAI = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    model: str = "openrouter/free"
    messages: list[dict[str, str]] = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    response = client.chat.completions.create(model=model, messages=messages)

    if response.usage is None:
        raise RuntimeError("Chat request failed: 'usage' is 'None'")

    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print(f"User Prompt: {args.user_prompt}")
    print(f"Response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
