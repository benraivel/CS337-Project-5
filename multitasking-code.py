# Ben Raivel

import HashTable as ht
import multiprocessing
import re
import time


WRD = re.compile(r"[a-z][a-z']*")

def tokenize(line):
    
    tokens = []

    words = WRD.findall(line.lower())

    if words != []:

        # loop over list of words in line
        for word in words:

            tokens.append(word)

    return tokens

def count(block):

    table = ht.HashTable()

    for line in block:

        words = WRD.findall(line.lower())

        if words != []:

            # loop over list of words in line
            for word in words:

                table.increment(word)

    return table

def gen_block(file, n_lines = 100000):
    
    block = []

    for i, line in enumerate(file):
        if i % n_lines == 0:
            yield block
            block = []
        block.append(line)
    yield line


def main():

    # open file
    file = open('rc/reddit_comments_2008.txt', 'r')

    blocks = gen_block(file)

    table = ht.HashTable()

    #p_tokenizer = multiprocessing.Process(target = count_line, args = (filename, wrd, queue))
    pool = multiprocessing.Pool()

    tables = pool.imap(count, blocks)

    for table in tables:
        
        print(table.get('the'))

    




if __name__ == '__main__':

    start = time.time()
    main()
    end = time.time()

    print(end-start)


    