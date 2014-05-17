# -*- coding:utf-8 -*-

from zope.interface import implementer
from korpokkur.interfaces import IScaffoldTemplate
from korpokkur.input import compute_value
import os.path

## see: korpokkur.interfaces:IScaffoldTemplate
@implementer(IScaffoldTemplate)
class Package(object):
    """nested python package scaffold(e.g. foo.boo) extensions=[nose, pytest]"""
    source_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), "+package+")
    ##varname -> description, default
    expected_words = {
        "package": ("package name", "foo.boo"), 
        "description": ("package description", "boo for foo"), 
        "version": ("version number for project", "0.0")
    }
    cache = {
        "package_prefix": compute_value(lambda input, _: input.load("package").split(".", 1)[0]),
        "package_suffix": compute_value(lambda input, _: input.load("package").split(".", 1)[1]),
    }
    __dro__ = ["korpokkur.scaffolds.pygitignore:Package"] #todo:validation
    template_engine = "mako"
    support_extensions = ["unittest", "nose", "pytest"] #default is unittest
