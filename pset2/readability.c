#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    float word = 1;
    float sentence = 0;
    float letter = 0;
    int Grade = 0;
    
    string text ;

    text = get_string("Text : ");
    
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            word ++;
        }
        if (isalpha(text[i]) != 0)
        {
            letter ++;
        }
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentence ++;
        }
    }
    Grade = round(0.0588 * (letter / word) * 100 - 0.296 * (sentence / word) * 100 - 15.8);
    
    if (Grade < 1)
    {
        printf("Before Grade 1\n ");
    }
    else if (Grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", Grade);
    }
    

    
}