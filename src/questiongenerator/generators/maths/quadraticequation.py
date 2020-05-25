
import sympy
import random

from ..utils import get_random_number, range_list
from ..abstractgenerator import AbstractGenerator
from ...base import NumericalQuestion

class QuadraticEquation(AbstractGenerator):
    """docstring for QuadraticEquation.

        Args:
            type:
            max_coef:
            max_mult:
            more_terms:
            multiply:
            labels:

    """

    LABELS_DEFAULT = {
        "question-text":  "Resuelve la ecuación de segundo grado {equation}. Si obtienes dos soluciones, multiplícalas.",
        "question-name":  "Ecuación de segundo grado {}",
        "feedback-right": "Bien! :)",
        "feedback-wrong": "Revisa esta ecuación. La/s solución/es correcta/s es/son {solution}"
    }

    def __init__(self, type='complete', max_coef=10, max_mult=5, prob_more_terms=0, prob_multiply=0, labels=LABELS_DEFAULT):
        super(QuadraticEquation, self)
        self.type = type
        self.maxcoef = max_coef
        self.maxmult = max_mult
        self.prob_moreterms = prob_more_terms
        self.prob_mult = prob_multiply
        self.labels = labels

    def __add_terms(self, var, left_side, right_side):

        #Add random x**2 term at both sides
        if random.randint(1, 100) < self.prob_moreterms:
            coeficient = get_random_number(self.maxcoef, [0,])
            left_side += coeficient * var ** 2
            right_side += coeficient * var ** 2

        #Add random x term at both sides
        if random.randint(1, 100) < self.prob_moreterms:
            coeficient = get_random_number(self.maxcoef, [0,])
            left_side += coeficient * var
            right_side += coeficient * var

        #Add random independent term at both sides
        if random.randint(1, 100) < self.prob_moreterms:
            coeficient = get_random_number(self.maxcoef, [0,])
            left_side += coeficient
            right_side += coeficient

        #Multiply both side by a number
        if random.randint(1, 100) < self.prob_mult:
            coeficient = get_random_number(self.maxcoef, [0,])
            left_side = coeficient * left_side
            right_side = coeficient * right_side

        left_side = sympy.expand(left_side)
        right_side = sympy.expand(right_side)
        return sympy.Eq(left_side, right_side)

    def __get_pure_incomplete_equation(self):
        """ Generates a pure incomplete quadratic equation (x^2 + c = 0)."""
        x = sympy.symbols('x')
        root1 = get_random_number(self.maxcoef, [0,])
        left_side = x**2 - root1**2

        return self.__add_terms(x, left_side, 0)

    def __get_mixed_incomplete_equation(self):
        """ Generates a mixed incomplete quadratic equation (ax^2 + bx = 0)."""
        x = sympy.symbols('x')
        root1 = get_random_number(self.maxcoef, [0,])
        exp = (x - root1) * x
        left_side = sympy.expand(exp)

        return self.__add_terms(x, left_side, 0)

    def __get_complete_equation(self):
        """ Generates a complete quadratic equation (ax^2 + bx + c = 0)."""
        x = sympy.symbols('x')
        root1 = get_random_number(self.maxcoef, [0,])
        root2 = get_random_number(self.maxcoef, [0,])
        exp = (x-root1) * (x-root2)
        left_side = sympy.expand(exp)

        return self.__add_terms(x, left_side, 0)

    def __get_equation(self):
        """ Returns an equation. """
        type = self.type

        if self.type == 'random':
            type = random.choice(['complete', 'pureincomplete', 'mixedincomplete'])

        if (self.type == 'pureincomplete'):
            return self.__get_pure_incomplete_equation()
        elif (self.type == 'mixedincomplete'):
            return self.__get_mixed_incomplete_equation()
        else:
            return self.__get_complete_equation()

    def get_question(self):
        eq = self.__get_equation()
        equation = sympy.latex(eq)

        eq_sol = sympy.solve(eq)
        solution = eq_sol[0] if len(eq_sol) == 1 else eq_sol[0] * eq_sol[1]
        solution_text = str(eq_sol[0]) if len(eq_sol) == 1 else str(eq_sol[0]) + ' y ' + str(eq_sol[1])

        args = {
            "equation": ('tex', equation)
        }

        answers = [
            {
                "value": solution,
                "correct": True,
                "feedback": self.labels["feedback-right"]
            },
            {
                "value": "*",
                "correct": False,
                "feedback": self.labels["feedback-wrong"].format(solution=solution_text)
            }
        ]

        return NumericalQuestion(self.labels["question-name"], self.labels["question-text"], args, answers)
