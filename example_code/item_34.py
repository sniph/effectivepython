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
import math

# divide 2pi*r in steps and accumulate to full
def wave(amplitude, steps):#set sevral vars output as generator object
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output


# Example 2


def transmit(output):#styling input
    if output is None:
        print(f"Output is None")
    else:
        print(f"Output: {output:>5.1f}")


def run(it):#loops over generator object func use func for styling output
    for output in it:
        transmit(output)


# "run" function as decorator function for "wave" function
# "transmit" function takes "wave" items to print
run(wave(3.0, 8))#decorator approach classic


# Example 3
# first call next(1) assign 1 to "output" variable
def my_generator():#create generator with yield value command
    received = yield 1
    print(f"received = {received}")


it = my_generator()#assign generator object to var
output = next(it)  # Get first generator output every next is a call of the yield method in func so always a value is returned eq 1
print(f"output = {output}") #output still 1 just one next

# run above code first then below twice
# second call to next(it) assign None to "r eceived" variable
# third "assert false"
try:
    next(it)  # Run generator until it exits Traceback (most recent call last):
    #File "<stdin>", line 1, in <moduleStopIteration
except StopIteration:
    pass
else:
    assert False

output = next(it)  # Get first generator output every next is a call of the yield method in func so always a value is returned eq 1
print(f"output = {output}")

# Example 4
it = my_generator()
output = it.send(None)  # Get first generator output
print(f"output = {output}")
# call of "list" method on it generator returns with send method "None" for "received" variable
# b =list(it)
# print(b)

# call of it generator with "send" method returns "hello" for "received" variable
try:
    it.send("hello!")  # Send value into the generator 
    #need to send None first then other text is possible
    #TypeError: can't send non-None value to a just-started generator
except StopIteration:
    pass
else:
    assert False

a = list(it)
print(a)


# Example 5
def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield  # Receive initial amplitude yield takes over value amplitude left to right
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output  # Receive next amplitude output is assigned to var amplitude every send


# Example 6
# if amplitudes then to "output" variable  assigned with yield output
# to "amplitude"  
def run_modulating(it):
    amplitudes = [None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]#first item needs to be None for send method
    for amplitude in amplitudes:
        output = it.send(amplitude)#send is comparable to next method
        transmit(output)


# "run_modulating" as decorator for "wave_modulating" function
run_modulating(wave_modulating(12))


#extra example send
def double_number(number):
    while True:
        number *=2
        number = yield number

c = double_number(4)
print(c)
c.send(4)#TypeError: can't send non-None value to a just-started generator
        #generator must be started to accepted values therefore first None to start generator

c.send(None)
c.send(4)
c.send(5)



# Example 7
# direct approch with "yield from" with differnt amplitudes
def complex_wave():#use wave func with vars call 3 times anew
    yield from wave(7.0, 3)
    yield from wave(2.0, 4)
    yield from wave(10.0, 5)


def run(it):#use func as input
    for output in it:
        transmit(output)#get the output parsed


run(complex_wave())#classis else use decorators


# Example 8
# try the "yiled from" approch on combine yield/send method
# start every time with outpuy: None
def complex_wave_modulating():#call func with different args and direct yield from faster then double yield
    yield from wave_modulating(3)
    yield from wave_modulating(4)
    yield from wave_modulating(5)


run_modulating(complex_wave_modulating())#classic else as decorator func after func f(g()) type


# Example 9
def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it)  # Get next input
        output = amplitude * fraction
        yield output


# Example 10
def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)


# Example 11
# take the loop over "next" method approch, make generator from "it" variable by iter method on "amplitudes" list
def run_cascading():#can be called without arg because settled in func
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))#create a generator of iterator from list
    for amplitude in amplitudes:
        output = next(it)#call next in generator
        transmit(output)


run_cascading()#notice script without use of send to make it simpeler to read
