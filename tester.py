from emission_probs import EmissionProbEmitter #or some shit like this 


ex = EmissionProbEmitter()

ex.srcname = "new.counts"
ex.calculate_word_probs()
ex.tagger('gene.dev', 'gene.dev.p1.out')

#print ex.word_emm_probs['_RARE_']

print ex.trigram_given_bigram_tags('O', 'O', 'O')
print ex.trigram_given_bigram_tags('O', 'O', 'I-GENE')
print ex.trigram_given_bigram_tags('*', 'O', 'O')
print ex.trigram_given_bigram_tags('O', 'O', 'STOP')




