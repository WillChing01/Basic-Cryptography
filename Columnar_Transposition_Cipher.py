"""
Columnar Transposition Cipher:
Basic transposition cipher which jumbles plaintext without changing the letters.
Comes with a brute force algorithm to try all keys of len(10) and below.
"""

alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

import itertools
import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *

def rempunct(text):
    return ''.join([x for x in text.upper() if x in alphabet])

def encrypt(message,key,regular=True,cipher=True):
    message=message.upper()
    columns=[list() for x in range(0,len(key))]
    if cipher==True:
        for i in range(0,len(message)):
            columns[i%(len(key))].append(message[i])
        if regular==True and len(message)%len(key)!=0:
            for x in range(0,len(columns)):
                while len(columns[x])<(len(message)//len(key))+1:
                    columns[x].append('X')
        sort=sorted(key);sortcol=[]
        for i in sort:
            for x in range(0,len(key)):
                if i==key[x]:
                    if columns[x] not in sortcol:
                        sortcol.append(columns[x])
        return ''.join([item for sublist in sortcol for item in sublist])
    elif cipher==False:
        start=0
        end=0
        sortcol=[]
        sort=sorted(key)
        result=''
        for i in range(0,len(columns)):
            start,end=end,end+int(len(message)/len(columns))
            columns[i].append(message[start:end])
        for i in key:
            for j in range(0,len(key)):
                if sort[j]==i:
                    sortcol.append(columns[j])
        for y in range(0,len(sortcol[0][0])):
            for x in sortcol:
                result+=x[0][y]
        return result

def crack(ciphertext,maxkeylen=10):
    """Don't go above 10"""
    ciphertext=rempunct(ciphertext)
    bestfitness=-99e9
    bestplaintext=None
    bestkey=None
    for keylen in range(2,int(maxkeylen)+1):
        if len(ciphertext)%keylen!=0:
            continue
        keys=list(itertools.permutations(alphabet[0:keylen]))
        for tup in keys:
            key=''.join([x for x in tup])
            plaintext=encrypt(ciphertext,key,cipher=False)
            fit=fitness(plaintext)
            if fit>bestfitness:
                bestfitness=fit
                bestplaintext=plaintext
                bestkey=key
    print("Best fitness:",bestfitness)
    print("Best plaintext:",bestplaintext)
    print("Best key:",bestkey)
    return ciphertext,key
        
