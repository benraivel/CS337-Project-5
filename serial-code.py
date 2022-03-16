# Ben Raivel
# CS337 Project 5
# 10/14/22

# single-threaded implementation of word counting

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

        # define (key, val) pair dtype
        self.key_val = np.dtype([('key', np.unicode_, self.key_nchar), ('val', np.uint)])
        
        # create empty table
        self.table = np.empty(self.size, dtype=self.key_val)

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
        self.table = np.empty(self.size, dtype=self.key_val)


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


def count_words(filename, table):

    # open file
    file = open(filename, 'r')

    # regex definition of a word
    wrd = re.compile(r"[a-z][a-z']*")

    # loop over lines in file
    for line in file:

        words = wrd.findall(line.lower())

        if words != []:

            # loop over list of words in line
            for word in words:

                # increment
                table.increment(word)
    


def test_1(a, b):
    '''
    '''
    table = HashTable()

    print(a + '\t' + b +'\ti')
    for i in range(5):
        print(str(table.hash(a, i)) + '\t' + str(table.hash(b, i)) + '\t' + str(i))

def test_2(a, i):

    table = HashTable()

    start = time.perf_counter_ns()
    
    val = table.hash(a, i)

    end = time.perf_counter_ns()

    print('Hashed \'' + a + '\' to ' + str(val) + ' in ' + str(end-start) + ' ns')

def test_3():
    table = HashTable()
    
    table.insert('hello', 4)

    print(table.get('hello'))

def test_5():
    file = open('rc/reddit_comments_2008.txt', 'r')

    file.readline()
    file.readline()
    
    line = file.readline()

    wrd = re.compile(r"[a-z][a-z']*")

    print(wrd.findall(line.lower()))


def main():

    table = HashTable()

    count_words('rc/reddit_comments_2008.txt', table)

    print(table.get('the'))


if __name__ == '__main__':
    main()