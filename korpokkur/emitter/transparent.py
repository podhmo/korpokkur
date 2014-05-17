# -*- coding:utf-8 -*-
from zope.interface import implementer
from korpokkur.interfaces import IEmitter

## see: korpokkur.interfaces:IEmitter
@implementer(IEmitter)
class TransparentEmitter(object):
    @classmethod
    def create_from_setting(cls, settings):
        return cls()

    def __init__(self, open=open):
        self.open = open

    def emit(self, input, text="", filename=""):
        assert text or filename
        if text:
            return text
        with self.open(filename) as rf:
            return rf.read()

def includeme(config):
    config.add_plugin("emitter.transparent", TransparentEmitter, categoryname="emitter")

