
from PyQt5 import QtGui as qtg



class DateValidator(qtg.QValidator):
    '''Enforce entry of Date'''

    # Here we indicate the conditions that the search line must follow
    def validate(self, string, index):
        octets = string.split(':')
        # indicates that '-' cannot be deleted
        if len(octets) != 2:
            state = qtg.QValidator.Invalid
        # all symbols must me integers
        elif not all([x.isdigit() for x in octets if x != '']):
            state = qtg.QValidator.Invalid
        # year  must be before current year
        elif octets[0] and (
                (int(octets[0][0]) > 3 or int(octets[0][0]) < 0) or (int(octets[0]) >= 24 or int(octets[0]) < 0)):
            state = qtg.QValidator.Invalid
        # month must be from 1 to 12
        elif octets[1] and octets[1][0] and (
                (int(octets[1][0]) > 5 or int(octets[1][0]) < 0) or (int(octets[1]) >= 60 or int(octets[1]) < 0)):
            state = qtg.QValidator.Invalid
        else:
            state = qtg.QValidator.Acceptable
        return (state, string, index)
