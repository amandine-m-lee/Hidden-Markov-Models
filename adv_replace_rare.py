"""This program takes all of the words with counts < 5 and replaces
thier name with '_RARE_' to estimate the emmission probability of 
words not seen before"""

from sys import argv
from sets import Set
import string

script, countsrcfile, trainsrcfile, destfile = argv

# The file from which count values will be extracted 
srcfreq = open(countsrcfile)
# Initialize the list of rare words
rarewords = Set()
numrare = Set()
caprare = Set()
lastcap = Set()
# rarecount = 0
# Turns out to be about 40,000

"""Step through file and look for entries with 5 or less counts, 
add to rarewords, and exit when the evaluation type is no longer
'WORDTAG'"""

for line in srcfreq:
    parts = line.split(' ')
    if parts[1] == 'WORDTAG':
        word = parts[3].strip()
        freq = int(parts[0])
    
        if freq < 5:

            for letter in word:
                isupp = True

                if not letter in string.uppercase:
                        isupp = False

                if letter in string.digits:
                    numrare.add(word)
                    break

            if not word in numrare:
                if isupp:
                    caprare.add(word)
                elif word[-1] in string.uppercase:
                    lastcap.add(word)
                else:
                    rarewords.add(word)
            #rarecount += freq
    else:
        break

#File from which training data will be extracted
srctrain = open(trainsrcfile)
#Destination file to be written
dest = open(destfile, 'w')

#For keeping track of progress through file
#linnum =0
"""Look through the lines in the sourcefile, search and replace"""

for line in srctrain:
    words = line.split(' ')
   # linnum += 1
   # print linnum

    if len(words) == 2:
        word = words[0]

        if word in rarewords:
            dest.write('_RARE_ ' + words[1])
        elif word in numrare:
            dest.write('_NUMERIC_ ' + words[1])
        elif word in caprare:
            dest.write('_ALLCAPS_ ' + words[1])
        elif word in lastcap:
            dest.write('_NUMERIC_ ' + words[1])
        else:
            dest.write(line)
    else:
        dest.write(line)

