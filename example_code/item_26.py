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
# function on other function to change outcome func=trace(func) same as @trace
# before function call
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r}, {kwargs!r}) " f"-> {result!r}")
        return result

    return wrapper


# Example 2
# here fibonacci = trace(fibonacci) is called argument can be function
@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


print(fibonacci(3))

# Example 3
# wrapper around function fibonacci = trace(fibonacci)
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


fibonacci = trace(fibonacci)
print(fibonacci)


# Example 4
fibonacci(4)


# Example 5
# only info of wrapper not original function
# <function trace.<locals>.wrapper at 0x000001D50ABD20E0>
print(fibonacci)

# Example 6
help(fibonacci)
# missing help info of fibonacci function only wrapper
# Help on function wrapper in module __main__:
# wrapper(*args, **kwargs)


# Example 7
# pickle needs meta info from fibonacci function get info wrapper
# AttributeError: Can't pickle local object 'trace.<locals>.wrapper'
try:
    import pickle

    pickle.dumps(fibonacci)
except:
    logging.exception("Expected")
else:
    assert False


# Example 8
# use waps to assign correct in to help function about wrapped function by wrapper Trace
from functools import wraps


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r}, {kwargs!r}) " f"-> {result!r}")
        return result

    return wrapper


# call for trace before fibonacci function no with wraps function call
@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


# with @wraps in wrapper function trace meta info is available
try:
    import pickle

    pickle.dumps(fibonacci)
except:
    logging.exception("Expected")
else:
    assert True


# Example 9
# correct info in help about wrapped function fibonacci
help(fibonacci)
# Help on function fibonacci in module __main__:

# fibonacci(n)
#    Return the n-th Fibonacci number

# Example 10
# pickle can now access info about fibonacci
print(pickle.dumps(fibonacci))
