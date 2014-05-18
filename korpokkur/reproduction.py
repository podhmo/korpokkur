# -*- coding:utf-8 -*-
import re
import logging
import contextlib
logger = logging.getLogger(__name__)
import os.path
import shutil
from zope.interface import (
    implementer, 
    provider
)
from .interfaces import (
    IReproduction, 
    IAfterEmitFilter
)
from . import FileConflict

@provider(IAfterEmitFilter)
def marker_comments_filter(input, output_text):
    for name, marker in input.scaffold.marker_comments.items():
        def repl(m):
            padding = m.group(1)
            return "\n".join([m.group(0), m.group(1)+input.load(name)])
        pattern = re.compile(r'^(\s*){}.*$'.format(re.escape(marker)), re.MULTILINE)
        output_text = re.sub(pattern, repl, output_text)
    return output_text


## see: korpokkur.interfaces:IReproduction
@implementer(IReproduction)
class PhysicalReproduction(object):
    @classmethod
    def create_from_setting(cls, setting, emitter, input):
        after_emit_filter = setting[IAfterEmitFilter]
        return cls(emitter, input, after_emit_filter)

    def __init__(self, emitter, input, after_emit_filter):
        self.emitter = emitter
        self.input = input
        self.after_emit_filter = after_emit_filter

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
        output_text = (self.emitter.emit(self.input, filename=src_path))
        output_text = self.after_emit_filter(self.input, output_text)

        with open(dst_path, "w") as wf:
            wf.write(output_text)
        return output_text

import sys

def err(s):
    sys.stderr.write(s)
    sys.stderr.write("\n")

## see: korpokkur.interfaces:IReproduction
@implementer(IReproduction)
class SimulateReproduction(object):
    @classmethod
    def create_from_setting(cls, setting, emitter, input):
        after_emit_filter = setting[IAfterEmitFilter]
        return cls(emitter, input, after_emit_filter)

    def __init__(self, emitter, input, after_emit_filter):
        self.emitter = emitter
        self.input = input
        self.output = set()
        self.after_emit_filter = after_emit_filter

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
        output_text = (self.emitter.emit(self.input, filename=src_path))
        return self.after_emit_filter(self.input, output_text)


def includeme(config):
    config.add_plugin("reproduction.physical", PhysicalReproduction, categoryname="reproduction")
    config.add_plugin("reproduction.simulation", SimulateReproduction, categoryname="reproduction")
    config.setting[IAfterEmitFilter] = marker_comments_filter ##xxx?
