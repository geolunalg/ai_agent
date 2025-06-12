import os
import sys
from time import sleep
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


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

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for i in range(20):
        try:
            response = generate_content(client, messages, verbose)
            sleep(4)
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(response)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if response.candidates:
        for cadidate in response.candidates:
            response_content = cadidate.content
            messages.append(response_content)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main(sys.argv)
