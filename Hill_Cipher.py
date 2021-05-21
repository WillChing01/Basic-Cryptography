"""
Hill Cipher:
Uses a square matrix as a key and enciphers using matrix multiplication.
"""

import sys
import os
sys.path.insert(0,os.getcwd())
from Quadgram_Statistics import *

alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def encrypt(message,key,encryption=True):
    code=''
    verify=check(key)
    if verify==False:
        print("Please use a square matrix for the key.")
        return None
    if encryption==False:
        key=inversematrix2(key)
        if key==None:
            print("Key invalid, try another")
            return None
    message=rempunct(message)
    message=pad(message,key)
    for i in range(0,len(message),len(key[0])):
        ciphertext=matrixmultiply(message[i:i+len(key[0])],key,num=False)
        code+=ciphertext
    return code

def matrixmultiply(a,b,num=True):
    if type(a[0])==str:
        a=converttonum(a) #becomes a list of nums.
        matrix=[]
        for row in b:
            matsum=0
            for i in range(0,len(row)):
                matsum+=row[i]*a[i]
            matrix.append(matsum%26)
    else:
        matrix=[list() for x in range(0,len(a[0]))]
        for i in range(0,len(a)):
            for j in range(0,len(a[i])):
                total=sum([int(a[i][x]*b[x][j]) for x in range(0,len(a[i]))])
                matrix[i].append(total)
    if num==False:
        matrix=converttoeng(matrix) #turns list into str of letters.
    return matrix

def check(key):
    for i in range(0,len(key)):
        if len(key[i])!=len(key):
            return False
    else:
        return True

def converttonum(message):
    num=[]
    for i in message:
        for j in range(0,len(alphabet)):
            if alphabet[j]==i:
                num.append(j)
    return num

def converttoeng(matrix):
    letters=''
    for i in matrix:
        letters+=alphabet[i]
    return letters

def rempunct(text):
    rem=''
    text=text.upper()
    for i in text:
        if i in alphabet:
            rem+=i
    return rem

def pad(message,key):
    while (len(message)%len(key[0]))!=0:
        message+='X'
    return message

def matrixminors(matrix):
    

def inverse26(num):
    for i in range(0,26):
        if (num*i)%26==1:
            return i
    else:
        return False

def inversematrix2(matrix):
    matrix[0][0],matrix[1][1]=matrix[1][1],matrix[0][0]
    determinant=(matrix[0][0]*matrix[1][1])-(matrix[0][1]*matrix[1][0])
    matrix[0][1]*=-1
    matrix[1][0]*=-1
    inverse=inverse26(determinant)
    if inverse==False:
        return None
    for row in range(0,len(matrix)):
        for i in range(0,len(matrix[row])):
            matrix[row][i]*=inverse
            matrix[row][i]=int(matrix[row][i]%26)
    return matrix

def crack2(cipher,matrixsize):
    global ordered
    cipher=rempunct(cipher)
    bestplaintext=''
    bestfitness=-99e9
    bestkey=None
    count=0
    for crib in ordered:
        for i in range(0,len(cipher)-len(crib)+1,2):
            subcipher=cipher[i:i+len(crib)]
            key=solve(subcipher,crib)
            if key==None:
                continue
            plaintext=encrypt(cipher,key)
            if plaintext==None:
                continue
            fit=fitness(plaintext)
            if fit>bestfitness:
                bestkey=key
                bestplaintext=plaintext[:]
                bestfitness=fit
        count+=1
        if count%100==0:
            print(count)
            if count>200:
                break
    bestkey=inversematrix2(bestkey)
    return bestplaintext,bestkey

def solve(cipher,crib):
    cipher=converttonum(cipher)
    crib=converttonum(crib)
    ciphermat,cribmat=[],[]
    matsize=int(len(cipher)**0.5)
    for i in range(0,matsize):
        ciphermat.append([cipher[x] for x in range(i,len(cipher),matsize)])
        cribmat.append([crib[x] for x in range(i,len(crib),matsize)])
    inverse=inversematrix2(ciphermat)
    if inverse==None:
        return None
    else:
        result=matrixmultiply(cribmat,inverse)
        for i in range(0,len(result)):
            for j in range(0,len(result[i])):
                result[i][j]=result[i][j]%26
        return result
