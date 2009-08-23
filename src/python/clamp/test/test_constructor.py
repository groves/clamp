from java.io import EOFException
from java.lang import Integer, String
from nose.tools import eq_

import clamp
from org.sevorg.clamp import Reflector

class PrimitiveArg(clamp.Clamp):
    @clamp.java(Integer.TYPE, throws=[EOFException])
    def __init__(self, val):
        self.val = val

def test_constructor_gen():
    eq_('clamp.test.test_constructor.PrimitiveArg', PrimitiveArg(7).getClass().name)
    inst = Reflector.instantiate(PrimitiveArg, [Integer.TYPE], [7])
    eq_(7, inst.val)
    # check against the 1st constructor as we're generating a superfluous no-arg constructor
    eq_(EOFException, inst.getClass().constructors[1].exceptionTypes[0])

class OptionalArg(clamp.Clamp):
    @clamp.java(String, String)
    def __init__(self, first=None, second=7):
        self.first = first
        self.second = second

def test_default_constructor():
    allarg = Reflector.instantiate(OptionalArg, [String, String], ['one', 'two'])
    eq_("one", allarg.first)
    eq_("two", allarg.second)
    onearg = Reflector.instantiate(OptionalArg, [String], ['one'])
    eq_("one", onearg.first)
    eq_(7, onearg.second)
    noarg = Reflector.instantiate(OptionalArg, [], [])
    eq_(None, noarg.first)
    eq_(7, noarg.second)
