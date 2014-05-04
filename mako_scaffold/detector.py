# -*- coding:utf-8 -*-
from zope.interface import implementer
from mako_scaffold.interfaces import ISpecialObjectDetector, IPlugin
import re

## tentative implementation. interface is not fixed.

## see: mako_scaffold.interfaces:ISpecialObjectDetector
@implementer(ISpecialObjectDetector, IPlugin)
class SpecialObjectDetector(object):
    @classmethod
    def create_from_setting(cls, setting):
        return cls()

    def is_rewrite_name(self, dirname):
        return dirname.startswith("+") and dirname.endswith("+")

    def is_rewrite_file(self, filename):
        return filename.endswith(".tmpl")

    def replace_rewrite_file(self, filename):
        return filename.rstrip(".tmpl")

    file_rx = re.compile(r"\+([^+]+?)\+")
    def get_rewrite_patterns(self, filename):
        m = self.file_rx.search(filename)
        return m.group(0), m.group(1)

def includeme(config):
    config.add_plugin("detector", SpecialObjectDetector)
