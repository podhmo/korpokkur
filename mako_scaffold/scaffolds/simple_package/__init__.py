# -*- coding:utf-8 -*-

from zope.interface import implementer
from mako_scaffold.interfaces import IScaffoldTemplate
import os.path

## see: mako_scaffold.interfaces:IScaffoldTemplate
@implementer(IScaffoldTemplate)
class Package(object):
    """tiny python package scaffold (this is sample)"""
    source_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), "+package+")
    expected_words = [
        ("package", "package name")
    ]
