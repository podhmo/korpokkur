# -*- coding:utf-8 -*-
import unittest

class InputEnvTreatsAsDictTests(unittest.TestCase):
    def _getTarget(self):
        from korpokkur.emitter import InputEnv
        return InputEnv

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_use_star_star_mapping__dict_input(self):
        from collections import Mapping
        from korpokkur.input import DictInput

        input = DictInput(None, {"a": "b"})
        target = self._makeOne(input)

        def use_star_star_mappingn(**kwargs):
            self.assertEqual(kwargs["a"], "b")

        self.assertIsInstance(target, Mapping)
        use_star_star_mappingn(**target)

    def test_use_star_star_mapping__commandline_input(self):
        from collections import Mapping
        from korpokkur.input import CommandLineInput
        from korpokkur.compat import NativeIO

        input_port = NativeIO()
        error_port = NativeIO()
        output_port = NativeIO()

        input = CommandLineInput(None, input_port, output_port, error_port)
        input.update({"a": "b"})
        target = self._makeOne(input)

        def use_star_star_mappingn(**kwargs):
            self.assertEqual(kwargs["a"], "b")

        self.assertIsInstance(target, Mapping)
        use_star_star_mappingn(**target)
