"""finds period for bifid ciphers
I don't know if this works yet"""

def findperiod(cipher):
    if len(cipher)<150:
        print("Need more ciphertext.")
        return False
    else:
        variances=[]
        for step in range(1,21):
            bigramcount={}
            bigrams=[cipher[x]+cipher[x+step+1] for x in range(0,len(cipher)-(step+1))]
            for x in bigrams:
                if x not in bigramcount.keys():
                    bigramcount[x]=1
                else:
                    bigramcount[x]+=1
            totalbigrams=sum([x for x in bigramcount.values()])
            mean=totalbigrams/len(bigramcount.keys())
            differences=[(x-mean)**2 for x in bigramcount.values()]
            variance=sum(differences)/len(differences)
            variances.append(variance)
            bigrams.clear()
        for i in range(0,len(variances)):
            print(i+1,' : ',variances[i])
