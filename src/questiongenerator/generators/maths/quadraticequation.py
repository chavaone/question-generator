
import sympy
import random

from ..abstractgenerator import AbstractGenerator
from ...base import NumericalQuestion

class QuadraticEquation(AbstractGenerator):
    """docstring for QuadraticEquation."""

    def __init__(self, type='complete', maxcoef=10, maxmult=5, moreterms=0, multiply=0):
        super(QuadraticEquation, self)
        self.type = type
        self.maxcoef = maxcoef
        self.moreterms = moreterms
        self.multiply = multiply
        self.maxmult = maxmult

    def _get_coef (self, maxnumber, notvalid=[]):
        valid_numbers = list(range(-maxnumber, maxnumber + 1))
        for num in notvalid:
            valid_numbers.remove(num)
        return random.choice(valid_numbers)

    def _add_terms(self, x, left_side, right_side):
        #Multiply both terms by a number
        if not random.randint(0, self.multiply):
            coeficient = self._get_coef(self.maxmult, [0,])
            left_side = coeficient * left_side
            right_side = coeficient * right_side

        #Add random x**2 term at both sides
        if not random.randint(0, self.moreterms):
            coeficient = self._get_coef(self.maxcoef, [0,])
            left_side += coeficient * x ** 2
            right_side += coeficient * x ** 2

        #Add random x term at both sides
        if not random.randint(0, self.moreterms):
            coeficient = self._get_coef(self.maxcoef, [0,])
            left_side += coeficient * x
            right_side += coeficient * x

        #Add random independent term at both sides
        if not random.randint(0, self.moreterms):
            coeficient = self._get_coef(self.maxcoef, [0,])
            left_side += coeficient
            right_side += coeficient

        #Multiply both side by a number
        if not random.randint(0, self.multiply):
            coeficient = self._get_coef(self.maxcoef, [0,])
            left_side = coeficient * left_side
            right_side = coeficient * right_side

        left_side = sympy.expand(left_side)
        right_side = sympy.expand(right_side)
        return sympy.Eq(left_side, right_side)

    def _get_pure_incomplete_equation(self):
        x = sympy.symbols('x')
        root1 = self._get_coef(self.maxcoef, [0,])
        left_side = x**2 - root1**2
        return self._add_terms(x, left_side, 0)

    def _get_mixed_incomplete_equation(self):
        x = sympy.symbols('x')
        root1 = self._get_coef(self.maxcoef, [0,])
        exp = (x - root1) * x
        left_side = sympy.expand(exp)

        return self._add_terms(x, left_side, 0)

    def _get_complete_equation(self):
        x = sympy.symbols('x')
        root1 = self._get_coef(self.maxcoef, [0,])
        root2 = self._get_coef(self.maxcoef, [0,])
        exp = (x-root1) * (x-root2)
        left_side = sympy.expand(exp)

        return self._add_terms(x, left_side, 0)

    def _get_equation(self):
        """ Returns an equation. """
        type = self.type

        if self.type == 'random':
            type = random.choice(['complete', 'pureincomplete', 'mixedincomplete'])

        if (self.type == 'pureincomplete'):
            return self._get_pure_incomplete_equation()
        elif (self.type == 'mixedincomplete'):
            return self._get_mixed_incomplete_equation()
        else:
            return self._get_complete_equation()

    def get_question(self):
        eq = self._get_equation()
        equation = sympy.latex(eq)

        eq_sol = sympy.solve(eq)
        solution = eq_sol[0] if len(eq_sol) == 1 else eq_sol[0] * eq_sol[1]

        question_text = self._("Resuelve la ecuación de segundo grado {equation}. Si obtienes dos soluciones, multiplícalas.")

        args = {
            "equation": ('tex', equation)
        }

        name = self._('Ecuación de segundo grado {}')

        answers = [
            {
                "value": solution,
                "correct": True,
                "feedback": self._("Bien!! :D")
            },
            {
                "value": "*",
                "correct": False,
                "feedback": self._("Revisa esta ecuación. La/s solución/es de esta ecuación es/son {}").format(str(eq_sol[0]) if len(eq_sol) == 1 else str(eq_sol[0]) + ' y ' + str(eq_sol[1]))
            }
        ]

        return NumericalQuestion(name, question_text, args, answers)
