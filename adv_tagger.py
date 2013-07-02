"""Class that stores the number of counts for each word, and for each 
unigram, bigram and trigram tag pattern. It also calculates and stores 
the emission probability of a word given a tag."""

from collections import defaultdict

class HMM(object):

    def __init__(self, source_file=None):
        #Check for source file name
        if source_file is None:
            self.srcname = self.get_sourcename()
        else:
            self.srcname = source_file
        #State checkers
        self.counted = False
        self.prob_computed = False
        #Dictionaries
        self.word_emm_probs = defaultdict(dict)
        self.word_counts = defaultdict(dict)
        self.unigram_counts = defaultdict(int)
        self.bigram_counts = defaultdict(int)
        self.trigram_counts = defaultdict(int)

     
    def get_sourcename(self):
    
        """ FUNCTION: get_sourcename 
            ARGUMETNS: self

            Gets user input for the filename of the source file (should 
            be of the same form as gene.counts). Checks for valid file and 
            if invalid prompts again"""

        valid_file = False
        while not valid_file:
            print "Please supply a valid filename for the source file."
            file_name = raw_input('> ')
            try:
                valid_file = file(file_name)
            except IOError:
                pass
        return file_name

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

            with open(self.srcname) as src:

                #Step through file and identify record type
                for line in src:

                    parts = line.split(' ')

                    #Count for a single word-tag combo
                    if parts[1] == 'WORDTAG':
                        count, _, tagtype, name = parts
                        name = name.strip() #Get rid of trailing '\n'
                        #Check to see if word has already been recorded
                        (self.word_counts[name])[tagtype] = count
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

                    (self.word_emm_probs[word])[tag] = prob
 
                        
    def emission_prob(self, word, tag):
       
        """ FUNCTION: emission_prob
            ARGUMETNS: self
                       word - word ot look up emission probability of
                       tagtype - tag to be analyzes"""
        #Couldn't get this to work with nested default dicts, because I couldn't
#Set the inner type correctly
        try:
            return self.word_emm_probs[word][tag]

        except KeyError:
            return 0

       
    def third_tag_prob(self, tag1, tag2, tag3):

        if not self.counted:
            self.get_counts_from_file()

        bi_count = self.bigram_counts[(tag1, tag2)]
        tri_count = self.trigram_counts[(tag1, tag2, tag3)]
        
        if tri_count == 0:
            return None

        return float(tri_count)/float(bi_count)


    def rare_type(self, word):

        import string

        ret = '_RARE_'
        
        for letter in word:
            isupp = True

            if not letter in string.uppercase:
                isupp = False

            if letter in string.digits:
                ret =  '_NUMERIC_'

        if isupp:
            ret = '_ALLCAPS_'
        elif word[-1] in string.uppercase:
            ret = '_LASTCAP_'
        
        if not ret in self.word_counts:
            return '_RARE_'
        else:
            return ret



    def viterbi_tagger(self, devfile, destfile):

        with open(devfile) as dev:
            with open(destfile, 'w') as dest:
            
                mem = ('*', '*')

                for line in dev:
                    word = line.strip()

                    if word == '':
                        mem = ('*', '*')
                        dest.write('\n')

                    else:

                        if word in self.word_counts:
                            word_eff = word
                        else:
                            word_eff = self.rare_type(word)

                        possible_tags = self.word_counts[word_eff].keys()

                        #max with function version
                        maxtag = max(possible_tags, key= lambda tag: self.third_tag_prob(mem[0], mem[1], tag)\
                                * self.emission_prob(word_eff, tag)) 

                        dest.write(word + ' ' + maxtag + '\n')

                        mem = (mem[1], maxtag)
