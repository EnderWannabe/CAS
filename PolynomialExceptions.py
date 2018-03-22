
class PolynomialException(Exception):
    """Base class"""
    pass

class InsufficientInputError(PolynomialException):
    #Exception for when input is not sufficient to construct polynomial
    pass

class ConflictingInputError(PolynomialException):
    #Exception for when the input is conflicting
    pass

class TooManyVariables(PolynomialException):
    #Exception for when trying to solve an equation with >1 variables
    pass
