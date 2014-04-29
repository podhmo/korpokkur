# -*- coding:utf-8 -*-
import argparse
from mako_scaffold.config import Configurator
import sys

def err(s):
    sys.stderr.write(s)
    sys.stderr.write("\n")

def out(s):
    sys.stdout.write(s)
    sys.stdout.write("\n")

def get_app(setting={"entry_points_name": "mako.scaffold"}):
    config = Configurator(setting=setting)
    config.include("mako_scaffold.scaffoldgetter")
    return config #xxx:

def listing(args):
    app = get_app()
    cmd = app.activate_plugin("scaffoldgetter")
    for k, cls in cmd.all_scaffolds().items():
        out("{k} -- {path}".format(k=k, path=cls.__doc__ or cls.__name__))

def creation(args):
    # scaffold_cls = get_command().get_scaffold(args.name)
    # if scaffold_cls is None:
    #     return
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    sub_parsers = parser.add_subparsers()

    list_parser = sub_parsers.add_parser("list")
    list_parser.set_defaults(func=listing)

    create_parser = sub_parsers.add_parser("create")
    create_parser.add_argument("name")
    create_parser.set_defaults(func=creation)

    args = parser.parse_args(sys.argv)
    return args.func(args)

