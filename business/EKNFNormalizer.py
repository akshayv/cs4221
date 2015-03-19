from business.AbstractNormalizer import AbstractNormalizer
from domain.FunctionalDependency import FunctionalDependency
from domain.Relation import Relation

__author__ = 'akshay'


class EKNFNormalizer(AbstractNormalizer):

    @staticmethod
    def normalize_eknf(relation):
        requirements = [EKNFNormalizer.is_trivial, EKNFNormalizer.is_x_superkey,
                        EKNFNormalizer.is_elementary_prime_attribute]
        return AbstractNormalizer.normalize(relation, requirements)


if __name__ == "__main__":
    relation = Relation({'a', 'b', 'c'},
                        {FunctionalDependency({'a'}, {'b'}), FunctionalDependency({'b'}, {'a'})})
    relations = EKNFNormalizer.normalize_eknf(relation)
    for relation in relations:
        print relation