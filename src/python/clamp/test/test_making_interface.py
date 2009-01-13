from java.lang import Integer, String, Void
from nose.tools import assert_true, eq_

import clamp
from org.sevorg.clamp import Reflector

class Foo(clamp.Clamp):
    def __init__(self):
        self.val = 7

    @clamp.javamethod(String)
    def getName(self):
        return 'name'

    @clamp.javamethod(Integer.TYPE)
    def getValue(self):
        return self.val

    @clamp.javamethod(Void.TYPE, Integer.TYPE)
    def setValue(self, val):
        self.val = val

def testInstantiating():
    eq_("name", Foo().name) # Foo picks up a Java bean accessor by having a get* method...
    jcreated = Reflector.instantiate(Foo)
    assert_true(isinstance(jcreated, Foo))
    eq_("name", Reflector.call(jcreated, 'getName'))

def testPrimitiveReturn():
    eq_(7, Foo().getValue())
    eq_(7, Reflector.call(Foo(), "getValue"))

def testPrimitiveArgument():
    f = Foo()
    f.setValue(12)
    eq_(12, f.value)
    f.value += 1
    eq_(13, f.getValue())
    Reflector.call(f, "setValue", [Integer.TYPE], [18])
    eq_(18, f.value)

