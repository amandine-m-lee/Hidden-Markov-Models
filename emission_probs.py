"""Class that stores the number of counts for each word, and for each 
unigram, bigram and trigram tag pattern. It also calculates and stores 
the emission probability of a word given a tag."""

class EmissionProbEmitter(object):

    def __init__(self):
        self.srcname = ""
        self.counted = False
        self.prob_computed = False
        self.word_emm_probs = {}
        self.word_counts = {}
        self.unigram_counts = {}
        self.bigram_counts = {}
        self.trigram_counts = {}
     
    def get_sourcename(self):
    
        """ FUNCTION: get_sourcename 
            ARGUMETNS: self
            Gets user input for the filename of the source file (should 
            be of the same form as gene.counts). Checks for valid file and 
            if invalid prompts again"""

        print "Please supply a valid filename for the source file."
        self.srcname = raw_input('> ')
        try:
            file(self.srcname)
        except:
            self.get_sourcename()

    def get_counts_from_file(self):
     
        """"FUNCTION: get_coutns_from_file
            ARGUMETNS: self

            Generates the dictionaries word_counts, unigram_counts bigram_counts
            and trigram_counts, if not already generated. Calls get_sourcename if 
            necessary"""

        if self.counted:
            print "Already counted"
        else:
            #Mark self as counted
            self.counted = True
            #Attempd to oepn file
            try:
                src = open(self.srcname)
            except: #Get sourcename if necessary
                self.get_sourcename()
                src = open(self.srcname)
            #Step through file and identify record type
            for line in src:

                parts = line.split(' ')
                #Count for a single word-tag combo
                if parts[1] == 'WORDTAG':
                    count = parts[0]
                    tagtype = parts[2]
                    name = parts[3].strip() #Get rid of trailing '\n'
                    #Check to see if word has already been recorded
                    if name in self.word_counts:
                        (self.word_counts[name])[tagtype] = count
                    #If not create a new dict, otherwise add to existant dict
                    else:
                        self.word_counts[name] = {tagtype:count}
                #Unigram, bigram, or trigram count
                else:
                    count = parts[0]
                    seqtype = parts[1]
                    parts[-1] = parts[-1].strip() #Git rid of trailing '\n'
                    args = tuple(parts[2:]) #Make list into tuple

                    #Add to relevent dict. The key is a tuple with all tag types 
                    #in sequence
                    if seqtype == '1-GRAM':
                        self.unigram_counts[args] = count
                    elif seqtype == '2-GRAM':
                        self.bigram_counts[args] = count
                    else:
                        self.trigram_counts[args] = count

            src.close()
        

    def calculate_word_probs(self):
    
        """ FUCNTION: calculate_word_prob
            ARGUMETNGS: self
            
            Generates the dictionary of signle word probabilities. """

        #Check that file has been analyzed
        if not self.counted:
            self.get_counts_from_file()
        #Check for previous execution
        if self.prob_computed:
            print "Probabilities already computed"
        else:

            for word in self.word_counts:
                for tag in self.word_counts[word]:
                    count = (self.word_counts[word])[tag]
                    totalcount = self.unigram_counts[(tag,)]
                    prob = float(count)/float(totalcount)
                    
                    if word in self.word_emm_probs:
                        (self.word_emm_probs[word])[tag] = prob
                    else:
                        (self.word_emm_probs[word]) = {tag:prob}
                        
    def get_word_prob(self, word, tag):
       
        """ FUNCTION: get_word_prob
            ARGUMETNS: self
                       word - word ot look up emission probability of
                       tagtype - tag to be analyzes"""

        return (self.word_emm_probs[word])[tag]

    def best_tag(self, word):

        tagdict = self.word_emm_probs[word]
        vals = tagdict.values()
        keys = tagdict.keys()
        maxprob = max(vals)
        for key in keys:
            if tagdict[key] == maxprob:
                return key

        return None #Or some kind of error. What if word isn't in the dict? I should handle this error at some point
       
    def tagger(self, devfile, destfile):
        #best_tag
        dev = open(devfile)
        dest = open(destfile, 'w')

        for line in dev:
            word = line.strip()
            if word in self.word_emm_probs:
                dest.write(word + ' ' + self.best_tag(word) + '\n')
            else:
                dest.write(word + ' ' + self.best_tag('_RARE_') + '\n')

        dev.close()
        dest.close()

    def trigram_given_bigram_tags(self, tag1, tag2, tag3):

        if not self.counted:
            self.get_counts_from_file()

        bi_count = self.bigram_counts[(tag1, tag2)]
        tri_count = self.trigram_counts[(tag1, tag2, tag3)]

        return float(tri_count)/float(bi_count)
        

ex = EmissionProbEmitter()

ex.srcname = "new.counts"
ex.calculate_word_probs()
ex.tagger('gene.dev', 'gene.dev.p1.out')

#print ex.trigram_counts.items()

#print ex.word_emm_probs['_RARE_']

print ex.trigram_given_bigram_tags('O', 'O', 'O')
print ex.trigram_given_bigram_tags('O', 'O', 'I-GENE')
print ex.trigram_given_bigram_tags('*', 'O', 'O')
print ex.trigram_given_bigram_tags('O', 'O', 'STOP')




