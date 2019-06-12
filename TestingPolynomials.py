from Polynomials import *
#import itertools

def main():
    #a = Polynomial("ab-a+3b^2+1")
    #b = Polynomial("-3xy^2+3x-2y^3+xy-2")
    #c = Polynomial("-2+5y+4z+3x")
    d = Polynomial("-x+xy+2x^2+y^2")
    #e = Polynomial("4xy")
    #f = Polynomial("x^6+3x-1")
    #g = c + f
    #h = a + b
    #i = b + c
    #j = c - d
    #k = c + a
    #l = c * e
    #m = d * e
    #n = e * d
    #o = c * d
    #p = a.derive("a")
    #q = f.derive("x")
    r = Polynomial("x^2")
    s = Polynomial("x^3+x^5")
    #t = Polynomial("xyzabc-6")
    #Polylist = [a,f]
    #Polylist = [a,b,c,d,e,f,g,h,i,j,k]
    i, j = DivisionWithRemainder(d,[r])
    print(i[0],j)
main()
