"""
Caesar cipher:
Simple cipher which shifts letters along the alphabet.
"""
import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *
from Chi_Squared import *
import time

def cipher(message,shift,encode=True):
    cipher=''
    message=message.upper()
    alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
              'P','Q','R','S','T','U','V','W','X','Y','Z']
    for letter in message:
        if letter not in alphabet:
            cipher+=letter
        for i in range(0,len(alphabet)):
            if letter==alphabet[i]:
                if encode==True:
                    cipher+=alphabet[(i+shift)%26]
                elif encode==False:
                    cipher+=alphabet[(i-shift)%26]
    return cipher

def crack(cipher):
    alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
              'P','Q','R','S','T','U','V','W','X','Y','Z']
    frequencies={'A':0.08167,'B':0.01492,'C':0.02782,'D':0.04253,'E':0.12702,
                 'F':0.02228,'G':0.02015,'H':0.06094,'I':0.06966,'J':0.00153,
                 'K':0.00772,'L':0.04025,'M':0.02406,'N':0.06749,'O':0.07507,
                 'P':0.01929,'Q':0.00095,'R':0.05987,'S':0.06327,'T':0.09056,
                 'U':0.02758,'V':0.00978,'W':0.02360,'X':0.00150,'Y':0.01974,
                 'Z':0.00074}
    cipher=cipher.upper()
    messages={}
    for shift in range(1,26):
        code=''
        for letter in cipher:
            for i in range(0,len(alphabet)):
                if letter==alphabet[i]:
                    code+=alphabet[(i+shift)%26]
        chi=chisquared(code)
        messages[chi]=code
    sort=list(messages.keys())
    sort.sort()
    if len(cipher)>10:
        return messages[sort[0]]
    else:
        return messages[sort[0]],messages[sort[1]],messages[sort[2]]

def crack2(a):
    ciphers=[cipher(a,x) for x in range(1,26)]
    fit=[fitness(x) for x in ciphers]
    d={fit[x]:ciphers[x] for x in range(0,len(ciphers))}
    return d[max(d.keys())]
