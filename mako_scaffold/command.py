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

def get_app(setting=
            {"entry_points_name": "mako.scaffold", 
             "input.prompt": "{word}? :"
                 }):
    config = Configurator(setting=setting)
    config.include("mako_scaffold.scaffoldgetter")
    config.include("mako_scaffold.walker")
    config.include("mako_scaffold.detector")
    config.include("mako_scaffold.input")
    config.include("mako_scaffold.emitter")
    config.include("mako_scaffold.reproduction")
    return config #xxx:


def listing(args):
    app = get_app()
    cmd = app.activate_plugin("scaffoldgetter")
    for k, cls in cmd.all_scaffolds().items():
        out("{k} -- {path}".format(k=k, path=cls.__doc__ or cls.__name__))


def creation(args):
    app = get_app()
    getter = app.activate_plugin("scaffoldgetter")
    scaffold_cls = getter.get_scaffold(args.name)
    scaffold = scaffold_cls()
    input = app.activate_plugin("input.cli")
    emitter = app.activate_plugin("emitter.mako")
    reproduction = app.activate_plugin("reproduction.physical", emitter, input)
    detector = app.activate_plugin("detector")
    walker = app.activate_plugin("walker", input, detector, reproduction)
    walker.walk(scaffold.source_directory, ".")

def scanning(args):
    app = get_app()
    getter = app.activate_plugin("scaffoldgetter")
    scaffold_cls = getter.get_scaffold(args.name)
    scaffold = scaffold_cls()
    input = app.activate_plugin("input.cli")
    emitter = app.activate_plugin("emitter.mako")
    reproduction = app.activate_plugin("reproduction.simulation", emitter, input)
    detector = app.activate_plugin("detector")
    walker = app.activate_plugin("walker", input, detector, reproduction)
    walker.walk(scaffold.source_directory, ".")

    ##xxxx
    print("----------------------------------------")
    import json
    print(json.dumps(input.loaded_map, indent=2, ensure_ascii=False))

def setup_logging(args):
    if args.logging is None:
        return
    else:
        import logging
        level = getattr(logging, args.logging)
        logging.basicConfig(level=level)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    parser.add_argument("--logging", choices=["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"])
    sub_parsers = parser.add_subparsers()

    list_parser = sub_parsers.add_parser("list")
    list_parser.set_defaults(func=listing)

    create_parser = sub_parsers.add_parser("create")
    create_parser.add_argument("name")
    create_parser.set_defaults(func=creation)

    scan_parser = sub_parsers.add_parser("scan")
    scan_parser.add_argument("name")
    scan_parser.set_defaults(func=scanning)

    args = parser.parse_args(sys.argv)
    setup_logging(args)
    try:
        func = args.func
    except AttributeError:
        parser.error("unknown action")
    return func(args)

