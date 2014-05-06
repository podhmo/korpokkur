# -*- coding:utf-8 -*-
import unittest
from zope.interface import Interface, implementer

class IHasFoo(Interface):
    def foo():
        pass

class Foo(object):
    @classmethod
    def create_from_setting(cls, settings):
        return cls()

    def foo(self):
        return "foo"

class Boo(object):
    @classmethod
    def create_from_setting(cls, settings):
        return cls()

class ConfigurationPluginRegistrationIntegrationTests(unittest.TestCase):
    def _getTarget(self):
        from korpokkur.config import Configurator
        return Configurator

    def _makeOne(self):
        from zope.interface.registry import Components
        return self._getTarget()({}, registry=Components("test"))

    def test_it(self):
        @implementer(IHasFoo)
        class MyFoo(Foo):
            pass

        @implementer(IHasFoo)
        class YourFoo(Foo):
            pass

        target = self._makeOne()

        ## install many plugins about `foo`
        target.add_plugin("my.foo", MyFoo, categoryname="foo")
        target.add_plugin("your.foo", YourFoo, categoryname="foo")

        ## activate my.foo plugin, then, my.foo is used by plugin about `foo`.
        result = target.activate_plugin("my.foo")
        self.assertIsInstance(result, MyFoo)

        ## so, configurator has function about result
        self.assertEqual(target.foo, result)

class ConfigrationPluginMaybeDottedTests(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        from korpokkur.config import Configurator
        from zope.interface.registry import Components
        return Configurator({}, registry=Components("test"))

    def _callFUT(self, *args, **kwargs):
        config = self._makeOne()
        return config.maybe_dotted(*args, **kwargs)

    def test_object(self):
        from korpokkur.interfaces import IPlugin
        result = self._callFUT(IPlugin)
        self.assertEqual(result, IPlugin)

    def test_string__return_object(self):
        from korpokkur.interfaces import IPlugin
        result = self._callFUT("korpokkur.interfaces:IPlugin")
        self.assertEqual(result, IPlugin)

    def test_string_relative__return_object(self):
        from korpokkur.interfaces import IPlugin
        result = self._callFUT("..interfaces:IPlugin")
        self.assertEqual(result, IPlugin)

    def test_string_relative__return_object2(self):
        from korpokkur.interfaces import IPlugin
        def closure():
            result = self._callFUT("..interfaces:IPlugin")
            self.assertEqual(result, IPlugin)
        closure()

    def test_string_relative__return_object3(self):
        from korpokkur.interfaces import IPlugin
        target = self._makeOne()
        def closure():
            result = target.maybe_dotted("..interfaces:IPlugin")
            self.assertEqual(result, IPlugin)
        closure()

    def test_string_relative__return_object4(self):
        from korpokkur.interfaces import IPlugin
        target = self._makeOne()
        def closure():
            from korpokkur.tests import call
            result = call(target, "maybe_dotted", "..interfaces:IPlugin")
            self.assertEqual(result, IPlugin)
        closure()


class ConfiguratorAddPluginTests(unittest.TestCase):
    def _getTarget(self):
        from korpokkur.config import Configurator
        return Configurator

    def _makeOne(self):
        from zope.interface.registry import Components
        return self._getTarget()({}, registry=Components("test"))

    def test_passing_iface_directly__ok(self):
        class MyFoo(Foo):
            pass

        target = self._makeOne()

        target.add_plugin("foo.my", MyFoo, iface=IHasFoo)
        self.assertEqual(target.lookup_implementation(IHasFoo, "foo.my"), MyFoo)

    def test_strict_true_and_passing_bad_implementation__raise_error(self):
        from zope.interface.exceptions import BrokenImplementation

        class MyBoo(Boo):
            pass

        target = self._makeOne()
        with self.assertRaisesRegexp(BrokenImplementation, "foo attribute was not provided"):
            target.add_plugin("boo.my", MyBoo, iface=IHasFoo)

    def test_strict_false_and_passing_bad_implementation__treat_as_ok(self):
        class MyBoo(Boo):
            pass

        target = self._makeOne()

        target.add_plugin("boo.my", MyBoo, iface=IHasFoo, strict=False)
        self.assertEqual(target.lookup_implementation(IHasFoo, "boo.my"), MyBoo)

    def test_categorized_by_category_name(self):
        @implementer(IHasFoo)
        class MyFoo(Foo):
            pass

        target = self._makeOne()

        target.add_plugin("foo.my", MyFoo, categoryname="foo")
        self.assertEqual(target.installed_plugin_repository["foo.my"], (IHasFoo, "foo"))


