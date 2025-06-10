import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_wrk_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_wrk_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(target_file, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing file: {e}"


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
