# -*- coding:utf-8 -*-
from zope.interface import implementer
from mako_scaffold.interfaces import ISpecialObjectDetector, IPlugin

## see: mako_scaffold.interfaces:ISpecialObjectDetector
@implementer(ISpecialObjectDetector, IPlugin)
class SpecialObjectDetector(object):
    @classmethod
    def create_from_setting(cls, setting):
        return cls()

    def is_rewrite_directory(self, dirname):
        return dirname.startswith("+") and dirname.endswith("+")

    def is_rewrite_file(self, filename):
        return filename.endswith(".tmpl")

def includeme(config):
    config.add_plugin("detector", SpecialObjectDetector)
