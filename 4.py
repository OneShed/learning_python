import os
import sys

import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    pass
    #unittest.main()

class A():
    def getPath(self):
        print(self._path)
        self.fce()

    main = getPath()




class b(A):
    def __init__(self, path):
        print('konstruktor')
        self._path = path
    def fce(self):
        print('foo')


A.getPath.main()


