#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void mix(char* text);
void random();

int main()
{
    char string[]="abcdefg";
    char *p=&string;
    int j;
    string[strlen(string)]='\0';
    for (j=0;j<3;j++) {
        mix(p);
        printf("%s\n",p);
    }
    return 0;
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
