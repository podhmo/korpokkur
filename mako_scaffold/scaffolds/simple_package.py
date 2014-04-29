# -*- coding:utf-8 -*-

from zope.interface import implementer
from mako_scaffold.interfaces import IScaffoldTemplate

## see: mako_scaffold.interfaces:IScaffoldTemplate
@implementer(IScaffoldTemplate)
class Package(object):
    """tiny python package scaffold (this is sample)"""
    pass
