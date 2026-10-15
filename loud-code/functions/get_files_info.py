import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.isdir(target_dir):
            return f'Error:"{directory}" is not a directory'

        # INFO: restricting the direcotry to be inside the project
        is_inside_working_dir = (
            os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs
        )
        if not is_inside_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        dir_contents = os.listdir(target_dir)
        result = ""
        for content in dir_contents:
            content_path = os.path.join(target_dir, content)
            file_size = os.path.getsize(content_path)
            is_dir = os.path.isdir(content_path)
            result += f"- {content}: file_size={file_size}, is_dir={is_dir}\n"
        return result
    except Exception:
        return "Error: standard lib error"
