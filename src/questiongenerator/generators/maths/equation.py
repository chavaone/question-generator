import sympy
import random

from ..abstractgenerator import AbstractGenerator
from ...base import NumericalQuestion

class LinearEquation(AbstractGenerator):
    """docstring for LinearEquation."""

    def __init__(self, type, max_coef=10, max_sol=10, num_left_terms=0, num_right_terms=0):
        super(LinearEquation, self)
        self.maxcoef = max_coef
        self.maxsol = max_sol
        self.lterms = num_left_terms
        self.rterms = num_right_terms
        self.type = type

    def _get_random_number (self, include, exclude=[]):
        """ Returns a random number.
            The number is chosen from the include list excluding numbers from exclude list.
        """
        include_num = list(include)
        for num in exclude:
            try:
                include_num.remove(num)
            except ValueError:
                continue
        return random.choice(include_num)

    def _range(self, a, b=None):
        """ Return the range list between a and b """
        if b is None:
            return list(range(-a,a))
        return list(range(a,b))

    def _get_simple_term(self, var):
        """ Return a tuple with a random term and its sign.
            var -- variable to use or false if its an independent term
        """
        coeficient = self._get_random_number(self._range(1, self.maxcoef))
        term = coeficient * var if var else coeficient
        return (term, random.getrandbits(1))

    def _get_parentesis_term(self, var):
        """ Return a term with the form "a * (b * var + c)" where a, b and c are random numbers."""
        a = self._get_random_number(self._range(1, self.maxcoef))
        b = self._get_random_number(self._range(self.maxcoef), [0,])
        c = self._get_random_number(self._range(self.maxcoef), [0,])
        term = sympy.Mul(a, b * var + c, evaluate=False)
        return (term, random.getrandbits(1))

    def _get_fraction_term(self, var):
        """ Return a term with an division. """
        num, _ = self._get_term(var, type='parentesis')
        den = self._get_random_number(self._range(1, self.maxcoef))
        with sympy.evaluate(False):
            term = (num)/(den)
        return (term, random.getrandbits(1))

    def _get_term(self, var=False, type='simple'):
        if not var:
            return (self._get_random_number(self._range(1, self.maxcoef)), random.getrandbits(1))

        if type == 'random':
            type = random.choice(['simple', 'parentesis'])

        if (type == 'parentesis'):
            return self._get_parentesis_term(var)
        elif (type == 'fraction'):
            return self._get_fraction_term(var)
        else:
            return self._get_simple_term(var)

    def _get_exp(self, exp_terms, exp_signs):
        """ Returns the SymPy expression obtained from the list of terms and signs passed as parameter."""
        assert(len(exp_terms) == len(exp_signs))
        assert(exp_terms)
        assert(exp_signs)

        terms = list(exp_terms)
        signs = list(exp_signs)

        term = terms.pop(0)
        sign = signs.pop(0)

        exp = + term if sign else - term

        while (terms):
            term = terms.pop(0)
            sign = signs.pop(0)

            exp = exp + term if sign else exp - term
        return exp

    def _get_equation(self):
        """Returns a dictionary formed by the right side of an equation, the left side of this equation and its solution."""
        x, y = sympy.symbols('x y')
        term, sign = self._get_term(x, self.type)
        rs_terms = [term,]
        rs_signs = [sign,] #List of signs for each term: True if + False if -
        ls_terms = [y,]
        ls_signs = [True,]

        for _ in range(self.lterms):
            term, sign = self._get_term(x, self.type) if random.getrandbits(1) else self._get_term()
            ls_terms.append(term)
            ls_signs.append(sign)

        for _ in range(self.rterms):
            term, sign = self._get_term(x, self.type) if random.getrandbits(1) else self._get_term()
            rs_terms.append(term)
            rs_signs.append(sign)

        rs = self._get_exp(rs_terms, rs_signs)
        ls = self._get_exp(ls_terms, ls_signs)
        eq = sympy.Eq(rs,ls)
        sol = self._get_random_number(self._range(-self.maxsol, self.maxsol))
        eq = eq.subs(x, sol)
        soly = sympy.solve(eq)[0]
        ls_terms[0] =  abs(soly)
        ls_signs[0] =  soly >= 0

        return {
            "rs": (rs_terms, rs_signs),
            "ls": (ls_terms, ls_signs),
            "sol": sol
        }

    def _get_latex(self, expression):
        """ Returns the latex string corresponding to a list of terms and signs."""
        terms = list(expression[0])
        signs = list(expression[1])

        term = terms.pop(0)
        sign = signs.pop(0)

        ret = "" if sign else "-"
        ret += sympy.latex(term)

        while terms:
            term = terms.pop(0)
            sign = signs.pop(0)

            ret += " + " if sign else " - "
            ret += sympy.latex(term)
        return ret

    def get_question(self):
        """ Returns a NumericalQuestion with a simple first degree equation."""

        eq = self._get_equation()

        equation = self._get_latex(eq["rs"]) + " = " + self._get_latex(eq["ls"])

        question_text = self._("Resuelve la siguiente ecuación de primer grado: {equation}")

        args = {
            "equation": ('tex', equation)
        }

        name = self._('Ecuación de primer grado {}')

        answers = [
            {
                "value": eq["sol"],
                "correct": True,
                "feedback": self._("Bien!! :D")
            },
            {
                "value": "*",
                "correct": False,
                "feedback": self._("Revisa esta ecuación. La solución correcta es {}").format(eq["sol"])
            }
        ]

        return NumericalQuestion(name, question_text, args, answers)
