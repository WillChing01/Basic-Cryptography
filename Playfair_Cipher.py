"""
Playfair cipher:
Uses a 5x5 square to encode message and so misses out the letter j.
Needs simulated annealing to crack.
"""

import time
import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *
import random
import math

alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
punctuation=['0','1','2','3','4','5','6','7','8','9','.','"',"'",'?','!']

def encrypt(message,key,encrypt=True):
    cipher=[]
    message=message.upper()
    #key=key.upper()
    key,square=generateSquare(key)
    message=check(message)
    for pair in message:
        app=[]
        row1=0
        row2=0
        column1=0
        column2=0
        for row in range(0,len(square)):
            for column in range(0,len(square[row])):
                if pair[0] in square[row]:
                    row1=row
                if square[row][column]==pair[0]:
                    column1=column
                if pair[1] in square[row]:
                    row2=row
                if square[row][column]==pair[1]:
                    column2=column
        if row1==row2 and encrypt==True:
            app.append(square[row1][(column1+1)%5])
            app.append(square[row2][(column2+1)%5])
            cipher.append(app)
            continue
        elif row1==row2 and encrypt==False:
            app.append(square[row1][(column1-1)%5])
            app.append(square[row2][(column2-1)%5])
            cipher.append(app)
            continue
        elif column1==column2 and encrypt==True:
            app.append(square[(row1+1)%5][column1])
            app.append(square[(row2+1)%5][column2])
            cipher.append(app)
            continue
        elif column1==column2 and encrypt==False:
            app.append(square[(row1-1)%5][column1])
            app.append(square[(row2-1)%5][column2])
            cipher.append(app)
            continue
        else:
            app.append(square[row1][column2])
            app.append(square[row2][column1])
            cipher.append(app)
            continue
    output=''
    for i in cipher:
        for x in i:
            output+=x
    return output

def check(message):
    if len(message)%2==1:
        message+='X'
    message=list(message)
    for i in range(1,len(message),2):
        if message[i]==message[i-1]:
            message[i]='X'
    message=[message[i:i+2] for i in range(0,len(message),2)]
    return message

def generateSquare(key):
    alphabet2=alphabet[:]
    #key=key.upper()
    if 'J' in key:
        key=key.replace("J","")
        print("J has been removed from key")
    square=[
            [],
            [],
            [],
            [],
            []
            ]
    i=0
    
    key=list(key)
    for x in range(len(key)-1,-1,-1):
        if key.count(key[x])>=2:
            key.pop(x)
    for letter in key:
        square[i].append(letter)
        if len(square[i])==5:
            i+=1
    for x in square:
        for y in x:
            if y in alphabet2:
                alphabet2.remove(y)
    for x in alphabet2:
        if x!='J':
            square[i].append(x)
            if len(square[i])==5 and i<5:
                i+=1
    return key,square

def crack(cipher):
    """Simulated annealing"""
    alpha=list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
    temp=10+(0.087*(len(cipher)-84))
    step=1
    count=50000
    parentkey=alpha[:]
    random.shuffle(parentkey)
    parentkey=''.join(parentkey)
    parentfitness=fitness(encrypt(cipher,parentkey,encrypt=False))
    iteration=1
    while True:
        print("Annealing run:",iteration)
        for i in range(int(20/step)):
            print(temp)
            for j in range(0,count+1):
                childkey=swap(parentkey,j)
                childfitness=fitness(encrypt(cipher,childkey,encrypt=False))
                dF=childfitness-parentfitness
                if dF>0:
                    parentkey=childkey
                    parentfitness=childfitness
                elif dF<0:
                    probability=math.e**(dF/temp)
                    if random.random()<probability:
                        parentkey=childkey
                        parentfitness=childfitness
                if j%10000==0:
                    print(j)
                    print("Parent key:",parentkey)
                    print("Fitness:",parentfitness)
            temp-=step
            print("Parent key:",parentkey)
            print("Text:",encrypt(cipher,parentkey,encrypt=False))
            print("Fitness:",parentfitness)
        iteration+=1   

def swap(key,j):
    key=list(key)
    if j%49==0:
        while True:
            a=random.randint(1,5)
            b=random.randint(1,5)
            if a!=b:
                break
        key[5*a-5:5*a],key[5*b-5:5*b]=key[5*a-5:5*a],key[5*b-5:5*b]
        for i in range(0,5):
            key[5*i+a-1],key[5*i+b-1]=key[5*i+b-1],key[5*i+a-1]
    else:
        while True:
            a=random.randint(0,len(key)-1)
            b=random.randint(0,len(key)-1)
            if a!=b:
                break
        key[a],key[b]=key[b],key[a]
    return ''.join(key)

def timetest():
    start=time.time()
    key=list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
    for i in range(1000):
        random.shuffle(key)
        encrypt('defendtheeastwallofthecastletwentytimesoverandifyoufailyourheadwillbefedtothewall',key)
    end=time.time()
    return str(end-start)
