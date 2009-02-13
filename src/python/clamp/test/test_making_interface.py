from java.io import EOFException, FileNotFoundException 
from java.lang import Integer, Number, String, Void
from java.math import BigInteger
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

    @clamp.javamethod(Number, Number,
            exceptions=[FileNotFoundException, EOFException])
    def doubleIt(self, number):
        return number.longValue() * 2


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

def testObjectArgument():
    f = Foo()
    base = BigInteger.valueOf(12)
    result = base.multiply(BigInteger.valueOf(2))
    eq_(result , f.doubleIt(base))
    eq_(result, Reflector.call(f, "doubleIt", [Number], [base]))
    #XXX: getting to the IFoo interface this way is brittle.
    iface = f.__class__.__base__.__bases__[0]
    excepts = Reflector.getExceptionTypes(iface, "doubleIt", [Number])
    eq_(len(excepts), 2)
