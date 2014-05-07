# -*- coding:utf-8 -*-
import unittest
class ScaffoldSplitNameTests(unittest.TestCase):
    def _callFUT(self, name):
        from korpokkur.scaffoldgetter import ScaffoldGetter
        getter = ScaffoldGetter()
        return getter.split_scaffold_name(name)

    def test_with_normal_name(self):
        name = "scaffold"
        result = self._callFUT(name)
        self.assertEqual(result, ("scaffold", set()))

    def test_with_extension_name(self):
        name = "scaffold[pytest]"
        result = self._callFUT(name)
        self.assertEqual(result, ("scaffold", set(["pytest"])))

    def test_with_extension_name2(self):
        name = "scaffold[pytest mock fixture]"
        result = self._callFUT(name)
        self.assertEqual(result, ("scaffold", set(["pytest", "mock", "fixture"])))
