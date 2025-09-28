import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []

    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_full_path = os.path.abspath(working_directory)

    # Use commonpath to avoid false positives with startswith
    if (
        os.path.commonpath([full_path, working_dir_full_path])
        != working_dir_full_path
    ):
        return (
            f'Error: Cannot execute "{file_path}" as it is outside '
            "the permitted working directory"
        )

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    extension = os.path.splitext(file_path)[1].lower()
    if extension != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Use the current Python interpreter
        subprocess_args = [sys.executable, full_path] + args

        complete_process = subprocess.run(
            subprocess_args, capture_output=True, text=True, timeout=30
        )

        if complete_process.returncode != 0:
            return (
                f"STDERR: {complete_process.stderr}. "
                f"Process exited with code {complete_process.returncode}."
            )

        if complete_process.stdout == "":
            return "No output produced"

        return f"STDOUT: {complete_process.stdout}"
    except Exception as e:
        return f"Error executing Python file: {e}"
