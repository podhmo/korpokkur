# -*- coding:utf-8 -*-
import os.path
import sys
from korpokkur.command import main

def err(s):
    sys.stderr.write(s)
    sys.stderr.write("\n")

def cleanup():
    err("cleanup ..")
    if os.path.exists(os.path.join(here, "build")):
        import shutil
        shutil.rmtree(os.path.join(here, "build"))


here = os.path.abspath(os.path.dirname(__file__))
cleanup()
main("_ create --logging DEBUG --config {here}/foo.ini package[pytest] {here}/build".format(here=here).split(" "))

is_exists = lambda x : os.path.exists(os.path.join(here, "build", x))

assert (is_exists("foo"))
assert (is_exists("foo/setup.py"))
assert (is_exists("foo/.gitignore"))

print("ok")

