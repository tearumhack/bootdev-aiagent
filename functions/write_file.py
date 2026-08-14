import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if valid_target_file is False:
            return (
                f'Error: Cannot write to "{file_path}" as it is outside the '
                + "permitted working directory"
            )

        if os.path.isdir(target_file) is True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(working_dir_abs, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: Exception caught: {e}"
