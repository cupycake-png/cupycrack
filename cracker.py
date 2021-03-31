# import argument parser to- parse the arguments
from argparse import ArgumentParser
# get all printable ascii characters
from string import printable
# used to iterate over all possibilities
from itertools import product
# use this to time the cracking
from time import time
# import hash functionality
from hashlib import md5, sha1, sha256

# list of algorithms possible for use
ALGORITHM_LIST = ['md5', 'sha1', 'sha256']

# parse arguments, returns a tuple
def parse_args() -> tuple:
    # create the argument parser object, passing in a description of the program
    arg_parser = ArgumentParser(description="[!] Tool for cracking hashes! [!]", epilog="[!] Enjoy ^^ [!]")

    # add all arguments needed: algorithms, methods and target
    arg_parser.add_argument('-a', '--algorithm', metavar='algorithm', choices=ALGORITHM_LIST, action="store", type=str, help="Algorithm to use for cracking ({})".format(ALGORITHM_LIST), required=True)
    arg_parser.add_argument('-m', '--method', metavar='method', choices=[0, 1], action="store", type=int, help="Method to use (0 - Brute Force, 1 - Wordlist)", required=True)
    arg_parser.add_argument('-t', '--target', metavar='target', action="store", type=str, help="Hash to crack", required=True)

    # get the arguments
    args = arg_parser.parse_args()

    # store them in variables
    algorithm = args.algorithm
    method = args.method
    target = args.target

    # return them
    return(algorithm, method, target)

# function for cracking, passing in the three needed variables
def start_cracking(algorithm, method, target):
    # isCracked used to know when it's cracked successfully
    isCracked = False
    # the string used for the output
    output_string = ""
    # number of repeats, allows for all possibilities if setting as 1
    pass_len = 1
    # counter used to know how many tries have gone passed
    counter = 0

    # if the brute force method was selected
    if(method == 0):
        print("[/] Brute force starting...")

        try:
            # take the start time
            start = time()
            # while the hash isn't cracked
            while(not isCracked):
                # go over all possibilities of ASCII printable
                for i in product(printable, repeat=pass_len):
                    output_string = ''.join(i)

                    # if the md5 algorithm was selected
                    if(algorithm == "md5"):
                        # compare the hash of the current guess and the target hash
                        if(md5(output_string.encode()).hexdigest() == target):
                            # we've cracked it
                            isCracked = True;
                            # break out the loop
                            break;

                    # if sha1 algorithm was selected
                    elif(algorithm == "sha1"):
                        # compare the hash of the current guess and the target hash
                        if(sha1(output_string.encode()).hexdigest() == target):
                            # we've cracked it
                            isCracked = True;
                            # break out the loop
                            break;

                    # if sha256 algoritm was selected
                    elif(algorithm == "sha256"):
                        # compare the hash of the current guess and the target hash
                        if(sha256(output_string.encode()).hexdigest() == target):
                            # we've cracked it
                            isCracked = True;
                            # break out the loop
                            break;

                    # increment the counter variable
                    counter += 1

                # increment the pass length variable
                pass_len += 1
            # take the end time
            end = time()

        # pressing CTRL+C to exit
        except KeyboardInterrupt:
            # take the end time
            end = time()
            print("[-] Stopping brute force...")
            print("[*] Spent {:.5f} seconds brute forcing...".format(end - start))
            # exit
            exit()

        # display cracked password and time taken
        print("[*] Password ({}) obtained in {} tries!".format(output_string, counter))
        print("[*] Brute forcing took: {:.5f} seconds!".format(end - start))
        exit()

    # method being wordlist
    else:
        # get the filename
        filename = str(input("[?] File to use >> "))

        # try to open and read the contents of the file
        try:
            file = open(filename, "r")
            content = file.read().split("\n")
            file.close()

        # if not found, exit
        except FileNotFoundError:
            print("[-] File not found")
            exit()

        print("[/] Wordlist attack starting...")

        try:
            # take start time
            start = time()
            # for each guess in the wordlist
            for guess in content:
                # if the md5 algorithm was selected
                if(algorithm == "md5"):
                    # compare the hash of this guess and the target hash
                    if(md5(guess.encode()).hexdigest() == target):
                        isCracked = True
                        # take end time
                        end = time()
                        break;

                 # if sha1 algorithm was selected
                elif(algorithm == "sha1"):
                    # compare the hash of the current guess and the target hash
                    if(sha1(output_string.encode()).hexdigest() == target):
                        # we've cracked it
                        isCracked = True;
                        # break out the loop
                        break;

                # if sha256 algoritm was selected
                elif(algorithm == "sha256"):
                    # compare the hash of the current guess and the target hash
                    if(sha256(output_string.encode()).hexdigest() == target):
                        # we've cracked it
                        isCracked = True;
                        # break out the loop
                        break;

                # increment the counter variable
                counter += 1

            # take the end time
            end = time()

        # if CTRL+C pressed to end it
        except KeyboardInterrupt:
            # take end time
            end = time()
            print("[-] Stopping wordlist attack...")
            print("[*] Spent {:.5f} seconds attack...".format(end - start))
            # exit
            exit()

        # if the hash was cracked
        if(isCracked):
            # display password and time taken
            print("[*] Password ({}) obtained".format(guess))
            print("[*] Wordlist attack took: {:.5f} seconds!".format(end - start))
            # exit
            exit()

        # if not cracked
        else:
            # exit
            print("[-] Password not obtained from wordlist")
            exit()

# get data from argument parsing function
algorithm, method, target = parse_args()

# display information
print("[!] Hash cracking tool! [!]", end="\n\n")

# display based on method choice
if(method == 0):
    print("[+] Algorithm: {}\n[+] Method: Brute Force\n[+] Target: {}".format(algorithm, target))

else:
    print("[+] Algorithm: {}\n[+] Method: Wordlist\n[+] Target: {}".format(algorithm, target))

# start the cracking
start_cracking(algorithm, method, target)