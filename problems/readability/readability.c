#include<stdio.h>
#include<cs50.h>
#include<ctype.h>
#include<math.h>


int main(void)
{
    float letters = 0;
    float words = 1;
    float sentences = 0;
    int isalpha;
    int isspace;
    string text = get_string("Text :");

    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]) != 0)
        {
            letters++;
        }
        else if (isspace(text[i]) != 0)
        {
            words++;
        }
        else if (text[i] == '?' || text [i] == '!')
        {
            sentences++;
        }
        else if (text[i] == '.')
        {
            sentences++;
        }

    }

    float avgl = (100 / words * letters); //average of letters per 100 words
    float avgs = (100 / words * sentences); //average of sentences per 100 words

    float index = ((0.0588 * avgl) - (0.296 * avgs) - 15.8); //index calculation
    int total = round(index);

    if (total < 1) //check if less than 1
    {
        printf("Before Grade 1\n");
    }
    else if (1 <= total && total <= 16) //check if between 1 and 16
    {
        printf("Grade %i\n", total);
    }
    else if (total > 16) //check if it's more than 16
    {
        printf("Grade 16+\n");
    }


}