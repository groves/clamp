from java.io import EOFException, FileNotFoundException 
from java.lang import Number, String
from java.math import BigInteger
from nose.tools import assert_true, assert_raises, eq_

import clamp
from org.sevorg.clamp import Reflector

class Foo(clamp.Clamp):
    def __init__(self):
        self.val = 7

    @clamp.java(String)
    def getName(self):
        return 'name'

    @clamp.java(clamp.jint)
    def getValue(self):
        return self.val

    @clamp.java(clamp.jvoid, clamp.jint)
    def setValue(self, val):
        self.val = val

    @clamp.java(Number, Number, throws=[FileNotFoundException, EOFException])
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
    Reflector.call(f, "setValue", [clamp.jint], [18])
    eq_(18, f.value)

def testObjectArgument():
    f = Foo()
    base = BigInteger.valueOf(12)
    result = base.multiply(BigInteger.valueOf(2))
    eq_(result.longValue(), f.doubleIt(base))
    eq_(result, Reflector.call(f, "doubleIt", [Number], [base]))
    eq_(len(Reflector.getExceptionTypes(f.getClass(), "doubleIt", [Number])), 2)

def testDisallowedJavaMethodNames():
    def will_by_numbername():
        pass
    will_by_numbername.func_name = '7name'
    assert_raises(ValueError, clamp.java(clamp.jvoid), will_by_numbername)
    def double(): pass
    assert_raises(ValueError, clamp.java(clamp.jvoid), double)

