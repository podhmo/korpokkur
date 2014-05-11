# -*- coding:utf-8 -*-
from zope.interface import implementer
from korpokkur.interfaces import ISpecialObjectDetector, IPlugin
import re

## tentative implementation. interface is not fixed.

## see: korpokkur.interfaces:ISpecialObjectDetector
@implementer(ISpecialObjectDetector, IPlugin)
class SpecialObjectDetector(object):
    @classmethod
    def create_from_setting(cls, setting):
        return cls()

    def is_rewrite_name(self, dirname):
        return self.file_rx.search(dirname) is not None

    def is_rewrite_file(self, filename):
        return filename.endswith(".tmpl")

    def replace_rewrite_file(self, filename):
        return filename[:-5] #xxx

    file_rx = re.compile(r"\+([^+]+?)\+")
    def get_rewrite_patterns(self, filename):
        m = self.file_rx.search(filename)
        return m.group(0), m.group(1)

def includeme(config):
    config.add_plugin("detector", SpecialObjectDetector)
