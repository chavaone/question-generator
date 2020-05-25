
import sympy

from ..utils import get_random_number, range_list
from ..abstractgenerator import AbstractGenerator
from ...base import NumericalQuestion

class SystemOfEquations(AbstractGenerator):
    """docstring for SystemOfEquations."""

    __LABELS_DEFAULT = {
        "question-text":  "Solve next system of equations: {equation} Then, multiply x value by the y value.",
        "question-name":  "System of equations {}",
        "feedback-right": "Great!",
        "feedback-wrong": "Check this system of equations. Its solution is {solution} because x={x} and y={y}."
    }

    def __init__(self, max_coef=10, max_sol=10, labels=__LABELS_DEFAULT):
        super(SystemOfEquations, self)
        self.maxsol = max_sol
        self.maxcoef = max_coef
        self.labels = labels

    def __get_equation(self, valx, valy):
        x, y = sympy.symbols('x y')
        coefx = get_random_number(self.maxcoef, [0,])
        coefy = get_random_number(self.maxcoef, [0,])
        left_side = coefx * x + coefy * y
        right_side = left_side.subs(x, valx).subs(y, valy)

        return sympy.Eq(left_side, right_side)

    def get_question(self):
        valx = get_random_number(self.maxsol, [0,])
        valy = get_random_number(self.maxsol, [0,])
        eq1 = self.__get_equation(valx, valy)
        eq2 = self.__get_equation(valx, valy)
        equation = "\\begin{{cases}} {} \\\\ {} \\end{{cases}}".format(sympy.latex(eq1),  sympy.latex(eq2))

        solution = valx * valy

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
                "feedback": self.labels["feedback-wrong"].format(solution=solution, x=valx, y=valy)
            }
        ]

        return NumericalQuestion(self.labels["question-name"], self.labels["question-text"], args, answers)
