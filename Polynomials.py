from math import *
from MoreMath import *
from PolynomialExceptions import *
import itertools
import fractions
import random
import cmath

#redoing format of polynomial to no longer use a full exp list

class Polynomial(object):

    def __init__(self, string, polynomial = None, varlist = None, NewExpLst = None, paddingvars = None):
        """
        Polynomial constructor.
        Takes either a string or a list of coefficients (polynomial), a list of variables, and
        a list of exponents.
        Padding variables are used to add dummy variables to a polynomial, 
        which can be useful for various things such as division
        """
        if polynomial == None:
            polynomial = []
        if varlist == None:
            varlist = []
        if NewExpLst == None:
            NewExpLst = []
        if paddingvars == None:
            paddingvars = []
        if string == "" and (polynomial == [] or varlist == [] or NewExpLst == []):
            print(NewExpLst)
            print(polynomial)
            print(varlist)
            raise InsufficientInputError
        if string != "" and (polynomial != [] or varlist != [] or NewExpLst != []):
            raise ConflictingInputError #can't take both a string and other polynomial info
        self.Polynomial = polynomial[:]
        self.varlist = varlist[:]
        self.NewExpLst = NewExpLst[:]
        #finds the variables and makes a sorted list of them
        if string != "":
            for i in string:
                if i.isalpha() and i not in self.varlist:
                    self.varlist.append(i)
        disjointvars = []
        for i in paddingvars:
            if not(i in varlist):
                self.varlist.append(i)
                disjointvars.append(i)
        self.varlist.sort()
        self.varnum = len(self.varlist)
        self.degree = 0
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
                    elif counter == 0:
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
        else:
            if(len(self.NewExpLst) != 0) and (len(self.varlist) != 0):
                if len(self.NewExpLst[0]) != len(self.varlist):
                    padloc = []
                    for i in disjointvars:
                        padloc.append(self.varlist.index(i))
                    new = []
                    for i in self.NewExpLst:
                        temp = []
                        counter = 0
                        for j in range(len(self.varlist)):
                            if j in padloc:
                                temp.append(0)
                            else:
                                temp.append(i[counter])
                                counter += 1
                        new.append(temp)
                    self.NewExpLst = new
            doublegrevlexsort(self.NewExpLst,self.Polynomial)
            for i in self.NewExpLst:
                tempsum = sum(i)
                if(tempsum > self.degree):
                    self.degree = tempsum
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
            if abs(coeff) != 1 or inone(range(len(explist[i])),explist[i]): #inone checks if this is the constant term
                final += str(abs(poly[i]))
            for j in range(len(explist[i])):
                tempexponent = explist[i][j]
                if tempexponent != 0:
                    final += varlist[j]
                    if tempexponent != 1:
                        final += "^%d" %(tempexponent)
        return final

    def __add__(self, other):
        if isinstance(other, int):
            poly = self.Polynomial[:]
            poly[0] += other
            return Polynomial("", poly, self.varlist, self.NewExpLst)
        elif isinstance(other, Polynomial):
            a = self.varlist
            b = other.getVarlist()
            explst = self.NewExpLst
            oexplst = other.NewExpLst[:]
            spoly = self.Polynomial
            opoly = other.Polynomial[:]
            newvarlist = a
            if a != b:
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
                newvarnum = len(newvarlist) #new Polynomial # of variables
                poly1 = self.Polynomial
                poly2 = other.Polynomial
                snewexplst = self.NewExpLst
                onewexplst = other.NewExpLst
                spaddedexplst = []
                opaddedexplst = []
                for i in range(len(poly1)):
                    expvec = []
                    for j in range(newvarnum):
                        if(j in ons_vars_positions):
                            expvec.append(0)
                        else:
                            expvec.append(snewexplst[i][self_vars_positions.index(j)])
                    spaddedexplst.append(expvec)
                for i in range(len(poly2)):
                    expvec = []
                    for j in range(newvarnum):
                        if(j in sno_vars_positions):
                            expvec.append(0)
                        else:
                            expvec.append(onewexplst[i][other_vars_positions.index(j)])
                    opaddedexplst.append(expvec)
                explst = spaddedexplst
                oexplst = opaddedexplst
            polynomial = []
            newpolyexplst = []
            for i in range(len(explst)):
                temp = 0
                if(explst[i] in oexplst):
                    index = oexplst.index(explst[i])
                    temp += spoly[i] + opoly[index]
                    del opoly[index]
                    del oexplst[index]
                else:
                    temp += spoly[i]
                if temp != 0:
                    polynomial.append(temp)
                    newpolyexplst.append(explst[i])
            for i in range(len(oexplst)):
                polynomial.append(opoly[i])
                newpolyexplst.append(oexplst[i])
            if(len(polynomial) == 0):
                return 0
            return Polynomial("", polynomial, newvarlist, newpolyexplst)
        else:
            return NotImplemented
    
    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            poly = self.Polynomial[:]
            poly[0] -= other
            return Polynomial("", poly, self.varlist, self.NewExpLst)
        elif isinstance(other, Polynomial):
            poly = other.getPoly()[:]
            for i in range(len(poly)):
                poly[i] *= -1
            return self.__add__(Polynomial("", poly, other.getVarlist(),other.NewExpLst))
        else:
            return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, int):
            poly = self.Polynomial[:]
            for i in poly:
                i *= other
            return Polynomial("", poly, self.getVarlist(), self.NewExpLst)
        elif isinstance(other, Polynomial):
            if other.isMonomial():
                coeff = other.getPoly()[0]
                expvec = other.NewExpLst[0]
                final = multMonomial(self,other.getVarlist(),coeff,expvec)
                return final
            else:
                final = 0
                varlist1 = other.getVarlist()
                poly1 = other.getPoly()
                expveclist = other.NewExpLst
                for i in range(len(poly1)):
                    coeff = poly1[i]
                    expvec = expveclist[i]
                    temp = multMonomial(self,varlist1,coeff,expvec)
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
        poly = self.getPoly()[:]
        expveclst = self.NewExpLst
        coefflist = []
        newexpveclst = []
        deleteVar = True
        for i in range(len(poly)):
            if expveclst[i][position] != 0:
                coefflist.append(poly[i] * expveclst[i][position])
                tempexpvec = expveclst[i][:]
                tempexpvec[position] -= 1
                newexpveclst.append(tempexpvec)
                if(expveclst[i][position] != 0):
                    deleteVar = False
        if deleteVar:
            varlist.pop(position)
            for i in range(len(newexpveclst)):
                newexpveclst[i].pop(position)
        if varlist == []:
            return coefflist[0]
        return Polynomial("",coefflist,varlist,newexpveclst)
    
    def __eq__(self, other):
        if(isinstance(other, int)): #for this to work polynomial needs to be the left of equality???
            return (len(self.Polynomial) == 1) and (self.Polynomial[0] == other)
        if(isinstance(other,self.__class__)):
            if(self.varlist != other.varlist):
                return False
            sexpveclst = self.NewExpLst
            oexpveclst = other.NewExpLst
            spoly = self.Polynomial
            opoly = other.Polynomial
            if(len(sexpveclst) != oexpveclst):
                return False
            for i in range(len(spoly)):
                if (spoly[i] != opoly[i]) or (sexpveclst[i] != oexpveclst[i]):
                    return False
            return True

    def roots(self):
        """
        Returns a list of all complex and real roots.
        Calculated by the Aberth method. Kind of working,
        I miss some roots every time
        """
        varlist = self.getVarlist()
        if len(varlist) != 1:
            return TooManyVariables
        poly = self.getPoly()
        lastcoeff = poly[len(poly)-1]
        degree = self.getDegree()
        D = self.derive(varlist[0])
        maxlength = 0
        #calculates maximum abs of roots
        for n,i in enumerate(reversed(poly)):
            temp = (abs(Fraction(i,lastcoeff)))**Fraction(1,n+1)
            if n == len(poly) - 1:
                temp = (abs(Fraction(i,2*lastcoeff)))**Fraction(1,n+1)
            if maxlength < temp:
                maxlength = temp
        maxlength *= 2
        guess = []
        phi = random.uniform(0,2*cmath.pi)
        for i in range(degree):
            radius = random.uniform(0,maxlength)
            temp = radius * cmath.exp(1j*phi*i)
            guess.append(temp)
        for i in range(30):
            guess = Aberth(guess,self,D)
        """returnset = set([])
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
        returnlst = []
        toadd = True
        for i in range(len(final)):
            for j in range(i+1,len(final)):
                if(abs(final[i]-final[j]) < 10**-25):
                    toadd = False
            if(toadd):
                returnlst.append(final[i])"""
        return guess

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
    varlist1 = []
    varlist2 = []
    for i in divisors:
        for j in i.varlist:
            if not(j in varlist1):
                varlist1.append(j)
    for i in dividend.varlist:
        varlist2.append(i)
    if(varlist1 != varlist2):
        for i in varlist2:
            if not (i in varlist1):
                varlist1.append(i)
        for i in range(len(divisors)):
            divisors[i] = Polynomial("",divisors[i].Polynomial,divisors[i].varlist,divisors[i].NewExpLst,varlist1)
    p = Polynomial("",dividend.Polynomial, dividend.varlist, dividend.NewExpLst,varlist1)
    returnlst = [0]*len(divisors)
    remainder = 0
    while p != 0: 
        counter = 0
        divisionoccurred = False    
        coeff1 = p.Polynomial[len(p.Polynomial)-1]
        expvec1 = p.NewExpLst[len(p.NewExpLst)-1]
        varlist = p.varlist
        while counter < len(divisors) and (not divisionoccurred):
            coeff2 = divisors[counter].Polynomial[len(divisors[counter].Polynomial)-1]
            expvec2 = divisors[counter].NewExpLst[len(divisors[counter].NewExpLst)-1]
            tempdivide = DivideMonomial(coeff1,expvec1,coeff2,expvec2,varlist)
            if not (isinstance(tempdivide,True.__class__)):
                returnlst[counter] += tempdivide
                p -= tempdivide * divisors[counter]
                divisionoccurred = True
            else:
                counter += 1
        if not divisionoccurred:
            temppoly = Polynomial("", [coeff1],varlist, [expvec1])
            remainder += temppoly
            p -= temppoly
    return returnlst,remainder

def DivideMonomial(coeff1, expvec1, coeff2, expvec2, varlist):
    """divides monomial a by monomial b, where
    a = coeff1*(variables)**(expvec1) and b = coeff2*(variables)**(expvec2).
    assumes monomials have the same variables, which are given in varlist.
    Returns false if not divisible"""
    qexpvec = []
    print(expvec1)
    print(expvec2)
    for i in range(len(expvec1)):
        temp = expvec1[i] - expvec2[i]
        if(temp < 0):
            return False #not divisible. The fact that I can return a bool here is insane
        qexpvec.append(temp)
    qcoeff = coeff1/coeff2
    return Polynomial("",[qcoeff],varlist,[qexpvec])

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

def multMonomial(poly, varlist, coeff, expvec):
    "Multiplies monomials, helper function for polynomial multiplication"
    var_list1 = poly.getVarlist()
    poly1 = poly.getPoly()[:]
    explst = poly.NewExpLst
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
    newexpnonempty = []
    for i in explst:
        newexpnonempty.append([0]*len(newvarlist))
    for counter,i in enumerate(newexpnonempty):
        for j in range(len(i)):
            if j in self_vars_positions:
                i[j] += explst[counter][self_vars_positions.index(j)]
            if j in other_vars_positions:
                i[j] += expvec[other_vars_positions.index(j)]
    return Polynomial("",poly1,newvarlist,newexpnonempty)

def inone(positionlst, L):
    """
    Checks if elements in L at positions in the positionlst 
    are all 0. If all are 0, returns true, otherwise false
    """
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