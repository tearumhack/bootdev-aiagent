import os
import subprocess

schema_run_python_file = {  # pyright: ignore[reportUnknownVariableType]
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the specified python file in the python interpreter.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to a python file to execute, relative to the "
                    + "working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list[str]",
                    "description": "Arguments to provide to the executed python script",
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if valid_target_file is False:
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the '
                + "permitted working directory"
            )

        if os.path.isfile(target_file) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if file_path.split(".")[-1].lower() != "py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )

        output: list[str] = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if result.stdout == "" and result.stderr == "":
            output.append("No output produced")

        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")

        if result.stderr:
            output.append(f"STDERR: {result.stderr}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
