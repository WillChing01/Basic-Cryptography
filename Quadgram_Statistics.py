"""Quadgram statistics:
Checks how English-like a piece of text is.
Uses quadgrams (groups of 4 letters). Assesses
probabilities of all quadgrams in some text
against average probabilities in English.
Higher values translate to the text being
more similar to English.
"""

import math
import sys
import os
sys.path.insert(0,os.getcwd())

file=open('english_quadgrams.txt','r')
quadgrams=file.readlines()
quadgrams=[x[:-1] for x in quadgrams]
n=sum([int(x.split()[1]) for x in quadgrams])
ordered=[x.split()[0] for x in quadgrams]
quadgrams={x.split()[0]:int(x.split()[1]) for x in quadgrams}
for key in quadgrams.keys():
    quadgrams[key]=math.log10(float(quadgrams[key])/n)

def fitness(string):
    quad=[]
    string=string.upper()
    for i in range(0,len(string)-3):
        quad.append(string[i:i+4])
    prob=0
    for i in quad:
        if i not in quadgrams.keys():
            prob+=math.log10(0.01/n)
        else:
            prob+=quadgrams[i]
    return prob/len(string)
