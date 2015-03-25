__author__ = 'akshay'

class Key:
    attributes = set()

    def __init__(self, attributes):
        self.attributes = attributes


    def __repr__(self):
        s = str(self.attributes).replace("set(['", "").replace("'])", "").replace("', '", ",")
        s = s.replace("set([u'", "").replace("', u'", ",")
        return s

    def __len__(self):
        return len(self.attributes)

if __name__ == "__main__":
    k = Key({u'A', u'B', u'C'})
    print k