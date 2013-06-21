#!/usr/bin/env python

from __future__ import print_function
import sys
import os
from argparse import ArgumentParser

import re
import random
import math

__version__ = "1.0"
__description__ = "Generate easy to remember passwords"
__author__ = "Juan J. Martinez"
__author_email__ = "<jjm@usebox.net>"
__license__ = "MIT"
__url__ = "https://github.com/reidrac/erwgen"

LANG = os.environ.get("LANG", "en_US")
if '.' in LANG:
    LANG = LANG.split('.')[0]

# length in words
L = 3
# length of valid words
LETTERS = (5, 6)
# include a number at the end
NUMBERS = True

# search for dictionaries
DIC_PATH = ("/usr/share/myspell/dicts", "/usr/share/myspell/")

class Pwgen(object):
    """
    Generate easy to remember passwords

    It generates a password combining (without repetitions) common dictionary
    words to obtain a long enough password to be considered secure but easy to
    memorize.

    A MySpell (or Hunspell) dictionary is required.

    Example (assuming the British dictionary is installed):

    >>> gen = erpwgen.Pwgen('en_GB')
    >>> gen.passwd()
    'WhiteHassleMinty2'

    Parameters:

        lang        Locale ID (ie. en_US, en_GB, es_ES, etc)
        l           Password length in words
        letters     Length of valid words
        numbers     If a number will be added at the end of the passwords
        blacklist   Name of the file containing a list of blacklisted words
        verbose     Output details of the operation
        dic_path    List containing paths to look for dictionaries
        dic         Use this file as dictionary

    """
    def __init__(self, lang, l=L, letters=LETTERS, numbers=NUMBERS, blacklist=None, verbose=False, dic_path=DIC_PATH, dic=None):
        self.words = None
        self.n = 0
        self.lang = lang
        self.l = l
        self.letters = letters
        self.numbers = numbers
        self.blacklist = blacklist
        self.blacklist_list = []
        self.verbose = verbose

        if dic:
            self.lang = os.path.basename(dic)
            self.load_dic(dic)
        else:
            for path in dic_path:
                if os.path.isdir(path):
                    try:
                        self.load_dic(os.path.join(path, "%s.dic" % self.lang))
                    except IOError:
                        pass

        if not self.words:
            raise IOError("unable to load the dictionary (%s) " % lang)

    def load_dic(self, filename):
        """Load a dictionary"""
        re_word = re.compile(r"(^[\w]+).*$")

        if self.blacklist:
            with open(self.blacklist, "r") as fd:
                blacklist_list = fd.readlines()

                for word in blacklist_list:
                    m = re_word.match(word)
                    if m:
                        self.blacklist_list.append(m.group(1))

            if self.verbose:
                print("%s words blacklisted" % len(self.blacklist_list))

        with open(filename, "r") as fd:
            lines = fd.readlines()

        if self.verbose:
            print("%s lines read from %s" % (len(lines), self.lang))

        words = []
        for line in lines:
            m = re_word.match(line)
            if not m:
                continue
            word = m.group(1)
            if len(word) in self.letters and word not in self.blacklist_list:
                words.append(m.group(1))

        self.n = len(words)
        self.words = words

        if self.verbose:
            print("%s valid words in the dictionary, %r letters" % (self.n, self.letters))
            var = math.factorial(self.n) / math.factorial(self.n-self.l)
            ent = self.l * (math.log(self.n) / math.log(2))
            if self.numbers:
                var *= 10
                ent += math.log(10)/math.log(2)
            print("%s possible passwords, entropy ~%d bits\n" % (var, ent))

    def passwd(self):
        """Generate a password"""
        passwd = []
        while len(passwd) < self.l:
            random.shuffle(self.words)
            # we don't want duplicates
            if self.words[0] not in passwd:
                passwd.append(self.words[0].title())

        if self.numbers:
            passwd.append(str(random.randint(0, 9)))

        return ''.join(passwd)

def main():
    """Standalone application implementing the password generator"""

    parser = ArgumentParser(description=__description__,
                            epilog="A MySpell (or Hunspell) dictionary is required.",
                            )

    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true",
                        help="enable verbose operation"
                        )

    parser.add_argument("--no-numbers", dest="numbers",
                        action="store_false",
                        help="don't add a number at the end",
                        )

    parser.add_argument("--blacklist", dest="blacklist",
                        help="read blacklisted words from a file",
                        )

    parser.add_argument("-l", "--language", dest="lang",
                        default=LANG,
                        help="language code to look for the dictionary (default: %s)" % LANG,
                        )

    parser.add_argument("--dictionary", dest="dic",
                        help="use this file as dictionary",
                        )

    parser.add_argument("pw_length",
                        nargs="?",
                        type=int,
                        default=L,
                        help="number of words to use in the passwords (default: 3)",
                        )

    parser.add_argument("num_pw",
                        nargs="?",
                        type=int,
                        default=10,
                        help="number of passwords to generate (default: 10)",
                        )

    args = parser.parse_args()

    try:
        gen = Pwgen(args.lang,
                    l=args.pw_length,
                    numbers=args.numbers,
                    blacklist=args.blacklist,
                    dic=args.dic,
                    verbose=args.verbose)
    except IOError as ex:
        parser.error(ex)

    for _ in range(args.num_pw):
        print(gen.passwd())

    return 0

if __name__ == "__main__":
    sys.exit(main())

