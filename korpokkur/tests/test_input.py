# -*- coding:utf-8 -*-
import unittest

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
        scaffold = DummyScaffold({})

        target = self._makeOne(scaffold, input_port, output_port)
        self.assertNotIn("package", target)
        target.read("package")

        self.assertIn("package", target)
        self.assertEqual(target.load("package"), "foo")


    def test_read__expected_word_found__gently_prompt(self):
        from korpokkur.testing import DummyScaffold
        from ..compat import NativeIO
        input_port = NativeIO()
        output_port = NativeIO()
        scaffold = DummyScaffold({"package": ("package name", "sample")})

        target = self._makeOne(scaffold, input_port, output_port)
        target.read("package")
        self.assertEqual(output_port.getvalue(), "package (package name)[sample]:")

    def test_read__expected_word_not_found__bluntly_prompt(self):
        from korpokkur.testing import DummyScaffold
        from ..compat import NativeIO
        input_port = NativeIO()
        output_port = NativeIO()
        scaffold = DummyScaffold({"package": ("package name", "sample")})

        target = self._makeOne(scaffold, input_port, output_port)
        target.read("version")
        self.assertEqual(output_port.getvalue(), "version?:")

