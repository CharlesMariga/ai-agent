import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
    
        files_info: list[str] = []
        for file_name in os.listdir(target_dir):
            file_size = os.path.getsize(f"{working_directory}/{directory}/{file_name}")
            is_dir = os.path.isdir(f"{working_directory}/{directory}/{file_name}")
            result = f"- {file_name}: file_size={file_size}, is_dir={is_dir}"
            files_info.append(result)
            
    
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: listing files: {e}"
    