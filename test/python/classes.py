from java.lang import String
import clamp

class Foo(clamp.Clamp):
    @clamp.javamethod(String)
    def getName(self):
        return 'name'

from org.sevorg.clamp import Instantiator
print Instantiator.instantiateAndCall(Foo, 'getName')
print Foo().name # Foo picks up a Java bean accessor by having a get* method...
