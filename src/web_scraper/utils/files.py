"""
    File related utilities
"""

import os
import uuid


def make_file(root_dir: str, filename_prefix: str, file_extension: str = "tmp", make_unique: bool = False) -> str:
    """
    Creates a temp file under the specified root directory with the specified filename prefix and file extension
    Creates the full directory structure if it does not exist
    Does not create the file -- maybe it should?
    :param root_dir:
    :param filename_prefix:
    :param file_extension:
    :param make_unique: When True, adds a random string to the filename to ensure uniqueness.
    :return: The absolute path to the file
    """
    os.makedirs(root_dir, exist_ok=True)
    rand = ""
    if make_unique:
        rand = f"_{uuid.uuid4().hex}"

    filename = f"{filename_prefix}{rand}.{file_extension}"
    return os.path.join(root_dir, filename)


def read_all_content(filename: str, read_as_text: bool = True) -> str:
    """
    Reads all content from a file. Treats the file as text by default.
    Warning: Use this function with caution. It'll load all data into memory.
    :param filename:
    :param read_as_text: When True, reads the file as text. False, reads as binary.
    :return: All content as a string
    """
    flag = "" if read_as_text else "b"
    content = None
    with open(filename, f"r{flag}") as infile:
        content = infile.read()
    return content


def write_to_file(root_dir: str, content: str, filename_prefix: str, file_extension: str = "tmp",
                  make_unique: bool = False) -> str:
    """
    Creates and writes to a temp file under the specified root directory with the specified filename prefix and file extension
    :param root_dir:
    :param content:
    :param filename_prefix:
    :param file_extension:
    :param make_unique: When True, adds a random string to the filename to ensure uniqueness.
    :return: The filename
    """
    filename = make_file(root_dir, filename_prefix, file_extension, make_unique)
    with open(filename, "w") as outfile:
        outfile.write(content)
    return filename
