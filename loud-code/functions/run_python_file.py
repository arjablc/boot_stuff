import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the extension of .py, which is relative to the root",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file that is to be run. This path is relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments that are to be passed to the python interpretor when running the python file. default is None, provide a list of string if need be",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        is_inside_working_dir = (
            os.path.commonpath([file_path_abs, working_dir_abs]) == working_dir_abs
        )
        if not is_inside_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", file_path_abs]
        if args is not None:
            command.extend(args)
        result = subprocess.run(
            args=command, capture_output=True, text=True, timeout=30
        )
        cmd_return_code = result.returncode
        if cmd_return_code != 0:
            return "Process exited with code " + cmd_return_code
        if result.stderr == "" and result.stdout == "":
            return "No output produced"
        return "STDOUT:" + result.stdout + "\n" + "STDERR:" + result.stderr
    except Exception as ex:
        return f"Error: executing Python file: {ex}"
