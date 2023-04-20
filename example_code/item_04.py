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
a = 0b10111011
b = 0xc5f
print('Binary is %d, hex is %d' % (a, b))


# Example 2
key = 'my_var'
value = 1.234
formatted = '%-10s = %.2f' % (key, value)
print(formatted)


# Example 3
try:
    reordered_tuple = '%-10s = %.2f' % (value, key) #cannot treat string a float
except:
    logging.exception('Expected')
else:
    assert False


# Example 4
try:
    reordered_string = '%.2f = %-10s' % (key, value) #cannot treat float as string
except:
    logging.exception('Expected')
else:
    assert False


# Example 5
pantry = [
    ('avocados', 1.25),
    ('bananas', 2.5),
    ('cherries', 15),
]
for i, (item, count) in enumerate(pantry): #generate numbering with enumerate function
    print('#%d: %-10s = %.2f' % (i, item, count))


# Example 6
for i, (item, count) in enumerate(pantry):
    print('#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count)))


# Example 7
template1 = '%s loves food. See %s cook.' #name the variable layout
name = 'Max'
formatted = template1 % (name, name) #variable holds the layout and values
print(formatted)


# Example 8
name = 'brad'
formatted = template1 % (name.title(), name.title()) #works with title method of name
print(formatted)


# Example 9
key = 'my_var'
value = 1.234

old_way = '%-10s = %.2f' % (key, value) #string template insert key/value
print(old_way)

new_way = '%(key)-10s = %(value).2f' % { #show which place key or value has
    'key': key, 'value': value}  # Original

print(new_way)

reordered = '%(key)-10s = %(value).2f' % { #place of key or value is interchangable
    'value': value, 'key': key}  # Swapped

print(reordered)

assert old_way == new_way == reordered
print(old_way , new_way , reordered)

# Example 10
name = 'Max'

template = '%s loves food. See %s cook.' #use location of string
before = template % (name, name)   # Tuple

template = '%(name)s loves food. See %(name)s cook.' #use name as variable in string
after = template % {'name': name}  # Dictionary

assert before == after
print(before ,'==', after)

# Example 11
    for i, (item, count) in  enumerate(pantry): #enumerate to loop over list assign list in order placement
        before = '#%d: %-10s = %d' % (
            i + 1,
            item.title(),
            round(count))

        after = '#%(loop)d: %(item)-10s = %(count)d' % { #assign to string as variable names
            'loop': i + 1,
            'item': item.title(),
            'count': round(count),
        }

        assert before == after
        print(before," == ",after)
#krkrkr

# Example 12
soup = 'lentil'
formatted = 'Today\'s soup is %(soup)s.' % {'soup': soup} #assign var and use in string
print(formatted)


# Example 13
menu = {
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}
template = ('Today\'s soup is %(soup)s, '
            'buy one get two %(oyster)s oysters, '
            'and our special entrée is %(special)s.')
formatted = template % menu #combine key/value pairs  with string template
print(formatted)


# Example 14
a = 1234.5678
formatted = format(a, ',.2f')
print(formatted)

b = 'my string'
formatted = format(b, '^20s')
print('*', formatted, '*') #string length 20 pos with start and end string


# Example 15
key = 'my_var'
value = 1.234

formatted = '{} = {}'.format(key, value) #get vars into placeholders '{}'
print(formatted)


# Example 16
formatted = '{:<10} = {:.2f}'.format(key, value) #placeholders with pos and type
print(formatted)


# Example 17
print('%.2f%%' % 12.5)
print('{} replaces {{}}'.format(1.23)) #use double {{}} to get {} in string


# Example 18
formatted = '{0} = {1}'.format(key, value) #assign var by nymber of postion 0,1 ..
print(formatted)


# Example 19
formatted = '{0} loves food. See {1} cook.'.format(name,key) # assign var by pos 0,1 ..
print(formatted)


# Example 20
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % ( #assign vars as ordered below
        i + 1,
        item.title(),
        round(count))

    new_style = '#{}: {:<10s} = {}'.format( #assign also as ordered with {} as placeholders
        i + 1,
        item.title(),
        round(count))
    print(old_style , new_style)
    assert old_style == new_style


# Example 21
formatted = 'First letter is {menu[oyster][0]!r}'.format( #get item key/value then first pos
    menu=menu)
print(formatted)


# Example 22
old_template = (
    'Today\'s soup is %(soup)s, '
    'buy one get two %(oyster)s oysters, '
    'and our special entrée is %(special)s.')
old_formatted = old_template % { #assign key/value pairs to vars in string
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}

new_template = (
    'Today\'s soup is {soup}, '
    'buy one get two {oyster} oysters, '
    'and our special entrée is {special}.')
new_formatted = new_template.format( #use {} as placeholder with vars assigned below
    soup='lentil',
    oyster='kumamoto',
    special='schnitzel',
)

assert old_formatted == new_formatted
print(old_formatted ,"==", new_formatted)


# Example 23
key = 'my_var'
value = 1.234

formatted = f'{key} = {value}' #get vars into string with palceholder {} and vars name
print(formatted)


# Example 24
formatted = f'{key!r:<10} = {value:.2f}' # !r places '' around var : => assigns format
print(formatted)


# Example 25
f_string = f'{key:<10} = {value:.2f}' #takes value from vars

c_tuple  = '%-10s = %.2f' % (key, value) #positional ordering vars to string

str_args = '{:<10} = {:.2f}'.format(key, value) #positional ordered in format method

str_kw   = '{key:<10} = {value:.2f}'.format(key=key, value=value) #format method combined with vars assignment

c_dict   = '%(key)-10s = %(value).2f' % {'key': key, 'value': value} #key/value pairs to vars in string

assert c_tuple == c_dict == f_string
print(c_tuple ,'==', c_dict ,'==', f_string)
assert str_args == str_kw == f_string
print(str_args ,'==', str_kw ,'==', f_string)


# Example 26
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % (#ordering and style static
        i + 1,
        item.title(),
        round(count))

    new_style = '#{}: {:<10s} = {}'.format(#ordering style static with {} as placeholder
        i + 1,
        item.title(),
        round(count))

    f_string = f'#{i+1}: {item.title():<10s} = {round(count)}' #with direct in placeholder {} style and var

    assert old_style == new_style == f_string
    print(old_style, '==', new_style, '==', f_string) #within for loop every line is printed

# Example 27
for i, (item, count) in enumerate(pantry):
    print(f'#{i+1}: ' #with f' very direct way of layout with placeholder {} style and vars inside
          f'{item.title():<10s} = '
          f'{round(count)}')


# Example 28
places = 3
number = 1.23456
print(f'My number is {number:.{places}f}') #second is float

import importlib.metadata

distributions = importlib.metadata.distributions()
for distribution in sorted(distributions, key=lambda d: d.name): #use anoymous function to set name as sort item in distributions
   print(f"{distribution.name:30} {distribution.version}") #use f' in print to get the to columns with the style
