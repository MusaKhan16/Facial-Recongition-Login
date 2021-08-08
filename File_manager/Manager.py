from pathlib import Path, WindowsPath, PurePath
from typing import List
from shutil import copy


class FileManager:
    def make_dir(root_dir: WindowsPath, dirname: str) -> Path:
        new_directory = root_dir / dirname
        new_directory.mkdir(parents=True)
        return new_directory

    def get_dir(root_dir: WindowsPath, dirname: str) -> Path:
        for directory in (root_dir).iterdir():
            if directory.is_dir() and directory.name == dirname:
                return root_dir / dirname

    def convert_to_path_object(files: List[str]) -> List[PurePath]:
        return [PurePath(file) for file in files]

    def write_dir(destination: WindowsPath, files: List[PurePath]):
        for file in files:
            new_file = Path(destination / file.name)
            copy(file, new_file)
