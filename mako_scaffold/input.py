# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import sys
from zope.interface import implementer
from mako_scaffold.interfaces import IInput

## see: mako_scaffold.interfaces:IInput
@implementer(IInput)
class DictInput(object):
    def __init__(self, D):
        self.D = D

    def load_with_default(self, k, default=None):
        return self.D.get(k, default)

    def load(self, k, reload=False):
        return self.D[k]

    def read(self, k):
        return self.D[k]

    def save(self, k, v):
        self.D[k] = v

    def copy(self):
        self.__class__(self.D.copy())

    def update(self, d):
        self.D.update(d)

    def __iter__(self):
        return iter(self.D)

## see: mako_scaffold.interfaces:IInput
@implementer(IInput)
class CommandLineInput(object):
    prompt = "{word}?:"
    @classmethod
    def create_from_setting(cls, settings):
        return cls(sys.stdin, sys.stdout, prompt=settings["input.prompt"])

    def __init__(self, input_port, output_port, prompt):
        self.input_port = input_port
        self.output_port = output_port
        self.prompt = prompt
        self.cache = {}

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
        return value

    def save(self, word, value):
        self.cache[word] = value

    def copy(self):
        o = self.__class__(self.input_port, self.output_port, self.prompt)
        o.cache = self.cache.copy()
        return o

    def update(self, d):
        self.cache.update(d)

    def __iter__(self):
        return iter(self.cache)

## todo: from file?, ini file?
def includeme(config):
    config.add_plugin("input.cli", CommandLineInput, categoryname="input")
