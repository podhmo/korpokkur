# -*- coding:utf-8 -*-
def call(ob, name, *args, **kwargs):
    return getattr(ob, name)(*args, **kwargs)
