# Ben Raivel


import numpy as np
import time
import re


class HashTable():
    '''
    open-addressed hash table
    '''

    def __init__(self):
        '''
        create an empty hash table
        '''
        # initial size, must be power of 2
        self.size = 128
        self.n_entries = 0

        # keys are 20 characters
        # according to a website 99.9% of english words are <20 char
        self.key_nchar = 20

        # define (val, key) pair dtype
        self.val_key = np.dtype([('val', np.uint), ('key', np.unicode_, self.key_nchar)])
        
        # create empty table
        self.table = np.empty(self.size, dtype=self.val_key)

    def get(self, key):
        '''
        if key in table:
            returns (val, index) 
        if not:
            returns (None, index)
        '''
        # loop count variable
        i = 0

        # loop until return
        while True:

            # compute ith hash value
            index = self.hash(key, i)

            # get the struct indicated by hash
            struct = self.table[index]
            
            # get ith key
            key_i = struct['key']

            # empty string signifies uninitialized entry
            if key_i == '':
                return None, index # key not in table

            # if ith key matches
            elif key_i == key:
                return struct['val'], index # key found!

            i+=1 # increment

    def insert(self, key, val):
        '''
        insert val at key
        '''
        # trim any key longer than 20 char
        if len(key) > 20:
            key = key[:20]

        # get val
        prev_val, idx = self.get(key)

        # set key and val
        self.table[idx]['key'] = key
        self.table[idx]['val'] = val

        # if this entry is new
        if prev_val == None:

            # increment n_entries
            self.n_entries += 1

            # if density exceedes 50%
            if self.n_entries/self.size > 0.5:

                self.grow_table()

    def increment(self, key, i=1):
        '''
        increment val at key by i
        if no entry for key exists, create one with val = i
        '''
        # trim any key longer than 20 char
        if len(key) > 20:
            key = key[:20]

        # get val
        prev_val, idx = self.get(key)

        # increment val
        self.table[idx]['val'] += i

        # if this entry is new
        if prev_val == None:
            
            # set key
            self.table[idx]['key'] = key

            self.n_entries += 1

            # if density exceedes 50%
            if self.n_entries/self.size > 0.5:

                self.grow_table()

    def grow_table(self):
        '''
        doubles the size of the table and copies existing entries
        '''
        # copy old table
        old_table = self.table.copy()

        print('size: ' + str(self.size) + '\tthe = ' + str(self.get('the')[0]))

        # double size
        self.size *= 2

        # create new table
        self.table = np.empty(self.size, dtype=self.val_key)


        # loop over old table
        for i in range(old_table.size):

            # if an entry is non-empty
            if old_table[i]['key'] != '':
                
                # insert into new table
                self.insert(old_table[i]['key'], old_table[i]['val'])

    def __aux_hash_1(self, str):
        '''
        1st auxilary hashing function
        '''
        hash = 0
        for i in range(len(str)):
            hash += ord(str[-(i+1)])*(128**i)

        return hash % self.size

    def __aux_hash_2(self, str):
        '''
        2nd auxilary hashing function
        MUST generate an odd number
        '''
        hash = 0
        for i in range(len(str)):
            hash += ord(str[i])*(64**i)

        return (2*hash + 1) % self.size

    def hash(self, str, i):
        '''
        returns double hashed index corresponding to str
        '''
        return (self.__aux_hash_1(str) + (i+1)*self.__aux_hash_2(str)) % self.size
