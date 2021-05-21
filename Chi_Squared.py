"""Chi-Squared Statistic:
Used to check how well a set of data
correlates to another set. Useful for
checking how similar text is to English
by comparing average letter frequencies
to that found in text.
"""

alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
          'P','Q','R','S','T','U','V','W','X','Y','Z']
frequencies={'A':0.08167,'B':0.01492,'C':0.02782,'D':0.04253,'E':0.12702,
             'F':0.02228,'G':0.02015,'H':0.06094,'I':0.06966,'J':0.00153,
             'K':0.00772,'L':0.04025,'M':0.02406,'N':0.06749,'O':0.07507,
             'P':0.01929,'Q':0.00095,'R':0.05987,'S':0.06327,'T':0.09056,
             'U':0.02758,'V':0.00978,'W':0.02360,'X':0.00150,'Y':0.01974,
             'Z':0.00074}

def rempunct(text):
    return ''.join([x for x in text.upper() if x in alphabet])

def chisquared(string):
    """Low score=good"""
    string=rempunct(string)
    chisquared=0
    for letter in alphabet:
        count=string.count(letter)
        expected=len(string)*frequencies[letter]
        chisquared+=(((count-expected)**2)/expected)
    return chisquared
