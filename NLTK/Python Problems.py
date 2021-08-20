import nltk
from nltk.corpus import conll2000
grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}"""
cp = nltk.RegexpParser(grammar)
print(cp.parse(conll2000.chunked_sents('train.txt', chunk_types=['NP'])[99]))




#Pick one of the three chunk types in the CoNLL corpus.
#Inspect the CoNLL corpus and try to observe any patterns
#in the POS tag sequences that make up this kind of chunk.
# Develop a simple chunker using the regular expression chunker nltk.RegexpParser. Discuss any tag sequences that are difficult to chunk reliably.
