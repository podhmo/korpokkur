# -*- coding:utf-8 -*-
import pkg_resources
from collections import OrderedDict
from .interfaces import IScaffoldGetter, IPlugin
from zope.interface import implementer
import sys

def err(s):
    sys.stderr.write(s)
    sys.stderr.write("\n")

def out(s):
    sys.stdout.write(s)
    sys.stdout.write("\n")

@implementer(IScaffoldGetter, IPlugin)
class MakoScaffoldGetter(object):
    @classmethod
    def create_from_setting(cls, setting):
        return cls(setting["entry_points_name"])

    def __init__(self, entry_points_name="mako.scaffold", out=err):
        self.entry_points_name = entry_points_name
        self.out = out

    def iterate_scaffolds(self):
        eps = list(pkg_resources.iter_entry_points(self.entry_points_name))
        for entry in eps:
            try:
                scaffold_class = entry.load()
                yield entry.name, scaffold_class
            except Exception as e: # pragma: no cover
                self.out('Warning: could not load entry point %s (%s: %s)' % (
                    entry.name, e.__class__.__name__, e))

    def all_scaffolds(self):
        scaffolds = OrderedDict()
        for name, scaffold_class in self.iterate_scaffolds():
            scaffolds[name] = scaffold_class
        return scaffolds

    def get_scaffold(self, expected_name):
        for name, scaffold_class in self.iterate_scaffolds():
            if name == expected_name:
                return scaffold_class

def includeme(config):
    config.add_plugin("scaffoldgetter", MakoScaffoldGetter)
