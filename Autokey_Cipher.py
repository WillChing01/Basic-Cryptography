"""
Autokey cipher:
Similar to Vigenere, but uses plaintext as a key, granting extra security.
Cracking algo is a little slow, lowering the range of keylens should increase spd.
"""

import sys
import os
sys.path.insert(0,os.getcwd())
import Vigenere_Cipher
from Quadgram_Statistics import *

minlen=15
maxlen=10

alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
padchar='X'

def encrypt(message,key,encryption=True):
    code=''
    message=rempunct(message)
    key=rempunct(key)
    currentkey=key[:]
    message,padlen=pad(message,len(key))
    for i in range(0,len(message),len(key)):
        if encryption==True:
            code+=Vigenere_Cipher.encrypt(message[i:i+len(key)],currentkey)
            currentkey=message[i:i+len(key)][:]
        elif encryption==False:
            code+=Vigenere_Cipher.encrypt(message[i:i+len(key)],currentkey,encrypt=False)
            currentkey=code[i:i+len(key)][:]
    code=depad(code,padlen)
    return code

def rempunct(text):
    text=text.upper()
    rem=''
    for i in text:
        if i in alphabet:
            rem+=i
    return rem

def pad(message,keylen):
    global padchar
    padlen=0
    while True:
        message+=padchar
        padlen+=1
        if len(message)%keylen==0:
            break
    return message,padlen

def depad(message,padlen):
    return message[:-padlen]

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
                plain=encrypt(ciphertext,''.join(key[0:i])+alphabet[j],encryption=False)
                fit=fitness(plain)
                if fit>bestfitness:
                    bestkey=j
                    bestfitness=fit
            key[i]=alphabet[bestkey]
        if old==key:
            count+=1
        else:
            count=0
        old=key[:]
    fit=fitness(encrypt(cipher,''.join(key),encryption=False))
    return ''.join(key),fit

def crack(cipher):
    global minlen
    global maxlen
    bestkey=''
    bestfitness=-99e9
    for i in range(minlen,maxlen+1):
        key,fit=optimise(cipher,i)
        if fit>bestfitness:
            bestfitness=fit
            bestkey=key
    return bestkey,encrypt(cipher,bestkey,encryption=False)

def main():
    global maxlen
    global minlen
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
        try:
            key=crack(ciphertext)
            plaintext=encrypt(ciphertext,key,encryption=False)
            print("Key:",key)
            print("Plaintext:",plaintext)
            choice=input("Is plaintext correct? [y/n] ")
            if choice=='y':
                break
            elif choice=='n':
                minlen=int(input("Minimum length of key: "))
                maxlen=int(input("Maximum length of key: "))
                print("Keylength ranges changed.")
                print("Restarting...")
        except:
            print("Error occured. More ciphertext needed/wrong cipher type?")
            return None
    return True

if __name__=='__main__':
    main()
    input("Press enter to quit: ")
