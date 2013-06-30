import emission_probs #or some shit like this 


ex = EmissionProbEmitter()

ex.srcname = "new.counts"
ex.calculate_word_probs()
ex.tagger('gene.dev', 'gene.dev.p1.out')

print ex.word_emm_probs['_RARE_']


