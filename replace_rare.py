"""This program takes all of the words with counts < 5 and replaces
thier name with '_RARE_' to estimate the emmission probability of 
words not seen before"""

"""countsrcfile = raw_input("Count source file: ")
trainsrcfile = raw_input("Training source file: ")
destfile = raw_input("New training file destination: ")"""

countsrcfile = "gene.counts"
trainsrcfile = "gene.train"
destfile = "new.train"

srcfreq = open(countsrcfile)

lines = srcfreq.readlines()
rarewords = []
rarecount = 0

for line in lines:
    parts = line.split(' ')
    if parts[1] == 'WORDTAG':
        tagtype = parts[1]
        word = parts[3]
        freq = int(parts[0])
    
        if freq < 5:
            print word
            rarewords.append(word.strip())
            rarecount += freq
    else:
        break

srctrain = open(trainsrcfile)
dest = open(destfile, 'w')

lines1 = srctrain.readlines()

linnum =0

for line in lines1:
    words = line.split(' ')
    if len(words) == 2:
        word = words[0]
        linnum += 1
        print linnum

        if word in rarewords:
            print word
            words[0]=('__RARE__')
    
    newline = ""
    for word in words:
        newline += word + " "

    dest.write(newline)

