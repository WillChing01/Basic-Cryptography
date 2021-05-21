#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <ScoreText.h>

#define TEMP 20
#define STEP 0.2
#define COUNT 10000

void decipher(char plaintext[],char key[],char ciphertext[]);
int mod(int a,int b);
void shuffle(char key[]);
void swap2letters(char key[],int a,int b);
void swap2rows(char key[],int a, int b);
void swap2cols(char key[],int a,int b);
void scramble(char key[]);
void reverse(char key[]);
void crack(char ciphertext[],char bestkey[]);
bool weightedchoice(double prob);

int main() {
    char ciphertext[]="KSXNLXLIHKNMSRDLEBMSLVOTAPILDBDAKSSXFPNMELXSRQCFLIHMRYHAKMXNMRRYGAVNMTYZRMSBRYPHDZCFXBCLLVOTAPICDQCFMXTLMRSERATBZMGAQNNMTCXNAKKSBFQXBXCIBMXLFLSMHGBSAKTAIMPAARCSHGBXSZMVLIRAKDGLXEMKQAAPLFBEMSGLXELOGMSRQDSFBMPTELARAKHPNMQPNBIOKAXLGUMVTCCIPRTORPLESKOLNMSRRQCXQRNADMKSEBMSLIDMKLTBZMGAINDLXMUENOIBSDDQCFSKCLPDIUMGNCDMHQSRARQCTLLBMVTCDAIMTZCFCLXANIIU";
    char bestkey[]="ABCDEFGHIKLMNOPQRSTUVWXYZ";
    char plaintext[strlen(ciphertext)+1];

    srand(time(NULL));

    int iter=0;
    double maxscore=-99999999;
    double score;
    while(1) {
        iter++;
        crack(ciphertext,bestkey);
        decipher(plaintext,bestkey,ciphertext);
        score=score_quadgram(plaintext,strlen(plaintext));
        if (score>maxscore) {
            maxscore=score;
            printf("Best score: %f\n",score);
            printf("Iteration: %d\n",iter);
            printf("Key: %s\n",bestkey);
            printf("Plaintext: %s\n",plaintext);
        }
        else {
            printf("Iteration: %d\n",iter);
        }
    }
    return 0;
}

void crack(char ciphertext[],char bestkey[]) {
    char parentkey[]="ABCDEFGHIKLMNOPQRSTUVWXYZ";
    char parentplaintext[strlen(ciphertext)+1];
    decipher(parentplaintext,parentkey,ciphertext);
    double parentfitness=score_quadgram(parentplaintext,strlen(parentplaintext));

    double bestfitness=-9999999;

    char childkey[strlen(parentkey)+1];
    char childplaintext[strlen(ciphertext)+1];
    double childfitness;

    int count;
    float temp;
    double diff,prob;

    for (temp=TEMP;temp>=0;temp-=STEP) {
        for (count=0;count<COUNT;count++) {
            strcpy(childkey,parentkey);
            shuffle(childkey);
            decipher(childplaintext,childkey,ciphertext);
            childfitness=score_quadgram(childplaintext,strlen(childplaintext));
            diff=childfitness-parentfitness;
            if (diff>0) {
                strcpy(parentkey,childkey);
                parentfitness=childfitness;
            }
            else {
                prob=exp(diff/temp);
                bool outcome=weightedchoice(prob);
                if (outcome==true) {
                    strcpy(parentkey,childkey);
                    parentfitness=childfitness;
                }
            }
        }
        if (parentfitness>bestfitness) {
            bestfitness=parentfitness;
            strcpy(bestkey,parentkey);
        }
    }
}

bool weightedchoice(double prob) {
    double r=(double)rand()/(double)((unsigned)RAND_MAX+1);
    if (r<prob) {
        return true;
    }
    else {
        return false;
    }
}


void shuffle(char key[]) {
    int i=rand()%50;
    int a,b;
    switch(i) {
        case 0: reverse(key); break;
        case 1:
            a=rand()%5;
            b=rand()%5;
            swap2rows(key,a,b);
            break;
        case 2:
            a=rand()%5;
            b=rand()%5;
            swap2cols(key,a,b);
            break;
        case 3:
            swap2rows(key,0,4);
            swap2rows(key,1,3);
            break;
        case 4:
            swap2cols(key,0,4);
            swap2cols(key,1,3);
            break;
        default:
            a=rand()%25;
            b=rand()%25;
            swap2letters(key,a,b);
            break;
    }
}

void swap2letters(char key[],int a,int b) {
    char temp=key[a];
    key[a]=key[b];
    key[b]=temp;
}

void swap2rows(char key[],int a,int b) {
    int i;
    char temp;
    for (i=0;i<5;i++) {
        temp=key[(a*5)+i];
        key[(a*5)+i]=key[(b*5)+i];
        key[(b*5)+i]=temp;
    }
}

void swap2cols(char key[],int a,int b) {
    int i;
    char temp;
    for (i=0;i<5;i++) {
        temp=key[(i*5)+a];
        key[(i*5)+a]=key[(i*5)+b];
        key[(i*5)+b]=temp;
    }
}

void scramble(char key[]) {
    int a,i;
    char temp;
    for (i=24;i>=1;i--){
        a=rand()%(i+1);
        temp=key[a];
        key[a]=key[i];
        key[i] = temp;
    }
}

void reverse(char key[]) {
    int i;
    char newkey[strlen(key)+1];
    for (i=0;i<25;i++) {
        newkey[i]=key[24-i];
    }
    newkey[strlen(key)]='\0';
    strcpy(key,newkey);
}

int mod (int a,int b) {
    int ret=a%b;
    if (ret<0) {
        ret+=b;
    }
    return ret;
}

void decipher(char plaintext[],char key[],char ciphertext[]) {
    char a,b;
    int a_pos,b_pos,a_row,b_row,a_col,b_col;
    int i;
    for (i=0;i<strlen(ciphertext);i+=2) {
        a=ciphertext[i];
        b=ciphertext[i+1];
        a_pos=(int)(strchr(key,a)-key);
        b_pos=(int)(strchr(key,b)-key);
        a_row=a_pos/5;
        b_row=b_pos/5;
        a_col=a_pos%5;
        b_col=b_pos%5;
        if (a_row==b_row) {//row the same: shift to the right by 1
            plaintext[i]=key[((a_row*5)+mod(a_col-1,5))];
            plaintext[i+1]=key[((b_row*5)+mod(b_col-1,5))];
        }
        else if (a_col==b_col) {//col the same: shift down by 1
            plaintext[i]=key[mod(a_pos-5,25)];
            plaintext[i+1]=key[mod(b_pos-5,25)];
        }
        else {//form the rectangle
            plaintext[i]=key[((a_row*5)+(b_col))];
            plaintext[i+1]=key[((b_row*5)+(a_col))];
        }
    }
    plaintext[strlen(ciphertext)]='\0';
}
