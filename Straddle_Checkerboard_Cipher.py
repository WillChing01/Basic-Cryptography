"""Straddle Checkerboard cipher (substitution cipher)"""

from itertools import combinations

alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
nums=list('0123456789')

def rempunct(text):
    text=str(text).upper()
    return ''.join([x for x in str(text) if x in alphabet])

def rempunctnum(num):
    return ''.join([x for x in str(num) if x in nums])

def encrypt(message,key,sparepos,cipher=True):
    """sparepos should be two numbers in a list"""

    output=''
    key=rempunct(key)
    if len(set(key))!=26:
        print("Please enter a key with 26 letters")
        return False
    row1=list(key[0:8])
    row2=list(key[8:18])
    row3=list(key[18:])
    row1.insert(sparepos[0],'')
    row1.insert(sparepos[1],'')
    checkerboard=[row1,row2,row3]

    if cipher==True:
        message=rempunct(message)
        for i in message:
            for row in range(0,3):
                for col in range(0,len(checkerboard[row])):
                    if checkerboard[row][col]==i:
                        if row!=0:
                            output+=str(sparepos[row-1])
                        output+=str(col)
    elif cipher==False:
        skip=False
        for i in range(0,len(message)):
            if skip==True:
                skip=False
                continue
            elif skip==False:
                for x in range(0,len(sparepos)):
                    if int(message[i])==sparepos[x]:
                        output+=checkerboard[x+1][int(message[i+1])]
                        skip=True
                else:
                    output+=checkerboard[0][int(message[i])]
    return output
