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
class Field:
    def __init__(self, name):#init vars + get/set construct as dunder methods
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# Example 2
class Customer:#init set method of class
    # Class attributes
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


# Example 3
cust = Customer() 
print(f'Before: {cust.first_name!r} {cust.__dict__}')#Before: '' {} empty dict
cust.first_name = 'Euclid'
print(f'After:  {cust.first_name!r} {cust.__dict__}')#After:  'Euclid' {'_first_name': 'Euclid'} assign key/value to dict with dunder dict method


# Example 4
class Customer:
    # Left side is redundant with right side
    first_name = Field('first_name')#var same as instance names
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


# Example 5
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():#fill the default dict by a loop 
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls


# Example 6
class DatabaseRow(metaclass=Meta):#init meta class
    pass


# Example 7
class Field:
    def __init__(self):
        # These will be assigned by the metaclass.
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):#set values assigned by meta class and use of instance
        setattr(instance, self.internal_name, value)


# Example 8
class BetterCustomer(DatabaseRow):#no redudant var names and arg names
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


# Example 9
cust = BetterCustomer()#init class
print(f'Before: {cust.first_name!r} {cust.__dict__}')#Before: '' {}
cust.first_name = 'Euler'
print(f'After:  {cust.first_name!r} {cust.__dict__}')#After:  'Euler' {'_first_name': 'Euler'}


# Example 10
try:
    class BrokenCustomer:#no call for parsing classes
        first_name = Field()
        last_name = Field()
        prefix = Field()
        suffix = Field()
    
    cust = BrokenCustomer()
    cust.first_name = 'Mersenne'#TypeError: attribute name must be string, not 'NoneType
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
class Field:
    def __init__(self):#init vars
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):#connect instance with var dunder method all in one class als parsing var
        # Called on class creation for each descriptor
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


# Example 12
class FixedCustomer:#call without redundend var name and arg name
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

cust = FixedCustomer()
print(f'Before: {cust.first_name!r} {cust.__dict__}')#Before: '' {}
cust.first_name = 'Mersenne'
print(f'After:  {cust.first_name!r} {cust.__dict__}')#After:  'Mersenne' {'_first_name': 'Mersenne'}
