"""Class that stores the number of counts for each word, and for each 
unigram, bigram and trigram tag pattern. It also calculates and stores 
the emission probability of a word given a tag."""

from collections import defaultdict

class EmissionProbEmitter(object):

    def __init__(self, source_file=None):
        #Check for source file name
        if source_file is None:
            self.srcname = self.get_sourcename()
        else:
            self.srcname = source_file
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

        if self.word_counts:
            print "Already counted"
        else:
            with open(self.srcname) as src:

                #Step through file and identify record type
                for line in src:

                    parts = line.split()

                    #Count for a single word-tag combo
                    if parts[1] == 'WORDTAG':
                        count, _, tagtype, name = parts
                        #Check to see if word has already been recorded
                        self.word_counts[name][tagtype] = count
                    #Unigram, bigram, or trigram count
                    else:
                        count = parts[0]
                        seqtype = parts[1]
                        parts[-1] = parts[-1]
                        args = tuple(parts[2:]) #Make list into tuple so it can be hashed

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
        if not self.word_counts:
            self.get_counts_from_file()
        #Check for previous execution
        if self.word_emm_probs:
            print "Probabilities already computed"
        else:

            for word in self.word_counts:
                for tag in self.word_counts[word]:
                    count = self.word_counts[word][tag]
                    totalcount = self.unigram_counts[(tag,)]
                    prob = float(count)/float(totalcount)

                    self.word_emm_probs[word][tag] = prob
 
                        
    def emission_prob(self, word, tag):
       
        """ FUNCTION: emission_prob
            ARGUMETNS: self
                       word - word ot look up emission probability of
                       tagtype - tag to be analyzes"""

        return self.word_emm_probs[word].get(tag, 0)
 

    def best_tag(self, word):

        """ FUNCTION: best_tag
            ARGUMENTS: self
                       word - word to find the best unigram tag for

            Given word and no other info, find the most probable tag"""

        tagdict = self.word_emm_probs.get(word, self.word_counts['_RARE_'])

        return max(tagdict.keys(), key=lambda x: tagdict[x])

       
    def basic_tagger(self, devfile, destfile):

        """ FUNCTION: basic_tagger
            ARGUMENTS: self
                       defile - the file to be tagged
                       destfile - the file to write tagged version to

            Writes to destfile with defile and tag determined by best_tag"""

        with open(devfile) as dev:
            with open(destfile, 'w') as dest:
                #Step through each line
                for line in dev:

                    word = line.strip() #Strip newline
                    
                    if word == '': #Case of blank like
                        dest.write('\n')
                    else:
                        dest.write(word + ' ' + self.best_tag(word) + '\n')

    def third_tag_prob(self, tag1, tag2, tag3):

        if not self.word_counts:
            self.get_counts_from_file()

        bi_count = self.bigram_counts[(tag1, tag2)]
        tri_count = self.trigram_counts[(tag1, tag2, tag3)]
        
        if tri_count == 0:
            return None

        return float(tri_count)/float(bi_count)


    def viterbi_tagger(self, devfile, destfile):

#Note to self; better to put io stuff in separate function 
#Also probably shouldn't have the tagging algroithms in the class.
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
                            word_eff = '_RARE_'

                        possible_tags = self.word_counts[word_eff].keys()
                        #max with function version

                        maxtag = max(possible_tags, key= lambda tag: \
                                self.third_tag_prob(mem[0], mem[1], tag) * \
                                self.emission_prob(word_eff, tag)) 

                        dest.write(word + ' ' + maxtag + '\n')

                        mem = (mem[1], maxtag)
