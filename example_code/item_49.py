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
import json

class Serializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


# Example 2
class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'

point = Point2D(5, 3)
print('Object:    ', point)#without json method but dunder rpr method
print('Serialized:', point.serialize())#with json method


# Example 3
class Deserializable(Serializable):#extend class as own method with decorator
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


# Example 4
class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'

before = BetterPoint2D(5, 3)
print('Before:    ', before)#Before:     Point2D(5, 3) returns the dunder rpr method
data = before.serialize()
print('Serialized:', data)#Serialized: {"args": [5, 3]} return dict like key/list pair
after = BetterPoint2D.deserialize(data)
print('After:     ', after)#After:      Point2D(5, 3) return dunder rpr by latest class


# Example 5
class BetterSerializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })

    def __repr__(self):
        name = self.__class__.__name__
        args_str = ', '.join(str(x) for x in self.args)
        return f'{name}({args_str})'


# Example 6
registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):# input ->Serialized: {"class": "EvenBetterPoint2D", "args": [5, 3]}
    params = json.loads(data)#use input/output for method with key/pair,key/list construct
    name = params['class']#is the key
    target_class = registry[name]
    return target_class(*params['args'])#use connect key ->value,key -> list


# Example 7
class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

register_class(EvenBetterPoint2D)


# Example 8
before = EvenBetterPoint2D(5, 3)
print('Before:    ', before)#Before:     EvenBetterPoint2D(5, 3) use rpr method class name and loop over args
data = before.serialize()
print('Serialized:', data)#Serialized: {"class": "EvenBetterPoint2D", "args": [5, 3]} construct looks as dict of key/value and key/list pair
after = deserialize(data)
print('After:     ', after)#After:      EvenBetterPoint2D(5, 3) 


# Example 9
class Point3D(BetterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z


# Forgot to call register_class! Whoops!
register_class(Point3D)

# Example 10
try:
    point = Point3D(5, 9, -4)
    data = point.serialize()
    deserialize(data)
except:
    logging.exception('Expected')
else:
    assert False#not false after ->register_class(Point3D)

try:
    point = Point3D(5, 9, -4)
    data = point.serialize() #key/value,key/list construct
    deserialize(data)#Point3D(5, 9, -4) 
except:
    logging.exception('Expected')
else:
    assert True#return ->Point3D(5, 9, -4) 

# Example 11
class Meta(type):
    def __new__(meta, name, bases, class_dict):#class,name,tuple and a dict
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable,
                             metaclass=Meta):#to get the register class solved
    pass


# Example 12
class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

before = Vector3D(10, -7, 3)
print('Before:    ', before)#standard rpr method
data = before.serialize()#return key/value,key/list
print('Serialized:', data)
print('After:     ', deserialize(data))#input return key/value,key/list construct


# Example 13
class BetterRegisteredSerializable(BetterSerializable):#call with register
    def __init_subclass__(cls):
        super().__init_subclass__()
        register_class(cls)

class Vector1D(BetterRegisteredSerializable):#add var to class construct
    def __init__(self, magnitude):
        super().__init__(magnitude)
        self.magnitude = magnitude

before = Vector1D(6)#standard call ->Before:     Vector1D(6)
print('Before:    ', before)
data = before.serialize()
print('Serialized:', data)#Serialized: {"class": "Vector1D", "args": [6]}
print('After:     ', deserialize(data))#After:      Vector1D(6)
