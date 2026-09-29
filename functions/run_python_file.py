import os
import sys
import subprocess

from openai.types.chat import ChatCompletionFunctionToolParam


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = [sys.executable, target_file]
        if args is not None:
            command.extend(args)

        complete_process = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""
        if complete_process.returncode > 0:
            output += f"Process exited with code {complete_process.returncode}"

        if not complete_process.stderr and not complete_process.stdout:
            output += "No output produced"

        if complete_process.stdout:
            output += f"STDOUT: {complete_process.stdout}"

        if complete_process.stderr:
            output += f"STDERR: {complete_process.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file relative to the working directory with optional command-line arguments, returning its stdout and stderr",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}
