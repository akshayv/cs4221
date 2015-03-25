from business import create_db
from business.BCNFNormalizer import BCNFNormalizer
from business.EKNFNormalizer import EKNFNormalizer
from business.ThreeNFNormalizer import ThreeNFNormalizer
from business.TwoNFNormalizer import TwoNFNormalizer
from domain.FunctionalDependency import FunctionalDependency
from domain.Relation import Relation

__author__ = 'akshay'


def normalize_relation(relation, normal_form):
    if str(normal_form).lower() == "3nf":
        return ThreeNFNormalizer.normalize_3nf(relation)
    elif str(normal_form).lower() == "2nf":
        return TwoNFNormalizer.normalize_2_nf(relation)
    elif str(normal_form).lower() == "eknf":
        return EKNFNormalizer.normalize_eknf(relation)
    elif str(normal_form).lower() == "bcnf":
        return BCNFNormalizer.normalize_bcnf(relation)
    else:
        raise Exception("Not Supported")

def create_schema(relations, attribute_types, username, password):
    create_db.create_schema(relations, attribute_types, username, password)

if __name__ == "__main__":
    relation = Relation({'a', 'b'},
                        {FunctionalDependency({'a'}, {'b'}), FunctionalDependency({'a'}, {'c'})})
    relations = normalize_relation(relation, "2nf")
    for relation in relations:
        print relation

    # normalize_relation(relation, "4nf")
