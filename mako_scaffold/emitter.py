# -*- coding:utf-8 -*-
from zope.interface import implementer
from mako_scaffold.interfaces import IEmitter
from mako.template import Template as MakoTemplate
from mako import runtime as mako_runtime
from mako.util import FastEncodingBuffer
from mako import compat
from collections import Mapping

class InputEnv(Mapping):
    def __init__(self, input, undefined=mako_runtime.UNDEFINED):
        self.input = input
        self.undefined = undefined

    def __getitem__(self, k):
        return self.input.load(k)

    def __setitem__(self, k, v):
        return self.input.save(k, v)

    def __delitem__(self, k):
        raise Exception("not support")

    def get(self, k, default=None):
        return self.input.load_with_default(k, default=default)

    def copy(self):
        return self.input.copy()

    def __iter__(self):
        return iter(self.input)

    def __len__(self):
        raise Exception("not support")

class InputEnvTemplate(MakoTemplate):
    def render_by_env(self, env):
        return _render(self, self.callable_, (), env)

class InputEnvContext(mako_runtime.Context):
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
    context = InputEnvContext(buf, data)
    context._outputting_as_unicode = as_unicode
    context._set_with_template(template)

    mako_runtime._render_context(template, callable_, context, *args,
                    **mako_runtime._kwargs_for_callable(callable_, data))
    return context._pop_buffer().getvalue()


## see: mako_scaffold.interfaces:IEmitter
@implementer(IEmitter)
class MakoEmitter(object):
    @classmethod
    def create_from_setting(cls, settings, input):
        env_factory = settings.get("env_factory", InputEnv)
        return cls(env_factory)

    def __init__(self, env_factory):
        self.env_factory = env_factory

    def emit(self, template, input):
        env = self.env_factory(input)
        return InputEnvTemplate(template).render_by_env(env)

