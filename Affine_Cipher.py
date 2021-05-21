"""fairly simple substitution cipher"""

import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *

alphabet=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def encrypt(plaintext,a,b,encrypt=True):
    plaintext=rempunct(plaintext)
    code=''
    for letter in plaintext:
        for i in range(0,len(alphabet)):
            if letter==alphabet[i]:
                if encrypt==True:
                    code+=alphabet[(a*i+b)%len(alphabet)]
                elif encrypt==False:
                    code+=alphabet[(inverse(a)*(i-b))%len(alphabet)]
    return code

def rempunct(text):
    text=text.upper()
    rem=''
    for i in text:
        if i in alphabet:
            rem+=i
    return rem

def inverse(a):
    modulo=len(alphabet)
    for i in range(1,modulo):
        if (a*i)%modulo==1:
            return i

def crackmanual(a,b):
    x=list((a[0],a[1],b[0],b[1]))
    x=[y.upper() for y in x]
    for i in range(0,len(x)):
        for j in range(0,len(alphabet)):
            if x[i]==alphabet[j]:
                x[i]=j
    x=[int(y) for y in x]
    d=(inverse((x[1]-x[3]))*(x[0]-x[2]))%26
    e=(inverse((x[1]-x[3]))*((x[1]*x[2])-(x[3]*x[0])))%26
    return d,e

def crack(cipher):
    bestfitness=-99e9
    bestkey=[None,None]
    bestplaintext=""
    i=[1,3,5,7,9,11,15,17,19,21,23,25]
    for a in i:
        for b in range(0,25):
            plaintext=encrypt(cipher,a,b,encrypt=False)
            fit=fitness(plaintext)
            if fit>bestfitness:
                bestfitness=fit
                bestkey[0],bestkey[1]=a,b
                bestplaintext=plaintext
    return bestkey,bestplaintext

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
    while True:
        key,plaintext=crack(ciphertext)
        print("Key: ",key)
        print("Plaintext: ",plaintext)
        choice=input("Is plaintext correct? [y/n] ")
        if choice=='y':
            break
        elif choice=='n':
            print("Try more plaintext. Brute force attack has been used.")
            break
    return True

if __name__=='__main__':
    main()

input("Press enter to quit: ")
