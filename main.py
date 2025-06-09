import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def read_prop(argv):
    verbose = False

    if len(argv) == 1:
        print('Ask a question please -- example: python main.py "how are you?"')
        sys.exit(1)

    if len(argv) > 2:
        if argv[2] == "--verbose":
            verbose = True

    return (argv[1], verbose)


def main(argv):
    user_prompt, verbose = read_prop(argv)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    print(response.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main(sys.argv)
