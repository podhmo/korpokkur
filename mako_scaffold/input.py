# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import sys
from zope.interface import implementer
from mako_scaffold.interfaces import IInput

## see: mako_scaffold.interfaces:IInput
@implementer(IInput)
class DictInput(object):
    @classmethod
    def create_from_setting(cls, settings, scaffold, data):
        return cls(scaffold, data)

    def __init__(self, scaffold, D):
        self.scaffold = scaffold
        self.cache = D.copy()
        self.loaded_map = D

    def load_with_default(self, k, default=None):
        return self.cache.get(k, default)

    def load(self, k, reload=False):
        return self.cache[k]

    def read(self, k):
        return self.cache[k]

    def save(self, k, v):
        self.cache[k] = v

    def copy(self):
        self.__class__(self.scaffold, self.cache.copy())

    def update(self, d):
        self.cache.update(d)

    def __iter__(self):
        return iter(self.cache)


## see: mako_scaffold.interfaces:IInput
@implementer(IInput)
class CommandLineInput(object):
    prompt = "{word}?:"
    @classmethod
    def create_from_setting(cls, settings, scaffold):
        return cls(sys.stdin, sys.stdout, prompt=settings["input.prompt"]) ##TODO: get prompt via scaffold

    def __init__(self, scaffold, input_port, output_port, prompt):
        self.scaffold = scaffold
        self.input_port = input_port
        self.output_port = output_port
        self.prompt = prompt
        self.cache = {}
        self.loaded_map = {}

    def load(self, word, reload=False):
        if reload:
            return self.read(word)
        try:
            return self.cache[word]
        except KeyError:
            return self.read(word)

    def load_with_default(self, word, default=None):
        try:
            return self.load(word)
        except KeyError:
            return default

    def read(self, word):
        self.output_port.write(self.prompt.format(word=word))
        self.output_port.flush()

        value = self.input_port.readline().rstrip()
        self.cache[word] = value
        self.loaded_map[word] = value
        return value

    def save(self, word, value):
        self.cache[word] = value

    def copy(self):
        o = self.__class__(self.scaffold, self.input_port, self.output_port, self.prompt)
        o.cache = self.cache.copy()
        return o

    def update(self, d):
        self.cache.update(d)

    def __iter__(self):
        return iter(self.cache)



## todo: from file?, ini file?
def includeme(config):
    config.add_plugin("input.cli", CommandLineInput, categoryname="input")
    config.add_plugin("input.dict", DictInput, categoryname="input")
