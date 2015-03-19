from business.AbstractNormalizer import AbstractNormalizer
from domain.FunctionalDependency import FunctionalDependency
from domain.Relation import Relation

__author__ = 'akshay'


class BCNFNormalizer(AbstractNormalizer):
    @staticmethod
    def normalize_bcnf(relation):
        requirements = [BCNFNormalizer.is_trivial, BCNFNormalizer.is_x_superkey]
        return AbstractNormalizer.normalize(relation, requirements)


if __name__ == "__main__":
    relation = Relation({'a', 'b', 'c', 'd', 'e', 'f', 'g'},
                        {FunctionalDependency({'a'}, {'b'}), FunctionalDependency({'a'}, {'c'}),
                         FunctionalDependency({'b'}, {'c'}), FunctionalDependency({'b'}, {'d'}),
                         FunctionalDependency({'d'}, {'b'}), FunctionalDependency({'a', 'b', 'e'}, {'f'}),
                         FunctionalDependency({'e', 'a'}, {'d'})})
    relations = BCNFNormalizer.normalize_bcnf(relation)
    for relation in relations:
        print relation
