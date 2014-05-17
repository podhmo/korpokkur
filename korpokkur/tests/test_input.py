# -*- coding:utf-8 -*-
import unittest

class CompputeValueTests(unittest.TestCase):
    def _callFUT(self, input, name):
        return input.load(name)

    def _makeDictInput(self, *args, **kwargs):
        from korpokkur.input import DictInput
        scaffold = None
        return DictInput(scaffold, *args, **kwargs)

    def _makeCommandlineInput(self, *args, **kwargs):
        from korpokkur.input import CommandLineInput
        from korpokkur.testing import DummyScaffold
        scaffold = DummyScaffold({"package": ("package name", "sample")})
        return CommandLineInput(scaffold, *args, **kwargs)

    def _getComputeValueDefinition(self, compute_value_called):
        from korpokkur.input import compute_value
        @compute_value
        def get_basename(input, name):
            import os.path
            compute_value_called.append(True)
            fullpath = input.load("fullpath")
            return os.path.basename(fullpath)
        return get_basename

    def test_with_dict_input__exists_compute_value__ok(self):
        compute_value_called = []
        get_basename = self._getComputeValueDefinition(compute_value_called)

        cache = {
            "fullpath":"/tmp/foo/bar.txt", 
            "basename": get_basename, 
        }
        input = self._makeDictInput(cache)

        result = input.load("basename")
        self.assertEqual(result, "bar.txt")

    def test_with_dict_input__does_not_exists_compute_value__raise_exception(self):
        compute_value_called = []
        get_basename = self._getComputeValueDefinition(compute_value_called)

        cache = {
            "fullpath":"/tmp/foo/bar.txt", 
            "_basename": get_basename, 
        }
        input = self._makeDictInput(cache)

        with self.assertRaisesRegexp(KeyError, "basename"):
            input.load("basename")

    def test_with_dict_input__compute_value_is_cached(self):
        compute_value_called = []
        get_basename = self._getComputeValueDefinition(compute_value_called)

        cache = {
            "fullpath":"/tmp/foo/bar.txt", 
            "basename": get_basename, 
        }
        input = self._makeDictInput(cache)

        result = input.load("basename")
        result = input.load("basename")
        result = input.load("basename")
        self.assertEqual(result, "bar.txt")

        self.assertEqual(compute_value_called, [True])


    def test_with_commadline_input__compute_value_exists__ok(self):
        from ..compat import NativeIO
        input_port = NativeIO("/tmp/foo/bar.txt")
        output_port = NativeIO()
        error_port = NativeIO()
        target = self._makeCommandlineInput(input_port, output_port, error_port)

        compute_value_called = []
        get_basename = self._getComputeValueDefinition(compute_value_called)
        target.update({"basename": get_basename})

        result = target.load("basename")
        self.assertEqual(result, "bar.txt")


class CommandLineInputReadTests(unittest.TestCase):
    def _getTarget(self):
        from korpokkur.input import CommandLineInput
        return CommandLineInput

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_read_input_value_is_stored(self):
        from korpokkur.testing import DummyScaffold
        from ..compat import NativeIO
        input_port = NativeIO("foo\n")
        output_port = NativeIO()
        error_port = NativeIO()

        scaffold = DummyScaffold({})

        target = self._makeOne(scaffold, input_port, output_port, error_port)
        self.assertNotIn("package", target)
        target.read("package")

        self.assertIn("package", target)
        self.assertEqual(target.load("package"), "foo")


    def test_read__expected_word_found__gently_prompt(self):
        from korpokkur.testing import DummyScaffold
        from ..compat import NativeIO
        input_port = NativeIO()
        output_port = NativeIO()
        error_port = NativeIO()

        scaffold = DummyScaffold({"package": ("package name", "sample")})

        target = self._makeOne(scaffold, input_port, output_port, error_port)
        target.read("package")
        self.assertEqual(error_port.getvalue(), "package (package name)[sample]:")

    def test_read__expected_word_not_found__bluntly_prompt(self):
        from korpokkur.testing import DummyScaffold
        from ..compat import NativeIO
        input_port = NativeIO()
        output_port = NativeIO()
        error_port = NativeIO()

        scaffold = DummyScaffold({"package": ("package name", "sample")})

        target = self._makeOne(scaffold, input_port, output_port, error_port)
        target.read("version")
        self.assertEqual(error_port.getvalue(), "version?:")

