import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")


    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "user",
            "content": args.user_prompt
        }
    ]
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        
    generate_content(client=client, messages=messages, verbose=args.verbose)
        
    
def generate_content(client: OpenAI, messages: list[ChatCompletionMessageParam], verbose: bool) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )
    
    if response.usage == None:
        raise RuntimeError("API reponse appears to be mulformed")
    
    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
