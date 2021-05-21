"""frequency analysis"""

alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

engfreq={'A':0.08167,'B':0.01492,'C':0.02782,'D':0.04253,'E':0.12702,
         'F':0.02228,'G':0.02015,'H':0.06094,'I':0.06966,'J':0.00153,
         'K':0.00772,'L':0.04025,'M':0.02406,'N':0.06749,'O':0.07507,
         'P':0.01929,'Q':0.00095,'R':0.05987,'S':0.06327,'T':0.09056,
         'U':0.02758,'V':0.00978,'W':0.02360,'X':0.00150,'Y':0.01974,
         'Z':0.00074}

values=sorted(list(engfreq.values()),reverse=True)
engsort=[]
for i in values:
    for j in engfreq:
        if engfreq[j]==i:
            engsort.append(j)

def analyse(string):
    text=string
    text=text.upper()
    for i in text:
        if i not in alphabet:
            text=text.replace(i,"")
    letters=set(text)
    freq={}
    for letter in letters:
        if letter in alphabet:
            frequency=round((text.count(letter)/len(text)),2)
            freq[letter]=frequency
    vals=sorted(list(freq.values()),reverse=True)
    sort=[]
    for i in vals:
        for j in freq:
            if freq[j]==i:
                if j not in sort:
                    sort.append(j)
    print(string)
    for i in range(len(engfreq.keys())):
        if i>=len(sort):
            print(engsort[i]+": "+str(engfreq[engsort[i]]))
        else:
            print(engsort[i]+": "+str(engfreq[engsort[i]])+"    "+sort[i]+": "+str(freq[sort[i]]))
    return freq
