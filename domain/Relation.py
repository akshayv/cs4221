__author__ = 'akshay'


class Relation:
    attributes = set()
    functional_deps = []
    keys = set()
    elementary_keys = set()
    primary_key = None

    def __init__(self, attributes, functional_deps):
        self.attributes = attributes
        self.functional_deps = functional_deps

    def __repr__(self):
        return "Relation = [primary_key: " + str(self.primary_key) + ", attributes: " + str(
            self.attributes) + ", functional_deps: " + str(self.functional_deps) + " ]"