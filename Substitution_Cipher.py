"""simple substitution cipher with hill-climbing cracking algorithm"""

import random
import time
import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *

alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def rempunct(text):
    return ''.join([x for x in text.upper() if x in alphabet])

def cipher(plaintext,key,cipher=True):
    plaintext=rempunct(plaintext)
    output=''
    keydict={}
    if cipher==True:
        for i in range(0,26):
            keydict[alphabet[i]]=key[i]
    elif cipher==False:
        for i in range(0,26):
            keydict[key[i]]=alphabet[i]
    for letter in plaintext:
        output+=keydict[letter]
    return output

def keygen():
    """generate a random key"""
    a=alphabet[:]
    random.shuffle(a)
    return a

def crack(code):
    parent=alphabet[:]
    parentscore=fitness(cipher(code,parent,cipher=False))
    bestkey=parent[:]
    bestscore=-99e9
    iteration=0
    check=0
    while True:
        random.shuffle(parent)
        parentscore=fitness(cipher(code,''.join(parent),cipher=False))
        iteration+=1
        while True:
            improvement=False
            count=0
            while True:
                child=parent[:]
                i=random.randint(0,25)
                j=random.randint(0,25)
                child[i],child[j]=child[j],child[i]
                decrypted=cipher(code,''.join(child),cipher=False)
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
            print(cipher(code,bestkey,cipher=False))
        else:
            check+=1
        if check>0:
            print("Verifying: "+str(check*20)+"%")
        if check>=5:
            #plaintext has probably been found.
            break
    return ''.join(bestkey),str(cipher(code,''.join(bestkey),cipher=False))

def rempunct(text):
    text=text.upper()
    new=""
    for i in text:
        if i in alphabet:
            new+=i
    return new

def main():
    try:
        file=open("ciphertext.txt")
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
    while True:
        key,plaintext=crack(ciphertext)
        print("Key: ",key)
        print("Plaintext: ",plaintext)
        choice=input("Is plaintext correct? [y/n] ")
        if choice=='y':
            break
        elif choice=='n':
            continue
    return True

#if __name__=='__main__':
#    main()
#    input("Press enter to quit: ")
