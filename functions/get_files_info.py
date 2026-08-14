import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    RES_INDENT: str = "  - "
    ERR_INDENT: str = "    "
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir: bool = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        result: list[str] = []

        if directory == ".":
            result.append("Result for current directory:")
        else:
            result.append(f"Result for '{directory}' directory:")

        if valid_target_dir is False:
            result.append(
                ERR_INDENT
                + f'Error: Cannot list "{directory}" as it is outside the '
                + "permitted working directory"
            )
            return "\n".join(result)

        if os.path.isdir(target_dir) is False:
            result.append(ERR_INDENT + f'Error: "{directory}" is not a directory')
            return "\n".join(result)

        # return f'Success: "{directory}" is within the working directory'

        dir_contents = os.listdir(target_dir)
        for name in dir_contents:
            entry_path: str = os.path.join(target_dir, name)
            size: int = os.path.getsize(entry_path)
            is_dir: bool = os.path.isdir(entry_path)
            result.append(
                RES_INDENT + f"{name}: file_size={size} bytes, is_dir={is_dir}"
            )

        return "\n".join(result)

    except Exception as e:
        return f"Error: Exception caught: {e}"
