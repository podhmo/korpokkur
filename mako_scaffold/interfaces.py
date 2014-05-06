# -*- coding:utf-8 -*-
from zope.interface import (
    Interface,
    Attribute
)

class IScaffoldTemplate(Interface):
    __doc__ = Attribute("description text of scaffold")
    source_directory = Attribute("source directory for template")
    expected_words = Attribute("key and description list of rendering values")
    __dro__ = Attribute("delegation resolution order") #optional

class IScaffold(Interface):
    source_directory = Attribute("source directory for template")
    expected_words = Attribute("key and description list of rendering values")
    def iterate_children():
        pass

    def walk(walker, dst):
        pass

class IConfigurator(Interface):
    def include(module_or_function):
        pass

    def add_plugin(name, plugin, iface=None, categoryname=None):
        pass

    def activate_plugin(name, *args, **kwargs):
        pass

class IPlugin(Interface):
    def create_from_setting(setting): #classmethod
        pass


###
class IInput(Interface):
    def load(word, reload=False):
        """ load from cache if not found read from anywhere"""

    def read(word):
        """ read data"""

    loaded_map = Attribute("loaded pair store")

class ISpecialObjectDetector(Interface):
    def is_rewrite_name(dirname):
        """ template directory? (default: +package+)"""

    def is_rewrite_file(filename):
        """ template file? (default: filename.mako.tmpl)"""

    def replace_rewrite_file(filename):
        pass

    def get_rewrite_patterns(filename):
        pass

class IScaffoldGetter(Interface):
    def all_scaffolds():
        pass

    def get_scaffold(expected_name):
        pass

class ITreeWalker(Interface):
    def walk(root, dst):
        pass

class IEmitter(Interface):
    def emit(template, input): #input is IInput
        pass

class IReproduction(Interface):
    def prepare_for_copy_file(dst_path, overwrite):
        pass

    def prepare_for_copy_directory(dir_path):
        pass

    def copy_file(src_path, dst_path):
        pass

    def modified_copy_file(src_path, dst_path):
        pass
