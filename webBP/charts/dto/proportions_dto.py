from enums.prop_formula import PropFormula


class ProportionsDto(object):
    def __init__(self, alpha: float=0.01, title: str=None, x_label: str=None, y_label: str=None,
                 formula: PropFormula=PropFormula.ORIGINAL):
        self.alpha = alpha
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.formula = formula
