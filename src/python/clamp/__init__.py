from org.sevorg.clamp import AbstractClassBuilder, InterfaceBuilder

def javaconstructor(*argTypes):
    def jconst(f):
        f._clamp = argTypes
        return f
    return jconst

def javamethod(returnType, *argTypes):
    def jmethod(f):
        f._clamp = (returnType, argTypes)
        return f
    return jmethod

class Clamper(type):
    def __new__(meta, name, bases, dict):
        builder = None
        if '__init__' in dict and hasattr(dict['__init__'], '_clamp'):
            builder = AbstractClassBuilder("A" + name, dict['__init__']._clamp)
        for k, v in dict.iteritems():
            if hasattr(v, '_clamp') and not k == '__init__':
                if builder is None:
                    builder = InterfaceBuilder("I" + name)
                javaReturn, javaArgs = v._clamp
                builder.addMethod(k, javaReturn, javaArgs, [])
        if builder is None:# No new clamped methods on a subinterface, let it be
            return type.__new__(meta, name, bases, dict)
        iface = builder.load()
        newbases = []
        for base in bases:
            if type(base) == meta:# Remove the meta-type; PyType can't handle it yet
                newbases.append(iface)
            else:
                newbases.append(base)
        bases = tuple(newbases)
        if '__javaname__' not in dict:
            dict['__javaname__'] = '%s.%s' % (dict['__module__'], name)
        return type.__new__(type, name, bases, dict)

class Clamp(object):
    __metaclass__ = Clamper
