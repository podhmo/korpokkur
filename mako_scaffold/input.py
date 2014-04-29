# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import sys
from zope.interface import implementer
from mako_scaffold.interfaces import IInput

## see: mako_scaffold.interfaces:IInput
@implementer(IInput)
class CommandLineInput(object):
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

    def read(self, word):
        self.output_port.write(self.prompt.format(word=word))
        self.output_port.flush()

        value = self.input_port.readline().rstrip()
        self.cache[word] = value
        return value

## todo: from file?, ini file?
def includeme(config):
    config.add_plugin("input.cli", CommandLineInput, categoryname="input")
