from cs50 import get_int

def main():
    # get variables for main
    height = ask()
    counter = 0
    row = 0

    # make hill
    while row < height:
        row += 1
        if counter != height:
            spaces = (height -1) - counter
            while spaces > 0:
                spaces -= 1
                print(" ", end="")

            hashes = 0
            while hashes <= counter:
                hashes += 1
                print("#", end="")

            print("  ", end="")

            hashes = 0
            while hashes <= counter:
                hashes += 1
                print("#", end="")

            print()
            counter += 1

def ask():
    while True:
        height = get_int("Height: ")
        if height >= 1 and height <= 8:
            break
    return height

if __name__ == "__main__":
    main()