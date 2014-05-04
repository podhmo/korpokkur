# -*- coding:utf-8 -*-
import logging
import os.path
logger = logging.getLogger(__name__)
import tempfile
import contextlib
import shutil

@contextlib.contextmanager
def temporary_environment(cleanup=True):
    try:
        root = tempfile.mkdtemp()
        yield root
    finally:
        if cleanup and os.path.exists(root):
            shutil.rmtree(root)

def file_structure_from_dict(root, D):
    """
D = {"foo": {"setup.py": "testest",
             "readme.txt": "testtest", 
             "sample": {"foo.txt": "foo"}}}
    """
    if hasattr(D, "items"):
        for name, val in D.items():
            file_structure_from_dict(os.path.join(root, name), val)
    else:
        try:
            with open(root, "w") as wf:
                wf.write(D)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(root))
            with open(root, "w") as wf:
                wf.write(D)
