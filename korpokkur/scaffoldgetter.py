# -*- coding:utf-8 -*-
import pkg_resources
import re
from collections import OrderedDict
from . import (
    NotSupportExtension, 
    ScaffoldNotFound
)
from .langhelper import import_symbol
from .interfaces import (
    IScaffold,
    IScaffoldGetter,
    IPlugin
)
from zope.interface import implementer
import sys

def err(s):
    sys.stderr.write(s)
    sys.stderr.write("\n")

def out(s):
    sys.stdout.write(s)
    sys.stdout.write("\n")

## see: korpokkur.interfaces:IScaffold
@implementer(IScaffold)
class Scaffold(object):
    def __init__(self, template, lookup=import_symbol, extensions=None):
        self.template = template
        self.lookup = lookup
        self.extensions = extensions


    @property
    def marker_comments(self):
        return getattr(self.template, "marker_comments", {})

    @property
    def source_directory(self):
        return self.template.source_directory

    @property
    def expected_words(self):
        return self.template.expected_words

    def iterate_children(self, iterated=None):
        iterated = iterated or set()
        iterated.add(self.template)
        for sym in  getattr(self.template, "__dro__", []):
            template = self.lookup(sym)
            if not template in iterated:
                iterated.add(self.template)
                sub = self.__class__(template, lookup=self.lookup)
                yield sub
                for subsub in sub.iterate_children(iterated=iterated):
                    yield subsub

    def walk(self, walker, dst, overwrite=True, skiptop=False):
        if hasattr(self.template, "cache"):
            walker.input.update(self.template.cache)

        ## todo: reserved word "extensions"
        if self.extensions is not None: #xxx:
            walker.input.update({":extensions:": self.extensions})
        walker.walk(self.source_directory, dst, overwrite=overwrite, skiptop=skiptop)
        for sub_scaffold in self.iterate_children():
            sub_scaffold.walk(walker, dst, overwrite=overwrite)


## see: korpokkur.interfaces:IScaffoldGetter
@implementer(IScaffoldGetter, IPlugin)
class ScaffoldGetter(object):
    scaffold_name_rx = re.compile(r"(\S+)\s*\[(.+)\]")
    _import_symbol = staticmethod(import_symbol)

    @classmethod
    def create_from_setting(cls, setting, factory=Scaffold):
        return cls(setting["entry_points_name"], factory=factory)

    def __init__(self, entry_points_name="korpokkur.scaffold", out=err, factory=Scaffold):
        self.entry_points_name = entry_points_name
        self.out = out
        self.factory = factory

    def iterate_scaffolds(self, entry_points_name=None):
        entry_points_name = entry_points_name or self.entry_points_name
        eps = list(pkg_resources.iter_entry_points(entry_points_name))
        for entry in eps:
            try:
                scaffold_class = entry.load()
                yield entry.name, scaffold_class
            except Exception as e: # pragma: no cover
                self.out('Warning: could not load entry point %s (%s: %s)' % (
                    entry.name, e.__class__.__name__, e))

    def all_scaffolds(self, entry_points_name=None):
        entry_points_name = entry_points_name or self.entry_points_name
        scaffolds = OrderedDict()
        for name, scaffold_class in self.iterate_scaffolds(entry_points_name=entry_points_name):
            scaffolds[name] = scaffold_class
        return scaffolds

    def split_scaffold_name(self, name):
        m = self.scaffold_name_rx.search(name)
        if m:
            return m.group(1), set(e for e in m.group(2).split(" ") if not e == "")
        else:
            return name, set()

    def get_scaffold(self, expected_name):
        expected_name, extensions = self.split_scaffold_name(expected_name)
        for name, template_class in self.iterate_scaffolds():
            if name == expected_name:
                if (extensions and hasattr(template_class, "support_extensions")):
                    extensions = extensions.intersection(template_class.support_extensions)
                    if not extensions:
                        raise NotSupportExtension(expected_name)
                return self.factory(template_class, 
                                    lookup=self._import_symbol,
                                    extensions=extensions)
        raise ScaffoldNotFound(expected_name)

def includeme(config):
    config.add_plugin("scaffoldgetter", ScaffoldGetter)
