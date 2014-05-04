# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import os.path
import shutil
from zope.interface import implementer
from .interfaces import IReproduction


## see: mako_scaffold.interfaces:IReproduction
@implementer(IReproduction)
class PhysicalReproduction(object):
    def prepare_for_copy_file(self, dst_path):
        dir_path = os.path.dirname(dst_path)
        return self.prepare_for_copy_directory(dir_path)

    def prepare_for_copy_directory(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def copy_file(self, src_path, dst_path):
        self.prepare_for_copy(dst_path)
        shutil.copy(src_path, dst_path)

    def modified_copy_file(self, src_path, dst_path):
        self.prepare_for_copy(dst_path)
        with open(dst_path, "w") as wf:
            with open(src_path) as rf:
                template = rf.read()
                wf.write(self.emitter.emit(template, self.input))
