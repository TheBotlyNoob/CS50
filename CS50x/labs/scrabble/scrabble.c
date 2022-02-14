#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1 < score2)
    {
        printf("Player 2 Wins With %i Points!\n", score2);
        return 0;
    }
    else if (score2 < score1)
    {
        printf("Player 1 Wins With %i Points!\n", score2);
        return 0;
    }
    else
    {
        printf("\nIts A Tie! Player 1 Got %i Points, And Player 2 Got %i Points!\n", score1, score2);
        return 0;
    }
}

int compute_score(string word)
{
    int score = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (islower(word[i]))
        {
            // If the letter is uncapitalized make the letter capitalized
            word[i] -= 32;
        }
        int listnum = word[i] - 'A';

        score += POINTS[listnum];
    }
    return score;
}
