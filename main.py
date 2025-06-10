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

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
                ),
            },
        )
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Display the content of the file requested; limit output to only 10,000 characters, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="The file requested to read and display the content."
                ),
            },
        )
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Execute a Python script from a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="The Python file containing the script to execute."
                ),
            },
        )
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write content to a new file or override content of existing file with content provided, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write to."
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file."
                )
            }
        )
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main(sys.argv)
