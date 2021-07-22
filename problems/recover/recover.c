#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // define datatype BYTE (why not char: chars are not necessarily exactly 8 bits long)
    typedef uint8_t BYTE;

    // test for correct command line input
    if (argc != 2)
    {
        printf("Usage: ./recover image");
        return 1;
    }

    char *nameofrawfile = argv[1];

    // open raw file
    FILE *rawfile_ptr = fopen(nameofrawfile, "r");

    // test if file exists
    if (rawfile_ptr == NULL)
    {
        printf("Could not open %s.\n", nameofrawfile);
        return 1;
    }

    BYTE buffer[512]; //to store the currently read chunk

    //counter and title to name jpeg
    int counter = 0;
    char title[8];
    bool open = false;
    FILE *image_ptr;

    //for (int i = 0; i < 500; i++)
    while (fread(&buffer, 512, 1, rawfile_ptr) > 0) //the reading already takes place in the while condition
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 224) == 0xe0) ) //(224 = 0xe0 = 11100000 in binary)
            {
                sprintf(title, "%d%d%d.jpg", counter / 100, (counter % 100) / 10, counter % 10);
//                printf(title[7] == '\0' ? "true" : "false");  //in order to verify that sprintf includes terminating null character (which it does)
                image_ptr = fopen(title, "w");
                open = true;
                fwrite(buffer, 512, 1, image_ptr);
                counter++;
            }
        else if (open == true)
        {
//            FILE *image = fopen(title, "a"); //a => append
            fwrite(buffer, 512, 1, image_ptr);
        }
    }
    fclose(image_ptr);
    fclose(rawfile_ptr);
}