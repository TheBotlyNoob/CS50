#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int get_validkey(string A);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("useage: ./substitution key\n");

        return 1;
    }


        int validation = get_validkey(argv[1]);
        if (validation == 1)
        {
            printf("key must contain 26 alphabetical characters\n");

            return 1;
        }

            // prompting user for plaintext
            string plaintext = get_string("plaintext: ");
            printf("ciphertext: ");

            int length = strlen(plaintext);

            for (int c = 0; c < length ; c++)
            {
                // printing any non-alphabet characters unchanged
                if (plaintext[c] < 'A' || (plaintext[c] > 'Z' && plaintext[c] < 'a') || plaintext[c] > 'z')
                {
                    printf("%c", plaintext[c]);
                }
                else
                {
                    for (int b = 0; b <= 25; b++)
                    {
                        if (plaintext[c] == 65 + b)
                        {
                            char upper = argv[1][b];
                            int up = isupper(upper);
                            if (up == 0)
                            {
                                upper = toupper(upper);
                                printf("%c", upper);
                            }
                            if (up != 0)
                            {
                                printf("%c", upper);
                            }

                        }
                        else if (plaintext[c] == 97 + b)
                        {
                            char lower = argv[1][b];
                            int low = islower(lower);
                            if (low == 0)
                            {
                                lower = tolower(lower);
                                printf("%c", lower);
                            }
                            if (low != 0)
                            {
                                printf("%c", lower);
                            }

                        }

                    }

                }

            }
            printf("\n");
            return 0;

}

// function assesses if the key input is valid and returns 0 if it is and 1 if it is not
int get_validkey(string A)
{
    int inputlength = strlen(A);
    if (inputlength != 26)
    {
        return 1;
    }
    else
    {

        for (int g = 0; g < 26; g++)
        {
            // checks if the character is non alphabetical
            if (A[g] < 'A' || (A[g] > 'Z' && A[g] < 'a') || A[g] > 'z')
            {
                return 1;
            }
            // scans all characters before A[g] to see if it has already been used
            for (int k = (g - 1); k >= 0; k--)
            {
                if (A[k] == A[g])
                {
                    return 1;
                }
                // also checks if different case of the same character has been used
                if (A[k] == A[g] + 32)
                {
                    return 1;
                }
                if (A[k] == A[g] - 32)
                {
                    return 1;
                }
            }
            // scans all characters after A[g] to check if it has been used already. (Not sure if this is necessary)
            for (int l = (g + 1); l < 26; l++)
            {
                if (A[l] == A[g])
                {
                    return 1;
                }
                // also checks if a different case of the same letter is used
                if (A[l] == A[g]  + 32)
                {
                    return 1;
                }
                if (A[l] == A[g] - 32)
                {
                    return 1;
                }
            }

        }
        return 0;
    }

}