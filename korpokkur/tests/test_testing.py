# -*- coding:utf-8 -*-
import unittest

class TemporaryEnvironementTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from korpokkur.testing import temporary_environment
        return temporary_environment(*args, **kwargs)

    def test_it(self):
        import os.path
        dirname = None
        with self._callFUT() as d:
            dirname = d
            self.assertTrue(os.path.exists(d))
            with open(os.path.join(d, "foo.txt"), "w") as wf:
                wf.write("hei")
            self.assertTrue(os.path.exists(dirname))
            self.assertTrue(os.path.exists(os.path.join(d, "foo.txt")))

        self.assertFalse(os.path.exists(dirname))
        self.assertFalse(os.path.exists(os.path.join(dirname, "foo.txt")))


class FileStructureFromDictTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from korpokkur.testing import file_structure_from_dict
        return file_structure_from_dict(*args, **kwargs)

    def test_it(self):
        import os.path
        from korpokkur.testing import temporary_environment
        from korpokkur.compat import text_

        with temporary_environment() as root:
            input_data = {"foo": {"setup.py": ":setup.py:",
                                  "readme.txt": u"日本語", 
                                  "sample": {"foo.txt": "foo"}}}
            self._callFUT(root, input_data)

            is_exists = lambda x : os.path.join(root, x)

            ## file structure
            self.assertTrue(is_exists("foo"))
            self.assertTrue(is_exists("foo/setup.py"))
            self.assertTrue(is_exists("foo/readme.txt"))
            self.assertTrue(is_exists("foo/sample"))
            self.assertTrue(is_exists("foo/sample/foo.txt"))

            def read_data(x):
                with open(os.path.join(root, x)) as rf:
                    return text_(rf.read())

            ## file content
            self.assertEqual(read_data("foo/setup.py"), ":setup.py:")
            self.assertEqual(read_data("foo/readme.txt"), u"日本語")
            self.assertEqual(read_data("foo/sample/foo.txt"), u"foo")
