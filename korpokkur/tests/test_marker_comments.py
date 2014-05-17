# -*- coding:utf-8 -*-
import unittest


class FilterSettingsTests(unittest.TestCase):
    def _makeOne(self, config, plugin_name):
        emitter = None
        input = None
        return config.activate_plugin(plugin_name, emitter=emitter, input=input)

    def test_it_physical_reproduction(self):
        from configless import Configurator
        from korpokkur.interfaces import IAfterEmitFilter

        config = Configurator({})
        config.include("korpokkur.reproduction")

        target = self._makeOne(config, "reproduction.physical")
        self.assertTrue(IAfterEmitFilter.providedBy(target.after_emit_filter))

    def test_it_simulation_reproduction(self):
        from configless import Configurator
        from korpokkur.interfaces import IAfterEmitFilter

        config = Configurator({})
        config.include("korpokkur.reproduction")

        target = self._makeOne(config, "reproduction.simulation")
        self.assertTrue(IAfterEmitFilter.providedBy(target.after_emit_filter))

class MarkerCommentsTests(unittest.TestCase):
    def _getTarget(self):
        from korpokkur.reproduction import marker_comments_filter
        return marker_comments_filter

    def _makeOne(self, emitter, input):
        from korpokkur.reproduction import SimulateReproduction
        return SimulateReproduction(emitter, input, self._getTarget())

    def test_emit_marker_comment_does_not_exists__noeffect(self):
        import contextlib
        from korpokkur.testing import DummyScaffold
        from korpokkur.input import DictInput
        from korpokkur.emitter.transparent import TransparentEmitter

        template_data = """sample text"""
        @contextlib.contextmanager
        def dummy_open(xxx):
            class rf:
                read = staticmethod(lambda : template_data)
            yield rf

        emitter = TransparentEmitter(dummy_open)
        scaffold = DummyScaffold(marker_comments={"*replace*": "###this is marker comment***"})
        input = DictInput(scaffold, {"*replace*": "config.add_route('sample')"})

        target = self._makeOne(emitter, input)
        result = target.modified_copy_file("/src/file.txt.tmpl", "/dst/file.txt")

        self.assertEqual(result, """sample text""")

    def test_emit_marker_comment_without_padding(self):
        import contextlib
        from korpokkur.testing import DummyScaffold
        from korpokkur.input import DictInput
        from korpokkur.emitter.transparent import TransparentEmitter

        template_data = """\
this is test message
###this is marker comment***
end of message
"""
        @contextlib.contextmanager
        def dummy_open(xxx):
            class rf:
                read = staticmethod(lambda : template_data)
            yield rf

        emitter = TransparentEmitter(dummy_open)
        scaffold = DummyScaffold(marker_comments={"*replace*": "###this is marker comment***"})
        input = DictInput(scaffold, {"*replace*": "* ha * ha * ha * ha *"})

        target = self._makeOne(emitter, input)
        result = target.modified_copy_file("/src/file.txt.tmpl", "/dst/file.txt")

        text = result.split("\n")
        self.assertEqual("this is test message", text[0])
        self.assertEqual("###this is marker comment***", text[1])
        self.assertEqual("* ha * ha * ha * ha *", text[2])
        self.assertEqual("end of message", text[3])


    def test_emit_marker_comment_with_padding(self):
        import contextlib
        from korpokkur.testing import DummyScaffold
        from korpokkur.input import DictInput
        from korpokkur.emitter.transparent import TransparentEmitter

        template_data = """\
def includeme(config):
    config.add_route('foo')
    ###this is marker comment***
    config.scan('.views')
"""
        @contextlib.contextmanager
        def dummy_open(xxx):
            class rf:
                read = staticmethod(lambda : template_data)
            yield rf

        emitter = TransparentEmitter(dummy_open)
        scaffold = DummyScaffold(marker_comments={"*replace*": "###this is marker comment***"})
        input = DictInput(scaffold, {"*replace*": "config.add_route('sample')"})

        target = self._makeOne(emitter, input)
        result = target.modified_copy_file("/src/file.txt.tmpl", "/dst/file.txt")

        text = result.split("\n")
        self.assertEqual("def includeme(config):", text[0])
        self.assertEqual("    config.add_route('foo')", text[1])
        self.assertEqual("    ###this is marker comment***", text[2])
        self.assertEqual("    config.add_route('sample')", text[3])
        self.assertEqual("    config.scan('.views')", text[4])
