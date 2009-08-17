from java.lang import Integer, UnsupportedOperationException
from java.util import AbstractList

from nose.tools import assert_raises, eq_

from clamp import Clamp, java
from org.sevorg.clamp import Reflector


class ClampedList(Clamp, AbstractList):
    def get(self, idx):
        return idx

    def size(self):
        return 10

def test_extendingclass():
    clamped = Reflector.instantiate(ClampedList, [], [])
    eq_(5, Reflector.call(clamped, 'get', [Integer.TYPE], [5]))
    assert_raises(UnsupportedOperationException, clamped.add, 5)

class ExtraMethodList(ClampedList):
    @java(Integer.TYPE)
    def last(self):
        return self[-1]

def test_extendingclamped():
    extra = Reflector.instantiate(ExtraMethodList, [], [])
    last = Reflector.call(extra, "last", [], [])
    eq_(9, last)
