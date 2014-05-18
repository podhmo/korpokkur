# -*- coding:utf-8 -*-
import argparse
from .config import Configurator
from functools import partial
from . import FileConflict
import sys

def err(s):
    sys.stderr.write(s)
    sys.stderr.write("\n")

def out(s):
    sys.stdout.write(s)
    sys.stdout.write("\n")

default_setting = {
    "walker.skiptop": False, 
    "entry_points_name": "korpokkur.scaffold", 
    "input.prompt": "{word}? :"
}

def get_app(**kwargs):
    setting = {}
    setting.update(default_setting)
    setting.update(kwargs)
    config = Configurator(setting=setting)
    config.include("korpokkur.scaffoldgetter")
    config.include("korpokkur.walker")
    config.include("korpokkur.detector")
    config.include("korpokkur.input")
    config.include("korpokkur.reproduction")
    return config #xxx:


def listing(args, kwargs={}):
    app = get_app(**kwargs)
    setup_logging(app, args)
    cmd = app.activate_plugin("scaffoldgetter")
    out("create:")
    for k, cls in sorted(cmd.all_scaffolds().items()):
        out("  {k} -- {path}".format(k=k, path=cls.__doc__ or cls.__name__))

    out("add:")
    for k, cls in sorted(cmd.all_scaffolds(entry_points_name="korpokkur.partial.scaffold").items()):
        out("  {k} -- {path}".format(k=k, path=cls.__doc__ or cls.__name__))


def output_loadmap(input):
    ##xxxx
    import json
    err("----------------------------------------")
    err("*input values*")
    out(json.dumps(input.loaded_map, indent=2, ensure_ascii=False))

def creation(args, kwargs={}):
    app = get_app(**kwargs)
    setup_logging(app, args)
    getter = app.activate_plugin("scaffoldgetter")
    scaffold = getter.get_scaffold(args.name)
    input = setup_input(app, args, scaffold)
    emitter = setup_emitter(app, args, scaffold)
    reproduction = app.activate_plugin("reproduction.physical", emitter, input)
    detector = app.activate_plugin("detector")
    walker = app.activate_plugin("walker", input, detector, reproduction)
    try:
        skiptop = app.setting["walker.skiptop"]
        scaffold.walk(walker, args.destination, overwrite=not args.nooverwrite, skiptop=skiptop)
    except FileConflict as e:
        err("conflict file: {e.path} is already existed".format(e=e))
        output_loadmap(input)
        sys.exit(-1)

def scanning(args, kwargs={}):
    app = get_app(**kwargs)
    setup_logging(app, args)
    getter = app.activate_plugin("scaffoldgetter")
    scaffold = getter.get_scaffold(args.name)
    input = setup_input(app, args, scaffold)
    emitter = setup_emitter(app, args, scaffold)
    reproduction = app.activate_plugin("reproduction.simulation", emitter, input)
    detector = app.activate_plugin("detector")
    walker = app.activate_plugin("walker", input, detector, reproduction)
    try:
        scaffold.walk(walker, args.destination, overwrite=not args.nooverwrite)
    except FileConflict as e:
        err("conflict file: {e.path} is already existed".format(e=e))
        output_loadmap(input)
        sys.exit(-1)
    output_loadmap(input)
    sys.exit(0)


##xxxx:
def setup_emitter(app, args, scaffold):
    engine_name = getattr(scaffold.template, "template_engine", "mako")
    assert engine_name in ("mako", "jinja2")
    app.include("korpokkur.emitter.{}".format(engine_name))
    return app.activate_plugin("emitter.{}".format(engine_name))

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
    create_parser.add_argument("--nooverwrite", action="store_true", default=False)
    create_parser.add_argument("name")
    create_parser.add_argument("destination", default=".", nargs="?")
    create_parser.set_defaults(func=creation)

    add_parser = sub_parsers.add_parser("add")
    add_parser.add_argument("--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    add_parser.add_argument("-c", "--config")
    add_parser.add_argument("--nooverwrite", action="store_true", default=False)
    add_parser.add_argument("name")
    add_parser.add_argument("destination", default=".", nargs="?")
    add_parser_setting = {
        "entry_points_name": "korpokkur.partial.scaffold", 
        "walker.skiptop": True
    }
    add_parser.set_defaults(func=partial(creation, kwargs=add_parser_setting))

    create_scan_parser = sub_parsers.add_parser("scan")
    create_scan_parser.add_argument("--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    create_scan_parser.add_argument("-c", "--config")
    create_scan_parser.add_argument("--nooverwrite", action="store_true", default=False)
    create_scan_parser.add_argument("name")
    create_scan_parser.add_argument("destination", default=".", nargs="?")
    create_scan_parser.set_defaults(func=scanning)

    add_scan_parser = sub_parsers.add_parser("addscan")
    add_scan_parser.add_argument("--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    add_scan_parser.add_argument("-c", "--config")
    add_scan_parser.add_argument("--nooverwrite", action="store_true", default=False)
    add_scan_parser.add_argument("name")
    add_scan_parser.add_argument("destination", default=".", nargs="?")
    add_parser_setting = {
        "entry_points_name": "korpokkur.partial.scaffold", 
        "walker.skiptop": True
    }
    add_scan_parser.set_defaults(func=partial(scanning, kwargs=add_parser_setting))

    args = parser.parse_args(sys_args)
    try:
        func = args.func
    except AttributeError:
        parser.error("unknown action")
    return func(args)

