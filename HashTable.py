# Ben Raivel


import numpy as np
import time
import re
import os


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

        # number of unique words
        self.n_unique = 0

        # total number counted
        self.n_total = 0

        # keys are 20 characters
        # according to a website 99.9% of english words are <20 char
        self.key_nchar = 20

        # define (val, key) pair dtype
        self.val_key = np.dtype([('val', np.uint), ('key', np.unicode_, self.key_nchar)])
        
        # create empty table
        self.table = np.empty(self.size, dtype=self.val_key)

        # set init time
        self.init_time = time.time()

    def get(self, key):
        '''
        if key in table:
            returns (val, index) 
        else:
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

            # new unique entry
            self.n_unique += 1

            # if density exceedes 50%
            if self.n_unique/self.size > 0.5:

                self.grow_table()

        # counted word
        self.n_total += 1

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

            self.n_unique += 1

            # if density exceedes 50%
            if self.n_unique/self.size > 0.5:

                self.grow_table()

        # counted word
        self.n_total += 1

    def grow_table(self):
        '''
        doubles the size of the table and copies existing entries
        '''
        # copy old table
        old_table = self.table.copy()

        # double size
        self.size *= 2

        runtime = time.time() - self.init_time

        #print('pid: %d\tsize: %d\ttime: %.2f' % (os.getpid(), self.size, time.time() - self.init_time))
        print('%d, %d, %d, %.4f' % (os.getpid(), self.size, self.n_total, runtime))

        # create new table
        self.table = np.empty(self.size, dtype=self.val_key)

        # loop over old table
        for i in range(old_table.size):

            # if an entry is non-empty
            if old_table[i]['key'] != '':
                
                # insert into new table
                self.insert(old_table[i]['key'], old_table[i]['val'])

    def combine(self, hashmap):
        '''
        absorbs hashmap into self.table
        '''
        # get non-zero entries of table
        indices = np.nonzero(hashmap.table)[0]

        # for each nonzero entry
        for i in range(indices.size):

            # get val, key pair
            struct = hashmap.table[indices[i]]

            # increment key by val
            self.increment(struct['key'], struct['val'])
        
        runtime = time.time() - self.init_time

        print('%d, %d, %d, %.4f' % (os.getpid(), self.size, self.n_total, runtime))

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
