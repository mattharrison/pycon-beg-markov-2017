"""
This is a docstring. Here is an example
of running a Markov prediction:

>>> m = Markov('ab')
>>> m.predict('a')
'b'

>>> m.predict('c')
Traceback (most recent call last):
  ...
KeyError

>>> get_table('ab')
{'a': {'b': 1}}

>>> random.seed(42)
>>> m = Markov('Find a city, find yourself a city to live in', 4)
>>> test_predict(m, 20, 'F', 4)
'Find a city, find a c'

>>> with open('ts.txt', encoding='windows_1252') as fin:
...     data = fin.read()
>>> m2 = Markov(data, 4)
>>> test_predict(m2, 100, 'T', 4)
"""


import argparse
import random
import sys


class Markov:
   
    def __init__(self, data, size=1):
        self.tables = []
        for i in range(size):
            self.tables.append(get_table(data, i+1))
        #self.table = get_table(data)
        
    def predict(self, data_in):
        table = self.tables[len(data_in) - 1]
        options = table.get(data_in, {})
        if not options:
            raise KeyError()
        possible = ''
        for result, count in options.items():
            possible += result*count
        result = random.choice(possible)
        return result

    
def get_table(line, numchars=1):
    
    results = {}
    for i, char in enumerate(line):
        #print(i, char)
        chars = line[i:i+numchars]
        try:  # if i == len(line): # Look before you leap
            out = line[i+numchars]
        except IndexError:
            # easier to ask for forgiveness than permission
            break
        char_dict = results.setdefault(chars, {})
        char_dict.setdefault(out, 0)
        char_dict[out] += 1
        results[char] = char_dict
    return results

def test_predict(m, num_chars, start, size=1):
    res = [start]
    for i in range(num_chars):
        let = m.predict(start)
        res.append(let)
        start = ''.join(res)[-size:]
    return ''.join(res)

def repl(m, size=1):
    """
    This starts a repl, provide a Markov and
    optional size
    """
    while 1:
        txt = input(">")
        try:
            res = m.predict(txt[-size:])
        except KeyError:
            print("Try again...")
        print(res)

def main(args):
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--file', help='Input file')
    p.add_argument('--encoding', help='File encoding default(utf8)',
                   default='utf8')
    p.add_argument('-s', '--size', help='Size of input default(1)',
                   default=1, type=int)
    p.add_argument('-t', '--test', help='run tests', action='store_true')

    opts = p.parse_args(args)
    if opts.file:
        with open(opts.file, encoding=opts.encoding) as fin:
            data = fin.read()
        m = Markov(data, opts.size)
        repl(m)
    if opts.test:
        import doctest
        doctest.testmod()
    

if __name__ == '__main__':
    print("EXECUTED")
    #import doctest
    #doctest.testmod()
    main(sys.argv[1:])
else:
    print("IMPORTED")


