from org.sevorg.clamp import InterfaceBuilder

def javamethod(returnType, *argTypes):
    def jmethod(f):
        f._clamp = (returnType, argTypes)
        return f
    return jmethod

class Clamper(type):
    def __new__(meta, name, bases, dict):
        builder = None
        for k, v in dict.iteritems():
            if hasattr(v, '_clamp'):
                if builder is None:
                    builder = InterfaceBuilder("I" + name)
                javaReturn, javaArgs = v._clamp
                builder.addMethod(k, javaReturn, javaArgs, [])
        if builder is None:
            return type.__new__(meta, name, bases, dict)
        if builder is not None:
            iface = builder.load()
            newbases = []
            for base in bases:
                if type(base) == meta:
                    newbases.append(iface)
                else:
                    newbases.append(base)
            bases = tuple(newbases)
        return type.__new__(type, name, bases, dict)

class Clamp(object):
    __metaclass__ = Clamper
