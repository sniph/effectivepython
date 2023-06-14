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
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        global print
        orig_print = print
        print(f'* Running {meta}.__new__ for {name}')
        print('Bases:', bases)
        print = pprint
        print(class_dict)
        print = orig_print
        return type.__new__(meta, name, bases, class_dict) #=>see return type for args =># (method) def __new__(
#     cls: Type[Self@__new__],
#     __name: str,
#     __bases: tuple[type, ...],
#     __namespace: dict[str, Any],
#     **kwds: Any
# ) -> Self@__new__

class MyClass(metaclass=Meta):#use generic type construct in class arg
    stuff = 123

    def foo(self):
        pass

# * Running <class '__main__.Meta'>.__new__ for MyClass
# Bases: ()
# {'__module__': '__main__',
#  '__qualname__': 'MyClass',
#  'foo': <function MyClass.foo at 0x0000019757FC0790>,
#  'stuff': 123}

class MySubclass(MyClass):#use extend object as class arg
    other = 567

    def bar(self):
        pass

# * Running <class '__main__.Meta'>.__new__ for MySubclass
# Bases: (<class '__main__.MyClass'>,)
# {'__module__': '__main__',
#  '__qualname__': 'MySubclass',
#  'bar': <function MySubclass.bar at 0x0000019757FC0820>,
#  'other': 567}
#from noconflict import makecls
# Example 2
class ValidatePolygon(type):
    
    def __new__(meta, name, bases, class_dict):
        # Only validate subclasses of the Polygon class
        if bases:
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None  # Must be specified by subclasses

    #@classmethod #TypeError: Polygon.interior_angles() missing 1 required positional argument: 'cls'
    @classmethod
    def interior_angles(cls):#(method) def interior_angles(cls: Type[Self@Polygon]) -> Any
        return (cls.sides - 2) * 180

class Triangle(Polygon):#as first arg for class Polygon with method 
    sides = 3

class Rectangle(Polygon):
    sides = 4

class Nonagon(Polygon):
    sides = 9

assert Triangle.interior_angles() == 180
assert Rectangle.interior_angles() == 360
assert Nonagon.interior_angles() == 1260


# Example 3
try:
    print('Before class')
    
    class Line(Polygon):#test class with type change and method to deliver var with decorator
        print('Before sides')
        sides = 2
        print('After sides')
    
    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 4
class BetterPolygon:
    sides = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        super().__init_subclass__()#call parent class
        if cls.sides < 3:
            raise ValueError('Polygons need 3+ sides')

    @classmethod#method to expose var to class
    def interior_angles(cls):#get var from outer class as arg
        return (cls.sides - 2) * 180

class Hexagon(BetterPolygon):
    sides = 6

assert Hexagon.interior_angles() == 720 #->4 times 180
print(Hexagon.interior_angles())#720 ->call without creating instance of class see a= class

# Example 5
try:#ValueError: Polygons need 3+ sides
    print('Before class')
    
    class Point(BetterPolygon):#class call for parent class with var
        sides = 1
    
    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 6
class ValidateFilled(type):
    def __new__(meta, name, bases, class_dict):
        # Only validate subclasses of the Filled class
        if bases:
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('Fill color must be supported')
        return type.__new__(meta, name, bases, class_dict)

class Filled(metaclass=ValidateFilled):
    color = None  # Must be specified by subclasses



##---------------------------------
#from six import with_metaclass

# class M_C(M_A, M_B):
#     pass

# class C(with_metaclass(M_C, A, B)):
# implement your class here



# class M_A(type):
#     pass
# class M_B(type):
#     pass
# class A(object):
#     __metaclass__=M_A
# class B(object):
#     __metaclass__=M_B
# class C(A,B):
#     pass

# print(C)

#-----------------------------------
# class polygon(type):
#     pass
# class M_B(type):
#     pass
# class A(object):
#     __metaclass__=M_A
# class B(object):
#     __metaclass__=M_B
# class C(A,B):
#     pass

# print(C)



# class M_C(M_A, M_B):
#     pass

# class C(with_metaclass(M_C, A, B)):
# implement your class here




##----------------------------------
from six import with_metaclass #solves the metaclass confict type/object
# Example 7
class RedPentagon_C(ValidateFilled, ValidatePolygon):
    pass



try:
    #class RedPentagon(Filled, Polygon):
    class RedPentagon(with_metaclass(RedPentagon_C, Filled, Polygon)):

        color = 'blue'
        sides = 5
except:
    logging.exception('Expected')
else:
    assert False


try:
    #class RedPentagon(Filled, Polygon):
    class RedPentagon(ValidateFilled):#classic but part missed so use six module 

        color = 'blue'
        sides = 5
except:
    logging.exception('Expected')
else:
    assert True


# Example 8
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # Only validate non-root classes
        if not class_dict.get('is_root'):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    is_root = True
    sides = None  # Must be specified by subclasses
    
    
try:
    class RedPentagon(Polygon, Polygon):#obvious ->TypeError: duplicate base class Polygon
        color = 'blue'
        sides = 5
except:
    logging.exception('Expected')
else:
    assert False

class ValidateFilledPolygon(ValidatePolygon):
    def __new__(meta, name, bases, class_dict):
        # Only validate non-root classes
        if not class_dict.get('is_root'):
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('Fill color must be supported')
        return super().__new__(meta, name, bases, class_dict)

class FilledPolygon(Polygon, metaclass=ValidateFilledPolygon):
    is_root = True
    color = None  # Must be specified by subclasses


# Example 9
class GreenPentagon(FilledPolygon):#if only one metaclass can use dunder "new" method
    color = 'green'
    sides = 5

greenie = GreenPentagon()
assert isinstance(greenie, Polygon)


# Example 10
try:
    class OrangePentagon(FilledPolygon):
        color = 'orange'#ValueError: Fill color must be supported
        sides = 5
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
try:
    class RedLine(FilledPolygon):
        color = 'red'#ValueError: Polygons need 3+ sides
        sides = 2
except:
    logging.exception('Expected')
else:
    assert False


# Example 12
class Filled:#use subclass method to avoid metaclass conflicts
    color = None  # Must be specified by subclasses

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.color not in ('red', 'green', 'blue'):
            raise ValueError('Fills need a valid color')


# Example 13
class RedTriangle(Filled, BetterPolygon):#multiclass then use dunder subclass method
    color = 'red'
    sides = 3

ruddy = RedTriangle()
assert isinstance(ruddy, Filled)
assert isinstance(ruddy, BetterPolygon)


# Example 14
try:
    print('Before class')
    
    class BlueLine(Filled, BetterPolygon):
        color = 'blue'
        sides = 2#ValueError: Polygons need 3+ sides
    
    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 15
try:
    print('Before class')
    
    class BeigeSquare(Filled, BetterPolygon):
        color = 'beige'#ValueError: Fills need a valid color
        sides = 4
    
    print('After class')
except:
    logging.exception('Expected')
else:
    assert False


# Example 16
class Top:
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'Top for {cls}')

class Left(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'Left for {cls}')#Top for <class '__main__.Left'>

class Right(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'Right for {cls}')#Top for <class '__main__.Right'>

class Bottom(Left, Right):#Fill the stack first left -> top,right ->top, top->start printing order top-right-left
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'Bottom for {cls}')#Top for <class '__main__.Bottom'>
                                 # Right for <class '__main__.Bottom'>
                                  # Left for <class '__main__.Bottom'>
