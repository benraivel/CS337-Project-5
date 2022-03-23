# Ben Raivel

import HashTable as ht
import multiprocessing
import re
import time

WRD = re.compile(r"[a-z][a-z']*")

def m_count_words(block):
    '''
    generate and return hashtable for block of lines
    '''

    # create hashtable
    table = ht.HashTable()

    # loop over lines in block
    for line in block:

        # tokenize into list
        words = WRD.findall(line.lower())

        # if list is non-empty
        if words != []:

            # loop over words
            for word in words:

                # count the word into the table
                table.increment(word)

    return table

def gen_block(file, n_lines = 100000):
    '''
    generator that turns file into multi-line (block) iterator 
    '''
    # list to hold lines
    block = []

    # enumerate makes file indexed by line
    for index, line in enumerate(file):

        # if file has reached it's nth line
        if index % n_lines == 0:

            # yield the list of n lines
            yield block

            # reset list to be empty
            block = []

        # otherwise add the current line to the block
        block.append(line)

    # yield the last list
    yield block


def main():

    # open file
    file = open('rc/reddit_comments_2008.txt', 'r')

    # create main hashtable
    table = ht.HashTable()

    # create block generator
    blocks = gen_block(file)

    # create a pool
    pool = multiprocessing.Pool()

    # non-blocking map of count function to block iterator
    sub_tables = pool.imap(m_count_words, blocks)

    # for each table returned by pool
    for t in sub_tables:

        # combine with the main table
        table.combine(t)

    #print(table.get('the'))


if __name__ == '__main__':

    start = time.time()
    main()
    end = time.time()

    print(end-start)
