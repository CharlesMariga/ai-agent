import os
import argparse
import json

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    generate_content(client=client, messages=messages, verbose=args.verbose)


def generate_content(
    client: OpenAI, messages: list[ChatCompletionMessageParam], verbose: bool
) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("API reponse appears to be mulformed")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print("Response:")
    print(response.choices[0].message.content)

    message = response.choices[0].message

    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                continue

            result_message = call_function(tool_call=tool_call, verbose=verbose)

            if not result_message.get("content"):
                raise Exception("")

            if verbose:
                print(f"-> {result_message['content']}")
    else:
        print(message)


if __name__ == "__main__":
    main()
