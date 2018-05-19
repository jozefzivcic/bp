from enums.prop_formula import PropFormula


class PropOptions(object):
    def __init__(self, formula: PropFormula):
        self.formula = formula

    def __repr__(self) -> str:
        return '<formula: "{}">'.format(repr(self.formula))
