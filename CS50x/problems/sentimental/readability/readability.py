def main():
    letters = 0
    words = 1
    sentences = 0
    text = str(input("Text: "))

    for letter in text:
        if letter.isalpha():
            letters += 1
        elif letter.isspace():
            words += 1
        elif letter == "?" or letter == "!" or letter == ".":
            sentences += 1

    avgl = 100 / words * letters  # average of letters per 100 words
    avgs = 100 / words * sentences  # average of sentences per 100 words

    index = (0.0588 * avgl) - (0.296 * avgs) - 15.8  # index calculation
    total = round(index)

    if total < 1:  # check if less than 1
        print("Before Grade 1\n", end="")
    elif 1 <= total and total <= 16:  # check if between 1 and 16
        print(f"Grade {total}\n", end="")
    elif total > 16:  # check if it's more than 16
        print("Grade 16+\n", end="")


if __name__ == "__main__":
    main()
