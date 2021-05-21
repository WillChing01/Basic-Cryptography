#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#include <ScoreText.h>

void decrypt(char* ciphertext, char* key, char* plaintext);
int findrow(char letter, char* key);
int findcol(char letter, char* key);
void shuffle(char* key);
void swap2rows(char* key, int a, int b);
void swap2cols(char* key,int a,int b);
void swapletters(char* key);
void reversekey(char* key);
void mix(char* text);
void flipcols(char* key);
void fliprows(char* key);
void SimAnnealing(char* ciphertext, char* plaintext);
int mod(int a,int b);

int main()
{
    srand(time(NULL));
    char* alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    char* ciphertext="XZOGQRWVQWNROKCOAELBXZWGEQYLGDRZXYZRQAEKLRHDUMNUXYXSXYEMXEHDGNXZYNTZON\
YELBEUGYSCOREUSWTZRLRYBYCOLZYLEMWNSXFBUSDBORBZCYLQEDMHQRX";
    char plaintext[strlen(ciphertext)+1];
    SimAnnealing(ciphertext,plaintext);
    return 0;
}

void decrypt(char* ciphertext, char* key, char* plaintext)
{
    int i,row1,row2,col1,col2,temp;
    char block[2];
    for (i=0;i<(strlen(ciphertext)-1);i=i+2) {
        block[0]=ciphertext[i];
        block[1]=ciphertext[i+1];
        block[2]='\0';
        row1=findrow(block[0],key);
        row2=findrow(block[1],key);
        col1=findcol(block[0],key);
        col2=findcol(block[1],key);
        if (row1==row2) {
            col1=mod(col1-1,5);
            col2=mod(col2-1,5);
        }
        else if (col1==col2) {
            row1=mod(row1-1,5);
            row2=mod(row2-1,5);
        }
        else {
            temp=col2;
            col2=col1;
            col1=temp;
        }
        plaintext[i]=key[(row1*5)+col1];
        plaintext[i+1]=key[(row2*5)+col2];
    }
    plaintext[strlen(ciphertext)]='\0';
}

int mod (int a,int b) {
    int ret=a%b;
    if (ret<0) {
        ret+=b;
    }
    return ret;
}

int findrow(char letter, char* key)
{
    int i,j;
    for (i=0;i<25;i=i+5) {
        for (j=0;j<5;j++) {
            if (key[i+j]==letter) {
                return i/5;
            }
        }
    }
}

int findcol(char letter, char* key)
{
    int i,j;
    for (i=0;i<25;i=i+5) {
        for (j=0;j<5;j++) {
            if (key[i+j]==letter) {
                return j;
            }
        }
    }
}

void shuffle(char* key)
{
    switch (rand()%50) {
        case 0 :
            swap2rows(key,rand()%5,rand()%5);
        case 1 :
            swap2cols(key,rand()%5,rand()%5);
        case 2 :
            reversekey(key);
        case 3 :
            flipcols(key);
        case 4 :
            fliprows(key);
        default :
            swapletters(key);
    }
}

void swapletters(char* key)
{
    int a=rand()%25;
    int b=rand()%25;
    char temp=key[a];
    key[a]=key[b];
    key[b]=temp;
}

void swap2rows(char* key,int a,int b)
{
    char temp;
    int i;
    for (i=0;i<5;i++) {
        temp=key[(a*5)+i];
        key[(a*5)+i]=key[(b*5)+i];
        key[(b*5)+i]=temp;
    }
}

void swap2cols(char* key,int a,int b)
{
    char temp;
    int i;
    for (i=0;i<5;i++) {
        temp=key[(i*5)+a];
        key[(i*5)+a]=key[(i*5)+b];
        key[(i*5)+b]=temp;
    }
}

void flipcols(char* key)
{
    swap2cols(key,0,4);
    swap2cols(key,1,3);
}

void fliprows(char* key)
{
    swap2rows(key,0,4);
    swap2rows(key,1,3);
}

void reversekey(char* key)
{
    int i;
    char temp[26];
    for (i=0;i<25;i++) {
        temp[24-i]=key[i];
    }
    strcpy(key,temp);
}

void mix(char* text)
{
    int i;
    char temp;
    int random;
    for (i=strlen(text)-1;i>-1;i--) {
        temp=text[i];
        random=rand()%(i+1);
        text[i]=text[random];
        text[random]=temp;
        //printf("%s\n",text);
    }
}

void SimAnnealing(char* ciphertext, char* plaintext)
{
    char parentkey[]="ABCDEFGHIKLMNOPQRSTUVWXYZ";
    char parentplaintext[strlen(ciphertext)+1];
    double parentfitness;

    char childkey[strlen(parentkey)+1];
    char childplaintext[strlen(ciphertext)+1];
    double childfitness;

    char bestkey[strlen(parentkey)+1];
    char bestplaintext[strlen(ciphertext)+1];
    double bestfitness=-99999;

    double temp;
    float step=0.2;
    int maxiter=10;
    int i;
    int count;
    double diff;
    double prob;

    for (i=0;i<maxiter;i++) {
        printf("Iteration: %i\n",i);
        mix(parentkey);
        decrypt(ciphertext,parentkey,parentplaintext);
        parentfitness=score_quadgram(parentplaintext,strlen(parentplaintext));
        for (temp=20;temp>=0;temp=temp-step) {
            for (count=0;count<10000;count++) {
                strcpy(childkey,parentkey);
                shuffle(childkey);
                decrypt(ciphertext,childkey,childplaintext);
                childfitness=score_quadgram(childplaintext,strlen(childplaintext));
                diff=childfitness-parentfitness;
                if (diff>=0) {
                    strcpy(parentkey,childkey);
                    strcpy(parentplaintext,childplaintext);
                    parentfitness=childfitness;
                }
                else if (temp>0) {
                    prob=exp(diff/temp);
                    if (prob>(1.0*rand()/RAND_MAX)) {
                        strcpy(parentkey,childkey);
                        strcpy(parentplaintext,childplaintext);
                        parentfitness=childfitness;
                    }
                }
            }
        }
        if (parentfitness>bestfitness) {
                bestfitness=parentfitness;
                strcpy(bestkey,parentkey);
                strcpy(bestplaintext,parentplaintext);
                printf("Key: %s\n",bestkey);
                printf("Plaintext: %s\n",bestplaintext);
                printf("Fitness: %f\n",bestfitness);
        }
    }
}
