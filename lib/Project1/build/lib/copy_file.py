import shutil

def copy_file(source_path, destination_dir):
    """Copies a file to a specified directory.

    Args:
        source_path: The path to the file to be copied.
        destination_dir: The directory to copy the file to.
    """
    try:
        shutil.copy(source_path, destination_dir)
        print(f"File '{source_path}' copied successfully to '{destination_dir}'")
    except FileNotFoundError:
        print(f"Error: File '{source_path}' not found.")
    except PermissionError:
      print(f"Error: Permission denied to access '{source_path}' or '{destination_dir}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")