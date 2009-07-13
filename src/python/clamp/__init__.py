from java.lang import Class
from org.sevorg.clamp import AbstractClassBuilder, InterfaceBuilder

class JavaConstructorInfo(object):
    def __init__(self, argtypes, **kwargs):
        self.argtypes = extract_argcombinations(argtypes)
        self.throws = []
        for k, v in kwargs.iteritems():
            if k == 'throws':
                self.throws = v
            else:
                raise TypeError("clamp doesn't understand keyword argument '%s'" % k)

class JavaMethodInfo(JavaConstructorInfo):
    def __init__(self, returntype, argtypes, **kwargs):
        JavaConstructorInfo.__init__(self, argtypes, **kwargs)
        self.returntype = returntype

def java(*argTypes, **kwargs):
    def jconst(f):
        if f.__name__ == "__init__":
            f._clamp = JavaConstructorInfo(argTypes, **kwargs)
        else:
            f._clamp = JavaMethodInfo(argTypes[0], argTypes[1:], **kwargs)
        return f
    return jconst

def extract_argcombinations(argtypes):
    '''Takes a list of Java types and returns a list of lists of overloaded combinations.

    If any position in the initial list is itself a list, an overloaded method is created for each
    of the arg types in the list.'''
    argcombinations = [[]]
    for arg in argtypes:
        if not hasattr(arg, '__iter__'):
            arg = [arg]
        newcombinations = []
        for option in arg:
            if not isinstance(option, Class):
                raise TypeError("clamp only takes Java classes as argument types, not '%s'" %
                        option)
            for combo in argcombinations:
                newcombinations.append(combo[:])
                newcombinations[-1].append(option)
        argcombinations = newcombinations
    return argcombinations

class Clamper(type):
    def __new__(meta, name, bases, dict):
        builder = None
        if '__init__' in dict and hasattr(dict['__init__'], '_clamp'):
            builder = AbstractClassBuilder("A" + name)
            info = dict['__init__']._clamp
            for combo in info.argtypes:
                builder.addConstructor(combo, info.throws)
        for k, v in dict.iteritems():
            if hasattr(v, '_clamp') and not k == '__init__':
                if builder is None:
                    builder = InterfaceBuilder("I" + name)
                for combo in v._clamp.argtypes:
                    builder.addMethod(k, v._clamp.returntype, combo, v._clamp.throws)
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
