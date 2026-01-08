#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void no() {
    puts("Nope.");
    exit(1);
}

void ok() {
    puts("Good job.");
}

int main() {
    char input[100];
    char result[9];
    int i, j;
    char temp[4];

    printf("Please enter key: ");
    if (scanf("%s", input) != 1) {
        no();
    }

    if (input[0] != '0' || input[1] != '0') {
        no();
    }

    fflush(stdin);
    memset(result, 0, 9);
    result[0] = 'd';
    
    i = 2;
    j = 1;

    while (strlen(result) < 8) {
        if (i >= strlen(input)) break;

        temp[0] = input[i];
        temp[1] = input[i+1];
        temp[2] = input[i+2];
        temp[3] = '\0';
        
        int val = atoi(temp);
        result[j] = (char)val;
        
        i += 3;
        j += 1;
    }
    
    result[j] = '\0';

    if (strcmp(result, "delabere") == 0) {
        ok();
    } else {
        no();
    }

    return 0;
}
