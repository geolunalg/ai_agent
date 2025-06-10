import os
import subprocess


def run_python_file(working_directory, file_path):
    abs_wrk_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_wrk_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'

    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    SECONDS = 30
    try:
        results = []
        output = subprocess.run(["python", target_file], timeout=SECONDS, capture_output=True)
        if not output:
            return "No output produced."

        results.append(f"STDOUT: {output.stdout}")
        results.append(f"STDERR: {output.stderr}")

        if output.returncode != 0:
            results.append("Process exited with code {output.returncode}")

        return "\n".join(results)

    except Exception as e:
        return f"Error: executing Python file: {e}"
