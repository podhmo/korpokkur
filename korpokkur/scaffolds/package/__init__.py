# -*- coding:utf-8 -*-

from zope.interface import implementer
from korpokkur.interfaces import IScaffoldTemplate
from korpokkur.input import compute_value
import os.path


# see: korpokkur.interfaces:IScaffoldTemplate
@implementer(IScaffoldTemplate)
class Package(object):
    """sample python package scaffold extensions=[nose, pytest]"""
    source_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), "+package+")
    # varname -> description, default
    expected_words = {
        "package": ("package name", "sample"),
        "description": ("package description", "-"),
        "version": ("version number for project", "0.0")
    }
    cache = {
        "module": compute_value(lambda input, _: input.load("package").replace("-", "_"))
    }
    __dro__ = ["korpokkur.scaffolds.pygitignore:Package"]  # todo:validation
    template_engine = "mako"
    support_extensions = ["unittest", "nose", "pytest"]  # default is unittest
