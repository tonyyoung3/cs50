#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    int count = 0;
    int n;
    do
    {
        n = round(get_float("Change owed::") * 100);
    }
    while (n < 0);

    if (n  / 25 > 0)
    {
        count += n / 25 ;
        n = n % 25 ;
    };
    if (n  / 10 > 0)
    {
        count += n / 10 ;
        n = n % 10 ;
    };
    if (n  / 5  > 0)
    {
        count += n / 5 ;
        n = n % 5 ;
    };
    count += n;
    printf("%i\n", count);
}
