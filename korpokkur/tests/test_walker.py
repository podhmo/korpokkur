# -*- coding:utf-8 -*-
import unittest
import os.path

class GetPrefixTests(unittest.TestCase):
    def _getTarget(self):
        from korpokkur.walker import StructualWalker
        return StructualWalker

    def _makeOne(self, input, reproduction):
        from korpokkur.detector import SpecialObjectDetector
        detector = SpecialObjectDetector()
        return self._getTarget()(
            input=input, detector=detector, reproduction=reproduction
        )

    def test_for_create__skiptop_is_False__include_toplevel_dirname(self):
        from korpokkur import testing
        from korpokkur.input import DictInput

        ## /my/scaffolds/+package+/sample.txt -> /tmp/foo/sample.txt
        root = "/my/scaffolds/+package+"
        package = "foo"
        dst = "/tmp"
        skiptop = False

        input = DictInput(testing.DummyScaffold(), {"package": package})
        reproduction = testing.DummyReproduction(root)
        target = self._makeOne(input, reproduction)

        result = target.get_prefix(root, dst, {}, skiptop=skiptop)
        self.assertEqual(result, "/tmp/foo")

    def test_for_add__skiptop_is_True__without_toplevel_dirname(self):
        from korpokkur import testing
        from korpokkur.input import DictInput

        ## /my/scaffolds/+package+/sample.txt -> /tmp/sample.txt
        root = "/my/scaffolds/+package+"
        package = "foo"
        dst = "/tmp"
        skiptop = True

        input = DictInput(testing.DummyScaffold(), {"package": package})
        reproduction = testing.DummyReproduction(root)
        target = self._makeOne(input, reproduction)

        result = target.get_prefix(root, dst, {}, skiptop=skiptop)
        self.assertEqual(result, "/tmp")



class FileTreeWalkerTests(unittest.TestCase):
    def _getTarget(self):
        from korpokkur.walker import StructualWalker
        return StructualWalker

    def _makeOne(self, input, reproduction):
        from korpokkur.detector import SpecialObjectDetector
        detector = SpecialObjectDetector()
        return self._getTarget()(
            input=input, detector=detector, reproduction=reproduction
        )

    def test_it(self):
        from korpokkur import testing
        with testing.temporary_environment() as src_dir:
            dst_dir = "/my"

            structure_data = {"+package+": {"setup.py.tmpl": "${package}", "sample.txt": "yay"}}
            testing.file_structure_from_dict(src_dir, structure_data)

            from korpokkur.input import DictInput
            input = DictInput(testing.DummyScaffold(), {"package": "foo"})
            reproduction = testing.DummyReproduction(src_dir)
            target = self._makeOne(input, reproduction)
            target.walk(os.path.join(src_dir, "+package+"), dst_dir)

            self.assertEqual(len(reproduction.files), 1)
            self.assertEqual(len(reproduction.modified_files), 1)

            self.assertEqual(reproduction.files[0][0], ":S:/+package+/sample.txt")
            self.assertEqual(reproduction.files[0][1], "/my/foo/sample.txt")

            self.assertEqual(reproduction.modified_files[0][0], ":S:/+package+/setup.py.tmpl")
            self.assertEqual(reproduction.modified_files[0][1], "/my/foo/setup.py")


    def test_conflict__overwrite_is_false__then_exception_is_raised(self):
        from korpokkur import testing
        from korpokkur import FileConflict
        with testing.temporary_environment() as src_dir:
            dst_dir = "/my"

            structure_data = {"+package+": {"setup.py.tmpl": "${package}", "sample.txt": "yay"}}
            testing.file_structure_from_dict(src_dir, structure_data)

            from korpokkur.input import DictInput
            input = DictInput(testing.DummyScaffold(), {"package": "foo"})
            reproduction = testing.DummyReproduction(src_dir)

            with self.assertRaises(FileConflict):
                target = self._makeOne(input, reproduction)
                target.walk(os.path.join(src_dir, "+package+"), dst_dir, overwrite=False)
                target = self._makeOne(input, reproduction)
                target.walk(os.path.join(src_dir, "+package+"), dst_dir, overwrite=False)

    def test_conflict__overwrite_is_true__ok(self):
        from korpokkur import testing
        with testing.temporary_environment() as src_dir:
            dst_dir = "/my"

            structure_data = {"+package+": {"setup.py.tmpl": "${package}", "sample.txt": "yay"}}
            testing.file_structure_from_dict(src_dir, structure_data)

            from korpokkur.input import DictInput
            input = DictInput(testing.DummyScaffold(), {"package": "foo"})
            reproduction = testing.DummyReproduction(src_dir)

            target = self._makeOne(input, reproduction)
            target.walk(os.path.join(src_dir, "+package+"), dst_dir, overwrite=True)
            target = self._makeOne(input, reproduction)
            target.walk(os.path.join(src_dir, "+package+"), dst_dir, overwrite=True)
