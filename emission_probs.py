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
                        self.bigram_counts[args] = count

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
                    #Would casting as double be better?
                    self.word_emm_probs[(word, tag)] = float(count)/float(totalcount)
    
    def get_word_prob(self, word, tagtype):
       
        """ FUNCTION: get_word_prob
            ARGUMETNS: self
                       word - word ot look up emission probability of
                       tagtype - tag to be analyzes"""

        return self.word_emm_probs[(word, tagtype)]



#Testing
"""ex = EmissionProbEmitter()
ex.srcname = "new.counts"
ex.get_counts_from_file()
ex.get_counts_from_file()
ex.calculate_word_probs()
ex.calculate_word_probs()"""



