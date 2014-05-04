# -*- coding:utf-8 -*-
import unittest
import os.path

class DummyReproduction(object):
    def __init__(self, src_root):
        self.src_root = src_root
        self.makedirs = []
        self.files = []
        self.modified_files = []

    def _simplify(self, path):
        return path.replace(self.src_root, ":S:")

    def prepare_for_copy_file(self, dst_path):
        self.makedirs.append(self._simplify(os.path.dirname(dst_path)))

    def prepare_for_copy_directory(self, dir_path):
        self.makedirs.append(self._simplify(dir_path))

    def copy_file(self, src_path, dst_path):
        self.files.append([self._simplify(src_path), self._simplify(dst_path)])

    def modified_copy_file(self, src_path, dst_path):
        self.modified_files.append([self._simplify(src_path), self._simplify(dst_path)])


class FileTreeWalkerTests(unittest.TestCase):
    def _getTarget(self):
        from mako_scaffold.walker import StructualWalker
        return StructualWalker

    def _makeOne(self, input, reproduction):
        from mako_scaffold.detector import SpecialObjectDetector
        detector = SpecialObjectDetector()
        return self._getTarget()(
            input=input, detector=detector, reproduction=reproduction
        )

    def test_it(self):
        from mako_scaffold import testing
        with testing.temporary_environment() as src_dir:
            dst_dir = "/my"

            structure_data = {"+package+": {"setup.py.tmpl": "${package}", "sample.txt": "yay"}}
            testing.file_structure_from_dict(src_dir, structure_data)

            from mako_scaffold.input import DictInput
            input = DictInput({"package": "foo"})
            reproduction = DummyReproduction(src_dir)
            target = self._makeOne(input, reproduction)
            target.walk(os.path.join(src_dir, "+package+"), dst_dir)

            self.assertEqual(len(reproduction.files), 1)
            self.assertEqual(len(reproduction.modified_files), 1)

            self.assertEqual(reproduction.files[0][0], ":S:/+package+/sample.txt")
            self.assertEqual(reproduction.files[0][1], "/my/foo/sample.txt")

            self.assertEqual(reproduction.modified_files[0][0], ":S:/+package+/setup.py.tmpl")
            self.assertEqual(reproduction.modified_files[0][1], "/my/foo/setup.py")


