import os
from google.genai import types

MAX_CHARS = 10000


schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file that are relative to the working directory, provides at max 10000 characters of output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to files to be read from, relative to the working directory",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        is_inside = (
            os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        )
        if not is_inside:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        file_content = ""
        with open(target_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content
    except Exception as ex:
        print(ex)
        return "Error: something went wrong horribly"
