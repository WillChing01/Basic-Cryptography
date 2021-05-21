#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>
#include <ScoreText.h>
#include <Shuffle.c>

char* alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ";

bool decipher(char* input, char* oldalpha, char* newalpha, char* ouput);
void crack(char* ciphertext);
void mix(char* text);
void swap(char* text);

int main()
{
    char* ciphertext="AMZSRFSATARATQCPTXMZVTSKLZUUNCQLCPTXMZVAMKAMKSFZZCKVQRCHBQVKUQCIXZVTQHTASBTVSAVZPQVHZHRSZLKSLTAMPKZSKVKCHAMZPKZSKVPTXMZVKUAMQRIMTAMKSOKCE";
//    char ciphertext[250];
//    printf("Ciphertext: ");
//    fgets(ciphertext,250,stdin);
    crack(ciphertext);
//    char key[]="XZTJWUMOBEPARIQKYLFSCHVGND";
//    char plaintext[strlen(ciphertext)+1];
//    char* point=&plaintext;
//    while (true) {
//        decipher(ciphertext,key,alphabet,point);
//        printf("Plaintext: %s\n",plaintext);
//    }
    return 0;
}

bool decipher(char* input, char* oldalpha, char* newalpha, char* output)
{
    int a;
    for (a=0;a<strlen(input);a++) {
        if (input[a]==' ') {
            char* error="Error, space in message.";
            strcpy(output,error);
            return false;
        }
    }

    int i;
    for (i=0;i<strlen(input);i++) {
        const char* a=strchr(oldalpha,input[i]);
        int index=a-oldalpha;
        if (a&&index>=0) {
            output[i]=toupper(newalpha[index]);
        }
        else {
            output[i]=input[i];
        }
    }
    output[strlen(input)]='\0';
    return true;
}

void crack(char* ciphertext)
{
    char parentkey[27]="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    parentkey[strlen(parentkey)]='\0';
    char parentplaintext[strlen(ciphertext)+1];
    decipher(ciphertext,parentkey,alphabet,parentplaintext);
    double parentscore=score_quadgram(parentplaintext,strlen(parentplaintext));

    char bestkey[27];
    char bestplaintext[strlen(ciphertext)+1];
    double bestscore=-99999;

    char childkey[27];
    char childplaintext[strlen(ciphertext)+1];
    double childscore;
    int iter=0;

    bool improvement=true;
    int count;

    int check=0;

    while (true) {
        mix(parentkey);
        decipher(ciphertext,parentkey,alphabet,parentplaintext);
        parentscore=score_quadgram(parentplaintext,strlen(parentplaintext));
        iter++;
        improvement=true;
        if (check>50) {
            char* exit;
            printf("Potential key/plaintext combo found.");
            break;
        }
        while (improvement==true) {
            improvement=false;
            count=0;
            while (count<1000) {
                strcpy(childkey,parentkey);
                swap(childkey);
                decipher(ciphertext,childkey,alphabet,childplaintext);
                childscore=score_quadgram(childplaintext,strlen(childplaintext));
                if (childscore>parentscore) {
                    parentscore=childscore;
                    strcpy(parentkey,childkey);
                    strcpy(parentplaintext,childplaintext);
                    improvement=true;
                    count=0;
                }
                count++;
            }
        }
        if (parentscore>bestscore) {
            check=0;
            bestscore=parentscore;
            strcpy(bestkey,parentkey);
            strcpy(bestplaintext,parentplaintext);
            printf("Iter: %i\n",iter);
            printf("Best key: %s\n",bestkey);
            printf("Plaintext: %s\n",bestplaintext);
            printf("Score: %f\n",bestscore);
        }
        else {
            check++;
        }
    }
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

void swap(char* text)
{
    int a=rand()%25;
    int b=rand()%25;
    char temp=text[a];
    text[a]=text[b];
    text[b]=temp;
}
