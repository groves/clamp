from java.lang import Integer, String
from clamp import Clamp, java, extract_argcombinations
from org.sevorg.clamp import Reflector

from nose.tools import assert_raises, eq_

class OverloadedMethods(Clamp):
    @java([Integer.TYPE, String])
    def __init__(self, arg):
        self.val = self.primitiveOrObject(arg)

    @java(String, [Integer.TYPE, String])
    def primitiveOrObject(self, arg):
        if isinstance(arg, int):
            return 'int'
        else:
            return 'String'

    @java(String, [Integer.TYPE, String])
    def overloadedDefault(self, arg=7.0):
        if isinstance(arg, float):
            return 'float'
        elif isinstance(arg, int):
            return 'int'
        else:
            return 'String'

def testOnClass():
    eq_("int", Reflector.call(OverloadedMethods(7), "primitiveOrObject", [Integer.TYPE], [12]))
    eq_("String", Reflector.call(OverloadedMethods('hi'), "primitiveOrObject", [String], ["hello"]))
    eq_("int", Reflector.instantiate(OverloadedMethods, [Integer.TYPE], [7]).val)
    eq_("int", Reflector.call(OverloadedMethods(7), "overloadedDefault", [Integer.TYPE], [12]))
    eq_("String", Reflector.call(OverloadedMethods('hi'), "overloadedDefault", [String], ["hello"]))
    eq_("float", Reflector.call(OverloadedMethods('hi'), "overloadedDefault", [], []))

def eq_unordered(list1, list2):
    eq_(len(list1), len(list2))
    for item in list2:
        assert item in list1, '%s in one list but not another' % item

def test_combinations():
    eq_unordered([[Integer.TYPE], [String]], extract_argcombinations([[Integer.TYPE, String]]))
    eq_unordered([[], [Integer.TYPE], [String]], extract_argcombinations([[Integer.TYPE, String]], 1))
    eq_unordered([[Integer.TYPE, String], [Integer.TYPE, Integer.TYPE]],
            extract_argcombinations([Integer.TYPE, [Integer.TYPE, String]]))
    eq_unordered([[Integer.TYPE, String], [Integer.TYPE, Integer.TYPE], [String, Integer.TYPE],
        [String, String]],
        extract_argcombinations([[Integer.TYPE, String], [Integer.TYPE, String]]))
    assert_raises(TypeError, extract_argcombinations, [None])
    assert_raises(TypeError, extract_argcombinations, [[None]])
    assert_raises(TypeError, extract_argcombinations, [[String, [Integer.TYPE, None]]])
