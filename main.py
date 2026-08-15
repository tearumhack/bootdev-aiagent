import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from typing import Any
from call_function import available_functions, call_function  # type: ignore

load_dotenv()
api_key: str | None = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("Openrouter API Key not found in .env file.")


def format_text(text: str) -> str:
    words: list[str] = text.split()
    if not words:
        return text

    lines: list[str] = []
    current_line: list[str] = []

    for word in words:
        current_line.append(word)
        if len(current_line) == 16:
            lines.append(" ".join(current_line))
            current_line = []

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(f"    {line}" for line in lines)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client: OpenAI = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages: list[Any] = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,  # type: ignore
    )

    if response.usage is None:
        raise RuntimeError("Chat request failed: 'usage' is 'None'")

    if args.verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print("User prompt:")
        print(format_text(args.user_prompt))

    message = response.choices[0].message
    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)  # type: ignore
            if result_message.get("content", None) is None:  # type: ignore
                raise Exception("Tool call received, but message content is not None.")

            if args.verbose:
                print(f"-> {result_message['content']}")

    else:
        if response.choices[0].message.content is None:
            print("Response empty!")
        else:
            print("Response:")
            print(format_text(response.choices[0].message.content))


if __name__ == "__main__":
    main()
