"""Function that produces the emission probabilities for a given tag and value"""
class EmissionProbEmitter(object):

    def __init__(self):
        self.srcname = ""
        self.counted = False
        self.prob_computed = False
        self.word_emm_probs = dict()
        self.word_counts = dict()
        self.ngram_counts = dict()
     
    def get_sourcename(self):
        
        print "Please supply a valid filename for the source file."
        self.srcname = raw_input('> ')
        try:
            file(self.srcname)
        except:
            self.get_sourcename()

#For now going to hardwire the source file... Might make it an argument later
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
                    
                    self.word_counts[(name, tagtype)] = count

                else:
                    count = parts[0]
                    seqtype = parts[1]
                    parts[-1] = parts[-1].strip()
                    args = tuple(parts[2:])

                    (self.ngram_counts)[(seqtype, args)] = count


    def calculate_word_probs(self):
        if not self.counted:
            self.get_counts_from_file()

        if self.prob_computed:
            print "Probabilities already computed"
        else:

            for wordntag in self.word_counts:
                self.word_emm_probs[wordntag] = float(self.word_counts[wordntag]) / float(self.ngram_counts[('1-GRAM', (wordntag[1],))])

    def get_word_prob(self, word, tagtype):
        return self.word_emm_probs[(word, tagtype)]



#Testing
ex = EmissionProbEmitter()
ex.srcname = "new.counts"
ex.get_counts_from_file()
ex.get_counts_from_file()
ex.calculate_word_probs()

print ex.get_word_prob('necessary', 'O')
#print ex.word_counts['sample', 'O']
"""for key in (ex.word_emm_probs).keys():
    print key
    print ex.word_emm_probs[key]"""



