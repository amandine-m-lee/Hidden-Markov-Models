"""This program takes all of the words with counts < 5 and replaces
thier name with '_RARE_' to estimate the emmission probability of 
words not seen before""" 

from sys import argv
from sets import Set

script, countsrcfile, trainsrcfile, destfile = argv

# The file from which count values will be extracted 
srcfreq = open(countsrcfile)
# Initialize the list of rare words
rarewords = Set()
# rarecount = 0
# Turns out to be about 40,000

"""Step through file and look for entries with 5 or less counts, 
add to rarewords, and exit when the evaluation type is no longer
'WORDTAG'"""

for line in srcfreq:
    parts = line.split(' ')
    if parts[1] == 'WORDTAG':
        count, _, tag, word = parts
        word = word.strip()
        freq = long(count)
    
        if freq < 5:
            rarewords.add((word, tag))
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
    
    if len(words) == 2:
        word, tag = words
        tag = tag.strip()

        if (word, tag) in rarewords:
            dest.write('_RARE_ ' + tag + '\n')
        else:
            dest.write(line)
    else:
        dest.write(line)

