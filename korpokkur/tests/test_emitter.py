# -*- coding:utf-8 -*-
import unittest
import os.path

class MakoEmitterTests(unittest.TestCase):
    def _makeCommandLineInput(self, input_string):
        from korpokkur.testing import DummyScaffold
        from korpokkur.input import CommandLineInput
        from ..compat import NativeIO
        input_port = NativeIO(input_string)
        output_port = NativeIO()
        error_port = NativeIO()

        return CommandLineInput(DummyScaffold(),
                                 input_port, output_port, error_port, 
                                 prompt="{word}?:")

    def _makeDictInput(self, cache):
        from korpokkur.testing import DummyScaffold
        from korpokkur.input import DictInput
        return DictInput(DummyScaffold(), cache)

    def test_it(self):
        from korpokkur.emitter.mako import (
            MakoEmitter, 
            InputEnv
        )

        input = self._makeDictInput({"name": "foo"})
        template = "myname is ${name}"

        target = MakoEmitter(InputEnv)
        result = target.emit(input, text=template)
        self.assertEqual(result, "myname is foo")

    HERE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
    def test_input_dict__lookup_template_filename(self):
        from korpokkur.emitter.mako import (
            MakoEmitter, 
            InputEnv
        )

        input = self._makeDictInput({"name": "foo"})
        filename = os.path.join(self.HERE, "hello.mako")

        target = MakoEmitter(InputEnv)
        result = target.emit(input, filename=filename)
        self.assertEqual(result.rstrip(), "hello foo")

    def test_input_dict__lookup_template_filename__with_namespace(self):
        from korpokkur.emitter.mako import (
            MakoEmitter, 
            InputEnv
        )

        input = self._makeDictInput({"name": "foo"})
        filename = os.path.join(self.HERE, "hello_with_helpers.mako")

        target = MakoEmitter(InputEnv)
        result = target.emit(input, filename=filename)
        self.assertEqual(result.strip(), "foo,foo")

    def test_input_commandline(self):
        from korpokkur.emitter.mako import (
            MakoEmitter,
            InputEnv
        )

        input = self._makeCommandLineInput(input_string="foo\n")
        template = "myname is ${name}"

        target = MakoEmitter(InputEnv)
        result = target.emit(input, text=template)
        self.assertEqual(result, "myname is foo")

    def test_input_commandline__with_deftemplate(self):
        from korpokkur.emitter.mako import (
            MakoEmitter,
            InputEnv
        )

        input = self._makeCommandLineInput(input_string="foo\n")
        template = """\
<%def name="greeting(name)">
myname is ${name}
</%def>
${greeting(name)}
${greeting(name)}
"""

        target = MakoEmitter(InputEnv)
        result = target.emit(input, text=template).replace("\n", "")
        self.assertEqual(result, "myname is foomyname is foo")


class Jinja2EmitterTests(unittest.TestCase):
    def test_it(self):
        from korpokkur.testing import DummyScaffold
        from korpokkur.emitter.jinja2 import (
            Jinja2Emitter, 
            InputEnv
        )
        from korpokkur.input import DictInput

        input = DictInput(DummyScaffold(), {"name": "foo"})
        template = "myname is {{name}}"

        target = Jinja2Emitter(InputEnv)
        result = target.emit(input, text=template)
        self.assertEqual(result, "myname is foo")

    def test_input_commandline(self):
        from korpokkur.testing import DummyScaffold
        from korpokkur.emitter.jinja2 import (
            Jinja2Emitter, 
            InputEnv
        )
        from korpokkur.input import CommandLineInput
        from ..compat import NativeIO
        input_port = NativeIO("foo\n")
        output_port = NativeIO()
        error_port = NativeIO()

        input = CommandLineInput(DummyScaffold(),
                                 input_port, output_port, error_port, 
                                 prompt="{word}?:")
        template = "myname is {{name}}"

        target = Jinja2Emitter(InputEnv)
        result = target.emit(input, text=template)
        self.assertEqual(result, "myname is foo")

    @unittest.skip("jinja2 not support define function on runtime?")
    def test_input_commandline__with_deftemplate(self):
        from korpokkur.testing import DummyScaffold
        from korpokkur.emitter.jinja2 import (
            Jinja2Emitter, 
            InputEnv
        )
        from korpokkur.input import CommandLineInput
        from ..compat import NativeIO
        input_port = NativeIO("foo\n")
        output_port = NativeIO()

        input = CommandLineInput(DummyScaffold(), input_port, output_port, "{word}?:")
        template = """\
<%def name="greeting(name)">
myname is ${name}
</%def>
${greeting(name)}
${greeting(name)}
"""

        target = Jinja2Emitter(InputEnv)
        result = target.emit(input, text=template).replace("\n", "")
        self.assertEqual(result, "myname is foomyname is foo")
