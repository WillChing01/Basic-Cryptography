#include <stdio.h>
#include <string.h>
#include <ScoreText.h>

char alphabet[]={'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};

void encipher(char plaintext[],int shift,char ciphertext[]);
void decipher(char plaintext[],char ciphertext[],int shift);
void crack(char ciphertext[],int shift, char plaintext[]);

int main() {
    char unknown[256];
    int shift=0;
    char plaintext[]="";
    printf("Ciphertext to crack: ");
    gets(unknown);
    crack(unknown,shift,plaintext);
    char quit[100];
    printf("Press enter to quit: ");
    gets(quit);
    return 0;
}

void crack(char ciphertext[],int shift,char plain[]) {
    int i;
    double score;
    char testplaintext[strlen(ciphertext)+1];
    //strcpy(testplaintext,plain);
    double bestscore=-99999;
    for (i=0;i<26;i++) {
        decipher(testplaintext,ciphertext,i);
        score=score_quadgram(testplaintext,strlen(testplaintext));
        if (score>bestscore) {
            bestscore=score;
            plain=testplaintext;
            shift=i;
        }
    }
    char newplain[256];
    decipher(newplain,ciphertext,shift);
    printf("Plain: %s \n",newplain);
    printf("Shift: %i \n", shift);
    printf("Score: %f \n", bestscore);
}

void encipher(char plaintext[], int shift,char ciphertext[]) {
    //char plaintext[]="HELLO";
    //int shift=20;
    int i,j;
    //char code[strlen(plaintext)];
    for (i=0;i<strlen(plaintext);i++){
        for (j=0;j<26;j++) {
            if (alphabet[j]==plaintext[i]) {
                int index=j+shift;
                ciphertext[i]=alphabet[index%26];
            }
        }
    }
    ciphertext[strlen(plaintext)]='\0';
}

void decipher(char plaintext[], char ciphertext[],int shift) {
    int i,j;
    //char code[strlen(ciphertext)];
    for (i=0;i<strlen(ciphertext);i++){
        for (j=0;j<26;j++) {
            if (alphabet[j]==ciphertext[i]) {
                int index=j-shift+26;
                plaintext[i]=alphabet[index%26];
            }
        }
    }
    plaintext[strlen(ciphertext)]='\0';
}
