#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void ___syscall_malloc(void) {
    puts("Nope.");
    exit(1);
}

void ____syscall_malloc(void) {
    puts("Good job.");
}

int main(void) {
	int		scanf_ret;			// rbp-0x8
	int     out_idx	= 1;		// rbp-0xc
	int     cmp_result;			// rbp-0x10
	long	in_idx	= 2;		// rbp-0x18

	char    out[9];				// rbp-0x21
	char    input[31];			// rbp-0x40
	char    temp[4];			// rbp-0x44

	printf("Please enter key: ");

	scanf_ret = scanf("%23s", input);
	if (scanf_ret != 1)		___syscall_malloc();	// Nope

	if (input[1] != '2')	___syscall_malloc();	// Nope
    if (input[0] != '4')	___syscall_malloc();	// Nope

	fflush(stdin);

	memset(out, 0, 9);
	out[0] = '*';
	temp[3] = '\0';

	while (strlen(out) < 8 && in_idx < strlen(input)) {
		temp[0] = input[in_idx];
		temp[1] = input[in_idx + 1];
		temp[2] = input[in_idx + 2];

		out[out_idx] = (char)(atoi(temp));

		in_idx  += 3;
		out_idx += 1;
	}

	out[out_idx] = '\0';

	cmp_result = strcmp(out, "********");
	switch (cmp_result) {
		case -2: ___syscall_malloc(); break;  // fail
		case -1: ___syscall_malloc(); break;  // fail
		case 0: ____syscall_malloc(); break;  // success
		case 1: ___syscall_malloc(); break;   // fail
		case 2: ___syscall_malloc(); break;   // fail
		case 3: ___syscall_malloc(); break;   // fail
		case 4: ___syscall_malloc(); break;   // fail
		case 5: ___syscall_malloc(); break;   // fail
		case 115: ___syscall_malloc(); break; // fail
		default: ___syscall_malloc(); break;  // fail
	}

	return 0;
}
