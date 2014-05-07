# -*- coding:utf-8 -*-
from __future__ import absolute_import #for py2.x
from zope.interface import implementer
from korpokkur.interfaces import IEmitter
from mako.template import Template as MakoTemplate
from mako import runtime as mako_runtime
from mako.util import FastEncodingBuffer
from mako import compat
from . import InputEnv

class MakoInputEnvTemplate(MakoTemplate):
    def render_by_env(self, env):
        return _render(self, self.callable_, (), env)

class MakoInputEnvContext(mako_runtime.Context):
    def __init__(self, buffer, data):
        self._buffer_stack = [buffer]

        self._data = data

        self._kwargs = data.copy()
        self._with_template = None
        self._outputting_as_unicode = None
        self.namespaces = {}

        # "capture" function which proxies to the
        # generic "capture" function
        self._data['capture'] = compat.partial(mako_runtime.capture, self)

        # "caller" stack used by def calls with content
        self.caller_stack = self._data['caller'] = mako_runtime.CallerStack()


def _render(template, callable_, args, data, as_unicode=False):
    """create a Context and return the string
    output of the given template and template callable."""

    if as_unicode:
        buf = FastEncodingBuffer(as_unicode=True)
    elif template.bytestring_passthrough:
        buf = compat.StringIO()
    else:
        buf = FastEncodingBuffer(
                        as_unicode=as_unicode,
                        encoding=template.output_encoding,
                        errors=template.encoding_errors)
    context = MakoInputEnvContext(buf, data)
    context._outputting_as_unicode = as_unicode
    context._set_with_template(template)

    mako_runtime._render_context(template, callable_, context, *args,
                    **mako_runtime._kwargs_for_callable(callable_, data))
    return context._pop_buffer().getvalue()


## see: korpokkur.interfaces:IEmitter
@implementer(IEmitter)
class MakoEmitter(object):
    @classmethod
    def create_from_setting(cls, settings):
        env_factory = settings.get("env_factory", InputEnv)
        return cls(env_factory)

    def __init__(self, env_factory):
        self.env_factory = env_factory

    def emit(self, template, input):
        env = self.env_factory(input)
        return MakoInputEnvTemplate(template).render_by_env(env)

def includeme(config):
    config.add_plugin("emitter.mako", MakoEmitter, categoryname="emitter")
