
import os

# Set the maximum number of characters to read from the file
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_full_path = os.path.abspath(working_directory)

    if not full_path.startswith(working_dir_full_path):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string += (
                    f"\n[...File \"{file_path}\" truncated at 10000 characters]."
                )

        return file_content_string
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"
