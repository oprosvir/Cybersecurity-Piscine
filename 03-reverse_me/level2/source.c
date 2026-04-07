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
    int     scanf_ret;      // ebp-0xc
    int     out_idx	= 1;    // ebp-0x10
    int     in_idx	= 2;    // ebp-0x14

    char    out[9];         // ebp-0x1d
    char    input[24];      // ebp-0x35
    char    temp[4];        // ebp-0x39

    printf("Please enter key: ");

    scanf_ret = scanf("%23s", input);    // read 23 symbols max + '\0'
    if (scanf_ret != 1)     no();

    if (input[1] != '0')    no();
    if (input[0] != '0')    no();

    fflush(stdin);

    memset(out, 0, 9);
    out[0] = 'd';
    temp[3] = '\0';

    while (strlen(out) < 8 && in_idx < strlen(input)) {
        temp[0] = input[in_idx];            // read from input after "00"
        temp[1] = input[in_idx + 1];
        temp[2] = input[in_idx + 2];
        
        out[out_idx] = (char)(atoi(temp));  // write to out after "d"
              
        in_idx  += 3;
        out_idx += 1;
    }
    
    out[out_idx] = '\0';

    if (strcmp(out, "delabere") == 0)
        ok();
    else
        no();

    return 0;
}
