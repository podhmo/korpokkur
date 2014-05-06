# -*- coding:utf-8 -*-
import pkg_resources

def import_symbol(symbol): #todo cache
    return pkg_resources.EntryPoint.parse("x=%s" % symbol).load(False)

