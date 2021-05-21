"""
Vigenere Cipher:
Encrypts and Decrypts Messages
"""

import math
import sys
import os
sys.path.insert(0,os.getcwd())
from Index_Coincidence import *
from Quadgram_Statistics import *

alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def encrypt(message,key,encrypt=True):
    cipher=''
    message=message.upper()
    message=rempunct(message)
    key=key.upper()
    while len(key)<len(message):
        key+=key
    if len(key)>len(message):
        key=key[:len(message)]
    for i in range(0,len(message)):
        row=None
        column=None
        for x in range(0,len(alphabet)):
            if key[i]==alphabet[x]:
                row=x
            if message[i]==alphabet[x]:
                column=x
            if row!=None and column!=None:
                break
        if encrypt==True:
            cipher+=alphabet[(column+row)%26]
        else:
            cipher+=alphabet[(column-row)%26]
    return cipher

def encryptporta(message,key,encrypt=True):
    table=[list('NOPQRSTUVWXYZABCDEFGHIJKLM'),
           list('OPQRSTUVWXYZNMABCDEFGHIJKL'),
           list('PQRSTUVWXYZNOLMABCDEFGHIJK'),
           list('QRSTUVWXYZNOPKLMABCDEFGHIJ'),
           list('RSTUVWXYZNOPQJKLMABCDEFGHI'),
           list('STUVWXYZNOPQRIJKLMABCDEFGH'),
           list('TUVWXYZNOPQRSHIJKLMABCDEFG'),
           list('UVWXYZNOPQRSTGHIJKLMABCDEF'),
           list('VWXYZNOPQRSTUFGHIJKLMABCDE'),
           list('WXYZNOPQRSTUVEFGHIJKLMABCD'),
           list('XYZNOPQRSTUVWDEFGHIJKLMABC'),
           list('YXNOPQRSTUVWXCDEFGHIJKLMAB'),
           list('ZNOPQRSTUVWXYBCDEFGHIJKLMA')]
    cipher=''
    message=message.upper()
    message=rempunct(message)
    key=key.upper()
    alphadict={}
    for i in range(26):
        alphadict[alphabet[i]]=i
    for i in range(len(message)):
        keyind=i%len(key)
        row=alphadict[key[keyind]]//2
        col=alphadict[message[i]]
        cipher+=table[row][col]
    return cipher
        

def findperiod(cipher,limit):
    ics={}
    for i in range(2,limit+1):
        total=0
        for j in range(i):
            string=''.join([cipher[x] for x in range(j,len(cipher),i)])
            total+=ic(string)
        total/=i
        ics[total]=i
    return ics

def chisquared(cipher):
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
    for shift in range(0,26):
        code=''
        for letter in cipher:
            for i in range(0,len(alphabet)):
                if letter==alphabet[i]:
                    code+=alphabet[(i+shift)%26]
        chisquared=0
        letters=set(code)
        for letter in letters:
            count=code.count(letter)
            expected=len(code)*frequencies[letter]
            chisquared+=((count-expected)**2)/expected
        messages[chisquared]=shift
    sort=list(messages.keys())
    sort.sort()
    return messages[sort[0]],sort[0]

def crack(cipher,limit,method=1):
    poss=[]
    code=[]
    ic=findperiod(cipher,limit)
    for i in ic.keys():
        if i>0.04:
            poss.append(ic[i])
    if method==1:
        bestf=-99e9
        bestk=None
        for i in poss:
            key=''
            for j in range(i):
                string=''.join([cipher[x] for x in range(j,len(cipher),i)])
                key+=alphabet[(26-chisquared(string)[0])%26]
            code.append(key)
        for k in code:
            f=fitness(encrypt(cipher,k,encrypt=False))
            if f>bestf:
                bestf=f
                bestk=k
        return bestk
    elif method==2:
        bestkey=None
        bestfit=-99e9
        for i in poss:
            key,fit=optimise(cipher,i)
            if fit>bestfit:
                bestfit=fit
                bestkey=key[:]
        return bestkey

def optimise(cipher,keylen):
    old=None
    key=['A' for i in range(keylen)]
    count=0
    while count<2:
        for i in range(0,keylen):
            bestkey=0
            bestfitness=-99e9
            ciphertext=''.join([cipher[x:x+i+1] for x in range(0,len(cipher),keylen)])
            for j in range(0,26):
                plain=encryptporta(ciphertext,''.join(key[0:i])+alphabet[j],encrypt=False)
                fit=fitness(plain)
                if fit>bestfitness:
                    bestkey=j
                    bestfitness=fit
                    key[i]=alphabet[bestkey]
        if old==key:
            count+=1
        else:
            count=0
        old=key
    fit=fitness(encryptporta(cipher,''.join(key),encrypt=False))
    return ''.join(key),fit

def rempunct(text):
    text=text.upper()
    new=""
    for i in text:
        if i in alphabet:
            new+=i
    return new

def main():
    try:
        file=open('ciphertext.txt')
        lines=file.readlines()
        ciphertext=rempunct(''.join(lines))
        if len(ciphertext)==0:
            ciphertext=input("Ciphertext to crack: ")
            ciphertext=rempunct(ciphertext)
        else:
            print("File found.")
    except:
        ciphertext=input("Ciphertext to crack: ")
        ciphertext=rempunct(ciphertext)
    print("Process initiated: ")
    limit=10
    while True:
        try:
            choice=input("Method:\n\t1\n\t2\nChoice: ")
            key=''.join(crack(ciphertext,limit,int(choice)))
            if len(key)==0:
                print("More ciphertext needed.")
                return None
            plaintext=encrypt(ciphertext,key,encrypt=False)
            print("Key:",key)
            print("Plaintext:",plaintext)
            choice=input("Is plaintext correct? [y/n] ")
            if choice=='y':
                break
            elif choice=='n':
                inc=input("Increase max key-length? [y/n] ")
                if inc=='y':
                    limit+=5
        except:
            print("Error occured. More ciphertext needed/wrong cipher type?")
            return None
    return True

if __name__=='__main__':
    main()
    input("Press enter to quit: ")
