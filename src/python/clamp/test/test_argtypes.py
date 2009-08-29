from java.lang import String
from clamp import Clamp, java, jint, extract_argcombinations
from org.sevorg.clamp import Reflector

from nose.tools import assert_raises, eq_

class OverloadedMethods(Clamp):
    @java([jint, String])
    def __init__(self, arg):
        self.val = self.primitiveOrObject(arg)

    @java(String, [jint, String])
    def primitiveOrObject(self, arg):
        if isinstance(arg, int):
            return 'int'
        else:
            return 'String'

    @java(String, [jint, String])
    def overloadedDefault(self, arg=7.0):
        if isinstance(arg, float):
            return 'float'
        elif isinstance(arg, int):
            return 'int'
        else:
            return 'String'

def testOnClass():
    eq_("int", Reflector.call(OverloadedMethods(7), "primitiveOrObject", [jint], [12]))
    eq_("String", Reflector.call(OverloadedMethods('hi'), "primitiveOrObject", [String], ["hello"]))
    eq_("int", Reflector.instantiate(OverloadedMethods, [jint], [7]).val)
    eq_("int", Reflector.call(OverloadedMethods(7), "overloadedDefault", [jint], [12]))
    eq_("String", Reflector.call(OverloadedMethods('hi'), "overloadedDefault", [String], ["hello"]))
    eq_("float", Reflector.call(OverloadedMethods('hi'), "overloadedDefault", [], []))

def eq_unordered(list1, list2):
    eq_(len(list1), len(list2))
    for item in list2:
        assert item in list1, '%s in one list but not another' % item

def test_combinations():
    eq_unordered([[jint], [String]], extract_argcombinations([[jint, String]]))
    eq_unordered([[], [jint], [String]], extract_argcombinations([[jint, String]], 1))
    eq_unordered([[jint, String], [jint, jint]], extract_argcombinations([jint, [jint, String]]))
    eq_unordered([[jint, String], [jint, jint], [String, jint], [String, String]],
        extract_argcombinations([[jint, String], [jint, String]]))
    assert_raises(TypeError, extract_argcombinations, [None])
    assert_raises(TypeError, extract_argcombinations, [[None]])
    assert_raises(TypeError, extract_argcombinations, [[String, [jint, None]]])
