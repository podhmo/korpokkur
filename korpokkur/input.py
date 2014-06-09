# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import sys
from zope.interface import (
    implementer, 
    provider
)
from korpokkur.interfaces import (
    IInput, 
    IComputeValue
)

def cached_call(cache, k, fn):
    def callee(*args, **kwargs):
        v = fn(*args, **kwargs)
        cache[k] = v
        return v
    return callee

def is_compute_value(v):
    try:
        return callable(v) and IComputeValue.providedBy(v)
    except IndexError:
        return False

def compute_value(fn):
    return provider(IComputeValue)(fn)

## see: korpokkur.interfaces:IInput
@implementer(IInput)
class DictInput(object):
    @classmethod
    def create_from_setting(cls, settings, scaffold, data):
        return cls(scaffold, data)

    def __init__(self, scaffold, D):
        self.scaffold = scaffold
        self.clear()
        self.cache.update(D.copy())

    def load_with_default(self, k, default=None):
        try:
            return self.read(k)
        except KeyError:
            return default

    def load(self, k, reload=False):
        return self.read(k)

    def read(self, k):
        v = self.cache[k]
        if is_compute_value(v):
            v = cached_call(self.cache, k, v)(self, k)
        return v

    def save(self, k, v):
        self.cache[k] = v

    def copy(self):
        return self.__class__(self.scaffold, self.cache.copy())

    def update(self, d):
        self.cache.update(d)

    def __iter__(self):
        return iter(self.cache)

    def __contains__(self, k):
        return k in self.cache

    def clear(self):
        self.loaded_map = {}
        self.cache = {}
        self.cache.update(__builtins__.items())  # xxx:

## see: korpokkur.interfaces:IInput
@implementer(IInput)
class CommandLineInput(object):
    prompt = "{varname} ({description})[{default}]:"

    @classmethod
    def create_from_setting(cls, settings, scaffold):
        return cls(scaffold, sys.stdin, sys.stdout, sys.stderr, prompt=settings["input.prompt"])  # TODO: get prompt via scaffold

    def __init__(self, scaffold, input_port, output_port, error_port, prompt="{word}?:"):
        self.scaffold = scaffold
        self.input_port = input_port
        self.output_port = output_port
        self.error_port = error_port
        self.prompt = prompt
        self.clear()

    def load(self, word, reload=False):
        if reload:
            return self.read(word)
        try:
            v = self.cache[word]
            if is_compute_value(v):
                v = cached_call(self.cache, word, v)(self, word)
            return v
        except KeyError:
            return self.read(word)

    def load_with_default(self, word, default=None):
        try:
            return self.load(word)
        except KeyError:
            return default

    def ask_message(self, word):
        try:
            description, default = self.scaffold.expected_words[word]
            if is_compute_value(default):
                default = default(input, word)
                self.scaffold.expected_words[word] = description, default
            self.error_port.write(self.__class__.prompt.format(varname=word, description=description, default=default))
        except KeyError:
            self.error_port.write(self.prompt.format(word=word))
            default = ""
        self.error_port.flush()
        return default

    def read(self, word):
        default = self.ask_message(word)
        value = self.input_port.readline().rstrip()
        if value == "" and default is not None:
            value = default

        self.cache[word] = value
        self.loaded_map[word] = value
        return value

    def save(self, word, value):
        self.cache[word] = value

    def copy(self):
        o = self.__class__(self.scaffold, self.input_port, self.output_port, self.error_port, prompt=self.prompt)
        o.cache = self.cache.copy()
        return o

    def update(self, d):
        self.cache.update(d)

    def __iter__(self):
        return iter(self.cache)

    def __contains__(self, k):
        return k in self.cache

    def clear(self):
        self.loaded_map = {}
        self.cache = {}
        self.cache.update(__builtins__.items())  # xxx:


## todo: from file?, ini file?
def includeme(config):
    config.add_plugin("input.cli", CommandLineInput, categoryname="input")
    config.add_plugin("input.dict", DictInput, categoryname="input")
