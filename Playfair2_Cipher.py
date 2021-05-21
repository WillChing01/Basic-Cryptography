"""Faster version of Playfair cipher"""

import time
import math
import random
import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *

alphabet=list('ABCDEFGHIKLMNOPQRSTUVWXYZ')

TEMP=20
STEP=0.2
COUNT=10000

def rempunct(text):
    return ''.join([x for x in text.upper() if x in alphabet])

def pad(message):
    if len(message)%2==1:
        message+='X'
    for i in range(0,len(message)-1,2):
        if message[i]==message[i+1]:
            message[i+1]='X'
    return message

def encrypt(message,key,cipher=True):
    """Key should be 25 element list"""
    message=rempunct(message)
    message=pad(message)
    mainkey={}
    output=''
    for i in range(25):
        mainkey[key[i]]=i

    if cipher==True:
        for i in range(0,len(message)-1,2):
            if mainkey[message[i]]//5==mainkey[message[i+1]]//5:
                #row the same
                output+=key[(mainkey[message[i]]//5)*5+((mainkey[message[i]]%5)+1)%5]
                output+=key[(mainkey[message[i+1]]//5)*5+((mainkey[message[i+1]]%5)+1)%5]
            elif mainkey[message[i]]%5==mainkey[message[i+1]]%5:
                #column the same
                output+=key[(mainkey[message[i]]+5)%25]
                output+=key[(mainkey[message[i+1]]+5)%25]
            else:
                #form the rectangle
                output+=key[(mainkey[message[i]]//5)*5+(mainkey[message[i+1]]%5)]
                output+=key[(mainkey[message[i+1]]//5)*5+(mainkey[message[i]]%5)]
    elif cipher==False:
        for i in range(0,len(message)-1,2):
            if mainkey[message[i]]//5==mainkey[message[i+1]]//5:
                #row the same
                output+=key[(mainkey[message[i]]//5)*5+((mainkey[message[i]]%5)-1)%5]
                output+=key[(mainkey[message[i+1]]//5)*5+((mainkey[message[i+1]]%5)-1)%5]
            elif mainkey[message[i]]%5==mainkey[message[i+1]]%5:
                #column the same
                output+=key[(mainkey[message[i]]-5)%25]
                output+=key[(mainkey[message[i+1]]-5)%25]
            else:
                #form the rectangle
                output+=key[(mainkey[message[i]]//5)*5+(mainkey[message[i+1]]%5)]
                output+=key[(mainkey[message[i+1]]//5)*5+(mainkey[message[i]]%5)]
    return output

def swaprows(a,b,key):
    for i in range(5):
        key[a*5+i],key[b*5+i]=key[b*5+i],key[a*5+i] 
    return key

def swapcols(a,b,key):
    for i in range(5):
        key[i*5+a],key[i*5+b]=key[i*5+b],key[i*5+a]
    return key

def changekey(key):
    chance=random.randint(1,50)
    if chance==1:
        #switch 2 rows
        a=random.randint(0,4)
        b=random.randint(0,4)
        key=swaprows(a,b,key)
        return key
    elif chance==2:
        #switch 2 cols
        a=random.randint(0,4)
        b=random.randint(0,4)
        key=swapcols(a,b,key)
        return key
    elif chance==3:
        #flip rows up-down
        key=swaprows(0,4,key)
        key=swaprows(1,3,key)
        return key
    elif chance==4:
        #flip cols left-right
        key=swapcols(0,4,key)
        key=swapcols(1,3,key)
        return key
    elif chance==5:
        #shuffle
        random.shuffle(key)
        return key
    else:
        #swap two letters
        a=random.randint(0,24)
        b=random.randint(0,24)
        key[a],key[b]=key[b],key[a]
        return key

def crack(cipher,parentkey):
    global TEMP,COUNT,STEP
    start=time.time()
    cipher=rempunct(cipher)
    #parentkey=alphabet[:]
    #random.shuffle(parentkey)
    parentfit=fitness(encrypt(cipher,parentkey,cipher=False))

    bestkey=None
    bestfit=-99e9

    temp=TEMP
    
    while temp>=0:
        prog=round(100*(1-temp/20))        
        print(str(prog)+"%")
        for count in range(COUNT):
            childkey=changekey(parentkey)
            childfit=fitness(encrypt(cipher,childkey,cipher=False))
            diff=childfit-parentfit
            if diff>0:
                parentkey=childkey[:]
                parentfit=childfit
            else:
                prob=math.e**(diff/temp)
                choice=weighted_choice([[True,prob],[False,1-prob]])
                if choice==True:
                    parentkey=childkey[:]
                    parentfit=childfit

            if parentfit>bestfit:
                bestfit=parentfit
                bestkey=parentkey[:]
##        print("Best key:",str(bestkey))
##        print("Best plaintext:",encrypt(cipher,bestkey,cipher=False))
##        print("Fitness:",str(bestfit))
        temp-=STEP
    end=time.time()
##    print("Process took:",str(end-start),"secs")
    return bestkey,bestfit,end-start

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def timetest():
    start=time.time()
    key=list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
    for i in range(1000):
        random.shuffle(key)
        encrypt('defendtheeastwallofthecastletwentytimesoverandifyoufailyourheadwillbefedtothewall',key)
    end=time.time()
    return str(end-start)

def main():
    c='ATSKVLXPPBVESHESUIBKATASLNFESZITUTTIMBLORESTANEOUTWHUTINURSTOMATNEYFYENUBKUOOZDWHEUODSYFERETUFESIFFEINUPHWQKWOFWHEAFEDBLCYVGVLXPPBUIPCSZNSTOHEATEMENSCATHISHESRIESEDYFOUAELICERCRTQNPBEQSCETHTOMQILORESTONOWEDIXSCONCIETETHTOMKBONDWESONSOETANEOUTWHUTINURSTOM'[0:150]
    bestk=alphabet[:]
    bestf=-99e9
    i=1
    totaltime=0
    while True:
        localbestk,localbestf,time=crack(c,bestk)
        totaltime+=time
        print("Iteration:",i)
        print("Time elapsed:",str(round(totaltime)),"secs")
        i+=1
        if localbestf>bestf:
            bestk=localbestk[:]
            bestf=localbestf
            print("Best key:",bestk)
            print("Best fitness:",bestf)
            print("Decrypted:",encrypt(c,bestk,cipher=False))
