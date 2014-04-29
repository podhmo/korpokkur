# -*- coding:utf-8 -*-
from zope.interface import (
    Interface, 
    Attribute
)

class IMakoScaffoldTemplate(Interface):
    __doc__ = Attribute("description text of scaffold")

class IConfigurator(Interface):
    def include(module_or_function):
        pass

    def add_plugin(plugin, marker_iface):
        pass

class IPlugin(Interface):
    def create_from_setting(setting):
        pass


###

class ISpecialObjectDetector(Interface):
    def is_template_directory(dirname):
        """ template directory? (default: +package+)"""

    def is_template_file(filename):
        """ template file? (default: filename.mako.tmpl)"""

class IScaffoldGetter(Interface):
    def all_scaffolds():
        pass

    def get_scaffold(expected_name):
        pass
