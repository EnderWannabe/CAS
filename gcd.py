#calculates the gcd of two numbers and coefficients s and t of sa+tb = gcd(a,b)

def get_input(): #name suggests
    user = ["hi","hi"]
    while not user[0].isdigit() or not user[1].isdigit():
        user_str = input("Input two numbers seperated by a comma: ")
        user = user_str.split(",")
        if len(user) < 2:
            user += ["hi"]
        if not user[0].isdigit() or not user[1].isdigit():
            print("Try again, that's not a valid input")
    if int(user[0]) < int(user[1]):
        user = [user[1],user[0]]
    return user

def gcd(numbers,testing): #Euclidean algorithm
    x = int(numbers[0])
    y = int(numbers[1])
    if x % y == 0:
        lst = [y]
        return lst
    else:
        r = x % y
        lst = [y,r]
        test = [x] + [(x-r)/y] + lst
        testing.append(test)
        return lst

def inverse(numbers, testing): #coeff s and t
    if numbers[0] == 1:
        coeff = [1,-testing[len(testing)-1][1]]
        for i in range(len(testing)-2,-1,-1):
            coeff = [coeff[1],coeff[0]-coeff[1]*testing[i][1]]
        return coeff
    return "Those two numbers are not relatively prime, no inverses a mod b" 

def main():
    print("This program computes the gcd of two numbers")
    testing = []
    numbers = get_input()
    while len(numbers) == 2:
        numbers = gcd(numbers,testing)
    print(numbers[0]) #gcd
    inv = inverse(numbers,testing)
    print(inv) #s and t
main()
