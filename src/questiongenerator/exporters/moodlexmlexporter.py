
class MoodleXMLExporter:
    """Export question to a XML file with Moodle Format."""

    BEGIN_XML = '<?xml version="1.0" ?>\n<quiz>\n'
    END_XML = '</quiz>'

    def __init__ (self, category, importmathjax=False):
        self.category = category
        self.importmathjax = importmathjax

    def _get_xml_category (self):
        "Rerturns XML text for specifying the category."
        return """\t<question type="category">\n\t\t<category>\n\t\t\t<text>$course$/{category}</text>\n\t\t</category>\n\t</question>\n""".format(category = self.category)

    def _format_expander (self, arg):
        if arg[0] == 'tex':
            return '<span class="math display">\(' + arg[1] + '\)</span>'
        return arg[1]

    def _get_questionname (self, name_number, question):
        return '\t\t<name><text>{}</text></name>\n'.format(question.name.format(name_number))

    def _get_questiontext (self, question):
        ret = '\t\t<questiontext format="html">\n\t\t\t<text>\n\t\t\t\t<![CDATA['

        if (self.importmathjax):
            ret += '<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>' \
                   '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3.0.1/es5/tex-mml-chtml.js"></script>'

        args = {k: self._format_expander(question.question_args[k]) for k in question.question_args}
        question_text = question.question_format.format(**  args)
        ret += '<p>' + question_text + '</p>'
        ret += ']]>\n\t\t\t</text>\n\t\t</questiontext>\n'
        return ret

    def _get_questionanswer(self, mark, value, feedback):
        ret =  '\t\t<answer fraction="{}">\n'.format(mark)
        ret += '\t\t\t<text>{}</text>\n'.format(value)
        ret += '\t\t\t<feedback><text>{}</text></feedback>\n'.format(feedback)
        ret += '\t\t</answer>\n'
        return ret

    def _get_xml_numerical (self, name_number, question):
        """ """
        ret  = '\t<question type="numerical">\n'
        ret += self._get_questionname(name_number, question)
        ret += self._get_questiontext(question)

        for answer in question.answers:
            mark = 100 if answer["correct"] else 0
            ret += self._get_questionanswer(mark, answer["value"], answer["feedback"])

        ret += '\t</question>\n'
        return ret

    def _get_xml_question(self, name_number, question):
        """Wrapper function to call different functions depending on the type of question."""
        try:
            method = getattr(self, '_get_xml_' + question.type)
            return method(name_number, question)
        except Exception as e:
            raise

    def export_questions(self, question_list, file):
        file.write(self.BEGIN_XML)
        file.write(self._get_xml_category())
        for num, question in enumerate(question_list):
            file.write(self._get_xml_question(num + 1, question))
        file.write(self.END_XML)
