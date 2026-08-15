import json

from collections.abc import Callable
from functions.get_file_content import schema_get_file_content, get_file_content  # type: ignore
from functions.get_files_info import schema_get_files_info, get_files_info  # type: ignore
from functions.run_python_file import schema_run_python_file, run_python_file  # type: ignore
from functions.write_file import schema_write_file, write_file  # type: ignore

available_functions = [  # type: ignore
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(tool_call, verbose: bool = False) -> dict:  # type: ignore
    function_name = tool_call.function.name  # type: ignore
    function_args = json.loads(tool_call.function.arguments or "{}")  # type: ignore

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if not function_map.get(function_name, None):  # type: ignore
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,  # type: ignore
            "content": f"Error: Unknown function: {function_name}",
        }

    function_args["working_directory"] = "./calculator"
    result = function_map[function_name](**function_args)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,  # type: ignore
        "content": result,
    }
