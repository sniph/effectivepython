#!/usr/bin/env PYTHONHASHSEED=1234 python3.5

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


# Example 3
# Python 3.5
baby_names = {
    "cat": "kitten",
    "dog": "puppy",
}
# print key in a list with "list  .key"
print(list(baby_names.keys()))
# print values in a list with "list  .values"
print(list(baby_names.values()))
# print list of tuples with "list and tuple (key,value)
print(list(baby_names.items()))
# now the last goes out first
print(baby_names.popitem())  # Randomly chooses an item
