from org.sevorg.clamp import AbstractClassBuilder, InterfaceBuilder

def javaconstructor(*argTypes, **kwargs):
    def jconst(f):
        f._clamp = (argTypes, kwargs)
        return f
    return jconst

def javamethod(returnType, *argTypes, **kwargs):
    def jmethod(f):
        f._clamp = (returnType, argTypes, kwargs)
        return f
    return jmethod

def extract_argcombinations(argtypes):
    '''Takes a list of Java types and returns a list of lists of overloaded combinations.

    If any position in the initial list is itself a list, an overloaded method is created for each
    of the arg types in the list.'''
    argcombinations = [[]]
    for arg in argtypes:
        if hasattr(arg, '__iter__'):
            newcombinations = []
            for option in arg:
                for combo in argcombinations:
                    newcombinations.append(combo[:])
                    newcombinations[-1].append(option)
            argcombinations = newcombinations
        else:
            for combo in argcombinations:
                combo.append(arg)
    return argcombinations

class Clamper(type):
    def __new__(meta, name, bases, dict):
        builder = None
        if '__init__' in dict and hasattr(dict['__init__'], '_clamp'):
            argtypes, javaOpts = dict['__init__']._clamp
            builder = AbstractClassBuilder("A" + name)
            for combo in extract_argcombinations(argtypes):
                builder.addConstructor(combo)
        for k, v in dict.iteritems():
            if hasattr(v, '_clamp') and not k == '__init__':
                if builder is None:
                    builder = InterfaceBuilder("I" + name)
                javaReturn, argtypes, javaOpts = v._clamp
                exceptions = javaOpts.get("exceptions", [])
                for combo in extract_argcombinations(argtypes):
                    builder.addMethod(k, javaReturn, combo, exceptions)
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
