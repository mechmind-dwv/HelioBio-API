import os

def create_directory_structure():
    """
    Creates a specific directory structure for application data.

    The structure includes:
    - data/
      - cache/    (for temporary or cached files)
      - exports/  (for user-facing data exports)
      - logs/     (for application logs)
    """

    # Define the base directory and the list of subdirectories to be created.
    base_dir = "data"
    sub_dirs = ["cache", "exports", "logs"]

    print(f"Creating directory structure under '{base_dir}'...")

    try:
        # Use os.makedirs with exist_ok=True to create the base directory
        # and all necessary parent directories without raising an error if they exist.
        os.makedirs(base_dir, exist_ok=True)
        print(f"Base directory '{base_dir}' created or already exists.")

        # Loop through the list of subdirectories and create them inside the base directory.
        for sub_dir in sub_dirs:
            path = os.path.join(base_dir, sub_dir)
            os.makedirs(path, exist_ok=True)
            print(f"Subdirectory '{path}' created or already exists.")

        print("\nDirectory structure created successfully.")

    except OSError as e:
        # Catch any potential OS errors, such as permission issues.
        print(f"Error: Failed to create directories. Details: {e}")


# Call the function to run the script.
if __name__ == "__main__":
    create_directory_structure()
