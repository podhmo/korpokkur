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
    setup_logging(app, args)
    cmd = app.activate_plugin("scaffold:getter")
    for k, cls in cmd.all_scaffolds().items():
        out("{k} -- {path}".format(k=k, path=cls.__doc__ or cls.__name__))


def creation(args):
    app = get_app()
    setup_logging(app, args)
    getter = app.activate_plugin("scaffold:getter")
    scaffold_cls = getter.get_scaffold(args.name)
    scaffold = app.activate_plugin("scaffold:factory", scaffold_cls)
    input = setup_input(app, args, scaffold)
    emitter = app.activate_plugin("emitter.mako")
    reproduction = app.activate_plugin("reproduction.physical", emitter, input)
    detector = app.activate_plugin("detector")
    walker = app.activate_plugin("walker", input, detector, reproduction)
    scaffold.walk(walker, args.destination)



def scanning(args):
    app = get_app()
    setup_logging(app, args)
    getter = app.activate_plugin("scaffold:getter")
    scaffold_cls = getter.get_scaffold(args.name)
    scaffold = app.activate_plugin("scaffold:factory", scaffold_cls)
    input = setup_input(app, args, scaffold)
    emitter = app.activate_plugin("emitter.mako")
    reproduction = app.activate_plugin("reproduction.simulation", emitter, input)
    detector = app.activate_plugin("detector")
    walker = app.activate_plugin("walker", input, detector, reproduction)
    scaffold.walk(walker, args.destination)

    ##xxxx
    import json
    out("----------------------------------------")
    out(json.dumps(input.loaded_map, indent=2, ensure_ascii=False))


def setup_input(app, args, scaffold):
    if args.config is None:
        return app.activate_plugin("input.cli", scaffold)
    elif args.config.endswith(".json"):
        #xxx
        import json
        with open(args.config) as rf:
            data = json.load(rf)
            return app.activate_plugin("input.dict", scaffold, data)
    elif args.config.endswith(".ini"):
        try:
            from configparser import ConfigParser
        except ImportError:
            from ConfigParser import SafeConfigParser as ConfigParser
        parser = ConfigParser()
        assert parser.read(args.config)
        data = dict(parser.items("scaffold"))
        return app.activate_plugin("input.dict", scaffold, data)

def setup_logging(app, args):
    if args.logging is None:
        return
    else:
        import logging
        level = getattr(logging, args.logging)
        logging.basicConfig(level=level)

def main(sys_args=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    sub_parsers = parser.add_subparsers()

    list_parser = sub_parsers.add_parser("list")
    list_parser.add_argument("--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    list_parser.set_defaults(func=listing)

    create_parser = sub_parsers.add_parser("create")
    create_parser.add_argument("--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    create_parser.add_argument("-c", "--config")
    create_parser.add_argument("name")
    create_parser.add_argument("destination", default=".", nargs="?")
    create_parser.set_defaults(func=creation)

    scan_parser = sub_parsers.add_parser("scan")
    scan_parser.add_argument("--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    scan_parser.add_argument("-c", "--config")
    scan_parser.add_argument("name")
    scan_parser.add_argument("destination", default=".", nargs="?")
    scan_parser.set_defaults(func=scanning)

    args = parser.parse_args(sys_args)
    try:
        func = args.func
    except AttributeError:
        parser.error("unknown action")
    return func(args)

