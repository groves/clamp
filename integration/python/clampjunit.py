from junit.framework import TestCase

from clamp import Clamp, java, jvoid

class TestJUnit(Clamp, TestCase):
    @java(jvoid)
    def testAddition(self):
        self.assertEquals(4, 1 + 3)
