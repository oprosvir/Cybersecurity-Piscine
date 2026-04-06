#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void no(void) {
    puts("Nope.");
    exit(1);
}

void ok(void) {
    puts("Good job.");
}

int main(void) {
    int scan_result;    // ebp-0xc
    int j;              // ebp-0x10
    int i;              // ebp-0x14

    char out[9];        // ebp-0x1d
    char input[24];     // ebp-0x35
    char temp[4];       // ebp-0x39

    printf("Please enter key: ");
    scan_result = scanf("%23s", input);    // read 23 symbols max + '\0'
    if (scan_result != 1) {
        no();
    }
    if (input[1] != '0') {
        no();
    }
    if (input[0] != '0') {
        no();
    }

    fflush(stdin);

    memset(out, 0, 9);
    out[0] = 'd';
    temp[3] = '\0';

    i = 2;      // read from input after "00"
    j = 1;      // write to out after "d"

    while (strlen(out) < 8) {
        if (i >= strlen(input)) break;

        temp[0] = input[i];
        temp[1] = input[i+1];
        temp[2] = input[i+2];
        
        out[j] = (char)atoi(temp);        
        i += 3;
        j += 1;
    }
    
    out[j] = '\0';

    if (strcmp(out, "delabere") == 0)
        ok();
    else
        no();

    return 0;
}
