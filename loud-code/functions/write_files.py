import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file which is relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to files to be read from, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content that is to be written to the file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_inside_working_dir = (
            os.path.commonpath([target_file_abs, working_dir_abs]) == working_dir_abs
        )
        if not is_inside_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        (parent_dir, _) = os.path.split(target_file_abs)
        # create path if not exitst
        os.makedirs(parent_dir, exist_ok=True)
        with open(target_file_abs, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as ex:
        print(ex)
        return "Error: standard lib error"
