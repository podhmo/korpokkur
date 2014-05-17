# -*- coding:utf-8 -*-

from zope.interface import implementer
from korpokkur.interfaces import IScaffoldTemplate
from korpokkur.input import compute_value
import os.path

## see: korpokkur.interfaces:IScaffoldTemplate
@implementer(IScaffoldTemplate)
class Template(object):
    """korpokkur scaffold template template"""
    source_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), "+package+")
    ##varname -> description, default
    expected_words = {
        "package": ("package name", "foo.boo"), 
        "description": ("template description", "boo for foo"), 
        "version": ("version number for project", "0.0"), 
        "scaffold_name": ("scaffold name when shown by koropokkur list", ""), 
    }
    cache = {
        "replace_package": "+package+", 
        "package_prefix": compute_value(lambda input, _: input.load("package").split(".", 1)[0]),
        "package_suffix": compute_value(lambda input, _: input.load("package").split(".", 1)[1]),
    }
    __dro__ = ["korpokkur.scaffolds.pygitignore:Package"] #todo:validation
    template_engine = "mako"
