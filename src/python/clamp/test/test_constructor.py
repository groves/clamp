from java.io import EOFException
from java.lang import Integer
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
    eq_(EOFException, inst.getClass().superclass.constructors[1].exceptionTypes[0])
