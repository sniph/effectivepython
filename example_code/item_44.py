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
class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms


# Example 2
r0 = OldResistor(50e3)
print('Before:', r0.get_ohms())
r0.set_ohms(10e3)
print('After: ', r0.get_ohms())


# Example 3
r0.set_ohms(r0.get_ohms() - 4e3)#10e3-4e3=6e3 make call to method and subtract from result in arg
                                #use arg as input for set method
assert r0.get_ohms() == 6e3


# Example 4
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)#init value for ohms
#r1 = Resistor()#TypeError: Resistor.__init__() missing 1 required positional argument: 'ohms'
r1.ohms = 10e3 #10000.0 ohms, 0 volts, 0 amps
print(f'{r1.ohms} ohms, '
      f'{r1.voltage} volts, '
      f'{r1.current} amps')


# Example 5
r1.ohms += 5e3 #15000.0 ohms, 0 volts, 0 amps can add to last value

print(f'{r1.ohms} ohms, '
      f'{r1.voltage} volts, '
      f'{r1.current} amps')

# Example 6
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)#need super to call parent class in arg
        self._voltage = 0

    @property#return the getter version of property decorator
    def voltage(self):
        return self._voltage

    @voltage.setter#is the setter version of property decorator
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


# Example 7
r2 = VoltageResistance(1e3)
print(f'Before: {r2.current:.2f} amps')#0/1000 ->0
print(r2.ohms #set to 1e3 in int of r2 0/1000 ->0
r2.voltage = 10
print(f'After:  {r2.current:.2f} amps')#10/1000->0.01
print(r2.ohms)


# Example 8
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'ohms must be > 0; got {ohms}')#raise error through setter method of property decorator
        self._ohms = ohms


# Example 9
try:
    r3 = BoundedResistance(1e3)
    r3.ohms = 0 #ValueError: ohms must be > 0; got 0
except:
    logging.exception('Expected')
else:
    assert False

print(r3.ohms)

# Example 10
try:
    BoundedResistance(-5) #ValueError: ohms must be > 0; got -5
except:
    logging.exception('Expected')
else:
    assert False


# Example 11
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):#cannot set var ohms raise error with if hasattr method
        if hasattr(self, '_ohms'):
            raise AttributeError("Ohms is immutable")
        self._ohms = ohms


# Example 12
try:
    r4 = FixedResistance(1e3)
    r4.ohms = 2e3
except:
    logging.exception('Expected')
else:
    assert False
print(r4.ohms)#still 1000 not changed

# Example 13
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms


# Example 14

r7 = MysteriousResistor(10)#init with value
r7.current = 0.01
print(f'Before: {r7.voltage:.2f}')#Before: 0.00
r7.ohms#only call on setter assigns value 10(arg) to vars
print(r7.ohms)
print(f'After:  {r7.voltage:.2f}')#After:  0.10
