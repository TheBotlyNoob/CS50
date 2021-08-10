from math import log10

def main():
    card_number = get_card()
    checksum = calculate_checksum(card_number)
    check_card_type(card_number, checksum)


def get_card():
    while True:
        card_number = input("Credit card number: ")
        if card_number.isnumeric():
            break

    return int(card_number)


def calculate_checksum(card_number):
    even_sum = 0
    odd_sum = 0
    card_number = reversed([int(digit) for digit in str(card_number)])
    for i, digit in enumerate(card_number):
        if (i + 1) % 2 == 0:
            odd_digit = digit * 2
            if odd_digit > 9:
                odd_sum += int(odd_digit / 10) + odd_digit % 10
            else:
                odd_sum += odd_digit
        else:
            even_sum += digit
    checksum = even_sum + odd_sum
    return checksum


def check_card_type(card_number, checksum):
    start_numbers = int(str(card_number)[0:2])
    card_length = int(log10(card_number)) + 1
    checksum_last_digit = checksum % 10

    if checksum_last_digit == 0:
        if start_numbers in [34, 37] and card_length == 15:
            print("AMEX")
        elif int(str(card_number)[0]) == 4 and card_length in [13, 16]:
            print("VISA")
        elif start_numbers in range(51, 56) and card_length == 16:
            print("MASTERCARD")
        else:
            print("INVALID")
    else:
        print("INVALID")

if __name__ == "__main__":
  main()
