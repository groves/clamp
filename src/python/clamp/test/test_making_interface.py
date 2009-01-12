from java.lang import String

import clamp
from org.sevorg.clamp import Instantiator

class Foo(clamp.Clamp):
    @clamp.javamethod(String)
    def getName(self):
        return 'name'

def testInstantiating():
    assert Instantiator.instantiateAndCall(Foo, 'getName') == Foo().name # Foo picks up a Java bean accessor by having a get* method...
