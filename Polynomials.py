from math import *
from MoreMath import *
from PolynomialExceptions import *
import itertools
import fractions
import random
import cmath

#redoing format of polynomial to no longer use a full exp list

class Polynomial(object):

    def __init__(self, string, polynomial = None, varlist = None, degree = None, NewExpLst = None):
        if polynomial == None:
            polynomial = []
        if varlist == None:
            varlist = []
        if degree == None:
            degree = 0
        if NewExpLst == None:
            NewExpLst = []
        if string == "" and (polynomial == [] or varlist == [] or degree == 0 or NewExpLst == []):
            raise InsufficientInputError
        if string != "" and (polynomial != [] or varlist != [] or degree != 0 or NewExpLst != []):
            raise ConflictingInputError #can't take both a string and other polynomial info
        self.Polynomial = polynomial
        self.varlist = varlist
        self.degree = degree
        #finds the variables and makes a sorted list of them
        if string != "":
            for i in string:
                if i.isalpha() and i not in self.varlist:
                    self.varlist.append(i)
        self.varlist.sort()
        self.varnum = len(self.varlist)
        if string != "":
            #finds coefficients and corresponding exponent vectors
            counter = 0
            plusminus = ["-","+"]
            tempexplist = []
            coeflist = []
            for i in string:
                if string[counter - 1] in plusminus or (counter == 0 and string[0] != "-"):
                    if i.isdigit():
                        value = int(i)
                        if counter != 0:
                            if string[counter - 1] == "-":
                                value *= -1
                    elif string[counter-1] == "+":
                        value = 1
                    else:
                        value = -1
                    coeflist.append(value)
                    expvec = []
                    end = min(counter + 3*self.varnum + 1, len(string))
                    #makes a list of exponents
                    for j in range(self.varnum):
                        expvec.append(0)
                    for j in range(counter, end):
                        if string[j] in ["+"," ","-"]:
                            break
                        if string[j].isalpha():
                            if j+2 < len(string):
                                if string[j+2].isdigit() and string[j+1] not in plusminus:
                                    expvec[bsearch(self.varlist, string[j])] = int(string[j+2])
                                else:
                                    expvec[bsearch(self.varlist, string[j])] = 1
                            else:
                                expvec[bsearch(self.varlist, string[j])] = 1
                    tempexplist.append(expvec)
                counter += 1
            #finds the degree of the polynomial
            #and creates an exp list with corresponding coefficients
            temppolynomial = []
            for i in range(len(tempexplist)):
                temppolynomial.append(coeflist[i])
                tempsum =sum(tempexplist[i])
                if(tempsum > self.degree):
                    self.degree = tempsum
            doublegrevlexsort(tempexplist,temppolynomial)
            self.Polynomial = temppolynomial
            self.NewExpLst = tempexplist
        self.Monomial = False
        if len(self.Polynomial) == 1:
            self.Monomial = True

    def __getitem__(self, L):
        varlist = self.getVarlist()
        if len(varlist) != 1:
            if len(L) != len(varlist):
                return KeyError
            if not isinstance(L, list):
                return TypeError
            poly = self.getPoly()
            explist = self.NewExpLst
            final = 0
            for i in range(len(poly)):
                temp = poly[i]
                for j in range(len(explist[i])):
                    temp *=  L[j] ** explist[i][j]
                final += temp
            return final
        else:
            if not (isinstance(L, int) or isinstance(L, list) or isinstance(L,type(1j))):
                return TypeError
            if isinstance(L, int) or isinstance(L,type(1j)):
                poly = self.getPoly()
                explist = self.NewExpLst
                final = 0
                for i in range(len(poly)):
                    temp = poly[i] * (L ** explist[i][0])
                    final += temp
                return final
            elif isinstance(L, list):
                poly = self.getPoly()
                explist = self.NewExpLst
                final = 0
                for i in range(len(poly)):
                    temp = poly[i] * L[0] ** explist[i][0]
                    final += temp
                return final

    def __str__(self):
        poly = self.getPoly()
        explist = self.NewExpLst
        varlist = self.getVarlist()
        final = ""
        for i in range(len(poly)):
            coeff = poly[i]
            if coeff < 0:
                final += "-"
            elif coeff > 0 and i != 0:
                final += "+"
            if abs(coeff) != 1:
                final += str(abs(poly[i]))
            for j in range(len(explist[i])):
                tempexponent = explist[i][j]
                if tempexponent != 0:
                    final += varlist[j]
                    if j != 1:
                        final += "^%d" %(j)
        return final

    def __add__(self, other):
        if isinstance(other, int):
            poly = self.Polynomial[:]
            poly[0] += other
            return Polynomial("", poly, self.varlist, self.degree, self.explist)
        elif isinstance(other, Polynomial):
            a = self.varlist
            b = other.getVarlist()
            if a == b:
                if len(self.Polynomial) > len(other.getPoly()):
                    poly1 = self.Polynomial
                    poly2 = other.getPoly()
                    end1 = len(poly2)
                    end2 = len(poly1)
                    deg = self.degree
                else:
                    poly2 = self.Polynomial
                    poly1 = other.getPoly()
                    end1 = len(poly2)
                    end2 = len(poly1)
                    deg = other.getDegree()
                polynomial = []
                for i in range(end1):
                    polynomial.append(poly1[i] + poly2[i])
                for i in range(end1,end2):
                    polynomial.append(poly1[i])
                return Polynomial("", polynomial, a, deg)
            sharedvarlist = list(set(a) & (set(b)))
            sno_vars = list(set(a) - set(b)) #variables in self but not other
            sno_vars.sort()
            ons_vars = list(set(b) - set(a)) #variables in other but not self
            ons_vars.sort()
            newvarlist = list(set(a) | set(b))
            newvarlist.sort()
            sno_vars_positions = [] #positions in the new varlist
            for i in sno_vars:
                sno_vars_positions.append(bsearch(newvarlist, i))
            ons_vars_positions = [] #positions in the new varlist
            for i in ons_vars:
                ons_vars_positions.append(bsearch(newvarlist, i))
            self_vars_positions = []
            for i in a:
                self_vars_positions.append(bsearch(newvarlist, i))
            other_vars_positions = []
            for i in b:
                other_vars_positions.append(bsearch(newvarlist, i))
            newdegree = max(self.degree, other.getDegree())
            newvarnum = len(newvarlist) #new Polynomial # of variables
            poly1 = self.Polynomial
            poly2 = other.getPoly()
            explist1 = self.explist
            explist2 = other.getExplist()
            newpoly = [] #new Polynomial list
            newexplist = makeExpVec(newvarnum, newdegree) #list of new expvectors
            for i in range(nCk(newdegree + newvarnum, newvarnum)):
                check = True
                if inone(sno_vars_positions, newexplist[i]):
                    copy = []
                    for j in other_vars_positions:
                        copy.append(newexplist[i][j])
                    if copy in explist2:
                        check = False
                        d = grevsearch(explist2, copy)
                        newpoly.append(poly2[d])
                if inone(ons_vars_positions, newexplist[i]):
                    copy = []
                    for j in self_vars_positions:
                        copy.append(newexplist[i][j])
                    if copy in explist1:
                        check = False
                        c = grevsearch(explist1, copy)
                        try:
                            newpoly[i] += poly1[c]
                        except IndexError:
                            newpoly.append(poly1[c])
                if check:
                    newpoly.append(0)
            return Polynomial("", newpoly, newvarlist, newdegree, newexplist)
        else:
            return NotImplemented

    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            poly = self.Polynomial[:]
            poly[0] -= other
            return Polynomial("", poly, self.varlist, self.degree, self.explist)
        elif isinstance(other, Polynomial):
            poly = other.getPoly()[:]
            for i in range(len(poly)):
                poly[i] *= -1
            return self.__add__(Polynomial("", poly, other.getVarlist(),other.getDegree(),other.getExplist()))
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int):
            poly = self.Polynomial[:]
            for i in poly:
                i *= other
            return Polynomial("", poly, self.getVarlist(), self.getDegree(), self.getExplist())
        elif isinstance(other, Polynomial):
            if other.isMonomial():
                coeff = other.getPoly()[other.getloclist()[0]]
                expvec = other.getexpNonZero()[0]
                degree = other.getDegree()
                final = multMonomial(self,other.getVarlist(),coeff,expvec,degree)
                return final
            else:
                final = 0
                loclist1 = other.getloclist()
                varlist1 = other.getVarlist()
                poly1 = other.getPoly()
                expveclist = other.getExplist()
                for i in loclist1:
                    coeff = poly1[i]
                    expvec = expveclist[i]
                    degree = sum(expvec)
                    temp = multMonomial(self,varlist1,coeff,expvec,degree)
                    final += temp
                return final
        else:
            return NotImplemented

    def __rmul__(self,other):
        return self.__mul__(other)

    def derive(self, variable):
        varlist = self.getVarlist()[:]
        if variable not in varlist:
            return 0
        position = varlist.index(variable)
        loclist = self.getloclist()[:]
        poly = self.getPoly()[:]
        expvectemp = self.getexpNonZero()
        expvectemp2 = []
        for i in expvectemp:
            temp = []
            for j in i:
                temp.append(j)
            expvectemp2.append(temp)
        coefflist = []
        expvec = []
        for counter, i in enumerate(loclist):
            if expvectemp2[counter][position] != 0:
                coefflist.append(poly[i] * expvectemp2[counter][position])
                expvec.append(expvectemp2[counter])
                expvectemp2[counter][position] -= 1
        deleteVar = True
        for i in expvec:
            if i[position] != 0:
                deleteVar = False
                break
        if deleteVar:
            varlist.pop(position)
            for i in range(len(expvec)):
                expvec[i].pop(position)
        varnum = len(varlist)
        newdegree = 0
        newloclist = []
        for i in expvec:
            if sum(i) > newdegree:
                newdegree = sum(i)
            newloclist.append(rPolylocate(i))
        newpoly = []
        for i in range(nCk(varnum+newdegree,newdegree)):
            if i in newloclist:
                newpoly.append(coefflist[newloclist.index(i)])
            else:
                newpoly.append(0)
        if varlist == []:
            return newpoly[0]
        return Polynomial("",newpoly,varlist,newdegree)

    def roots(self):
        """
        Returns a list of all complex and real roots.
        Calculated by the Aberth method. Kind of working
        """
        varlist = self.getVarlist()
        if len(varlist) != 1:
            return TooManyVariables
        poly = self.getPoly()
        loclist = self.getloclist()
        last_pos = loclist[len(loclist)-1]
        degree = self.getDegree()
        D = self.derive(varlist[0])
        maxlength = 0
        #calculates maximum abs of roots
        for n, i in enumerate(reversed(loclist)):
            temp = (abs(Fraction(poly[i],poly[last_pos])))**Fraction(1,n+1)
            if n == len(loclist) - 1:
                temp = (abs(Fraction(poly[i],2*poly[last_pos])))**Fraction(1,n+1)
            if maxlength < temp:
                maxlength = temp
        maxlength *= 2
        returnset = set([])
        for i in range(5):
            guess = []
            phi = random.uniform(0,2*cmath.pi)
            for i in range(degree):
                radius = random.uniform(0,maxlength)
                temp = radius * cmath.exp(1j*phi*i)
                guess.append(temp)
                for i in range(50):
                    guess = Aberth(guess, self, D)
            for i in guess:
                returnset.add(i)
        final = list(returnset)
        """returnlst = []
        toadd = True
        for i in range(len(final)):
            for j in range(i+1,len(final)):
                if(abs(final[i]-final[j]) < 10**-25):
                    toadd = False
            if(toadd):
                returnlst.append(final[i])"""
        return final

    def getVarlist(self):
        "Gets the list of variables in a Polynomial"
        return self.varlist

    def getDegree(self):
        "Gets the degree of the Polynomial"
        return self.degree

    def getPoly(self):
        "Gets the ordered list of coefficients"
        return self.Polynomial

    def isMonomial(self):
        "Returns True if the polynomial has one term, False if it has more"
        return self.Monomial



def DivisionWithRemainder(dividend, divisors):
    """divides the dividend by the divisor(s) with remainder. dividend should be
    a polynomial, divisor(s) should be a list of polynomials. returns a
    list of polynomials a_i corresponding to the divisors f_i
    for multivariable polynomials, non unique remainder"""


def Aberth(L, polynomial, derivative):
    final = []
    for i in L:
        for j in L:
            tempsum = 0
            if i != j:
                tempsum += 1/(i - j)
        try:
            tempfrac = polynomial[i]/derivative[i]
        except TypeError:
            tempfrac = polynomial[i]/(derivative)
        offset = tempfrac/(1-tempfrac*tempsum)
        final.append(i-offset)
    return final

def MonomialDivisible(expvec1, expvec2):
    """returns true if the dividend = (variables)**(expvec1)
    is divisible by the divisor = (variables)**(expvec2). assumes
    monomials have the same variables"""
    returnbool = True
    for i in range(len(expvec1)):
        if(expvec1[i] - expvec2[i] < 0):
            returnbool = False
    return returnbool

def DivideMonomial(coeff1, expvec1, coeff2, expvec2, varlist):
    """divides monomial a by monomial b, where
    a = coeff1*(variables)**(expvec1) and b = coeff2*(variables)**(expvec2).
    assumes monomials have the same variables, which are given in varlist."""
    qexpvec = []
    for i in range(len(expvec1)):
        temp = expvec1[i] - expvec2[i]
        if(temp < 0):
            raise MonomialNotDivisible
        qexpvec.append(temp)
    qcoeff = coeff1/coeff2
    #make the monomial a polynomial now
    

def MakeMonomial(coeff, expvec, varlist):
    #makes a polynomial from the coeff, expvec, and varlist
    pass

def multMonomial(poly, varlist, coeff, expvec, degree):
    "Multiplies monomials"
    var_list1 = poly.getVarlist()
    poly1 = poly.getPoly()[:]
    loclist1 = poly.getloclist()
    ExpNonEmpty1 = poly.getexpNonZero()
    for i in range(len(poly1)):
        poly1[i] *= coeff
    newvarlist = list(set(var_list1) | set(varlist))
    newvarlist.sort()
    self_vars_positions = []
    for i in var_list1:
        self_vars_positions.append(bsearch(newvarlist, i))
    other_vars_positions = []
    for i in varlist:
        other_vars_positions.append(bsearch(newvarlist, i))
    newdegree = poly.getDegree() + degree
    newvarnum = len(newvarlist)
    newexplist = makeExpVec(newvarnum, newdegree)
    newexpnonempty = [] #new list of powers with non zero coeff
    for i in ExpNonEmpty1:
        newexpnonempty.append([0]*newvarnum)
    for counter,i in enumerate(newexpnonempty):
        for j in range(len(i)):
            if j in self_vars_positions:
                i[j] += ExpNonEmpty1[counter][j]
            if j in other_vars_positions:
                i[j] += expvec[j]
    grevlexsort(newexpnonempty)
    counter3 = 0
    newpoly = []
    for i in newexplist:
        if i in newexpnonempty:
            newpoly.append(poly1[loclist1[counter3]])
            counter3 += 1
        else:
            newpoly.append(0)
    return Polynomial("",newpoly,newvarlist,newdegree,newexplist)

def inone(positionlst, L):
    for i in positionlst:
        if L[i] != 0:
            return False
    return True

def makeExpVec(varnum, degree):
    """
    Makes the grevlex sorted list of exp vectors for a certain variable number
    and certain degree
    """
    explist = [] #temp list of partitions
    for i in range(varnum+1):
        explist += list(revlex_partitions(degree, i))
    temp2 = []
    newexplist = []
    for i in explist:
        while len(i) < varnum:
            i.append(0)
        temp2 += list(itertools.permutations(i))
    for i in temp2:
        thingy = list(i)
        if thingy in newexplist:
            continue
        newexplist.append(thingy)
    grevlexsort(newexplist)
    return newexplist

def bsearch(lst, item):
	low = 0
	high = len(lst) - 1
	while low <= high:
		middle = int((low + high)/2)
		if item == lst[middle]:
			return middle
		elif item > lst[middle]:
			low = middle + 1
		else:
			high = middle -1
	return -1

def rPolylocate(expL):
    #calculates the location of an exponent vector
    #in a grevlex ordered list
    if expL == []:
        return 0
    temp = nCk(sum(expL) + len(expL) - 1, len(expL))
    expL.pop(len(expL)-1)
    return temp + rPolylocate(expL)

def revlex_partitions(n, k):
    #calculates k place partitions of n. returns an iterable
    if n == 0:
        yield []
    if n <= 0:
        return
    for p in revlex_partitions(n-1, k):
        if len(p) == 1 or (len(p) > 1 and p[-1] < p[-2]):
            p[-1] += 1
            if len(p) <= k:
                yield p[:]
            else:
                yield p
            p[-1] -= 1
        p.append(1)
        if len(p) <= k:
            yield p[:]
        else:
            yield p
        p.pop()

def grevsearch(lst, item):
    #modified binary search to work with grevlex sorted lists
    low = 0
    high = len(lst) - 1
    while low <= high:
    	middle = int((low + high)/2)
    	if item == lst[middle]:
    		return middle
    	elif grevlexhelper(lst[middle], item):
    		low = middle + 1
    	else:
    		high = middle -1
    return -1

def grevlexsort(lst):
    """
    Perform insertion sort on the list.
    Sorts by grevlex order
    """
    for i in range(1, len(lst)):
        elt = lst[i]
        j = i-1
        # if not at the start of the list and items are out of order
        while (j >= 0) and grevlexhelper(elt,lst[j]):
            lst[j+1] = lst[j]
            j=j-1
        lst[j+1] = elt

def grevlexhelper(L1, L2):
    """
    Returns Frue if L1 < L2 and False if L1 > L2
    Decides using grevlex
    """
    a = sum(L1)
    b = sum(L2)
    if a < b:
        return True
    elif a > b:
        return False
    else:
        for i in range(len(L1)-1, -1, -1):
            if L1[i] < L2[i]:
                return False
            elif L1[i] > L2[i]:
                return True

def doublegrevlexsort(lst1, lst2):
    """
    Sorts both lst1 and lst2 according to the grevlex sorted order of lst1
    requires that len(lst1) == len(lst2)
    """
    for i in range(1, len(lst1)):
        elt = lst1[i]
        elt2 = lst2[i]
        j = i-1
        # if not at the start of the list and items are out of order
        while (j >= 0) and grevlexhelper(elt,lst1[j]):
            lst1[j+1] = lst1[j]
            lst2[j+1] = lst2[j]
            j=j-1
        lst1[j+1] = elt
        lst2[j+1] = elt2