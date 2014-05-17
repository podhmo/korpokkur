# -*- coding:utf-8 -*-
from __future__ import absolute_import #for py2.x
import sys
from zope.interface import implementer
from korpokkur.interfaces import IEmitter
from jinja2.environment import Template as Jinja2Template
from jinja2.utils import concat
from . import InputEnv

class Jinja2InputEnvTemplate(Jinja2Template):
    def render_by_env(self, env):
        env
        try:
            return concat(self.root_render_func(self.new_context(env, shared=True)))
        except Exception:
            exc_info = sys.exc_info()
        return self.environment.handle_exception(exc_info, True)


## see: korpokkur.interfaces:IEmitter
@implementer(IEmitter)
class Jinja2Emitter(object):
    @classmethod
    def create_from_setting(cls, settings):
        env_factory = settings.get("env_factory", InputEnv)
        return cls(env_factory)

    def __init__(self, env_factory):
        self.env_factory = env_factory

    def emit(self, input, text="", filename=""):
        assert text or filename
        env = self.env_factory(input)
        return Jinja2InputEnvTemplate(text).render_by_env(env)


def includeme(config):
    config.add_plugin("emitter.jinja2", Jinja2Emitter, categoryname="emitter")
