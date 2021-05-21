"""Index of Coincidence:
Used to check if a substitution cipher is used.
Score is same for plaintext or substitution cipher
text (0.7)
"""

alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def rempunct(text):
    return ''.join([x for x in text.upper() if x in alphabet])

def ic(string):
    string=list(rempunct(string))
    ic=0
    letters=set(string)
    for i in letters:
        a=string.count(i)
        ic+=((a**2)-a)
    ic/=(len(string)**2)-len(string)
    return ic

def ic2(string):
    string=rempunct(string)
    string=[string[x:x+2] for x in range(0,len(string),2)]
    ic=0
    letters=set(string)
    for i in letters:
        a=string.count(i)
        ic+=((a**2)-a)
    ic/=(len(string)**2)-len(string)
    return ic
    

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
