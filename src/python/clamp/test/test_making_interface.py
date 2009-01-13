from java.lang import Integer, String
from nose.tools import assert_true, eq_

import clamp
from org.sevorg.clamp import Reflector

class Foo(clamp.Clamp):
    @clamp.javamethod(String)
    def getName(self):
        return 'name'

    @clamp.javamethod(Integer.TYPE)
    def getValue(self):
        return 7

def testInstantiating():
    eq_("name", Foo().name) # Foo picks up a Java bean accessor by having a get* method...
    jcreated = Reflector.instantiate(Foo)
    assert_true(isinstance(jcreated, Foo))
    eq_("name", Reflector.call(jcreated, 'getName'))

def testPrimitiveReturn():
    eq_(7, Foo().getValue())
    eq_(7, Reflector.call(Foo(), "getValue"))
