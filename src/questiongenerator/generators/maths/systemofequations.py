import sympy
import random

from ..abstractgenerator import AbstractGenerator
from ...base import NumericalQuestion

class SystemOfEquations(AbstractGenerator):
    """docstring for SystemOfEquations."""

    def __init__(self, maxcoef=10, maxsol=10):
        super(SystemOfEquations, self)
        self.maxsol = maxsol
        self.maxcoef = maxcoef

    def _get_coef (self, maxnumber, notvalid=[]):
        """ Returns a random number between  """
        valid_numbers = list(range(-maxnumber, maxnumber + 1))
        for num in notvalid:
            valid_numbers.remove(num)
        return random.choice(valid_numbers)

    def _get_equation(self, valx, valy):
        x, y = sympy.symbols('x y')
        coefx = self._get_coef(self.maxcoef, [0,])
        coefy = self._get_coef(self.maxcoef, [0,])
        left_side = coefx * x + coefy * y
        right_side = left_side.subs(x, valx).subs(y, valy)

        return sympy.Eq(left_side, right_side)

    def get_question(self):
        valx = self._get_coef(self.maxsol, [0,])
        valy = self._get_coef(self.maxsol, [0,])
        eq1 = self._get_equation(valx, valy)
        eq2 = self._get_equation(valx, valy)
        equation = "\\begin{{cases}} {} \\\\ {} \\end{{cases}}".format(sympy.latex(eq1),  sympy.latex(eq2))

        solution = valx * valy

        question_text = self._("Resuelve el siguiente sistema de ecuacioens lineales: {equation} Una vez resuelto, multiplica el valor de x y el de y.")

        args = {
            "equation": ('tex', equation)
        }

        name = self._('Sistema de ecuaciones lineales {}')

        answers = [
            {
                "value": solution,
                "correct": True,
                "feedback": self._("Bien!! :D")
            },
            {
                "value": "*",
                "correct": False,
                "feedback": self._("Revisa este sistema. La solución correcta es {} ya que x={} e y={}").format(solution, valx, valy)
            }
        ]

        return NumericalQuestion(name, question_text, args, answers)
