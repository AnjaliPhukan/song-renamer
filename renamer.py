# Python3 program to rename files using their metadata
# By default, renames it to "[Title] - [Artist]"
# Author: Anjali Phukan (https://github.com/AnjaliPhukan)
# Creation Date: December 16, 2025

from pathlib import Path
from tinytag import TinyTag
import sys

HELP_TEXT: str = """
This program is used to rename music/video files using their metadata.
The format for running this program is:
uv run renamer.py [INPUT DIRECTORY/FILE]
If an input file is supplied, only that file will be renamed. If it is a directory, every mp3 or m4a file inside the directory will be recursively renamed.
"""

def file_rename(path: Path) -> int:
    if not path.exists():
        print(f"Input path {path} does not exist.")
        return 1
    if not path.is_file():
        print(f"Input path {path} was not a file.")
        return 1
    # Weed out unsupported files
    if path.suffix not in (".mp3", ".m4a"):
        print(f"File {path} was not an .mp3 or .m4a file.")
        return 1
    file = TinyTag.get(path)
    new_path = path.parents[0].joinpath(Path(f"{file.artist if (file.artist != None) else "Unknown"} - {file.title if (file.title != None) else "Unknown"}{path.suffix}"))
    temp = new_path
    i: int = 1
    while temp.exists():
        temp = new_path
        temp = temp.parents[0].joinpath(Path(f"{temp.stem}({i}){path.suffix}"))
        i += 1
    new_path = temp
    path.rename(new_path)
    return 0

def dir_file_rename(dir_path: Path) -> int:
    if not dir_path.exists():
        print(f"Input path {dir_path} does not exist.")
        return 1
    if not dir_path.is_dir():
        print(f"Input path {dir_path} was not a directory.")
        return 1
    paths = Path(dir_path).glob("*")
    for path in paths:
        if not path.exists():
            print(f"File path {path} does not exist. Aborting program.")
            return 1
        if (path.is_file()):
            file_rename(path)
        else:
            dir_file_rename(path)
    return 0
    
def main() -> int:
    # Check if no arguments supplied, provide help text if so
    if (len(sys.argv) == 1) or (sys.argv[1] in ("help", "-h", "--help")):
        print(HELP_TEXT)
        return 0

    # If don't need to print help text
    file_path: Path = Path(sys.argv[1])
    if (not file_path.exists()):
        print(f"Input file {file_path} does not exist.")
        return 1
    
    exit_code: int = 0
    if (file_path.is_file()):
        exit_code = file_rename(file_path)
        print("Input file renamed!");
    
    if (file_path.is_dir()):
        exit_code = dir_file_rename(file_path)
        print("Finished renaming everything in directory!")
    return exit_code

if __name__ == "__main__":
    sys.exit(main())