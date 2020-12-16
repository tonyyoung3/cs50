#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    int count = 0;
    string result = "INVALID";
    long n;
    
    
    n = get_long("Number:");
    int length  = floor(log10(n)) + 1;
    
    for (int i = 0 ; i < length ; i++)
    {
        
        
        if ((i + 1) % 2 == 0)
        {
            
            if (n % 10 * 2 > 9)
            {
                count += 1;
                count += n % 10 * 2 - 10;
            }
            else
            {
                count += n % 10 * 2;
            }
        }
        else
        {
            count += n % 10 ;
        }
            
        if (i == length - 2)
        {

            if (n % 100 > 50 && n % 100 < 56 && length == 16)
            {
                result = "MASTERCARD";
            }
            if ((n % 100 == 34 || n % 100 == 37)  && length == 15)
            {
                printf("test");
                result = "AMEX";
            }
            
        }
    
        if (i == length - 1)
        {
            if (count % 10 == 0)
            {
                if (n % 10 == 4 && (length == 13 || length == 16))
                {
                    result = "VISA";
                }
            }

            else 
            {
                result = "INVALID";
            }
        }
        n = n / 10;

        
    }
    
    printf("%s\n", result);

}
