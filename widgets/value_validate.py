
from PyQt5 import QtGui as qtg



class ValueValidator(qtg.QValidator):
    '''Enforce entry of Date'''

    # Here we indicate the conditions that the search line must follow
    def validate(self, string, index):
        if string and (int(string) > 60 or int(string) < 0):
            state = qtg.QValidator.Invalid
        else:
            state = qtg.QValidator.Acceptable
        return (state, string, index)
