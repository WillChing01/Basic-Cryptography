#ifndef SCORETEXT_H_INCLUDED
#define SCORETEXT_H_INCLUDED
#include <quadgram.h>

double score_quadgram(char* word, int len);

double score_quadgram(char* word,int len) {
    int index[4];
    int i;
    double score=0;
    for (i=0;i<len-3;i++) {
        index[0]=(word[i]-'A');
        index[1]=(word[i+1]-'A');
        index[2]=(word[i+2]-'A');
        index[3]=(word[i+3]-'A');
        score+=quadgram[17576*index[0]+676*index[1]+26*index[2]+index[3]];
    }
    return score;
}

#endif // SCORETEXT_H_INCLUDED
