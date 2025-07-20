import os
import shutil


class Cleaner:
    """A class to clean specified directories by removing all files except .gitkeep."""

    def __init__(
        self,
        directories: str = [
            "db",
            "code_doc_agent/db",
            "docs",
            "workdir",
        ],
    ):
        # Directories to clean
        self.directories = directories

    def clean(self):
        """Clean specified directories by removing all files except .gitkeep."""
        for dir_path in self.directories:
            for root, dirs, files in os.walk(dir_path, topdown=False):
                for file in files:
                    if file != ".gitkeep":
                        file_path = os.path.join(root, file)
                        try:
                            os.remove(file_path)
                            print(f"Deleted file: {file_path}")
                        except Exception as e:
                            print(f"Error deleting file {file_path}: {e}")
                for d in dirs:
                    dir_to_remove = os.path.join(root, d)
                    try:
                        shutil.rmtree(dir_to_remove)
                        print(f"Deleted directory and its contents: {dir_to_remove}")
                    except Exception as e:
                        print(f"Error deleting directory {dir_to_remove}: {e}")
