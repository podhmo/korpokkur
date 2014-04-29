# -*- coding:utf-8 -*-

from zope.interface import implementer
from mako_scaffold.interfaces import IMakoScaffoldTemplate

## see: mako_scaffold.interfaces:IMakoScaffoldTemplate
@implementer(IMakoScaffoldTemplate)
class Package(object):
    """tiny python package scaffold (this is sample)"""
    pass
