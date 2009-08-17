from java.lang import String, Void
from junit.framework import TestCase

from clamp import Clamp, java

class TestJUnit(Clamp, TestCase):
    @java(Void)
    def testAddition(self):
        self.assertEquals(4, 1 + 3)
