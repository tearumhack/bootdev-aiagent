import os
from config import MAX_CHARS


def get_file_content(working_file_path: str, file_path: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_file_path)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if valid_target_file is False:
            return (
                f'Error: Cannot read "{file_path}" as it is outside '
                + "the permitted working directory"
            )

        if os.path.isfile(target_file) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            content: str = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: Exception caught: {e}"
