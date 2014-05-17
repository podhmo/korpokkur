# -*- coding:utf-8 -*-
import logging
import os.path
logger = logging.getLogger(__name__)
import tempfile
import contextlib
import shutil
from .reproduction import FileConflict
from .compat import (
    FileNotFoundError, 
    bytes_
)

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
            with open(root, "wb") as wf:
                wf.write(bytes_(D))
        except FileNotFoundError:
            os.makedirs(os.path.dirname(root))
            with open(root, "wb") as wf:
                wf.write(bytes_(D))

## dummy object
class DummyScaffold(object):
    default_expected_words = {
        "_varname" : ("_description", "_default")
    }
    def __init__(self, words=None, marker_comments=None):
        self.expected_words = words or self.default_expected_words
        self.source_directory = "."
        if marker_comments:
            self.marker_comments = marker_comments

class DummyReproduction(object):
    def __init__(self, src_root):
        self.src_root = src_root
        self.makedirs = []
        self.files = []
        self.modified_files = []

    def _simplify(self, path):
        return path.replace(self.src_root, ":S:")

    def is_copy_file_ng(self, dst_path, overwrite):
        if overwrite:
            return False
        k = self._simplify(dst_path)
        return k in [f[1] for f in self.files] or k in [f[1] for f in self.modified_files]

    def prepare_for_copy_file(self, dst_path, overwrite):
        if self.is_copy_file_ng(dst_path, overwrite):
            raise FileConflict(dst_path)
        self.makedirs.append(self._simplify(os.path.dirname(dst_path)))

    def prepare_for_copy_directory(self, dir_path):
        self.makedirs.append(self._simplify(dir_path))

    def copy_file(self, src_path, dst_path):
        self.files.append([self._simplify(src_path), self._simplify(dst_path)])

    def modified_copy_file(self, src_path, dst_path):
        self.modified_files.append([self._simplify(src_path), self._simplify(dst_path)])
