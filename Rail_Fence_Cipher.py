"""
Rail-Fence cipher:
Simple fractionating cipher.
No substitution involved.
"""

import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *

alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def encrypt(plaintext,key,encryption=True):
    if type(plaintext)!=str:
        print("Input plaintext as a string.")
        return None
    code=''
    plaintext=rempunct(plaintext)
    rails=[]
    for i in range(key):
        rails.append(list())
    rail=0
    step=1
    for i in range(0,len(plaintext)):
        rails[rail].append(plaintext[i])
        i+=1
        if i==len(plaintext):
            break
        rail+=step
        if rail==key:
            step*=-1
            rail=key-2
        elif rail<0:
            step*=-1
            rail=1
    if encryption==True:
        for r in rails:
            code+=''.join(r)
    elif encryption==False:
        rails2=[list() for x in range(0,len(rails))]
        start=0
        end=0
        for i in range(0,len(rails)):
            start,end=end,end+len(rails[i])
            rails2[i].append(plaintext[start:end])
        rloop=[]
        for r in rails2:
            lp=loop(len(r[0]))
            rloop.append(lp)
        rail=0
        step=1
        for i in range(0,len(plaintext)):
            code+=rails2[rail][0][int(next(rloop[rail]))]
            rail+=step
            if rail==len(rails2):
                rail=len(rails2)-2
                step*=-1
            elif rail<0:
                rail=1
                step*=-1
    return code

def rempunct(text):
    text=text.upper()
    rem=''
    for i in text:
        if i in alphabet:
            rem+=i
    return rem

def loop(length):
    for i in range(0,length):
        yield i

def crack(ciphertext,limit):
    ciphertext=rempunct(ciphertext)
    bestplaintext=''
    bestfitness=-99e9
    for i in range(2,limit+1):
        plaintext=encrypt(ciphertext,i,encryption=False)
        fit=fitness(plaintext)
        if fit>bestfitness:
            bestfitness=fit
            bestplaintext=plaintext[:]
    return bestplaintext

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
    limit=15
    while True:
        if len(ciphertext)<15:
            limit=len(ciphertext)-1
        plaintext=crack(ciphertext,limit)
        print("Plaintext: ",plaintext)
        choice=input("Is plaintext correct? [y/n] ")
        if choice=='y':
            break
        elif choice=='n':
            increase=input("Increase key limit? [y/n] ")
            if increase=='y':
                limit+=5
                print("Limit increased.")
            else:
                print("Limit maintained.")
            continue
    return True

if __name__=='__main__':
    main()

input("Press enter to quit: ")
                
