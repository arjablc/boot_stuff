from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.write_files import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_files_content

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_files_content,
    ],
)
