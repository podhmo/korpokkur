# -*- coding:utf-8 -*-
from zope.interface import implementer
from mako_scaffold.interfaces import ITreeWalker, IPlugin
import os
import os.path

## see: mako_scaffold.interfaces:ITreeWalker
@implementer(ITreeWalker, IPlugin)
class StructualWalker(object):
    @classmethod
    def create_from_setting(cls, setting, detector):
        return cls(detector)

    def __init__(self, detector):
        self.detector = detector

    def walk(self, root):
        for r, ds, fs in os.walk(root):
            for f in fs:
                filename = os.path.join(r, f)
                print(filename)


def includeme(config):
    config.add_plugin("walker", StructualWalker)
