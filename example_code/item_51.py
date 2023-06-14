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
from functools import wraps

def trace_func(func):
    if hasattr(func, 'tracing'):  # Only decorate once
        return func

    @wraps(func)#decorator to keep info of wrapped function at call .name etc.
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f'{func.__name__}({args!r}, {kwargs!r}) -> '
                  f'{result!r}')

    wrapper.tracing = True
    return wrapper


# Example 2
class TraceDict(dict):
    @trace_func
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, *args, **kwargs):
        return super().__setitem__(*args, **kwargs)

    @trace_func
    def __getitem__(self, *args, **kwargs):
        return super().__getitem__(*args, **kwargs)


# Example 3
trace_dict = TraceDict()#invokes init with empty dict-> __init__(({},), {}) -> None -> tuple and dict enclosed with ()
trace_dict = TraceDict([('hi', 1)])#invokes init method -> __init__(({'hi': 1}, [('hi', 1)]), {}) -> None no kwargst ->{}
                                                                #create arg as dict as part of tuple in rpr method

trace_dict['there'] = 2 #invokes set method -> __setitem__(({'hi': 1, 'there': 2}, 'there', 2), {}) -> None
trace_dict['hi']#ivokes get method -> __getitem__(({'hi': 1, 'there': 2}, 'hi'), {}) -> 1
try:
    trace_dict['does not exist']#__getitem__(({}, 'does not exist'), {}) -> KeyError('does not exist') if key not found then empty {} and error as result
except KeyError:
    pass  # Expected
else:
    assert False


# Example 4
import types

trace_types = (#var as tuple of types
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType)

class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)#call to result class with rpr method as return
            if isinstance(value, trace_types):#only with set call to type class
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass


# Example 5
class TraceDict(dict, metaclass=TraceMeta):
    pass
trace_dict = TraceDict()#__new__((<class '__main__.TraceDict'>,), {}) -> {} returns new method attributes also instance of type style empty {} for key/value
trace_dict = TraceDict([('hi', 1)])#__new__((<class '__main__.TraceDict'>, [('hi', 1)]), {}) -> {} added call to wrapper and rpr style class
trace_dict['there'] = 2#set object 
trace_dict['hi']#__getitem__(({'hi': 1, 'there': 2}, 'hi'), {}) -> 1 return without extended type info
try:
    trace_dict['does not exist']#return without type info with raise of error
                        #__getitem__(({'hi': 1, 'there': 2}, 'does not exist'), {}) -> KeyError('does not exist')
except KeyError:
    pass  # Expected
else:
    assert False


# Example 6
try:
    class OtherMeta(type):
        pass
    
    class SimpleDict(dict, metaclass=OtherMeta):
        pass
    
    class TraceDict(SimpleDict, metaclass=TraceMeta):
        pass
except:
    logging.exception('Expected')
else:
    assert False
#-----------------------------------------------------
try:
    class OtherMeta(type):
        pass
    
except:
    logging.exception('Expected')
else:
    assert False#AssertionError so this would work
    
#--------------------------------------------
try:

    
    #class SimpleDict(dict, metaclass=OtherMeta):
    class SimpleDict(dict, metaclass=TraceMeta):
        pass
    

except:
    logging.exception('Expected')
else:
    assert False #this would work AssertionError   
#--------------------------------------
try:

    
    #class TraceDict(SimpleDict, metaclass=TraceMeta):
    class TraceDict(SimpleDict, metaclass=TraceMeta):
        pass
except:
    logging.exception('Expected')
else:
    assert False# this would work AssertionError
   
# Example 7
class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = type.__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass

class OtherMeta(TraceMeta):
    pass

class SimpleDict(dict, metaclass=OtherMeta):
    pass

#class TraceDict(Dict, metaclass=TraceMeta):#NameError: name 'Dict' is not defined. Did you mean: 'dict'? Dict already definded as arg
    #pass

class TraceDict(SimpleDict, metaclass=TraceMeta):#__init_subclass__((), {}) -> None reference to class with Dict in arg
    pass

trace_dict = TraceDict([('hi', 1)])#__new__((<class '__main__.TraceDict'>, [('hi', 1)]), {}) -> {}
trace_dict['there'] = 2
trace_dict['hi']#__getitem__(({'hi': 1, 'there': 2}, 'hi'), {}) -> 1
try:
    trace_dict['does not exist']#__getitem__(({'hi': 1, 'there': 2}, 'does not exist'), {}) -> KeyError('does not exist')
except KeyError:
    pass  # Expected
else:
    assert False




# Example 8
def my_class_decorator(klass):
    klass.extra_param = 'hello'
    return klass

@my_class_decorator
class MyClass:
    pass

print(MyClass)
print(MyClass.extra_param)


# Example 9
def trace(klass):#trace will be decorator for init of classes for adding types
    for key in dir(klass):
        value = getattr(klass, key)
        if isinstance(value, trace_types):
            wrapped = trace_func(value)
            setattr(klass, key, wrapped)
    return klass


# Example 10
@trace
class TraceDict(dict):#metaclass type incured through decorator
    pass

trace_dict = TraceDict([('hi', 1)])#__new__((<class '__main__.TraceDict'>, [('hi', 1)]), {}) -> {}
trace_dict['there'] = 2
trace_dict['hi']#__getitem__(({'hi': 1, 'there': 2}, 'hi'), {}) -> 1
try:
    trace_dict['does not exist']#__getitem__(({'hi': 1, 'there': 2}, 'does not exist'), {}) -> KeyError('does not exist')
except KeyError:
    pass  # Expected
else:
    assert False


# Example 11
class OtherMeta(type):
    pass

@trace
class TraceDict(dict, metaclass=OtherMeta):#added type only pass else trace type
    pass

trace_dict = TraceDict([('hi', 1)])#__new__((<class '__main__.TraceDict'>, [('hi', 1)]), {}) -> {}
trace_dict['there'] = 2
trace_dict['hi']#__getitem__(({'hi': 1, 'there': 2}, 'hi'), {}) -> 1
try:
    trace_dict['does not exist']#__getitem__(({'hi': 1, 'there': 2}, 'does not exist'), {}) -> KeyError('does not exist')
except KeyError:
    pass  # Expected
else:
    assert False
