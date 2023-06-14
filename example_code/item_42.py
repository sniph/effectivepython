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
class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10 #use of double underscore

    def get_private_field(self):
        return self.__private_field


# Example 2
foo = MyObject()
assert foo.public_field == 5


# Example 3
#assert foo.__private_field == 10 #AttributeError: 'MyObject' object has no attribute '__private_field'. Did you mean: 'get_private_field'?
assert foo.get_private_field() == 10


# Example 4
try:
    foo.__private_field #call only through method ->foo.get_private_field()
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod #parse args of class
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
#assert bar.__private_field == 71 #AttributeError: 'MyOtherObject' object has no attribute '__private_field'
assert MyOtherObject.get_private_field_of_instance(bar) == 71 


# Example 6
try:
    class MyParentObject:
        def __init__(self):
            self.__private_field = 71
    
    class MyChildObject(MyParentObject):
        def get_private_field(self):
            return self.__private_field
    
    baz = MyChildObject()
    #baz.get_private_field()
except:
    logging.exception('Expected')
else:
    assert False


# Example 7
assert baz._MyParentObject__private_field == 71


# Example 8
print(baz.__dict__)#a dict is created default "_" as start of name_dict


# Example 9
class MyStringClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

foo = MyStringClass(5)
assert foo.get_value() == '5'#call method to get value as string


# Example 10
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)

foo = MyIntegerSubclass('5')
assert foo.get_value() == 5#call method to get value as int


# Example 11
class MyBaseClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

class MyStringClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())         # Updated

class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)  # Not updated


# Example 12
try:
    foo = MyIntegerSubclass('5')#the value is not converted to int ->'5'
    foo.get_value()
except:
    logging.exception('Expected')
else:
    assert False


# Example 13
class MyStringClass:
    def __init__(self, value):
        # This stores the user-supplied value for the object.
        # It should be coercible to a string. Once assigned in
        # the object it should be treated as immutable.
        self._value = value


    def get_value(self):
        return str(self._value)
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return self._value

foo = MyIntegerSubclass(5)
assert foo.get_value() == 5
print(foo.get_value())#doesn't change to string


# Example 14
class ApiClass:
    def __init__(self):#notice one underscore can be overwritten
        self._value = 5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # Conflicts

a = Child()
print(f'{a.get()} and {a._value} should be different') #result strang -> "hello and hello should be different"

mro_str = '\n'.join(repr(cls) for cls in Child.mro())#Return a type's method resolution order.
print(mro_str)
#<class '__main__.Child'>
#<class '__main__.ApiClass'>
#<class 'object'>


# Example 15
class ApiClass:
    def __init__(self):
        self.__value = 5       # Double underscore

    def get(self):
        return self.__value    # Double underscore

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # OK!

a = Child()
print(f'{a.get()} and {a._value} are different')#(extra)"_" gives unmutable value for call

mro_str = '\n'.join(repr(cls) for cls in Child.mro())#Return a type's method resolution order.
print(mro_str)

#<class '__main__.Child'>
#<class '__main__.ApiClass'>
#<class 'object'>