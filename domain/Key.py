__author__ = 'akshay'

class Key:
    attributes = set()

    def __init__(self, attributes):
        self.attributes = attributes


    def __repr__(self):
        return str(self.attributes)

    def __len__(self):
        return len(self.attributes)