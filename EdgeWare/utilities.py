#!/usr/bin/python
import os
from pathlib import PurePosixPath

def convert_path(path):
    if os.name == 'posix':
        return PurePosixPath(path)
    else:
        return path