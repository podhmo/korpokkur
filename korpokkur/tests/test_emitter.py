# -*- coding:utf-8 -*-
import unittest

class TranslatorTests(unittest.TestCase):
    def test_it(self):
        from korpokkur.testing import DummyScaffold
        from korpokkur.emitter import (
            MakoEmitter, 
            InputEnv
        )
        from korpokkur.input import DictInput

        input = DictInput(DummyScaffold(), {"name": "foo"})
        template = "myname is ${name}"

        target = MakoEmitter(InputEnv)
        result = target.emit(template, input)
        self.assertEqual(result, "myname is foo")

    def test_input_commandline(self):
        from korpokkur.testing import DummyScaffold
        from korpokkur.emitter import (
            MakoEmitter, 
            InputEnv
        )
        from korpokkur.input import CommandLineInput
        from io import StringIO
        input_port = StringIO("foo\n")
        output_port = StringIO()

        input = CommandLineInput(DummyScaffold(), input_port, output_port, "{word}?:")
        template = "myname is ${name}"

        target = MakoEmitter(InputEnv)
        result = target.emit(template, input)
        self.assertEqual(result, "myname is foo")

    def test_input_commandline__with_deftemplate(self):
        from korpokkur.testing import DummyScaffold
        from korpokkur.emitter import (
            MakoEmitter, 
            InputEnv
        )
        from korpokkur.input import CommandLineInput
        from io import StringIO
        input_port = StringIO("foo\n")
        output_port = StringIO()

        input = CommandLineInput(DummyScaffold(), input_port, output_port, "{word}?:")
        template = """\
<%def name="greeting(name)">
myname is ${name}
</%def>
${greeting(name)}
${greeting(name)}
"""

        target = MakoEmitter(InputEnv)
        result = target.emit(template, input).replace("\n", "")
        self.assertEqual(result, "myname is foomyname is foo")

