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
    def create_from_setting(cls, setting, input,  detector):
        return cls(input, detector)

    def __init__(self, input, detector):
        self.input = input
        self.detector = detector

    ## todo:move
    def convert_path(self, root, r, name, dst):
        reldir = r.replace(root, dst)
        return os.path.join(reldir, name)

    def rewrite_name(self, name):
        pattern, varname = self.detector.rewrite_target_from_filename(name)
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
        if not self.detector.is_rewrite_file(f):
            shutil.copy(os.path.join(r, f),
                        self.convert_path(root, r, name, dst) 
                    )
        else:
            print("rewrite!")
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
