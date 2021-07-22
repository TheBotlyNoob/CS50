#include <cs50.h>
#include <stdio.h>

int calculate(int s_size, int e_size);

int main(void)
{
    int s_size;
    int e_size;

    do
    {
        s_size = get_int("What Is The Start Size: ");
    }
    while(s_size < 9);

    do
    {
        e_size = get_int("What Is The End Size:");
    }
    while (e_size < s_size);

    calculate(s_size, e_size);
}

int calculate(int s_size, int e_size)
{
    int years = 0;
    int population = s_size;
    int gain = 0;
    int lose = 0;

    while (population < e_size)
    {
        gain = population / 3;
        lose = population / 4;
        population = population + gain - lose;
        years++;
    }

    // Print number of years
    printf("Years: %d\n", years);
    return 0;
}