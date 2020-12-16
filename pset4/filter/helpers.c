#include "helpers.h"
#include "math.h"
#include "stdio.h"
#include "stdlib.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            int avg = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            image[i][j].rgbtBlue = avg ;
            image[i][j].rgbtGreen = avg ;
            image[i][j].rgbtRed = avg ;

        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed  + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed  ; 
            }


            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue ;
            }
            
            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen ;
            }            

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width / 2 ; j++)
        {
            int x = image[i][j].rgbtBlue;
            int y = image[i][j].rgbtGreen;
            int z = image[i][j].rgbtRed;
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue ;
            image[i][width - 1 - j].rgbtBlue = x;

            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen ;
            image[i][width - 1 - j].rgbtGreen = y;

            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed ;
            image[i][width - 1 - j].rgbtRed = z;

        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*temp)[width] = calloc(height, width * sizeof(RGBTRIPLE));

    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            float count = 0;
            float sumred = 0;
            float sumgreen = 0;
            float sumblue = 0;
            for (int k = j - 1 ; k < j + 2 ;  k ++)
            {

                for (int m  = i - 1 ; m < i + 2 ; m ++)
                {
                    if (k >= 0 && k < width && m >= 0 && m < height)
                    {
                        count += 1;
                        sumred += image[m][k].rgbtRed;
                        sumgreen += image[m][k].rgbtGreen;
                        sumblue += image[m][k].rgbtBlue;
                    }
                }
            }

            temp[i][j].rgbtRed = round(sumred / count);
            temp[i][j].rgbtGreen = round(sumgreen / count);
            temp[i][j].rgbtBlue = round(sumblue / count);

        }
    }

    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {

            image[i][j].rgbtBlue = temp[i][j].rgbtBlue ;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen ;
            image[i][j].rgbtRed = temp[i][j].rgbtRed  ;

        }
    }



    free(temp);

    return;
}
