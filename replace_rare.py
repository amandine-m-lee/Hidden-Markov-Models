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
        word = parts[3]
        freq = int(parts[0])
    
        if freq < 5:
            rarewords.add(word.strip())
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
        if words[0] in rarewords:
            dest.write('__RARE__ ' + words[1])
        else:
            dest.write(line)
    else:
        dest.write(line)

