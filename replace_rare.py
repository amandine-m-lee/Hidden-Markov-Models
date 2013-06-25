"""This program takes all of the words with counts < 5 and replaces
thier name with '_RARE_' to estimate the emmission probability of 
words not seen before"""

"""countsrcfile = raw_input("Count source file: ")
trainsrcfile = raw_input("Training source file: ")
destfile = raw_input("New training file destination: ")"""

countsrcfile = "gene.counts"
trainsrcfile = "short.train"
destfile = "new.train"

srcfreq = open(countsrcfile)

rarewords = []
rarecount = 0

for line in srcfreq:
    parts = line.split(' ')
    if parts[1] == 'WORDTAG':
        word = parts[3]
        freq = int(parts[0])
    
        if freq < 5:
          #  print word
            rarewords.append(word.strip())
            rarecount += freq
    else:
        break

srctrain = open(trainsrcfile)
dest = open(destfile, 'w')

linnum =0

for line in srctrain:
    words = line.split(' ')
    linnum += 1
    print linnum
    if len(words) == 2:
        if words[0] in rarewords:
            dest.write('__RARE__ ' + words[1])
        else:
            dest.write(line)
    else:
        dest.write(line)

