#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Reproduce book environment
import random
random.seed(1234)

import logging
from pprint import pprint
from sys import stdout as STDOUT

# Write all output to a temporary directory
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

# Make sure Windows processes exit cleanly
OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)

def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()

atexit.register(close_open_files)


# Example 1
class MyBaseClass:
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    def __init__(self):#gets value from parents class
        MyBaseClass.__init__(self, 5)#add value to var in parent class

    def times_two(self):
        return self.value * 2

foo = MyChildClass()
assert foo.times_two() == 10
print(foo.times_two())#10


# Example 2
class TimesTwo:
    def __init__(self):
        self.value *= 2

class PlusFive:
    def __init__(self):
        self.value += 5


# Example 3
class OneWay(MyBaseClass, TimesTwo, PlusFive):#class with link to other classes
    def __init__(self, value):
        MyBaseClass.__init__(self, value)#orig class with link to parent
        TimesTwo.__init__(self)#independent class
        PlusFive.__init__(self)#independent class
        

# Example 4
foo = OneWay(5)#call overview class
print('First ordering value is (5 * 2) + 5 =', foo.value)#init value from orig class used with different methods


# Example 5
class AnotherWay(MyBaseClass, PlusFive, TimesTwo):#overview class link to other classes
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


# Example 6
bar = AnotherWay(5)#call overview class as new class order args not relevant for result
print('Second ordering value is', bar.value)


# Example 7
class TimesSeven(MyBaseClass):#class with link to parent
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 7

class PlusNine(MyBaseClass):#class with link to parent
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 9


# Example 8
class ThisWay(TimesSeven, PlusNine):#overview class with link to classes
    def __init__(self, value):
        TimesSeven.__init__(self, value)
        PlusNine.__init__(self, value)

a=TimesSeven(5)
print(a.value)#35
b=PlusNine(5)
print(b.value)#14
foo = ThisWay(5)
print('Should be (5 * 7) + 9 = 44 but is', foo.value)#Should be (5 * 7) + 9 = 44 but is 14 => var seems to be overwritten


# Example 9
class MyBaseClass:
    def __init__(self, value):
        self.value = value

class TimesSevenCorrect(MyBaseClass):#first in stack last executed
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7

class PlusNineCorrect(MyBaseClass):#second in stack lifo system so first add then multiply
    def __init__(self, value):
        super().__init__(value)
        self.value += 9


# Example 10
class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    def __init__(self, value):
        super().__init__(value)

foo = GoodWay(5)
print('Should be 7 * (5 + 9) = 98 and is', foo.value)#Should be 7 * (5 + 9) = 98 and is 98


# Example 11
mro_str = '\n'.join(repr(cls) for cls in GoodWay.mro())#Return a type's method resolution order.
print(mro_str)
#<class '__main__.GoodWay'>
#<class '__main__.TimesSevenCorrect'>
#<class '__main__.PlusNineCorrect'>
#<class '__main__.MyBaseClass'>
#<class 'object'>


# Example 12
class ExplicitTrisect(MyBaseClass):
    def __init__(self, value):
        
        super(ExplicitTrisect, self).__init__(value)#detailed call of super even same class
        self.value /= 3
assert ExplicitTrisect(9).value == 3


# Example 13
class AutomaticTrisect(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value)#detailed call of super even same class
        self.value /= 3

class ImplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)#standaard call of super
        self.value /= 3

assert ExplicitTrisect(9).value == 3
assert AutomaticTrisect(9).value == 3
assert ImplicitTrisect(9).value == 3
