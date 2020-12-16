#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height:");

    }
    while (n < 1 || n > 8);
    int count = 1;
    for (int i = 0; i < n ; i++)
    {
        for (int k = 0 ; k < n - count; k++)
        {
            printf(" ");
        }
        for (int j = 0; j < count ; j++)
        {
            printf("#");

        }
        printf("  ");


        for (int x = 0 ; x < count ; x++)
        {
            printf("#");
        }
        printf("\n");
        count ++ ;
    }


}
