Hidden-Markov-Models
====================
Michael Collins's NLP Coursera Course - Lab #1

Goal: Accurately generate part of speech tags using a trigram Hidden Markov Model. In this application, I distinguish between 'I-GENE' and normal words
in biological text. 

Tasks:

1. Figure out which words in the training data occur < 5 times, and can be used to estimate counts for rare words to smooth the probabilities. 
Replace those words in the counts file with '_RARE_'. See **replace_rare.py**
2. Compile the unigram, bigram and trigram probabilities. See **emission_probs.py**
3. Implement the Vitterbi Algorithm to generated the most likely tags given the training data. Also see **emission_probs.py**
4. Classify rare types based on capitalization, digits, etc. SEe **adv_replace_rare.py**
