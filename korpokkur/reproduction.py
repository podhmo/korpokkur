# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import os.path
import shutil
from zope.interface import implementer
from .interfaces import IReproduction
from . import FileConflict

## see: korpokkur.interfaces:IReproduction
@implementer(IReproduction)
class PhysicalReproduction(object):
    @classmethod
    def create_from_setting(cls, setting, emitter, input):
        return cls(emitter, input)

    def __init__(self, emitter, input):
        self.emitter = emitter
        self.input = input

    def is_copy_file_ng(self, dst_path, overwrite):
        return not overwrite and os.path.exists(dst_path)

    def prepare_for_copy_file(self, dst_path, overwrite):
        dir_path = os.path.dirname(dst_path)
        if self.is_copy_file_ng(dst_path, overwrite):
            raise FileConflict(dst_path)
        return self.prepare_for_copy_directory(dir_path)

    def prepare_for_copy_directory(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def copy_file(self, src_path, dst_path):
        shutil.copy(src_path, dst_path)

    def modified_copy_file(self, src_path, dst_path):
        self.input.update({":src:":src_path, ":dst:":dst_path})
        with open(dst_path, "w") as wf:
            with open(src_path) as rf:
                template = rf.read()
                wf.write(self.emitter.emit(template, self.input))


import sys

def err(s):
    sys.stderr.write(s)
    sys.stderr.write("\n")

## see: korpokkur.interfaces:IReproduction
@implementer(IReproduction)
class SimulateReproduction(object):
    @classmethod
    def create_from_setting(cls, setting, emitter, input):
        return cls(emitter, input)

    def __init__(self, emitter, input):
        self.emitter = emitter
        self.input = input
        self.output = set()

    def is_copy_file_ng(self, dst_path, overwrite):
        return not overwrite and os.path.exists(dst_path)

    def prepare_for_copy_file(self, dst_path, overwrite):
        dir_path = os.path.dirname(dst_path)
        if self.is_copy_file_ng(dst_path, overwrite):
            raise FileConflict(dst_path)
        return self.prepare_for_copy_directory(dir_path)

    def prepare_for_copy_directory(self, dir_path):
        message = "d[c]: {}".format(dir_path)
        if not message in self.output:
            self.output.add(message)
            err(message)

    def copy_file(self, src_path, dst_path):
        err("f[c]: {} -> {}".format(src_path, dst_path))

    def modified_copy_file(self, src_path, dst_path):
        err("f[m]: {} -> {}".format(src_path, dst_path))
        self.input.update({":src:":src_path, ":dst:":dst_path})
        with open(src_path) as rf:
            template = rf.read()
            (self.emitter.emit(template, self.input))


def includeme(config):
    config.add_plugin("reproduction.physical", PhysicalReproduction, categoryname="reproduction")
    config.add_plugin("reproduction.simulation", SimulateReproduction, categoryname="reproduction")
