import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_full_path = os.path.abspath(working_directory)

    if not full_path.startswith(working_dir_full_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    extension = os.path.splitext(file_path)[1].lower()
    if extension != '.py':
        return f'Error: "{file_path}" is not a Python file.'

    try:
        subprocess_args = ['python', full_path] + args

        complete_process = subprocess.run(
            subprocess_args, capture_output=True, text=True, timeout=30)

        if complete_process.returncode != 0:
            return f'STDERR: {complete_process.stderr}. Process exited with code {complete_process.returncode}.'

        if complete_process.stdout == "":
            return "No output produced"

        return f"STDOUT:{complete_process.stdout}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
