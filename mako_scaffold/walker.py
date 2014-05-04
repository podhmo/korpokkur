# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer
from mako_scaffold.interfaces import ITreeWalker, IPlugin
import os
import os.path


## see: mako_scaffold.interfaces:ITreeWalker
@implementer(ITreeWalker, IPlugin)
class StructualWalker(object):
    @classmethod
    def create_from_setting(cls, setting, input,  detector, reproduction):
        return cls(input, detector, reproduction)

    def __init__(self, input, detector, reproduction):
        self.input = input
        self.detector = detector
        self.reproduction = reproduction

    ## todo:move
    def convert_to_modified_path(self, root, r, name, dst, dirmap):
        reldir = r.replace(root, dst)
        path = os.path.join(reldir, name)
        if r in dirmap:
            path = path.replace(r, dirmap[r])
        return path

    def get_modified_name(self, name):
        if not self.detector.is_rewrite_name(name):
            return name
        else:
            pattern, varname = self.detector.get_rewrite_patterns(name)
            replaced = name.replace(pattern, self.input.load(varname))
            logger.debug("rewrite: %s -> %s", name, replaced)
            return replaced

    def on_dirname(self, root, r, d, dst, dirmap):
        name = self.get_modified_name(d)
        dirpath = self.convert_to_modified_path(root, r, name, dst, dirmap)
        self.reproduction.prepare_for_copy_directory(dirpath)
        return dirpath

    def on_filename(self, root, r, f, dst, dirmap):
        name = self.get_modified_name(f)

        src_path = os.path.join(r, f)
        dst_path = self.convert_to_modified_path(root, r, name, dst, dirmap)

        self.reproduction.prepare_for_copy_file(dst_path)

        if not self.detector.is_rewrite_file(f):
            self.reproduction.copy_file(src_path, dst_path)
        else:
            dst_path = self.detector.replace_rewrite_file(dst_path)
            self.reproduction.modified_copy_file(src_path, dst_path)
        return dst_path

    def walk(self, root, dst):
        dst = os.path.abspath(dst)
        replaced_dirmap = {}
        prefix = self.on_dirname(
            os.path.dirname(root), 
            os.path.dirname(root), 
            os.path.basename(root), 
            dst, 
            replaced_dirmap
        )

        dst = os.path.join(dst, prefix)
        for r, ds, fs in os.walk(root):
            rel = r.replace(root, prefix)
            for d in ds:
                logger.debug("watch: d %s/%s", rel, d)
                replaced_dirname = self.on_dirname(root, r, d, dst, replaced_dirmap)
                replaced_dirmap[os.path.join(r, d)] = replaced_dirname
            for f in fs:
                logger.debug("watch: f %s/%s", rel, f)
                self.on_filename(root, r, f, dst, replaced_dirmap)


def includeme(config):
    config.add_plugin("walker", StructualWalker)
