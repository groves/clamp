from java.util import AbstractList
from clamp import Clamp
from org.sevorg.clamp import TestSubclassing

class ClampedList(Clamp, AbstractList):
    def get(self, idx):
        return idx

    def size(self):
        return 10

def test_extendingclass():
    TestSubclassing.manipulate(ClampedList())
