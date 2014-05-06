# -*- coding:utf-8 -*-

from zope.interface import implementer
from korpokkur.interfaces import IScaffoldTemplate
import os.path

## see: korpokkur.interfaces:IScaffoldTemplate
@implementer(IScaffoldTemplate)
class Template(object):
    """korpokkur scaffold template template"""
    source_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), "+package+")
    ##varname -> description, default
    expected_words = {
        "package": ("package name", "sample"), 
        "description": ("template description", "-"), 
        "version": ("version number for project", "0.0"), 
        "scaffold_name": ("scaffold name when shown by koropokkur list", ""), 
    }
    cache = {"replace_package": "+package+"}
    __dro__ = ["korpokkur.scaffolds.pygitignore:Package"] #todo:validation
    template_engine = "mako"
