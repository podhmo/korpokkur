# -*- coding:utf-8 -*-
from __future__ import absolute_import #for py2.x
from zope.interface import implementer
from korpokkur.interfaces import IEmitter
import posixpath
import re
import os.path
from mako.template import Template as MakoTemplate
from mako.lookup import TemplateLookup
from mako import exceptions as mako_exceptions
from mako import runtime as mako_runtime
from mako.util import FastEncodingBuffer
from mako import compat

from . import InputEnv

class MakoInputEnvLookup(TemplateLookup):
    FISRT_IS_SLASH_RX = re.compile(r'^\/+')
    def get_template(self, uri):
        try:
            if self.filesystem_checks:
                return self._check(uri, self._collection[uri])
            else:
                return self._collection[uri]
        except KeyError:
            ## WHAT IS THIS!!!!!!!!
            is_abs_uri = os.path.isabs(uri)
            u = self.FISRT_IS_SLASH_RX.sub('', uri)
            for dir in self.directories:
                if is_abs_uri:
                    srcfile = uri
                else:
                    srcfile = posixpath.normpath(posixpath.join(dir, u))
                if os.path.isfile(srcfile):
                    return self._load(srcfile, uri)
            else:
                raise mako_exceptions.TopLevelLookupException(
                                    "Cant locate template for uri %r" % uri)

    def _load(self, filename, uri):
        self._mutex.acquire()
        try:
            try:
                # try returning from collection one
                # more time in case concurrent thread already loaded
                return self._collection[uri]
            except KeyError:
                pass
            try:
                if self.modulename_callable is not None:
                    module_filename = self.modulename_callable(filename, uri)
                else:
                    module_filename = None
                self._collection[uri] = template = MakoInputEnvTemplate(
                                        uri=uri,
                                        filename=posixpath.normpath(filename),
                                        lookup=self,
                                        module_filename=module_filename,
                                        **self.template_args)
                return template
            except:
                # if compilation fails etc, ensure
                # template is removed from collection,
                # re-raise
                self._collection.pop(uri, None)
                raise
        finally:
            self._mutex.release()

    def put_string(self, uri, text):
        self._collection[uri] = MakoInputEnvTemplate(
                                    text,
                                    lookup=self,
                                    uri=uri,
                                    **self.template_args)


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
    _render_context(template, callable_, context, args,
                                 mako_runtime._kwargs_for_callable(callable_, data))
    return context._pop_buffer().getvalue()

def _render_context(tmpl, callable_, context, args, kwargs):
    import mako.template as template
    # create polymorphic 'self' namespace for this
    # template with possibly updated context
    if not isinstance(tmpl, template.DefTemplate):
        # if main render method, call from the base of the inheritance stack
        (inherit, lclcontext) = mako_runtime._populate_self_namespace(context, tmpl)
        mako_runtime._exec_template(inherit, lclcontext, args=args, kwargs=kwargs)
    else:
        # otherwise, call the actual rendering method specified
        (inherit, lclcontext) = mako_runtime._populate_self_namespace(context, tmpl.parent)
        mako_runtime._exec_template(callable_, context, args=args, kwargs=kwargs)

## see: korpokkur.interfaces:IEmitter
@implementer(IEmitter)
class MakoEmitter(object):
    @classmethod
    def create_from_setting(cls, settings):
        env_factory = settings.get("env_factory", InputEnv)
        return cls(env_factory)

    def __init__(self, env_factory):
        self.env_factory = env_factory
        self.lookup_cache = {}

    def get_lookup(self, dirpath):
        try:
            return self.lookup_cache[dirpath]
        except KeyError:
            lookup = self.lookup_cache[dirpath] = MakoInputEnvLookup(directories=[dirpath])
            return lookup

    def emit(self, input, text=None, filename=None):
        assert text or filename
        if text and filename:
            text = None
        env = self.env_factory(input)
        lookup = None
        if filename and os.path.isabs(filename):
            lookup = self.get_lookup(os.path.dirname(filename))
        return MakoInputEnvTemplate(text=text, filename=filename, lookup=lookup).render_by_env(env)

def includeme(config):
    config.add_plugin("emitter.mako", MakoEmitter, categoryname="emitter")
