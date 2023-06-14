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
class LazyRecord:#get and set with init as key/value
    def __init__(self):
        self.exists = 5#init var with value

    def __getattr__(self, name):
        value = f'Value for {name}'
        setattr(self, name, value)
        return value


# Example 2
data = LazyRecord()
print('Before:', data.__dict__)
data.foo = 6#if key value construct then add to dict
print('After: ', data.__dict__)
print('foo1:   ', data.foo1)#if only key take default value with setattr method
print('After: ', data.__dict__)

# Example 3
class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f'* Called __getattr__({name!r}), '
              f'populating instance dictionary')
        result = super().__getattr__(name)
        print(f'* Returning {result!r}')
        return result

data = LoggingLazyRecord()
print('exists:     ', data.exists)
print('First foo:  ', data.foo)#* Called __getattr__('foo'), populating instance dictionary
print('Second foo: ', data.foo)#checks the dict at every call 
print('After: ', data.__dict__)#After:  {'exists': 5, 'foo': 'Value for foo'}
                                #

# Example 4
class ValidatingRecord:
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        try:
            value = super().__getattribute__(name)#test for attribute if not error and assign of value
                                                    #second call attribute found
            #value = __getattribute__(name)#"__getattribute__" is not defined
            print(f'* Found {name!r}, returning {value!r}')
            return value
        except AttributeError:
            value = f'Value for {name}'
            print(f'* Setting {name!r} to {value!r}')
            setattr(self, name, value)
            return value

data = ValidatingRecord()
print('exists:     ', data.exists)
print('First foo:  ', data.foo)
print('Second foo: ', data.foo)


# Example 5
try:
    class MissingPropertyRecord:
        def __getattr__(self, name):
            if name == 'bad_name':
                raise AttributeError(f'{name} is missing')
            value = f'Value for {name}'
            setattr(self, name, value)
            return value
    
    data = MissingPropertyRecord()
    assert data.foo == 'Value for foo'  # Test this works
    data.bad_name#raises error -> AttributeError: bad_name is missing
except:
    logging.exception('Expected')
else:
    assert False


# Example 6
data = LoggingLazyRecord()  # Implements __getattr__ class with class approach through fill up dict
print('Before:         ', data.__dict__)
print('Has first foo:  ', hasattr(data, 'foo'))
print('After:          ', data.__dict__)
print('Has second foo: ', hasattr(data, 'foo'))


# Example 7
data = ValidatingRecord()  # Implements __getattribute__ class by using attribute error to fill up with get/set atribute
                            #sort of key/value construct
print('Has first foo:  ', hasattr(data, 'foo'))
print('Has second foo: ', hasattr(data, 'foo'))


# Example 8
class SavingRecord:
    def __setattr__(self, name, value):
        # Save some data for the record
        pass
        super().__setattr__(name, value)


# Example 9
class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f'* Called __setattr__({name!r}, {value!r})')
        super().__setattr__(name, value)

data = LoggingSavingRecord()#init new class instance
print('Before: ', data.__dict__)#Before:  {} sets dict to empty
data.foo = 5
print('After:  ', data.__dict__)#* Called __setattr__('foo', 5) -> After:   {'foo': 5} 
data.foo = 7
print('Finally:', data.__dict__)#* Called __setattr__('foo', 7) ->Finally: {'foo': 7} here overwrite foo
data.foo1 = 8
print('Finally1:', data.__dict__)#* Called __setattr__('foo1', 8) ->Finally1: {'foo': 7, 'foo1': 8}

# Example 10
class BrokenDictionaryRecord:#RecursionError: maximum recursion depth exceeded while calling a Python object
    def __init__(self, data):
        self._data = {}

    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        return self._data[name]


# Example 11
try:
    data = BrokenDictionaryRecord({'foo': 3})
    data.foo
except:
    logging.exception('Expected')
else:
    assert False


# Example 12
class DictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):#(method) def __getattribute__(self: Self@DictionaryRecord,name: Any) -> (Type[DictionaryRecord] | Any)
        # Prevent weird interactions with isinstance() used
        # by example code harness.
        print(name)
        if name == '__class__':
            return DictionaryRecord
        print(f'* Called __getattribute__({name!r})')
        data_dict = super().__getattribute__('_data')#Return getattr(self, name)
        #data_dict = __getattribute__('_data') ->"__getattribute__" is not defined
        return data_dict[name]

data = DictionaryRecord({'foo': 3,'foo1':5})#only data from DictionaryRecord returned
print('foo: ', data.foo)
print('foo1: ', data.foo1)#* Called __getattribute__('foo1') ->foo1:  5
