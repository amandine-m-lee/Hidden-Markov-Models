"""Function that produces the emission probabilities for a given tag and value"""
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
        
        print "Please supply a valid filename for the source file."
        self.srcname = raw_input('> ')
        try:
            file(self.srcname)
        except:
            self.get_sourcename()

    def get_counts_from_file(self):
        
        if self.counted:
            print "Already counted"
        else:

            try:
                src = open(self.srcname)
            except:
                self.get_sourcename()
                src = open(self.srcname)

            for line in src:
                parts = line.split(' ')
                if parts[1] == 'WORDTAG':
                    count = parts[0]
                    tagtype = parts[2]
                    name = parts[3].strip()
                    
                    if name in self.word_counts:
                        (self.word_counts[name])[tagtype] = count

                    else:
                        self.word_counts[name] = {tagtype:count}

                else:
                    count = parts[0]
                    seqtype = parts[1]
                    parts[-1] = parts[-1].strip()
                    args = tuple(parts[2:])
                    
                    if seqtype == '1-GRAM':
                        self.unigram_counts[args] = count
                    elif seqtype == '2-GRAM':
                        self.bigram_counts[args] = count
                    else:
                        self.bigram_counts[args] = count
        
    def calculate_word_probs(self):
        if not self.counted:
            self.get_counts_from_file()

        if self.prob_computed:
            print "Probabilities already computed"
        else:

            for word in self.word_counts:
                for tag in self.word_counts[word]:
                    count = (self.word_counts[word])[tag]
                    totalcount = self.unigram_counts[(tag,)]

                    self.word_emm_probs[(word, tag)] = float(count)/float(totalcount)

    def get_word_prob(self, word, tagtype):
        return self.word_emm_probs[(word, tagtype)]



#Testing
ex = EmissionProbEmitter()
ex.srcname = "new.counts"
ex.get_counts_from_file()
ex.calculate_word_probs()



