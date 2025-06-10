import os
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_wrk_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_wrk_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000
    try:
        with open(target_file, 'r') as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) == MAX_CHARS:
                return f'{file_content} [...File "{file_path}" truncated at 10000 characters]'
            return file_content
    except Exception as e:
        return f"Error reading file: {e}"


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
