
import sympy

from ..utils import get_random_number, range_list
from ..abstractgenerator import AbstractGenerator
from ...base import NumericalQuestion

class BiquadraticEquation(AbstractGenerator):
    """
        Generator for biquadratic equations.


        Args:
            max_coef: The terms coeficients will be between -max_coef and +maxcoef. It must be a positive value.
            labels: Labels that should be used in the question. Must containe the keys "question-text", "question-name", "feedback-right" and "feedback-wrong". Question text value must have a format placeholder called "equation" and feeedback-wrong must have a format placeholder called solution_list and other called solution.
    """

    __LABELS_DEFAULT = {
        "question-text":  "Solve this biquadratic equation: {equation}. If there is more than one solution, write the biggest.",
        "question-name":  "Biquadratic equation {}",
        "feedback-right": "Great! :)",
        "feedback-wrong": "Review this equation. The correct solutions were {solution_list} so you should have wrote {solution}."
    }

    def __init__(self, max_coef=10, labels=__LABELS_DEFAULT):
        super(BiquadraticEquation, self)

        if max_coef <= 0:
            raise ValueError("Parameters max_coef must be a positive value.")

        missing_labels = [k for k in self.__LABELS_DEFAULT.keys() if k not in labels]
        if missing_labels:
            raise ValueError("Labels {} are missing.".format(missing_labels))

        self.maxcoef = max_coef
        self.labels = labels


    def __get_equation(self):
        """ Generates a complete quadratic equation (ax^2 + bx + c = 0)."""
        x = sympy.symbols('x')
        perfect_squares = [i**2 for i in range(1, self.maxcoef)]
        root1 = get_random_number(perfect_squares)
        valid_numbers = perfect_squares + [-i for i in range(1, self.maxcoef)]
        root2 = get_random_number(valid_numbers)
        exp = (x-root1) * (x-root2)
        left_side = sympy.expand(exp)
        left_side = left_side.subs(x, x**2)
        return sympy.Eq(left_side, 0)


    def get_question(self):
        eq = self.__get_equation()
        equation = sympy.latex(eq)

        eq_all_solutions = sympy.solve(eq)
        #Pick only real solutions
        eq_real_sols = [i for i in eq_all_solutions if i.is_real]
        solution = max(eq_real_sols)
        solution_list = ", ".join([str(i) for i in eq_real_sols])

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
                "feedback": self.labels["feedback-wrong"].format(solution_list=solution_list, solution=solution)
            }
        ]

        return NumericalQuestion(self.labels["question-name"], self.labels["question-text"], args, answers)
