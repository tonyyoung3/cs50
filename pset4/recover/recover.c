#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{

    FILE *file = fopen(argv[1], "r");

    // check file exists
    if (file == NULL)
    {
        printf("Usage: ./recover image");
        return 1;
    }
    else
    {
        int jpg_count = 0 ;
        FILE *img = NULL;
        char newfile[8];
        uint8_t *buffer = malloc(sizeof(uint8_t) * 512); //assign memories for a block

        while (fread(buffer, sizeof(uint8_t), 512, file) != 0)     // read file til end
        {
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) //start
            {
                if (jpg_count == 0)     //first
                {
                    
                    sprintf(newfile, "%03i.jpg", jpg_count); //newjpg
                    img = fopen(newfile, "w");
                    fwrite(buffer, 1, sizeof(uint8_t) * 512, img);
                    jpg_count++;

                    //fclose(img);
                }
                else
                {
                    fclose(img);
                    sprintf(newfile, "%03i.jpg", jpg_count); //new jpg
                    img = fopen(newfile, "w");
                    fwrite(buffer, 1, sizeof(uint8_t) * 512, img);
                    jpg_count++;
                   
                    
                }
            }
            else //append if not header and file opened
            {
                if (jpg_count > 0)
                {
                    fclose(img);
                    img = fopen(newfile, "a");
                    fwrite(buffer, 1, sizeof(uint8_t) * 512, img);
                }
            }



        }

        free(buffer);
        fclose(img);
        fclose(file);

    }


}
