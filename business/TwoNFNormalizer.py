from business.AbstractNormalizer import AbstractNormalizer
from domain.FunctionalDependency import FunctionalDependency
from domain.Relation import Relation

__author__ = 'akshay'


class TwoNFNormalizer(AbstractNormalizer):

    @staticmethod
    def normalize_2_nf(relation):
        requirements = [TwoNFNormalizer.is_trivial, TwoNFNormalizer.is_x_not_proper_subset,
                        TwoNFNormalizer.is_prime_attribute]
        return AbstractNormalizer.normalize(relation, requirements)

if __name__ == "__main__":
    relation = Relation({'a', 'b', 'c', 'd', 'e'},
                        {FunctionalDependency({'a', 'b'}, {'c', 'd', 'e'}), FunctionalDependency({'a'}, {'c'}),
                         FunctionalDependency({'d'}, {'e'})})
    relations = TwoNFNormalizer.normalize_2_nf(relation)
    for relation in relations:
        print relation

