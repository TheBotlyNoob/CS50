#include <cs50.h>
#include <stdio.h>
#include <math.h>

int calculate(void);

long ask(void);

int main (void)
{
    calculate();
}

int calculate(void)
{
    // Determine whether it has a valid number of digits
    long cardnumber = ask();
    int count = 0;
    long long digits = cardnumber;
    while (digits > 0)
    {
        digits = digits/10;
        count++;
    }
    if ((count != 13) && (count != 15) && (count != 16))
    {
        printf("INVALID\n");
    }
    int number[count];


    for (int i = 0; i < count; i++)
    {
        number[i] = cardnumber % 10;
        cardnumber = cardnumber / 10;
    }

    int originalnumber[count];
    for (int i = 1; i < count; i++)
    {
        originalnumber[i] = number[i];
    }

    for (int i = 1; i < count; i+=2)
    {
        number[i] = number[i] * 2;
    }

    int v = 0;
    int temp;

    if (count == 13)
    {
      for (int i = 0; i < count; i++)
      {
        temp = (number[i] % 10) + (number[i]/10 % 10);
        v = v + temp;
      }
      if (originalnumber[12] == 4 && v % 10 == 0)
      {
        printf("VISA\n");
      }
      else
      {
        printf("INVALID\n");
      }
    }
    if (count == 15)
    {
      for (int i = 0; i < count; i++)
      {
        temp = (number[i] % 10) + (number[i]/10 % 10);
        v = v + temp;
      }
      if (originalnumber[14] == 3 && v % 10 == 0 && (originalnumber[13] == 4 || originalnumber[13] == 7))
      {
        printf("AMEX\n");
      }
      else
      {
        printf("INVALID\n");
      }
    }
    if (count == 16)
    {
      for (int i = 0; i < count; i++)
      {
        temp = (number[i] % 10) + (number[i]/10 % 10);
        v = v + temp;
      }
      if (originalnumber[15] == 4 && v % 10 == 0)
      {
        printf("VISA\n");
      }
      else if (originalnumber[15] == 5 && v % 10 == 0 && (originalnumber[14] == 1 || originalnumber[14] == 2 || originalnumber[14] == 3 || originalnumber[14] == 4 || originalnumber[14] == 5))
        {
            printf("MASTERCARD\n");
        }
      else
      {
        printf("INVALID\n");
      }
    }

    return 0;
}

long ask(void)
{
    long cardnumber;

    // Prompt user
    do
    {
         cardnumber = get_long("Enter credit card number: ");
    }

    while (cardnumber < 0);

    return cardnumber;
}