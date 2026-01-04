# setup.py
import os
import shutil

try:
    from Cython.Build import cythonize
except ImportError:
    raise ImportError(
        "Cython is required to build the extensions. Try installing it via 'pip install cython'."
    )
from setuptools import Command, setup

# blacklist files, these files will be excluded from build
EXCLUDE_FILES = [
    "main.py",
    "compile.py",
]


def get_files_to_build():
    files_to_build = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if file in EXCLUDE_FILES or "migrations" in root:
                    continue
                files_to_build.append(file_path)

    return files_to_build


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # 1. Xóa folder build
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("Removed 'build' directory")

        # scan .c and .so files
        for root, _, files in os.walk("."):
            for file in files:
                # skip non-C/C++ files
                if not file.endswith((".c", ".so")):
                    continue

                file_name = file.split(".")[0]
                for _file in files:
                    # only remove files with the same base name
                    if not _file.startswith(file_name):
                        continue
                    if _file == file:
                        continue
                    if not _file.endswith((".py", ".pyx")):
                        continue

                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Removed: {file_path}")


setup(
    ext_modules=cythonize(
        get_files_to_build(), compiler_directives={"language_level": "3"}
    ),
    cmdclass={
        "clean": CleanCommand,
    },
)
