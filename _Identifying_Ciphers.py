"""This program should give an indication as to what cipher you are dealing with"""

import sys
import os
sys.path.insert(0,os.getcwd())
from Chi_Squared import *
from Index_Coincidence import *

alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def rempunct(text):
    return ''.join([x for x in text.upper() if x in alphabet])

def main():
    print('Input ciphertext:')
    cipher=input()
    cipher=rempunct(cipher)
    print(cipher+"\n")

    chi=chisquared(cipher)
    indexco=ic(cipher)
    indexco2=ic(cipher)
    even=not bool(len(cipher)%2)
    letterset=set(cipher)

    print("Chi-squared:",str(chi))
    print("Index of coincidence:",str(indexco))
    print("Diagraphic index of coincidence:",str(indexco2))
    print("Even length:",str(even))
    print("Letters:",str(letterset))
    print("Number of letters:",str(len(letterset)),"\n")

    
    """Check if it's a transposition"""
    transciphers=['Columnar transposition','Rail fence']
    if indexco>0.055 and chi<(len(cipher)/2):
        print("Possibly a transposition cipher:")
        for i in transciphers:
            print("-"+str(i))
        return None

    """Check if it's a substitution cipher"""
    subciphers=['Caesar','Affine','Simple Substitution']
    if indexco>0.055:
        print("Possibly a substitution cipher:")
        for i in subciphers:
            print("-"+str(i))
        return None
    elif indexco2>0.055 and even==True and len(letterset)==5:
        print("Possibly a substitution cipher:")
        print("Polybius square")
        return None

    """Check if it's a polyalphabetic substitution cipher"""
    polyciphers=['Vigenere','Beaufort','Porta','Gronsfeld']
    if indexco<0.055:
        ics=findperiod(cipher,20 if len(cipher)>20 else len(cipher)-1)
        mean=sum(ics.keys())/len(ics.keys())
        if max(ics.keys())>=mean*1.2 and max(ics.keys())>0.055:
            likelyperiod=ics[max(ics.keys())]
            print("Possibly a polyalphabetic cipher:")
            for i in polyciphers:
                print("-",str(i))
            print("Possible period:",likelyperiod)
            return None

    """Check if it's a polygraphic grid cipher"""
    gridciphers=['Playfair','Bifid','Foursquare']
    if len(letterset)<=25 and 'J' not in letterset:
        print("Possibly a polygraphic cipher:")
        for i in gridciphers:
            print("-"+str(i))
            return None

if __name__=='__main__':
    main()
