import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)


def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    working_dir_full_path = os.path.abspath(working_directory)

    if not full_path.startswith(working_dir_full_path):

        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a valid directory'

    items = os.listdir(full_path)
    info_list = []
    for item in items:
        try:
            item_size = os.path.getsize(os.path.join(full_path, item))
            is_dir = os.path.isdir(os.path.join(full_path, item))
            data = f"- {item}: file_size={item_size} bytes, is_dir={is_dir}"
            info_list.append(data)
        except Exception as e:
            info_list.append(f"Error: {e}")

    result = "\n".join(info_list)
    return result
