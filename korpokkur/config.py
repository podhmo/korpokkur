# -*- coding:utf-8 -*-
import re
from zope.interface.registry import Components
from zope.interface import implementer, implementedBy
from zope.interface.verify import verifyClass
from .interfaces import IConfigurator, IPlugin
from .langhelper import import_symbol
import pkg_resources
import logging
logger = logging.getLogger(__name__)

_registry = None
def get_registry():
    global _registry
    if _registry is None:
        _registry = Components("korpokkur")
    return _registry


@implementer(IConfigurator)
class Configurator(object):
    def __init__(self, setting, registry=None):
        self.setting = setting
        self.registry = registry or get_registry()
        self.registry.setting = setting
        if not hasattr(self.registry, "installed_plugin"):
            self.registry.installed_plugin = {}
        if not hasattr(self.registry, "activated_plugin"):
            self.registry.activated_plugin = {}

    @property
    def installed_plugin_repository(self):
        return self.registry.installed_plugin

    @property
    def activated_plugin_repository(self):
        return self.registry.activated_plugin

    relative_rx = re.compile("^\.+")
    module_cache = {}
    def maybe_dotted(self, xxx):
        if hasattr(xxx, "encode"):
            m = self.relative_rx.search(xxx)
            ## relative import support. this is uggly.
            if m:
                logger.warn("maybe_dotted: relative import is experimental support.: %s", xxx)
                star_size = len(m.group(0))
                if star_size > 1:
                    import inspect
                    import sys
                    caller_module = inspect.getmodule(inspect.currentframe().f_back)

                    if hasattr(caller_module, "__path__"):
                        filename_list = caller_module.__path__
                    else:
                        filename_list = [pkg_resources.resource_filename(caller_module.__name__, "")]

                    for filename in filename_list:
                        if filename in self.module_cache:
                            xxx = "{}.{}".format(self.module_cache[filename], xxx.lstrip("."))
                            break

                        word_list = filename.split("/")
                        for _ in range(star_size-1):
                            word_list.pop()

                        root_module_path = "/".join(word_list)
                        matched_module_name = None
                        for name, m in sys.modules.items():
                            if hasattr(m, "__path__") and any(p == root_module_path for p in m.__path__):
                                matched_module_name = name
                                break
                        if matched_module_name:
                            self.module_cache[filename] = matched_module_name
                            xxx = "{}.{}".format(matched_module_name, xxx.lstrip("."))
                            break
            return import_symbol(xxx)
        return xxx

    def include(self, module_or_object):
        if ":" in module_or_object:
            self.maybe_dotted(module_or_object)(self)
        else:
            module = self.maybe_dotted(module_or_object)
            if hasattr(module, "includeme"):
                module.includeme(self)

    def lookup_implementation(self, iface, name):
        return self.registry.adapters.lookup([IConfigurator], iface, name)

    def register_implementation(self, iface, name, plugin_factory):
        self.registry.adapters.register([IConfigurator], iface, name, plugin_factory)

    def add_plugin(self, installname, plugin, iface=None, categoryname=None, strict=True):
        if iface is None:
            try:
                iface = next(iter(implementedBy(plugin)))
                if iface is IPlugin:
                    iface = next(iter(implementedBy(plugin))) #xxx
            except StopIteration:
                raise Exception("plugin {} is not implemented by any interface".format(plugin))

        if strict:
            implementer(iface)(plugin)
            verifyClass(iface, plugin)

        if categoryname is None:
            categoryname = installname

        plugin_factory = self.maybe_dotted(plugin)
        self.register_implementation(iface, installname, plugin_factory)

        logger.info("install: %s -- %s (category:%s)", installname, plugin_factory.__name__, categoryname)
        self.registry.installed_plugin[installname] = (iface, categoryname)


    def activate_plugin(self, installname, *args, **kwargs):
        iface, categoryname = self.registry.installed_plugin[installname]
        plugin_class = self.lookup_implementation(iface, installname)
        if plugin_class is None:
            raise Exception("plugin {nam} not found(iface={iface})".format(nam=installname, iface=iface))
        plugin = plugin_class.create_from_setting(self.setting, *args, **kwargs)

        logger.info("activate: %s -- %s", categoryname, plugin)
        self.registry.activated_plugin[categoryname] = plugin
        return plugin

    def __getattr__(self, categoryname):
        try:
            plugin = self.registry.activated_plugin[categoryname]
        except KeyError:
            raise AttributeError("forget to call self.activate_plugin('{name}.*')?".format(name=categoryname))
        setattr(self, categoryname, plugin) #cache
        return plugin

