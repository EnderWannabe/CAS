#generates primes
import math
def main():
    pr_str = input("How high? ")
    pr = int(pr_str)
    primes= []
    #composites = []
    checker = 0
    file = open("primes2.txt", "w")
    for i in range(2,pr):
        for pri in primes:
            if (pri >= math.sqrt(i)+1):
                break
            if (i % pri == 0):
                checker = i #if I want composites
                break
        if (checker == 0):
            file.write(str(i))
            file.write(",")
            file.write("\n")
            primes.append(i)
        #else:
            #composites.append(i)
        checker = 0
    #print("primes:", primes)
    #print("composites:", composites)
main()
