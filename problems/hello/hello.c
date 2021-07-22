#include <stdio.h>
#include <cs50.h>

int main (void) {
    // Get User Name And Greet User
    string answer = get_string("Whats your name? ");
    printf("Hello, %s\n", answer);
}