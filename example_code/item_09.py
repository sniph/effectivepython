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
# range(3) => items 0,1,2 zo 3 elements
for i in range(3):#range 0,1,2 <3 end for loop then else block
    print("Loop", i)
# stops with else block
else:
    print("Else block!")


# Example 2
for i in range(3):
    print("Loop", i)
    # stops the for loop at i =1
    # then break out of loop no else block
    if i == 1:#break out of for loop with if then no else block
        break
else:
    print("Else block!")


# Example 3
for x in []:#empty list direct else block
    print("Never runs")
# only else bock for doesn't iterate over empty list
else:
    print("For Else block!")

for x in [1]:#non-emptt list runs for loop then else block
    print("Never runs")
# only else bock for doesn't iterate over empty list
else:
    print("For Else block!")


# Example 4
while False:#doesn't run only else block
    print("Never runs")
# first while block doesn't run else
# block does
else:
    print("While Else block!")

#while True:#endless loop
    print("Never runs")
# first while block doesn't run else
# block does
else:
    print("While Else block!")


# Example 5
a = 4
b = 9

for i in range(2, min(a, b) + 1):
    # range is 2,3,4
    print("Testing", i)
    # test both number on divison by i
    # close with else block
    if a % i == 0 and b % i == 0:#if both numbers have a divisor next to int 1 then no coprime
        print("Not coprime")#breaks with not coprime no else block
        break
else:
    print("Coprime")


# Example 6
def coprime(a, b):
    # test divison of a,b by i mod 0 with helper function
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False #returns string False => no coprime
    return True #if for loop fails then return string True so coprime no other divisor next to 1


assert coprime(4, 9)
assert not coprime(3, 6)
print(coprime(4, 9)) #=> True coprime
print(coprime(3, 6))#=> False not coprime

# Example 7
def coprime_alternate(a, b):
    is_coprime = True #initial coprime True
    # initial True check for for false check in function
    # else initial still true
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False #if not comprime False
            break
    return is_coprime


assert coprime_alternate(4, 9)
assert not coprime_alternate(3, 6) #use of negate in unit test
print(coprime_alternate(4, 9))
print(coprime_alternate(3, 6))
