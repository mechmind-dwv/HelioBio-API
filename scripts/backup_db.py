import os
import subprocess
from datetime import datetime

# --- Configuration Variables ---
# IMPORTANT: Replace these with your actual database credentials and paths.
# Do not hardcode sensitive information in a real-world application; use environment variables.
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_strong_password"
DB_NAME = "your_database_name"

# The directory where backup files will be stored.
BACKUP_DIR = "backups"

def backup_database():
    """
    Performs a full backup of the specified MySQL database.
    The backup is saved to a timestamped file in the BACKUP_DIR.
    """
    # Create the backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created backup directory: {BACKUP_DIR}")

    # Generate a timestamp for the backup file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = f"{DB_NAME}_backup_{timestamp}.sql"
    backup_path = os.path.join(BACKUP_DIR, backup_file)

    print(f"Starting backup of database '{DB_NAME}'...")

    try:
        # Construct the mysqldump command.
        # Note: The password is included with -p and no space to prevent a security warning.
        command = [
            "mysqldump",
            f"--host={DB_HOST}",
            f"--user={DB_USER}",
            f"--password={DB_PASSWORD}",
            DB_NAME,
        ]

        # Use subprocess.run to execute the command and capture output.
        # This is more secure than using os.system().
        with open(backup_path, "w") as f:
            result = subprocess.run(
                command,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                check=True  # Raise an exception if the command fails
            )
        
        print(f"Backup completed successfully! Saved to: {backup_path}")

    except FileNotFoundError:
        print("Error: 'mysqldump' not found. Make sure MySQL client tools are installed and in your PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Backup failed with an error. Return code: {e.returncode}")
        print(f"Error output:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

    return True

# This block ensures the backup_database function is called when the script is executed.
if __name__ == "__main__":
    backup_database()
