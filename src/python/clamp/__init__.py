from java.lang import Class, Object
from org.python.core.util import StringUtil
from org.sevorg.clamp import ClampMetaclass as Clamper

class JavaCallableInfo(object):
    def __init__(self, numdefaults, argtypes, **kwargs):
        self.argtypes = extract_argcombinations(argtypes, numdefaults)
        self.throws = []
        for k, v in kwargs.iteritems():
            if k == 'throws':
                self.throws = v
            else:
                raise TypeError("clamp doesn't understand keyword argument '%s'" % k)

class JavaConstructorInfo(JavaCallableInfo):
    def __init__(self, numdefaults, argtypes, **kwargs):
        JavaCallableInfo.__init__(self, numdefaults, argtypes, **kwargs)
        # No-arg constructor for subclass that handles initializing everything
        # TODO - check if this is extending a Java class that requires args and disable this
        if not [] in self.argtypes:
            self.argtypes.append([])

class JavaMethodInfo(JavaCallableInfo):
    def __init__(self, numdefaults, returntype, argtypes, **kwargs):
        JavaCallableInfo.__init__(self, numdefaults, argtypes, **kwargs)
        if not isinstance(returntype, Class):
            raise TypeError("returntypes must be an instance of java.lang.Class")
        self.returntype = returntype

def java(*argtypes, **kwargs):
    def jconst(f):
        if f.func_defaults:
            numdefaults = len(f.func_defaults)
        else:
            numdefaults = 0
        if f.__name__ == "__init__":
            f._clamp = JavaConstructorInfo(numdefaults, argtypes, **kwargs)
        else:
            if not StringUtil.isJavaIdentifier(f.func_name):
                raise ValueError("clamped method name '%s' isn't a valid Java identifier" %
                        f.func_name)
            if len(argtypes) == 0:
                raise ValueError("clamped methods must specify a return type as their first arg. \
Use java.lang.Void to indicate returning nothing.")
            f._clamp = JavaMethodInfo(numdefaults, argtypes[0], argtypes[1:], **kwargs)
        return f
    return jconst

def extract_argcombinations(argtypes, numdefaults=0):
    '''Takes a list of Java Classes and returns a list of lists of overloaded combinations.

    If any item in the initial list is itself a list, an overloaded method is created for each
    of the arg types in the list.'''
    finishedcombinations = []
    argcombinations = [[]]
    completeidx = len(argtypes) - numdefaults - 1
    if completeidx == -1:
        finishedcombinations.append([])
    for idx, arg in enumerate(argtypes):
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
        if idx >= completeidx:
            finishedcombinations.extend(argcombinations)
    return finishedcombinations

class Clamp(object):
    __metaclass__ = Clamper
