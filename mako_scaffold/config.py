# -*- coding:utf-8 -*-
from zope.interface.registry import Components
from zope.interface import implementer, implementedBy
from .interfaces import IConfigurator
import pkg_resources
import logging
logger = logging.getLogger(__name__)

_registry = None
def get_registry():
    global _registry
    if _registry is None:
        _registry = Components("mako_scaffold")
    return _registry

def import_symbol(symbol): #todo cache
    return pkg_resources.EntryPoint.parse("x=%s" % symbol).load(False)

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

    def maybe_dotted(self, xxx):
        if hasattr(xxx, "encode"):
            return import_symbol(xxx)
        return xxx

    def include(self, module_or_object):
        if ":" in module_or_object:
            self.maybe_dotted(module_or_object)(self)
        else:
            module = self.maybe_dotted(module_or_object)
            if hasattr(module, "includeme"):
                module.includeme(self)

    def add_plugin(self, installname, plugin, iface=None, name=""):
        if iface is None:
            try:
                iface = iter(implementedBy(plugin)).__next__()
            except StopIteration:
                raise Exception("plugin {} is not implemented by any interface".format(plugin))
        plugin_factory = self.maybe_dotted(plugin)
        self.registry.adapters.register([IConfigurator], iface, name, plugin_factory)

        logger.info("install: %s -- %s", installname, plugin_factory)
        self.registry.installed_plugin[installname] = iface

    def activate_plugin(self, installname, *args, **kwargs):
        name = kwargs.get("name", "")
        iface = self.registry.installed_plugin[installname]
        plugin_class = self.registry.adapters.lookup([IConfigurator], iface, name)
        if plugin_class is None:
            raise Exception("plugin {nam} not found(iface={iface})".format(nam=installname, iface=iface))
        plugin = plugin_class.create_from_setting(self.setting, *args, **kwargs)

        logger.info("activate: %s -- %s", installname, plugin)
        self.registry.activated_plugin[installname] = plugin
        return plugin

    def __getattr__(self, installname):
        try:
            plugin = self.registry.activated_plugin[installname]
        except KeyError:
            raise AttributeError(installname)
        setattr(self, installname, plugin) #cache
        return plugin

