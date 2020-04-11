
import gettext

class AbstractGenerator:
    """docstring for AbstractGenerator."""

    def __init__(self, ):
        gettext.bindtextdomain('question-generator', '/path/to/my/language/directory')
        gettext.textdomain('question-generator')

    def _(self, s):
        return gettext.gettext(s)

    def get_question():
        pass
