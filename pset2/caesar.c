#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>


int main(int argc, char **argv)
{
    if (argv[2])
    {
        return 1;
    }



    int check = 1;
    for (int i = 0 ; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]) == 0)
        {
            check = 0 ;
            printf("USAGE : %s key\n", argv[0]);
            return 1;
            break;
        }
    }

    printf("%s\n", argv[1]);
    printf("Success\n");



    string c = get_string("Input: ");
    printf("ciphertext: ");

    for (int i = 0; i < strlen(c); i++)
    {

        if (isalpha(c[i]) != 0)
        {
            if (isupper(c[i]) != 0)
            {
                c[i] = tolower(c[i]);
                if ((c[i] + (atoi(argv[1]) % 26)) > 122)
                {
                    printf("%c", toupper((c[i] + (atoi(argv[1]) % 26)) - 26));
                }
                else
                {
                    printf("%c", toupper((c[i] + (atoi(argv[1]) % 26))));
                }
            }
            else
            {
                if ((c[i] + (atoi(argv[1]) % 26)) > 122)
                {
                    printf("%c", (c[i] + (atoi(argv[1]) % 26)) - 26);
                }
                else
                {
                    printf("%c", (c[i] + (atoi(argv[1]) % 26)));
                }
            }
        }
        else
        {
            printf("%c", c[i]);
        }

    }
    printf("\n");
    return 0;
}
