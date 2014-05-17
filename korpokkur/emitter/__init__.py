# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from collections import Mapping

class InputEnv(Mapping):
    def __init__(self, input):
        self.input = input

    def __getitem__(self, k):
        return self.input.load(k)

    def __setitem__(self, k, v):
        return self.input.save(k, v)

    def __delitem__(self, k):
        raise Exception("not support")

    def get(self, k, default=None):
        return self.input.load_with_default(k, default=default)

    def pop(self, k, default=None):
        try:
            return self.input.cache.pop(k)
        except KeyError:
            return default

    def update(self, D):
        return self.input.update(D)

    def copy(self):
        return self.__class__(self.input.copy())

    def __iter__(self):
        return iter(self.input)

    def __len__(self):
        return len(self.input.cache) #xxx:
