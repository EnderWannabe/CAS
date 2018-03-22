"""
solves a system of linear equations. not very fancy.
(Now less prone to numerical instability)

Alex 12/11/17
"""
def main():
    while True:
        try:
            num = int(input("How many linear equations? "))
            break
        except ValueError:
            print("That's not a valid number. Try again. ")
    matrix = getMatrix(num) #a list of lists
    for i in range(num):
        if matrix[i][i] != 0:
            rowReduce(matrix, num, i)
        else:
            print("No pivot in every column, free variable")
            for j in range(num+1):
                matrix[i][j], matrix[i+1][j] = matrix[i+1][j], matrix[i][j]
            rowReduce(matrix, num, i)
    for i in range(num-1, 0,-1):
        for j in range(i):
            matrix[j][num] -= matrix[j][i]*matrix[i][num]
            matrix[j][i] = 0
    prettyPrint(matrix, num)

def getMatrix(n):
    matrix = []
    for i in range(n):
        row = getRow(n)
        while len(row) != n+1:
            print("Thats not a good row. Please input a new row")
            row = getRow(n)
        for i in range(len(row)):
            row[i] = float(row[i])
        matrix.append(row)
    return matrix

def rowReduce(matrix, num, i):
    a = matrix[i][i]
    for j in range(i, num+1):
        matrix[i][j] /= a
    for j in range(i+1,num):
        for k in range(i+1,num+1):
            matrix[j][k] -= matrix[j][i]*matrix[i][k]
        matrix[j][i] = 0

def getRow(n):
    row = input("Please input a row of the augmented matrix, seperated by spaces: ")
    row = row.split()
    return row

def prettyPrint(matrix, num):
    for i in range(num):
        print(matrix[i])
main()
