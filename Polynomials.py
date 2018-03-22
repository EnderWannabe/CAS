from math import *
from MoreMath import *
from PolynomialExceptions import *
import itertools
import fractions
import random
import cmath

class Polynomial(object):

    def __init__(self, string, coefflst = None, expnonempty = None,
                 varlist = None, degree = None):
        #initializing to empty in the case when only string is passed in
        if varlist == None:
            varlist = []
        if degree == None:
            degree = 0
        if coefflst == None:
            coefflst = []
        if expnonempty == None:
            expnonempty = []
        #errors in the case that inputs to constructor conflict
        if string == "" and (coefflst == [] or varlist == []
                            or expnonempty == []):
            raise InsufficientInputError
        if string != "" and (coefflst != [] or varlist != []
                            or expnonempty != []):
            raise ConflictingInputError
        self.varlist = varlist
        self.degree = degree
        self.explist = []
        self.coefflst = coefflst
        self.ExpNonEmpty = expnonempty
        #finds the variables and makes a sorted list of them
        if string != "":
            for i in string:
                if i.isalpha() and i not in self.varlist:
                    self.varlist.append(i)
        self.varlist.sort()
        self.varnum = len(self.varlist)
        if string != "":
            #finds coefficients and corresponding exponent vectors
            plusminus = ["-","+"]
            tempexplist = []
            tempcoefflst = []
            for counter,i in enumerate(string):
                if string[counter - 1] in plusminus or (counter == 0 and string[0] != "-"):
                    if i.isdigit():
                        str_counter = counter + 1
                        str_temp = i
                        while str_counter < len(string):
                            if string[str_counter].isdigit():
                                str_temp += string[str_counter]
                                str_counter += 1
                            else:
                                break
                        value = int(str_temp)
                        if counter != 0:
                            if string[counter - 1] == "-":
                                value *= -1
                        if counter < len(string) - 2:
                            if string[counter + 1] == "/":
                                value /= int(string[counter+2])
                    elif string[counter-1] == "+" or counter == 0:
                        value = 1
                    else:
                        value = -1
                    tempcoefflst.append(value)
                    expvec = []
                    #makes a list of exponents
                    for j in range(self.varnum):
                        expvec.append(0)
                    j = counter
                    while True:
                        if j == len(string) or string[j] in ["+"," ","-"]:
                            break
                        if string[j].isalpha():
                            if j+2 < len(string):
                                if string[j+2].isdigit() and string[j+1] == "^":
                                    k = j + 2
                                    tempstring = ""
                                    while True:
                                        if k == len(string) or not string[k].isdigit():
                                            break
                                        tempstring += string[k]
                                        k += 1
                                    expvec[bsearch(self.varlist, string[j])] = int(tempstring)
                                else:
                                    expvec[bsearch(self.varlist, string[j])] = 1
                            else:
                                expvec[bsearch(self.varlist, string[j])] = 1
                        j += 1
                    tempexplist.append(expvec)
            #finds the degree of the polynomial
            #and the locations of the terms in the grevlex ordering
            for i in tempexplist:
                if sum(i) > self.degree:
                    self.degree = sum(i)
            self.coefflst = modifiedgrevlexSort(tempexplist, tempcoefflst)
            self.ExpNonEmpty = tempexplist
        if self.degree == 0:
            for i in self.ExpNonEmpty:
                if sum(i) > self.degree:
                    self.degree = sum(i)
        self.Monomial = False
        if len(self.coefflst) == 1:
            self.Monomial = True

    #evaluates the polynomial at a given point
    def __getitem__(self, L):
        varlist = self.getVarlist()
        if len(varlist) != 1:
            if len(L) != len(varlist):
                return KeyError
            if not isinstance(L, list):
                return TypeError
            coefflist = self.getCoefflist()
            nonempty = self.getexpNonZero()
            final = 0
            for i in range(len(coefflist)):
                temp = coefflist[i]
                for j in range(len(nonempty[i])):
                    temp *= L[j] ** nonempty[i][j]  #evaluates term by term
                final += temp                       #this is the sum
            return final
        else:
            if not (isinstance(L, int) or isinstance(L, list) or isinstance(L,type(1j))):
                return TypeError
            if isinstance(L, int) or isinstance(L,type(1j)):
                coefflist = self.getCoefflist()
                nonempty = self.getexpNonZero()
                final = 0
                for counter, i in enumerate(coefflist):
                    temp = i * (L ** nonempty[counter][0])
                    final += temp
                return final
            elif isinstance(L, list):
                coefflist = self.getCoefflist()
                nonempty = self.getexpNonZero()
                final = 0
                for counter, i in enumerate(coefflist):
                    temp = i * (L[0] ** nonempty[counter][0])
                    final += temp
                return final

    #turns polynomial into a string
    def __str__(self):
        varlist = self.getVarlist()
        coefflist = self.getCoefflist()
        nonempty = self.getexpNonZero()
        final = ""
        for counter, i in enumerate(coefflist):
            if i < 0:   #append "+" if positive, "-" if negative
                final += "-"
            elif i > 0 and counter != 0:
                final += "+"
            if abs(i) == 1:
                if nonempty[counter] == [0]*len(varlist):
                    final += "1"
            else:
                final += str(abs(i))
            for counter2, j in enumerate(nonempty[counter]):
                if j != 0:
                    final += varlist[counter2]
                    if j != 1:
                        final += "^%d" %(j)
        return final

    def __add__(self, other):
        if isinstance(other, int):
            coefflist = self.getCoefflist()
            nonempty = self.getexpNonZero()
            varlist = self.getVarlist()
            constantcheck = True #checks if the polynomial has a constant term
            for i in range(len(varlist)):
                if nonempty[0][i] != 0:
                    constantcheck = False
            if constantcheck:
                coefflist[0] += other
            else:
                templist = []
                for i in range(len(varlist)):
                    templist.append(0)
                nonempty.insert(0,templist)
                coefflist.insert(0,other)
            return Polynomial("", coefflist, nonempty, varlist, self.degree)
        elif isinstance(other, Polynomial):
            a = self.varlist
            b = other.getVarlist()
            newdegree = max(self.degree, other.getDegree())
            if a == b:
                poly1 = self.getCoefflist()[:]
                poly2 = other.getCoefflist()
                explst1 = self.getexpNonZero()[:]
                explst2 = other.getexpNonZero()
                for i in range(len(poly2)):
                    if explst2[i] in explst1: #if terms combine
                        poly1[explst1.index(explst2[i])] += poly2[i]
                    else: #if terms do not combine
                        poly1.append(poly2[i])
                        explst1.append(explst2[i])
                newcoefflst = modifiedgrevlexSort(explst1, poly1) #sort
                return Polynomial("", newcoefflst, explst1, a, newdegree)
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
            newvarnum = len(newvarlist) #new Polynomial # of variables
            coefflst1 = self.getCoefflist()[:]
            coefflst2 = other.getCoefflist()[:]
            explst1 = self.getexpNonZero()[:]
            explst2 = other.getexpNonZero()[:]
            #explst1 padded with 0 where the varliables in other are
            newexplst1 = []
            for i in explst1:
                newexpvec = []
                counter = 0
                for j in range(newvarnum):
                    if j in ons_vars_positions:
                        newexpvec.append(0)
                    else:
                        newexpvec.append(i[counter])
                        counter += 1
                newexplst1.append(newexpvec)
            grevlexsort(newexplst1)
            #explst2 padded with 0 where the varliables in self are
            newexplst2 = []
            for i in explst2:
                newexpvec = []
                counter2 = 0
                for j in range(newvarnum):
                    if j in sno_vars_positions:
                        newexpvec.append(0)
                    else:
                        newexpvec.append(i[counter2])
                        counter2 += 1
                newexplst2.append(newexpvec)
            grevlexsort(newexplst1)
            newcoefflst = []
            newexplst = []
            counter1 = 0 #position in newexplst1
            counter2 = 0 #position in newexplst2
            while counter1 < len(newexplst1) or counter2 < len(newexplst2):
            #while not at the end of both lists
                if counter1 < len(newexplst1) and counter2 < len(newexplst2):
                    #if the exponents are the same
                    if newexplst1[counter1] == newexplst2[counter2]:
                        newcoefflst.append(coefflst1[counter1]+coefflst2[counter2])
                        newexplst.append(newexplst1[counter1])
                        counter1 += 1
                        counter2 += 1
                    elif grevlexhelper(newexplst1[counter1], newexplst2[counter2]):
                        #preserving grevlex order
                        newcoefflst.append(coefflst1[counter1])
                        newexplst.append(newexplst1[counter1])
                        counter1 += 1
                    else:
                        newcoefflst.append(coefflst2[counter2])
                        newexplst.append(newexplst2[counter2])
                        counter2 += 1
                elif counter1 < len(newexplst1):
                    newcoefflst.append(coefflst1[counter1])
                    newexplst.append(newexplst1[counter1])
                    counter1 += 1
                elif counter2 < len(newexplst2):
                    newcoefflst.append(coefflst2[counter2])
                    newexplst.append(newexplst2[counter2])
                    counter2 += 1
            return Polynomial("", newcoefflst, newexplst, newvarlist, newdegree)
        else:
            return NotImplemented

    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            tempint = other * -1
            return self.__add__(tempint)
        elif isinstance(other, Polynomial):
            tempPoly = other * -1 #needs to be other * -1
            return self.__add__(tempPoly)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other,float):
            coeff = self.getCoefflist()[:]
            for i in range(len(coeff)):
                coeff[i] *= other
            return Polynomial("", coeff, self.getexpNonZero(), self.getVarlist(),
                              self.getDegree())
        elif isinstance(other, Polynomial):
            if other.isMonomial():
                coeff = other.getCoefflist()[0]
                expvec = other.getexpNonZero()[0]
                final = multMonomial(self,other.getVarlist(),coeff,expvec)
                return final
            else:
                final = 0
                varlist1 = other.getVarlist()
                coefflst1 = other.getCoefflist()
                expveclist = other.getexpNonZero()
                for i in range(len(expveclist)):
                    coeff = coefflst1[i]
                    expvec = expveclist[i]
                    temp = multMonomial(self,varlist1,coeff,expvec)
                    final += temp
                return final
        else:
            return NotImplemented

    def __rmul__(self,other):
        return self.__mul__(other)

    def derive(self, variable):
        """
        derives the polynomial with respect to the variable passed in
        """
        varlist = self.getVarlist()[:]
        if variable not in varlist:
            return 0
        position = varlist.index(variable)
        coefflst = self.getCoefflist()[:]
        expvecold = self.getexpNonZero()
        expvec = []
        for i in expvecold: #since copying doesn't copy inner lists
            expvec.append(i[:])
        deletelist = []
        deleteVarList = [True] * len(varlist)
        for i in range(len(coefflst)):
            if expvec[i][position] == 0:
                deletelist.append(i)
            else:
                coefflst[i] *= expvec[i][position]
                expvec[i][position] -= 1
        for i in range(len(deletelist)-1,-1,-1):
            coefflst.pop(deletelist[i])
            expvec.pop(deletelist[i])
        for i in expvec:
            for counter, j in enumerate(i):
                if j != 0:
                    deleteVarList[counter] = False
            if deleteVarList == [False] * len(varlist):
                break
        for i in range(len(varlist)-1,-1,-1):
            if deleteVarList[i]:
                for j in range(len(expvec)):
                    expvec[j].pop(i)
                varlist.pop(i)
        if len(varlist) == 0:
            varlist.append(None)
            expvec[0].append(0)
        return Polynomial("",coefflst,expvec,varlist)

    def makeExpVec(self):
        """
        Makes the grevlex sorted list of all possible exp vectors for a certain
        variable number and certain degree
        """
        varnum = len(self.getVarlist())
        degree = self.getDegree()
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

    def roots(self):
        """
        Returns a list of all complex and real roots.
        Calculated by the Aberth method.
        Works now!
        """
        guess = makeGuess(self)
        D = self.derive(self.getVarlist()[0])
        counter = 0
        while True:
            off = True
            newguess = []
            for i in guess:
                for j in guess:
                    tempsum = 0
                    if i != j:
                        tempsum += 1/(i - j)
                try:
                    tempfrac = (self[i])/(D[i])
                except TypeError:
                    tempfrac = self[i]/D
                offset = tempfrac/(1-tempfrac*tempsum)
                newguess.append(i-offset)
                if abs(offset.real) > 0.0000001 or abs(offset.imag) > 0.00000001:
                    off = False
            guess = newguess
            if off or counter == 1000:
                break
            counter += 1
        print(counter)
        return guess

    def getVarlist(self):
        "Gets the list of variables in a Polynomial"
        return self.varlist

    def getDegree(self):
        "Gets the degree of the Polynomial"
        return self.degree

    def isMonomial(self):
        "Returns True if the polynomial has one term, False if it has more"
        return self.Monomial

    def getexpNonZero(self):
        "Returns list of powers in the polynomial"
        return self.ExpNonEmpty

    def getCoefflist(self):
        "Returns a list of non zero coefficients"
        return self.coefflst

def makeGuess(polynomial):
    """
    Generates a list of guesses for roots
    """
    varlist = polynomial.getVarlist()[:]
    if len(varlist) != 1:
        raise TooManyVariables
    poly = polynomial.getCoefflist()[:]
    loclist = polynomial.getexpNonZero()[:]
    last_pos = poly[len(poly)-1]
    degree = polynomial.getDegree()
    maxlength = 0
    #calculates maximum norm of roots
    for n,i in enumerate(reversed(poly)):
        temp = (abs(i/last_pos))**Fraction(1,n+1)
        if n+1 == len(loclist):
            temp = (abs(i/2*last_pos))**Fraction(1,n+1)
        if maxlength < temp:
            maxlength = temp
    maxlength *= 2
    guess = []
    for i in range(degree):
        phi = random.uniform(0,2*cmath.pi)
        radius = random.uniform(0,maxlength)
        temp = radius * cmath.exp(1j*phi)
        guess.append(temp)
    return guess

def multMonomial(poly, varlist, coeff, expvec):
    "Multiplies monomials"
    var_list1 = poly.getVarlist()
    coefflst = poly.getCoefflist()[:]
    explst = poly.getexpNonZero()
    for i in range(len(coefflst)):
        coefflst[i] *= coeff
    newvarlist = list(set(var_list1) | set(varlist))
    newvarlist.sort()
    self_vars_positions = []
    #creates a list of locations of (variables in self) in newvarlist
    for i in var_list1:
        self_vars_positions.append(bsearch(newvarlist, i))
    other_vars_positions = []
    #creates a list of locations of (variables in other) in newvarlist
    for i in varlist:
        other_vars_positions.append(bsearch(newvarlist, i))
    newdegree = poly.getDegree() + sum(expvec)
    newvarnum = len(newvarlist)
    newexpnonempty = [] #new list of powers with non zero coeff
    for i in explst:
        newexpnonempty.append([0]*newvarnum)
    for counter,i in enumerate(newexpnonempty):
        for j in range(len(i)):
            if j in self_vars_positions:
                i[j] += explst[counter][j]
            if j in other_vars_positions:
                i[j] += expvec[j]
    coefflst = modifiedgrevlexSort(newexpnonempty, coefflst)
    return Polynomial("",coefflst,newexpnonempty,newvarlist,newdegree)

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

def modifiedgrevlexSort(explst, coefflst):
    """
    Perform insertion sort on the explst. Sorts coefflist accordingly.
    Sorts by grevlex order
    """
    if len(explst) != len(coefflst):
        raise ConflictingInputError
    for i in range(1, len(explst)):
        elt = explst[i]
        elt2 = coefflst[i]
        j = i-1
        # if not at the start of the list and items are out of order
        while (j >= 0) and grevlexhelper(elt,explst[j]):
            explst[j+1] = explst[j]
            coefflst[j+1] = coefflst[j]
            j=j-1
        explst[j+1] = elt
        coefflst[j+1] = elt2
    return coefflst

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
    Returns True if L1 < L2 and False if L1 > L2
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
