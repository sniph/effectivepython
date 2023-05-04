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

votes = {#create dict by stucture str:value pair
    "otter": 1281,
    "polar bear": 587,
    "fox": 863,
}

print(votes)#returns dict as default by structure
print(votes.items())
print(votes.values())

# names = list(votes.keys())
names = list(votes)#places the keys in a list
print(names)
names.sort(key=votes.get, reverse=True)#sort on values reverse
print(names)


def populate_ranks(votes, ranks):
    # only key are seleted and sorted
    names = list(votes.keys())#place names of key/value in list
    
    # sort names on values(reverse) of the keys(names)
    names.sort(key=votes.get, reverse=True) #sort votes on value level
    for i, name in enumerate(names, 1):#numbering start with 1
        ranks[name] = i #create key/value pair with name/numbering => str = 1 -> str:1

ranks = {}
print(populate_ranks(votes, ranks))
print(ranks)


def get_winner(ranks):
    # return next(iter(ranks))
    return iter(ranks)


ranks = {}
populate_ranks(votes, ranks)
print(ranks)
next(iter(ranks))
next(iter(ranks))
winner = get_winner(ranks)
# with next in the function it gives the first item eve
# rytime
print(winner)#prints the object winner
# with next outside function you'll get the next rank
print(next(winner))#next walks the keys with iter

# Example 17
# Check types in this file with: python -m mypy <path>

from typing import Dict, MutableMapping


def populate_ranks(votes: Dict[str, int], ranks: Dict[str, int]) -> None:
    names = list(votes.keys())#create a list with the keys
    names.sort(key=votes.get, reverse=True)#sort on value of the keys
    for i, name in enumerate(names, 1):#number the keys
        ranks[name] = i#create dict by structure


def get_winner(ranks: Dict[str, int]) -> str:#set type of ranks and output type
    return next(iter(ranks))#return next key in dict on every call


from typing import Iterator, MutableMapping


class SortedDict(MutableMapping[str, int]):
    def __init__(self) -> None:
        self.data: Dict[str, int] = {}

    def __getitem__(self, key: str) -> int:#get value for key
        return self.data[key]

    def __setitem__(self, key: str, value: int) -> None:#set data dict items key/value pairs
        self.data[key] = value

    def __delitem__(self, key: str) -> None:#delete item in data dict on key
        del self.data[key]

    def __iter__(self) -> Iterator[str]:
        keys = list(self.data.keys())#create list of keys from data dict
        #keys.sort()#Wrong !! sort list makes the list be sorted on keys already ordered by value
        for key in keys:#produce next on list with yield at call
            yield key

    def __len__(self) -> int:#return length of data dict
        return len(self.data)


votes = {
    "otter": 1281,
    "polar bear": 587,
    "fox": 863,
}

sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
#print(ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)
