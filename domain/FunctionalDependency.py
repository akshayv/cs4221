__author__ = 'akshay'


class FunctionalDependency:
    lhs_attributes = set()
    rhs_attributes = set()

    def __init__(self, lhs_attributes, rhs_attributes):
        self.lhs_attributes = lhs_attributes
        self.rhs_attributes = rhs_attributes

    def __repr__(self):
        return "[ lhs: " + str(self.lhs_attributes) + ", rhs: " + str(self.rhs_attributes) + "]"