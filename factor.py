#finds prime factorization
import math
import csv
def factor(pr_int,lst):
    prime_factors = []
    while pr_int != 1:
        for p in lst:
            if (pr_int % p == 0):
                pr_int = pr_int / p
                prime_factors.append(p)
                break
    print(prime_factors)

def main():
    pr_str = input("What number do you want to factor? ")
    pr_int = int(pr_str)
    primelst = []
    with open("primes.txt") as csvfile:
        primes = csv.reader(csvfile, delimiter = ",")
        for row in primes:
            primelst.append(int(row[0]))
    factor(pr_int,primelst)

main()
