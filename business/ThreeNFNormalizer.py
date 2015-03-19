from business.AbstractNormalizer import AbstractNormalizer
from domain.FunctionalDependency import FunctionalDependency
from domain.Relation import Relation

__author__ = 'akshay'


class ThreeNFNormalizer(AbstractNormalizer):

    @staticmethod
    def normalize_3nf(relation):
        requirements = [ThreeNFNormalizer.is_trivial, ThreeNFNormalizer.is_x_superkey,
                        ThreeNFNormalizer.is_prime_attribute]
        return AbstractNormalizer.normalize(relation, requirements)


if __name__ == "__main__":
    relation = Relation({'a', 'b', 'c'},
                        {FunctionalDependency({'a'}, {'b'}), FunctionalDependency({'b'}, {'a'})})
    relations = ThreeNFNormalizer.normalize_3nf(relation)
    for relation in relations:
        print relation
