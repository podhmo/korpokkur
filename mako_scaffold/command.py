# -*- coding:utf-8 -*-
import pkg_resources
import argparse
from collections import OrderedDict
import sys

def err(s):
    sys.stderr.write(s)
    sys.stderr.write("\n")

def out(s):
    sys.stdout.write(s)
    sys.stdout.write("\n")

class MakoScaffoldCommand(object):
    def __init__(self, entry_points_name="mako.scaffold", out=err):
        self.entry_points_name = entry_points_name
        self.out = out

    def all_scaffolds(self):
        scaffolds = OrderedDict()
        eps = list(pkg_resources.iter_entry_points(self.entry_points_name))
        for entry in eps:
            try:
                scaffold_class = entry.load()
                scaffolds[entry.name] = scaffold_class
            except Exception as e: # pragma: no cover
                self.out('Warning: could not load entry point %s (%s: %s)' % (
                    entry.name, e.__class__.__name__, e))
        return scaffolds


def get_command():
    return MakoScaffoldCommand("mako.scaffold")

def listing(args):
    cmd = get_command()
    for k, cls in cmd.all_scaffolds().items():
        out("{k} -- {path}".format(k=k, path=cls.__doc__ or cls.__name__))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    sub_parsers = parser.add_subparsers()
    list_parser = sub_parsers.add_parser("list")
    list_parser.set_defaults(func=listing)
    args = parser.parse_args(sys.argv)
    return args.func(args)

