# Ben Raivel
# CS

import numpy as np
import pandas as pd
import time
import os

class HashTable():
    '''
    open-addressed hash table
    - table length is always power of 2
    - size doubled when density > 0.5
    - uses double hash with two different auxillary hashing functions
    - keys are 20 char
    '''

    def __init__(self, init_time = None, log_folder = 'log'):
        '''
        creates an empty hash table
        pass init_time for multithreaded performace tracking
        '''
        # initial size, size must always be power of 2
        self.size = 128

        # number of unique words / total words
        self.n_unique = 0
        self.n_total = 0

        # folder to use for logging
        self.log_folder = log_folder

        # define (val, key) pair dtype keys are 20 characters
        self.val_key = np.dtype([('val', np.uint), ('key', np.unicode_, 20)])
        
        # create empty table
        self.table = np.empty(self.size, dtype=self.val_key)

        # use provided init_time if possible
        if init_time != None:
            self.init_time = init_time
        
        else: # set init time to current time
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

        # get previous val, index in table
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

        # get previous val, index in table
        prev_val, idx = self.get(key)

        # increment val by i
        self.table[idx]['val'] += i

        # if this entry is new
        if prev_val == None:
            
            # set key
            self.table[idx]['key'] = key
            
            # added new entry
            self.n_unique += 1

            # if density exceedes 50%
            if self.n_unique/self.size > 0.5:
                self.grow_table()

        # counted i words
        self.n_total += i

        if self.n_total % 100000 == 0:
            self.log()

    def grow_table(self):
        '''
        doubles the size of the table and re-inserts existing entries
        '''
        # copy old table
        old_table = self.table.copy()

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


    def combine(self, hashmap):
        '''
        absorbs all entries of hashmap into self.table (this hashmap)
        '''
        # get non-zero entries of table
        indices = np.nonzero(hashmap.table)[0]

        # for each nonzero entry
        for i in range(indices.size):

            # get val, key pair
            struct = hashmap.table[indices[i]]

            # increment key by val
            self.increment(struct['key'], struct['val'])

        self.log()

    def to_df(self):
        '''
        returns a pandas DataFrame copy of HashTable
        - empty values are dropped
        - additional column for frequency is added
        '''

        # create df from table
        df = pd.DataFrame.from_records(self.table)

        # replace empty string with None
        df = df[df.val != 0]

        # add cols: year is constant, freq in count/total
        df = df.assign(freq = lambda x: x['val']/self.n_total)

        # sort values descending
        df = df.sort_values('val', ascending = False)

        return df

    def log(self):
        '''
        logs hashtable performance stats to csv file

        file headers:
            table_size, n_unique, n_total, time
        '''
        # get path for log file based on pid
        log_path = self.log_folder + '/' + str(os.getpid()) + '_log.csv'

        # if file does not exist
        if not os.path.exists(log_path):

            file = open(log_path, 'w')
            
            # write headers
            file.write('table_size,n_unique,n_total,time\n')

        else:
            file = open(log_path, 'a')

        # compute elapsed time
        elapsed_time = time.time() - self.init_time

        # write values
        file.write('{size:d},{unique:d},{total:d},{time:.4f}\n'.format(
                    size = int(self.size), 
                    unique = int(self.n_unique), 
                    total = int(self.n_total), 
                    time = elapsed_time))

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
        MUST generate an odd number (paired with even table size this ensures self.hash() spans the table)
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
