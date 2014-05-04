# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer
from mako_scaffold.interfaces import ITreeWalker, IPlugin
import os
import os.path
import shutil

## see: mako_scaffold.interfaces:ITreeWalker
@implementer(ITreeWalker, IPlugin)
class StructualWalker(object):
    @classmethod
    def create_from_setting(cls, setting, input,  detector, emitter):
        return cls(input, detector, emitter)

    def __init__(self, input, detector, emitter):
        self.input = input
        self.detector = detector
        self.emitter = emitter

    ## todo:move
    def convert_path(self, root, r, name, dst):
        reldir = r.replace(root, dst)
        return os.path.join(reldir, name)

    def rewrite_name(self, name):
        pattern, varname = self.detector.get_rewrite_patterns(name)
        replaced = name.replace(pattern, self.input.load(varname))
        logger.debug("rewrite: %s -> %s", name, replaced)
        return replaced

    def on_dirname(self, root, r, d, dst):
        if self.detector.is_rewrite_name(d):
            name = self.rewrite_name(d)
        else:
            name = d
        dirpath = self.convert_path(root, r, name, dst)
        if not os.path.lexists(dirpath):
            os.makedirs(dirpath)
        return name

    def on_filename(self, root, r, f, dst):
        if self.detector.is_rewrite_name(f):
            name = self.rewrite_name(f)
        else:
            name = f

        src_path = os.path.join(r, f)
        dst_path = self.convert_path(root, r, name, dst)

        dir_path = os.path.dirname(dst_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if not self.detector.is_rewrite_file(f):
            shutil.copy(src_path, dst_path)
        else:
            dst_path = self.detector.replace_rewrite_file(dst_path)
            with open(dst_path, "w") as wf:
                with open(src_path) as rf:
                    template = rf.read()
                    wf.write(self.emitter.emit(template, self.input))
        return name

    def walk(self, root, dst):
        dst = os.path.abspath(dst)
        prefix = self.on_dirname(
            root, 
            os.path.dirname(root), 
            os.path.basename(root), 
            dst
        )
        dst = os.path.join(dst, prefix)
        for r, ds, fs in os.walk(root):
            rel = r.replace(root, prefix)
            for d in ds:
                logger.debug("watch: d %s/%s", rel, d)
                self.on_dirname(root, r, d, dst)
            for f in fs:
                logger.debug("watch: f %s/%s", rel, f)
                self.on_filename(root, r, f, dst)


def includeme(config):
    config.add_plugin("walker", StructualWalker)
