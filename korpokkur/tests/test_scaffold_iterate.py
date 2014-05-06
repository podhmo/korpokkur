# -*- coding:utf-8 -*-
import unittest

class ScaffoldIterateTests(unittest.TestCase):
    def _getTarget(self):
        from korpokkur.scaffoldgetter import Scaffold
        return Scaffold

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_it__simplest_forward(self):
        class A(object):
            pass
        class B(object):
            pass
        class C(object):
            pass
        A.__dro__ = [B]
        B.__dro__ = [C]

        target = self._makeOne(A, lookup=lambda x: x)
        children = list(target.iterate_children())

        self.assertEqual(len(children), 2)
        self.assertEqual(children[0].template, B)
        self.assertEqual(children[1].template, C)

    def test_it__same_children(self):
        class A(object):
            pass
        class B1(object):
            pass
        class B2(object):
            pass
        class C(object):
            pass
        A.__dro__ = [B1, B2]
        B1.__dro__ = [C]
        B2.__dro__ = [C]

        target = self._makeOne(A, lookup=lambda x: x)
        children = list(target.iterate_children())

        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].template, B1)
        self.assertEqual(children[1].template, C)
        self.assertEqual(children[2].template, B2)

    def test_it_cycled(self):
        class A(object):
            pass
        class B(object):
            pass
        class C(object):
            pass
        A.__dro__ = [B]
        B.__dro__ = [C]
        C.__dro__ = [A]

        target = self._makeOne(A, lookup=lambda x: x)
        children = list(target.iterate_children())

        self.assertEqual(len(children), 2)
        self.assertEqual(children[0].template, B)
        self.assertEqual(children[1].template, C)
