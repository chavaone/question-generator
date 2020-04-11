
from .abstractquestion import AbstractQuestion

class NumericalQuestion(AbstractQuestion):
    """docstring for Question."""

    def __init__(self, name, format, args, answers):
        super().__init__(name, 'numerical')
        self.question_format = format
        self.question_args = args
        self.answers = answers
