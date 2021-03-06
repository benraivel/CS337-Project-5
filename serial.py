# Ben Raivel
# CS337 Project 5
# 10/14/22

# single-threaded implementation of word counting

import numpy as np
import time
import re

import HashTable as ht

# regex definition of a word
WRD = re.compile(r"[a-z][a-z']*")

def s_count_words(filename, table):
    '''
    counts words in file into table
    '''

    # open file
    file = open(filename, 'r')

    # loop over lines in file
    for line in file:

        # tokenize
        words = WRD.findall(line.lower())

        if words != []:

            # loop over list of words in line
            for word in words:

                # increment
                table.increment(word)



def test_1(a, b):
    '''
    '''
    table = ht.HashTable()

    print(a + '\t' + b +'\ti')
    for i in range(5):
        print(str(table.hash(a, i)) + '\t' + str(table.hash(b, i)) + '\t' + str(i))

def test_2(a, i):

    table = ht.HashTable()

    start = time.perf_counter_ns()
    
    val = table.hash(a, i)

    end = time.perf_counter_ns()

    print('Hashed \'' + a + '\' to ' + str(val) + ' in ' + str(end-start) + ' ns')

def test_3():
    table = ht.HashTable()
    
    table.insert('hello', 4)

    print(table.get('hello'))

def test_4():

    key_val = np.dtype([ ('val', np.uint), ('key', np.unicode_, 20)])

    keys = ['one', 'two', 'three', 'four', 'five', 'six']
    vals = [1,2,3,4,5,6]

    arr = np.empty(10, key_val)

    for i in range(6):
        arr[i] = (vals[i], keys[i])

    np.random.shuffle(arr)

    print(arr)


    print(np.nonzero(arr)[0])

    arr.sort()

    print(arr)

def test_5():
    file = open('rc/reddit_comments_2008.txt', 'r')

    file.readline()
    file.readline()
    
    line = file.readline()

    wrd = re.compile(r"[a-z][a-z']*")

    print(wrd.findall(line.lower()))


def main():

    files = ['rc/reddit_comments_2008.txt', 'rc/reddit_comments_2009.txt', 'rc/reddit_comments_2010.txt', 
                'rc/reddit_comments_2011.txt', 'rc/reddit_comments_2012.txt', 'rc/reddit_comments_2013.txt',
                'rc/reddit_comments_2014.txt', 'rc/reddit_comments_2015.txt']

    # create hashtable
    table = ht.HashTable()

    start = time.time()

    count_words('rc/reddit_comments_2008.txt', table)

    end = time.time()

    print(table.n_total, str(end-start))


if __name__ == '__main__':
    main()
