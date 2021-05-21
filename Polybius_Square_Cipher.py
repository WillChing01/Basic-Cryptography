"""Polybius square cipher (substitution):
only 5 different letters in ciphertext
"""

###Need to write function to deal with case where order of letters is not known.

import random
import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *

alphabet=list('ABCDEFGHIKLMNOPQRSTUVWXYZ') #no 'J' in this cipher and alphabet

def rempunct(text):
    return [x for x in text.upper() if x in alphabet]

def encrypt(plaintext,key,letters=list('ABCDE'),cipher=True):
    """key is a 25 long list only"""
    plaintext=rempunct(plaintext)
    #key=rempunct(key)
    output=''
    if len(key)!=25:
        return "Key not long enough"
    elif 'j' in key or 'J' in key:
        return "J cannot be in key"
    if cipher==True:
        for i in range(len(plaintext)):
            for x in range(25):
                if key[x]==plaintext[i]:
                    output+=letters[x//5]
                    output+=letters[x%5]
    elif cipher==False:
        for x in range(0,len(plaintext)-1,2):
            output+=key[(letters.index(plaintext[x]))*5+(letters.index(plaintext[x+1]))]
    return output

def crack(code,letters):
    parent=alphabet[:]
    parentscore=fitness(encrypt(code,parent,letters,cipher=False))
    bestkey=parent[:]
    bestscore=-99e9
    iteration=0
    check=0
    while True:
        random.shuffle(parent)
        parentscore=fitness(encrypt(code,''.join(parent),letters,cipher=False))
        iteration+=1
        while True:
            improvement=False
            count=0
            while True:
                child=parent[:]
                i=random.randint(0,24)
                j=random.randint(0,24)
                child[i],child[j]=child[j],child[i]
                decrypted=encrypt(code,''.join(child),letters,cipher=False)
                score=fitness(decrypted)
                if score>parentscore:
                    parentscore=score
                    parent=child
                    improvement=True
                    count=0
                else:
                    count+=1
                if count>1000:
                    break
            if improvement==False:
                break
        if parentscore>bestscore:
            check=0
            bestscore,bestkey=parentscore,parent[:]
            print("Possible key found: ",''.join(bestkey),"\t Score:",int(bestscore))
            print("on iteration: "+str(iteration))
            print(encrypt(code,bestkey,letters,cipher=False))
        else:
            check+=1
        if check>0:
            print("Verifying: "+str(check*20)+"%")
        if check>=5:
            #plaintext has probably been found.
            break
    return ''.join(bestkey),str(encrypt(code,''.join(bestkey),letters,cipher=False))
